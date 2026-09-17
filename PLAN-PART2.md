# 第二编成稿方案（PLAN – Part 2）

> 适用范围：**M1-扩展（选 B，三章补齐 7–8k）+ M2（第4–8章）**。本计划与 `/mnt/SATASSDEXT4/cann` 源码逐一对应，写前先读计划；成稿流程仍为 plan → write → review 三轮。
> 状态：**计划草案（M1 决策已定 = B）**，待评审。下面每条「源码抓手」都已在本地核对存在。

---

## 0. 现状快照（2026-08 基线，`npm run verify` 全绿）

| 范围 | 字量 | 状态 |
|---|---|---|
| 第一编 第1–3章 | 总 11.2k / 中文 9.5k（三章 4.2k / 3.9k / 2.9k） | ✅ 已完成三轮重写，**达标存疑（评审门 M1' 待判）** |
| 第二编 第4–8章 | 5 章全成稿（4.5k/4.2k/2.7k/2.7k/3.5k 总字 = 17.6k总/14.1k中文） | ✅ 已成稿（M2），verify 绿 |
| 第三~七编 第9–24章 | 每章仅 0.25~0.35k 骨架 | ⬜ 未开始 |
| 附录 A–E | 4.1k（A 环境 /B 术语 /C 资源 /D 源映射 /E 风格） | ✅ 已建，随书维护 |
| 校验 | build / internal / source / terms / word-count 全绿 | ✅ 工具链闭环 |

**上一阶段的缺口（写进本计划的动机）**：

1. 三章字数 2.9–4.2k，距 8k 目标差一半——CHANGELOG 已注明是「增量深挖而非缺件」，等待评审定夺是否需要拉长。
2. 全书 24 章目前只成稿了前 3 章，**写作瓶颈在产品化质量之外，更在「素材→叙事」的拆解速度**。第二编素材（runtime 仓）量最大、最杂、最易写成源码逐行翻译，需要先定叙事骨架再动笔。

---

## 1. M1 决策已定：选 **B——三章补齐 8k**（先深挖总览编，再进 M2）

选 B 意味着把第一编三章从 3.6k/3.3k/2.4k 中文拉到 ≥7k（目标 7–8k，仍服从「质量优先、不灌水」）。工作量约 +10~12k 中文，等于再写两章半——**所以扩展必须全部是「真材实料的增量」，不允许水**。

### 1.1 扩展的总纪律（防止「回填水」）

1. **不抢第二编的饭碗**：PLAN-PART1 迁走的深度内容（错误码体系→ch4、MTE 路径详表→ch8/11、BQS 三类事件→ch5、URMA/UDMA→ch18 等）**不回填**。只补充「总览级证据」：真码三拍子、能力菜单总览、图模式上手片段——这些本来就应该在第一编给完的直观素材。
2. **每加一个小节，必须对应一个可核对的源码文件**（下表逐项给路径），成稿时进章末脚注。
3. 新增代码一律遵循「代码四句法 + 运行性分级」；能拿到的真码尽量标 `[需真机验证]`（add.asc 这类带 CPU-SIM 可能性的留到第8/10章）。

### 1.2 第1章扩展清单（3.57k → ≥7k，约 +3.5k）

| 位置 | 新增内容 | 源码抓手（已核对存在） | 估字 | 性质 |
|---|---|---|---|---|
| 1.2 | 七层剖面配一张「每层门牌」表：一层一行真实路径暗示该层都能到哪挖，让剖面从图变成可查档案 | `runtime/include/external/acl/acl_rt.h`、`runtime/src/runtime/api/`、`runtime/src/queue_schedule/server/`、`runtime/src/tsd/tsdclient/`、`asc-devkit/impl/basic_api/` | +600 | 广度，深挖留给 4–6 章 |
| 1.3.1 新增 | **两个 Hello 对照**：`aclnn` 两段式 vs 自定义 kernel launch 的形态差异（`<<<numBlocks,0,stream>>>` 一行 vs 两段式），只讲“形状”，细讲留给第4章 | `runtime/example/0_quickstart/4_custom_kernel_launch/{main.cpp,vector_add_kernel.cpp}`（151 行） | +900 | Put `[需真机验证]` |
| 1.4 | 厨房比喻落真码：引入 add.asc 的 CopyIn/Compute/CopyOut 一排代码，让「三拍子」第一次见真码 | `asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/add/add.asc` | +700 | `[需真机验证]`；CopyOut 已在 |
| 1.6 新增 | **一页总图**：纵向剖面 + AI Core 厨房缝成一张「全景拼图」，配全书导航总表（名词→章），作为开篇的回忆锚点 | 复用 1.2/1.4 的 mermaid，不引新源 | +500 | 一章一图增强 |
| 1.5.1 | FAQ「三连」→「四连」（补：“为什么先问尺寸”？→ 用两段式动机收口） | 复用 `^hello` | +300 | |

