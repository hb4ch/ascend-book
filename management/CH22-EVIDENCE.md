# CH22 EVIDENCE——HIXL 单边通信研究账本

日期：2026-10-09　仓库：`/mnt/SATASSDEXT4/cann/hixl`　commit：`9ed283b27309463ed0faa490b79c0dc9ddef6377`（SOURCE-BASELINE 固定值，`git log --oneline -1`＝`9ed283b 切换CCE集群` 实核）
标注：**C**=源码直接事实（文件:行号）／**D**=仓内文档陈述／**I**=本书推导／**U**=未证/未核。本轮不运行硬件、不下载；所有运行性结论标〔需真机验证〕。

## 0. 定位一段话

HIXL（Huawei Xfer Library）= 昇腾**单边**通信库：本地内存就绪后单边发起对端内存读/写，公开 API 精简（`hixl.h` 全部公开方法 15 个）〔C〕；下层区分**通信域 legacy 路径（version=0，HCCL 域）与 HIXL CS 自有路径（version=1，解耦通信域）**〔C：examples/cpp/hixl_example_d2rd.cpp L26/L115-146〕，再按 endpoint 协议×placement 路由到 DIRECT/UB 两类 handler〔C：endpoint_matcher.cc L33-58〕。LLM-DataDist 是**仓内另一上层库**（KV Cache 语义），不是 HIXL API 的别名〔C：src/llm_datadist 独立目录＋include/llm_datadist/llm_datadist.h〕。

## 1. 主锚点（文件级 5 个）

| # | 文件 | 角色 |
|---|---|---|
| A1 | `include/hixl/hixl.h`（194 行）＋`include/hixl/hixl_types.h`（110 行） | 公开 API/类型/错误码全量（§2） |
| A2 | `examples/cpp/hixl_example_quickstart.cpp` | 生命周期主线样例：双 engine（client dev0/server dev2）＋socket 交换地址＋READ 验证（§3） |
| A3 | `src/hixl/engine/hixl_impl.cc`（439 行）＋`hixl_engine.cc`（433 行） | Initialize/Finalize/Transfer* 的引擎层真相（§4.1） |
| A4 | `src/hixl/cs/hixl_cs_client.cc`（1300+ 行）＋`engine/direct_client_handler.cc`＋`ub_client_handler.cc` | 传输真身：Device 内核 chunked 路径/Host 路径/完成查询/失败 latch（§4.2） |
| A5 | `src/hixl/engine/endpoint_matcher.cc` L28-58＋`client_handler_factory.cc` | 协议×placement→handler 路由表（§5） |

辅助：`docs/zh/api/cpp/HIXL-interface.md`（接口约束 D）、`docs/zh/FabricMem.md`（D）、`src/hixl/fabric_mem/*`（C）、`benchmarks/{README.md,performance.md}`（D 口径）、`include/llm_datadist/llm_datadist.h`＋`src/llm_datadist`（C）、`examples/cpp/README.md`（运行矩阵 D）。

## 2. 公开 API 全量签名〔C：hixl.h L46-187〕

```cpp
Status Initialize(const AscendString &local_engine, const std::map<AscendString,AscendString> &options);
void Finalize();
Status RegisterMem(const MemDesc &mem, MemType type, MemHandle &mem_handle);   // MEM_DEVICE|MEM_HOST
Status DeregisterMem(MemHandle mem_handle);
Status Connect/ConnectAsync(const AscendString &remote_engine, int32_t timeout_in_millis=1000);
Status Disconnect/DisconnectAsync(...);   // 异步态 7 值：AsyncConnectStatus{NOT_CONNECT..DISCONNECTING}
Status GetAsyncConnectStatus(单/批量重载);
Status TransferSync(remote_engine, TransferOp operation/*READ|WRITE*/,
                    const std::vector<TransferOpDesc> &op_descs, int32_t timeout_in_millis=1000);
Status TransferAsync(..., const TransferArgs &optional_args, TransferReq &req);   // TransferReq=void*
Status GetTransferStatus(const TransferReq, TransferStatus&);   // WAITING|COMPLETED|TIMEOUT|FAILED
Status GetTransferStatus(const GetTransferStatusArgs{max_query_count,skip_waiting}, std::vector<TransferResult>&);
Status SendNotify(remote_engine, const NotifyDesc{name,notify_msg}, timeout);
Status GetNotifies(std::vector<NotifyDesc> &notifies);          // 取走并清空（doc L896 区语义见 §6）
static Status GetCapability(FeatureType/*AUTO_CONNECT|CLIENT_SERVER_COMM*/, int32_t &value);
```

