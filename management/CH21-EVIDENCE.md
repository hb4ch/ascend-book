# CH21 证据账本（HCCL/HCOMM）2026-10-09

基线：hcomm `1581d1608fd8840bbd46bcbe3f357b1d08460b6a`（SOURCE-BASELINE 同）；asc-devkit `28e7aba2`；cann-learning-hub `a3989658`。只读核查，未运行任何程序。**分级**：〔C〕直接代码／〔D〕源文文档声明／〔I〕推导／〔U〕未证。路径均 repo 相对根。

## 0. 名称关系（先立框架，防混层）

- **HCOMM＝通信基础库**（通信域/资源管理＋基础原语），**HCCL＝集合通信库**，**「HCCL 算子通过 dlsym 动态加载 HCOMM 接口，两仓独立编译独立演进」**〔D：`hcomm/docs/zh/api_ref/hcomm_header_and_lib.md` L3、`architecture/architecture-brief.md` §软件架构约束表〕。
- 对外 API 分层〔D：architecture-brief §3.3 表〕：L1 HCCL 算子（hccl.h，AI 框架用）→ L2-comm 通信域（hccl_comm.h）→ L2-res 拓扑/资源 → L3-prim 原语（hcomm_primitives.h）→ L3-res/CCU。
- **本机仅 hcomm 仓**；HCCL 算子仓（`src/ops/all_reduce…` 结构见 architecture-brief §3.2）**不在本地 10 仓**〔U：host 侧 `HcclAllReduce` 完整 host 实现不可本地引用，仅能引 asc-devkit device 侧头与 hcomm 内部〕。`hcomm/pkg_inc/legacy/hccl/hccl_inner.h` L22 仅有 `HcclAllReduceInner`（弱符号/内部）〔C〕。
- **device 侧集合通信 API 真身在 asc-devkit**：`asc-devkit/include/adv_api/hccl/hccl.h`——`AscendC::Hccl` 模板类，`AllReduce/AllGather/ReduceScatter/AlltoAll(V)/BatchWrite` 均 `__aicore__`、返回 `HcclHandle`，配 `Init/Commit/Wait/Query/Finalize`〔C：L77/103/133/165/230/284/304/316/326/368〕；头注 L47 明示 **A2/910_93 须指定 AICube/AIVector 核**。

## 1. 五锚点调用链（主线：Host 侧 AllReduce，样例 examples/01_communicators/01_one_device_per_process）

**A1 域创建**〔C：`main.cc` L114-132〕：`HcclGetRootInfo`（root rank）→ MPI_Bcast rootInfo（HCCL_ROOT_INFO_BYTES=4108，`include/hccl/hccl_types.h` L112）→ `HcclCommConfigInit`＋`config.hcclBufferSize=1024（MB，注释原文）／hcclDeterministic=1／hcclCommName` → `HcclCommInitRootInfoConfig(devCount,&rootInfo,devId,&config,&comm)`。config 全字段〔C：hccl_types.h HcclCommConfigDef〕含 `hcclOpExpansionMode（0 默认/1 host/2 aicpu/3 aiv——注释原文）`。**替代入口**：rank_table.json＋`HcclCommInitClusterInfoConfig`〔C：examples/…/02…/main.cc L130；rank_table.json 结构 server_list.device{device_id,device_ip,rank_id}〕。
**边界**：`HcclCommInitRootInfo`等产品支持矩阵〔D：`docs/zh/api_ref/comm_mgr_c/HcclCommInitRootInfo.md` L3-20：950PR/DT、A3、A2(910b)、310P、910 全支持〕。

**A2 资源与拓扑（控制面）**：`src/coll_communicator_mgr/`{communicator（coll_comm*）、rank_graph、resource_mgr、config_mgr、api_c_adpt}〔C：目录〕。拓扑模型 Node/Endpoint/Edge/Link/Fabric/netLayer（Layer0 server 内 HCCS、Layer1 跨 server RoCE）〔D：architecture-brief §2.2 表〕。RankGraph「Edge↔NCCL Link 名称对应不同」辨析〔D 同〕。