### 1.3 第2章扩展清单（3.3k → ≥7k，约 +3.7k）

| 位置 | 新增内容 | 源码抓手（已核对存在） | 估字 | 性质 |
|---|---|---|---|---|
| 2.1.1 | 「搬运字节数怎么数」最小方法论：一个算子的流量 = 各层 ELT×次数，教读者自己估（不只是我给的结论） | 复用 `basic_architecture.md`、`nddma_introduction` 口径 | +600 | 方法论，真数字留给第15章实测 |
| 2.2 | 三拍子读法实战：从「翻译腔」升级为 add.asc 真码—— CopyIn→`PipeBarrier`→`Add`→`PipeBarrier`→CopyOut，逐行配“这在干嘛” | `asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/add/add.asc` | +800 | `[需真机验证]`；衔接 1.6 |
| 2.3.4 | L1 中转的**手算复用例子**：直接 GM→L0 要搬 N 趟 vs 过 L1 复用省多少趟，把“为什么必须过 L1”算给读者看 | `basic_architecture.md`（L0/L1 口径）、`cann-learning-hub/blogs/operator/nddma_introduction/` | +700 | 手算直觉 |
| 2.4 | 补「同步的代价」：每次 barrier 都是一排气泡，为什么同步不能到处插（为 16 章双缓冲埋伏笔） | 复用 `memory_vector_computation.md`、`regbase_vec_add` | +400 | |
| 2.5.2 | 能力菜单从 5 行表升级为 **asc_950_feature_guide 13 项全表摘编**，选 RegBase/ND-DMA/SIMT/MX/UB互连/SSBuffer/Mutex 7 项各一行「一句话+去往章」 | `asc-devkit/docs/zh/asc_950_feature_guide.md`（13 项总览真实存在） | +900 | 广度，深度留给 11/16/18 |
| 2.6.1 | FAQ「二连」→「三连」（补：三拍子读法对矩阵算子也适用吗） | 复用 | +300 | |

### 1.4 第3章扩展清单（2.44k → ≥7k，约 +4.6k，增量最大）

| 位置 | 新增内容 | 源码抓手（已核对存在） | 估字 | 性质 |
|---|---|---|---|---|
| 3.1 | eager 四阶段的「下单调料」落地为表：找菜谱/取食材/递单/登记 → 各对应真实源码目录 + 一行说明；时间戳宏是什么、msprof 为什么看得到四段 | `runtime/src/runtime/core/src/launch/`（aix_stars.cc 等）、`runtime/src/runtime/core/src/kernel/`、`runtime/src/runtime/core/src/stream/stream_c.cc` | +800 | 与第15章点到为止 |
| 3.2 | SQE 字段级拆解：用 `task_to_sqe.cc` 讲清一张订单的机器形态（任务类型、cmd、blockDim 落哪、静态/动态），配「任务类型形态表」 | `runtime/src/runtime/core/src/task/task_to_sqe.cc`、`core/inc/task/*.hpp` | +900 | 深挖留给第5章，这里给“长什么样” |
| 3.3 | BQS 状态机（Full/NotFull/Range 事件在 `fsm//queue_manager` 真存在）+ TSD 客户端「进程/线程模式」一句话图 | `runtime/src/queue_schedule/server/{queue_manager.h,fsm/,state_manager.cpp}`、`runtime/src/tsd/tsdclient/` | +700 | 状态机完整翻版留第5章 |
| 3.4 | 新增「图模式上手代码」：`torch.npu.NPUGraph()` + `g.replay()` 两段真码 `[需真机验证]`；「该不该用」扩成决策表 | `cann-learning-hub/blogs/inference/npugraph_ex_aclgraph_graph_mode/` | +700 | 承接第22章 |
| 3.5 | 三笔账做一个**量级估算实例**（elemwise 4096²）每笔账怎么估、谁主导，标注为本书分析框架 | 复用 2.1.1 口径 + `launch/` 时间戳来源 | +800 | 方法论，不编厂商数字 |
| 3.6 | 源码线索表扩充一列「形态/状态」（区分 runtime 的 api/core/队列三层入口） | 复用上文路径 | +400 | |
| FAQ 新增 | 「常见疑问三连」小节（你会在第几章看见哪一层？FAQ 收口） | 复用 | +300 | |