关键类型〔C：hixl_types.h〕：`MemDesc{addr,len,reserved[128]}`、`TransferOpDesc{local_addr,remote_addr,len}`、`TransferResult{req,user_data,status,reserved[108]}`；错误码 `SUCCESS=0/PARAM_INVALID=103900/TIMEOUT=103901/NOT_CONNECTED=103902/ALREADY_CONNECTED=103903/NOTIFY_FAILED/UNSUPPORTED/FAILED=503900/RESOURCE_EXHAUSTED=203900`。options 七常量：`EnableUseFabricMem/RdmaTrafficClass/RdmaServiceLevel/BufferPool/GlobalResourceConfig/AutoConnect/LocalCommRes`〔C L38-44〕。

**方向语义（公开层）**〔C：hixl.h L125-131 注＋D：interface《TransferSync》〕：`READ`=将远端内存读到本地（local=目的），`WRITE`=本地写往远端（local=源）——**调用端永远是发起方；读写方向决定谁是数据源**。远端 addr 必须已在**远端 HIXL** 注册、本地 addr 在本地注册〔D：interface《RegisterMem》L372「TransferSync 指定的地址可以为注册地址子集」〕。**单边≠对端无准备**：对端须先注册内存＋（CS 路径）server 进程存活；quickstart 注释原文「先申请、填充并注册本地内存，再经 socket 交换地址，避免未注册地址被 client 提前使用」〔C：quickstart L180〕。

## 3. 生命周期主线（A2 quickstart 逐步，全部 C）

0. **进程模型（rev2 订正：非单进程双角色）**：`main`（L201-224）仅接受 `--role=client|server`，分别进 `RunClient()/RunServer()`——**双进程两终端**：server 终端 `--role=server`（dev2 先起），client 终端 `--role=client`（dev0）；engine 名 `127.0.0.1:16000/16001`。**不得用 d2rd 命令冒充本样例。**
2. **Initialize**：`aclrtSetDevice` 后 `opts[OPTION_GLOBAL_RESOURCE_CONFIG]={"comm_resource_config.protocol_desc":["hccs:device"]}`→`engine.Initialize(local,opts)`〔L76-78〕。
3. **Client 侧次序（rev2 订正）**：`PrepareClientMemAndOp`＝malloc＋填 desc＋**先 ExchangeAddr(true) 收远端地址（L146，位于 PrepareClientMemAndOp 内）→后 RegisterMem（L159）**〔RunClient L155-159 区〕。
4. **Server 侧次序（rev2 订正）**：malloc＋H2D 填 0x5A（L181-185）→**先 RegisterMem（L187）→后 ExchangeAddr(false) 发自身地址（L191）**；注释原文「先申请、填充并注册本地内存，再经 socket 交换地址，避免未注册地址被 client 提前使用」〔L180〕。两端镜像，**不可写成同序或说反**。交换通道＝自写 TCP socket（port 17001）传 `uintptr_t`，HIXL 不提供该通道〔C〕。
5. **建链/传输**：client `Connect`（L162）→`TransferSync(READ)`（L163）→`VerifyData`（L165）。
6. **传输**：client `TransferSync(READ,{op{local,remote,len}},5000)`——**从 server buffer 读回**〔L163〕；server 侧只注册+填充不调用传输（`TransferOpDesc op; // Server 不使用` L71）。
7. **校验**：`aclrtMemcpy` D2H 后比对 `0x5A`〔`VerifyData` L132-140 区〕——样例自带正确性验证（对比 ch21 样例只打印）。
8. **收尾时序（rev2 订正）**：client **先 send done（L167）后 Disconnect（L168）**；server `recv done`（L194）后**立即** Finalize（L197；helper L120-137）（helper：close fd→DeregisterMem→free→engine.Finalize→ResetDevice），**无等待同步**。
9. **Finalize 等待断链真相**：`HixlCSServer::Finalize`（hixl_cs_server.cc L273-320）＝停 listener/join→msg_handler_.Finalize→endpoint_store_.Finalize→free flag→TransferPool::Finalize——**不遍历 clients_、不等任何 client**；client 断链靠 epoll 关闭事件→`CleanupClient`（L586-605）异步清。⇒ recv done 即 Finalize 与 client 随后 Disconnect 并发，**存在收尾窗口**（msg_handler 已 Finalize 后到达的 DestroyChannelReq 处置未证〔U〕）；样例靠 done→Disconnect 紧邻时序经验性错开，**正文不得宣称该样例满足全部接口顺序约束**。
10. **顺序约束（D：interface Finalize 节 L363-365）**：Finalize 前断链＋解注册/Server 等所有 Client/读写未完勿动地址——文档义务；样例靠时序而非显式同步满足〔I〕。

DeregisterMem 边界〔D：interface L440〕：重复 dereg 第一次实际释放后续 SUCCESS 空转；非本库 handle 非 null→SUCCESS 空转；null→`PARAM_INVALID`。

## 4. 引擎层与传输真身

### 4.1 引擎层（A3，C）

