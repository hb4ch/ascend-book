# CH23-EVIDENCE——通算融合（MC2）源码证据账本（rev2，2026-10-09）

任务：`management/tasks/CH23-EVIDENCE-CLOSE.md`＋评审 `management/reviews/CH23-RESEARCH-R1.md`。仅研究，未写正文，未动 21/22 章。
基线（management/SOURCE-BASELINE.md）：`ops-transformer@e75072d7e751…`、`asc-devkit@28e7aba2f62e…`、`pto-isa@dd3cb0fbd5d7…`、`cann-learning-hub@a3989658…`。**本 rev2 所有引用为完整 repo/path；行号已实核。**
rev2 变更：①A3 产品支持订正；②Mc2SyncAll 定义闭环；③Wait/repeat 完成计数闭环（A2 vs 950 不再是「猜语义」）；④fallback 定论；⑤gen_task CCU 分派新证；⑥combine 独立表征（去「镜像」）；⑦未知账本收窄至 5 条。

## 0. 主线与产品支持（订正）

- **`ops-transformer/mc2/matmul_all_reduce/README.md` 产品表**：`Ascend 950PR/950DT √`、`Atlas A2 训练/推理 √`、**`Atlas A3 … ×`**（产品支持节，前 8 行）。**主线限定 A2 与 950 两平台；一切 A3 结论只许出现在 MoE 线（其 README A3=√）**。
- rev1 称「arch22 注释覆盖 A3」有误：`ops-transformer/mc2/matmul_all_reduce/op_kernel/arch22/matmul_all_reduce.cpp` L24 实为 `#if ASC_DEVKIT_MAJOR >= 9`（头文件选择），**非 A3 支持声明**；L25 注释 `arch22/A2/A3/910b/910_93` 仅文件用途描述，不构成产品矩阵证据。A2 支持以 README 产品表为准。
- MoE 线平台表：`ops-transformer/mc2/moe_distribute_dispatch/README.md`（950DT/A3/A2 均 √）与 `moe_distribute_combine/README.md` 同；kernel 入证：`moe_distribute_dispatch/op_kernel/arch22/moe_distribute_dispatch_a3.cpp` L37 `ArchTag==TILINGKEY_TPL_A3`（A2/A3 各有入口文件）。

## 1. 形态：通信在 device 侧发起，host 只见一次算子调用

- `ops-transformer/mc2/matmul_all_reduce/op_kernel/arch22/matmul_all_reduce_base.h` L143：`Hccl<HCCL_SERVER_TYPE_AICPU> hccl_;`；L48-56 `Init()`：`hccl_.Init(GetHcclContext<0>())`。
- host 任务投递：`ops-transformer/mc2/matmul_all_reduce/op_host/op_tiling/matmul_all_reduce_tiling_base.cpp` L147 `args.taskType=KfcTaskType::KFC_TASK_HCC_TASK_DELIVER`；L149 `commOrder=1 // 0先AiCPU后MM; 1为先MM后AICPU`；L166 `notifyOff=sizeof(KFCMsgBody)`；消息区结构 L56-63（`HcclAicpuOpParam msgSndArea/msgRcvArea`）。
- **gen_task 分派（rev2 新证）**：`ops-transformer/mc2/matmul_all_reduce/op_graph/matmul_all_reduce_gen_task.cpp`——`MatmulAllReduceCalcParamFunc/GenTaskFunc`：**A5 且 `comm_mode=="ccu"`→`"ccu server","ccu_stream"`（`Mc2Arch35GenTaskCallBack`）；其余（含 A5 缺省）→`"aicpu kfc server","kfc_stream"`**。即 950 CCU 路由在 host task 生成层完成。
- AICPU server 实体：`asc-devkit/impl/adv_api/detail/hccl/cc/src/aicpu_kfc/`（`mc2_server_kernel_entry.cc` 等；消费循环未读→未知①）。

## 2. Host API→注册→tiling