### 1.5 收口动作（照旧）

1. 三章每轮 proofread + `npm run verify` 全绿后再进下一章；
2. 新增所有脚注与源码映射同步进附录D；`grep '📄\|📦'`（正文）为空；
3. CHANGELOG 记录「M1 选 B：三章补齐至 ~7–8k」的决策与差值说明；README 里程碑表 M1 转 ✅（编内字数口径仍写「总览编 7–8k 为编内自定」，不宣称强制）。

---

## 2. M2 总原则（在第一编六则之上新增三条）

第一编六则照旧：叙事优先 / 行内引用清零 / 代码瘦身 / 一动一套模型 / 先动机后机制 / 一章一图。

M2 专属新增：

1. **证据密度服务叙事，不追源码行数**。选每一节里"最能代表机制"的 ≤25 行关键代码讲透，其余只给路径（扔进章末脚注清单）。第二编源码都在 `runtime/src/...`，诱惑是把 `runtime/core` 逐文件翻；纪律是每章只挑 3–5 个锚点文件。
2. **API 层讲"怎么用顺手"，实现层讲"为什么这么设计"**。第4章是 API 使用编（对着 `acl_rt.h` 与 example 讲用法）；第5章才进实现（对着 `core/src` 讲机制）；第6章讲边界（驱动只讲用户态可观测）。
3. **运行性分级必须严**：`runtime/example` 与 ACL 程序均依赖真机 NPU，一律标 `[需真机验证]`，并在正文给出「无 NPU 时如何收窄验证」（用 `asc-devkit` 的 cmodel/CPU-SIM 能力、`runtime/src/cmodel_driver/` 作为旁证）；严禁把「看起来能跑」标注为「可运行」。

---

## 3. 五章详细方案

每章固定四件事：**一句心智模型（That's the take-away）→ 章节骨架 → 源码抓手（已核实在 /mnt/SATASSDEXT4/cann）→ 收尾与验收**。沿用第一编的「人话入手 + 术语后置」笔法。

---

### 第4章 ACL 编程接口（第二编开篇，材料最齐、最先写）

**心智模型一句**：ACL 是昇腾的「前台接待」——你所有的不 NPU 交流（初始化、选卡、开流、分配内存、下单算子）都透过它，而且它全是异步的，你要学会「说完就等回执」。

**承接**：第1章 1.2/1.3 已给出七层剖面与 `aclnn` 第一个 C 程序；第4章把 1.3 的 15 行扩成完整程序逐步剖析，并补上第1章迁走的「ACL 接口地图、错误码体系」，第3章迁走的「错误码 107000/145000 详述」。

**章节骨架**（沿用 STYLEGUIDE 四段式）：

1. 初始化与会话：`aclInit/aclFinalize`，`ACL_ERROR_*` 宏族——为什么"先建会话"（资源账本模型）
2. 设备/上下文/流/事件四件套：`aclrtSetDevice`、上下文与流的关系、事件 Event→notify→（`cntNotify`，950 新增）——用「餐桌/手机」类比点到为止
3. 内存管理：`aclrtMalloc/Memcpy/set` 与 `aclrtMallocHost`、虚拟/物理内存、`ACL_MEM_MALLOC_HUGE_FIRST` 的选择逻辑——**这是全书第一个"钱"的话题，多花一节**
4. 三种 Launch：`aclnn` 算子两层式 vs Ascend C kernel（`aclrtLaunchKernel`，V3 系）vs 旧 `rtKernelLaunch`——给「ACL 年代简表」
5. 异步执行与同步原语：stream 顺序、`aclrtSynchronizeStream/Device`、事件同步、`aclrtLaunchCallback`——还第一编异步的债
6. 错误码体系与错误处理：`rt_error_codes.h` 分段读法、`aclGetRecentErrMsg`、`1_error_handling` 示例
7. 完整程序逐步剖析：`0_quickstart/0_hello_cann/main.cpp`（229 行）按「初始化→建卡开流→分配内存→下单 Add→取回结果→销毁」剖开

