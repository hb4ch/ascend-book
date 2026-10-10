---
title: 附录D 来源映射表
description: 每章 → 源码导航入口；读者溯源由此进，论断级证据见各章脚注
---

# 附录D 来源映射表

> **本表是导航，不是论断证明**：每章至多 3 个主入口，以短名呈现；**完整路径见页末脚注**。支撑具体论断的逐条证据，见该章末「本章来源与进一步阅读」。路径基准为本书源码快照（版本见 `management/SOURCE-BASELINE.md`），`npm run check:source` 据此校验；引用与结论的支持关系以各章脚注及正文为准。

## 第一编 昇腾平台全景

| 章 | 主入口 |
|---|---|
| [第1章 平台与生态总览](../01-platform/ch01-overview.md) | 快速上手样例[^d1a]、Add 样例[^d1b]、ACL C 接口头[^d1c] |
| [第2章 硬件体系结构](../01-platform/ch02-hardware.md) | 硬件实现总览[^d2a]、SIMD 抽象架构[^d2b]、950 特性指南[^d2c] |
| [第3章 执行主链路](../01-platform/ch03-exec-path.md) | 任务转 SQE 与调度服务[^d3a]、TSD 客户端[^d3c]、Event 样例[^d3d] |

[^d1a]: `runtime/example/0_quickstart/0_hello_cann/`
[^d1b]: `asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/add/add.asc`
[^d1c]: `runtime/include/external/acl/acl_rt.h`
[^d2a]: `asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/basic_architecture.md`
[^d2b]: `asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/abstract_hardware_architecture.md`
[^d2c]: `asc-devkit/docs/zh/asc_950_feature_guide.md`
[^d3a]: `runtime/src/runtime/core/src/task/task_to_sqe.cc`、`runtime/src/queue_schedule/server/`
[^d3c]: `runtime/src/tsd/tsdclient/`
[^d3d]: `runtime/example/1_basic_features/event/`

## 第二编 运行时、驱动与维测

| 章 | 主入口 |
|---|---|
| [第4章 ACL 编程接口](../02-runtime/ch04-acl.md) | ACL 头文件族[^d4a]、官方案例目录[^d4b]、Runtime API 参考[^d4c] |
| [第5章 运行时核心实现](../02-runtime/ch05-runtime-impl.md) | 核心机制四文件[^d5a]、设计文档·模块篇[^d5e] |
| [第6章 驱动与系统软件协同](../02-runtime/ch06-driver.md) | 用户态驱动适配层[^d6a]、cmodel 驱动[^d6b]、架构总览[^d6c]（内核态 `ascend_km`/`/dev/davinci*` 为概念性描述，源码不在开源仓） |
| [第7章 维测子系统 DFX](../02-runtime/ch07-dfx.md) | DFX 五模块[^d7a]、Dump 配置接口[^d7b]、精度/调试案例[^d7c] |
| [第8章 内存与数据通路](../02-runtime/ch08-memory.md) | 第 2 章两篇架构文档（[^d2a][^d2b]）、NDDMA 接口页[^d8a]、NDDMA 样例[^d8b] |

[^d4a]: `runtime/include/external/acl/`（`acl_rt.h`、`acl.h`、`acl_op.h` 等）
[^d4b]: `runtime/example/0_quickstart/`、`runtime/example/1_basic_features/`
[^d4c]: `runtime/docs/zh/api_ref/`（01–14 号主题文件）
[^d5a]: `runtime/src/runtime/core/src/task/task_to_sqe.cc`、`runtime/src/runtime/core/src/stream/stream_factory.cc`、`runtime/src/runtime/core/src/kernel/binary_loader.cc`、`runtime/src/runtime/core/src/device/ctrl_sq.cc`
[^d5e]: `runtime/docs/zh/design/modules/stream/stream.md`、`runtime/docs/zh/design/modules/task/task.md`、`runtime/docs/zh/design/modules/kernel/kernel.md`、`runtime/docs/zh/design/modules/device/device.md`
[^d6a]: `runtime/src/runtime/driver/`（`driver.cc` 工厂与 `npu_driver*` 族）
[^d6b]: `runtime/src/cmodel_driver/`
[^d6c]: `runtime/docs/zh/design/architecture.md`
[^d7a]: `runtime/src/dfx/{msprof,adump,log,trace,error_manager}/`
[^d7b]: `runtime/docs/zh/api_ref/18_dump_configuration.md`
[^d7c]: `cann-learning-hub/blogs/operator/ms_sanitizer/`、`cann-learning-hub/blogs/operator/dumptensor_operator_debugging/`
[^d8a]: `asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/DataCopy_GMToUB_NDDMA.md`
[^d8b]: `asc-devkit/examples/01_simd_cpp_api/03_basic_api/00_data_movement/data_copy_gm2ub_nddma/`

