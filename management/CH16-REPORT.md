# 第16章交付报告（CH16-REPORT）

> 2026-10-09。依据 management/tasks/CH16.md；P0-REVIEW 七项已先期修毕（见 git 前次状态与下表§1）。

## 1. P0-REVIEW 七项修订落实

| # | 修订 | 落实 |
|---|---|---|
| 1 | 日期/锚点/伪路径 | EVIDENCE 改 2026-10-09；「5 组文件」措辞；A3 改四例真实文件清单 |
| 2 | 同步种类/数量 | 全文统一「4 类 HardEvent＋反向预置 6 个 flag 实例（MTE1_MTE2×4＋M_MTE1×2）」；删除「六对/反向三类」 |
| 3 | 性能口径 | 3022.92μs 只对比 aic_mac 3076.396（误差 1.77%）；mac_ratio=占比≠峰值率显式声明；官方混用处加注 |
| 4 | B 转置 | 删「isTrans 参数」说；改「gen_data L43 物理转置＋IS_B_TRANSPOSE 编译期分支＋LoadData enTranspose/ifTranspose」双层真相（EVIDENCE§U2/正文 16.4） |
| 5 | bank 表述 | 「16 bank（各 16KB）组成 8 组×2 bank，总 256KB」；3510 判据原文照录、两架构并列不比较 |
| 6 | U1–U5 | 全部补读销账（EVIDENCE 末节附证据）；容量仅写有文档者；性能补 dtype/量纲（half×half→half、fp32 累加 F322F16、μs/cycles） |
| 7 | STYLEGUIDE 节号 | ACCEPTANCE 改「§3 代码与运行性分级」 |

## 2. 正文交付（docs/03-ascendc/ch16-matmul-cube.md）

- **8 节结构**：16.1 双路线（高阶五步+Iterate/IterateAll 辨析）→ 16.2 九级阶梯因果（含 Case2/3 尾块均衡推导【标注 A】、四层口径示范、950 对照）→ 16.3 基础 API 全生命周期（四阶段真码+4 类事件表+6 预置 flag+DataLoadB 2×2 矩阵+K 循环走查）→ 16.4 NZ/转置双破除＋**表 16-2 架构分岔** → 16.5 搬收四例（含同 bank 反直觉）→ 16.6 L0C/出口族谱表 → 16.7 性能观测四层口径教学 → 16.8 ops-nn 导览。
- **图**：`docs/figures/ch16-pipeline.svg`（四级流水+双缓冲+正反向同步+时空表，满足「流水/缓冲图」）；mermaid 学习路线图（16-A）；架构差异表×2（16-2、LoadDataB 2×2）。
- **字数**：5,934 总/**4,023 中文**——达重点章 4k 最低线；**未达 8k 深度目标，覆盖情况**：已覆盖任务书全部七个重点（高阶入口/九级因果/生命周期/NZ/双缓冲同步/L0C Fixpipe/bank 反例与单参数）；未展开：mmad.asc 逐行全文翻译（645 行仅引关键段）、matmul.asc Case4-8 模板参逐个源码走读（引结论）、ops-nn 单算子解剖（16.8 仅族谱）。请验收裁量。
- **运行性标签**：全部代码块 `[需真机验证]`（本机无 NPU）；性能数据全部标注「官方数据+架构+CANN 版本」，未声称本机复现。
- **状态**：frontmatter `status: 待审`。

## 3. 验证

- `npm run verify` 完整日志：`management/validation/ch16-verify.log`——build ✓、42 文件内链 OK、check-source 240 引用 0 无效、术语无高置信误用。
- HTML 抽查（dist/03-ascendc/ch16-matmul-cube.html）：脚注 8 定义/13 引用/全带 backref；表格 7 张渲染；SVG 内嵌；mermaid 块存在。
- 字数：`npm run word:count`→ch16 5,936/4,023 中文。

## 4. 未验证项/边界

- 无 NPU：所有「可在 NPU 运行」判断仅据仓内 README，未本机执行；CPU-SIM 未用于本章（Cube 样例无 CPU-SIM 路径声明）。
- Case2/3 尾块均衡归因为本书推导（已标注【A】），官方未明说。
- 950 L0C→UB 直通对融合成本的量化对比留待 ch17 实测措辞。
- ch11 由经理修订的 bank 表述未复核一致性（本轮未动 ch11）。

## 5. 未动文件

scripts/*、reviews/*、ch11、management/STATUS.md、其他章节——均未触碰。未提交未推送。

---

## 附录：R1 退修（2026-10-09）

- 按 `reviews/CH16-R1.md` 六组全改；逐项位置见 `CH16-R1-RESPONSE.md`。
- 正文重写后 7,375 字/5,069 中文；UnitFlag 专节、LoadDataB 2×2 表、输出基块账本、CMake 复现入口为新增四块。
- SVG 时空面板重画（两级节奏/Fixpipe 时点/删断言）；verify 绿；状态仍「待审」。
