# CH26 证据集 —— 生态与接入层次：你的模型该从哪层进入昇腾

rev1（2026-10-10）。任务：`management/tasks/CH26-RESEARCH.md`。基线：`management/SOURCE-BASELINE.md`（本篇涉及的快照：cann-learning-hub `a3989658`、asc-devkit `28e7aba2`、pto-isa `dd3cb0fb`、pypto `883e7dfb`，均 2026-08-22 前后，dirty=0）。
证据三分类标签：【码】=本仓源码/文件已读；【文】=仓内一手文章/官方文档陈述；【外】=项目仓库不在本地，只有外链与转述——**不据名称推断其内部实现**。
主问题：**已有 PyTorch 模型或自定义算子，应从哪一层接入**。层次：①模型推理框架 ②图捕获/执行 ③编译后端（图编译/自动融合）④算子语言。

---

## A. 资料面盘点：什么在仓、什么只有外链

| # | 事实 | 类 | 证据 |
|---|------|----|------|
| A1 | learning-hub blogs 为本书可引的一手文章库，含推理/算子两类；各博客 README 表带月份标注 | 【码】 | `cann-learning-hub/README.md` L178-196（kernel 直调 2025.11、npugraph_ex 三篇 2025.12/2026.2、torchair FX 2025.12、SuperKernel 综述 2025.11、vLLM-Ascend 2025.11）；单篇最后提交日期（git 提交日期≠文章发布时间，仅作资料快照锚）：aot_superkernel/autofuse 2026-07-28、tilelang_ascend 2026-08-11、torchair FX 2026-03-23（`git log -1 --date=short` 实测） |
| A2 | **torchair / inductor_npu_ext / npugraph_ex / vllm-ascend / PyAsc / TileLang 源码均不在本地 10 仓** | 【外】 | 本地仓列表实测（仅 asc-devkit/cann-learning-hub/hcomm/hixl/ops-nn/ops-sparse/ops-transformer/pto-isa/pypto/runtime）；外链：torchair `gitcode.com/Ascend/torchair`（autofuse 博客 L95 含 `experimental/_inductor_npu_ext/README.md` 深链）、npugraph_ex 同址（npugraph_ex 博客 L38「开源了相关代码（https://gitcode.com/Ascend/torchair ）」）、PyAsc `gitcode.com/cann/pyasc`（asc-devkit CHANGELOG L107、`docs/zh/guide/getting_started/ascend_c_overview_and_learning_path.md` L21）、vLLM PR 4700/SGLang PR 13410（npugraph_ex 博客） |
| A3 | PyAsc 在仓内的全部信息只有定位句与建设状态 | 【文】 | asc-devkit 学习路径文 L21：「**Python前端PyAsc**：基于Python原生接口（参见 PyAsc），提供芯片底层完备编程能力，并将逐步引入Layout化Tensor编程、SIMT编程等」；learning-hub README L107「PyASC 算子开发系列｜🚧 建设中」——**除此之外无任何一手材料，正文不得描述其语法/能力细节** |
| A4 | PTO-AS 是 pto-isa 路线图项，汇编规范目录在仓 | 【码/文】 | `pto-isa/README_zh.md` L185（路线图「PTO-AS｜PTO ISA 的字节码（Byte Code）支持｜编译器/工具链｜持续演进」）；`pto-isa/docs/assembly/` 目录存在（规范文本在仓，未读内容——如引用须先读） |
| A5 | TileLang(-Ascend) 在仓内只有两篇实践博客 | 【文】 | `blogs/operator/tilelang_ascend_operator_optimization/tilelang_ascend_operator_optimization.md`、`blogs/operator/tilelang_xllm_qwen35_operator_adaptation/tilelang_xllm_qwen35_operator_adaptation.md`；源码外链未在本地 |

## B. 四层接入地图（每层：入口/证据/约束）

