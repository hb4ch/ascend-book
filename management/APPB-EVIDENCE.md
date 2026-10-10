# APPB 证据集 —— 术语表源码审查

rev2（2026-10-10；rev1 研究+本轮五项补证，见文末 rev2 节，与对应条目冲突处以 rev2 为准）。任务 `APPB-RESEARCH.md`/`APPB-EVIDENCE-CLOSE.md`。链路：根 `glossary.md`（唯一源）→`scripts/sync-glossary.mjs`（构建期原样拼接，仅加 frontmatter/标题）→`docs/附录/appB-glossary.md`；`check:terms` 按根表校验。**术语修订将来只改 glossary.md，不改 appB**。本证据逐条：原句→问题→建议→源证（完整路径）→架构限定/不确定。**未回源的不写**；书中他章说法不作自证。

## 1. AIC/AIV： expansions 错误＋「950 代称」错误（高优先）

- **原句**：`AIV（AI Vector）｜AIV 矢量核｜昇腾950 代称 AI Vector`；`AIC（AI Core）｜AIC 计算核｜昇腾950 代称 AI Compute`。
- **问题**：①AIC 展开成「AI Compute」无据——官方文档明写 **AIC（AI Cube）**；②AIC/AIV 并非 950 代称，**2201 架构（Atlas A2/A3 系）即已分核**。
- **建议**：AIV=AI Vector 核；AIC=AI Cube 核；适用范围注「AIC/AIV 分核形态见 2201 及以后架构；2002 架构 Cube/Vector 同核」。
- **源证**：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/cpp_tensor_programming/cpp_tensor_programming_overview.md` L272「AIC（AI Cube，主要用于Cube计算）…AIV（AI Vector，负责Vector计算）」；`…/advanced_programming/hardware_implementation/architecture_spec/npu_arch_2201.md` L14「AI Core分为AIC和AIV两个独立的核…配比1:2」；`npu_arch_2002.md` L15-17「Cube计算单元和Vector计算单元同核部署，共享同一个Scalar」。
- **不确定**：AIC 展开是否另有「AI Core」读法（asc_950_feature_guide 只用缩写）；不写死。

## 2. Cube/Vector 与 AI Core 的关系必须按架构分述

- **原句**：AI Core=「vector+cube 计算核」；Cube/Vector 为「AI Core 内××单元」。
- **问题**：2002 同核、2201 分核（AIC/AIV 各带独立 Scalar、1:2、经 GM 传递数据）——「内含」说法只对同核架构成立。
- **建议**：AI Core 条注明两代部署形态；Cube Core/Vector Core 条加「部署形态随架构：2002 同核共享 Scalar；2201 起分核」。
- **源证**：上条同两文件（`npu_arch_2002.md` L15-17；`npu_arch_2201.md` L14/L22）。
- **不确定**：3002 架构形态未读（`npu_arch_3002.md` 存在未审），表中不写 3002。

## 3. MTE1/2/3 搬运方向（glossary 三条全需修）

- **原句**：MTE1「L1→L0 等核内路径」、MTE2「搬入/搬出团簇」、MTE3「面向 L2/外存路径」。
- **问题**：MTE2/MTE3 方向表述含糊且 MTE3「L2/外存」无出处。
- **建议**（直接采用官方流水表）：MTE1=L1→L0A/L0B；MTE2=GM→L1、GM→UB；MTE3=UB→GM、L1→GM；另可补 FIX=L0C→GM/L1（glossary 未收）。
- **源证**：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/c_pointer_programming/c_programming_overview.md` L215-222 流水表；旁证 `…/architecture_spec/npu_arch_3002.md` L155「MTE2从GM搬运数据至UB」。
- **不确定**：无；方向为文档明示。

## 4. GM≠HBM、host 访问方式

