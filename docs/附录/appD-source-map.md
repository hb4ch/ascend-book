---
title: 附录D 来源映射表
description: 每章 → 源仓路径对照，写作自我一致性的基准
---

# 附录D 来源映射表

> 维护规则：随写作扩展，新增章/改出处必须同步本表。`npm run check:source` 校验脚本的路径基准也是 `/mnt/SATASSDEXT4/cann/`。
> 每个引用必须精确 `repo/path`；本表用「章 → 主来源路径（启发集合，非穷尽）」形式记录，正文以行内 `📦 源码:` / `📄 资料:` 精标。

## 第一编 昇腾平台全景

> 2026-XX 第一编按三轮迭代重写：正文改为「先人话后术语」叙事，行内引用全部脚注化（聚合于每章末尾「本章来源与进一步阅读」）；图表升级为 Mermaid（每章 ≥2 张）。下表的「主来源路径」仍是全文的总账本，正文不再重复。

| 章 | 主来源路径 |
|---|---|
| 第1章 平台与生态总览 | `runtime/include/external/acl/acl_rt.h`、`runtime/example/0_quickstart/{0_hello_cann,1_error_handling,4_custom_kernel_launch}/`、`asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/add/add.asc`、`ops-nn/examples/add_example/`、`asc-devkit/docs/zh/asc_950_feature_guide.md`、`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/abstract_hardware_architecture.md`、`runtime/include/external/acl/error_codes/`、`runtime/docs/zh/api_ref/06_stream_management.md` |
| 第2章 硬件体系结构 | `asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/basic_architecture.md`、`…/abstract_hardware_architecture.md`、`asc-devkit/docs/zh/guide/technical_appendix/concepts_and_terms/memory_access/scalar_read_write.md`、`asc-devkit/docs/zh/.../memory_vector_computation.md`、`asc-devkit/examples/01_simd_cpp_api/00_introduction/{01_add/add/add.asc,02_matrix/matmul_basic_api/matmul_basic_api.asc}`、`asc-devkit/docs/zh/asc_950_feature_guide.md`、`cann-learning-hub/blogs/operator/{nddma_introduction,regbase_vec_add,ascend950_aiv_urma_shmem_communication}/` |
| 第3章 执行主链路 | `runtime/src/runtime/{api,core/src/{stream,launch,task,kernel,device}}/`（含 `task/task_to_sqe.cc`）、`runtime/src/queue_schedule/server/`（含 `fsm/`、`queue_manager.h`、`state_manager.cpp`）、`runtime/src/tsd/tsdclient/`、`runtime/src/runtime/feature/model/model_c.cc`、`runtime/docs/zh/api_ref/{06_stream_management,07_event_management}.md`、`runtime/example/1_basic_features/event/`、`cann-learning-hub/blogs/inference/{npugraph_ex_aclgraph_graph_mode,aot_superkernel_graph_execution}/` |

## 第二编 运行时、驱动与维测底层

| 章 | 主来源路径 |
|---|---|
| 第4章 ACL 编程接口 | `runtime/include/external/acl/{acl_rt.h,acl.h,acl_op.h,acl_rt_api.h}`、`error_codes/{rt_error_codes.h,ge_error_codes.h}`，`runtime/example/0_quickstart/{0_hello_cann,1_error_handling,4_custom_kernel_launch}/`，`runtime/example/1_basic_features/{device,context,stream,event,memory}/`，`runtime/docs/zh/api_ref/{01~14,21,22}_*.md`、`runtime/docs/zh/error_code_ref/`，`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/aclnn_operator_development` |
| 第5章 运行时核心实现 | `runtime/src/runtime/core/src/task/task_to_sqe.cc`、`runtime/pkg_inc/runtime/rt_external_preload.h`、`runtime/src/runtime/core/src/stream/{stream_factory.cc,stream.cc}`、`runtime/src/runtime/core/src/kernel/binary_loader.cc`、`runtime/src/runtime/core/src/device/ctrl_sq.cc`、`runtime/src/runtime/core/inc/base.hpp`、`runtime/src/queue_schedule/server/{fsm/,queue_manager.h,state_manager.cpp}`、`runtime/src/tsd/tsdclient/src/`、`runtime/src/aicpu_sched/`、`runtime/src/tprt/`、`runtime/src/runtime/feature/model/model_c.cc`、`runtime/docs/zh/design/modules/{stream,task,kernel,device}.md` |
| 第6章 驱动与系统软件协同 | `runtime/src/runtime/driver/`（`npu_driver*.cc`、`driver.cc`（DriverFactory）、`v100/v200/v201`、`npu_driver_base[_soma].hpp`、`npu_driver_dcache_lock_{common,david,opb}.cpp`、`xpu_driver`）、`runtime/src/cmodel_driver/`、`runtime/docs/zh/design/{architecture.md,modules/device/device.md,modules/memory/memory.md}`；内核态 `ascend_km` / `/dev/davinci*` 为概念性描述（源码不在开源仓） |
| 第7章 维测子系统 DFX | `runtime/src/dfx/{msprof,adump,log,trace,error_manager}/`，`runtime/docs/zh/{api_ref,design,log_ref,error_code_ref}`，`cann-learning-hub/blogs/operator/{ms_sanitizer,dumptensor_operator_debugging}/` |
| 第8章 内存与数据通路 | `asc-devkit/docs/zh/guide/programming_guide/{programming_model/ai_core_simd_programming/abstract_hardware_architecture.md,advanced_programming/hardware_implementation/basic_architecture.md}`、`runtime/include/external/acl/acl_rt.h`（内存分配/策略）、`asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/DataCopy_GMToUB_NDDMA.md`、`asc-devkit/examples/01_simd_cpp_api/03_basic_api/00_data_movement/data_copy_gm2ub_nddma/`、`cann-learning-hub/blogs/operator/nddma_introduction/深入理解NDDMA多维数据搬运-昇腾算子开发性能优化利器.md`、`runtime/src/tprt/` |