**源码抓手（已核对存在）**：

- `runtime/include/external/acl/acl_rt.h`（5,973 行，V2/V3 接口、`aclrtLaunchKernel` 与 950 事件族标记）、`acl.h`、`acl_op.h`、`error_codes/rt_error_codes.h`
- `runtime/example/0_quickstart/{0_hello_cann,1_error_handling,4_custom_kernel_launch}`（main.cpp / run.sh / CMakeLists）
- `runtime/example/1_basic_features/{context,device,stream,event,memory}/*`
- `runtime/docs/zh/api_ref/{02_initialization_and_deinitialization,04_device_management,05_context_management,06_stream_management,07_event_management,11-*_memory,12_execution_control,13_exception_handling,14_Kernel_loading_and_execution,21_snapshot_management,22_error_reporting_APIs}.md`
- `asc-devkit/docs/zh/guide/programming_guide/advanced_programming/aclnn_operator_development`（aclnn 两层式背景）

**一个必须写进章末脚注的实情（勘误级）**：`0_hello_cann/main.cpp` 包含的 `aclnnop/aclnn_add.h` 并不在开源树里（属安装包生成头），正文按「示意/需真机」标注，别让读者去找一个不存在的头文件——这是第二编写作中第一个"源码缺头"案例，正好训练"带批判地看厂方示例"。

**验收**：`grep '📄\|📦'`（正文）为空；≥2 张 Mermaid（完整程序状态图、内存决策图）；word:count ≥5k 中文（编首章达标线可略低，体现"质量优先"）；`npm run verify` 绿；appD/glossary/CHANGELOG 同步更新。

---

### 第5章 运行时核心实现（最难的一章，不要逐文件翻译）

**心智模型一句**：runtime 是「厨房的中枢调度室」——API 只是前台点单，真正把单子做成"机器能读的 SQE"、塞进队列、交给设备并回收结果的，是 `runtime/core` 里的 stream→task→SQE→device 四条水管。

**承接**：第3章把「流=取菜带、任务=订单、SQE=订单的机器可读版」讲成了形态；第5章还第3章的债，把第3章迁走的「BQS 三类事件、TSD 客户端文件细节、task_to_sqe」落地成实现。第4章讲"怎么调用"，本章讲"调用后内部发生了什么"。

**章节骨架**：

1. 一张总装图画清 runtime 模块桌（api → core/{stream,task,launch,kernel,device} → tsd/queue_schedule → 驱动）
2. 流的实现：`stream_factory.cc` / `coprocessor_stream.cc`——流为什么是"任务的有序容器"，`ACL_STREAM_PERSISTENT` 等 flag 落到哪
3. 任务与 SQE：`task.h` / `task_to_sqe.cc` ——**本章锚点文件**：一条命令/一条搬运/一条内核启动分别怎么编码成 SQE；`task_submit/` 管谁提交
4. 内核加载：`kernel/binary_loader.cc`、`module.cc`、`program.cc`——.o/ELF 怎么被解析、二进制怎么进设备
5. 设备侧执行：`device/ctrl_sq.cc`、`device_msg_handler.cc`——SQ/CQ 环、设备回执（与第3章 BQS 呼应）；`tsd/tsdclient/` 客户端怎么完成"最后一段"
6. 队列与调度：`queue_schedule/{client,server,common,proto}`——用户态到 TSD 的队列协议（结合第3章外卖柜比喻）
7. 一张「API→SQE→设备→回执」时序图收尾

**源码抓手（已核对存在）**：