- **原句**：「GM｜全局内存｜通常映射 HBM，host 可见地址空间」；「GM/HBM｜片外大容量内存」。
- **问题**：「host 可见地址空间」易读成 host 可直接寻址 GM——官方编程模型是 host 经 Runtime API 分配/拷贝，核函数经指针访问；GM 与 HBM 的对应是平台层实现（PlatformAscendC 中 `HBM = 6, // GM`），不宜写成同义。
- **建议**：GM=设备侧全局内存，核内 `__gm__` 地址空间、Runtime API 分配；「多数平台映射 HBM（如 2201 规格表），由平台层定义」；host 侧经 API 拷贝访问。
- **源证**：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simt_programming/memory_hierarchy.md` L21-27（Runtime API 分配/拷回）；`c_programming_overview.md` L315（`__gm__` 地址空间）与 L26（Host 分配 GM→拷贝→启动→释放）；`asc-devkit/docs/zh/api/Utils-API/platform_info/PlatformAscendC/GetCoreMemSize.md` L15（`HBM = 6, // GM`）；`npu_arch_2201.md`（容量表）。
- **不确定**：各代 GM→HBM 映射是否无一例外（未逐架构查）；保留「多数平台」限定。

## 5. SMEM：非「950 引入的核间共享内存」

- **原句**：「SMEM｜SMEM 共享内存｜950 引入的核间共享内存机制」。
- **问题**：仓内 SMEM=**SIMT 编程中 UB 内的线程块共享区**（+Data Cache），属 SIMT 抽象，非核间机制、非 950 专属名词（随 SIMT 模型于 3510 引入的是整个 SIMT 单元：DCache/Warp Scheduler/128KB RegFile）。
- **建议**：SMEM=Shared Memory，SIMT 编程里 UB 按功能划分出的线程块共享区；「SIMT 单元为 3510 新增」可注。
- **源证**：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simt_programming/abstract_hardware_architecture.md` L5/L13；`asc_950_feature_guide.md` 特性#2（SIMT 硬件单元=DCache、Warp Scheduler、128KB Register File）。
- **不确定**：无。

## 6. URMA：限定通信语境与出处

- **原句**：「URMA｜950 引入的统一远程内存访问通信机制」。
- **问题**：展开与「950 引入」需精确——官方全称 **Unified Remote Memory Access（统一远端内存访问）**，出现在 950 通信栈（CCU 执行搬运）与 hixl 配置项（「原有纯 URMA 路径」）中；作为「机制引入代际」的论断书内无独立出处。
- **建议**：URMA（不译）=Unified Remote Memory Access，hcomm/hixl 通信栈中的远端内存访问机制（CCU 依之搬运）；适用语境注 950 通信路径文献。
- **源证**：`hcomm/docs/zh/architecture/architecture-brief.md` L155、`hcomm/docs/zh/comm_op_dev_guide/prog_models_concepts/comm_engine.md` L55；`hixl/docs/zh/api/cpp/HIXL-interface.md` L307（comm_resource_config，「原有纯URMA路径」）。
- **不确定**：URMA 是否用于 950 以前代际（未查）；表中不写死「仅 950」。

## 7. 910B/910C ↔ Atlas A2/A3 映射：可证，留出处

- **原句**：「910B/910C｜昇腾910 系列两代，分别对应 Atlas A2/A3」。
- **结论**：**方向正确但有据可依**——pto-isa 官方平台支持表「Ascend A2（Ascend 910B）/A3（910C）/A5（950）」；asc-devkit 样例构建单元 `ascend910b ascend910_93 ascend950`；runtime ops 表按 Atlas A2→910b。建议保留并加脚注上述三处；**910_93（910B2?）与 910C 的对应**仓内未见明示，不写。
- **源证**：`pto-isa/README_zh.md` L168-172（平台支持）；`asc-devkit/examples/01_simd_cpp_api/02_features/99_acl_based/00_acl_compilation/custom_op/CMakeLists.txt` L31；`runtime/README.md` L126-133。
- **不确定**：`910_93` 含义（本书 ch27 曾按门控处理）；不在术语表展开。

## 8. Event/Barrier/Notify/CntNotify 分层

- **原句**：Event「流间同步原语」；Notify「片上同步轻量原语（aclrtCntNotify 等）」；无 Barrier 条。
- **问题**：①Notify 与 CntNotify 混写——runtime 是两个接口族（08 Notify 管理/09 CntNotify 计数型通知）；「片上」错，这是 **host runtime API**；②设备侧核间同步是另一层（CrossCoreSetFlag/WaitFlag、3510 起 Mutex/asc_lock）；③Barrier 在 SIMT 语境=线程同步屏障。三层不可混。
- **建议**：Event=host runtime 流间同步/计时（aclrtCreateEvent…）；Notify=host runtime 流上记录/等待原语，另有 CntNotify 计数型变体；设备侧核内/核间同步单列条目（CrossCore*/Mutex，3510 新增 mutex 机制并兼容 notify/wait）；Barrier=SIMT 线程屏障。
- **源证**：`runtime/docs/zh/api_ref/07_event_management.md` 头部（创建/记录/等待/计时）；`08_notify_management.md`、`09_cntNotify_management.md`（两族分立）；`asc-devkit/.../c_programming_overview.md` L224-230（3510 mutex 与 notify/wait 兼容表）；`npu_arch_2201.md` L189-190（CrossCore 两模式）；`ai_core_simt_programming/synchronization.md` L5（barrier 定义）。
- **不确定**：Notify 硬件实现细节（本书未拆）；表中只写接口层语义。

## 9. PTO/PyPTO 边界与 Tile 层次

- **原句**：PTO=「昇腾通用编程库…虚拟 ISA」；Tile/Block=「PyPTO 表达层级」；Execution Graph 同。
- **问题**：①PTO 官方定位句=「Parallel Tile Operation…面向 tile 编程的虚拟 ISA」（仓名 PTO Tile Library），「通用编程库」非原话；②Tile/Block/Execution Graph 的准确层次是 PyPTO 编译管线 **Tensor Graph→Tile Graph→Block Graph→Execution Graph**，Tile/Block 是图层级+暴露给不同角色的抽象（算法=Tensor/性能=Tile/系统=Block）。
- **建议**：PTO 条引官方定位句；新增「Tensor/Tile/Block/Execution Graph（PyPTO 编译层级，逐级降低抽象）」表述；PyPTO=PTO 的 Python 前端框架（编译至 PTO 虚拟指令）。
- **源证**：`pto-isa/README_zh.md` L5-7、L226（PyPTO=上层编程框架）；`pypto/README.md` L12/L19/L24（IR 管线与三角色分层）；`pypto/python/pypto/tensor.py` L61（class Tensor）。
- **不确定**：无。

## 10. 其余核对项（简）

- **AICPU**：概念=Device 上辅助处理器（ARM），「控制流复杂/数据依赖强任务」；**其编程文档标注仅支持 950PR/DT**——术语条可注「编程入口当前文档仅覆盖 950」（`ai_cpu_programming.md` L8-12；`programming_model.md` L99-101）。
- **UB 192KB**：是 **2201 架构规格值**（预留 256B；L1=512KB）——「通常 192KB 上下」应改「按架构规格表（如 2201=192KB）」（`npu_arch_2201.md` L45/L55/L61）。
- **N-DMA**：glossary「数据搬移引擎（scalar 侧）」无仓内出处；仓内实证是 **ND-DMA 搬运指令**（3510 新增，DataCopy 多维/stride 扩展）——建议改「ND-DMA：3510 新增多维搬运指令」或删条（`asc_950_feature_guide.md` 特性#7 及 DataCopy_GMToUB_NDDMA 链）。
- **CMO**：`aclrtCmoAsync`＝Device 上 Cache 内存操作（`runtime/docs/zh/api_ref/11-06_CMO_memory_operation.md` L5）——glossary「cache management operation」可保留并补接口名。
- **RegBase**：3510 起 AIV 从 MemBase→RegBase（`asc_950_feature_guide.md` 特性#1）——glossary「寄存器文件底座编程模型（语扩展）」可加此限定。
- **TSD/SQE/BQS/queue_schedule/aicpu_sched**：本书 ch4-5 依据，本轮未在 runtime docs 独立回源（仅 error/log 文档带及）——**保持现状不改**，标注「书中运行时章出处」；后续如需强证再回源 runtime 源码。
- **UBoE**：展开「UNified Bus over Ethernet」未见仓内明示（hixl comm_resource 仅协议名 `uboe`）；「总路线」错别字；建议只写「以太互连协议（hixl comm_resource 协议枚举之一）」。
- **HCCL/HCOMM/HIXL/HCCS/RoCE/PD 分离/KV Cache/MPMD**：与各仓 README 及已验收章一致，不动。

## D. 边界

仅只读 cat/grep；无新脚本、无缓存生成；appB/glossary 均未改。check:terms 现状：106 条、warn 1 处（ch24 既有「昇腾 C」子串，非术语表问题）。


---

# rev2 补证（APPB-EVIDENCE-CLOSE 五项）

## R2-1 MTE/流水方向：逐架构实证，废除单表推广

c_programming_overview 的流水表**未标适用架构**，rev1 直接采表有推广风险。逐架构实测（`architecture_spec/npu_arch_{2002,2201,3510}.md`「不同数据通路的带宽」表+正文）：

| 通路口径 | 2002 | 2201 | 3510 |
|---|---|---|---|
| MTE1 | L1→L0A/B（2002 表同构，带宽值不同） | L1→L0A/B（L67-68） | L1→L0A/B **＋L1→UB**（L131-133 新增） |
| MTE2 | GM→UB 实例（L100） | GM 侧搬入（L241「DMA(MTE2)…搬入」） | GM→UB 实例（L273） |
| MTE3 | 搬出（对称） | **UB→GM、L1→GM**（overview L256 同） | **UB→L1**（L134；未列 UB→GM 直达行） |
| FIX | —（2002 未列） | 未单列通路行 | **L0C→UB、L0C→L1**（L135-136） |

**术语结论（rev2 定稿口径）**：MTE1/2/3 只写「常见方向」——MTE1=L1→L0/L1 内搬运、MTE2=GM→片内（L1/UB）、MTE3=片内→GM/L1；**FIX 与 L1↔UB 等通路随架构变化，逐条注明「见对应 npu_arch_*.md 带宽表」，不合并成万能表**。已审架构=2002/2201/3510 三份（3002 未审，不推断）；**「2201 及以后」措辞废止，改「已审 2002/2201/3510 中…」**。

源路径：`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/architecture_spec/npu_arch_2002.md`（L98-100）、`npu_arch_2201.md`（L66-69 带宽表、L241）、`npu_arch_3510.md`（L130-136 带宽表、L263）。

## R2-2 SMEM 同名语境：全书仅一处使用，通信侧无实证，分立定义

- **全书使用处**：仅 glossary 本身（`glossary.md` L24）；正文各章未以「SMEM」行文——无既有语义需保护，修订自由度大，但仍按两类语境分立：
- **语境 A（SIMT 编程，已证）**：Shared Memory=UB 按功能划分的线程块共享区＋Data Cache（`abstract_hardware_architecture.md` L5/L13）；样例实操 `extern __ubuf__ float smem[]` 即 UB 指针（`asc-devkit/examples/03_simt_api/02_features/01_api_features/01_sync_instruction/memory_fence/sync_barrier.asc` L28-46）；3510 SIMT 单元含 DCache（`asc_950_feature_guide.md` 特性#2）。
- **语境 B（通信侧）**：**快照内未证**——hcomm/hixl 全源 `grep -r 'smem|SMEM'` 仅 memset/transmem 等子串命中，无独立「SMEM 共享内存」机制/库名；cann-learning-hub .md 零命中。**术语表不设「通信 SMEM」条**；如后续版本出现，再分立。
- **定稿建议**：SMEM 条单一义项＝语境 A，注「SIMT 编程语境；勿与泛化 shared memory 混用」。

## R2-3 GM 表述：去「多数平台」统计性断言

- **rev1 弊病**：「多数平台映射 HBM」未统计，不成立。
- **rev2 口径**：**GM 是地址空间概念，HBM 是存储介质**——两者关系由平台/架构规格定义（已证实例：`PlatformAscendC/GetCoreMemSize.md` L15 `HBM = 6, // GM`，2201 规格以 HBM 承载）；host 访问**按所用 API**（Runtime 分配/拷贝、核内 `__gm__` 指针），不写「必须经拷贝」「不可直接映射」的绝对句（统一映射型访问是否存在留待读者按平台文档确认）。
- 术语条建议：GM=设备侧全局内存地址空间（`__gm__`），容量与承载介质见对应架构规格；host 经 Runtime API 使用。

