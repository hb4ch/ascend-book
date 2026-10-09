# CH17 提纲（CH17-OUTLINE）

> 2026-10-09。配套 `CH17-EVIDENCE.md`（下称 EV §n）。目标 8–10k 中文（深度目标内）；实战章底线 4k 已含余量。**读者可复演**：每节给出可跟着走的数据/控制走查，不做 API 罗列。图表 3 幅＋表 3 张（预算内）。

## 章定位与开篇（≈600 字）

- 承接：ch16 末 Fixpipe 出口族谱（16.6）与 L0C→UB 直通是本章硬件地基；ch15 RegBase/VF 是 Vector 侧武器。
- 破题：**CV 融合≠把两个算子写进一个文件**。AI Core 内 AIC/AIV 双单元、`__mix__(a,b)` 任务模型、以及「Cube 结果如何交给 Vector」的三条通路（GM 中转/L2 隐式/L0C→UB 直通）才是本体。
- 表 17-1 样例版本矩阵（两样例×三架构×CANN 版本，EV §一；**软件要求≠实测环境**声明沿用 ch16 体例）。

## 17.1 `__mix__` 任务模型：一个核函数，两套执行流（≈900 字）

- `__global__ __mix__(1,2)` 语义（EV A L676）：1 AIC＋2 AIV 绑定为一条逻辑核；`ASCEND_IS_AIC/AIV` 编译期分叉。
- 三套 ID 辨析（可复演走查①：给定 blockIdx 手算三个值）：
  - `GetBlockIdx()`：AIC/AIV 各自独立编号（EV A L207 注/C L207-213）；
  - `GetSubBlockIdx()%2`：AIV 子块（EV A L572/L630）；
  - `GetTaskRation()`：运行时比值，quant 用除法映射回逻辑核（C L213）——**与 README「/2」字面不同，以 API 为准**。
- 核间同步原语预讲：CrossCore 计数器制、模式 0/1/2/4、**总量配对**（1↔M / M↔1）；modeId/pipe/flagId 配对一致（EV「CrossCore 同步语义」节）。**模式 2 的 AIC→AIV 与 AIV→AIC 是两类独立配对，无自动双向**。
- 图 17-1（SVG 重画）：逻辑核解剖——1 AIC＋2 AIV、ID 空间、flag 计数器示意。

## 17.2 范式Ⅰ 紧耦合循环：mmad_gelu 精读（≈1800 字，全书重点之一）

- **编排**：AIC/AIV 在同一双层 nBlock/mBlock 循环体内分叉（A L91-107）——迭代序锁死，同步耦合强。Cube 侧复用 ch16 全套（4+2 HardEvent 预置，A L114-137/L141-227），一句话带过不重述。
- **Scenario 1 GM 中转走查（可复演②，A2 视角）**：
  1. AIC `CopyOutAic`：`FixpipeParamsV220`（+ndNum/srcNdStride/dstNdStride 三字段——ch16 版无，EV §六.1）ROW_MAJOR 直写 GM，`unitFlag=3`；
  2. `CrossCoreSetFlag<0x2,PIPE_FIX>(0x8)`（L559）；
  3. 每 AIV `WaitFlag(0x8)`→**各领 halfM=curM/2 行**（gmOffset 含 `localSubIdx*baseM/2*N`，L572-575——手算示例：mBlockIdx/baseM/localSubIdx 代入）；
  4. `DataCopyPad` GM→xUB（PadExt{false}）→**自同步 `Set/Wait<MTE2_V>`**→GELU（A2 MemBase：Mul 链+每步 `PipeBarrier<PIPE_V>`，输出缓冲复用为中间值）→`Set/Wait<V_MTE3>`→写回 GM。
  5. **AIV 内部两处自同步的意义**：MTE2→V、V→MTE3 管道边界，与跨核 flag 正交。
