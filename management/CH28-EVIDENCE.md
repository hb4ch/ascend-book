# CH28 证据集 —— 路线图与读者决策

rev4（2026-10-10；rev2=实现核验，rev3=VF 核体误称修正，rev4=R1 事实纠错）。任务 `CH28-RESEARCH.md`/`CH28-EVIDENCE-CLOSE.md`/`CH28-WRITE.md`。基线 `SOURCE-BASELINE.md`（采集 2026-10-09，只读 git log）：**各仓快照日不同**——asc-devkit `28e7aba2`/2026-08-22、pto-isa `dd3cb0fb`/2026-08-22、pypto `883e7dfb`/2026-08-22、hixl `9ed283b`/2026-08-22、hcomm `1581d16`/2026-08-22、cann-learning-hub `a3989658`/2026-08-21、ops-transformer `e75072d7`/2026-08-23；**引用实现证据须能在对应 commit 下复现，不得统称 8 月 22 日**。本书不联网核对今天状态。三种论断标注：**【发布】**=CHANGELOG/ReleaseNote/README 新闻条目（带发布日期）；**【码】**=快照内源码/样例实存（回源验证）；**【推】**=作者推断（正文须标）。

## A. 时间线骨架（全部【发布】，日期语义各异，正文不得混用）

| 时间 | 事件 | 类别/语义 | 出处 |
|---|---|---|---|
| 2026-01-06 | PyPTO v0.1.0 首发发布 | 发布日期（README 最新动态） | `pypto/README.md` L7 |
| 2026-03 | HIXL 超节点 FabricMem 文档化（公告月+doc 在仓；**公告时间≠实现时点**） | `hixl/README.md` Latest News；`hixl/docs/zh/FabricMem.md` |
| 2026-04-10 | PyPTO 0.2.0：**变更前端表达方法** | 发布日期 | `pypto/README.md` L4 |
| 2026-04-30 | asc-devkit v9.1.0-beta.1：**Tensor API 合入主线正式提供**、SIMT DCCI/浮点比较、低比特 cube 样例 | CHANGELOG「发布日期」栏 | `asc-devkit/CHANGELOG.md` beta.1 节 |
| 2026-05 | HIXL 应用开发教程发布（learning-hub） | 新闻月份 | `hixl/README.md`；`cann-learning-hub/tutorials/hixl_development` |
| 2026-05-31 | asc-devkit v9.1.0-beta.2：**SIMD VF printf/reg dump**、基础 API NPU Check、SIMT ld/st与AddrSpace、A5 L1 Tensor dump、950 兼容样例整改 | CHANGELOG「发布日期」 | 同上 beta.2 节 |
| 2026-08-21~23 | 各仓快照日（**逐仓不同**，见头部；提交日期≠发布/特性完成日） | SOURCE-BASELINE 逐行 |

**关键区分**（正文须写）：CHANGELOG 发布日期=打包发布时点；PR 合入时点未逐条查（本书不做 git 追溯每 PR）；「2026 Q2 Roadmap」是 issue 外链（`asc-devkit/README.md` L224，issues/316），**本书未抓取其内容**——只可写「存在该规划入口」，不得转述其条目【缺口】。过去目标日期已到与否无据可判。

## B. 四条「有实证的变化」（rev2：实现核验后改写；目录存在≠核验，以下均为**实读代码**）

### B1 Tensor API：新在「Layout/Shape/Stride 抽象」，且当前仅 Cube——「默认路径改变」废止

- 【发布】beta.1（2026-04-30）：「Tensor API分支代码合入主线，正式提供Tensor编程支持」。
- 【码·实现核验①】样例 `examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_mxfp4_tensor_api_high_performance/mmad_mx.asc`（548 行）实读：
  - 入口 `#include "tensor_api/tensor.h"`（L18，**独立于** `kernel_operator.h` 老路径）；
  - 张量构造 `AscendC::Te::MakeTensor(AscendC::Te::MakeMemPtr(ptr), AscendC::Te::MakeFrameLayout<Te::NDExtLayoutPtn/ScaleANDLayoutPtn…>(M,K))`（L71-84）——**Layout 模板显式表达排布**；
  - 切片 `tensor.Slice(Te::MakeCoord(...), Te::MakeShape(...))`（L86-98）；
  - 算子 `Te::Mmad(mmadAtom.with(mmadParams), l0C, l0A, l0B)`＋`Te::MakeMmad(Te::MmadOperation{}, MmadTraitMX{})` 静态装配（L329/L452），`MmadType::MX`、`fp8_e8m0_t` scale、`Te::Location::L0ScaleA/B`（L52-56/L150-157）；
  - GM/L1/L0 全链同名抽象＋`Mutex::Lock/Unlock<PIPE_MTE1>` 双缓冲同步（L159-166/L312-322，注释「Reverse synchronization…release」）。
