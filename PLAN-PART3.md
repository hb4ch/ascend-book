# 第三编成稿方案（PLAN – Part 3，M3：Ascend C 算子开发）

> 基线：2026-09，第一编 22.9k 总字 / 第二编 17.6k 总字，`npm run verify` 全绿，GitHub Pages 已上线。
> 本编目标：第 9–14 章成稿，预计新增 25k–30k 总字；全书总字数迈向 80k。

## 0. 现状快照

- ch9–14 均为 M0 骨架占位（~300 字/章），frontmatter `status: 未成稿（M3 里程碑）`。
- 附录 D 已登记各章来源（ch9–14 的源仓路径均存在，`check:source` 绿）。
- 第 8 章预支的「债」：搬运 API 写法（`DataCopy`/`DataCopyPad`）在第 10 章还；N-DMA 五场景实操在第 10/14 章展开。
- 本地源码仓：`asc-devkit`（impl/include/examples/docs 四件套齐全）、`ops-nn`、`ops-transformer`、`ops-sparse`、`cann-learning-hub`。

## 1. 总纪律（在 STYLEGUIDE §1–§9 与 §10 三条之上）

1. **API 层讲「怎么选、怎么用顺手」**：第 9 章是地图与决策章，不逐 API 翻译；机制深挖留给第 10/11 章。
2. **锚点 ≤5/章**：每章选 ≤5 个锚点文件讲透（样例 `.asc`/`.cpp` 每处 ≤25 行），其余进脚注。
3. **运行性分级从严**：Ascend C device 样例一律 `[需真机验证]` 并给验证步骤（§8：本机无 NPU）；cmodel/CPU-SIM 只作旁证。
4. **每章一图起步**：至少 1 张能背的 Mermaid 小结图；决策树类内容优先图化（§6）。
5. **架构差异显式标注**：SIMT 仅 950（dav-3510）起支持；A2/A3（dav-2201）为 SIMD 单模型——所有跨架构论断标注适用范围。

## 2. 六章方案

### 第9章 编程模型与 API 选择（地图章，材料最齐，最先写）
- **骨架**：① API 分层总览（Tpipe/Tque 框架 / 基础 API / 语言扩展 SIMD C / SIMT C / 高阶 API / 算子模板库 / PyAsc）；② host/device 分工与 `<<<>>>` 启动；③ Tiling 概念与 host 侧职责；④ PyAsc Python 前端；⑤ 按场景选 API 决策树。
- **锚点**：`asc-devkit/docs/zh/asc_how_to_choose_api.md`（决策依据）、`examples/01_simd_cpp_api/00_introduction/01_add/add_tpipe_tque/add_tpipe_tque.asc`、`examples/02_simd_c_api/00_introduction/01_add/c_api_sync_add/c_api_add.asc`、`docs/zh/guide/programming_guide/programming_model/programming_model_overview.md`（SIMD/SIMT 模型与 950 架构差异）、`README.md`（PyAsc 定位）。
- **图**：API 分层金字塔图 + 选型决策树（Mermaid）。
- **验收**：读者能拿着自己的算子场景在 5 分钟内选对层级；verify 绿。

### 第10章 核心编程能力详解（本编最重的一章）
- **骨架**：TPipe/TQue 范式原理（队列事件、EnQue/DeQue 同步语义）；Tensor 体系（GlobalTensor/LocalTensor/静态 Tensor）；内存管理 API（InitBuffer/AllocTensor 与第 8 章对齐）；计算 API 家族（向量计算/矩阵计算/数据搬入搬出，N-DMA 实操还债）；双 Lazy/同步控制。
- **锚点**：`impl/basic_api/`、`impl/tensor_api/`、`include/kernel_operator.h`、`examples/01_simd_cpp_api/03_basic_api/00_data_movement/data_copy_gm2ub_nddma/`、`docs/zh/api/SIMD-API/`。
- **图**：TPipe/TQue 数据流时序图（sequence）；计算 API 家族树。
- **验收**：Add 三种写法（Tpipe/Tque、基础 API、C API）对照完成；搬运 API 五场景表格；verify 绿。