## 第三编 算子开发：Ascend C

| 章 | 主入口 |
|---|---|
| [第9章 编程模型与 API 选择](../03-ascendc/ch09-api-map.md) | 多级 API 选择指南[^d9a]、三类 API 的 Add/Gather 例[^d9b] |
| [第10章 核心编程能力](../03-ascendc/ch10-core-programming.md) | TPipe/TQue 编程范式[^d10a]、Tensor 编程总览[^d10b]、基础 API 参考[^d10c] |
| [第11章 SIMD/SIMT 与高级特性](../03-ascendc/ch11-simd-simt.md) | 语言扩展关键字[^d11a]、950 特性指南[^d2c]、SIMD/SIMT 混合样例[^d11b] |
| [第12章 编译、工具链与部署](../03-ascendc/ch12-compile-tools.md) | 算子编译指南与 AOT 优化[^d12a]、编译特性样例[^d12c]、工程配置与仿真说明[^d12d] |
| [第13章 算子库体系](../03-ascendc/ch13-operator-libs.md) | 三算子仓 README[^d13a]、开发指南[^d13b] |
| [第14章 实战Ⅰ：Add 与工程链路](../03-ascendc/ch14-op-practice.md) | ops-nn Add 例[^d14a]、asc-devkit Add 样例[^d14b]、教程绪论[^d14c] |
| [第15章 实战Ⅱ：向量算子](../03-ascendc/ch15-vector-softmax.md) | Softmax/GELU 高性能例[^d15a]、VF 优化指南[^d15b] |
| [第16章 实战Ⅲ：矩阵算子](../03-ascendc/ch16-matmul-cube.md) | Matmul 教程[^d16a]、高性能双实现[^d16b]、访存与Cube存储[^d16c] |
| [第17章 实战Ⅳ：融合算子](../03-ascendc/ch17-fusion.md) | MatMul+GELU 例[^d17a]、量化分组 MatMul 例[^d17b]、跨核同步 API[^d17c] |
| [第18章 Flash Attention](../03-ascendc/ch18-flash-attention.md) | FA kernel（arch35）[^d18a]、公共组件[^d18b]、ACLNN 调用样例[^d18c] |