| 层 | 入口（读者视角） | 证据 | 关键约束 |
|---|------|------|------|
| ①模型推理框架 | vLLM 与 SGLang 各自社区有 npugraph_ex 接入代码合入（vLLM 走 vllm-ascend 仓库 PR 4700；SGLang 走 sgl 仓库 PR 13410——两个独立社区、各自 PR，博客原链接即此）——**集成存在≠默认启用**：博客只说「相关代码已经合入至对应社区」与「可以无缝集成」，未说任何一方默认启用 npugraph_ex 后端；两框架本就「提供了其默认的图模式后端」（未必是 npugraph_ex） | 【文】npugraph_ex 博客 §3 L93-96 原句；【文】`blogs/inference/vllm_ascend_inference_optimization`（仅证 vLLM-Ascend 适配存在） | 各框架默认后端归属属社区仓配置，本书无证据——正文写「已合入接入代码，是否默认启用须查各自仓库配置」（【外】） |
| ②图捕获/执行（手工） | `torch.npu.NPUGraph` 捕获/重放（aclGraph 的 torch 封装） | 【文】npugraph_ex 博客 §1 示例（static_* 命名系示例变量名，**不构成静态 shape 产品限制的证据**）；「aclGraph提供了图捕获及重放能力的C接口……在Pytorch层也封装了对等的接口（torch.npu.graph）」 | **shape 边界（据 §2.2 原文）**：捕获期「固化图相关的内存地址」——单次捕获内地址固定；`dynamic=True` 时「每次出现新的shape就会触发一次新的aclGraph的捕获」（同 FX 图多 capture 间内存复用，默认开）；`dynamic=False` 多 FX 图跨池复用默认关、须自证无踩踏。即：shape 变化=重新捕获，后端不拒绝动态 shape；**不得概括为「只支持静态 shape」** |
| ②′图编译（自动） | `torch.compile(model, backend=...)` 接 npugraph_ex/torchair | 【文】npugraph_ex 博客 §2「以torch.compile为入口……基于FX图的NPU优化组件」；第三方集成文 §2 三阶段：TorchDynamo→AOTAutograd→FX Compile（FX Pass/Tiling Update/Static Kernel/aclgraph capture 四步） | 需处理编译缓存/冷启动（第三方集成文主题） |
| ③编译后端（inductor 系） | `import inductor_npu_ext` 后照常 `@torch.compile` | 【文】autofuse 博客 L99-110 完整示例：`import torch; import torch_npu; import inductor_npu_ext; @torch.compile def test_add_sum(x,y): return torch.add(x,y).sum()`；「AutoFuse扩展了inductor在NPU上的Codegen后端，通过将InductorLoopIR转换为AscIR，调用AutoFuse……生成高效的Ascend C Kernel实现」 | 仅 NPU 后端扩展；源码【外】 |
| ④算子语言（手写） | Ascend C（本书 ch9-18）；TileLang-Ascend；PyPTO（ch25）；PyAsc（建设中）；Kernel 直调 | 【文】tilelang 博客（「TileLang-Ascend 是 TileLang 针对 Ascend NPU 的高性能算子开发框架」）；【码】pypto 见 ch24/25 证据；【文】kernel 直调博客（「基于Ascend C算子开发衍生……异构混合编程，简化编译部署」） | 语言间不可简单互换；成熟度差异见 §F |

## C. 路径一深追：torch.compile → torchair/npugraph_ex 的 FX Pass 注入（多流并行）