- `runtime/src/runtime/core/src/{stream/stream_factory.cc,stream/coprocessor_stream.cc, task/task_to_sqe.cc, task/task_submit/, launch/label.cc, launch/memcpy_stars.cc, kernel/{binary_loader.cc,module.cc,program.cc}, device/{ctrl_sq.cc,device_msg_handler.cc,device.cc}}`
- `runtime/src/runtime/core/inc/{stream,task,launch,kernel,device}/*.hpp`
- `runtime/src/runtime/api/api_c_stream.cc / api_c_memory.cc / api_c_kernel.cc`（入口层怎么转 core 内部）
- `runtime/src/tsd/tsdclient/...`、`runtime/src/queue_schedule/{client,server,common,proto}/...`
- `runtime/docs/zh/design/modules/{stream,task,event,kernel,memory,device}/*.md` + `design/architecture.md`

**控制篇幅的纪律**：`task_to_sqe` 系列真实实现很大；本轮只做「形态级」拆解（一段内核启动 SQE 的结构 + 一条 memcpy 的结构 + 放行到 submit 的路径），不做指令级全枚举。对读者价值最高的三问固定为：① 一次 Add 在 runtime 流过哪几个对象；② SQE 长什么样、谁来写、谁来读；③ 设备做完怎么回执。

**验收**：正文脚注化、`grep '📄|📦'` 为空；本章只解读 ≤5 个锚点文件、其余进脚注清单；时序图>2 张；`npm run verify` 绿；CHANGELOG 记录「本轮没有真机验证，所有时序结论标注为按源码推演 + 需 msprobe 实证的前置说明」。

---

### 第6章 驱动与系统软件协同（边界最受限的章，提前圈范围）

**心智模型一句**：驱动是「游客和本地向导」——你（用户态）永远只握着一个"翻译官"句柄，真正的指令走的是翻译官跟内核/设备的私有通道，而那条通道在开源仓库里是看不见的，只能看得到它的「护照面」。

**承接**：第3章 3.3「从队列到芯片」最后一段；第5章 device 侧把请求交给驱动。本章只回答三个问题：① 驱动在哪一层、什么时候被用到；② 用户态可观测的"护照面"有哪些（队列、DMA、内存注册、上下文）；③ 内核侧为什么不在仓库、怎么在书里诚实地写。

**章节骨架**：

1. 分层再剖：runtime 用户态驱动（`runtime/src/runtime/driver/`）与内核驱动的边界、`cmodel_driver` 的定位
2. 用户态可观测能力：`npu_driver_queue.cc`（队列），`npu_driver_mem.cc`（内存注册），`npu_driver_res.cc`（资源），`npu_driver_base.hpp`（基础句柄）——每个只给「一句动机 + 一个关键数据结构 + 一条 ioctl/队列路径」
3. 内核边界概念（无源码，明示资料性质）：页表/DMA/中断/隔离，统称"不可观测区"，给出官方资料的路径
4. 用一个可运行的旁证替代真机：`runtime/src/cmodel_driver/`（CPU 模型驱动）能演示"驱动动作的日志级行为"——这是第二编唯一能标 CPU 侧可跑的驱动相关材料
5. 诚实性规则落地：一个「哪些能写、哪些只能推断」的对照表

**源码抓手（已核对存在）**：

- `runtime/src/runtime/driver/{npu_driver.cc,npu_driver_queue.cc,npu_driver_mem.cc,npu_driver_res.cc,npu_driver_base.hpp,npu_driver.hpp}`
- `runtime/src/cmodel_driver/...`
- `runtime/docs/zh/design/...`（驱动相关段落）、`runtime/docs/zh/dev_guide/...`
- 内核侧明文标注：**不在开源仓**，正文用「概念描述 + 官方资料链接」写，不做编译级断言

**验收**：本章每一条"内核行为"论断都带「源码不可见/以官方资料为准」前缀；能跑的部分只有 cmodel 日志演示；脚注聚合清单里区分「仓内源码 / 仓外资料」两类，避免读者误以为内核驱动在仓里。**这是全书"争议与边界"（STYLEGUIDE §8）的样板章。**

---

### 第7章 维测子系统 DFX（四个工具箱讲成一套"报告单系统"）

**心智模型一句**：DFX 是给你看清"看不见的执行"的体检报告——日志（病历）、错误码（诊断书）、数据 Dump（切片）、Profiling（心电图），四张单子合起来定位一个 bug/性能问题。

