# CH23-OUTLINE——第23章 通算融合：一个 GEMM+AllReduce 的完整旅程（rev2，2026-10-09）

依据：`management/CH23-EVIDENCE.md`（rev2）＋STYLEGUIDE §「读者理解与图表」（2026-10-09 用户新增）。**读者优先**：全书围绕一个可追随的主例回答三个问题——**为何把 M 切块？算完的一块何时交给通信？结果何时可读？**MoE 仅一个补充案例；URMA/PTO/系统场景降为延伸对照。目标 7 节 ≈9.5k 字（中文 ~8k），每节答一问、低密度、短段。

## 主例贯穿设定

`ops-transformer/mc2/matmul_all_reduce`（A2 非量化主路径）：8 卡、x[M,K]×W[K,N]→AllReduce。随章复用同一组具体数字示例（如 M=4096 切 4 tile，仅示意切分结构，**不标任何性能数字**）；每节开头一句「上一节我们知道了…这一节回答…」。

## 章节规划（7 节）

### 23.1 问题：算完再通信，慢在哪（~1.0k）
- 先给串行时间线直觉（算完全部→再通信全部），指出通信设备空闲/Cube 空闲交替；
- MC² 解法一句话：M 切块后「第 2 块的计算」与「第 1 块的通信」重叠（引 asc-devkit `docs/zh/guide/operator_practice/best_practices/mc_operator_tuning.md` L5 机理句，重绘不截原图）。
- **图①（概念图，Mermaid）**：串行 vs 切块流水两条时间带。*图前问题：为什么切块能省时间？* *图后带读：注意第二块 MM 与第一块 Comm 并行；本图只示结构，不带时间数值。*
- 边界一句：融合≠消除 GM 中转——中转只是换成了 HCCL window（细节留给 23.3）。

### 23.2 认识主例：一次 `aclnnMatmulAllReduce` 调用（~1.0k）
- 用户视角：两段式调用＋前置 `HcclCommInitAll`（examples 实录，`[需真机验证]`）；约束精选（A2 1/2/4/8 卡、950 至 64 卡、x2 限制）只留影响使用的；
- **图②（数据流图）**：rank0..3 视角 x/W→MM→c→AllReduce→out，及「hcom 名字→通信域」关系。*图前问题：这个算子在网格上发生了什么？*
- 三层预告：host tiling／kernel／设备 HCCL server——本章后续逐层下潜。

### 23.3 Host 侧准备：切多少、放哪里、交给谁（~1.3k）
- 切分：M→tile+tail（`commOrder=1 先MM后AICPU`、`turnNum=tileCnt+tailCnt`——先算后通信的顺序在 host 写定）；
- 放哪里：窗口决策树（`HCCL_BUFFSIZE` 缺省 200MB→WINDOW_IN 直写 vs OUTPUT 独立缓冲；确定性模式退回；DAV_2002 强制 OUTPUT）——**small 表：三种落点×取舍**；
- 交给谁：gen_task 分派（aicpu kfc server / 950+ccu→ccu server）＋KFC 任务消息——通信是 device 侧发起的，host 只投递。
- *节末句：准备完成，进入 kernel。*

### 23.4 设备侧主循环：算一块，交一块（~1.8k，核心）
- A2 骨架逐段带读（只讲主线非量化）：`Init`（窗口 remap cGM；notifyFlag=仅 0 号核）→每轮「AIC `mm.Process`→全核 `Mc2SyncAll`→0 号核 `Commit`」→指针平移进下一轮；
- **回答本章核心问题½：算完的一块何时交给通信？＝每轮末尾 Commit；重复调用 AllReduce(repeat=tileCnt) 只登记一次、逐轮放行。**
- Mc2SyncAll 三形态小表（ON_CUBE_AND_VECTOR 硬件全核屏障为主线）；
- bias/BF16 特例一段带过（AIV0 cast）。
- *图②b（可并入图②的下半）：单 rank 内 AIC/AIV/HCCL-server 三泳道一轮数据流。*