**A3 算法选择（证到条件）**：两层——
①**拓扑级** `alg_configurator.cc SelectCurrOpAlgType`（L57-140 区）：`Is310P3Common→WHOLE_RING`；超节点 server 非对称＋ARS 类→AHC；`isNoARS/isNoAHC→WHOLE_RING`；nicList!=8 且 deviceNumPerAggregation==8 时强校验 8P ring（L114-119 ERROR 原文）。algType 三层 Level0/1/2〔C〕。
②**算子级** `operator/all_reduce_operator.cc SelectAlg`（L108-160）：`userRankSize==1→SingleExecutor`；按 `deviceType_` 分派 910A/910B/910_93/310P 选择器；**910B 路径全条件**（L295-380 区）：`isAivMode=（AivModeConfig∧!Barrier）∧IsSupportAIVReduce(dtype,op)∧mesh∧CCLBuffer≥16M∧（单机∨小数据≤190KB/rank∨中数据≤16M）∧（非确定性∨≤8M deter）`〔C——每括号内条件均源码原文级〕；pipeline 超 FFTS 容量重定向 HD（L337-347 区）；**环境变量 `HCCL_ALGO`**（`level0:NA;level1:<algo>` 语法）经 `env_config.cc` L233-251/MM_ENV_HCCL_ALGO 解析〔C〕。**结论表述纪律：目录名（coll_all_reduce_ring…）≠执行路径；执行哪个 executor 由上两条件链＋HCCL_ALGO 共同决定**〔I，条件本身〔C〕〕。executor 注册/名字映射 `HCCL_ALGO_LEVEL1_NAME_MAP`（all_reduce_operator L146）、「AllReduceARSFor91093Executor」附加 ringSize（L164-168）〔C〕。

**A4 数据传输（引擎×协议×路径）**：引擎四类〔D：architecture-brief §2.4 表〕AICPU_TS（Task 描述符，不占计算核）/CPU_TS（A2 专用）/AIV（占 Vector 核、低延迟小包）/CCU（950 硬化、URMA、950PR/DT 限定）。数据面原语真名〔C：`docs/zh/api_ref/comm_opdev/data_plane_api/cpu-cpu_ts-aicpu_ts/communication_operations/` 目录〕：`HcommWrite/Read/ReadReduce/WriteReduce(WithNotify)(Nbi)(OnThread)`、`HcommChannelNotify{Record,Wait}(OnThread)`、`HcommChannelFence`——与 AICPU P2P blog 引用一致（见 §3）。内存语义 vs 网络语义原语二分〔D：architecture-brief §2.3.1〕；协议集 UBC/UB_RTP/UBoE/RoCE(v2)/HCCS/UB_MEM〔D 同 §1.2；**物理层关系仅照录，不展开硬件推断**〕。CCL buffer：`cclBufferManager_.GetIn/OutCCLbuffer`（all_reduce_operator L327-330 区）〔C〕；零拷贝/内存预留 `HcclCommSetMemoryRange`（配 `aclrtReserveMemAddress`，域名「对当前进程所有通信域可见」）〔D：comm_mgr_c/HcclCommSetMemoryRange.md 功能节〕。

**A5 完成与释放**：host 流上异步下发＋`aclrtSynchronizeStream` 阻塞（main.cc L72-74 注释原文「阻塞等待任务流中的集合通信任务执行完成」）〔C〕；device 侧 `Wait(handleId)` 阻塞语义＋**「须与 Prepare 同序调用」**（hccl.h L308-316）＋`Query` 非阻塞〔C〕；async 错误 `HcclGetCommAsyncError`〔D：comm_mgr_c 文件〕；Barrier=「所有 rank 都下发执行该操作为止」阻塞 stream〔D：HcclBarrier.md 功能节〕。释放序（样例真序，main.cc L140-147）：Sample 内 free buf/destroyStream → `HcclCommDestroy` → `aclrtResetDevice` → `aclFinalize` → `MPI_Finalize`〔C——**这是「销毁顺序」唯一样例级证据；反向或省略的后果无文档断言，U**〕。notify 配对闭环（Record→Wait→Record）见 §3 P2P：发送端 Step2 Record/Step3 Wait/Step4 收到读完成；接收端 Wait→单边读→Record〔D：blog §3；**单向通知不构成释放证明，blog 四步双向配对才是完整闭环**〕。

## 2. 平台矩阵与执行路径（A2/A3/950 分叉实据）