- 两段式样例：`ops-transformer/mc2/matmul_all_reduce/examples/test_aclnn_matmul_all_reduce.cpp` L122-133（GetWorkspaceSize→malloc→execute→`aclrtSynchronizeStreamWithTimeout(stream,10000)`）；通信域前置 L70-83 `HcclGetCommName`、L188 `HcclCommInitAll`——**域由调用方先建，算子收 `hcom_name`**。
- **fallback 定论（rev2，解 rev1 未知②）**：`ops-transformer/mc2/matmul_all_reduce/op_graph/fallback_matmul_all_reduce.cpp`（286 行）＝**host opapi 执行分派**：`MatmulAllreduceExecuteFunc` 按量化/comm 参数在 `aclnnMatmulAllReduce{,V2,V3}/Quant…V2..V5/WeightQuant…` 间选择 `EXEC_OPAPI_CMD`（L215-286 区）——**不存在「拆成 Matmul+AllReduce 两算子」的图改写**；入参校验失败返回 GRAPH_FAILED（L33-54）。
- tiling 关键决策（`ops-transformer/mc2/matmul_all_reduce/op_host/op_tiling/matmul_all_reduce_tiling_base.cpp`）：L150 `reuseMode=tileCnt+tailCnt`；L157-159 `totalCnt/turnNum/tailNum`（M 切 tile+tail）；L204-238 窗口决策：`HCCL_BUFFSIZE` 缺省 200MB（L206-213），`tileSendOff+tailSendOff>=max→MC2_BUFFER_TYPE_OUTPUT 否则 WINDOW_IN`（L226-229）；L237 `DAV_2002→强制 OUTPUT`；L1542-1549 comm_mode attr 缺省 AICPU。
- kernel 侧引擎选择：`ops-transformer/mc2/matmul_all_reduce/op_kernel/common.h` L49-50 `COMM_MODE_CCU=0/AICPU=1`、L52-60 `HcclTypeSelector`（CCU→`Hccl<HCCL_SERVER_TYPE_CCU>`）。

## 3. Mc2SyncAll 定义闭环（rev2 解 rev1 未知③）

`ops-transformer/mc2/matmul_all_reduce/op_kernel/common.h`：

- L263-266 `enum class Mc2CoreType { ON_CUBE_AND_VECTOR=0, ON_VECTOR=1, ON_CUBE=2 }`；
- L341-352 `template<Mc2CoreType type> Mc2SyncAll()`：
  - `ON_CUBE_AND_VECTOR`→`SyncAll<false>()`（AIC+AIV 全核硬件屏障）；
  - `ON_VECTOR`→`SyncAll()`；
  - `ON_CUBE`→`PipeBarrier<PIPE_ALL>()`＋`CrossCoreSetFlag<0x0,PIPE_FIX>(3)`＋`WaitFlagDevLocal(3)`（L335-338＝`CrossCoreWaitFlag(3)`）——**纯 AIC 时退化为软件 flag#3 全核互等**。
- 实例化（`ops-transformer/mc2/matmul_all_reduce/op_kernel/arch22/matmul_all_reduce.cpp` L114-127）：非量化主路径 `MM_TYPE==FP_MM`→**`ON_CUBE_AND_VECTOR`（L123/125）**；仅 `FP_MM_CUBE_ONLY` 变体才 `ON_CUBE`（L119）；quant pertoken 系 `ON_VECTOR`（L151 区）。**正文主线（非量化）按 ON_CUBE_AND_VECTOR＝硬件全核屏障引用。**

## 4. A2（arch22）kernel 主链

`ops-transformer/mc2/matmul_all_reduce/op_kernel/arch22/matmul_all_reduce_base.h`＋`matmul_all_reduce_910_general.h`：