**承接**：第4章错误码体系（诊断书）在此展开成整套维测；第1章「大楼会出错」的 107000/145000 在此给完整排查闭环。

**章节骨架**：

1. 日志子系统：`dfx/log/`——日志级别、渠道、`ASCEND_GLOBAL_LOG_LEVEL` 落入哪、`log_ref`
2. 错误管理与 watchdog：`dfx/error_manager/` + `dfx/trace/`（atrace、awatchdog）——错误上报、任务失败回调、设备异常检测
3. 数据 Dump：`dfx/adump/` + api_ref 18_dump——算子/张量 dump 的原理与落盘格式（对接第三编调试）
4. 性能 Profiling：`dfx/msprof/` + api_ref 19-*——msprof 的采集架构、API 插桩（本章只给架构与关键 API，量化解读留给第15章）
5. 综合排查案例：拿一个"算子结果不对/超时"的场景，四张单子怎么依次用（参考 hub 博客 ms_sanitizer / dumptensor_operator_debugging）

**源码抓手（已核对存在）**：

- `runtime/src/dfx/{log,error_manager,trace/{atrace,awatchdog},adump,msprof}/...`
- `runtime/docs/zh/{log_ref,error_code_ref,api_ref/18_dump_configuration,api_ref/19-*_profiling,api_ref/22_error_reporting_APIs}.md`
- `cann-learning-hub/blogs/operator/{ms_sanitizer_operator_cache_prevention,dumptensor_operator_debugging}/`（博客支撑案例）

**验收**：一张「四张单子怎么用」Mermaid；至少 1 个端到端排查案例；全部 `[需真机验证]`；verify 绿。

---

### 第8章 内存与数据通路（把第一编的搬运模型钉死在存储层次上）

**心智模型一句**：第2章说"性能天花板在搬运不在算"——本章把这句话落到存储地图：GM/L1/UB/各类片内缓存谁有、谁能搬到谁那、一次搬运怎么下单，同时把「要不要搬整块、要不要分块」的工程直觉立起来。

**承接**：第2章 2.2/2.3 的 GM→L1→UB 路线图、第3章「搬运带宽」这笔账；本章是**第三编（Ascend C 数据搬运 API）的前置章**，所以它一半属于第二编、一半预支第三编——写法上只讲"搬运的路线与成本"，不展开写码（那在第10/14章）。

**章节骨架**：

1. 存储层次全图：GM / L1 / UB / 寄存器 / L0A/L0B/L0C / 参数区，一张带"谁拥有、谁访问"的表（这是全书能背的第四张图）
2. 搬运单元分工：MTE1/2/3 与 FixPipe、NDMA 与 950 的 URMA/SHMEM（预告，详写在第18章）——只讲"谁能搬谁"
3. 数据通路形态：DAT/带步长搬运/广播/转置/压缩搬——给形态不给全部细节
4. 内存的"量"与"时"：UB 容量、分配/释放、暂存区生命周期、`LocalMemAllocator`
5. 成本心智模型落地：一次 copy 的字节数 × 单位带宽 vs 一次计算的 FLOPs——算给读者看的三笔账（呼应 3.5）
6. 一个贯穿案例：第2章那盘 Add 的搬运账单，逐段计算耗时构成

**源码抓手（已核对存在）**：

- `asc-devkit/docs/zh/guide/programming_guide/.../{memory_model,memory_access}*.md`（含 `concepts_and_terms/memory_access/{scalar_read_write,memory_vector_computation}.md`）
- `asc-devkit/examples/01_simd_cpp_api/05_best_practices/*/datacopy*`（可搬示例）
- `asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute` + `resource_management/LocalMemAllocator`
- `cann-learning-hub/blogs/operator/nddma_introduction/`（NDMA 前传）
- `runtime/docs/zh/api_ref/11-*`（GM 侧 malloc/物理内存，接第4章）

**验收**：存储层次总图（可背）+ 一次 Add 的搬运账单；grep 空；verify 绿。**本章收尾即第三编的桥头堡**：在章末「进一步阅读」预告第9/10章 API 层写法，保持书内前后引。

---

## 4. 执行顺序与落地步骤（M1 扩展先行，再进 M2）