- DevType 映射〔C：`src/legacy/ascend910/platform/inc/adapter/adapter_hal.h` L40-58〕：`Ascend910B1-B4→DEV_TYPE_910B`（A2 系）；`Ascend910_9362-9392→DEV_TYPE_910_93`（A3 系，9392/9382 注释「预留暂不支持」）；`Ascend950PR_958b→DEV_TYPE_950`。**「A2=910B、A3=910_93」由 device_capacity.cc L25 注释「A2和A3场景…」旁证＋映射表**〔C＋I〕。
- **legacy 目录语义**：`src/legacy/ascend910`=A2&A3 兼容、`ascend950`=A5 旧流程兼容；**legacy 不持续演进、新能力在标准目录**〔D：README 目录注释＋architecture-brief 约束表〕——正文引 950 新特性勿引 legacy/ascend950。
- AICPU 展开「目前只有 A3 和 300I 支持」〔C：`framework/communicator/comm_config.cc` L363 注释原文，`SetConfigOpExpansionMode` case 2〕；`hccl_communicator_device.cc` L1300 `GetAivModeConfig(){return false;}`（device 版恒 false——**AIV 判定以 host 侧 config 为准，此细节正文须精确到文件**）〔C〕。
- AIV Reduce dtype/op 白名单〔C：`platform/common/device_capacity.cc` L57-66〕：fp32/fp16/int8/16/32/bfp16 × sum/max/min。
- 引擎-平台对应：CPU_TS「Atlas A2 专用」、CCU「Ascend 950PR/950DT」〔D：architecture-brief §2.4 表〕；950 AIV 直驱 URMA（SHMEM+UDMA+同 kernel 编排）〔D：learning-hub `blogs/operator/ascend950_aiv_urma_shmem_communication/…md`（525 行，§3 软件栈/§7 编程模型）——**ch21 仅引为 950 数据面新路径概览，编程细节归 ch23/自定义章按需**〕。
- Host/Device/AICPU 执行位置分层：Host（框架/域管理/选择）→ AICPU_TS/AIV/CCU（Device 数据面）→ 硬件（RoCE/SDMA/UB）〔D：architecture-brief §2.4〕。

## 3. 两个「待验真」主线候选（结论：可入正文，均给真链）

**P2P 自定义算子（AICPU）**：**可行**——完整方法论＋API 名链在 `hcomm/docs/zh/comm_op_dev_guide/aicpu_comm_op_dev/`（overall_flow/define_op_if/query_topo/algo_select/create_res/task_sched/op_dispatch/build_deploy 八篇）＋blog `cann-learning-hub/blogs/operator/hccl_custom_operator_aicpu_p2p/基于AICPU引擎的HCCL点对点通信算子开发.md`（261 行）：控制面 HcclEngineCtxGet→资源（Thread/Channel/Notify，aclrtCreateNotify）→句柄 memcpy 下发；数据面 Kernel 内 `HcommAclrtNotifyWaitOnThread`→`HcommChannelNotifyRecordOnThread`/`WaitOnThread`/`HcommReadOnThread`（单边读）→`HcommAclrtNotifyRecordOnThread` 回 Host〔D：blog §4 步骤原文；API 与 data_plane_api 目录名对上〔C〕〕。**样例代码 `examples/04_custom_ops_p2p` 不在本地 hcomm（examples 仅 01/02）**——blog/gitcode 外链 `cann/hccl examples/04_custom_ops_p2p`＋`build.sh --vendor=cust --ops=p2p --custom_ops_path=…`〔D：blog L52/L192、aicpu…/build_deploy.md L7/22/76〕；**正文引用须标注「仓外资源，本地未核全码」〔U〕**。
**高精度 ReduceScatter**：**为「二开思路案例」非 HCCL 现成开关**——blog `hccl_reducescatter_high_precision_redevelopment/HCCL ReduceScatter精度优化.md`：原方案 4 步（拷入 cclBuffer→对端拷→**MTE3 归约**→拷出）＋BF16→插 Cast FP32 计算→改 AIV 执行 Cast+Add+Cast＋数据切分并行〔D，全文定性〕。**现成接口侧证据**：CCU `LocalReduce` 支持「升精度：仅 SUM，int8→fp32 类，输出按精度膨胀预留」〔D：`docs/zh/api_ref/comm_opdev/data_plane_api/ccu/data_movement/LocalReduce.md` L72〕——**两者合流：正文讲「精度-性能权衡＋二开路径」，不得称「HCCL 自带高精度 RS 开关」〔U：host 侧 RS dtype 升级未系统核查〕**。
**与 ch22/23 分工**：单边/零拷贝/SymWin→ch22（hcomm `zero_copy.md`/`symmetric_mem.md`/`HcclCommSymWin*` 仅登记）；通算融合 MC2→ch23（ops-transformer/mc2、pto-isa gemm_ar）；950 AIV URMA 编程细节→按 ch23 需要再深挖。本章收：域/资源/选择/传输/完成＋传统集合原语＋自定义算子方法论。

