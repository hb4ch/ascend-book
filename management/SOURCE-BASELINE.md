# 源码基线（SOURCE-BASELINE）

> 采集日期：2026-10-09。采集方式：只读 `git log`/`git status`，未执行任何更新/修改/checkout。
> 用途：全书所有「repo/path」引用与行号证据以本快照为准；后续若源仓变动，须刷新本表并在对应章 CHANGELOG 注明。

| 仓库 | 分支 | HEAD commit（完整 40 位） | 日期 | 一句话主题 | dirty |
|---|---|---|---|---|---|
| asc-devkit | master | `28e7aba2f62e0940e4240442fa3acb794ae4e4d2` | 2026-08-22 | add aclgraph sk inner core sync check | 0 |
| cann-learning-hub | master | `a3989658fa1dce436d4ab402042e0682a2e9bdc7` | 2026-08-21 | 完善readme | 0 |
| hcomm | master | `1581d1608fd8840bbd46bcbe3f357b1d08460b6a` | 2026-08-22 | repair hcomm thread res get info return value | 0 |
| hixl | master | `9ed283b27309463ed0faa490b79c0dc9ddef6377` | 2026-08-22 | 切换CCE集群 | 0 |
| ops-nn | master | `e5c3fa9327ea95ba26d06227e746923580d10921` | 2026-08-22 | 编译任务机器规格调整以及冒烟脚本调整 | 0 |
| ops-sparse | master | `ae60d05a7224158e854d1a33b483f85c132f345a` | 2026-08-21 | feat: 新增 aclsparseLtMatmulPlanInit/AlgSelectionInit 接口及执行计划类 | 0 |
| ops-transformer | master | `e75072d7e7519405025d05a98cf1b2f106ad3874` | 2026-08-23 | mqsmla perf：change v0buffer DSize to 640 | 0 |
| pto-isa | master | `dd3cb0fbd5d7c226c001b8a50ab18614aaaa806d` | 2026-08-22 | revert trem | 0 |
| pypto | master | `883e7dfb018da764a65fd2c2f8c1e1d2de2d2471` | 2026-08-22 | feat(pass): Fold assemble toOffset into L0C2UB copy in ReplaceTensor | 0 |
| runtime | master | `681ef7610df13c8128982901142a2c869ddbb53e` | 2026-08-22 | refactor: 隔离 arch5162 ApiMbuf 组件 | 0 |

## 备注

- 10 个仓库全部 worktree 干净（dirty=0），无未提交修改，证据可复现。
- 各仓 HEAD 即本书证据基线；正文中引用行号时须能在此 commit 下复现。
- ch16 相关主力仓：`cann-learning-hub`（04_matmul_basic 教程）、`asc-devkit`（matmul_high_performance / matmul_basic_api_high_performance / 04_memory_access 四例）、`ops-nn`（matmul/ 真仓对照）。