- `HixlImpl::Initialize`：`EngineFactory::CreateEngine(local_engine,options,parsed_options)`→`engine_->Initialize`→`connect_pool_executor_.Initialize`；失败回滚 `engine_->Finalize()`〔hixl_impl.cc L82-99〕。`Finalize`：pool Shutdown→engine Finalize→reset〔L101-110〕。
- `RegisterMem`→`engine_->RegisterMem`→**server_.RegisterMem + client 侧同步**（hixl_engine.cc L103-110 区：server 注册＋广播给已连 client——本书未见广播体细节，标注 U：client 侧刷新机制未逐行）。
- `TransferSync`（hixl_engine.cc L193-215；impl 转发层 TransferAsync=hixl_impl.cc L194）：`AutoConnect`（链路池按需建链）→`client_ptr->TransferSync(...)`；**失败→`AutoDisconnect` 后返回错误**（引擎级自动断链；传输级重试见 rev2 §13.4）。`TransferAsync` L217-240：同 AutoConnect（固定 `kAutoConnectTimeout`）＋`client_manager_.RegisterTransferReq(req,client_ptr,user_data)`——req↔client 绑定记录在 manager。
- `GetTransferStatus` 单/批：转发 client；批版按 `max_query_count/skip_waiting` 过滤〔L241-290 区〕。

### 4.2 handler/CS 层（A4，C）

- **两类 handler**〔client_handler_factory.cc L17-31〕：`DIRECT`（DirectClientHandler）与 `UB`（UbClientHandler）；选择由 §5 路由表定。
- **DirectClientHandler**（direct_client_handler.cc）：薄封装→`HixlCSClient*`（include/cs/hixl_cs.h L173-216 C API：`BatchPutAsync/BatchGetAsync/BatchPutSync/BatchGetSync/QueryCompleteStatus`）；WRITE→Put、READ→Get；async 记 `complete_handles_[req]`；查询经 `HixlCSClientQueryCompleteStatus`，**查询返回 FAILED 时删 handle**（L128-138）。
- **Device 内存路径**（hixl_cs_client.cc `BatchTransferDeviceAsync` L852-906）：校验→`AcquireSharedSlot`（TransferPool 槽）→`AllocateHostFlag`→`DeviceCompleteHandle{magic,shared_slot,host_flag,dev_op_desc_buf}`→**desc 列表 H2D 拷到 device**→`LaunchDeviceChunkedKernels`（L720-737：按 `kMaxKernelBatchSize` 分块；`need_notify_wait=(chunk_end%kNotifyWaitTaskInterval==0)||末块`）→`aclrtMemcpyAsync(host_flag←dev_const_one,D2H,stream)`——**完成判定=host flag 可读，由 device kernel 内 notify 置位**（kernel 细节 U：未逐行核 load_kernel/设备侧）。
- **Host 内存路径**（`BatchTransferHostAsync` L508+）：分块 `BatchTransferTask`＋flag 队列 `AcquireFlagIndex`；**flag 耗尽→`RESOURCE_EXHAUSTED`，错误消息原文要求先查询已完成任务再新建**（L521-527）——并发上限的显式机制〔C〕。
- **失败 latch**：`ShouldLatchTransferFailure(FAILED||TIMEOUT)`→`transfer_failure_latched_`（L738-757 区）——复位/重试/重建全链**已在 rev2 §13.4 核清（复位唯一点=L339 Create）**。
- **RDMA 重试 env**：`HCCL_RDMA_RETRY_CNT/HCCL_RDMA_TIMEOUT` 解析与合法域〔L1250-1266〕；doc 给出配置公式（timeout=log2(超时µs/(RETRY+1)/4.096) 向上取整，默认建议 15）〔D：interface 环境变量表 L62〕——**这是网卡级重试，不是传输级重试**〔I〕。
- **notify 资源**（`InitNotifyResources` L317-335）：仅 device endpoint；**非 HCCS 协议才 `ResolveNotifyAddr`；非 ROCE/HCCS 才注册 notify 内存**——协议分支实证。

### 4.3 同步/异步/可复用语义（C+D）

- `TransferSync` 阻塞至完成或 timeout；返回 `NOT_CONNECTED（未建链且未开链路池）/TIMEOUT/RESOURCE_EXHAUSTED`〔D：interface 返回值表〕。
- 异步：**`GetTransferStatus` 查得 COMPLETED/FAILED 即释放相关资源，该 req 不支持再查**〔D：interface L896/L941 原文〕——**「查询即消费」语义，I：意味着调用方须自行保存结果后再丢弃 req**。
- buffer 复用：doc 未给「传输完成后源缓冲可改写」的显式承诺；可引用的只有 sync 返回/async COMPLETED（D 缺失处 I 保守推断：同步返回后本地缓冲才可确信可复用；异步须 COMPLETED）。

## 5. 路由矩阵：协议×placement→handler（A5，C）

`endpoint_matcher.cc L33-58 两张静态表`（reason 字段原文）：

