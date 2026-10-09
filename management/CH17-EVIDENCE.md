# CH17 证据表（CH17-EVIDENCE）

> 2026-10-09。任务：management/tasks/CH17-RESEARCH.md。全部行号亲验自当期源码（快照见 SOURCE-BASELINE.md）；证据类型 S=源码/D=文档/R=README，限制列注明不可外推处。**只读研究，未动正文/appD。**

## 一、文件级锚点（5 组）

| # | 文件 | 行数 | 角色 |
|---|---|---|---|
| A | `asc-devkit/examples/01_simd_cpp_api/05_best_practices/03_fusion_compute/matmul_gelu_high_performance/mmad_gelu.asc` | 759 | CV 融合主样例（紧耦合循环编排） |
| B | `…/03_fusion_compute/matmul_gelu_high_performance/README.md` | ~470 | 场景/性能/机制说明 |
| C | `…/03_fusion_compute/quant_group_matmul_high_performance/quant_group_matmul_custom.asc` | 685 | 量化分组 MatMul+GELU（松耦合流水编排） |
| D | `…/03_fusion_compute/quant_group_matmul_high_performance/README.md` | ~470 | 场景/性能/边界说明 |
| E | `…/02_reg_compute/gelu_high_performance/README.md` | — | GELU 单算子优化出处（Case1 RegBase+VF／Case2 展开），ch17 只引用不重述 |

辅助：`03_fusion_compute/README.md`（样例总表）；`ops-nn/vfusion/`（8 条目，见 §五）。

## 二、mmad_gelu.asc 结构与关键行（A）

| 行号 | 符号/事实 | 类型 | 架构/限制 |
|---|---|---|---|
| L27/L30-31 | `scenarioNum=SCENARIO_NUM`；`static_assert(scenarioNum==1)` 仅 2201 分支 | S | A2/A3 编译期锁死 S1；3510 无此断言 |
| L34-36 | `COEFF_A=0.044715/COEFF_B=-1.595769`（GELU tanh 近似系数） | S | 与 ch15 GELU 变体同族 |
| L39-40 | `CFG_ROW_MAJOR_UB={CO2Layout::ROW_MAJOR,true}`／`_GM={…,false}`——**isToUB 由 FixpipeConfig 第二元控制** | S | 两架构共用此定义 |
| L42-45/L673-680 | 类模板 11 参；`__global__ __mix__(1,2) void mmad_vector_custom`；host 常量：**2201 baseM=128/stepKa=8/singleCoreN=1536/2048/24 核；3510 baseM=256/stepKa=4/singleCoreN=1024/singleCoreM=2048/32 核；baseK=64/baseN=256/singleCoreM 两代均 2048**（L688-705） | S | 与 ch16 mmad 同参数族；singleCoreM=2048 相同 |
| L56-63 | `xUB/geluOutUB = LocalTensor<float>(VECCALC, …, baseM/2*baseN)`——**每 AIV 各持 baseM/2×baseN float**；两架构同一公式 | S | VECCALC 位置；addr 由 geluOutUBAddr 递推 |
| L72-89 | A1/B1/A2/B2/CO1 缓冲与 ch16 mmad 完全同构（含 `L0_PINGPONG_BYTES=32KB`） | S | Cube 侧沿用 |
| L91-107 | **AIC/AIV 在同一双层 nBlock/mBlock 循环体内 `if ASCEND_IS_AIC/AIV` 分叉**——紧耦合：两侧迭代序完全一致 | S | 编排范式Ⅰ |
| L114-137 | `InitAicSyncFlags`：MTE1_MTE2×4＋M_MTE1×2 预置（同 ch16）；`WaitAicSyncFlags` 收尾对称等待 | S | 仅 AIC 调用 |
| L141-227 | `ProcessLoopAic`：4 事件对 A1/B1 DB＋M_MTE1，同 ch16；L227 收尾 `CopyOutAic` | S | Cube 侧 |
| L515-543(2201) | CopyOut S1：`FixpipeParamsV220`＋**`ndNum=1/srcNdStride=0/dstNdStride=0`**（ch16 版无此三字段——同结构不同用途字段集）＋`unitFlag=3`，`CFG_ROW_MAJOR_GM` | S | A2/A3 仅 GM |
| L544-558(3510) | S1 `FixpipeParamsArch3510<ROW_MAJOR>` GM；**S2：`mSize=DivCeil(curM,2)*2`（偶数对齐）、`dstStride=curN`、`dualDstCtl=0b01`、`CFG_ROW_MAJOR_UB`→`xUB`** | S | dualDstCtl 按 M 拆 2 AIV；mSize 强制偶 |
| L559 | `CrossCoreSetFlag<0x2, PIPE_FIX>(0x8)`——AIC→AIV **单向**通知，flag id 0x8 | S | 全文仅此一条 SetFlag 跨核 |
| L563-610 | `GeluFromGM`：`CrossCoreWaitFlag(0x8)`→`halfM=curM/2`、`localSubIdx=GetSubBlockIdx()%2`、gmOffset 含 `localSubIdx*baseM/2*N`→`DataCopyPadExtParams{false,…}` GM→xUB→**`SetFlag/WaitFlag<MTE2_V>(EVENT_ID0)` 自同步**→GELU（2201 MemBase/3510 RegBase）→`Set/Wait<V_MTE3>`→DataCopyPad 出 GM | S | AIV 内部管道自同步两处；pad 关闭 |
| L612-645 | `GeluFromUB`（仅 3510 S2）：wait 0x8→直接 `GeluRegBaseCompute(xUB,…)`（**无 MTE2**）→V_MTE3→出 GM | S | xUB 即 Fixpipe 落点 |
| L249-267 | `GeluMemBaseCompute`：Mul 链 x²→x³…每步 `PipeBarrier<PIPE_V>`；**输出缓冲复用为中间值**（README「无需额外中间缓冲」与代码一致） | S | A2/A3 路径 |
| L269+ | `GeluVf`：`__simd_vf__`＋`Reg::RegTensor/MaskReg/LoadAlign/StoreAlign`＋`UpdateMask`（RegBase，ch15 同族） | S | 950 路径 |
| L648-656 | 成员：xUB/geluOutUB 注释明确「S1 从 GM 读／S2 接收 Fixpipe（仅 3510）」 | S | — |

