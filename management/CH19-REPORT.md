# CH19 交付报告（CH19-REPORT）2026-10-09

## 交付物
- 正文 `docs/04-perf/ch19-perf-analysis.md`（word:count **7,502 字／中文 5,896**）
- 图 `docs/figures/ch19-perf-pipeline.svg`（采集链＋判定红线，无装饰）
- 验证 `management/validation/ch19-verify.log`（0 FAIL）、`ch19-offline-calc.log`（带宽复算/百分比/理论值）、`ch19-svg-render.png`（rsvg-convert→PIL 四色块像素统计 blue101/green111/orange98/purple202，全非零）

## 任务书逐项对照
| 要求 | 落实 |
|---|---|
| 先纠正口径 | 19.1①Task−均值≠纯调度（OpTime 双锚点 startAicore/endAicore 真码 L40-46＋analyzer L199/L137，差额分解须 timeline，case2 9.44μs 只称总差额）；19.1③单 ratio≤1、**和**可>1（case4≈1.364）；19.1④驱动频率=返回值非实测瞬时，**syscnt 钟≠AI Core 钟两套分母**；19.4 hwts 核级定位≠timeline 全由该类事件构成（四结构锚点表）;msprof CLI 参数不在仓→**明确不覆盖**，msprof op 无本地证据不提；msprof 库 API 与 CLI 分立（19.2 边界①–④） |
| 有效吞吐≠DRAM 实测 | 19.5 末段：README 口径 BW=D/T_mte2（读/混合两公式 L519-23）复算 case2–6 全对上表值；Task 分母者称「端到端产出率/有效吞吐」**不称带宽**、**不假设全 DRAM**，与 Memory.csv 硬件流量区分 |
| Add shape/dtype 核查 | 8192²×half×3 tensor（README L50-52 真码）；百分比保留复算（1→2=95.56%）**并注明 README 95.5 系舍入** |
| 因果措辞 | 19.5 表格逐跳「README 解释/置信/需补证/实验变量」四栏；case3→4、4→5 明标「相关性成立因果未证」；变量具体可测（核数/块尺寸/depth/bypass 开关/地址布局） |
| 正文覆盖八项 | 测量对象边界§19.1/工具与真实命令§19.2（msopprof 上板+仿真两条，均文档背书）/字段分母§19.3＋列间自洽校验/源码时间戳频率§19.1④+19.4/完整案例链§19.5/均值尾核§19.6（47×5+2×50 算例）/预热重复扰动§19.7（稳定性控制≠验证，**无「排除频漂」式保证**）/记录模板§19.7（字段+三级置信） |
| 不重复 ch16–18 | §19.9 只收编引用；性能四层口径操作化（L1–L4 warning 框）承 ch16 表16-1 |
| 代码命令回源 | cmake -DSCENARIO_NUM/RUN_MODE、msopprof 两命令、SetL2CacheHint L365-6、ProfConfig L49-56——全部真码脚注 8 条双向闭环（HTML fn 26 处渲染） |
| 无实测 | 全章声明；复现序列给全（§19.5 编译链真码） |

## 字数声明（ACCEPTANCE §1）
核心章目标 8–12k 中文，本文 **5,896**（word:count 口径 7,502/5,939 含脚注代码注释）。**覆盖**：测量学全链＋案例链深读＋实验设计模板；**未展开**：msprof CLI 全参数（不在仓）、csv 生成器实现（不在仓）、pmu[8] 语义（未文档化，U1–U5 已列§19.9）——由 PM 裁量是否补足或接受。

## 验证汇总
verify 0 FAIL；build 过；HTML 脚注 26 处、SVG 内联渲染像素验证过；图节点对应 19.2/19.3/19.5 无装饰元素。CH18 未触碰（仅修 R3 后遗留的一处代码块缺 `}` 使 build 恢复——见下）。

## 附注：ch18 build 修复
R3 后 `ch18-flash-attention.md` L120 分支树代码块缺右括号致 vitepress build 全站失败；本轮补 `}`（示意代码块内，无文字改动）——已最小化，请 PM 复核该块。

## 状态
**status: 待审**。等经理验收；ch20 未动。
