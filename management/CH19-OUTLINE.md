# CH19 提纲（CH19-OUTLINE）

> 2026-10-09。配套 `CH19-EVIDENCE.md`（EV 编号）。**非重点算子章**，按 ACCEPTANCE 走核心章 8k–12k？——ch19 属方法论章，目标 6–8k 中文，低于 8k 时报告声明（P2 行「不重复前章代码」约束下以工具链/口径/案例三足撑）。无实测；全部数字仓内引用或离线算术（log 已存）。

## 章定位（≈400 字）

- 承 ch16–18：会写之后，**如何知道好坏**。给测量口径、诊断链、扩展性方法论；性能数字纪律四层（Task/AI Core/分单元/理论）承 ch16 表16-1。
- 工具三分图：msprof（服务/枚举）–msopprof（单算子）–simulator（仅 SIMD）——安装边界与本书「未运行」声明。

## 19.1 指标口径：先学读表，再看数（≈1200 字，全书重点①）

- csv 族逐字段（EV §二表）＋**四个易错**：Task Duration≠核时间（E1，调度/响应差额）；非首列皆**均值**（E2，方差被吃）；ratio 分母 total cycle 且**可加和>1**（E3，case4 实例 0.973+0.33+…）；μs 来自 syscnt/频率（E4）而**频率是查表**（E4/E5 双轨：配置表 vs DrvGeAicFrq 实测）——「分母错误」专项框。
- 表：9 项 aicMetrics↔csv 对应＋PipeUtilization→Exct 版本岔（CHIP_V4_1_0）。

## 19.2 数据从哪来：采集链解剖（≈1000 字）

- hwts start/end 原子（E6）→Task 聚合；OpPMU 计数器；timeline 事件↔算子**靠显式打点**（E7 aclprofTensorInfo/RangerPushEx，torch 样例）——「时间线上认领任务」的机制与限制。
- msprof 服务侧结构一瞥（collector/dvvp/analyzer），点到为止。

## 19.3 七 case 调优链：观测→解释→补证→变量（≈1800 字，全书重点②）

- add_high_performance 全表复现＋六跳逐段：每跳「观测差→README 解释→**置信标注**（成立/相关未证因果）→需补证 csv→下一实验变量」——把 EV §四范式表格化呈现。
- 专项小节：**重叠≠可加**（case4 mte2 .973 但 task 仅−4.5μs、mte3 反升）；**负结果价值**（case6 bank冲突收益 3μs→冲突非瓶颈）。
- 离线算术示范：有效带宽 2.18TB/s 推演＋假设声明（log `validation/ch19-offline-calc.log`）。

## 19.4 时间线与算子定位（≈800 字）

- PipeTimeline（`--aic-metrics=`）视觉分析：找气泡/错相/长尾；与 ch17 流水图对读法。
- timeline 认领：host 打点→csv tensor 列；无打点时的算子边界法（OpBasicInfo/起止差）——**灰区诚实声明**。

## 19.5 多核扩展性与负载均衡（≈800 字）

- 均匀切分＋余数前置（case2 源码级）；AIC/AIV 前缀分族；扩展性曲线实验设计（核数扫描模板：固定 problem/核幂次/中位数）。
- Amdahl 式预期 vs 实测落差归因路径（调度常数 E1、带宽摊薄、尾核）——每步挂需补证 csv。

## 19.6 pto-isa 方法论收编＋迭代纪律（≈600 字）

- 四阶段占比诊型（feed-limited/Cube饿/带宽饱和/transform 主导）→映射 msopprof 列。
- 调优纪律清单：一次一杠杆/warmup-drain/同 shape 回归/记录入 README 表——工程化收口。

## 19.7 复现与边界（≈400 字）

- 无 NPU：复现步骤全集（编译→msopprof→csv→timeline），本书未运行声明；安装前提（商用/社区版）。
- U 清单转正文脚注：csv 生成器不在仓/950 freq 表行/simulator SIMD only/pmu[8] 语义。

## 图表预算

表×3（字段字典/七 case 总表/诊断映射）；图×1 SVG「采集链：hwts→analyzer→csv/timeline」（分层,`ch19-perf-pipeline.svg`）；mermaid 1（调优循环）。无性能自造。

## 字数预算

400+1200+1000+1800+800+800+600+400≈**7.0k**；若 PM 要求 8k，扩 19.3 案例逐跳与 19.5 实验设计。交付时声明覆盖。
