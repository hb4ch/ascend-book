# CH18 提纲（CH18-OUTLINE）

> 2026-10-09。配套 `CH18-EVIDENCE.md`（下引 EV §n/E 编号）。目标 9–11k 中文；本章为实战收官（★章），深度目标上限 12k。所有机制讲解以 **arch35 regbase（950）为主线、arch22（A2）对照**，U 项未证处显式标注；无 NPU，全程「未实测」口径。

## 章定位（≈500 字）

- 收官：ch15 Vector 极限＋ch16 Cube 全路径＋ch17 CV 协同——FA 是三者总装：两次矩阵乘＋online softmax＋四级流水＋跨核握手，一个核内全占。
- 与第 6 章 attention 库/第 13 章算子库导览呼应但不重复：本章下钻**单算子内核实现**（ops-transformer/attention/flash_attention_score 真码）。
- 训练（flash_attention_score/backward）与推理（fused_infer_attention_score 等）分家；prefill/decode 不混谈（EV E16/U11）。

## 18.1 问题与算法骨架（≈1200 字）

- 注意力=两次矩阵乘夹 softmax；FlashAttention 核心改动=**分块在线 softmax**：不落完整 S×S 分数矩阵。
- 数学递推完整推导（可复演①数值例铺垫）：块 t 到 t+1，`m_new=max(m_old,rowmax)`、`l_new=l_old·e^{m_old−m_new}+Σ…`、`O=O·(l_old/l_new 重缩放)+P·V`——**三个量各重缩放一次**，复杂度 O(S²D) 时间不变、激活 O(SD)。
- 与真码对应预告：m=softmaxMax、l=softmaxSum、重缩放=FlashUpdateNew（E7/E8）。

## 18.2 仓库地图与模板体系（≈800 字）

- 目录结构：op_kernel/{arch22,arch35}、common 共享 vf、op_host tiling、docs 设计文档（E 锚点表）。
- 模板矩阵：noquant/quant×train/infer×布局（BNHD/TND）×特化（empty/sparse/RCM）——E12；`flash_attention_score.cpp` 697 行入口如何按 TilingKey 选实例（E12/B）。
- **声明讲解主线=arch35 regbase**；arch22 为上一代 API 风格（U4 对照深度受限，如实）。

## 18.3 四级软件流水：FA 的心跳（≈1500 字，全书重点）

- 主循环解剖（E1 真码节选＋注）：taskId 单调增、`runInfo[taskId&3]` 环、前 3 拍填充、`notLast*` 收敛——**软件流水把 CV 串行依赖摊成四级重叠**。
- 与 ch17 两范式的关系：FA=范式Ⅱ的极致版——不是环形 slot 而是**每级独立缓冲策略**（E3：mm1 UB DB/mm2 GM 3buff/bmm2Write2Ub 编译期岔路）。
- preload 架构差（E11）：A2 双发→MTE2 bound 设计意图；950PR 三发——引用设计文档原文，**非实测结论**。
- 同步网：CrossCore（Buffer 携带 SyncType 自动 Set/Wait，E4）＋HardEvent 单元内（V_MTE3 等）——层次表沿用 17.2 三层。
- 图 18-1（SVG 新画）：四级任务×时间甘特＋缓冲环＋同步位点（标示意）。

## 18.4 Vec1：从分数到 P（≈1300 字）

- 流程：WaitCrossCore→mask/pse 挂点（E13）→**VF softmax 按 s2≤256/≤512 模板特化**（E5）→max/exp/sum（half 存储，U7）→**cast half 写 L1 当 mm2 的 A**（E6，含 subBlockIdx 半块偏移与 64 对齐）。
- CV 交接①细讲：为什么 P 落 L1 而非 GM/L2——mm2 的 A 侧本就走 L1（ch16）；Vec 直写 L1 的通路与约束。
- dtype 链：mm1 fp32 累加（U1 标注）→softmax fp32 计算→P cast INPUT_T——每步精度陈述+U。

## 18.5 Vec2：online 更新与输出（≈1300 字）

- `ProcessVec2` 主路/短路（s2≤128 NoGlobalUpdate，E7）/**末块重载**；`FlashUpdateBasicVF` 递推真码全录（U8 补全后）——**寄存器级，无 UB 往返**。
- 三重缩放落地对照：O 缩放（expMax 比）、l 累加、最终 cast OUTPUT_T；softmaxMax/Sum GM 副产物（E9，LSE 用户可取）。
- 数值例接线：18.1 手算例的每一步对应此处哪条指令——**全书唯一完整数值走查**。

## 18.6 mask、尾块与工程特化（≈900 字）

- 因果 mask 的块级裁剪（上三角→s2LoopLimit 收紧，A L296 `s2LoopLimit` 即此）、pse 两式（README）、drop 独立通路、prefix/padding/learnableSink 变长挂点（E13）。
- 尾块：s1Base 尾/TND 变长（E14 正倒序分核防长尾）——**负载均衡是真码显式设计**。
- 特化模板举隅（E12）：empty/AA_INVALID_LINE 高精度/Fp8 deScale 族——点到为止。

## 18.7 Tiling 与资源账（≈800 字）

- CV 基本块 512KB 推导（E10 原文）：通信开销 vs buffer 容量折中；1:16 配比与 nRatio=8；核内再切 32KB。
- arch35 tiling：块尺寸=模板选择（S1∈16..256/S2∈16..512，已闭）；场景取值 U5′：s1/s2Base、workspace 组成（mm2 GM 三缓冲大小公式 B L286-291）。
- 与 ch16「base 受 L0C 容量反推」方法论呼应：FA 的 base 是 **CV 交互粒度**，约束源不同。

## 18.8 性能、复现与边界（≈700 字）

- 性能口径：仓内无统表（EV §三）——给结构性结论（E10/E11）＋「本书未实测」＋U12 来源计划；禁自造数字。
- 构建：`build.sh`（ophost/opapi/opgraph/onnxplugin）＋样例 test_aclnn_* 编译运行式；UT 目标；**均未运行，NPU 前提明示**。
- 交叉验证建议：与 ch16 mmad 同法——先 CPU 侧小型 numpy 复算 18.1 数值例，再上板对拍（标注为读者实验）。
- 陷阱表（8-10 行）：train/infer 混用、preload 当实测、half max/sum 精度假设、P 布局 64 对齐、mask 块级裁剪漏尾、runInfo 环误解为缓存、TND 分核、bmm2Write2Ub 编译期岔路漏判。

## 图表预算（3 图 2 表内）

1. 图 18-1 SVG：四级流水甘特＋缓冲＋同步位点（新画 `ch18-fa-pipeline.svg`；**示意**标注）。
2. 图 18-2 mermaid：online softmax 数据递推（块序列→m/l/O 更新）——或并入 18.1 正文公式＋小型表。
3. 表 18-1 模板矩阵举隅；表 18-2 缓冲策略对照（E3 三行）。

## 字数预算

500+1200+800+1500+1300+1300+900+800+700≈**9.0k（上限 12k 内）**；U 残项（U2′/U5′/U7′非主线）如需，优先砍 18.2/18.6 特化列举。交付时按 ACCEPTANCE 声明覆盖。

## 写作纪律

- 每断言挂 EV 编号；源码引用「文件 L 行」；U 项正文标「未证/待实测」；性能零自造。
- 不动 ch17（经理收尾中）；appD 由经理处理——**本章不碰**。
- 交付后 STATUS 待审，不 commit/push，等待经理评审。