- **同 instance**：UB group（`COMM_TYPE_UB_D2D`）→ HCCS device → UBoE device → UB_RTP device → RoCE device → RoCE host。
- **跨 instance**：UBoE device → UB_RTP device（fallback）→ RoCE device → RoCE host。

**平台条件（D：examples/cpp/README.md L129 参数表）**：`hccs:device/roce:device` 仅 A2/A3；`uboe/ub_rtp/ub_ctp(:device/:host)` 仅 950PR/DT——**从配置参数与匹配表双源印证，非文件名推断**。`version=0`（legacy）**只支持 `roce:device`＋HCCL 通信域路径**（`HCCL_INTRA_ROCE_ENABLE=1`＋`OPTION_LOCAL_COMM_RES "1.2"`，hixl_example_d2rd.cc L115-146）；`version=1`=HIXL CS 解耦通信域，A2/A3/950 全支持〔D：同表 `--version` 行〕。A5：LLM-DataDist 样例只支持 hixl CS 后端、默认 UB 协议〔D：examples/cpp/README L61 区〕。

## 6. 内存注册经济学与中转（C+D）

- **前置**：Connect 前须完成全部 local 注册〔D：interface RegisterMem 约束〕。
- **上限（D：interface L406-414 区，A2/A3 限定块）**：建议单实例注册数≤4K（多则建链慢/OOM 风险）；Device 内存≤50GB；Host 内存 HDK<25.5 →20GB、≥25.5→1TB。
- **重复注册**：同 addr+len→返回原 handle 不建新资源〔D L372〕。
- **中转 buffer**：`OPTION_BUFFER_POOL`＝`"${NUM}:${SIZE}"` 默认 `4:8`(MB)，`0:0` 关闭；用途=RDMA Host 注册受限/小块（如 128K）中转提频；**与 `EnableUseFabricMem` 互斥**；A2 限定：800I A2/A200I A2 Box 的 Server HCCS 仅 D2D〔D：interface L94 原文〕——**「零拷贝」非无处不在：中转路径存在且默认开启**〔I〕。
- **零拷贝真实含义**：直传路径用户内存→用户内存无中转拷贝（README D＋DIRECT handler 直传 op_desc）；FabricMem/UB/中转路径各有不同机制，**不得把「零拷贝」写成库级保证**〔I〕。

## 7. FabricMem 专题（D+C）

- **背景**（docs/zh/FabricMem.md D）：A3 超节点 DRAM 统一编址，RoCE ~20GB/s 瓶颈→FabricMem 百 GB 级；D2RH/RH2D 双向；CPU 零介入。
- **机制**（D，同页）：CANN VMM——`aclrtMallocPhysical`→`aclrtReserveMemAddress`→`aclrtMapMem`；物理地址交换；映射页表；**SDMA 直接读写任意进程片上/DRAM 内存**。
- **代码**（C）：`fabric_mem_d2d.cpp` L52 `options[OPTION_ENABLE_USE_FABRIC_MEM]="1"`；L133-142 三 ACL 调用实证；`src/hixl/fabric_mem/`24 文件（aicpu dispatcher/transfer service/allocator/slot_pool/virtual_memory_manager…——内部分支未逐行，U：仅目录级＋入口已核）。
- **配置**（D：interface FabricMem 块）：`fabric_memory.max_capacity`（(0,1024] 整数 TB 默认 32）等 `fabric_memory.*`；仅 A3；**与 BUFFER_POOL 互斥**〔D L94〕；HDK 25.5 Host 内存须 `AdxlEngine::MallocMem/FreeMem`，26.0+ 可直接 ACL〔D interface L425〕。

## 8. LLM-DataDist：另一层，不与 HIXL API 混写（C）

- 独立头 `include/llm_datadist/llm_datadist.h`：`LLMDataDist(role,cluster_id)`、`init(LLMConfig)`、`SetLlmRole`（**role 仅标识，对传输无影响**——D：interface L36）、`LinkLlmClusters/UnlinkLlmClusters(force_flag)`、`AllocateCache/CacheDesc{placement:kDevice…}`、`PullKvCache/PullKvBlocks/PushKvCache/PushKvBlocks(batch_index)`；错误码段 `0x5010B0xx`（LLM_NOT_YET_LINK/LLM_LINK_BUSY…）〔C L46-63〕——**链接态机显式成错误码族**。
- 实现 `src/llm_datadist/`：adxl/cache_mgr/comm_adapter/data_transfer/fsm…；`OPTION_TRANSFER_BACKEND="hixl"` 切 HIXL CS 后端，默认 adxl/HCCL 后端〔D：LLM-DataDist-interface L104＋examples README〕。
- 样例成对运行（prompt/decoder 双进程、WAIT_TIME 5s/10s）〔D：examples/cpp/README L55-56〕；python 侧 `HCCL_INTRA_ROCE_ENABLE=1 python llm_datadist/pull_cache_sample.py --device_id .. --cluster_id ..`〔D：examples/python/README L80-82〕。
- 生态对接（Mooncake/SGLang/vLLM/NIXL/TENT）＝**仓外上层**，本书只述「HIXL 作为其传输后端」〔D：README News/博客；不展开外部仓内部〕。博客 `sglang_mooncake_hixl_pd_separation_d2d`（76 行）/`hixl_fabricmem_kv_cache_transfer`（82 行）为场景叙述，无新 API〔D〕。