- 【码·对照】非 Tensor 版 `matmul_mxfp4_high_performance/`（`matmul_mx.h/.asc`）include `kernel_operator.h`+`lib/matmul_intf.h` 手工传参——两样例同任务不同范式，**「新在哪」有对照物**。
- 【文·边界】`cpp_tensor_programming_overview.md` L19/L21 自述：基础 Tensor（指针+大小）早已有（**书 ch9/ch11 的 LocalTensor/GlobalTensor 并非 beta.1 才出现**）；扩展 Tensor=Layout/Shape/Stride+自动推导＋`AscendC::Te` 命名空间；**「当前能力赋能于 Cube 矩阵计算，后续将逐步支持 Vector」**——「新学算子默认路径改变」**废止**，改为「Cube/MX 类新项目可评估此路径；Vector 侧官方自述未覆盖」。RegTensor 绑定 3510（L19 括注），**3510 三级层级是 SIMD 视角特有，不替代芯片全局层级、不暗示旧代无寄存器**。产品条件**逐 README**：tensor_api 版=950PR/DT **>9.1.0**（其 README L11）；老范式 `matmul_mxfp4_high_performance`=950PR/DT **≥9.1.0**（其 README L16）——同族两样例条件差一个符号，不得以「样例族」泛化；编译均 `dav-3510`。样例性能数据（主频/每 cycle 乘加数、L2 带宽）为**其 README 自述**，本书不转抄正文。

### B2 设备内调试：新在 SIMD VF 路径；「打印靠 host」句书内无出处，改为对照书内既有能力

- 【发布】beta.2（2026-05-31）：SIMD VF printf/reg dump；基础 API NPU Check；A5 L1 Tensor dump。
- 【码·实现核验②】`examples/01_simd_cpp_api/01_utilities/00_printf/simd_vf_printf/simd_vf_printf.asc`（103 行）实读：`__simd_vf__ inline` 设备子函数内直接 `printf(fmt,…)`，经 **`asc_vf_call<…>(__ubuf__ float*…)`** 由核体调用（L68-75 区段）；**L72 `extern "C" __global__ __vector__ void simd_vf_printf_kernel()` 为设备核体，L76-77 `AscendC::printf`/`GetBlockIdx()` 就在核体内——是设备侧打印，不是 host 侧**（rev3 修正：核体≠host，设备侧执行；不写「host 仅 aclInit」式绝对句）。dump 侧 `02_dump/simd_vf_dump/simd_vf_dump.asc`：`asc_dump_ubuf/asc_dump/asc_dump_reg` 三接口＋`AscendC::Reg::LoadAlign/Duplicate`（L29-43 区段）。
- 【书对账】本书 ch11 已写 **SIMT `asc_printf`（`utils/debug/asc_printf.h`）**与 DumpTensor/msSanitizer（L210-215），且**ch11 注明「NPU-Check 在本地基线未检索到，降级处理」**——本轮复核：基线检索未见独立 doc/样例；**本章对 NPU Check 仅据公告转述、未做实现核验**（不声称全仓仅一句）。beta.2 公告=VF 路径新增打印/dump 接口；**不写「把 SIMT 能力补到 SIMD」的沿革推断**（技术演进叙事无据），只陈述公告与样例调用方式。
- 产品条件：simd_vf printf/dump=**仅 950PR/DT，≥9.1.0，dav-3510**（两 README 产品表/L73）；同目录 `simple_printf`（静态 Tensor）才覆盖 A2/A3/950——**能力-架构绑定须逐样例查**。`06_cpu_debug/README.md` L11-13：950PR/DT≥9.1.0、**A3≥9.0.0、A2≥9.0.0**（rev4 补 A2），L58 架构 `dav-2201/dav-3510`；GDB 断点/单步不依赖 NPU 但**仍需 CANN 工具链**。

### B3 低比特/MX 与 950（同 B1 样例族；无新增核验点）

【码】`matmul_mxfp4_{high_performance,tensor_api_high_performance,basic_api_high_performance}` 三样例实存；3510/950 条件同上。动作表述只到「阅读样例/具备 950 才可上板」。

### B4 HIXL 通信语义（改写：去数字、降 issue 强度）

【文·仓内 doc】`hixl/docs/zh/FabricMem.md` 实读：动机=LLM KVCache 内存压力、RoCE 瓶颈；方案=**Atlas 800T A3 超节点内 DRAM 统一编址、HCCS 直接访远端**——**带宽具体数字（20GB/s/百 GB 级）为该文自述，本书不转抄**（22 章已按未完整口径处理，此处更不重复）。Device UBoE（issue#275）与 A2/A3/A5 异构（#138/#115）仅 issue 标题级公告【文】，**不证明通用跨代互通已可用**；LlamaData等入门见 learning-hub 教程（存在性）。动作：KVCache 分离部署者关注该机制方向；验证条件=超节点环境，本书无。

## E2′ 计划类证据（rev4 按 R1 重写：pto-isa 有正式路线图，此前「无 dated roadmap」表述错误）