## 第三编 算子开发：Ascend C

| 章 | 主来源路径 |
|---|---|
| 第9章 编程模型与 API 选择 | `asc-devkit/docs/zh/asc_how_to_choose_api.md`，`asc-devkit/docs/zh/guide/programming_guide/programming_model/{programming_model_overview.md,heterogeneous_system.md}`，`asc-devkit/docs/zh/guide/getting_started/ascend_c_overview_and_learning_path.md`，`asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/add_tpipe_tque/add_tpipe_tque.asc`，`asc-devkit/examples/02_simd_c_api/00_introduction/01_add/c_api_sync_add/c_api_add.asc`，`asc-devkit/examples/03_simt_api/00_introduction/01_gather/basic_gather/gather_1d/gather_1d.asc`，`asc-devkit/include/c_api/asc_simd.h`，`asc-devkit/README.md`（PyAsc 定位） |
| 第10章 核心编程能力 | `asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/tpipe_tque_programming/{tpipe_tque_paradigm.md,tpipe_tque_principles.md}`，`…/cpp_tensor_programming/cpp_tensor_programming_overview.md`，`asc-devkit/docs/zh/api/SIMD-API/basic_api/{memory_vector_compute/data_move/,sync_control/system_sync_overview.md,basic_api_list.md}`，`asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/{DataCopy_GMToUB_NDDMA.md,DataCopyPad_GMToUB.md}`，`asc-devkit/examples/01_simd_cpp_api/03_basic_api/00_data_movement/data_copy_gm2ub_nddma/multidimensional_data_movement.asc`，`asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/{add_tpipe_tque/add_tpipe_tque.asc,add/add.asc}`，`asc-devkit/include/kernel_operator.h`，`asc-devkit/impl/{basic_api,c_api,tensor_api,aicpu_api}/`，`asc-devkit/include/` |
| 第11章 SIMD/SIMT 与高级特性 | `asc-devkit/impl/{simt_api,c_api}/`，`asc-devkit/docs/zh/asc_950_feature_guide.md`，`asc-devkit/docs/zh/guide/programming_guide/language_extension/{simt_builtin_keywords.md,simd_builtin_keywords.md}`，`asc-devkit/docs/zh/api/SIMD-API/basic_api/sync_control/system_sync_overview.md`，`asc-devkit/examples/05_simd_simt_hybrid/00_introduction/simd_simt_gather_and_adds/gather_and_adds.asc`，`asc-devkit/examples/03_simt_api/00_introduction/00_quickstart/hello_world_simt/hello_world.asc`，`asc-devkit/examples/03_simt_api/05_troubleshooting/stack_overflow/`，`asc-devkit/examples/04_aicpu/README.md`，`asc-devkit/examples/02_simd_c_api/03_c_api/02_reg_vector_compute/`，`cann-learning-hub/blogs/operator/regbase_vec_add/` |
| 第12章 编译、工具链与部署 | `asc-devkit/docs/zh/guide/compilation_and_execution/`（bisheng_compiler.md、rtc_runtime_compilation.md、ai_core_operator_compilation.md），`asc-devkit/scripts/`，`asc-devkit/tools/`，`cann-learning-hub/blogs/operator/ascendc_rtc_compilation/`，`ops-nn/docs/zh/debug/npu_sim.md` |
| 第13章 算子库体系 | `ops-nn/README.md`、`docs/`、`experimental/`、`torch_extension/`，`ops-transformer/README.md`、`ops-sparse/README.md`，`ops-nn/docs/zh/develop/`、`docs/QUICKSTART.md` |
| 第14章 算子实战 | `cann-learning-hub/tutorials/ascendc_operator_development/`，`asc-devkit/examples/01_simd_cpp_api/05_best_practices/`，`ops-nn/matmul`、`ops-transformer/attention`（+ Flash Attention 精要），`cann-learning-hub/blogs/operator/*` |