## 9. benchmark 口径与已知数字（D；本书不实测）

- **口径**（benchmarks/README.md＋performance.md）：总数据 128MiB；block 16K→2M 梯；方向命名 `源→远端`（**D=Device,H=Host,r=remote**；D2rD=initiator device write→remote device 等 8 列）；A3 表按 FabricMem（AICPU 展开/Host 展开 4 流）→ROCE→HCCS、各分 hixl_cs/通信域；A2 表仅 ROCE/HCCS。
- **代表值（D，引用须带全部条件）**：A3 FabricMem AICPU 展开 D2rD：16K=16.113→1M=170.514 GB/s（峰值区 512K=170.724）；Host 展开 4 流 16K=2.874。README 概述：A3 128M HCCS 119GB/s、RDMA 22GB/s。
- **工具**：`hixl_comm_bench --role=initiator --device_id --local/remote_engine --memory --remote_memory --op --transport --transfer_size --block_sizes --loops`；`run_all_bench.sh 仅单机`，双机 `run_comm_benchmark.py --role=target|initiator`〔D README L118〕。
- 本书性能章职责：**引用口径与条件，不新造数据**；无硬件不运行〔U→本轮不运行〕。

## 10. 与邻章边界／HCOMM SymWin 对照（I，承 ch21 §7.6）

- ch21 SymWin=HCOMM 通信域内对称窗口（集合通信域上下文）；HIXL=独立 engine 拓扑（engine 名=ip:port、用户态交换地址、无 rank 概念）——**两套注册/建链/完成语义，不得互证**；ch22 正文对照表一处即可。
- ch23 通算融合=Device 侧 `AscendC::Hccl`＋MC2；HIXL 的 device kernel（chunked copy/notify）是其**传输实现细节**，不属 ch23 主线，正文一句带过。

## 11. 复现命令（全部〔需真机验证〕；本书整理，出处标注）

```bash
# ①构建（docs/zh/build.md L184-190 原文命令；联网自动拉第三方；源仓只读先复制）
CANN_SRC=/mnt/SATASSDEXT4/cann; WK=$(mktemp -d)
cp -r "$CANN_SRC/hixl" "$WK"/ && cd "$WK/hixl"
source /usr/local/Ascend/ascend-toolkit/set_env.sh   # 路径按部署；见 build.md L53
bash build.sh --examples          # 含样例/benchmark；不涉及 src/ops 改动可加 --host
# ②单进程双 engine（同机两 device；≥CANN 9.1.0）——README L121/131 区参数
./build/examples/cpp/hixl_example_d2rd --protocol=hccs:device --device=0,2   # A2/A3；950 改 uboe:device 等
# ③多进程：server 先启动（L122）；fabric_mem_d2d 成对双终端（L123）
# ④benchmark 单机/双机（README L124/L118）：
bash benchmarks/run_all_bench.sh --loops 10 --device-ids 0,1,2,3,4,5,6,7
# 双机：python benchmarks/run_comm_benchmark.py --role=target|initiator ...
```

环境前提（D build.md）：Toolkit+ops 包；python 样例另需 ops；docker 镜像 A2/A3/A5。

## 12. 未证/未核清单（rev2 收敛后；正文须声明）

1. device 侧 kernel 内部（CANN opp `libcann_hixl_kernel.json`，load_kernel.cc L27 仅加载）——notify/数据落地保障在二进制内〔U〕。
2. RegisterMem 后 server→client 资源广播体——未见〔U〕。
3. UbClientHandler/FabricMem engine 内部——仅入口〔U〕。
4. quickstart 收尾窗口实际竞争是否可观——需真机〔U〕。
5. 性能数字全部来自仓内 benchmark 文档，本书无实测〔D〕。

## 13. EVIDENCE-CLOSE 补证（rev2；逐条对应任务书六点）

### 13.1 双端时序（订正定稿，行号可核）

```text
Server(dev2,:16001)                        Client(dev0,:16000)
InitEngine→SetDevice(2)                    InitEngine→SetDevice(0)
malloc+H2D fill 0x5A                       malloc（PrepareClientMemAndOp）
RegisterMem [L187]                        ExchangeAddr(true):connect:17001,recv addr [L146]
ExchangeAddr(false):accept,send addr [L191] RegisterMem [L159]
（等）                                      Connect [L162]
（等）                                      TransferSync READ [L163]→VerifyData [L165]
recv done 阻塞 [L194]                     send done [L167]
Finalize:dereg→free→engine.Finalize→reset [L197]（无等待，窗口见§3.9）
                                           Disconnect [L168]→Finalize [L171]
```