- **pto-isa 有带日期路线图**：`pto-isa/README_zh.md`「🛒 路线图」表 **L177-192**，10 行×4 列（功能/描述/范围/进度或完成时间）；标 **2026 Q2** 的有：集合通信扩展（Ccu/Roce 异步通信指令、TPREFETCH AIV 直驱）、微指令、基础指令（A5 性能优化+Pooling）、CostModel、CPU-SIM 同步构建；另有「持续演进」（Auto Mode/Tile Fusion/PTO-AS/卷积）与「规划中」（系统调度）。同 README 提示 master 可能与 CANN 版本不匹配；版本变更记录在 `pto-isa/ReleaseNote_zh.md`（Unreleased 暂无+初次公开发布条目）。**读法：目标季度≠完成，完成看后续 ReleaseNote 版本条目**；「Unreleased 暂无」只说明当前无新条目，**不推断记录纪律**（rev3 的该推断废止）。
- PyPTO：本书仅在 README「最新动态」核对到版本公告序列（0.1.0→0.2.0）；**未做全仓路线图检索，不下「无路线图」结论**。
- asc-devkit 规划入口=README 外链 issue（内容未读）；快照内未见独立 roadmap 文档。

## C. 回源验证记录（rev2：两项实现核验＋两项文档核验；「可编译示例存在」≠「已执行验证」）

| # | 级别 | 内容 |
|---|---|---|
| C1 | **实现核验①** | Tensor API 样例 `mmad_mx.asc`（548 行）全文实读：`tensor_api/tensor.h` include、`Te::MakeTensor/MakeFrameLayout/Slice/MakeMemPtr/Location::L0ScaleA`、`Te::Mmad(mmadAtom.with…)`/`MakeMmad` 静态装配、`Mutex::Unlock<PIPE_MTE1>` 双缓冲——符号/行号见 B1；对照样例 `matmul_mxfp4_high_performance/matmul_mx.h`（kernel_operator+matmul_intf 老范式）同读。**仅静态实读，未编译未运行**（dav-3510/950 条件，本书无环境） |
| C2 | **实现核验②** | 调试样例实读：`simd_vf_printf.asc`（`__simd_vf__`+`printf`、`asc_vf_call` UB 桥、`extern "C" __global__ __vector__`+`InitSocState`）与 `simd_vf_dump.asc`（`asc_dump_ubuf/asc_dump/asc_dump_reg`+`AscendC::Reg::LoadAlign/Duplicate`）；产品条件 950PR/DT≥9.1.0（README 表）。**未运行** |
| C3 | 文档核验 | `cpp_tensor_programming_overview.md` L19/L21：基础 Tensor vs 扩展 Tensor 定义、**「当前赋能 Cube，Vector 后续」**、3510 括注——B1 边界表述的直接出处 |
| C4 | 文档核验 | `hixl/docs/zh/FabricMem.md` 全文读：动机/方案结构；数字为文内自述。书 ch11 L210-215/L215 对账：SIMT asc_printf 已写、NPU-Check 曾降级——本轮复核基线内 NPU Check 仍仅 CHANGELOG 句 |

## C′. 本书 ch11/ch12 相关旧表述对账（B2 修正依据）

ch11 L210：`asc_printf`（SIMT/SIMD 核内打印，hello_world 真码）**书内已有**——「打印靠 host 日志的旧约束」并非书内原话，EVIDENCE rev1 该句无证，废止；净新增只能是 SIMD VF 路径原语。ch11 L215：NPU-Check 降级注记——beta.2 后仍无 doc/样例，注记继续成立。ch12 L94-96：asc_printf include 示例属 SIMT 路径，同前。

## D. 边界与未验证清单（正文「局限」节材料）

1 无 NPU/无 A5、950 实机：两项样例已**实读实现**（C1/C2），但未编译未运行——「可编译示例存在」与「已执行验证」全程分开表述；2 asc-devkit roadmap issue#316 内容未抓取（外链），只写入口存在；3 各 PR 仅 CHANGELOG 转述，未回溯 git 合入点；4 hixl issue#275/138/#115 仅标题级；5 性能数字（FabricMem 带宽等）为文档自述，无本书实测；6 PyPTO/pto-isa 无 dated roadmap 文件——「计划」类证据薄弱，正文不得虚构路线；7 今天线上状态未核对（纪律：不以网站覆盖基线）。

## E. 图表方案（1–2 幅）

| # | 形式 | 内容 | 备注 |
|---|---|---|---|
| 图① | mermaid timeline/flowchart TD | 2026-01→06 五节点时间线：PyPTO 0.1.0→HIXL FabricMem→PyPTO 0.2→beta.1 TensorAPI→beta.2 调试/HIXL教程；每节点标【发布】与日期语义 | 节点短名无括号引号 |
| 表① | markdown | 四条变化×（发布证据/回源/读者行动/条件）四列——行动列写「做什么+需要什么条件」 | 主表，正文围绕它展开 |
| 表②（备选） | markdown | 三种论断标签示例两行（【发布】vs【码】同一条信息的两种强度） | 若版面紧可并入正文句 |

## F. 写作纪律映射

不重讲 26 章生态（PyAsc/TileLang/torchair 等不再出现）；不编四代硬件性能对比、不预测日期/倍数；框架能力（Tensor API）/产品支持（A5,950 样例）/宏存在（3510 三级层级）分属不同证据强度，分别措辞；每条结论带路径+版本+状态；学习行动以短段给出「做什么/需要什么/本书验证到哪一层」。
