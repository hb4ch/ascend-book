# APPC-EVIDENCE —— 附录C 改写证据

2026-10-10。任务 management/tasks/APPC-REVIEW.md。只读核验；每条新导航入口均落到本地快照真实路径。

## 入口逐条核验（存在性）

| 新表入口 | 实测路径（`ls` 通过） |
|---|---|
| cann_basics notebooks | `cann-learning-hub/quick_start/`（README 表格列 01_ai_basics/02_what_is_npu，L42-43） |
| ascендc 直调版/完整版教程 | `cann-learning-hub/tutorials/{ascendc_operator_development_light,ascendc_operator_development}`（目录实存；README L10/L12 新闻条） |
| conv 教程 | `tutorials/conv_operator_development/`（README L12） |
| 硬件文档 | `asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/{basic_architecture.md,architecture_spec/}` |
| 性能博客 | `cann-learning-hub/blogs/operator/{scalar_npu_operator_performance_optimization,mx_quantized_matmul_optimization,…}`（20 目录实存） |
| msprof 接口 | `runtime/docs/zh/api_ref/19-01_data_profiling_apis.md`、`19-02_msproftx_extension_apis.md` |
| 调试文档 | `asc-devkit/docs/zh/guide/programming_guide/debug_and_tuning/{functional_debug/,npu_board_debug.md,overview.md}` |
| HCCL 教程/API | `tutorials/hccl_development/`；`hcomm/docs/zh/api_ref/` |
| HIXL | `hixl/README.md`；`blogs/inference/hixl_*` 5 篇 |
| 推理博客 | `blogs/inference/{npugraph_ex_aclgraph_graph_mode,npugraph_ex_third_party_framework_integration,torchair_fx_pass_multi_stream,…}`（20 目录实存） |
| PTO/PyPTO | `pto-isa/README_zh.md`+`docs/`；`pypto/README.md`+`docs/` |
| 算子仓 | `ops-nn/`、`ops-transformer/`、`ops-sparse/` README 实存 |

## 旧版问题清单（本次改写动因）

1. **裸链接堆砌**：官网三 URL、GitCode 十仓 URL 无任务语境、无「读什么」。
2. **含糊集合**：旧版「生态仓：pyasc、pyto-gym…」与 blogs 省略号列表为目录级堆砌，本次未纳入核验（资源不在本地 10 仓不代表不存在，仅不收入导航）；「HICANN.ascend-c-toolkit 插件」「pandoc/pagedjs」「B站/SIG meetup」无仓内锚，删除。
3. **外链当可用资源**：旧版直列 URL 未声明「未核验可达性」。
4. 无先备/读什么引导，无与本书章节映射。

## 外链来源（只声明出处）

- hiascend 社区文档徽章：`asc-devkit/README.md` L7（shields badge→hiascend document redirect）；L47 Ascend C 介绍段。
- gitcode cann 组织：各仓 README「上游」属性；`cann-learning-hub/README.md` L26（release-management 版本对应表链接）。
- mssanitizer 用户指南外链：`npu_board_debug.md` L60。
- asc-tools 样例外链：`show_kernel_debug_data_tool.md` L3。
- learning-hub 在线体验（ai.gitcode.com notebook）：`cann-learning-hub/README.md` L42-43。

## 边界

- 未改附录 A/D/E；未动 glossary/appB（经理接管）。
- 未联网；所有外链标注「未核验」。
- 源仓只读（status=0）；未提交。


---

# R1 修订（reviews/APPC-R1，2026-10-10）

1. **域名**：`hiascent.com`拼写错误→**hiascend.com**；全部外链 href 逐个取自本地仓内原文：asc-devkit README L7/L47/L202（CannCommunityOpdevAscendC、/cann/ascend-c）、runtime README L94/L133（InstWizard、download）、L172（`gitcode.com/cann/runtime.git`）、各仓 clone 行（ops-nn L38/ops-transformer L45/ops-sparse L25/pto-isa getting-started L93）、hub L42-43（notebook 在线体验）、npu_board_debug L60（mssanitizer 指南全链）、show_kernel_debug_data_tool L3（asc-tools）。**未联网**，页内标注「未在线核验」。
2. **假路径修正**：`19-01/19-02`→完整文件名两条；`ascendc_operator_development/`补仓前缀；`docs/`、`hixl_*`、`npugraph_ex_*`→具体 README/文章文件。**内容实读**：直调版教程 README（核函数/编译/Tiling/矩阵/融合/调优原文）、hccl 教程 README（概念→算子→算法→模拟验证原文）、npugraph_ex 博文标题页、scalar 性能博文标题页——「读什么」与文件内容对应，非仅 ls。
3. **三列短表**：目标/入口/阅读提示；先备融入提示句；正文短名+外链，完整 `仓/路径` 全部入脚注（[^1]–[^17]），check-source 可覆盖（536 引用含本文件后复验）。
4. **虚构断言删除**：「pyasc/pyto-gym 虚构」→「本次未纳入核验；资源不在本地不代表不存在」。
5. 范围仍只 appC+本证据/报告+附录 index 一行；B/D/E 未动。