[^d9a]: `asc-devkit/docs/zh/asc_how_to_choose_api.md`
[^d9b]: `asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/add_tpipe_tque/add_tpipe_tque.asc`、`asc-devkit/examples/02_simd_c_api/00_introduction/01_add/c_api_sync_add/c_api_add.asc`、`asc-devkit/examples/03_simt_api/00_introduction/01_gather/basic_gather/gather_1d/gather_1d.asc`
[^d10a]: `asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/tpipe_tque_programming/`
[^d10b]: `asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/cpp_tensor_programming/cpp_tensor_programming_overview.md`
[^d10c]: `asc-devkit/docs/zh/api/SIMD-API/basic_api/`（data_move/sync_control 各页）
[^d11a]: `asc-devkit/docs/zh/guide/programming_guide/language_extension/simt_builtin_keywords.md`、`asc-devkit/docs/zh/guide/programming_guide/language_extension/simd_builtin_keywords.md`
[^d11b]: `asc-devkit/examples/05_simd_simt_hybrid/`
[^d12a]: `asc-devkit/docs/zh/guide/programming_guide/compilation_and_execution/operator_compilation/`（bisheng/ai_core/rtc/constraints）、`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/aot_compilation_optimization.md`
[^d12c]: `asc-devkit/examples/01_simd_cpp_api/02_features/04_compile/`
[^d12d]: `ops-nn/cmake/custom_kernel.cmake`、`ops-nn/docs/zh/debug/npu_sim.md`
[^d13a]: `ops-nn/README.md`、`ops-transformer/README.md`、`ops-sparse/README.md`
[^d13b]: `ops-nn/docs/QUICKSTART.md`、`ops-transformer/docs/zh/develop/aicore_develop_guide.md`
[^d14a]: `ops-nn/examples/add_example/{op_host,op_kernel}/`
[^d14b]: `asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/`（Tensor 与 TPipe/TQue 样例）
[^d14c]: `cann-learning-hub/tutorials/ascendc_operator_development/01_basic_overview/`
[^d15a]: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/02_reg_compute/softmax_high_performance/`、`asc-devkit/examples/01_simd_cpp_api/05_best_practices/02_reg_compute/gelu_high_performance/`
[^d15b]: `asc-devkit/docs/zh/guide/operator_practice/simd_operator_optimization/vector_compute/vf_optimization/`
[^d16a]: `cann-learning-hub/tutorials/ascendc_operator_development/04_matmul_basic/`
[^d16b]: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_high_performance/`、`asc-devkit/examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_basic_api_high_performance/`
[^d16c]: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/04_memory_access/`、`asc-devkit/docs/zh/api/SIMD-API/basic_api/cube_compute_ISASI/cube_compute_store/`
[^d17a]: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/03_fusion_compute/matmul_gelu_high_performance/`
[^d17b]: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/03_fusion_compute/quant_group_matmul_high_performance/`
[^d17c]: `asc-devkit/docs/zh/api/SIMD-API/basic_api/sync_control/inter_core_sync/`
[^d18a]: `ops-transformer/attention/flash_attention_score/op_kernel/arch35/`
[^d18b]: `ops-transformer/attention/common/op_kernel/`（buffer 策略与 regbase 公共头）
[^d18c]: `ops-transformer/attention/flash_attention_score/examples/test_aclnn_flash_attention_score.cpp`

## 第四编 性能优化

| 章 | 主入口 |
|---|---|
| [第19章 性能分析](../04-perf/ch19-perf-analysis.md) | msprof 分析器与 API 头[^d19a]、性能调优指南[^d19c]、PTO 优化笔记[^d19d] |
| [第20章 优化专题](../04-perf/ch20-opt-topics.md) | 访存专题例[^d20a]、SIMD+SIMT 高性能例[^d20b]、稀疏与低精度例[^d20c] |

[^d19a]: `runtime/src/dfx/msprof/collector/dvvp/`（analyzer 与 op_analyzer）、`runtime/src/dfx/msprof/inc/toolchain/prof_acl_api.h`
[^d19c]: `asc-devkit/docs/zh/guide/programming_guide/debug_and_tuning/performance_tuning.md`
[^d19d]: `pto-isa/docs/coding/opt_zh.md`
[^d20a]: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/04_memory_access/bank_conflict_nd2nz/`、`asc-devkit/examples/01_simd_cpp_api/05_best_practices/04_memory_access/data_copy/`
[^d20b]: `asc-devkit/examples/05_simd_simt_hybrid/02_best_practices/simd_simt_high_performance/`
[^d20c]: `asc-devkit/examples/01_simd_cpp_api/03_basic_api/03_matrix_compute/mmad_with_sparse/`、`asc-devkit/examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_mxfp4_basic_api_high_performance/`

## 第五编 分布式通信

| 章 | 主入口 |
|---|---|
| [第21章 HCCL](../05-comm/ch21-hccl.md) | 通信样例[^d21a]、legacy 归约实现（内部案例）[^d21b]、架构总览与 asc-devkit 特化[^d21c] |
| [第22章 HIXL](../05-comm/ch22-hixl.md) | 快速上手例[^d22a]、引擎与客户端[^d22b]、性能基准说明[^d22d] |
| [第23章 通算融合与大规模系统](../05-comm/ch23-supernode.md) | MC2 算子目录[^d23a]、PTO AllReduce 融合 kernel[^d23b]、MC2 教程[^d23c]；超节点案例见章内脚注 |

