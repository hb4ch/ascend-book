---
title: 附录B 术语表
description: 全书术语唯一源（由根目录 glossary.md 同步生成，勿手改）
---

# 附录B 术语表

<!-- 自动由 npm run sync:glossary 生成；修改请在仓库根目录 glossary.md -->

# 术语表（glossary）

> 全书术语用词的**统一维护入口**。中英对照、一义一译、全书统一。`check:terms` 依据本表校验正文高频术语用词一致。
> 本站同步进「附录B 术语表」，构建期自动复制。新增术语→先在此登记→再全书替换。

约定：**加粗**为推荐译法；「不译」表示正文直接使用英文。

## 平台与芯片

| 英文 | 中文 | 说明 / 出处 |
|---|---|---|
| Ascend / 昇腾 | 昇腾 | 华为 AI 处理器品牌 |
| AI Core | AI Core（不译） | 昇腾 AI 处理器的计算单元；Cube/Vector 部署形态随架构而异（部分架构同核共享 Scalar，部分分核）[^1] |
| Cube Core | Cube（不译） | 分核架构中的矩阵计算核，含 Scalar、矩阵计算与搬运单元；2002 的同核形态见 AI Core，不套用此组成[^28] |
| Vector Core | Vector（不译） | 分核架构中的矢量计算核，含 Scalar、矢量计算与搬运单元；与同核架构中的矢量计算单元区分[^28] |
| Scalar | 标量（不译） | AI Core 标量计算单元：标量运算，并承担对 MTE/Vector/Cube 的指令发射[^28] |
| AICPU | AICPU（不译） | 设备侧辅助 CPU 核，可承担不适合 AI Core 的计算及调度任务[^5] |
| MTE2 | MTE2（不译） | Memory Transfer Engine 2：GM→L1/L0A/L0B/UB 搬入流水（能力随硬件）[^28] |
| MTE3 | MTE3（不译） | 内存搬运流水；2201/2002 叙述与 3510 带宽表中见 UB→GM、UB→L1；完整通路随架构而异[^1] |
| MTE1 | MTE1（不译） | 内存搬运流水；各架构带宽表中见 L1→L0A/L0B，3510 另有 L1→UB（PIPE_MTE1）；完整通路随架构而异[^1] |
| AIV（AI Vector） | AIV 矢量核 | AI Core 分离模式下一组 Cube/Vector Core 组合中的 Vector Core（分核形态见 2201/3510）[^28] |
| AIC（AI Cube） | AIC 核 | AI Cube 核，分核架构中的矩阵核（释义见 cpp_tensor_programming_overview[^3]；分核形态见架构规格[^1]） |
| GM / HBM | 全局内存 / 高带宽内存 | GM=设备侧全局内存地址空间（核内 `__gm__`，host 经 Runtime API 使用）[^28]；HBM=存储介质，两者对应关系由架构/平台规格定义 |
| SMEM（Shared Memory） | SMEM 共享内存 | SIMT 编程中 UB 按功能划分出的线程块共享内存区（Data Cache 为 UB 内另一分区，勿混）；见 SIMT 编程抽象架构文档[^3] |
| URMA | URMA（不译） | Unified Remote Memory Access（统一远端内存访问）；hcomm/hixl 通信栈中的远端内存访问机制（CCU 依之搬运）[^8] |
| 910B / 910C | — | 昇腾910 系列两代，分别对应 Atlas A2/A3 |
| Ascend 950 / 950PR / 950DT | — | 昇腾950 系列（A5 平台）及 950PR/950DT |
| SOC | 片上系统 | 芯片整体 |
| die / multi-die | 芯粒 / 多芯粒 | 950 平台多芯粒封装 |

## 内存与数据

