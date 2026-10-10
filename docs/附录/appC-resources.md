---
title: 附录C 资源导航
description: 按任务入口的开发资源：快照 commit 深链（构造自本地路径，未在线核验）与官方站点
---

# 附录C 资源导航

「入口」链接为**按本书源码快照 commit 构造的 GitCode 深链**（blob/tree＋固定 commit），由本地仓库真实路径生成——**非原文自带的绝对 URL，本书未在线核验其可达性**；复现本书内容时请使用该快照。仓库主页仅作仓名入口；论断级证据见各章脚注。安装与环境见附录 A，源码映射见附录 D。

## 按任务入口

| 目标 | 入口 | 阅读提示 |
|---|---|---|
| 零基础理解 NPU 与昇腾 | [入门 notebook：AI 基础／什么是 NPU](https://gitcode.com/cann/cann-learning-hub/blob/a3989658/quick_start/cann_basics/01_ai_basics.ipynb)[^1] | 两个笔记本：AI 基本概念；DaVinci 架构与 AI Core/AI CPU/Vector/Cube、存储层级。先备：无。 |
| 写第一个 Ascend C 算子 | [Ascend C 算子开发（Kernel 直调版）](https://gitcode.com/cann/cann-learning-hub/blob/a3989658/tutorials/ascendc_operator_development_light/README.md)[^2] | 核函数→编译→Tiling→矩阵/融合→调试调优。先备：本书第 9–10 章、[多级 API 选择指南][choose-api]。 |
| 工程化完整版教程 | [Ascend C 算子开发（完整工程版）](https://gitcode.com/cann/cann-learning-hub/blob/a3989658/tutorials/ascendc_operator_development/README.md)[^3] | 九模块工程化路线，与直调版互补；第 14–18 章多用其子课程。先备：上一行。 |
| Conv 类算子专项 | [Conv 算子开发实战（首子课程）](https://gitcode.com/cann/cann-learning-hub/tree/a3989658/tutorials/conv_operator_development/01_conv_basic_operator_development)[^4] | 卷积算子概念与开发实操（notebook 序列）。Matmul 对照本书第 16 章四例。 |
| 硬件边界与代际差异 | [硬件实现总览与架构规格](https://gitcode.com/cann/asc-devkit/blob/28e7aba2/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/basic_architecture.md)[^5] | 存储层级总览＋2002/2201/3510 架构规格（带宽/通路表）。先备：本书第 2 章，进阶第 11 章。 |
| 性能诊断案例与接口 | [Scalar 性能影响与优化][perf1]｜[MX 量化 Matmul 优化][perf2]｜[msprof 采集接口（runtime）][msprof] | 来源文章的瓶颈案例＋Profiling 打点 API（非本书实测）。先备：本书第 19 章。[^6][^7] |
| 调试与内存检测 | [上板调试：打印／msSanitizer／msDebug](https://gitcode.com/cann/asc-devkit/blob/28e7aba2/docs/zh/guide/programming_guide/debug_and_tuning/functional_debug/npu_board_debug.md)[^8] | DumpTensor/printf 上板打印；msSanitizer 内存/竞争/未初始化/同步四类检测——**本书快照文档仅列 SIMD 编程场景**；msDebug 单步。先备：本书第 7、11 章；运行验证边界见 [msSanitizer 官方指南][mssan]；asc-tools 样例原链见[^14]。 |
| 多卡集合通信开发 | [HCCL 开发系列课程](https://gitcode.com/cann/cann-learning-hub/blob/a3989658/tutorials/hccl_development/README.md)[^9] | 基础概念→核心算子→算法实现→模拟验证；接口以 hcomm `docs/zh/api_ref/` 为准（快照内）。先备：本书第 20–23 章。 |
| 单边传输与 KV 池化实战 | [HIXL README（能力与接口总览）](https://gitcode.com/cann/hixl/blob/9ed283b2/README.md)[^10]＋[HIXL 在 RL 推理中的长尾时延优化][hixl-rl] | 单边通信生产案例（转述级）。先备：本书第 22 章。 |
| 推理图后端与框架接入 | [CANN npugraph_ex 图模式优化](https://gitcode.com/cann/cann-learning-hub/tree/a3989658/blogs/inference/npugraph_ex_aclgraph_graph_mode)[^11] | 图模式原理、捕获重放、vLLM/SGLang 接入记录（转述级）。先备：本书第 26 章。 |
| 后端与 PTO 生态 | [PTO Tile Library（pto-isa）](https://gitcode.com/cann/pto-isa/blob/dd3cb0fb/README_zh.md)[^12]｜[PyPTO][pypto] | 虚拟 ISA 指令手册（`docs/PTO-Virtual-ISA-Manual_zh.md`）与 Python 前端。先备：本书第 24–25 章。 |
| 读生产级算子实现 | [ops-nn][opsnn]｜[ops-transformer][opstf]｜[ops-sparse][opssparse]（各仓 README 及算子目录） | 生产约束与工程化对照；Matmul/FA 分别见本书第 16、18 章已引文件。先备：对应领域章。[^13] |

[^1]: `cann-learning-hub/quick_start/cann_basics/01_ai_basics.ipynb` 与同目录 `02_what_is_npu.ipynb`；课程表见 hub `README.md`「快速开始」表。
[^2]: `cann-learning-hub/tutorials/ascendc_operator_development_light/README.md`（内容句为原文摘录：「算子核函数、算子编译、Tiling 计算、矩阵算子开发、CV 融合算子开发、算子调试调优」）。
[^3]: `cann-learning-hub/tutorials/ascendc_operator_development/README.md`（子课程 01_basic_overview…09_course_practice）。
[^4]: `cann-learning-hub/tutorials/conv_operator_development/01_conv_basic_operator_development/`（01.01–01.03 notebook）。
[^5]: `asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/basic_architecture.md`；同目录 `architecture_spec/npu_arch_2002.md`、`npu_arch_2201.md`、`npu_arch_3510.md`。
[^6]: `cann-learning-hub/blogs/operator/scalar_npu_operator_performance_optimization/scalar_npu_operator_performance_optimization.md`；`cann-learning-hub/blogs/operator/mx_quantized_matmul_optimization/mx_quantized_matmul_optimization.md`。
[^7]: `runtime/docs/zh/api_ref/19-01_data_profiling_apis.md`、`runtime/docs/zh/api_ref/19-02_msproftx_extension_apis.md`。
[^8]: `asc-devkit/docs/zh/guide/programming_guide/debug_and_tuning/functional_debug/npu_board_debug.md`（调试手段总览与 msSanitizer 节）。
[^9]: `cann-learning-hub/tutorials/hccl_development/README.md`（课程范围句为原文摘录）；接口参考 `hcomm/docs/zh/api_ref/`。
[^10]: `hixl/README.md`；案例 `cann-learning-hub/blogs/inference/hixl_rl_tail_latency_optimization/HIXL在RL推理中的长尾时延优化.md`。
[^11]: `cann-learning-hub/blogs/inference/npugraph_ex_aclgraph_graph_mode/CANN npugraph_ex图模式优化.md`。
[^12]: `pto-isa/README_zh.md`；指令手册 `pto-isa/docs/PTO-Virtual-ISA-Manual_zh.md`；`pypto/README.md`。
[^13]: `ops-nn/README.md`、`ops-transformer/README.md`、`ops-sparse/README.md`；clone 地址见各 README 安装节（`git clone -b <tag> https://gitcode.com/cann/<repo>.git`）。
[^14]: msSanitizer 用户指南（npu_board_debug L60 原链）：`https://gitcode.com/Ascend/mssanitizer/blob/master/docs/zh/user_guide/mssanitizer_user_guide.md`；asc-tools 样例（show_kernel_debug_data_tool L3 原链）：`https://gitcode.com/cann/asc-tools/tree/master/examples/01_show_kernel_debug_data`。
[^15]: 快照 commit：asc-devkit `28e7aba2`、runtime `681ef761`、hcomm `1581d160`、hixl `9ed283b2`、pto-isa `dd3cb0fb`、pypto `883e7dfb`、ops-nn `e5c3fa93`、ops-transformer `e75072d7`、ops-sparse `ae60d05a`、cann-learning-hub `a3989658`（见 `management/SOURCE-BASELINE.md`）。

## 官方站点（原文即绝对 URL，来自仓内引用）

- [Ascend C 产品页](https://www.hiascend.com/cann/ascend-c)与[社区版算子开发指南][choose-api]：出处 asc-devkit `README.md`（L7 徽章、L47 正文、L202 表格）。
- [CANN 安装向导][inst-wizard]与 [CANN 下载页][dl]：出处 runtime `README.md`（安装/获取节）。
- 版本配套：[release-management][rel]（hub/ops 仓 README 共同指向的版本对应表）。

> 本书未联网核验以上任一链接的当前可达性；深链内容由快照路径构造（commit 见 [^15]），复现本书内容时以固定快照为准。

[choose-api]: https://www.hiascend.com/document/redirect/CannCommunityOpdevAscendC
[inst-wizard]: https://www.hiascend.com/document/redirect/CannCommunityInstWizard
[dl]: https://www.hiascend.com/cann/download
[rel]: https://gitcode.com/cann/release-management
[perf1]: https://gitcode.com/cann/cann-learning-hub/blob/a3989658/blogs/operator/scalar_npu_operator_performance_optimization/scalar_npu_operator_performance_optimization.md
[perf2]: https://gitcode.com/cann/cann-learning-hub/blob/a3989658/blogs/operator/mx_quantized_matmul_optimization/mx_quantized_matmul_optimization.md
[msprof]: https://gitcode.com/cann/runtime/blob/681ef761/docs/zh/api_ref/19-01_data_profiling_apis.md
[mssan]: https://gitcode.com/Ascend/mssanitizer/blob/master/docs/zh/user_guide/mssanitizer_user_guide.md
[hixl-rl]: https://gitcode.com/cann/cann-learning-hub/tree/a3989658/blogs/inference/hixl_rl_tail_latency_optimization
[pypto]: https://gitcode.com/cann/pypto/blob/883e7dfb/README.md
[opsnn]: https://gitcode.com/cann/ops-nn/blob/e5c3fa93/README.md
[opstf]: https://gitcode.com/cann/ops-transformer/blob/e75072d7/README.md
[opssparse]: https://gitcode.com/cann/ops-sparse/blob/ae60d05a/README.md
