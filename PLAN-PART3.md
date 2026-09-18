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

### 第11章 SIMD/SIMT 与高级特性（M3-3 详细方案）

**章节结构（6 节，对骨架重排）**
1. **SIMD C API 接口分级**：`asc_xxx` 命名、`_sync` 易用口 vs `repeat/stride` 极致口（真码：`02_simd_c_api/03_c_api/{00_data_movement,02_reg_vector_compute}`）
2. **SIMT 编程模型**：Warp/线程、ld/st/AddrSpace、分支掩蔽；硬件三件套（DCache · Warp Scheduler · 128KB Register File，出自 950 特性表第2行）；**CUDA 开发者迁移对照表**（blockIdx/threadIdx/shared memory↔SSBuffer、bank conflict）；何时逃逸到 AICPU（`04_aicpu` 样例定位）
3. **SIMD/SIMT 混合编程**：`__simt_vf__`/`__simd_vf__` 双 VF + `asc_vf_call` 派发；`simd_simt_gather_and_adds` 全程精读（SIMT 做离散 gather、SIMD 做 UB 连续加，UB 是交接面）
4. **同步进阶**：PipeBarrier/DataSyncBarrier/Lock（核内）、CrossCore AIV0/AIV1 独立触发 AIC（核间）、SSBuffer（950 新增核间存储）——接第10章 §10.2 三类表落实操
5. **RegBase 寄存器底座**：MemBase vs RegBase 深化（第2章预支）、RegTensor/VF 融合优化/循环优化、`02_reg_vector_compute` 20 例导览
6. **A5(950) 新特性导览 + 调试**：13 项特性表按类分组（计算/搬运通路/同步/存储结构/低比特）；printf、reg dump、NPU-Check（材料风险：zh 文档未检索到 NPU-Check，写作时在 `03_simt_api/05_troubleshooting/` 与 blogs 中补充取证，找不到则明示并降级）

**配图方案（5 张，均带中英文 alt+图注+正文解释）**
| 图 | 类型 | 内容 | 为什么是 SVG/Mermaid |
|---|---|---|---|
| 图 11-1 SIMT 硬件三件套与线程执行模型 | SVG | AIV 内 SIMT 单元解剖：DCache/Warp Scheduler/128KB RF；warp→线程束调度、独立 PC、分支掩蔽；右侧 CUDA 对照小栏 | 结构剖视图，Mermaid 不擅长 |
| 图 11-2 SIMD vs SIMT 执行模型对比 | SVG | 上半：1 指令→多 lane 同构数据（Vector 单元，数据驻 UB）；下半：1 指令→多线程独立分支（Warp Scheduler，数据经 DCache/RF）；与第9章图 9-2「四步法」互补——那是编程流程对比，这是硬件执行视角 | 同一坐标框架双栏结构图 |
| 图 11-3 混合编程数据流 | SVG | 单 kernel 内：GM --(SIMT VF: gather 离散读)--> UB --(SIMD VF: adds 连续算)--> GM；标注 `asc_vf_call` 两次派发与 UB 交接面；真码行摘 `gather_and_adds.asc` | 双引擎分工 + 数据流向，结构图 |
| 图 11-4 MemBase vs RegBase | SVG | 双流水对照：MemBase（算一步→写回 UB→再读→算下一步，UB 读写 N 次）vs RegBase（UB→Register 一次装载，中间结果留寄存器，VF 融合链）；标注读写次数差 = 性能来源 | 第2章已有 mini-mermaid，此处深化为寄存器文件视角 |
| 图 11-5 950 新特性分类图 | Mermaid | 13 项特性按「计算单元 / 搬运通路 / 同步 / 存储结构 / 低比特类型」五组归类，标注与 ch2 能力菜单、ch10 已讲项的呼应 | 分类树，Mermaid 足够 |

**锚点（≤5）**：`asc_950_feature_guide.md`（13 特性表）、`examples/05_simd_simt_hybrid/.../gather_and_adds.asc`、`examples/03_simt_api/00_introduction/{00_quickstart/hello_world_simt,01_gather/gather_1d}`、`examples/02_simd_c_api/03_c_api/02_reg_vector_compute/`、`cann-learning-hub/blogs/operator/regbase_vec_add/`。其余（simt_builtin_keywords、simt_language_extension_c_api、vf_optimization 两篇）进脚注。

**验收**：CUDA 老手 30 分钟能写出第一个 SIMT gather；读者能判断自己的算子该用 SIMD/SIMT/混合/RegBase 四条路中的哪条；verify 绿。