| 英文 | 中文 | 说明 |
|---|---|---|
| GM | 全局内存 | 设备侧全局内存地址空间：核函数内 `__gm__` 指针访问；host 侧按所用 Runtime API 分配/拷贝；与 HBM 的承载关系见架构规格（勿等同） |
| L1 Buffer | L1 缓冲 | Cube 侧高速缓冲：经 MTE1 向 L0A/L0B 供给矩阵输入，容量随架构[^1] |
| L0A / L0B / L0C | L0A/L0B/L0C | Cube 计算操作数缓冲：L0A 存左矩阵、L0B 存右矩阵、L0C 存结果与中间结果[^15] |
| UB（Unified Buffer） | 统一缓冲 | AI Core 内部存储，主要供矢量计算；容量按架构（如 2201=192KB、预留 256B）[^28] |
| L2 | L2 Cache | 片上二级缓存：缓存 GM 访问（含代码/数据段），以 Cache Line 为单位加载[^15] |
| Register | 寄存器 | 计算单元最内层存储；3510 起矢量计算构建「GM→UB→Register」三级流转并开放 Reg 编程[^16] |
| Tiling | 分块/切块（tiling 不译更常见，保留英文） | 数据切分与分块：先按核切分、核内再分块多次计算；参数 Host 侧算好后传设备[^28] |
| TilingKey | TilingKey | 区分核函数特例实现的键：不同 TilingKey 编译生成不同二进制（另见 tilingkey 模板编程博文）[^28] |
| ping-pong | 乒乓 | 双缓冲（Double Buffer）交替搬运/计算，以缓冲换并行[^17] |
| bank | bank | 存储内部独立可并行读写的子体（低位编址多 bank）[^16] |
| bank conflict | bank 冲突 | 多读写请求同时访问同一 bank 时被迫排队等待，引起性能下降[^16] |
| Address Space | 地址空间 | SIMT/SIMD 编程中的地址空间限定（如 `__gm__`）；SIMT 访问 GM 经 DCache 中转（3510 架构说明） |
| ND-DMA | ND-DMA | N 维数据搬运：3510 新增的 DataCopy 扩展，可配置维度与 Stride[^7] |

## 运行与调度

| 英文 | 中文 | 说明 / 出处 |
|---|---|---|
| runtime | 运行时（不译更常见） | CANN 的设备管理/任务调度库 |
| ACL / AscendCL | AscendCL | 华为昇腾计算语言接口层（runtime `src/acl` 实现，Host 编程入口） |
| ACLNN | ACLNN 算子接口 | 两段式调用接口（`aclnnXxxGetWorkspaceSize`→`aclnnXxx`，张量参数 `aclTensor`[^9]）；覆盖预置算子与自定义算子工程生成的单算子 API[^13] |
| aclnn | aclnn | aclnn 系列接口/函数前缀；张量参数为 `aclTensor`[^9] |
| Stream | Stream（流） | 任务执行序列：同一流内任务按序执行，提供创建/销毁/同步等接口[^4] |
| Task | 任务 | 一次可调度执行单元 |
| Event | 事件 | host 侧 Runtime 同步/计时原语；能力由创建 flag 决定（多 Stream 同步、时间戳、捕获进度等[^4]） |
| Notify | Notify（通知） | 流上记录/等待原语（aclrtNotify）；计数型变体 aclrtCntNotify\* 另族分立[^4] |
| SQE | SQE（Submission Queue Entry，任务描述符） | runtime 提交给设备执行的任务描述符；AIC/AIV 等核任务 SQE 结构按架构定义于 runtime 源码，经 task 构建链填充下发[^5] |
| TSD | TSD（不译） | runtime 服务子系统，管理设备侧子进程（aicpu 调度、queue_schedule 等的启停与事件，经 HDC 通道与 host 通信，详见[^6]） |
| queue_schedule | 队列调度 | runtime 设备侧队列调度服务（内部命名空间 `bqs`，含 ezcom client/server）[^6] |
| aicpu_sched | AICPU 调度 | AICPU 侧任务调度实现（`src/aicpu_sched`）[^6] |
| Host | Host（不译） | 与 Device 相连的服务器（x86/ARM 等），调用 Device 提供的计算能力[^28] |
| Device | Device（不译） | 承载昇腾计算的设备，与 Host 相对；跨设备数据访问需遵循相应互联与通信接口的约束[^28] |
| H2D / D2H / D2D | — | host↔device / device↔device 拷贝方向 |
| CMO | CMO（cache memory operation） | Device 侧 Cache 内存操作，含 PREFETCH/WRITEBACK/INVALID/FLUSH 等类型[^4]；各接口支持哪些类型以接口说明为准 |
| SQ / CQ | 提交队列 / 完成队列 | 设备侧任务环：Host 将 SQE 写入 SQ，设备完成回报 CQ |
| DFX | 维测组件 | runtime 维测功能组件族：性能采集（msprof）、精度 Dump（adump）、日志（log）、错误管理（error_manager）、跟踪（trace）[^10] |
| tprt | tprt（不译） | runtime 内任务提交传输层：SQ/CQ 资源管理与任务推送（`TprtSqCqCreate`/`TprtSqPushTask` 等[^5]） |