**CrossCore 同步语义（已核实，`sync_control/inter_core_sync/{key_features,CrossCoreSetFlag_ISASI,CrossCoreWaitFlag_ISASI}.md`）**：
- **计数器制，非硬件 flag 值**：每 flagId 一个计数器；Set 后由调度模块收集「所有参与核」的上报，Wait 检测计数非 0 则放行并减 1。**配对是总量配对**：模式 2 第一类=AIC 1 次 Set ↔ M 个 AIV 各 1 次 Wait；第二类=M 个 AIV 各 1 次 Set ↔ AIC 1 次 Wait。
- **模式 2（0x2）=单 AI Core 内 AIC↔所有 AIV**：AIC Set→两 AIV 的 Wait 解除；两 AIV 都 Set→AIC Wait 解除。不同 AI Core 之间模式 1/2 不互相影响（模式 0 才跨核）。
- modeId 取值 0/1/2/4（950/A3/910b 支持集见文档「modeId 支持表」）；pipe 需配对一致、flagId 需配对一致；Set 的 pipe=前置流水（完成后才上报）。
- **quant 双向握手的计数配对验证（源码可见）**：AIC `Wait(SYNC_AIV_TO_AIC)` ↔ 两 AIV 在 `VectorCompute` 外层循环尾**无条件** `SetFlag<2,PIPE_MTE2>`（L395；`taskRation` 过滤只 continue 内层计算，不跳过 SetFlag）——满足「2 AIV Set↔1 AIC Wait」总量配对，反向握手成立。`PostCompute` 补 Wait 排空未消费计数。
- **matmul_gelu 仅单向（源码可见）**：AIC `SetFlag<0x2,PIPE_FIX>(0x8)`（L559）↔每 AIV `CrossCoreWaitFlag(0x8)`（L566/614）=模式 2 第一类，配对成立；**AIC 从不 Wait 任何 AIV flag——「AIV 读毕→通知 AIC」的第二类配对全文不存在**。