## 4. 完成条件/生命周期核对清单（正文必写）

①AllReduce 返回=入队非完成〔D：hccl.h「asynchronously…Wait (blocking)」〕②stream 同步才可见结果〔C：main.cc L74〕③device Wait 同序约束〔C：hccl.h L314〕④notify 双向配对才闭环〔D：blog 四步〕⑤资源复用：多次调用复用 ctx（blog §4.1「Per-Device…资源复用」）⑥销毁序样例唯一〔C；缺证后果 U〕⑦确定性 `hcclDeterministic`（0/1，注释）与 STRICT 模式限制（all_reduce_operator L172-179「混合组网不支持规约保序」ERROR）〔C〕。

## 5. 提纲路径核对（旧提纲→实际）

| 旧提纲 | 实际 | 状态 |
|---|---|---|
| `hcomm/src/base_comm/`、`src/coll_communicator_mgr/`、`docs/zh/`、`examples/` | 存在 | ✓ |
| `cann-learning-hub/tutorials/hccl_development/` | 存在（6 PDF slides+README；**PDF 未逐页核**〔U〕） | ✓ |
| `blogs/operator/hccl_custom_operator_aicpu_p2p/` | 存在 | ✓ |
| appD 已列 `hccl_reducescatter_high_precision_redevelopment/` | 存在（appD L57 已录） | ✓ |
| blog 内 `examples/04_custom_ops_p2p` | **本地无**（gitcode cann/hccl） | 记录 |
| HCCL 算子仓（L1 实现host） | 本地无 hccl 仓 | 记录，正文只引 asc-devkit device 侧＋hcomm |

## 6. 可复现条件（无硬件，仅列出）

样例 01：CANN 包（含 hcomm）＋source set_env＋MPI（mpich，`MPI_HOME`）＋`make && make test N=$RANK_SIZE`（950=2 卡、他 8 卡，README L59-73）＋自编 tar 需关驱动验签（README L55→build.md）。950 AIV URMA/P2P/CCU 按 comm_op_dev_guide 各 build_deploy。**本书一律不宣称已运行**；CPU-SIM 路径未见 hcomm 侧文档〔U：留待 PM 定〕。

## 7. 补证（R1，2026-10-09）：调用链分层边界

### 7.1 Host 契约只用 Host 证据；样例参数全录

- **主线 Host 契约证据**＝样例 `hcomm/examples/01_communicators/01_one_device_per_process/main.cc`＋`docs/zh/api_ref/comm_mgr_c/*.md`；**device 侧 `AscendC::Hccl`（asc-devkit hccl.h）头注不得引为 Host 异步/完成语义依据**——两者仅「同名算子、不同层」，完成机制分属 stream 同步 vs `Wait(handleId)`〔C，修正前稿混引〕。
- **样例参数实录**〔C：main.cc L44-77〕：`count=ctx->devCount`（=进程数=卡数，**非固定 8**）；`mallocSize=count*sizeof(float)`；send/recv 各一块 Device buffer（`aclrtMalloc HUGE_ONLY`）＋hostBuf；输入每 rank `tmpHostBuff[i]=i`（0..N-1）；FP32＋SUM，**按元素跨 rank 归约——输出第 j 元素=Σ_rank j=N·j（手算 N=2：输出 [0,2]；非 [1,1]、非标量 Σ 或 N(N−1)/2）〔I，本书手算非实测；样例仅打印不校验〕**；完成后 `aclrtSynchronizeStream`（L74）→拷回打印→`aclrtFree(sendBuf/recvBuf)/FreeHost→DestroyStream`（L92-96 区）→主流程 `HcclCommDestroy→aclrtResetDevice→aclFinalize→MPI_Finalize`（L140-147）。
- **rank↔deviceID 映射**：样例 `devId=(uint32_t)procRank`（L83 区）——**单机单进程单卡假设，非通用规则**；通用映射由 rank_table.json `device_id/rank_id` 显式给出（样例 02）〔C；多机/跨机映射本文不证〔U〕〕。