## 算子与编译

| 英文 | 中文 | 说明 |
|---|---|---|
| Ascend C | Ascend C（不译） | CANN 提供的算子开发语言（多层级 API） |
| Tpipe / Tque | — | Tpipe/Tque 框架编程 API：基于 Tensor 编程，由框架统一管理内存与同步[^27] |
| basic API | 基础 API | Ascend C 基础 API：基于 Tensor 的 C++ 完备编程，自主管理同步与内存（MakeTensor/LocalMemoryAllocator）[^27] |
| SIMD / SIMT API | 语言扩展层 | 语言扩展层：基于指针的 C 完备编程，SIMD 矢量/SIMT 并行两族[^27] |
| PyAsc | PyAsc | Ascend C Python 前端 |
| RegBase | RegBase | 寄存器编程模型：3510 起 AIV 由 MemBase 切至 RegBase，数据驻留寄存器计算[^7] |
| Launcher | 启动器 | 算子 host 侧入口 |
| Tiling 结构体 | tiling 结构体 | host 侧计算的切块参数 |
| AOT Compile | AOT（提前编译） | Ahead-of-Time：运行前完成编译产出可执行产物的编译方式；Ascend 场景下可将运行时参数常量化、按 Tiling 匹配预编译特化版本（循环展开/死代码消除等）[^24] |
| JIT / RTC | 运行时编译 | 运行时实时编译（RTC） |
| IR | IR（中间表示） | 表达计算流程的抽象数据结构（Ascend IR 为 AI 处理器专用中间表示）[^28] |
| GE | 图引擎 | 计算图编译调度引擎 |
| Graph / 图模式 | 图模式 | 以整图为单位的编译与调度执行；图捕获/重放为其常见实现之一 |
| aclGraph | aclGraph | CANN 图下发/捕获重放机制 |
| npugraph_ex | npugraph_ex | 以 `torch.compile` 为入口的 NPU 图后端；相关机制与适用条件见第 26 章 |
| SuperKernel | 超级核 | 核函数二进制融合：将多个已编译子核函数融合为单一超级核，以子函数调用方式整合，降低 Task 调度开销[^24] |
| Kernel Launch | 核启动 | 将核函数（Kernel）提交至硬件启动执行的过程[^28] |
| BLOCK_DIM | block dim | 核函数启动的逻辑 block 数；与物理核的映射取决于核类型和运行配置 |

## 通信与并行

| 英文 | 中文 | 说明 |
|---|---|---|
| HCCL | HCCL | Huawei Collective Communication Library：集合通信库（架构文档见 hcomm docs/zh/architecture）[^19] |
| HCOMM | HCOMM | HCCL 的通信基础库：通信域与通信资源管理（开源仓库名 hcomm）[^19] |
| HIXL | HIXL | 昇腾跨设备通信库：屏蔽芯片底层差异，支持 RDMA/HCCS 等多条链路的跨设备数据传输（含单边通信）[^20] |
| RDMA / RoCE | — | RDMA 为远程直接内存访问；RoCE 是在以太网上承载 RDMA 的协议族，本书所引通信栈包含 RoCE v2[^21] |
| HCCS | HCCS | 昇腾片间高速互联链路，hcomm/HIXL 支持的传输协议之一[^20][^21] |
| UBoE | UBoE（不译） | hixl 通信协议枚举之一（`roce/ub_ctp/uboe/ub_rtp`，以太网系）[^8] |
| MC2 | 通算融合 | 通信与计算融合算子：经原型注册 MC2 接口声明、HcclGroup 配置通信域；亦为通信服务名（HCCL/MC2）[^22] |
| MoE | 专家混合 | Mixture-of-Experts |
| AllReduce / AllGather / ReduceScatter | 全归约 / 全收集 / 归约散播（英文不译） | AllReduce：各 rank 对同一数据归约、结果各持一份（如梯度同步）；AllGather：各 rank 数据聚合后全员可见；ReduceScatter：先归约再按 rank 切分[^8] |
| P2P | 点对点 | 单边/双边点对点通信 |
| 单边通信 | 单边（one-sided） | 由主动侧发起远端读写，无需接收侧为每次传输提交匹配操作；资源准备、完成确认与数据使用仍需协调[^23] |
| supernode / superpod | 超节点/SuperPod | 大规模训练集群形态 |
| PD 分离 | PD 分离 | Prefill 与 Decode 分离部署的推理服务架构（见 xLLM 性能优化等实践文章[^23]，属部署模式转述） |
| KV Cache | KV 缓存 | 推理注意力的键值缓存；分布式场景经 HIXL 等做池化后跨节点传输（见实践文章[^23]） |
| D2D 直传 | D2D 直传 | device 到 device 直接传输 |