## 第四编 性能优化方法论

| 章 | 主来源路径 |
|---|---|
| 第15章 性能分析 | `runtime/src/dfx/msprof/`，`runtime/docs/zh/`，`asc-devkit/docs/zh/guide/programming_guide/debug_and_tuning/`，`pto-isa/docs/coding/opt_zh.md`，`asc-devkit/examples/01_simd_cpp_api/06_profiling/` |
| 第16章 优化专题 | `asc-devkit/examples/01_simd_cpp_api/05_best_practices/`，`asc-devkit/docs/zh/asc_950_feature_guide.md`，`cann-learning-hub/blogs/operator/{mx_quantized_matmul_optimization,scalar_npu_operator_performance_optimization,cross_entropy_zloss_fusion,ascend_c_mmad_selection_guide}/`，`ops-nn/docs/` |

## 第五编 分布式通信

| 章 | 主来源路径 |
|---|---|
| 第17章 HCCL | `hcomm/README.md`，`hcomm/src/base_comm/`，`hcomm/src/coll_communicator_mgr/`，`hcomm/docs/zh/`，`hcomm/examples/`，`cann-learning-hub/tutorials/hccl_development/`，`blogs/operator/{hccl_custom_operator_aicpu_p2p,hccl_reducescatter_high_precision_redevelopment}/` |
| 第18章 HIXL | `hixl/README.md`，`hixl/docs/zh/{api,guide}/`，`hixl/examples/`，`hixl/src/hixl/`，`hixl/benchmarks/`，`cann-learning-hub/tutorials/hixl_development/`，`blogs/inference/hixl_{fabricmem_kv_cache_transfer,mooncake_vllm_kv_cache_pooling,...}/` |
| 第19章 通算融合与大规模系统 | `ops-transformer/mc2/`，`pto-isa/kernels/manual/a2a3/gemm_ar/`，`cann-learning-hub/tutorials/MC2_fused_operator_development/`，`blogs/inference/deepseek_*`、`blogs/training/*` |

## 第六编 现代编译后端与编程范式

| 章 | 主来源路径 |
|---|---|
| 第20章 PTO 虚拟 ISA | `pto-isa/docs/{README_zh,PTO-Virtual-ISA-Manual_zh,isa/,coding/,machine/,figures}`，`pto-isa/include/pto/`，`pto-isa/kernels/`，`pto-isa/demos/`，`pto-isa/tests/` |
| 第21章 PyPTO | `pypto/README.md`，`pypto/framework/{src/passes,src/codegen,include}`，`pypto/python/pypto/`，`pypto/docs/zh/tutorials/`，`pypto/examples/{01_beginner,02_intermediate,03_advanced}/`，`pypto/models/` |
| 第22章 生态与前沿 | `pypto/README.md`，`pto-isa/README_zh.md`，`cann-learning-hub/blogs/{inference/torchair_fx_pass_multi_stream,aot_superkernel_graph_execution,npugraph_ex_third_party_framework_integration,operator/tilelang_ascend_operator_optimization}/`，`asc-devkit`（PyAsc 规划） |
| 第23章 综合案例 | `ops-transformer/attention/`、`cann-learning-hub/blogs/inference/longcat_*`、`deepseek_*`、`pto-isa/kernels/manual/`（MLA 落点待定） |

## 第七编 展望

| 章 | 主来源路径 |
|---|---|
| 第24章 路线图 | 各仓 `README`/`ReleaseNote_zh.md`/`CHANGELOG.md` 的 Roadmap 声明，`cann-learning-hub/blogs/README.md` |