### 13.2 完成保障链（订正归因：host_flag 非 kernel 直接置位）

1. `dev_const_one`=设备上常量 1（transfer_pool.cc L513-521 初始化；L178 填入 handle）。
2. `LaunchDeviceChunkedKernels`（L720-737）按 `kMaxKernelBatchSize` 分块；`need_notify_wait`（每 1920 或末块，L726/L51）时 param 携带 remote_flag/local notify（BuildDeviceChunkParam L798-818 区；HCCS `use_notify_record=1`）。
3. launch 后**同 stream** `aclrtWaitAndResetNotify(notify,stream,timeout)`（L786-789 区）——stream 内阻塞点。
4. **标志写入**：L893-897 `aclrtMemcpyAsync(host_flag←dev_const_one,D2H,同 stream)`——**写 1 的是常量拷贝**。host_flag==1 ⟺ D2H 已执行 ⟺（stream 序）先前全部 kernel＋notify-wait 完成。
5. 语义分层：**提交**（launch+D2H 入队，返回 handle 即有效）→**stream 顺序**→**Host 可读**（CheckStatusDevice L1093-1098 读 flag）。kernel 内「数据落地才放行 notify」在 CANN 二进制内（§12.1 U）；host 侧证据链到此，**不得写 kernel notify 直接置位**。错误旁路：err_flag≠0→Latch(FAILED)（L1112-1121）；DeviceSync 超时 Abort slot（L946 区）。

### 13.4 失败 latch 全景（复位点=L339 实证）

- **置位**：`LatchTransferFailure`（L741-747 幂等）；入口①提交失败 `LatchTransferFailureIfNeeded`（L749-753，Sync/Async 尾 L1013/L1053 区）②查询见 err_flag（L1113）；判据 FAILED||TIMEOUT（L735-739）。
- **拒绝新传输**：Sync/Async 入口 `!latched` 否则 FAILED+last_status（L988-991/L1028-1031）。
- **存量查询**：latched→CheckStatusDevice 判 FAILED＋ReleaseDevCompleteHandle（L1102-1110）——挂起任务一次性判死回收。
- **slot**：末引用释放时 latched→`pool->Abort` 否则 `Release`（L671-683）；err_flag 仅无 pending 引用时清零。
- **复位唯一点**：`Create` L339-340＝**新 client 对象**。
- **闭环（rev3 订正：受 auto_connect_ 门控，非无条件）**：`AutoConnect`（hixl_engine.cc L383-408）**两分支**——`auto_connect_==false` 时**只 `GetClient`，查无即 `NOT_CONNECTED` 返回，不重建**（L386-393）；==true 时查无才 `GetOrCreateClient` 全新建链（L400-406）。`AutoDisconnect`（L422-431）**仅在 auto_connect_==true 才 Disconnect**，false 时**空转 SUCCESS（保留可能已坏的 client！）**。⇒ 正确用户语义：**自动模式**（OPTION_AUTO_CONNECT=1，doc：跳过建链/异常自动清理/心跳 10s，interface L98）失败后下次传输自动重建；**显式模式**（默认 false，L94 `value_or(false)`）失败后 client 残留，须**应用显式 Disconnect→Connect** 重建，直接重试只会再吃 NOT_CONNECTED/FAILED。**自动断链本身也可能失败**（AutoDisconnect 内 HIXL_CHK_STATUS_RET Disconnect）。**对象复位≠传输可安全重放**：timeout 可能已部分写入（DeviceSync 超时仅 Abort slot，数据态未证）；源数据/远端注册须保持稳定；**重试决策归应用**，本书不承诺幂等或完成〔C+I〕。
- **传输内部重试（订正「无传输级重试」）**：host 路径 `TransferWithRetry`（L495-533 区）——HCCL_E_AGAIN 时 ChannelFence 后重试，总窗 20min 超时 TIMEOUT；device 路径重试在 kernel/Hcomm 层（U）。RDMA env 作用于建链 channel 参数（InitRdmaRetryConfig L1348 区），非传输重试。

### 13.5 完成查询三层语义（返回值≠status 输出）