- 入口分派 L114-127（见 §3）；`MatmulAllReduce910General::Process()`（910_general L38-44）＝bias 预处理（仅 BF16：AIV0 cast＋`SyncAll<false>`，base L88-101）→`InnerProcess(false,tileCnt)`→（tail）→`HcclFinalize()`。
- 每轮（InnerProcess L49-70）：AIC（`block_idx<usedCoreNum`）`mmOp.Init/Process`，后续轮仅 `UpdateGlobalTensor` 平移——**mm 对象跨轮复用**；全核 `PostProcEachTurn`（base L103-119）：addFlag 时 x3 加法→指针平移→`Mc2SyncAll`→notifyFlag（L37-41：AIC block0 或 AIV block0）`hccl_.Commit(handleId)`。
- `Init()` 窗口直写 L55-58：`WINDOW_IN && determinism!=1→cGM=GetWindowsInAddr(rankId)`。
- **收尾精确语义（rev2 订正，见 §5）**：`HcclFinalize`（base L121-133）＝`Wait(tileHandle)`（一次）→`Mc2SyncAll`→`Finalize()`。

## 5. Wait/Commit/Finish 完成计数——设备 HCCL impl 闭环（rev2 核心）(解「不猜代际语义」)

`asc-devkit/impl/adv_api/detail/hccl/common/hccl_aicpu_impl.h`（AICPU server 型 impl）：

- Prepare（L249-288）：`handleIdRepeat_=param.repeat`（L272）；`SetCommitTurnCntToGm(..., repeat×GetStepCntsPerRepeat, handleId)`（L275）。`GetStepCntsPerRepeat`=非 AlltoAllV 时 1（L196-200）→**AllReduce 总 turn 数=repeat**。
- `Commit(handle)`（L461-483）：每次 `SetCommitTurnCntToGm(+1)`（stepSize=0 时计 1 turn），超 `repeat×stepCnts` 报错——**每轮 Commit=Server 侧可开工一个 turn**。
- `Wait(handle)`（L416-453）：`waitCnt+=1`（stepSize 0）后**自旋 `WaitFinishCntFromGm(curMsgPos, waitCnt)`**（L231-244：`while finishGM->cnt < expectedCnt` 刷 cache 读 GM 计数）——**一次 Wait 只押韵一个 turn 的完成**。
- `Finalize()`（L486-530）：`sync` 分支 **`while Query(curHandleId)<handleIdRepeat_[handleId]` 旋等至全部 repeat 完成**（L501-506 区注释「Wait hccl task finished for last HandleId」）→发 Finalize msg→等 server 读→`ResetFinishedTurnCnt`。
- **结论（订正 rev1）**：A2 主链「单次 Wait」只保证第 1 turn；**全 repeat 收敛点在 `Finalize` 的 Query-until-repeat**。950 arch35 的 `for i<tileCnt: Wait`（`ops-transformer/mc2/matmul_all_reduce/op_kernel/arch35/matmul_all_reduce_based_all_reduce.h` L123-137）则显式消费满 repeat——**两者最终保证相同（Finalize sync 兜底），差异是中间阻塞点**：A2 提前放行 Mc2SyncAll 后续？否——A2 的 Mc2SyncAll 在 Wait 后、Finalize 前，此时仅 1 turn 有证。**正文表述：A2 路径「逐轮数据可见性由 Commit 计数与 finishTurnCnt GM 计数构成，完全收敛以 Finalize 返回为准」；不得写「A2 单 Wait=全部完成」。**
- CCU 侧：`asc-devkit/impl/adv_api/detail/hccl/impl/platform_v310/hccl_ccu_v0.h` L499+ `Wait` 同为 commit/finish 计数式（内部算法未全读→未知④收窄）。

## 6. 950（arch35）改点

`ops-transformer/mc2/matmul_all_reduce/op_kernel/arch35/matmul_all_reduce_based_all_reduce.h`：L36-37 `InitV2`＋`SetCcTilingV2(offsetof(MC2TilingHeader,mc2CcTiling))`；L40-41 `3510→cGM=workspace+nd2NzWorkLen+biasLen`（无窗口直写）；L123-137 逐轮 Wait；L46 单 tile m=rankM；L52-70 fp4x2/e1m2 半字节。引擎 `HcclTypeSelector<commMode>`（§2）。