## R2-4 运行时术语源码回溯（TSD/SQE/BQS/queue_schedule/aicpu_sched）

| 术语 | 回溯结果（完整路径） | 结论 |
|---|---|---|
| TSD | `runtime/src/tsd/` 子系统实存；`runtime/src/tsd/common/basic_define.h` L17 `enum class HDCServiceType { FRAMEWORK, TDT, TSD, … }`——TSD 是 **HDC 服务类型之一**；`tsdclient/inc/tsd_process_controller.h`（进程控制器，HDC 消息构造 `ConstructOpenMsg/CloseMsg`） | glossary「片上任务调度/执行器」**不准确**：证据只支持「runtime↔设备间 HDC 通信中的服务端角色（与 TDT 并列的服务类型）」；**「片上」无据，待审**——建议改「runtime 设备通信服务（HDC 服务类型之一，见 tsd 子系统）」，细节留白 |
| SQE | runtime 侧未检索到 SQE 结构定义；旁证=`hcomm/src/legacy/ascend950/unified_platform/resource/stream/aicpu/hccl_sqe_v82.cc`（`Rt91095StarsMemcpySqe` 等 Rt 层 SQE 结构）——SQE 是 **Rt/设备接口层任务结构**，runtime 开源部分未见定义 | glossary 句「runtime 将任务转成 SQE 提交」**超出快照可证**；**待审**——建议改「设备接口层的提交任务结构（Rt 非开源头/二进制侧），本书未回溯其定义」或删条 |
| BQS/queue_schedule | `runtime/src/queue_schedule/` 子系统实存；`common/bqs_util.h` L11-12 include guard `QUEUE_SCHEDULE_BQS_UTIL_H`＋`namespace bqs`（`client/inc/ezcom_client.h` L21，EzcomClient/proto/easycom_message.pb）——BQS 是 queue_schedule 内部命名空间/组件族，**展开名未证** | glossary「用户态队列调度模块（BQS）」方向对；展开缩写不写；注「内部命名空间 `bqs`，含 ezcom client/server」 |
| aicpu_sched | `runtime/src/aicpu_sched/{aicpu_cust_schedule,aicpu_kernel,aicpu_processer,aicpu_prof}` 目录实存 | 「AICPU 任务调度模块」可证（目录结构），保留；补「含定制调度/Kernel/执行器/Profiling 子目录」 |
| UBoE | `hixl/docs/zh/api/cpp/HIXL-interface.md` L296-297：endpoint 协议枚举 `roce/ub_ctp/uboe/ub_rtp`，uboe 填 device uboe 网卡 ip——**仅协议枚举+配置项** | 「UNified Bus over Ethernet…总路线」展开无据→**改「hixl 通信协议枚举之一（以太系）；展开名未证」**，错别字一并修；不写成机制描述 |