### 7.2 Host→选择器真实调用链（legacy 全路径）与「无法全链证明」声明

**已证链（host 侧，全部 legacy/ascend910）**〔C〕：

```
op_base_host.cc HcclAllReduceInner(L62)                     # 入口校验/group 深度 taskAppend 分支
  →HcclAllReduceV2(...)（L118 区；910 侧 V2 实现不在本仓→见下「断点」）
  →hccl_communicator_host.cc HcclCommunicator::AllReduce(L3089)
     ├ aicpuUnfold 判定：AicpuUnfoldConfig∧IsSupportSDMAReduce∧910_93∧rankSize>1（L3094-3098）
     ├ totalSize=count*SIZE_TABLE[dtype]；OpParam 装填（L3125-3144）
     └ ExecOp(HCCL_CMD_ALLREDUCE, opParam)（L3151）
        →hccl_communicator_host.cc ExecOp(L4578)
           ├ implAlg_->GetAlgOperator(opType)（L4629 区）
           ├ algOperator->SelectAlg(tag,opParam,limit,&algName,&algDesc,&newTag)（L4649 区）
           ├ PrepareZeroCopy/CalcResRequest/PrepareCommInfo/Orchestrate（L4656-4790 区）
           └ StarsCounter(dispatcher,stream,…)（L4817 区）
  →hccl_alg.cc GetAlgOperator→AllReduceOperator（L136 区构造）
    →all_reduce_operator.cc SelectAlg(L108)＝前稿 A3 锚（完整路径：
      hcomm/src/legacy/ascend910/algorithm/impl/operator/all_reduce_operator.cc）
```

旁路（OPS_KERNEL_INFO_LIB 模式）：`hcom.cc HcomSelectAlg(L2121)→HcclSelectAlg（hccl_communicator_host L1921，重建 AlgOperator 仅算子信息查询）`——**与执行链不同模式，勿混**〔C〕。

**断点声明**：`HcclAllReduceV2` 在 910 侧仅 weak 声明（op_base.h L89）；950 侧有实现（ascend950/op_base_v2.cc L1263）。**样例最终是否落到 legacy/ascend910 选择器，缺 HCCL 算子仓（本机无）与链接期符号证据，无法端到端证明**〔U〕——正文改为**独立 legacy 选路案例**：以 `HcclCommunicator::AllReduce→ExecOp→SelectAlg` 链讲「选择如何发生」，**不宣称样例必经此链**。

**910B AIV 布尔式全展开**（`SelectAlgfor910B` L295-345 真符号）〔C〕：

```cpp
// [示意代码] 节录自 …/algorithm/impl/operator/all_reduce_operator.cc L299-341（未删节条件，注释为本书标注）
bool isOnlyAiv    = topoMatcher_->GetIsOnlyAivConfig();
bool isInlineReduce = IsSupportSDMAReduce(inputPtr,outputPtr,dataType,op);   // 地址/对齐/dtype 相关，见 device_capacity.cc
bool isRdmaReduce   = IsSupportRDMAReduce(dataType,op);
// isMeshTopo（拓扑枚举，本函数声明但 AIV 判定未用）≠ isMesh，两变量勿混：
bool isMeshTopo = topoType_∈{NP_MESH,4P_MESH,2P_MESH,1P_MESH};  bool isRingTopo=(topoType_==NP_SINGLE_RING);
bool isMesh = IsAlgTypeLevel0Mesh(algType_.algoLevel0);  // ← isAivMode 实用此（algType 层0，非 topoType_）
u64 dataSize = count * unitSize;                       // 【总字节】：全 rank 同 count 假设下的单卡负载
u64 rankCountSize = dataSize / deviceNumPerAggregation_; // 【每聚合单元（机内 8 卡）均摊字节】
bool isServNumPowOfTwo = serverNum_>0 && (serverNum_&(serverNum_-1))==0;
isSupportAivRdmaSmallCount = !isSingleMeshAggregation_ && !multiModuleDiffDeviceNumMode_ && isServNumPowOfTwo
    && (rankCountSize<=190*1024 || isOnlyAiv);          // HCCL_SMALL_COUNT_190_KB=190*1024（common.h L195，按每rank均摊）
isSupportAivRdmaMidCount  = !isSingleMeshAggregation_ && !multiModuleDiffDeviceNumMode_ && dataSize<=16*1024*1024; // 总字节
isSupportAivDeter = isSingleMeshAggregation_ && deter==ENABLE && dataSize<=8192*1024; // 总字节
isCCLBufferGE16M = !isOpbase || (in≥16M && out≥16M);    // comm buffer 实际容量
isBarrierOp = syncMode==UNLIMITED_TIMEWAITSYNCMODE;
isAivMode = (GetAivModeConfig() && !isBarrierOp) && IsSupportAIVReduce(dtype,op) && isMesh
    && isCCLBufferGE16M && (isSingleMeshAggregation_ || SmallCount || MidCount)
    && (deter==DISABLE || isSupportAivDeter);
```