### 第11章 SIMD/SIMT 与高级特性（950 新范式章）
- **骨架**：SIMD C API 全貌（`asc_xxx` 命名、`_sync` 后缀、repeat/stride 高级接口）；SIMT 编程模型（线程/warp、共享内存、与 CUDA 对照迁移）；SIMD/SIMT 混合编程；AICPU 算子（何时逃逸到 CPU 核）。
- **锚点**：`examples/02_simd_c_api/`、`examples/03_simt_api/00_introduction/01_gather/`、`examples/05_simd_simt_hybrid/`、`impl/simt_api/`、`cann-learning-hub/blogs/operator/regbase_vec_add/`。
- **图**：SIMD vs SIMT 执行模型对比图；混合编程分工图。
- **验收**：一张「CUDA 开发者迁移对照表」；每类 API 有真实 `.asc` 代码例证；verify 绿。

### 第12章 编译、工具链与部署（边界最明确的章）
- **骨架**：Host/Device 混合编译流程；`--npu-arch` 与目标芯片映射（dav-3510/2201/2002）；CMake 工程组织；kernel 二进制产物与加载（衔接第 5 章 binary_loader）；调试工具（衔接第 7 章 DFX）。
- **锚点**：`docs/zh/guide/compilation_and_execution/`、examples 各 `CMakeLists.txt`、`asc-devkit/build.sh`/`classify_rule.yaml`。
- **明示边界**：BiSheng 编译器源码不在开源仓（§8），写「文档+产物+用法」级。
- **图**：从 `.asc` 到可执行 kernel 的编译流水线图。

### 第13章 算子库体系（四仓横览）
- **骨架**：为什么要算子库（复用/性能/覆盖）；ops-nn 结构与 aclnn 算子生成（衔接第 4 章 aclnnop）；ops-transformer（大模型算子族）；ops-sparse；算子库视角的选型——先用库、再改模板、最后手写。
- **锚点**：`ops-nn/`（目录结构 + 一个典型算子全链）、`ops-transformer/`、`ops-sparse/`、`asc-devkit/docs/zh/guide/programming_guide/library_api/`。
- **图**：算子库分层复用图（库→模板→手写）。

### 第14章 经典算子实战（端到端收口章）
- **骨架**：一条龙旅程——Add 全家族（入门→Tiling→双流水）；MatMul（Cube 路径、分形、L0C）；Softmax 高阶 API 复用；融合算子设计（衔接第 8 章零拷贝动机）；性能验收（衔接第 7 章 msprof、第 15 章预告）。
- **锚点**：`examples/01_simd_cpp_api/{00_introduction,04_advanced_api,05_best_practices}/` 精选 5 个、`ops-nn/examples/add_example/`。
- **图**：端到端旅程总览图（设计→Tiling→实现→编译→运行→调试→优化）。
- **验收**：读者照书可独立完成一个自定义算子的开发闭环（真机步骤齐全）。

## 3. 执行顺序与落地

| 步骤 | 内容 | 收口动作 |
|---|---|---|
| M3-1 | 第9章成稿（地图+决策树+分层对照） | ✅ 完成（4.4k总字，3图4码例） |
| M3-1.5 | 第4–8章 SVG 图表补强（6 张）+ reviewer 子代理审查 22 处缺陷修复 | ✅ 完成 |
| M3-2 | 第10章成稿（最重，可拆两轮） | ✅ 完成（4.3k总字，4图5表，N-DMA 债还清） |
| M3-3 | 第11章成稿 | ⬜ 下一站（收口：verify+三轮自审+图表） |
| M3-4 | 第12章成稿 | 同上收口动作 |
| M3-5 | 第13章成稿 | 同上 |
| M3-6 | 第14章成稿（收口章） | 同上 + 第三编总回顾 |

- 每章收口：frontmatter `status` 改「已成稿（M3，第三编）」→ appD 同步 → CHANGELOG 记录 → README 里程碑更新 → push（Pages 自动发布）。
- 每章完稿后执行自查 review：重读全文、核对 API/路径拼写、表格无裸 `|`、图表齐注、无 TODO 残留、与四大能力目标对齐。

## 4. 风险与边界

1. **无真机**：所有 `[可在 NPU 运行]` 论断只能来自仓内 examples 的官方标注，自己跑不了——统一 `[需真机验证]` + 验证步骤（§8/§10）。
2. **SIMT 材料新**：950 起才有 SIMT，旧架构读者需明确「你的芯片可能用不了」；对照 CUDA 时不得暗示 API 完全等价。
3. **模板库在外部仓**（ATVC/ATVOSS/CATLASS/pyasc 在 gitcode）：只写定位与入口，不展开内部实现（源码不在本地基线内）。
4. **字数目标**：核心章 8k–12k 中文（§4）；地图章/工具章可按 M2 先例（3–4k 中文）不注水，宁缺毋滥。