| 阶段 | 步 | 动作 | 产出/验收 |
|---|---|---|---|
| **M1-扩展（选 B）** | B-1 | 按 §1.2 清单第1章扩展（含新增 1.3.1/1.6、FAQ 四连） | 第1章 ≥7k CN，verify 绿，三轮 review |
| | B-2 | 按 §1.3 清单第2章扩展（add.asc 实战、L1 手算、950 能力菜单 13 项） | 第2章 ≥7k CN，verify 绿 |
| | B-3 | 按 §1.4 清单第3章扩展（SQE 字段/图模式上手/三笔账实例） | 第3章 ≥7k CN，verify 绿 |
| | B-4 | 三章总校验 + appD/glossary/README/CHANGELOG 同步，README 里程碑 M1 转 ✅ | M1 评审门关闭 |
| **M2（照旧）** | M2-1 | STYLEGUIDE §2/§8 增量规则（M2 专属三条）并入，附录E 同步 | 风格基线锁定 |
| | M2-2 | 第4章成稿（材料最齐、承接最直接） | verify + review 三轮 |
| | M2-3 | 第5章成稿（最难，卡在 ≤5 锚点纪律） | verify + review 三轮 |
| | M2-4 | 第8章成稿（提前做，给第三编搭桥） | verify + review 三轮 |
| | M2-5 | 第7章成稿 | verify + review 三轮 |
| | M2-6 | 第6章成稿（边界章压轴，样式经验已就位） | verify + review 三轮 |
| | M2-7 | 第二编总收口：appD 更新、术语表增量、目录序言 | 里程碑表 M2 转 ✅ |

> 写作顺序 4→5→8→7→6：第4/5章是主线（ACL→runtime），第8章是为第三编提前搭桥（与第2章呼应），第7章（DFX）独立性强靠后，第6章（驱动，边界最受限）放最后以便借鉴前四章的经验与风格。

---

## 5. 工具链落地（这轮要顺手补的）

| 项 | 动作 | 涉及脚本/文件 |
|---|---|---|
| 字数口径 | `word-count.mjs` 增加「按编汇总达标/欠标」输出；M1 口径调整（总览编 3–5k：达标）写进脚本注释与 STYLEGUIDE | `scripts/word-count.mjs`、`STYLEGUIDE.md` |
| 脚注清单校验 | 加一个 advisory 脚本：每章「本章来源与进一步阅读」聚合清单的 `repo/` 路径自动过 `check-source` 同款校验（目前只校验脚注里的反引号路径） | `scripts/check-source.mjs`（扩展） |
| 头文件存在性 | 对 `#include "aclnnop/*.h"` 这类**生成头**加一条白名单规则：明确「生成头不在开源树」，避免 check:source 误报也不误导读者 | `scripts/check-source.mjs` |
| 里程碑表 | README 里程碑表与 CHANGELOG 保持一致并联动更新 | `README.md`、`CHANGELOG.md` |

---

## 6. 风险与边界（先承认，别等写完再补）

1. **无 NPU 真机**：第二编除第6章 cmodel 日志、第8章 CPU-SIM 可跑片段外，绝大部分样例 `[需真机验证]`。对策：每章给一张「怎么验证」清单（AsyncErr 透传、`NSys`/`msprof` 侧写流程），把"不可真机验证"写成"给你一套验证脚本"。
2. **无内核驱动源码**：第6章只能写「护照面」，力度靠"诚实性规则"（先声明可观测边界再写）。
3. **源码量巨大**：`runtime/core` 目录很厚（task 下就有 task_info/task_recycle/task_res_manage/task_submit 四子目录）。风险是写成源码翻译+流水账——应对是每章「≤5 锚点文件」纪律与「一句话动机 → ≤25 行关键码」强制。
4. **生成头/安装包产物不在仓**（`aclnnop/aclnn_add.h` 等）：已列为第4章勘误级脚注 + check:source 白名单，避免全书以「源码缺文件」为写作噪音。
5. **内容与第三/四编重叠**（DFX→15 章 profiling、内存→10/14 章数据搬运、NDMA→18 章）：用「预告/回指」而不是提前全写，保持每编一次讲透。**这条在选 B 后尤其关键**——§1.2–1.4 的新增小节全部按「总览级证据」挑选，凡 PLAN-PART1 已约定迁出的深度内容概不回填。