**量纲明示**：`dataSize`＝**总字节（count×unitSize）**；`rankCountSize`＝**每聚合单元均摊**——190KB 阈值按均摊、16M/8M 按总量〔C：L318/L328-334 注释与常量 `common.h` L195-202〕。**isAivMode 实用 `isMesh=IsAlgTypeLevel0Mesh(algType_.algoLevel0)`而非 `isMeshTopo`（该枚举本函数声明但 AIV 判定未用）；原式含 OR 分支与排除项，前稿「五连∧」压缩不忠实，正文按本节全式且不得标「未删节」——变量映射已注。**

### 7.3 引擎平台支持：文档范围 vs legacy 源码条件（分列）

| 引擎 | 文档声明范围 | legacy 源码条件 | 新标准目录证据 |
|---|---|---|---|
| AICPU_TS | 数据面原语支持 950/A3/A2（如 HcommWriteOnThread 支持表）〔D〕；AICPU **展开配置**仅「A3 和 300I」（comm_config.cc L363 注释）〔C〕 | `SetConfigOpExpansionMode case2`：910_93/910B 才置 aicpuUnfold〔C〕；910 侧 device 版 `GetAivModeConfig(){return false}`（hccl_communicator_device L1300）〔C〕 | `include/hcomm_res_defs.h` L109-114 `CommEngine` 枚举含 CPU/CPU_TS/AICPU/AICPU_TS/AIV/CCU〔C〕；`hccl_team.h` L37 engine 字段〔C〕 |
| CPU_TS | 「Atlas A2 专用」（arch-brief §2.4）〔D〕 | ——（未逐条）〔U〕 | 枚举存在〔C〕 |
| AIV | 950/A3/A2 原语支持表＋910B 选择条件〔C/D〕 | 上 7.2 布尔式 | 同上 |
| CCU | 950PR/DT（arch-brief §2.4；ccu 文档树）〔D〕 | —— | `include/hccl/hccl_ccu_res.h` 等〔C〕 |

**结论措辞**：「AICPU 仅 A3/300I」限定于**展开配置分支**；引擎枚举与原语支持表按各接口页产品注释逐条核——**不得合并成「HCOMM AICPU 平台支持」单句**。

### 7.4 P2P 四步两端 timeline 与 buffer 保护（照录＋边界）

| 时刻 | 发端 | 收端 | 被保护 buffer | 何时可动 |
|---|---|---|---|---|
| t0 | LocalCopy sendBuf→LocalBuffer〔D：blog「数据拷贝」节；API `HcommLocalCopyOnThread`（local_operations/，950/A3/A2 支持同 Write 页式注释）〕 | notifyWait 等 ACK | 发 LocalBuffer 写入中 | t1 后可读 |
| t1 | notifyRecord→ACK（本端数据就绪） | 收 ACK | —— | 收端可发起读 |
| t2 | —— | 单边读 RemoteBuffer→recvBuf（`HcommReadOnThread`） | 发 LocalBuffer／收 recvBuf | 读期间双端禁写 |
| t3 | notifyWait 等 SIGNAL | notifyRecord→SIGNAL（读完成） | 发端 LocalBuffer **t3 后方可复用**（blog Step4 原文「以便发送端释放或复用」） | —— |

**边界**：以上为**单次传输**语义；**多轮/环形槽复用安全须双 notify 配对逐轮成立，blog 未给连轮证明**〔U〕——正文不得称「已证可无限轮转」。原语签名实证一条〔C〕：`int32_t HcommWriteOnThread(ThreadHandle, ChannelHandle, void* dst, const void* src, uint64_t len)`（文档 L28），**异步**（L23「该接口为异步接口」）、返回 0/非 0（L41-43）；完成语义靠 notify 对，非接口返回〔D〕；950 附加约束「仅 UB_CTP/UBoE」（该页约束节）〔D〕。**API 目录名≠签名**——正文引用以各 .md 原型节为准。