- **层1 CS**：CheckStatus* 只产 WAITING/COMPLETED/FAILED，**从不产 TIMEOUT**（枚举映射 client_handler.h L33-45）；COMPLETED/FAILED 即 Release*Handle（L593-624 等）＝查询即消费；WAITING 保留。
- **层2 handler**（direct_client_handler.cc L107-135 区）：查无 req→PARAM_INVALID+FAILED；底层 ret≠SUCCESS→**status=FAILED+erase+返回 ret**；WAITING 保留；终态 erase。
- **层3 engine 单条**（hixl_engine L243-262，rev4 逐分支）：owner 查无→status=FAILED+PARAM_INVALID；**查询调用失败 ret≠SUCCESS**→EraseTransferReq+**AutoDisconnect（返回值被 HIXL_CHK_STATUS_RET 检查）**+返回 ret；**查询成功且 status≠WAITING（含 FAILED）→仅 EraseTransferReq，无 AutoDisconnect**——「FAILED」≠「自动断链」，二者条件不同。
- **批量**（L264-310，rev4 逐分支）：①client==nullptr→**仅 erase+continue，无结果元素**（L273-276）；②**ret≠SUCCESS（查询调用失败）**→该 engine 入 `disconnected_engines`+AutoDisconnect（**`(void)` 忽略返回值，显式模式下空转也入集合**）+本 req status=FAILED+erase+出结果（L286-295）——**入集合条件=调用失败，≠status==FAILED、≠断链成功**；③集合中 engine 其余 req 免查询直接 FAILED+erase（L277-285）；④status≠WAITING→erase；⑤skip_waiting 仅过滤（req 仍注册 L301-303）；max_query_count 截断；返回恒 SUCCESS。
- **TIMEOUT 出处**：仅同步路径——HostSync deadline（L975-981，释放 handle）/DeviceSync sync 超时（Abort slot）/TransferWithRetry 20min/UB handler L135；**异步查询不产 TIMEOUT（CS）**。⇒ **同步返回 SUCCESS 才算完成；sync TIMEOUT 数据落定未证→缓冲不得视为可复用**；FAILED 返回值会写入输出 status（两层均写）〔C〕。

### 13.6 路由「候选≠选中」与宣传语边界

- **引擎选择阶梯**（engine_factory L38-75，先于 endpoint 匹配）：FabricMem 开→FabricMemEngine；LocalCommRes 1.3→HixlEngine(CS)；其他 version→CommEngine(legacy)；`protocol_desc` 非空→HixlEngine；SoC kV5(950)→HixlEngine；else CommEngine。**quickstart 实际**：protocol_desc=["hccs:device"]→CS 分支〔L60/L66-68〕。
- **endpoint 匹配**：两张 rule 表只是**候选优先级**；最终选中=建链协商 MatchEndpoint（client 发起/server 匹配，hixl_cs_client L1410-1440 区）依赖**双端配置交集**——正文写「优先级∩双端配置」，不写「一定选中」。
- **BUFFER_POOL≠实走中转**：option 仅 FabricMem/CommEngine 路径解析（fabric_mem_engine L34-41）；**CS HixlEngine 直传路径无 buffer_pool 引用**〔C：grep；U：legacy ADXL 内部〕——默认 4:8MB 是选项默认，非传输事实。
- **FabricMem「CPU 零介入」**：doc 原文限定「无需 CPU 介入的单边通信：源端发起，对端零开销」（FabricMem.md L18）＝数据面措辞；控制面与 Host 展开 4 流路径均含 Host 参与——不得泛化全流程无 Host；极值引用带 AICPU/Host 展开+块+方向全条件。

### 13.8 rev4 补证（R1 评审；2026-10-09）

- **GetAsyncConnectStatus=本端连接池台账**：impl 转发 `connect_pool_executor_.GetStatus`（hixl_impl.cc L173-176），读 `task_result_`（connect_pool_executor.cc L128-133；**无记录→NOT_CONNECT**）；只有 Async 提交的任务写表（L96/L124；同步 Connect 不经此）。**不能用它观察 server 侧入站 client 断链进度**——22.3.2 建议据此删改。
- **性能读数订正**（performance.md 实核）：A3 单机 FabricMem D2rD/1M——AICPU=170.514、**Host 展开 4 流=175.102**（L30/L43）；156.698 是 **rD2D**（L30 第3列）；16K AICPU=16.113、**Host 展开 16K=2.874**（L25）；170.514/16.113≈**10.58 倍**（非40）。1M/2M Host 展开反超（181.431@2M），差距集中 16K–256K。
- **LLM-DataDist 默认后端**：pull 样例默认 adxl、push 样例默认 HCCL（examples/cpp/README L79/L93 原文）；接口文档仅承诺可选 hixl；A5 仅 hixl CS+UB——无统一默认，引用须带场景。
- **fabric_mem 目录实文件**：fabric_mem_aicpu_dispatcher.{cc,h}/fabric_mem_aicpu_transfer_service.{cc,h}/fabric_mem_allocator.{cc,h} 等（`ls` 实核）。

### 13.9 rev5 补证（R2 评审；2026-10-09）