[^d21a]: `hcomm/examples/01_communicators/01_one_device_per_process/`
[^d21b]: `hcomm/src/legacy/ascend910/algorithm/impl/operator/all_reduce_operator.cc`
[^d21c]: `hcomm/docs/zh/architecture/architecture-brief.md`、`asc-devkit/impl/adv_api/detail/hccl/`（2201/3510 特化分派）
[^d22a]: `hixl/examples/cpp/hixl_example_quickstart.cpp`
[^d22b]: `hixl/src/hixl/engine/hixl_engine.cc`、`hixl/src/hixl/cs/hixl_cs_client.cc`
[^d22d]: `hixl/benchmarks/performance.md`
[^d23a]: `ops-transformer/mc2/`
[^d23b]: `pto-isa/kernels/manual/a2a3/gemm_ar/`
[^d23c]: `cann-learning-hub/tutorials/MC2_fused_operator_development/`

## 第六编 编译后端与编程范式

| 章 | 主入口 |
|---|---|
| [第24章 PTO 虚拟 ISA](../06-backend/ch24-pto-isa.md) | PTO README[^d24a]、虚拟 ISA 手册[^d24b]、isa/coding/machine 与 kernels/demos[^d24c] |
| [第25章 PyPTO](../06-backend/ch25-pypto.md) | PyPTO README[^d25a]、编译框架与前端[^d25b]、教程与分级示例[^d25d] |
| [第26章 生态与前沿](../06-backend/ch26-ecosystem.md) | 图模式/FX Pass/超核博文[^d26a]、TileLang 实践[^d26b]；PyAsc 定位见 asc-devkit README（Python 前端段）[^d26c] |
| [第27章 全栈综合案例](../06-backend/ch27-case.md) | SparseAttention 工程分支[^d27a]、DSA 贡献实录[^d27b]；细粒度锚点见本章脚注 |

[^d24a]: `pto-isa/README_zh.md`
[^d24b]: `pto-isa/docs/PTO-Virtual-ISA-Manual_zh.md`
[^d24c]: `pto-isa/docs/isa/`、`pto-isa/docs/coding/`、`pto-isa/docs/machine/`、`pto-isa/kernels/`、`pto-isa/demos/`
[^d25a]: `pypto/README.md`
[^d25b]: `pypto/framework/{src/passes,src/codegen,include}/`、`pypto/python/pypto/`
[^d25d]: `pypto/docs/zh/tutorials/`、`pypto/examples/{01_beginner,02_intermediate,03_advanced}/`
[^d26a]: `cann-learning-hub/blogs/inference/npugraph_ex_aclgraph_graph_mode/`、`cann-learning-hub/blogs/inference/torchair_fx_pass_multi_stream/`、`cann-learning-hub/blogs/inference/aot_superkernel_graph_execution/`
[^d26b]: `cann-learning-hub/blogs/operator/tilelang_ascend_operator_optimization/`
[^d26c]: `asc-devkit/README.md`（Python 前端段）
[^d27a]: `ops-transformer/attention/sparse_flash_attention/`（快照 `e75072d7`：examples/op_host/op_kernel/tests）
[^d27b]: `cann-learning-hub/blogs/operator/dsa_operator_open_source_contribution/`

## 第七编 展望

| 章 | 主入口 |
|---|---|
| [第28章 路线图](../07-outlook/ch28-roadmap.md) | asc-devkit 变更记录与 Tensor/VF 样例[^d28a]、HIXL 边界[^d28b]、PTO 路线[^d28c]；公告/计划/代码边界见章内声明 |

[^d28a]: `asc-devkit/CHANGELOG.md` 及第 10/16 章所引 Tensor/VF 样例
[^d28b]: `hixl/README.md`、`hixl/docs/zh/FabricMem.md`
[^d28c]: `pto-isa/README_zh.md`、`pto-isa/ReleaseNote_zh.md`、`pypto/README.md`