**附录B 审计范围声明（rev2）**：以上五条+rev1 十组为**已审**；**术语表其余条目（约 60+）本书未逐一回源，不宣称「全表审毕」**——报告/提纲明示审计覆盖清单。

## R2-5 PyPTO 定位：非唯一后端、PTO 注入门控

结合 ch25 已审源码（`docs/06-backend/ch25-pypto.md` 25.4-25.5 及 `management/CH25-EVIDENCE.md`）：

- 码生成**主路径产出 CCE 壳＋TileOp 调用**（`pypto/framework/src/codegen/npu/codegen_npu.cpp` `GenCode` L270-315）；PTO 头注入受 **`codegen_support_tile_tensor`（默认 false）门控**，经 `GetPtoTileLibPathByEnv` 找 pto-isa `include/pto`（环境变量 `PTO_TILE_LIB_CODE_PATH` 或 CANN 包内）；另有不受该开关控制的头链包含（`tileop_common.h→pto/pto-inst.hpp`），最终是否入编译单元视 tileop 与架构路径——**「PyPTO 必经 PTO」不成立**。
- 执行分派三路（NPU/精度仿真 SIM/纯 host `DeviceInit+compile+_run_with_cpu`），host 分支内部显式 `compile`——**纯 host 路径可不经任何设备后端**。
- **术语条结论**：PyPTO=「PTO 生态的 Python 前端框架（PTO 上层编程框架，pto-isa README L226 原句）」；**不写「唯一后端」**；补一句「其码生成以 CCE 路径为主，PTO 调用为门控选项（`codegen_support_tile_tensor`，默认关）」；Tile/Block/Execution Graph 层次表述不变（rev1 §9 源证继续有效）。
- 源路径（完整）：`pypto/framework/src/codegen/npu/codegen_npu.cpp`、`.../codegen_npu.h`、`.../codegen/codegen_factory.h`、`pypto/CMakeLists.txt`；书内审记 `docs/06-backend/ch25-pypto.md` §25.4-25.5。