- **HostAsync 内联重试链**：`BatchTransferHostAsync` L508-516 →`BatchTransferTask` L495-501→`TransferWithRetry` L452-487（kRetryTimeoutMs=20min L454；TIMEOUT 返回 L480）——**异步提交阶段同步执行全部传输/重试**；提交 `Status TIMEOUT`=提交失败，≠查询态 `TransferStatus::TIMEOUT`（仅枚举/映射 client_handler.h）。`BatchTransferHostSync` deadline 路径 L966-970（释放 handle 后 TIMEOUT）。DeviceSync=`aclrtSynchronizeStreamWithTimeout` 失败→Abort slot。
- **端点协商无交集**：`ExchangeEndpointAndCreateChannel`→`SendMatchEndpointRequest/RecvMatchEndpointResponse` 失败即建链失败（HIXL_CHK_STATUS_RET 链）——「交集为空→协商失败」，无次选保证（次选仅表内优先序，前提是命中）。
- **quickstart 无 --version**：main 仅 `--role`（L201-224 实核）；`--version` 属 d2rd 系（d2rd.cpp L26/L100-105）。
- **构建产物路径**：build.sh BUILD_PATH=`<repo>/build/`（L15/L78），examples 可执行=`build/examples/cpp/`（examples/cpp/README L49 原文）；`build_out`=CMAKE_INSTALL_PREFIX/package（build.sh L215 CMAKE_INSTALL_PREFIX=OUTPUT_PATH；make package）——run 包与可执行分离。

### 13.10 rev6 补证（R3 评审；2026-10-09）

- **ACL 错误映射**：`HIXL_CHK_ACL_RET`（common/hixl_checker.h L116-125）——仅 `ACL_ERROR_RT_STREAM_SYNC_TIMEOUT`→`hixl::TIMEOUT`，其余 `static_cast<Status>(acl返回值)` 原样透传；DeviceSync 先 Abort 后 CHECK（L946 区）→「同步失败」三分：SUCCESS/TIMEOUT/其他 ACL 码。
- **HostAsync 提交≠完成**：L508-516 BatchTransferTask（内联重试）后→L504 Fence→L530-537 对端 flag `ReadNbiOnThread`→返回 handle；完成仍靠 CheckStatus 读 flag。**提交期可长阻塞（重试 20min/次，每次调用独立计时）≠传输完成**。
- **HostSync 计时起点**：deadline=`now()+timeout_ms` 在 HostAsync **返回后**（L962 区）——timeout_ms 不覆盖提交重试耗时（次序推导，非实测）。
- **公开 wrapper 层**：`Hixl::TransferAsync` L374-382/`GetTransferStatus` 单 L386-391/批 L393-397——前置 `impl_` 空检查 FAILED；「恒 SUCCESS」仅引擎内部层，公开层返回码须查。`TransferResult{req,user_data,status,reserved[108]}`（hixl_types.h L87-91）；`TransferAsync` 参数序=(remote,op,descs,TransferArgs,req)。
- **批量未出结果三成因**：B1 owner 消失（无结果）/B5 skip_waiting 过滤/B6 max_query_count 截断未遍历——对账三分；单条查询 `PARAM_INVALID` 可作结束条件。
- **复现**：独立 shell 不继承 WK→两终端显式赋值占位+`test -d`+`set -e`；构建块 echo WK。

### 13.11 rev7 补证（R4 评审；2026-10-09）

- **批量逐行（hixl_engine.cc L264-310）**：erase 条件=`status!=WAITING`（L302-304/L323-325 区）——**WAITING 永不 erase**，`skip_waiting`（L307-309）只过滤元素；调用失败分支 status 强制 FAILED→照常 erase＋emplace FAILED；COMPLETED/FAILED 终态→erase＋emplace。分支表重排 B1–B7（补 B4 COMPLETED、B6 WAITING 保留注册、B7 截断）。
- **同步 TIMEOUT 三路**：`BatchTransferHostSync` 先 `HIXL_CHK_STATUS_RET(BatchTransferHostAsync…)`（L958-959，③提交链 TIMEOUT/错误经此透传）再 deadline 轮询（L962-983：到期→`ReleaseCompleteHandle`）；`CheckStatusLocked` 失败→释放 handle 返回该码。DeviceSync=②ACL 映射。**HostSync 的清理（release handle）只属①deadline 与查询失败分支；③透传时句柄未必建立**——清理逐分支，不统一承诺。
- **公开 API 签名**（hixl.h L143-145/L143 区；hixl_types.h L76-79/L87-92）：`TransferArgs{user_data,reserved[120]}`；`TransferResult{req,user_data,status,reserved[108]}`——结果 user_data 即提交时传入指针。
- **quickstart Finalize 次序**（L120-137）：close socket→DeregisterMem（返回码忽略）→printf done→aclrtFree（忽略）→engine.Finalize→ResetDevice——打印在 free 前，不证成功。
- **复现**：构建块 `set -e`＋echo WK 根目录（防 /hixl 双拼）；终端 `test -d` 与 `cd` 分行（&& 短路不触发 set -e）。

### 13.7 对 OUTLINE 的增量（§22.3/22.4 改写点）

双进程镜像时序图；完成链「常量拷贝+stream 序」归因；**auto_connect 两模式重试语义（rev3）**；查询三层表；路由优先级∩交集；收尾窗口如实声明。