### 第12章 编译、工具链与部署（M3-4 详细方案）

**章节结构（骨架 8 节收拢为 6 节）**
1. **编译总流程与产物**：bisheng 命令行（`bisheng x.asc -o out --npu-arch=dav-xxxx`）；异构编译四路（Host 编译 / Cube 二进制 / Vector 二进制 → Fatbin 链接 → 与 Host 二进制合并 → 可执行）；产物 anatomy 与第 5 章 binary_loader 衔接（编译终点=加载起点）；真码：`examples/01_simd_cpp_api/02_features/04_compile/00_basic_compile/`
2. **`--npu-arch` 与跨代际编译**：dav-2201（A2/A3）/dav-3510（950）映射与查证方法（文档实际只出现这两个值+`dav-xxxx` 占位，**不硬造 dav-2002**——骨架期登记的值待写作时再证）；950 编译迁移（`2201_to_3510_guide/op_compilation_migration.md`）
3. **工程组织与四种编译形态**：全程序（默认）/ 单独编译（`-dc` + extern 强制约束 + LTO 补性能）/ 动态库 / 静态库（四例真码）；CMake 实战（`ops-nn/cmake/{custom_kernel,gen_ops_info}.cmake` 真仓组织 + asc-devkit `tools/build`）
4. **RTC 运行时编译**：动机（大模型动态 shape 逐个最优 + 源码交付迭代便利）→ `aclrtc` 接口流程（`ACL_RTC_NPU_ARCH` 宏默认 dav-2201 真码）→ 静态 vs RTC 对比；锚点博客 `ascendc_rtc_compilation`
5. **NPU Simulator 无卡开发**：SoC 级仿真（bit 级精度 + 指令流水图）、与真板二进制兼容；**约束表**（仅 950PR/950DT、单卡、不支持 MC2/HCCL、不支持 arm 宿主）
6. **部署与工具箱**：单算子/多算子包（`multi_operator_package.md`）、交叉编译、编译加速、编译调试（`compilation_debug.md`，衔接第 7 章 DFX）+ 陷阱表（-dc 忘 extern、arch 选错、Simulator 约束踩坑）

**配图方案（3 张）**
| 图 | 类型 | 内容 |
|---|---|---|
| 图 12-1 从 .asc 到可执行：异构编译流水线 | SVG | 本章核心记忆图：`.asc`/`.cpp` 源 → bisheng 分三路编译（Host/Cube/Vector）→ Fatbin 链接 → 合并可执行 → 右侧接第 5 章 binary_loader（编译终点=加载起点）；标注 `--npu-arch` 在分路口选型 |
| 图 12-2 静态编译 vs RTC 运行时编译 | Mermaid | 双泳道流程对比：离线（编译→部署二进制→加载）vs 在线（部署源码/中间码→运行时 aclrtc 编译→执行）；标动态 shape 动机 |
| 图 12-3 编译形态选型树 | Mermaid | 全程序/单独/动态库/静态库/RTC 五分支决策树，叶节点给适用场景与代价 |

Simulator 节用表格（约束多、无图必要）。

**锚点（≤5）**：`compilation_and_execution/operator_compilation/{bisheng_compiler.md,rtc_runtime_compilation.md,ai_core_operator_compilation.md}`、`examples/01_simd_cpp_api/02_features/04_compile/`、`ops-nn/cmake/`、`cann-learning-hub/blogs/operator/ascendc_rtc_compilation/`、`ops-nn/docs/zh/debug/npu_sim.md`。其余（cross_compilation、multi_operator_package、compilation_acceleration、2201→3510 迁移）进脚注。

**明示边界（§8）**：BiSheng 编译器源码不在开源仓——只写「文档+产物+用法」级；`dav-2002` 等骨架期猜测值写作时逐个取证，证不到就删。

**验收**：读者能把一个 `.asc` 沿静态/RTC 两条路走到能跑；`--npu-arch` 会选会查；没卡时知道用 Simulator；verify 绿。

### 第13章 算子库体系（M3-5 详细方案）

