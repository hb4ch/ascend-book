# P0 交付报告（P0-REPORT）

> 2026-10-09。任务来源：management/tasks/P0.md；经理检查：management/reviews/P0-CHECKS.md（已读并纳入）。
> 本轮按约：未动正文、未提交推送、未动 scripts/check-source*、未切换模型。

## 交付清单

| # | 文件 | 状态 |
|---|---|---|
| 1 | `management/SOURCE-BASELINE.md` | ✅ 10 仓完整 40 位 commit/分支/dirty=0/日期；只读采集（`rev-parse`+`log`+`status`） |
| 2 | `management/ACCEPTANCE.md` | ✅ 已按经理补充修订：①运行性标签沿用 STYLEGUIDE 四种（含 `[示意代码]`），本机执行记录仅作附加证据；②核心章<8k 与重点章<深度目标均改为「列明覆盖情况→经理验收裁量」，删除「不达标不发布」的自裁表述；③锚点改**文件级** |
| 3 | `management/CH16-EVIDENCE.md` | ✅ 5 文件级锚点+依赖补充；提纲六节×证据对照；草稿 8 条断言逐条核实（2 处须修正：Fixpipe NZ2DN 仅 950、「8 组×16KB」→16 bank（各 16KB）组成 8 组×2 bank，总 256KB）；关键行号亲验（mmad.asc L502-523/526-543/576-598 与经理抽查一致） |
| 4 | `management/P0-REPORT.md` | ✅ 本文件 |

## 关键发现（供 ch16 成稿直接引用）

1. **两条路线必须分开讲**：教程（04_matmul_basic，ascend910b1，高阶 API 五步）≠ 性能样例（A2/A3/950，9 级阶梯+显式流水）。正文先讲学习顺序再进机制。
2. **A1 搬入即转 NZ**：Nd2Nz 在 MTE2 搬 GM→L1 时随路完成（mmad.asc L348-357）——草稿「A/B 按 NZ 驻 L1」的机制真相。
3. **Fixpipe NZ2DN 仅 950**（Fixpipe_L0CToL1.md L99 原文）；L0C→UB 通路有专文档且 `dualDstCtrl/subBlockId` 仅该通路有效——ch11 11.6 引用成立但须标架构。
4. **架构参数分岔实证**（mmad.asc L576-598）：2201 baseM=128/stepKa=8/24 blocks vs 3510 baseM=256/stepKa=4/32 blocks——同文件 `#if NPU_ARCH` 分岔，正文可直接对照。
5. **同步体系**（mmad.asc L155-166 + README）：4 类 HardEvent；反向预置 6 个 flag 实例（MTE1_MTE2×4 + M_MTE1×2），防首次 WaitFlag 死锁。
6. **nd2nz 单参数调优**：dstNzC0Stride 144（16 倍数→同 bank group→8 拍）→145；UB tile 144×128；「padding 不改输出紧凑布局」须随句说明。
7. **bank_conflict_ub 反直觉点**：scenario4 同 bank 2389 < scenario5 异 bank 3751——同 bank 读写在 2201 上是硬件优化点。
8. **性能五要素齐全的样板数据**：A2 Case0→8 = 759363.98→4012.44μs（189.25×，mac 18.7%→86.4%）；950PR Case8=2558.155μs（428.68×，mac 99.7%）；两表架构参数不同，禁止混排。

## 未解问题（U1–U5）

详见 CH16-EVIDENCE.md 末节：matmul.h 常量 CFG 模板全貌、mmad.asc DataLoad 参数段、950 L0C 容量、data_copy 具体数字、950 Case 结构差异——均为 ch16 成稿对应节前须补读项，不阻塞 P0 验收。

## 流程遵守

- 未改 `docs/` 正文（仅 management/ 下 4 个新文件）。
- 未 git commit/push（工作区新增 4 个 management 文件待经理验收后处置）。
- 未动 scripts/；模型/会话未变。

---

## 附录：P0 后续闭环（2026-10-09 追加）

- **经理评审**：`reviews/P0-REVIEW.md` 七项修订已全部落实（对照表见 `CH16-REPORT.md` §1）；本报告正文保留评审前时点原文，以下为差异终态：
  - 同步口径终态：**4 类 HardEvent＋反向预置 6 个 flag 实例（MTE1_MTE2×4＋M_MTE1×2）**（正文/证据表/图 alt 三处一致）。
  - bank 容量终态：**16 bank（各 512 行×32B=16KB）组成 8 组×2 bank，总 256KB**；3510 判据原文照录、不与 A2 比较方向。
- **U1–U5 已全部销账**（补读证据见 `CH16-EVIDENCE.md` 末节「未解问题→已解决」）：matmul.h L257/L289/L425、mmad.asc DataLoad L396-497、L0C 128KB/950 256KB、data_copy 四优化点数字、950 表同构性。
- **行号终审**：交付前全量复核修正 3 处（DataCopyInA L344、matmul.h 模板 L425-427、DataLoadB 上界 L497），正文脚注与证据表同步。
- **ch16 正文已交付**：见 `CH16-REPORT.md`（4,023 中文，待审）；verify 日志 `validation/ch16-verify.log`。