## R2 对 OUTLINE 的落点

提纲相应三条改写：MTE 条→「常见方向+逐架构带宽表引用，已审 2002/2201/3510」；SMEM 条→单义项 SIMT；TSD/SQE 条→降级待审表述或删；新增「审计覆盖声明」节（已审 15 条+未审清单）；PyPTO 条补门控句。


---

# rev3 补证（APPB-R1：SQE 漏检纠正、MTE 架构标签收敛、运行时术语第二批）

## R3-1 SQE：经理指正漏检，定义/填充链已回源（推翻 rev2「仅 Rt 层/未回溯」句）

- **目录实存**：`runtime/src/runtime/inc/sqe/aic_aiv_sqe_common.hpp`（372 行，`namespace cce::runtime`；`ConfigSqeDieFriendly`/`ConstructAivSqePart` 模板助手，L22-86）。
- **结构定义**：`runtime/src/runtime/core/inc/sqe/v200_base/stars_david.hpp`——`RtDavidStarsAicAivKernelSqe`（L148：header/groupDim/featureFlag/dieFriendly/mix/stackPhyBase…）、`RtDavidStarsAicpuKernelSqe`（`.../v200_base/aicpu_sqe.h` L114）、Notify/FunctionCall/HostfuncCallback Sqe 同文件；另有 `.../sqe/arch5162/stars_sqe.hpp`（`RtStarsAicAivKernelSqe` L106、`RtFftsPlusKernelSqe`）——**按架构分族**。
- **填充调用链**：task 构建器填 SQE——`davinci_kernel_task_v201.cc` L27-36（`ConstructDavidAICpuSqeForDavinciTask`→`aicpuSqe.header.type=RT_DAVID_SQE_TYPE_AICPU_D`）、L70-115（`ConfigSqeDieFriendly<RtDavidStarsAicAivKernelSqe>` 显式实例化）；`davinci_kernel_task_v200_base.cc` L283/307/320（`command->aicAivSqe` 直填）。
- **下发链**：`runtime/src/tprt/inc/external/tprt_type.h`——`TprtTaskSendInfo_t{sqeAddr,sqId,sqeNum}`＋`TPRT_ALLOC_SQ/CQ`（SQ/CQ 分配/查询）——SQE 经 tprt SQ 提交，与 glossary「SQ/CQ」条互证。
- **术语定稿**：SQE=runtime 构建并经 SQ 下发的任务描述符，结构按架构分族定义于 `core/inc/sqe/<arch>`；**rev2「设备接口层…定义未回溯」句废止**；glossary 已照此改。