## 编译后端生态

| 英文 | 中文 | 说明 |
|---|---|---|
| PTO | PTO（Parallel Tile Operation） | CANN 定义的面向 tile 编程的虚拟 ISA：以标准 tile 指令桥接不同代际实现差异，含计算/搬运/通信扩展指令[^18] |
| PTO Virtual ISA | PTO 虚拟 ISA | 面向 tile 的指令体系，定义计算、搬运及通信操作，具体支持依架构与版本而异[^18] |
| PyPTO | PyPTO | PTO 生态的 Python 前端编程框架，以 Tensor/Tile/Block 多层图抽象组织编译；详见第 25 章 |
| MPMD | MPMD | 多程序多数据执行调度（PyPTO 调度模型） |
| Execution Graph / Tile Graph / Block Graph | 执行图/Tile 图/Block 图 | PyPTO 编译管线 Tensor Graph→Tile Graph→Block Graph→Execution Graph 的逐级中间表示 |
| Tile | Tile（分块） | PTO 编程的计算/数据分块层级：以 tile 指令描述计算与数据流[^18] |
| Block | Block | PyPTO 表达层级之一（Tile 之下的组织单元，见第 25 章编译管线） |
| TileLang | TileLang | 社区 tile 级编程语言，昇腾有适配优化实践（官方博客转述[^25]） |
| tilelang-ascend | tilelang-ascend | tilelang 的昇腾后端 |
| torch.compile | torch.compile（不译） | PyTorch 编译 API |
| torchair | torchair | torch 图模式对接 NPU 的组件；自定义算子经 TorchAir 入图（TorchNPU 文档章节[^26]） |
| autofuse | AutoFuse | CANN 自动融合组件：与 TorchInductor 等后端对接实现算子自动融合（官方实践博客[^25]；亦有 TensorFlow 场景实践） |
| vLLM / SGLang | — | 主流开源推理服务框架（官方实践文章语境[^25]） |
| Mooncake | Mooncake | KV 缓存池化/传输中间件（实践案例中与 HIXL 对接做 KV 传输[^23]） |

## 维测

| 英文 | 中文 | 说明 |
|---|---|---|
| msprof | msprof | 性能调优工具：采集分析 AI 任务各阶段关键性能指标含 msproftx 打点扩展接口[^4][^10] |
| adump | adump | 精度调试 Dump：单算子/模型逐层输入输出比对数据；异常时含 Workspace/Tiling接口见 Dump 配置[^4][^10] |
| msSanitizer | msSanitizer | AI 处理器异常检测工具：内存/竞争/未初始化/同步四子功能；当前仅支持 SIMD 场景调试[^14] |
| DumpTensor | DumpTensor | AscendC 设备侧张量打印/dump 接口；配 Dump 配置与 show_kernel_debug_data 离线解析[^11] |
| Simulator / npu_sim | 仿真器 | 仿真统称，按语境分指：pto-isa CPU Simulator（CPU 功能验证）与 CANN 构建仿真（`CMAKE_ASC_RUN_MODE=sim`），非同一物[^12] |
| Error Manager | 错误管理组件 | runtime 错误管理：错误码记录与上报（`src/dfx/error_manager`）[^10] |
| trace | trace（不译） | 跟踪：过程记录与打点（runtime `src/dfx/trace`）[^10] |