| # | 论断 | 类 | 证据（`blogs/inference/torchair_fx_pass_multi_stream/TorchAir自定义FX Pass.md`） |
|---|------|----|------|
| C1 | torchair 在 FX 图优化阶段有内置 pass，自定义 pass 可注册到内置前后两个位置 | 【文】 | 「若注册到**post_grad_custom_pre_pass**阶段……之前执行；若注册到**post_grad_custom_post_pass**阶段……之后执行」＋截图 torchair_optimize_stage.png（流程位置图，【文】图） |
| C2 | Pass 签名与可用能力 | 【文】 | 原文签名 `def your_pass_name(gm, example_inputs, config: torchair.CompilerConfig) -> None`（gm 为 AOT 后 GraphModule，example_inputs 为 FakeTensor）；能力清单：模式识别/增删改节点/**流控制**（`torch.ops.air.scope_enter.default`/`scope_exit.default` 包裹、`torchair.ops.record`/`wait` 建跨流同步）/通用规则变换 |
| C3 | 三步接入，不改模型代码 | 【文】 | 「1.编写FX Pass函数 2.通过torchair.CompilerConfig注册 3.编译时自动应用……原有模型脚本无需改动」；示例场景=多流并行从「手动打流标签」变声明式图变换 |
| C4 | 边界 | — | torchair 源码、pass 执行序的实现、与 inductor 关系：**本仓无源码**，只转述博客；博客亦未给 pass 内部实现截图以外细节——正文不猜 |

## D. 路径二深追：inductor_npu_ext → AutoFuse（IR 级自动融合）

| # | 论断 | 类 | 证据（`blogs/inference/autofuse_torchinductor_deepseek_fusion/autofuse_torchinductor_deepseek_fusion.md`，2026-07-28 快照） |
|---|------|----|------|
| D1 | 对接点=inductor 的 Codegen 后端；IR 链 InductorLoopIR→AscIR（AscGraph） | 【文】 | L89 原句（见 B 表）；L11「AutoFuse以AscIR图（AscGraph）作为输入。上层框架……先基于框架侧IR完成Lowering……若上层能够提供CANN中抽象层级更高的Ascend IR图，AutoFuse提供了相应的能力将其转换为AscGraph」 |
| D2 | 三阶段管线：Schedule→Auto Tiling→Codegen | 【文】 | Schedule：HintGraph→多 `ImplGraph` 候选，循环合并/生成 `TilingCase`/并行/内存复用/多模板；AutoTiling：约束符号化→耗时公式建模（映射 Ascend C API 流水图）→求解器；Codegen：每 ImplGraph 出模板函数，运行时 `TilingKey` 选模板；Host 侧 `tiling_func`+Kernel 侧代码 |
| D3 | 使用面=一个 import | 【文】 | L99-110 示例全文（B 表已引）；「在脚本开头导入 inductor_npu_ext 以启用 inductor NPU 后端扩展」 |
| D4 | 收益数字（文档陈述，非本书实测） | 【文】 | 「Atlas A3 单卡、DeepSeekV3.1-Terminus、batchsize=16：Eager 157.58 TPS → TorchInductor+AutoFuse 185.10 TPS（+17%）」——五要素中**测量口径/环境细节博客未给全——按 CH26-WRITE 第 5 条，此类数字正文直接省略，不入主线**（本行为证据存档） |
| D5 | 边界 | — | AutoFuse/inductor_npu_ext 源码不在本地；「Ascend C API 耗时公式库」内部未见于本仓——不展开 |

## E. 图执行底座与「为什么要图模式」（动机链）

| # | 论断 | 类 | 证据 |
|---|------|----|------|
| E1 | aclGraph 模型：Stream=Task 队列，Task 分 Kernel/Event（record/wait/reset），跨流依赖靠 Event | 【文】 | `blogs/inference/aot_superkernel_graph_execution/aot_superkernel_graph_execution.md`（2026-07-28）：「Task 是 Aclgraph 的基本调度单元……Kernel Task：入口、参数、Block 数、Kernel 类型；Event Task：record、wait、reset」＋「硬件调度器基于 Aclgraph 提供的 ModelRI 启动不同 Stream 的任务调度」 |
| E2 | 图模式动机=调度等待与启动开销；小 Kernel 多、跨流依赖频繁时恶化 | 【文】 | 同文：「每个 Task 被调度时都会产生调度间隙……推理场景小数据量计算时，硬件调度开销占比突出」 |
| E3 | AOT SuperKernel=执行前把可融合 Task 合并为单个 SuperKernel Task，保持图语义与 Kernel 逻辑不变；生成关注 Scope 边界/SubTask 编排/同步表达/运行入口 | 【文】 | 同文开头定义＋四要素列表；综述篇 `blogs/inference/superkernel_inference_acceleration`（2025.11，DeepSeekV3/R1 背景、「整网编译为大算子，性能再提升 10%-20%」——**博客宣传数字，五要素不全，只可带限定转述**） |
| E4 | npugraph_ex 四步 FX Compile：FX Pass→Tiling Update（如 FA tiling 随 prompt 长度刷新，capture 插 event wait/replay 插 record）→Static Kernel→aclgraph capture | 【文】 | 第三方集成文 §2；npugraph_ex 博客 §2.1 Host tiling 刷新两阶段细节；§2.2 内存复用两机制（**dynamic=True：同 FX 图多次捕获间，默认开**；**dynamic=False：跨 FX 图池复用，默认关须自证无踩踏**；捕获期固化地址=单次捕获内固定，新 shape 触发重新捕获）；§2.4 静态化编译收益原理；§2.5 多流 Event 规则（「加入捕获状态的 Stream 最终需 Record 回主流」） |

## F. 算子语言层横览（定位对照，不排名、不重讲前章；「Kernel 直调」是**调用方式**非语言，见 F 尾注）

| 语言/方式 | 本仓证据 | 定位一句 | 证据边界 |
|------|------|------|------|
| Ascend C | 本书 ch9-18 全链 | C++ 模板 DSL | asc-devkit 学习路径文【码】；不做横向排名 |
| TileLang-Ascend | 【文】tilelang 博客两篇 | python 数学式 DSL；方法论「先单核（C/V 核内）后核间」；案例 FA/SFA 优化与 xLLM×Qwen3.5 GDN 算子适配（C++ Wrapper→Specialization→Kernel 查找） | 博客 2026-08；源码【外】 |
| PyPTO | 【码】ch24/25 已证 | Python DSL→PTO 虚拟指令，本章只回指定位 | pypto 仓在本地，0.2.0 前端 |
| PyAsc | 【文】A3 两句 | Python 原生底层编程，规划 Layout/SIMT | 官方学习路径提及；hub「PyASC 算子开发系列🚧建设中」是**教程栏目建设状态，非产品可用性结论**；无仓无例 |
| PTO-AS | 【码】目录在仓 | PTO 字节码/汇编（路线图「持续演进」） | docs/assembly 在仓未读 |


## G. 图表连接证据（正文两图每条箭头的出处）

| 箭头 | 证据 |
|------|------|
| torch.compile→TorchDynamo→AOTAutograd→FX Compile | 第三方集成文 §2 文字+torch_compile_stage.jpeg【文】 |
| FX Compile 内四步（Pass/Tiling/StaticKernel/aclgraph capture） | 同文 fx_compile_stage.jpeg＋文字【文】 |
| FX Pass 两注入点（pre/post） | torchair 博客 torchair_optimize_stage.png＋文字 C1【文】 |
| InductorLoopIR→AscIR→AutoFuse(Schedule/AutoTiling)→Ascend C | autofuse 博客 torchinductor_autofuse_integration.png＋L89/L11【文】 |
| aclGraph：Stream 队列+Event 跨流 | aot 博文 aclgraph_stream_task_scheduling.png＋E1 文字【文】 |
| npugraph_ex 三层优化（Common/融合 pass/NPU 高阶） | npugraphex_architecture.png＋§2 分层文字【文】 |
| vLLM/SGLang←npugraph_ex | §3 PR 链接【外】 |

**禁画**：不得画「所有语言/后端汇入同一 PTO 后端」——PyAsc/TileLang 的后端实现无本地证据；PyPTO→PTO 链仅限 ch24/25 已证部分。

## H. 复现可行性（本轮实测）

| # | 事实 |
|---|------|
| H1 | 已做：只读核对 learning-hub `git status` 干净、HEAD `a3989658`；blogs 全为 md+图片，无可在本机执行的代码工程（示例片段依赖 torch_npu/torchair/inductor_npu_ext——本机无 CANN/torch_npu，**未运行**） |
| H2 | 结论：本章复现节只给「读者环境自查清单」（torch/torch_npu/torchair/inductor_npu_ext 版本与 `torch.compile` 后端注册冒烟），明标本机未跑；不造假运行输出 |

## I. 写作纪律映射

不写生态名词清单——每节回答一个「读者此刻在哪/能做什么」；PyAsc/TileLang/PTO-AS 只写 A3/A4/A5/E 快照可证内容+来源日期；性能数字全部带「博客自述/五要素缺口」限定；PyPTO/PTO 一句回指；两图箭头均有 G 表证据；提纲短段场景化、不堆版本号。

**F 尾注（调用方式，非语言）**：Kernel 直调（【文】`blogs/operator/kernel_direct_call_programming`，2025.11，「基于Ascend C算子开发衍生……异构混合编程，简化编译部署」）描述的是**绕过框架 op 下发、直接调用 kernel 的使用方式**，可叠加于任意语言写的 kernel——不入语言对照表。