**缺口（源码无保证处，如实记录；区分「机制可见」与「安全条件未证实」）**：
1. **S2 xUB 复用保护未证实**：AIC 下一 tile `Fixpipe→xUB` 与 AIV 上一 tile 读 xUB 的隔离，源码仅有单向数据就绪通知（0x8），**无任何可见的反向握手或 WaitFlag**。CrossCore 计数器机制本身不能自动提供该保证（模式 2 反向需 AIV 显式 Set+AIC 显式 Wait，代码均无）。可能依赖 Fixpipe unitFlag 块状态（对 UB 目标的语义未见文档）或 AIC 侧既有 HardEvent 等待时长掩盖——**列为未证实安全条件，写作时标「待真机验证/机制未明」，不得写成「由 XX 保证」**。
2. `GetTaskRation` 契约、quant 模板实参（U3/U4 见 §七）。
3. matmul_gelu AIC 结尾 `WaitAicSyncFlags`（L127-137）只对称等待**AIC 内部** HardEvent，不涉及跨核——勿与 CrossCore 计数混写。

## 三、quant_group_matmul_custom.asc 结构与关键行（C）

| 行号 | 符号/事实 | 类型 | 架构/限制 |
|---|---|---|---|
| L16-18 | 计算链：x[M,K]int8×weight[G,K,N]int8(NZ)→mmOut int32→per-channel 反量化→per-token 反量化→FasterGelu→Cast fp16 | S/D | 三段精度提升链 |
| L32-34/L41-45 | 场景 0/1/2（mix 1,1/1,2×DEPTH1/1,2×DEPTH4）；`SYNC_AIC_TO_AIV=5`、`SYNC_AIV_TO_AIC=3`——**双向 flag 对**；`BUFFER_NUM=2` | S | 编排范式Ⅱ |
| L92/L94 | `UB_CAL_SIZE=24*BASE_N`（Vector 单次 24 行）；`UB_REST_BYTES=118784` | S | UB 预算常量 |
| L96-105 | Tiling 常量分岔：**2201 depthA1=16/stepKa=8；3510 depthA1=8/stepKa=4；两代 depthB1=8/stepKb=4**——注意 3510 此处 depthA1=8，非 mmad 的 16（按 UB/L1 预算另调） | S | 勿跨样例混记 |
| L107-110 | `MatmulType`：A ND/B **NZ**/C **GM,ND**/Bias ND；`CONSTANT_CFG` | S | C 型位置=GM（直写 workspace） |
| L112-127 | `GetCustomConstantCFG`：`CONFIG_MDL`＋`enUnitFlag=true`＋手填 depth/step（**高阶 API 亦可常量 Tiling**） | S | — |
| L139 | `matmul::Matmul<A_TYPE,…,CONSTANT_CFG> matmulObj`——AIC 侧对象 | S | — |
| L191-221 | Init：`coreIdx=GetBlockIdx()`；**AIV 侧 `coreIdx/=GetTaskRation()`**（=2）映射回逻辑核——与 README §3 一致但实现用除法非 `/2` 字面 | S | taskRation 运行时值 |
| L224-252 | `InitUbBuffer`：AIC 直接 return；UB 布局 `GetWithOffset`：dequantMiddleResult/mulsResult/actResult/sharedTmp(2×UB_CAL_SIZE×4)——**tmpBuff 与结果区重叠复用** | S | 见 L443-447 时序不冲突注 |
| L254-292 | `Process`：`groupListGlobal.GetValue(groupIdx)` 动态 groupM（≤0 跳过）；**`preCount` 跨组余数传递＋`curBlockIdx=coreIdx>=preCount?coreIdx:coreIdx+CORE_NUM` 连续轮询**——跨 Group 负载均衡核心；Step3 `PostCompute` | S | groupList MoE 式变长 M |
| L294-334 | `MMCompute`(AIC)：`SetOrgShape(groupM,N,K)+SetSingleShape(curSingleM,…)` 每块重设；`while(matmulObj.Iterate())`：slot 满（`cubeTaskIdx>=DEPTH`）`Wait(SYNC_AIV_TO_AIC)`→`GetTensorC(mmOutGlobal[workSpaceOffset],0,true)`→`SetFlag<2,PIPE_FIX>(SYNC_AIC_TO_AIV)`；**workspace 环形 slot：`BASE_M*BASE_N*(coreIdx+(cubeTaskIdx%DEPTH)*CORE_NUM)`** | S | Iterate 粒度=BASE_M×BASE_N |
| L336-401 | `VectorCompute`(AIV)：`vecBaseM=min(UB_CAL_SIZE/BASE_N, curCubeM)`；外层 offsetN 步进=BASE_N**与 Cube Iterate 一一对应**；`DataCopyScale`→`Wait(SYNC_AIC_TO_AIV)`→内层 offsetM：`taskRation` 过滤（`vecCount%taskRation!=subBlockIdx` 跳）→`vecInQueue` Alloc→`DataCopyPad2D`←workspace→…→出 GM→`Free scale`→**`SetFlag<2,PIPE_MTE2>(SYNC_AIV_TO_AIC)`**→`vecTaskIdx++` | S | 双向握手闭环；TQue BUFFER_NUM=2 |
| L403-417 | `PostCompute`：AIC 按 `min(cubeTaskIdx,DEPTH)` 补 Wait——**收尾排空环形 slot** | S | 防收尾悬挂 |
| L419-475 | `ComputeDequantAndActivate` 五步：per-token `DataCopy+Brcb`（BROADCAST_DIM=2）→`AscendDequant`(int32×scale)→`Mul`(×perToken)→`FasterGelu`（**actTmp 复用 dequant/pertoken 空间，注释「时序上不冲突」**）→`Cast CAST_NONE`；每步 `PipeBarrier<PIPE_V>` | S | TQue 队列纪律贯穿 |
| L477-490 | `DataCopyScale`：一维 `DataCopyPad`（blockCount=1, len=curBaseN×4B）入 `scaleInQueue` | S | per-channel scale 按 N 切片进 UB |