## 7. 950 AIV URMA 融合（apace）

- 融合体：`ops-transformer/mc2/common/op_kernel/apace/kernel/fusions/all_to_all_quant_matmul/all_to_all_mx_quant_matmul_urma_impl.h`——L47-54 `UrmaCommWaitPolicy::WaitTile=CrossCoreWaitFlag<0x2,PIPE_MTE2>(tileIdx)`；L107-113 注入 `Kernel::AllToAllQbmmMxKernel<...,UrmaCommWaitPolicy>`；L208-218 AIV/AIC 分派（`localMatmul==1` 先本地块）；AIV L220-243 逐轮 Commit/Wait/`CrossCoreSetFlag`＋收尾 `dcci` 整 commBuffer（L243-247）；AIC `RunMatmul` L313-323 `aGmAddr=selfWinAddr`、splitKNum 按 mode 0/1/2（L299-304）。
- 底层：`ops-transformer/mc2/common/op_kernel/apace/core/aiv_comm/all_to_all_udma_get.h` 等，基于 `asc-devkit` `adv_api/hcomm/hcomm.h`（ch21/22 已审同族）。
- 宿主：`ops-transformer/mc2/allto_all_matmul/`（README 950/A3/A2 √）`op_kernel/arch35/allto_all_mx_quant_matmul_arch35.h`＋`_pipeline.h`。

## 8. MoE：dispatch 推写＋combine 拉取归约（rev2 独立表征，去「镜像」）

- **950 dispatch**：`ops-transformer/mc2/moe_distribute_dispatch/op_kernel/moe_distribute_dispatch.h` L890-900 `Process=AlltoAllDispatch→SetStatus→WaitDispatch→LocalWindowCopy→UpdateTokenNumsOut`（全 AIV）；win 寻址 L82-90＋L214 `GetHcclContext<HCCL_GROUP_ID_0>`；状态区偏移 `WIN_STATE_OFFSET=384KB`（`moe_distribute_dispatch_v2/op_kernel/moe_distribute_v2_constant.h` L49）、`A5_MTE_STATE_WIN_SIZE=1MB`/`EP_RANK_OFFSET_STEP=1024`（`ops-transformer/mc2/common/op_kernel/moe_distribute_base.h` L35-38）；**完成判定=状态字轮询**：`WaitDispatch` L653-685 `while(sumOfFlag∉[min,max]){DataCopy(status);GatherMask;Sum;}`。
- 3510/A3 地址模型分叉：`ops-transformer/mc2/common/op_kernel/moe_distribute_base.h` L459-505——A5 `windowsIn[rankId]+偏移`；A3 `localWindowsIn`/`remoteRes[rankId].nextDevicePtr→windowsIn`（L497-501）。`DataplaneMode{HOST=0,AICPU=1,AIV=2}` L353-357。
- **950 combine（rev2 新读）**：`ops-transformer/mc2/moe_distribute_combine/op_kernel/moe_distribute_combine.h`（695 行）`Process` L??＝`BuffInit→ExpertAlltoAllDispatchCopyAdd→AlltoAllBuffInit→SetStatus→WaitDispatch→LocalWindowCopy`——**归约=本端 AIV 向量加法**：`ExpertAlltoAllDispatchInnerCopyAdd`（L427+）从各 rank win `DataCopy` 进 UB→`Muls(scale)`＋`Add` 累加（L640-647 区）——**非 HCCL reduce**；专家份寻址 `GetWinAddrByRankId(ep,expertIdx)`（L75-79）；共享专家份单独累加（L649-660 区）。同样 status 轮询收敛。A2/A3 入口 `arch22/moe_distribute_combine_{a2,a3}.cpp`（`TPL_A2/TPL_A3`）；A2 layered 实现于 `moe_distribute_combine_v2/op_kernel/arch22/`（未逐行→未知⑤）。
- 约束（README 实文）：dispatch/combine 配套；输出元素「不同型号/算法/版本可能不同，不得业务依赖」；A2 `HCCL_BUFFSIZE>=(BS*epWorldSize*min(localExpertNum,K)*H*4B+4MB)`；950DT 仅 UB Memory 通信（kernel 对应实现未定位→未知⑥）。