### 23.5 结果何时可读：commit 计数、finish 计数与 Finalize（~1.5k，核心）
- 设备 HCCL 实现的三本账：`handleIdRepeat`（登记总量）、commitTurnCnt（GM，每 Commit+1）、finishedTurnCnt（GM，server 完成轮数）；`Wait`=自旋直到 finish≥已 Wait 数；**Finalize 兜底 Query 直到 repeat 全满**。
- **回答核心问题②：结果何时可读？＝`Wait` 返回仅保证部分轮；完全收敛以 `Finalize` 返回为准**——A2 主链单次 Wait 的真实含义。
- **图③（关键同步时序图，Mermaid sequenceDiagram）**：AIC(0号)↔GM 计数↔AICPU Server 三方：Prepare(repeat=N)→逐轮 Commit→finishTurnCnt 递增→Wait/Finalize 收敛。*图前问题：Wait 返回时数据都到了吗？* *图后：指出单 Wait 只押 1 轮、Finalize 才封顶。*
- 950 差异一段：显式 for-Wait×tileCnt＋InitV2/SetCcTilingV2＋3510 workspace 中转——**同一收敛保证、不同中间阻塞点**（对照小表 3 行）。

### 23.6 补充案例：MoE dispatch/combine——推与拉（~1.6k）
- dispatch（950 全 AIV）：推写 token→win，状态字登记；combine：从各 rank win 拉回＋**本端向量加法归约（非 HCCL reduce）**→写回；完成判定=状态字轮询（GatherMask+Sum 收敛窗口）。
- **与前两节并成「设备侧同步三范式」收束表**：①Commit/finish 计数（23.4-23.5）②CrossCore flag 嵌调度器（延伸，见 23.7 URMA）③状态字轮询（本节）——各答「谁通知谁、在哪计数、何时放行」。
- A2/A3 双入口与 3510/A3 地址模型分叉一句带过（细节脚注）；约束只留「dispatch/combine 配套、输出不得被业务依赖、HCCL_BUFFSIZE 公式示例」。

### 23.7 延伸对照与边界（~1.3k）
- **URMA 融合（950）**：AIV 通信/AIC 计算、等待嵌进 matmul 调度器（`UrmaCommWaitPolicy`）——范式②的实例；`dcci` 整 cache 刷=设备 cache 一致性坑实例。0.4k。
- **PTO gemm_ar（A2/A3）**：双 kernel 双 stream＋ready queue——host 侧并发路线；「与 MC2 不可拼为同一调用链」。0.3k。
- **系统场景**：SuperPod/PD/RL 仅「系统构成×算子行为」定性＋博客数字须注出处（11 节点 7P8-1D、608QPM 等，不可复现声明）；无拓扑源码锚→不写拓扑。0.3k。
- 复现块（构建/运行/依赖缺口，`[需真机验证]`）＋章末脚注（主锚 5＋辅，全 repo/path）。0.3k。

## 图表清单（3 图 2 表，每图一问）

| 编号 | 形态 | 回答的问题 | 落点 |
|---|---|---|---|
| 图① | Mermaid 时序带 | 切块为何能重叠计算与通信 | 23.1 |
| 图② | 数据流（rank×阶段矩阵） | 这个算子在网络与单卡内如何搬数据 | 23.2（23.4 复用下半） |
| 图③ | Mermaid sequenceDiagram | Wait 返回≠全部完成，收敛在哪 | 23.5 |
| 表A | 3 行 | 缓冲落点取舍（window/output/确定性） | 23.3 |
| 表B | 3 行 | 设备侧同步三范式 | 23.6 |

图①③先写 Mermaid 草稿随提纲评审；成稿后按 STYLEGUIDE 渲染检查（文字/箭头/裁切/阅读顺序）。**无性能曲线、无虚构时间数值。**

## 写作纪律（自 STYLEGUIDE 新增条款落地）

- 每节=一个问题→例子→机制→边界；行号/分支/平台矩阵入脚注与 `CH23-EVIDENCE.md`，正文不串行号；
- 缩写首现解释（MC2/MTE/AIV/AIC/KFC/window）；短段；关键使用条件（Wait 语义、卡数、BUFFSIZE）随结论正文出现，不藏脚注；
- 运行性标签沿用全书四标签；无 NPU→主线链路`[需真机验证]`；
- 字数 ~9.5k（中文 ~8k），无重复凑字。

## 待经理裁定（不阻塞提纲评审）

①图①③ Mermaid 草稿是否随本提纲先审（建议是）；②23.7 URMA/PTO 深度是否再压（现 0.7k 合计）；③章名是否从「通算融合与大规模系统」改窄为「通算融合：以 MatmulAllReduce 为镜」（更贴单主线）——现提纲按旧章名占位 `docs/05-comm/ch23-supernode.md` 不动。