- **Scenario 2 UB 直通（仅 950，走查③）**：`dualDstCtl=0b01`＋`mSize=DivCeil(curM,2)*2` 偶对齐＋`dstStride=curN`＋`CFG_ROW_MAJOR_UB`→xUB（L544-558）——**拆分成立是三件套**（EV §六.1）；AIV 无 MTE2 直接算（L612-645）。
- **xUB 复用：源码可见机制 vs 未证实安全条件**（EV 缺口 1，按经理核查口径写）：可见=单向 0x8 通知；AIC→AIV 反向握手不存在且 CrossCore 计数器不自动提供；结论表述为「本样例未显现错覆，机制依赖未证实，列待真机验证」。**不写「由 XX 保证」**。
- GELU 双实现对照表：MemBase（A2，UB 内 PipeBarrier 串行）vs RegBase/VF（950，寄存器内）——引 ch15，一句机制+ EV A L249-267/L269+。

## 17.3 茬式Ⅱ 松耦合流水：quant_group_matmul 精读（≈1800 字）

- **场景**：per-token 量化分组 MatMul（x int8×weight[G,K,N] int8 NZ→int32→per-channel→per-token→FasterGelu→fp16；EV C L16-18）——MoE 式 `groupList` 动态行数。
- **任务分配解耦（与范式Ⅰ对照核心）**：`Process` 按 `curBlockIdx` 跨组连续轮询＋`preCount` 余数传递（C L254-292，可复演④：GROUP_NUM=8、CORE_NUM=24 手算块分配）；AIC/AIV **不再共享循环体**，靠 workspace 环形 slot＋双向 flag 解耦。
- **环形 workspace slot 机制（走查⑤）**：AIC `Iterate()` 每产出 BASE_M×BASE_N 块→slot 满则 `Wait(SYNC_AIV_TO_AIC)`→`GetTensorC(workspace,BASE_M*BASE_N*(coreIdx+(idx%DEPTH)*CORE_NUM),true)`→`SetFlag(AIC_TO_AIV)`（C L321-327）；AIV 外层 offsetN 与 Iterate 一一对应→`Wait(AIC_TO_AIV)`→内层按 `vecBaseM=min(UB_CAL_SIZE/BASE_N,curCubeM)` 切行→TQue 队列纪律→`Set<2,PIPE_MTE2>(AIV_TO_AIC)`（C L395）→`PostCompute` 补 Wait 排空（C L403-417）。
- **双向握手计数配对验证**：AIC 1 Wait↔2 AIV Set（SetFlag 在外层尾**无条件**执行，taskRation 只跳内层——EV「CrossCore 同步语义」节）——范式Ⅱ握手闭环成立，与范式Ⅰ单向对照。
- **反量化五步链**（C L419-475，走查⑥数据变换：int32→×scale[j]→×perToken[i]→GELU→fp16，每步 UB 张量与 TQueue 进出）；**临时空间复用**：actTmp 覆盖 dequant/pertoken 区（「时序不冲突」注释＋PipeBarrier 序）。
- 高阶 API 也能常量 Tiling：`CONFIG_MDL+enUnitFlag+手填 depth/step`（C L112-127）——修正「常量 Tiling=基础 API 专属」可能的误解；**2201 depthA1=16 vs 3510=8 分岔勿混**（EV §三）。

## 17.4 两种编排范式对照（≈600 字，表 17-2）

| 维度 | Ⅰ 紧耦合循环（mmad_gelu） | Ⅱ 松耦合 slot（quant_group） |
|---|---|---|
| 迭代序 | AIC/AIV 同一循环体锁死 | 各自循环＋flag/slot 解耦 |
| 跨核同步 | 单向 0x8×1 | 双向 5/3＋DEPTH 深度＋PostCompute |
| 数据交接 | GM 或 UB 直通（per-tile 双份 xUB half） | workspace 环形 int32（DEPTH×CORE_NUM 个 slot） |
| 适用 | 后处理轻、tile 均匀（GELU） | 后处理重、形状动态、需流水重叠（量化） |
| 风险 | xUB 复用保护未证实（§17.2） | slot 满等待链／收尾悬挂需 PostCompute |

*表 17-2 由源码结构归纳；「适用」列限本两例观察，不外推。*

## 17.5 数据通路三态与收益边界（≈900 字）