## 9. PTO gemm_ar 对照（独立后端，不拼链）

`pto-isa/kernels/manual/a2a3/gemm_ar/`（A2/A3，910B 参考）：双 kernel 双 stream（`GemmComputeKernel` AIC／`GemmCommAllKernel` AIV）＋无锁 ready queue（`ready_queue.hpp`，TTEST/TWAIT）＋RS/AG 单循环 overlap＋publish fence `pipe_barrier(PIPE_ALL)+dsb(DSB_DDR)`（README 优化节）；PTO 通信指令操作 HCCL RDMA 窗口（`common.hpp` HcclRemotePtr）；`run.sh` 一键 MPI+HCCL。**与 MC2 差异：host 双流并发 vs 单 kernel 内设备通信。**

## 10. 教程对照

`cann-learning-hub/tutorials/MC2_fused_operator_development/01_MC2_basic_fused_operator_development/01.03_*.ipynb`：950 Kernel 直调 Matmul+ReduceScatter；AIC mm→AIV `WriteStatus/ReadStatus 轮询→ReduceGatherFromWin`；`SOC_VERSION=ascend950pr_957c`。教学镜像，非生产链证据。

## 11. SuperPod/PD/RL 边界

`cann-learning-hub/blogs/inference/deepseek_r1_superpod_inference_optimization/….md`（11 节点 7P8-1D32、608QPM＝厂商实践数字，无复现脚本）；`deepseek_v4_supernode_support.md`（宣传综述）；RL=`hixl_rl_tail_latency_optimization/`（ch22 域）。**仓内无超节点拓扑源码**→正文只写系统构成×算子行为。

## 12. 复现与依赖

`bash build.sh --pkg --soc=ascend910b|ascend950 --ops=matmul_all_reduce`（`ops-transformer/build.sh` L107/L110）；运行需 ≥2 同型卡＋HCCL 域＋HCCL_BUFFSIZE 预检。本机无 NPU→`[需真机验证]`；不发明新标签。

## 13. 主锚（完整 repo/path）

1. `ops-transformer/mc2/matmul_all_reduce/op_kernel/arch22/matmul_all_reduce_base.h`
2. `ops-transformer/mc2/matmul_all_reduce/op_host/op_tiling/matmul_all_reduce_tiling_base.cpp`
3. `ops-transformer/mc2/matmul_all_reduce/op_kernel/arch35/matmul_all_reduce_based_all_reduce.h`
4. `asc-devkit/impl/adv_api/detail/hccl/common/hccl_aicpu_impl.h`（Wait/Commit/Finish 计数机）
5. `ops-transformer/mc2/common/op_kernel/apace/kernel/fusions/all_to_all_quant_matmul/all_to_all_mx_quant_matmul_urma_impl.h`
辅：`ops-transformer/mc2/matmul_all_reduce/op_kernel/common.h`（Mc2SyncAll）、`ops-transformer/mc2/matmul_all_reduce/op_graph/{gen_task,fallback}.cpp`、`ops-transformer/mc2/moe_distribute_{dispatch,combine}/op_kernel/…`、`pto-isa/kernels/manual/a2a3/gemm_ar/`。

## 14. 未知项账本（rev2 余 5 条）

①AICPU KFC server 消费循环未逐行（`aicpu_kfc/`）——正文写「host 填消息/finishTurnCnt 计数、server 消费」止步；②CCU server 内部算法未读（`hccl_ccu_v0*`）——只写「attr 可选、host 分派 ccu_server/ccu_stream、Wait 同为计数式」；③A2 layered/full-mesh MoE 内部协议未逐行——只写入口分派＋文件尺度；④950「UB Memory 通信」kernel 对应实现未定位——只引 README 原句；⑤`all_gather_matmul`（备选）内核未读——如需对比须二次研究。