### 7.5 LocalReduce 源文不一致（保留歧义）

`ccu/data_movement/LocalReduce.md`：参数表 L60/L71 列 **UINT8** 六种；示例 L117-126 用 **INT8→FP32**。两处同页共存〔C〕——**属源文内部不一致，正文照录两处并标「未定」**，不得择一当全量支持矩阵，也**不得与 AIV RS 高精度二开（blog，独立实现）拼成同一结论**——两者引擎（CCU vs AIV）、层级（原语 vs 算子改造）均不同〔I〕。

### 7.6 SymWin 边界＋标签纪律＋路径

- `HcclCommSymWin*`/`symmetric_mem.md`/`zero_copy.md` 属 **HCOMM 通信域内存能力**；ch21 仅解释「域内注册/可见性」，**HIXL 单边语义对照留 ch22**，不转移〔I；前稿 §3 已按此分〕。
- 标签：源码节录〔示意代码〕（7.2 已用）；样例/命令〔需真机验证〕——**不预标「已验证 NPU」**（本书未运行）。
- 全路径修正：选择器=`hcomm/src/legacy/ascend910/algorithm/impl/operator/all_reduce_operator.cc`；常量=`…/algorithm/pub_inc/common.h`；展开配置=`…/framework/communicator/comm_config.cc`；研究日期 2026-10-09。

### 7.7 服务端实现特化链（经理定位 impl 路径，2026-10-09 实核）

- **分派**：`asc-devkit/impl/adv_api/detail/hccl/impl/hccl_impl_def.h` L20-26——`__NPU_ARCH__==2201→hccl_v220_impl.h`；`==3510→hccl_v310_impl.h`。`impl/hccl_impl.h` L18-21：2201 仅 `platform_v220/hccl_aicpu.h`；3510＝`platform_v310/hccl_aicpu.h`＋`platform_v310/hccl_ccu_v0.h`（**双特化**）。外层 `Hccl::AllReduce` 等仅 DFX 包装→`impl_.template AllReduce<commit>`（L24-31 区）。
- **AICPU 特化（两代共用 common）**：声明 `common/hccl_aicpu_def.h` L21；实现 `common/hccl_aicpu_impl.h`——AllReduce L327→CommonPrepareImpl L250、Wait L416、Commit L457、Finalize L484；`InitWorkingFlag` L68-80＝`workingFlag_=(g_coreType==AIV/AIC && GetBlockIdx()==config.blockId)`（**AICube/AIVector 指定=模板二参 `HcclServerConfig{CoreType,blockId}`，hccl_common.h L69-73；DEFAULT_CFG hccl.h L33**）；L133-141 `#if 3510→AssembleHcclMsgV2`。平台覆写：310 InitV2 context=`OpResCtx`（platform_v310/hccl_aicpu.h L30-41）；2201 InitV2 context=`HcclCombineOpParam`＋queueNum_（platform_v220 L147-160）——**上下文结构随平台变**。
- **CCU 特化（仅 3510）**：声明 `impl/platform_v310/hccl_ccu_v0_def.h` L38；实现 `hccl_ccu_v0.h`——AllReduce L24→CommonPrepareImpl L338、InitV2 L200（INIT_TILING_CCU_NEW_VERSION→newCcuFlag_）、Commit L477、Wait L499（assert handleCommitCnt_>0）、Finalize L570；`ccu/hccl_ccu_v0_prepare.h` xn 组装。**2201 无 CCU 特化文件**（platform_v220/ 仅 hccl_aicpu.h）。
- **结论**：①头注「Only AICPU supported」（hccl.h L49）与 3510 双特化不一致→**头注过窄**，非「CCU=另一 API 形态」；②AICPU 3510 不拒绝（完整特化+消息 V2）；③2201 编 CCU 模板无实现可链（错误形态未证不下）；④CoreType 指定编译期生效，AIV 版非工作核旁路（workingFlag_ 假）。
- 正文落点：21.6.1/21.6.2 新节；脚注 oI 全路径；SVG 重绘（三分范围+服务端分立陈述，跨范围不画实线）。