**章节结构（骨架 6 节保持，重排重心）**
1. **三仓定位与版图**：ops-nn（高阶 NN：matmul/activation/quant/index/loss/conv/pooling/rnn/optim/foreach…）/ ops-transformer（进阶：attention/moe/mc2/ffn/gmm/posembedding）/ ops-sparse（2026-05 上线：SpMM/SpMV，仅 CANN 9.0.0+）；三仓同构（build.sh/cmake/classify_rule.yaml/CONTRIBUTING/experimental）；**版本配套纪律**（配 release 标签，master 有风险）；「先用库→再改模板→最后手写」呼应第9章决策树
2. **ops-nn 深看**：add_example 全链解剖（op_host def + op_kernel + config binary.json → 编译 → aclnn，衔接第4章两段式与第12章「目录即约定」）；量化矩阵（fp8/mxfp8/hifp8/mxfp4 × pertensor/perchannel/pertoken/pergroup/perblock，真例 quant_batch_matmul_v4）；SIMD/SIMT 同构算子（MapIndex/ScatterSub，衔接第11章）；ops-tensor 分层结构优化 Cube 类
3. **ops-transformer：大模型算子族谱**：attention 族（flash_attn/quant_flash_attn/sparse_flash_mla/lightning_indexer…DSV4 场景）/ moe / **mc2 通算融合**（matmul_allto_all、engram_fetch，衔接第17章通信伏笔）；时效性纪律：A5 每月上新，写作时以 CHANGELOG 当期为准；onnx 算子插件（framework 目录）
4. **ops-sparse 短节**：稀疏计算定位、SpMM/SpMV、与稀疏 4:2 量化 matmul 呼应
5. **开发与贡献路径**：`build.sh --genop=examples/add_example` 工程创建、最小交付件（aicore_develop_guide）、QUICKSTART（Docker）、experimental→正式目录贡献流（CONTRIBUTING）、npusim 调试衔接第12章
6. **二开方法论**：读一个库算子的标准动作清单（README→binary.json→tiling→kernel→调用侧）；torch_extension/NpuOpsTransformerExt 工程模板（PyTorch 张量操作+自动微分+GPU/NPU 统一接口）

**配图方案（3 张）**
| 图 | 类型 | 内容 |
|---|---|---|
| 图 13-1 三仓版图 + 典型算子解剖 | SVG | 核心：左半三仓定位地图（高阶/进阶/稀疏，各自覆盖域），右半一个典型算子的目录解剖（op_host/op_kernel/config → 编译 → aclnn API，双向衔接第4章 aclnn 与第12章构建系统） |
| 图 13-2 算子获取决策树 | Mermaid | 查 ops-nn → transformer/sparse → experimental → 改模板 → 手写 → 贡献回去，闭环 |
| 图 13-3 一个算子的完整交付链 | Mermaid | 源码目录 → binary.json → 编译(第12章) → 安装包 → aclnn 两段式调用(第4章) → torch_extension 可选 |

**锚点（≤5）**：`ops-nn/README.md`、`ops-nn/docs/QUICKSTART.md`、`ops-transformer/README.md`、`ops-transformer/docs/zh/develop/aicore_develop_guide.md`、`ops-sparse/README.md`。其余（contributing、torch_extension、experimental、classify_rule.yaml、算子级 README）进脚注。

**时效性纪律（§8）**：三仓上新极快（transformer 月更），正文只写结构性事实，算子清单给「截至写作时的族系+查证方法」，逐个算子不打包票；CHANGELOG 引用标注日期。

**验收**：读者能按图索骥找到目标算子并跑通「编译→安装→aclnn 调用」；知道改动后往哪贡献；verify 绿。

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
| M3-4 | 第12章成稿 | ✅ 完成（3.8k总字/2.9k中文，3图；dav-2002 证伪不采信） |
| M3-5 | 第13章成稿 | 同上 |
| M3-6 | 第14章成稿（收口章） | 同上 + 第三编总回顾 |

- 每章收口：frontmatter `status` 改「已成稿（M3，第三编）」→ appD 同步 → CHANGELOG 记录 → README 里程碑更新 → push（Pages 自动发布）。
- 每章完稿后执行自查 review：重读全文、核对 API/路径拼写、表格无裸 `|`、图表齐注、无 TODO 残留、与四大能力目标对齐。

## 4. 风险与边界

1. **无真机**：所有 `[可在 NPU 运行]` 论断只能来自仓内 examples 的官方标注，自己跑不了——统一 `[需真机验证]` + 验证步骤（§8/§10）。
2. **SIMT 材料新**：950 起才有 SIMT，旧架构读者需明确「你的芯片可能用不了」；对照 CUDA 时不得暗示 API 完全等价。
3. **模板库在外部仓**（ATVC/ATVOSS/CATLASS/pyasc 在 gitcode）：只写定位与入口，不展开内部实现（源码不在本地基线内）。
4. **字数目标**：核心章 8k–12k 中文（§4）；地图章/工具章可按 M2 先例（3–4k 中文）不注水，宁缺毋滥。
