# CH22 OUTLINE——HIXL 单边通信（提纲）

目标：核心章 8k–12k 中文字。主线=**真实数据流与生命周期**；性能只讲「口径与条件」，不编数据。读者问题链：**单边到底单在哪→API 长什么样→一次 READ 的完整旅程→库内怎么走到硬件→内存/注册的代价→路径怎么选→FabricMem 特殊在哪→LLM-DataDist 加了什么**。

## 22.1 单边通信的问题与 HIXL 定位（~0.8k）
- 对比集合通信（ch21）：无 rank/域收集；engine 名=`ip:port`；发起方单边操作对端内存。
- 澄清三件常被写错的：**单边≠对端零准备**（注册/建链/存活前提，quickstart L101 原文）；**零拷贝≠无中转**（BUFFER_POOL 默认 4:8MB，FabricMem/UB 各异）；**方向按接口分立**（READ=远→本，WRITE=本→远）。
- 版本双轨：version=0 HCCL 通信域 legacy（仅 roce:device，A2/A3）vs version=1 HIXL CS（解耦域，A2/A3/950）〔C/EV§5〕。
- 与 ch21 SymWin/ch23 通算融合边界一表。

## 22.2 API 全景与类型系统（~0.8k）
- 15 方法分四组：生命周期/内存/连接/传输(+notify/capability)；全签名表（EV§2）。
- 类型细读：`MemDesc.reserved[128]`/`TransferReq=void*`/`TransferResult.reserved[108]`——ABI 预留的演进意图〔C+I〕。
- 错误码族 `103900/503900/203900` 与 `GetCapability(AUTO_CONNECT/CLIENT_SERVER_COMM)`。
- options 七常量总览（细节散布后节）。

## 22.3 生命周期主线：quickstart 双端走读（~1.5k，正文锚 A2）
- 按 §3 九步逐段真码：Initialize(options)→RegisterMem→**socket 自备交换地址**（HIXL 不给通道）→Connect→TransferSync READ→VerifyData（样例自带校验，对比 ch21 只打印）→双向收尾序。
- **顺序约束表**（D）：注册先于建链/dereg 一次有效/Finalize 前断链+解注册/Server 等所有 Client/Client 读写未完 Server 勿动地址。
- 单进程双 engine（0,2）与多进程两态。

## 22.4 一次传输的库内旅程：从 API 到硬件（~2k，正文锚 A3/A4）
- `HixlImpl→EngineFactory→HixlEngine`：AutoConnect 链路池；失败→AutoDisconnect（**无传输级重试**，重试在 RDMA env 层）。
- handler 路由（§5 表）：同 instance UB group→HCCS→…；跨 instance UBoE→…；version=0 分叉。
- **Device 路径**：desc H2D→`LaunchDeviceChunkedKernels`（kMaxKernelBatchSize 分块+notify 间隔）→kernel＋host flag D2H→完成判定；**Host 路径**：BatchTransferTask+flag 队列，耗尽→`RESOURCE_EXHAUSTED`（错误消息原文：先查询再新建）。
- 完成语义：sync 阻塞；async「查询即消费」（COMPLETED/FAILED 后不可再查，D L896/941）——调用方须保存结果；失败 latch 机制＋未证复位〔U〕。
- RDMA env `HCCL_RDMA_RETRY_CNT/TIMEOUT` 公式（网卡级，非传输级）〔D〕。

## 22.5 内存注册经济学（~1k）
- 上限表：4K 个/Device 50GB/Host 20GB(HDK<25.5)→1TB；重复注册同 handle；dereg 幂等边界。
- 中转 BUFFER_POOL：默认 4:8MB、0:0 关闭、与 FabricMem 互斥、A2 HCCS Server 仅 D2D 限定〔D 原文〕。
- **「零拷贝」的准确边界**：直传路径成立；中转/FabricMem 另述——给判定流程不给口号。

## 22.6 路径矩阵与平台条件（~1.2k）
- 8 方向×{hixl_cs,通信域}×{FabricMem AICPU/Host 展开,ROCE,HCCS,UB 系}条件表（EV§5/§9 合成）；A2 无 FabricMem；950 走 UB 系（uboe/ub_rtp/ub_ctp）;A5 仅 CS 后端+UB 默认。
- 方向命名 D2rD…rD2H 全表（benchmarks README L164-175）——**本章所有性能讨论的坐标系**。
- 图：路径判定树（SVG 或 mermaid：version→instance→placement→protocol→handler→传输机制）。

## 22.7 FabricMem：超节点内存池化（~1.2k）
- 动机数据：RoCE~20GB/s vs 百 GB 级（D）；A3 限定。
- VMM 四步（mallocPhysical/reserve/map→物理地址交换→页表→SDMA 直读远端）＋fabric_mem_d2d L52/133-142 真码。
- 配置：`fabric_memory.max_capacity` 等；HDK 25.5 AdxlEngine MallocMem 特例；与 BUFFER_POOL 互斥。
- `src/hixl/fabric_mem/` 组件地图（aicpu dispatcher/host transfer service/slot_pool/virtual_memory_manager）——内部未逐行声明〔U〕。

## 22.8 LLM-DataDist 与生态＋benchmark 口径（~1.5k）
- 分层声明：独立库/KV 语义/链接 FSM（LLM_NOT_YET_LINK…错误码族）/role 仅标识；Link→AllocateCache→Pull/Push→Unlink 生命周期；OPTION_TRANSFER_BACKEND=hixl 切换。
- 样例矩阵：成对运行/超时WAIT、python 命令、A5 限制。
- 生态一段：Mooncake/SGLang/vLLM=仓外上层，HIXL=传输后端（ blogs 两篇为场景叙述无新 API〔D〕）。
- **benchmark 口径章**：128MiB/block 梯/方向表/hixl_cs vs 通信域/AICPU vs Host 展开；代表值引用规则（版本+架构+shape+口径+来源五要素）；复现命令（build --examples/单双机跑法）〔需真机验证〕；本书无实测声明。

## 22.9 小结＋陷阱清单（~0.3k）
- 单边三澄清回扣；查询即消费/flag 耗尽/latch/Server 先退/混版本 0-1 等陷阱 8 条。

## 图（2–3）
1. `ch22-hixl-stack.svg`：API→engine→handler(DIRECT/UB)→CS client→传输机制×3（Device kernel/Host flag/FabricMem SDMA）分层图（含 version0/1 分叉、legacy vs impl 两代并注）。
2. `ch22-lifecycle.svg`：双端时序（init/register/exchange/connect/transfer/verify/teardown＋约束注）。
3.（可选）路径判定树并入 1。

## 字数分配合计 ≈10.3k（8k–12k 带宽内）；证据=EV§1–12；标签纪律：样例/命令〔需真机验证〕、结构图〔示意代码〕标注节录改写。