- 三态数据流图（图 17-2 mermaid）：GM 中转／L2 隐式命中／L0C→UB 直通——**A2 只有前两态**（static_assert 编译期锁，A L30-31）。
- **「GM 中转」≠零收益**：Fixpipe 写 GM 后驻 L2，AIV MTE2 实读 L2——950 S1 aiv_mte2 320.543→57.145（−82.2%，EV §四 README 原文）；**「中转开销被 L2 隐式优化吃掉大半」是 README 明示机理，非本书推测**。
- S1→S2 增量：950 2606.91→2573.584（−33μs）；aiv_mte2→0.005；fixpipe 252.231→212.403——**直通省的是 MTE2 与部分 fixpipe，不是免费**（mte2_aic 反升 1917→2096? 如实并列）。
- 收益上界判断（走查⑦）：融合后 Task≈max(Cube,Vector) 而非求和——判据=vec 与 mac 时间对比＋ratio＋等待链；**A2 quant 仍 Vector bound（235.872>193.576）vs 950 已解除（112.218<180.347）**同构对照（EV §四）。**「占比高=瓶颈」保留意见沿用 ch16 16.7**。

## 17.6 量化数据类型链与精度路线（≈700 字）

- int8×int8→int32 累加→fp32 两级反量化→GELU→fp16 Cast：**每步精度/舍入**（CAST_NONE 语义，C L473）与为何 per-channel 在前 per-token 在后（结合律与数值域，按代码顺序陈述不外推数学证明）。
- weight 预转 NZ 离线布局（C L111 `CubeFormat::NZ`）——ch16 B 转置双层真相的量化版。
- scale/perToken 的 GM→UB 路径与队列（`scaleInQueue` 一维 Pad；per-token Brcb BROADCAST_DIM=2，C L477-490/L419-429）。
- fp32 出（matmul_gelu）vs fp16 出（quant）的 Fixpipe 量化差异：`F322F16` 随路 vs Cast 指令——两例对照。

## 17.7 失败模式、限制与未证条件清单（≈600 字，表 17-3）

static_assert 编译锁；A2 无 L0C→UB；xUB 反向握手未证（待真机验证标注）；slot 满死锁风险（DEPTH 与消费速率错配——代码以 Wait 链解，叙述机理）；`taskRation` 契约未读（U4）；FasterGelu 出处（U5）；UB 预算常量（UB_CAL_SIZE/REST_BYTES）如何约束 vecBaseM。**每条注明证据等级（源码可见/文档可见/未证实）**。

## 17.8 仓内生态与复现入口（≈400 字）

- ops-nn/vfusion 8 条目如实陈述（偏视觉/激活，无 quant 类；graph_fusion 另层概念）——**重型 CV 融合范式在 asc-devkit 样例层**。
- 复现：CMake `-DSCENARIO_NUM`（gelu 1/2；quant 0/1/2）×`-DCMAKE_ASC_ARCHITECTURES`；gen_data→run→verify；`msopprof --aic-metrics=PipeTimeline` 流水图。**均标 `[需真机验证]`，本书未运行**。
- 陷阱表（6-8 行，承 ch16 体例但全换 CV 项）。

## 图表清单（3 图 3 表内）

1. 图 17-1 SVG：`__mix__(1,2)` 逻辑核解剖＋ID/flag 计数器（新画，`docs/figures/ch17-mix-core.svg`）。
2. 图 17-2 mermaid：三态数据流（GM/L2/UB 直通）＋同步 flag 位点。
3. 图 17-3 mermaid：环形 workspace slot 时序（DEPTH=2/3 例，AIC/AIV 交错）——**或**改 SVG 视复杂度。
4. 表 17-1 版本矩阵；17-2 范式对照；17-3 失败模式分级。

## 写作纪律（自查清单）

- 性能数字五要素（版本/架构/shape-dtype/口径/来源）＋「msOpProf 5 次中位数」注明；占比≠峰值率（ch16 16.7 术语延续）。
- 源码可见/文档可见/未证实三级标注；U1 已闭、U2-U5 写作前闭（EV §七）。
- 不动 ch16 相关文件与 appD（经理正收尾）；交叉引用 ch15（RegBase）、ch16（16.3/16.6）只引不改。
- 交付后 STATUS 待审；不 commit/push。

## 字数预算合计

≈600+900+1800+1800+600+900+700+600+400=**8300 字目标**（±10%），核心深度达 8–12k 带内；如 17.2/17.3 走查写透超至 9k+，在交付报告声明覆盖情况（U3/U4/U5 处理方式）。
