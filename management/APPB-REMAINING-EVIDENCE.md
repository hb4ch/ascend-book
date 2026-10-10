# APPB-REMAINING-EVIDENCE —— 基础内存与生态/通信批（R4）

2026-10-10。任务：management/tasks/APPB-REMAINING.md。基线 SOURCE-BASELINE（各仓快照 08-21~23 逐仓）。**区分：源码/官方文档实证 vs 官方博客转述**，后者逐条标注。未找到/未核不记已核。

## 0. 经理纠错回执（三处）

1. **CMO 接口族泛化**：`aclrtCmoAsync`「仅支持 PREFETCH」是 L55 该接口参数节，**不能推广接口族**——`11-06_CMO_memory_operation.md` L71-110 `aclrtCmoAsyncWithBarrier` 参数节明载 cmoType=INVALID 时 barrierId 有效配 `aclrtCmoWaitBarrier`。术语改「类型支持依具体接口」并双例。
2. **ACLNN「预置」唯一限定**：`aclnn_operator_development/aclnn_quick_start.md`——自定义算子工程（AddCustom）编译部署后生成单算子 aclnn API。词条改「预置+自定义」双覆盖。
3. **Event flag 罗列**：表内收敛为「能力由创建 flag 决定」，细节留脚注[^4]（07_event L156/L257）。

## 1. ms_sanitizer→msSanitizer（更名+实证）

`asc-devkit/docs/zh/guide/programming_guide/debug_and_tuning/functional_debug/npu_board_debug.md` L51-60：**异常检测工具，内存/竞争/未初始化/同步四子功能；当前仅支持 SIMD 编程场景调试**；`debug_and_tuning/overview.md` L38（Global/Local Memory 越界与未对齐检测）。官方用户指南外链 gitcode Ascend/mssanitizer。**runtime 仓 dfx 无此目录**——工具属 devkit 调试族，非 runtime 组件；词条更名并改写。「待批」字样移出读者表。

## 2. 基础内存批

| 术语 | 证据 | 处理 |
|---|---|---|
| L1 Buffer | npu_arch_2201 L46（512KB）+MTE1 供给链（带宽表） | 「Cube 侧缓冲：经 MTE1 向 L0A/L0B 供给」 |
| L0A/L0B/L0C | npu_arch_2201 **L30**（L0A 左矩阵/L0B 右矩阵/L0C 结果与中间） | 按原文改 |
| L2 | basic_architecture L113/L206（缓存 GM 访问含代码段；Cache Line 128/256/512B 随规格） | 去「带 Cache 一致性域」无据句 |
| Register | c_programming_overview L15/L119（3510 GM→UB→Register 三级、Reg 编程） | 原「MTE/Vector 寄存器文件」泛称改具体 |
| bank/bank conflict | 同文 L174（低位编址多 bank 独立读写；同 bank 并发排队→冲突降性能） | 按原文改 |
| ping-pong/Double Buffer | asc-devkit `concepts_and_terms/glossary.md` L182（双缓冲官方定义：多缓冲区提并行） | ping-pong 条挂[^17]关联，不另立条 |

## 3. PTO 族

- `pto-isa/README_zh.md` **L7**：PTO（**Parallel Tile Operation**）=面向 tile 编程的虚拟 ISA——全称首次实证，词条更正。
- **L23**：90+ 条标准 tile 指令；「目标不是隐藏底层能力，而是提升抽象层级保留调优空间」——**旧「屏蔽 A2/A3/A5 差异」绝对句废止**，改「桥接代际差异/非屏蔽底层」。
- L42 统一 Tile ISA 抽象；L30 通信扩展指令（点对点/信号同步/集合通信三类）→Tile 条与 PTO 条。

## 4. 生态通信批

| 术语 | 证据（源码/文档） | 处理 |
|---|---|---|
| HCCL | `hcomm/docs/zh/architecture/README.md` L3 全称 Huawei Collective Communication Library | 保留+架构文档锚 |
| HCOMM | `hcomm/README.md` L9「HCCL 的通信基础库，通信域与通信资源管理」 | 按原文改 |
| HIXL | `hixl/README.md` L36/L50（屏蔽芯片差异；RDMA/HCCS 多链路；HCCS 119GB/s） | 补多链路定语 |
| RDMA/RoCE/HCCS/UBoE | `hcomm/docs/zh/architecture/architecture-brief.md` **L27 协议表**（UBC/UB_RTP/UBoE/RoCE(v2)/HCCS/UB_MEM） | RDMA 条补协议族；HCCS 补 119GB/s |
| MC2 | `hcomm/include/hccl/hccl_comm.h` L260（regName：HCCL or MC2）+`operator_impl.md` L208/215（MC2 注册+HcclGroup） | 双证：通信服务名+通算融合注册 |
| 单边通信/PD 分离/KV Cache/Mooncake | `cann-learning-hub/blogs/inference/hixl_rl_tail_latency_optimization/...md`（**转述**：HIXL 单边 KV 传输/Mooncake 对接/PD 分离部署）；`xllm_...md` L9（动态 PD 分离） | 词条挂「实践文章转述」标注 |
| AOT Compile | `aot_compilation_optimization.md` L3（运行时参数常量化+Tiling 匹配特化版本） | 按定义改 |
| SuperKernel（原 AOT Superkernel） | `super_kernel/principles.md` L5（**二进制融合**：多子核融合为超级核、子函数调用整合、降 Task 调度开销）；`kernel_direct_call_adaptation.md` L6 | 词条更名 SuperKernel；「AOT Superkernel」书内旧名废止 |
| npugraph_ex | 同上 L6（核函数直调**仅 npugraph_ex 后端，不支持 GE 图模式**）；`operator_self_verification.md` L5（两种开启方式） | 按原文改 |
| torchair | `ai_framework_adaptation/pytorch_framework.md` L7（TorchNPU「TorchAir>自定义算子入图」） | 补入图语义 |
| autofuse | `cann-learning-hub/blogs/inference/autofuse_torchinductor_deepseek_fusion/...md` L3-5（**转述**：CANN AutoFuse×TorchInductor 自动融合；DeepSeek 17%） | 标转述；TensorFlow 场景另有 blog |
| TileLang/tilelang-ascend | `cann-learning-hub/blogs/operator/tilelang_ascend_operator_optimization/...md`（**转述**） | 标转述 |
| vLLM/SGLang | 同上博客群语境提及（**转述**） | 「仅语境提及，不展开」 |

## 5. 统计

- 本批**已核改写 32 条**（含纠错 3）：CMO/ACLNN/Event/msSanitizer/L1/L0A-C/L2/Register/bank/bank conflict/ping-pong/PTO/PTO Virtual ISA/Tile/HCCL/HCOMM/HIXL/RDMA-RoCE/HCCS/MC2/单边/PD/KV Cache/AOT Compile/SuperKernel(更名)/npugraph_ex/torchair/autofuse/TileLang/vLLM-SGLang/Mooncake/tilelang-ascend 未动（社区后端名，仅注）。
- **转述级**：PD/KV/Mooncake/单边(部分)/autofuse/TileLang/vLLM——已标注，不冒充源码实证。
- **范围外未核**（台账 R4 附记）：ACLNN runtime 内实现、ACL 子模块实现、HCCL 算子族、UBoE 细节、supernode/EPD 等生态专有条。
- 台账 `APPB-AUDIT.md` R4 行已刷；glossary 脚注扩至 [^1]–[^26] 全文件级路径。