## R3-2 MTE3「L1→GM(2201)」降级：overview 未标架构，不得贴 2201 标签

- 复核 `npu_arch_2201.md` 带宽表**仅两行**（L1→L0A 256/L1→L0B 128，L65-69）；2201 正文只有「MTE2 GM→UB…搬回 GM」叙述（L156-160/L195）与 `PIPE_MTE3` flag 例子——**「2201 MTE3=UB→GM/L1→GM」无架构文档直证**（L1→GM 来自未标架构的 c_programming_overview L221 总表）。
- **收敛**：MTE3 术语条只保留「UB→GM（2201/2002 同步示例两面叙述）＋3510 带宽表 UB→L1」，其余「随架构而异见规格」；MTE1 同规则（L1→L0A/B 三表均有，3510 另 L1→UB）。glossary 已照此改（rev2 的 2201 L1→GM 标签撤除）。

## R3-3 运行时术语第二批回源（APPB-R1 第 6 条，独立深证）

### Stream/Task
- `runtime/docs/zh/api_ref/06_stream_management.md`（Stream 创建/同步接口族，同 07 Event 目录序列）；Task=runtime 任务抽象，task 构建链实体见 `core/src/task/task_info/`（davinci_kernel_task_v20x.cc 即 KernelTask→SQE 装配）。
- 待第二批正文化：Stream→SQ 映射关系（tprt 层）未逐行。