以下脚注为本表全部来源基线（快照见 management/SOURCE-BASELINE.md）：


[^1]: 架构规格带宽/通路表：`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/architecture_spec/npu_arch_2002.md`、`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/architecture_spec/npu_arch_2201.md`、`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/architecture_spec/npu_arch_3510.md`（各文件「不同数据通路的带宽」表）。
[^2]: 流水线总表（未标架构，仅索引）：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/c_pointer_programming/c_programming_overview.md`「PIPE_* 流水」节。
[^3]: Tensor/AIC/AIV 语义：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/cpp_tensor_programming/cpp_tensor_programming_overview.md`；SIMT 共享内存：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simt_programming/abstract_hardware_architecture.md`。
[^4]: Runtime 接口：`runtime/docs/zh/api_ref/06_stream_management.md`、`runtime/docs/zh/api_ref/07_event_management.md`、`runtime/docs/zh/api_ref/08_notify_management.md`、`runtime/docs/zh/api_ref/09_cntNotify_management.md`、`runtime/docs/zh/api_ref/11-06_CMO_memory_operation.md`、`runtime/docs/zh/api_ref/25-02_Enumerations.md`（L856-859 CMO 类型枚举）。
[^5]: SQE/任务链：`runtime/src/runtime/core/inc/sqe/v200_base/stars_david.hpp`、`runtime/src/runtime/core/inc/sqe/v200_base/aicpu_sqe.h`、`runtime/src/runtime/core/inc/sqe/arch5162/stars_sqe.hpp`；`runtime/src/runtime/inc/sqe/aic_aiv_sqe_common.hpp`；`runtime/src/runtime/core/src/task/task_info/davinci/davinci_kernel_task_v201.cc`、`runtime/src/runtime/core/src/task/task_info/davinci/davinci_kernel_task_v200_base.cc`；`runtime/src/tprt/inc/external/tprt_type.h`、`runtime/src/tprt/inc/external/tprt_api.h`。
[^6]: TSD/设备进程：`runtime/src/tsd/tsdclient/inc/tsd_process_controller.h`、`runtime/src/tsd/tsdclient/inc/tsd_event_interface.h`；`runtime/src/queue_schedule/common/bqs_util.h`；`runtime/src/aicpu_sched/`（子目录见仓）。
[^7]: 950 新特性：`asc-devkit/docs/zh/asc_950_feature_guide.md`。
[^8]: 通信：`hcomm/docs/zh/architecture/architecture-brief.md`；`hixl/docs/zh/api/cpp/HIXL-interface.md`。
[^9]: aclnn 两段式与张量类型：`asc-devkit/docs/zh/guide/programming_guide/appendix/common_operations/develop_dynamic_input_operator.md`（`aclnn...GetWorkspaceSize(const aclTensorList*, const aclTensor*, ...)` 签名）；`ops-transformer/posembedding/rope_with_sin_cos_cache/docs/aclnnRopeWithSinCosCache.md`（`const aclTensor*` 入参）；相关接口使用 `aclTensor`，不要写成 `aclnnTensor`。
[^10]: 维测组件：`runtime/README.md`「维测功能组件」节；`runtime/src/dfx/{msprof,adump,log,error_manager,trace}`；`runtime/docs/zh/api_ref/18_dump_configuration.md`、`runtime/docs/zh/api_ref/19-02_msproftx_extension_apis.md`。
[^11]: DumpTensor：`asc-devkit/docs/zh/guide/programming_guide/appendix/show_kernel_debug_data_tool.md`；接口 `asc-devkit/docs/zh/api/SIMD-API/basic_api/debug_interface/onboard_print/DumpTensor.md`。
[^12]: 仿真语境：`pto-isa/README_zh.md`「CPU Simulator 支持」；`asc-devkit/cmake/asc/asc_modules/CMakeASCInformation.cmake` L163-172（`CMAKE_ASC_RUN_MODE=npu/cpu/sim`）。

[^13]: 自定义算子 aclnn 工程：`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/aclnn_operator_development/aclnn_quick_start.md`（AddCustom 端到端生成单算子 API）。
[^14]: msSanitizer：`asc-devkit/docs/zh/guide/programming_guide/debug_and_tuning/functional_debug/npu_board_debug.md` L51-60（四子功能、仅 SIMD 场景）；`asc-devkit/docs/zh/guide/programming_guide/debug_and_tuning/overview.md` L38（内存检测定义）。
[^15]: 存储层级：`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/architecture_spec/npu_arch_2201.md` L30（L0A/L0B/L0C 语义）及各架构容量表；`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/basic_architecture.md` L113/L206（L2Cache 与 Cache Line 128/256/512B）。
[^16]: `asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/c_pointer_programming/c_programming_overview.md` L15/L119（3510 GM→UB→Register 三级与 Reg 编程）、L174（bank 并行与冲突排队）。
[^17]: 双缓冲定义：`asc-devkit/docs/zh/guide/technical_appendix/concepts_and_terms/glossary.md` L182（官方概念表）。
[^18]: PTO：`pto-isa/README_zh.md` L7（Parallel Tile Operation/虚拟 ISA 定位）、L23（90+ 条标准 tile 指令、非隐藏底层能力）、L42（统一 Tile ISA 抽象）、L30（通信扩展指令三类）。
[^19]: `hcomm/README.md` L9（HCOMM=HCCL 通信基础库，通信域/资源管理）；`hcomm/docs/zh/architecture/README.md` L3（HCCL 全称）。
[^20]: `hixl/README.md` L36（屏蔽芯片底层差异、RDMA/HCCS 多链路）。
[^21]: 协议表：`hcomm/docs/zh/architecture/architecture-brief.md` L27（UBC/UB_RTP/UBoE/RoCE(v2)/HCCS/UB_MEM）。
[^22]: MC2：`hcomm/include/hccl/hccl_comm.h` L260（regName：HCCL or MC2）；`asc-devkit/docs/zh/guide/operator_practice/simd_operator_impl/fusion_operator_programming/general_fusion/operator_impl.md` L208/L215（MC2 注册+HcclGroup）。
[^23]: 实践文章（转述级证据）：`cann-learning-hub/blogs/inference/hixl_rl_tail_latency_optimization/HIXL在RL推理中的长尾时延优化.md`（Mooncake 对接/HIXL 单边 KV 传输/PD 分离）；`cann-learning-hub/blogs/inference/xllm_inference_performance_optimization/xllm_inference_performance_optimization.md` L9（动态 PD 分离）。
[^24]: SuperKernel/AOT/npugraph_ex：`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/super_kernel/principles.md` L5（二进制融合定义）；`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/super_kernel/kernel_direct_call_adaptation.md` L6（仅 npugraph_ex 后端）；`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/aot_compilation_optimization.md` L3（AOT 常量化+Tiling 匹配特化版本）。
[^25]: `cann-learning-hub/blogs/inference/autofuse_torchinductor_deepseek_fusion/autofuse_torchinductor_deepseek_fusion.md` L3-5（AutoFuse×TorchInductor）；`cann-learning-hub/blogs/operator/tilelang_ascend_operator_optimization/tilelang_ascend_operator_optimization.md`（TileLang 实践）；vLLM 见 `cann-learning-hub/blogs/inference/hixl_nixl_ascend_backend/hixl_nixl_ascend_backend.md` 等语境。
[^26]: TorchAir：`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/ai_framework_adaptation/pytorch_framework.md` L7（TorchNPU「TorchAir>自定义算子入图」指引）。

[^27]: Ascend C 三类接口：`asc-devkit/docs/zh/asc_how_to_choose_api.md` L18-26（Tpipe/Tque 框架编程 API＝统一管理内存与同步；基础 API＝C++ Tensor 完备编程、自主管理同步/内存；语言扩展层＝指针 C 编程）。

[^28]: 官方概念/术语表：`asc-devkit/docs/zh/guide/technical_appendix/concepts_and_terms/glossary.md`（AI Core/Cube Core/Vector Core/Scalar/AIC/AIV/MTE1-3/GM/UB/Host/Device/Tiling/TilingKey/Kernel Launch/IR 等词条原文）。