### 三.5 host 侧实参与 workspace 总量（U3 已闭，C L611-637 逐行）

- 全局：`M=8192/N=8192/K=1024`、`BASE_N=256/BASE_K=128/GROUP_NUM=8`；`PIPELINE_DEPTH=(scenarioNum>=2)?4:1`；`SINGLE_N=1024`。
- 分架构：2201 `SINGLE_M=128/BASE_M=128/CORE_NUM=24`；3510 `SINGLE_M=256/BASE_M=256/CORE_NUM=32`（BASE_M=单次 Iterate 行数，注释原文）。
- 类型：`AType/BType=int8_t、CType=int32_t、BiasType=int32_t`。
- **`USER_WORKSPACE_SIZE = PIPELINE_DEPTH×BASE_N×BASE_M×sizeof(int32)×CORE_NUM`**（L637）——环形 slot 总字节数；代入 2201 S2：4×256×128×4×24=12.58MB；950 S2：4×256×256×4×32=33.55MB（自算，标推算）。
- 推论：单核 Iterate 粒度=BASE_M×BASE_N（非 SINGLE_M），与 L325 slot 地址公式一致。

## 四、README 性能数字（B/D，msOpProf 5 次中位数；占比=cycle 占比非峰值率）

**matmul_gelu**（M=K=N=8192，fp16 入 fp32 出）：
- A2（24 核，scM2048/N1536）：Gelu 单独 369.827μs（aiv_vec 236.506/mte2 316.672）；Matmul 单独 4227.605（mac 3083.197/0.82）；**S1=4236.944**（mac 3083.235；aiv_vec 174.327；aiv_mte2 90.315）——融合≈Cube 单独耗时。
- 950PR（32 核，scM2048/1024）：Gelu 348.868/Matmul 2601.311/**S1 2606.91/S2 2573.584**；S2 aiv_mte2=0.005（S1 57.145）；fixpipe 252.231→212.403。
- **L2 隐式收益（README 原文）**：Fixpipe 写 GM 后驻 L2，AIV MTE2 实际读 L2——S1 相比独立 Gelu mte2 降 82.2%（320.543→57.145）。**「GM 中转」≠无收益，中转数据走 L2**。
- 流水图：`figures/CVParallell_L0C_GM_UB.png/_UB.png`；`msopprof --aic-metrics=PipeTimeline`。

**quant_group**（x[8192,1024]int8，weight[8,1024,8192]int8 NZ，y fp16；GROUP_NUM=8）：
- A2 24 核：S0 583.512（vec 471.710）→S1 353.887（vec 235.871）→S2 299.286（vec 235.872）——**S2 比 S0 −48.71%；双 AIV 砍 vec 一半，4 深流水再叠 Cube 重叠**。
- 950 32 核：S0 282.717→S1 224.125→S2 204.129；S2 vec 112.218<Cube 180.347——**Vector bound 解除**。
- README 总结表（L419-420 原文）：A2 理论 Cube 188.93μs、实测 193.576=**97.60%**，仍 Vector bound（vec 235.872>mac 193.576）；950 mac_ratio 0.887「不再是 Vector 侧」。**端到端瓶颈判定=vec 与 mac 时间对比＋ratio，非单一 ratio**（L423 原文：受 Cube/workspace 同步/fixpipe/收尾共同影响）。

**限制**：两样例性能表架构/核数/singleCore 不同，禁止横排；无 A2 Scenario2 数据（编译期不支持）。

## 五、ops-nn 与仓内生态

- `ops-nn/vfusion/`：**8 个目录项＝1 个 CMakeLists.txt＋7 个算子目录**：`modulate`、`modulate_grad`、`multi_scale_deformable_attention_grad`、`multi_scale_deformable_attn_function`、`normalize_bbox`、`scaled_masked_softmax_grad_v2`、`scaled_masked_softmax_v2`——偏视觉/激活融合，无 quant/matmul 类；`ops-nn/experimental/vfusion/` 另存。仓内 CV 融合重型范式主要在 asc-devkit 样例层。
- `common/graph_fusion`：图融合（另一层概念），勿与算子内 CV 融合混谈。

## 六、README 与代码差异记录

1. README（B）称 AIC「通过 dualDstCtl=0b01 开启双目标模式」——代码还需 `mSize=DivCeil(curM,2)*2` 偶数对齐＋`dstStride=curN`，README 摘录未含；**拆分成立需三件套**。
2. README MemBase 摘录以「……」省略中间算子——完整链见 A L249-267（6 次 PipeBarrier），引用需回源。
3. quant README L191 注释举例「A2 Ceil(1024,128)=8／950 Ceil(1024,256)=4」反推 SINGLE_M=128/256——代码模板实参处未直接读到（见缺口 4）。
4. **缺口**：quant 模板实例化具体值（BASE_M/N、SINGLE、CORE_NUM=24/32 绑定）在文件尾实例化段，本次未逐行抄录——写作前补读 C 尾部。
5. matmul_gelu AIC 侧 flag 语义与 ch16 完全同构（4+2 预置），但**AIC↔AIV 通知 flag 0x8 与 AIC 内部 HardEvent 是两套**（CrossCore vs HardEvent），README 未明说，代码可证（L559 用 CrossCoreSetFlag 而非 SetFlag）。

## 七、未解清单（写作前须闭）

| # | 事项 | 动作 |
|---|---|---|
| U1 | ~~CrossCore 模式位语义~~ **已闭**：模式 0/1/2/4=计数器制；0x2=AIC↔全 AIV；总量配对（见上节） | 无 |
| U2 | S2 xUB 复用：**按「源码未显式给出反向保护证据」写**，禁写「未显现错覆」（未运行无观察）及「自然错位保证安全」猜测 | Fixpipe 对 UB 目标 unitFlag 语义无文档页→正文标待验证并给验证思路 |
| U3 | ~~模板实参~~ **已闭**：见 §三.5（host L611-637 全参） | 无 |
| U4 | `GetTaskRation`：**无独立 API 文档页**（docs 全文 grep 仅示例）；契约仅样例注释「__mix__ 下 AIV 除 2 回逻辑核」 | 正文表述为「样例所示用法」，不外推通用契约 |
| U5 | ~~FasterGelu 出处~~ **已闭**：库接口，`adv_api/activation_functions/Gelu_interface/FasterGelu.md`；原型带 `sharedTmpBuffer` 重叠约束 | 无 |


## 八、PRECHECK 落实补记（2026-10-09，reviews/CH17-PRECHECK.md 全收）

1. **AIV→AIC 回执的流水完成条件**（C L395 `SetFlag<2,PIPE_MTE2>`）：只保证**该 AIV 此前在 PIPE_MTE2 上对共享 workspace 的读取完成**；**不**等于 Vector 计算完成、更不等于最终 GM 输出完成——AIC 拿到回执复用 slot 时，该 slot 数据已被读走是唯一被保证的事实。正文叙述生命周期时按此精确表述。
2. **BUFFER_NUM=2（UB TQue 队列缓冲数）≠ PIPELINE_DEPTH（GM workspace 环形槽数）**：两套缓冲两套深度，禁混称双缓冲。场景映射：S0=1 AIV×深 1；S1=2 AIV×深 1；S2=2 AIV×深 4。
3. **CrossCore 平台差异**：950 上 Wait 模板参数（mode/pipe）生效；**旧架构模板 mode/pipe 不生效、阻塞范围不同**——引用处逐平台注，勿写「所有架构一致」。modeId 支持集以文档「modeId 支持表」为准（950：0/1/2/4）。
4. **FasterGelu 约束**（文档 L91）：**不支持 sharedTmpBuffer 与源/目的操作数地址重叠**。样例 `actTmpLocal` 复用的是**此前 PipeBarrier 后已消费的 dequantMiddleResult/pertokenBrcbLocal 区**，与本次调用的 src(`mulsResultLocal`)/dst(`actResultLocal`) 不同区——正是为满足该约束（C L443-447 注释「时序上不冲突」的准确含义）。
5. **测量版本未知如实记录**：README 版本表为最低运行要求（A2/A3≥9.0.0、950PR/DT≥9.1.0），**性能测量所用 CANN 具体版本 README 未给出**——正文记录「未知」，不得以最低版本冒充测量版本；950PR 实测不外推 950DT。
6. **同架构同 shape 才可比**：A2 583.512/353.887/299.286μs 与 950PR 282.717/224.125/204.129μS 两列独立；S1→S2 A2「vec 几乎不变而 Task 变短」是重叠收益与单单元加速区分的样例（PRECHECK 6）。
7. gelu 样例构建链补全：`cmake .. -DCMAKE_ASC_ARCHITECTURES=dav-3510 -DSCENARIO_NUM=N && make`→`python3 ../scripts/gen_data.py`→`./demo`→`python3 ../scripts/verify_result.py output/output.bin output/golden.bin`；sim 加 `-DCMAKE_ASC_RUN_MODE=sim`；切场景清 CMakeCache。quant 同构（L449-450）。**本书未运行，全部标需真机/仿真环境**。

## 九、R1 修订记录（2026-10-09，reviews/CH17-R1.md 全项落实）

1. **场景串用修正**：quant S0/1/2=1AIV深1/2AIV深1/2AIV深4 全 GM workspace，与 matmul_gelu S1/S2 通路编号是两套——正文 §17.6 已分流表述；A2 mac 列更正 192.020/192.612/193.576（168.645 是 mte1 列）。
2. **GELU 真码**：GeluMemBaseCompute=L249-281 八步 Mul/Mul/Muls/Add/Muls/Exp/Adds/Div（无 Fmad/Cast）；公式分子为 x。正文逐指令节选。
3. **行切分**：GM 路径=连续上下半块（gmOffset+localSubIdx·baseM/2·N）；Fixpipe dualDstCtl=0b01=DUAL_DST_SPLIT_M（前半 SUB0/后半 SUB1），出处 `cube_store_key_features/l0c_to_ub_dual_dst.md`——非奇偶行。图 alt 同步。
4. **同步表述**：回执方向=M AIV Set↔AIC 1 Wait（原文误 Wait）；计数随场景 AIV 数（S0 M=1）；计数器「传递完成事实、按次消费、无所有权语义」。
5. **性能归因收敛**：删「噪声级/只应两列/完全隐藏/差额即L2」断言；aic_mte2 1917.737→2096.38 记录不归因；320.551? 编辑迹清除。
6. **标签/复现**：伪分支与省略签名改[示意代码]；两例各自目录+环境前提（set_env）+真码才称节选；公式补 g/k 索引与 NZ 非转置注。
7. **脚注路径**：fusionr/fusionq 全仓库相对路径+构建文件；新增[^dualdst]。