### AICPU（补强 rev1 §10）
- 编程入口 950 限定（`ai_cpu_programming.md` L8-12）不变；**设备侧任务走 AICPU SQE**（`aicpu_sqe.h` `RtDavidStarsAicpuKernelSqe`、v201 `RT_DAVID_SQE_TYPE_AICPU_D`）——AICPU 任务与 AI Kernel 任务在 SQE 层分 type，同链下发。

### TSD（补强 rev2 R2-4：职责有据部分）
- `tsd_event_interface.h` L26-38 `TsdSubProcessType`：**TSD 编排的设备子进程=HCCP/COMPUTE(aicpu_schedule)/CUSTOM_COMPUTE(aicpu_cust_schedule)/QUEUE_SCHEDULE/UDF/NN/PROXY/BUILTIN_UDF/ADPROF**——直接把 aicpu_sched、queue_schedule 收进 TSD 管理。
- `tsd_process_controller.h/.cc`：`Open(rankSize)`/`OpenAicpuSd()`，日志「start hccp and computer process success」「skip to start aicpu-sd process」——启停编排实证。
- **定稿**：TSD=设备侧服务子系统，经 HDC 与 host 通信，负责上述设备子进程（含 aicpu/queue_schedule 调度进程）的生命周期编排；「任务调度器」泛称仍不写。

### BQS/queue_schedule、aicpu_sched
- 同上被 TSD 编排（`PROCESS_QUEUE_SCHEDULE`/`PROCESS_COMPUTE`）＋目录实存（`queue_schedule/{client,server,common,stub}`、`bqs_util.h` namespace）；aicpu_sched=aicpu 侧调度实现（`{aicpu_cust_schedule,aicpu_kernel,aicpu_processer,aicpu_prof}`）。

### tprt（新增核实）
- `runtime/src/tprt/`：`inc/external/tprt_type.h` SQ/CQ 属性枚举（SQ_HEAD/TAIL/STATUS、`SQCQ_MAX_DEPTH=1024`）与 `TaskSendInfo`——**tprt=runtime 内负责 SQ/CQ 资源管理与任务提交的传输层**（glossary tprt 条可由「跨主机/设备传输平台抽象」改此实证句；原句出处待查 ch5，暂不动词条，记录备批）。

## R3 glossary 落点（本轮已改）

SQE/TSD/MTE1/MTE3/PyPTO 五条再修订＋文末新增「来源与路径注记」节（7 组统一完整路径，供「见架构规格」类措辞收敛）；管理口吻（已审/本书未审）从说明列清除。sync 已再生 appB。
