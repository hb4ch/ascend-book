# CH24 证据集 —— PTO 虚拟 ISA（第 24 章）

rev3（2026-10-10，R1：图规划改三图实况；B7b 措辞与 624px 验收见 `CH24-R1-RESPONSE.md`）。rev2（2026-10-10，按 `management/tasks/CH24-EVIDENCE-CLOSE.md` 修订：B7/C1 重证、A1 引文纠错、A2/B1/E1/F2 收窄，新增 §I 布局·事件·设备约束补证）。
任务：`management/tasks/CH24-RESEARCH.md`（2026-10-10）、`CH24-EVIDENCE-CLOSE.md`。
正文与图已按本证据（rev2）落笔：`docs/06-backend/ch24-pto-isa.md`；写前余项（I2/I3/B7b/图②/cpu_stub 路径）已在本轮修订，见 `CH24-EVIDENCE-CLOSE-RESPONSE.md` 后续 `CH24-REPORT.md` 自查。
源码基线：`/mnt/SATASSDEXT4/cann/pto-isa`，master `dd3cb0fbd5…`（"revert trem"，2026-08-22；见 `management/SOURCE-BASELINE.md`）。
复核方式：所有行号为该基线工作树实测（`grep -n` / `sed -n`）；执行结论以 2026-10-09 经理记录 + 2026-10-10 本轮复跑为准（见 §F）。
写作纪律映射见 §H。**本文件只陈述"源码/文档怎么说"，不补因果、不推断未记载行为。**

---

## A. 仓库定位与规模

| # | 论断 | 证据 |
|---|------|------|
| A1 | PTO 定位：面向 tile 编程的虚拟 ISA，目标是平滑跨代迁移 | `README_zh.md:7`：「PTO（Parallel Tile Operation）是昇腾 CANN 定义的一套面向 tile 编程的虚拟 ISA。……帮助开发者在不同昇腾代际之间更平滑地迁移和优化算子」 |
| A2 | 指令规模只采 README 口径；通信扩展仅述存在，不列清单 | `README_zh.md:23`：「定义 90+ 条标准 tile 指令，用更高层的 tile 编程模型桥接不同代际之间的实现差异」；`:28` 同口径。`:30`：「除计算与数据搬运指令外……通信扩展指令集，覆盖点对点通信、信号同步和集合通信三类能力」 |
| A3 | 平台面：徽标 A2/A3/A5/CPU；A5 支持时间线 | `README_zh.md:10` Platform badge `Ascend A2 \| A3 \| A5 \| CPU`；`:18`：「2026-03-30：支持昇腾 A5 芯片，新增异步通信指令、CostModel 性能仿真」 |
| A4 | 仓库三大块：include/docs(demos+tests) | 顶层 `include/pto/`、`docs/`、`demos/`、`tests/` 目录清单（`ls` 实测）；`demos/{baseline,cpu,torch_jit}`、`tests/run_cpu.py --demo gemm`（`tests/run_cpu.py` 用法输出） |

## B. 核心抽象：Tile 五属性 / GlobalTensor / 布局

| # | 论断 | 证据 |
|---|------|------|
| B1 | Tile 五属性：所在位置、元素类型、容量形状、布局、有效区域；容量形状≥有效形状 | `docs/coding/Tile_zh.md`「Tile 的五个核心属性」节（明文“容量形状大于等于有效形状”）；`include/pto/common/pto_tile.hpp` `struct Tile`（L1395 起）模板含有效形状参数 `RowValid_`/`ColValid_`（默认等于 `Rows_`/`Cols_`，即可省略） |
| B2 | 有效区域可动态收缩：`RowMaskInternal/ColMaskInternal` + `SetValidShape` | `pto_tile.hpp`：`unsigned RowMaskInternal; unsigned ColMaskInternal;`（Tile 成员区，约 L1590 附近）；`PTO_INTERNAL void SetValidShape(unsigned rowMask, unsigned colMask)` 带 `PTO_ASSERT(rowMask <= Rows && colMask <= Cols, "rowMask and colMask must not exceed Rows and Cols.")` |
| B3 | 容量常量：32B 对齐 / AB 分形 512B / C 分形 1024B | `pto_tile.hpp:1078-1087` `namespace TileConfig`：`alignedSize = 32`（L1079）、`fractalABSize = 512`（L1084）、`fractalCSize = 1024`（L1085）、`fractalMxSize = 32` |
| B4 | 32B 对齐是 static_assert 硬约束（非文档口号） | `pto_tile.hpp` Tile 内：`"BFractal_ is RowMajor and SFractal_ is NoneBox: Rows must be 32 bytes align, ..."` static_assert（`Cols * sizeof(DType) % TileConfig::alignedSize == 0` 分支） |
| B5 | 分形布局偏移有唯一权威公式（Nz/Zn/Zz 三族） | `pto_tile.hpp` `GetTileOffset(int row, int col)`：`is_Nz_layout` → `(BlockNumRow * BlockCol + BlockRow) * InnerNumel + InnerRow * InnerCols + InnerCol`；Zn/Zz 各有分支；否则 `static_assert(sizeof(TileT) == 0, "Unsupported layout ... Nz or Zn layout.")` |
| B6 | GlobalTensor = 5 维 shape/stride 包装，默认 shape 全 1 | `pto_tile.hpp` `struct GlobalTensor` 成员 `Shape shape_; Stride stride_;`；`defaultShape{1, 1, 1, 1, 1}` / `defaultStride{1, 1, 1, 1, 1}`（GlobalTensor 定义后模板静态成员）；`GetStrideSize`/`SetAddr(DType* addr)` |
| B7 | 主例两层形状各司其职：GM 侧是行主序，Tile 侧 `BLayout` 只描述分形块布局，二者不混同 | `gemm_demo.cpp:83` `GlobalA = GlobalTensor<float, Shape<1,1,1,kM,kK>, Stride<1*kM*kK, 1*kM*kK, kM*kK, kK, 1>>`——末两维 stride `(kK,1)` 即行主序（kM=32,kK=16,kN=32，L57-59）；`:91` `TileMatA = Tile<TileType::Mat, float, kM, kK, BLayout::ColMajor, kM, kK, kM, kK, SLayout::RowMajor, kTileAlignBytes>`，`BLayout::ColMajor` 仅指 512B 分形块在线性存储中的排布次序，块内 `SLayout::RowMajor` 另论 |
| B7a | TLOAD 完成的转换：行主序 GM → 分形布局 tile，按有效区域抄写，容量余量填 pad | `include/pto/cpu/TLoad.hpp:127` `TLOAD_TILE_IMPL`：先 `std::fill(dst.data(), …, getPadValue<TileData>())` 填满整个容量（L142），再双循环 `for (row < validRow) for (col < validCol)` 用 GM 的 5 维 stride `GetElement` 取数、`dst.SetElement(row, col, …)` 按 tile 布局写入（L151-157）；即“布局转换 + 有效区域遮罩”都是 TLOAD 显式做的，非编译器魔法 |
| B7b | 偏移数值验证（复算脚本与输出；几何同主例 aMat：32×16 float、ColMajor 块、RowMajor 块内 512B） | `management/validation/ch24-tile-offset-compute.py`（可复现脚本）与 `.log`（输出）：该布局下 elem(1,1) 存储偏移 9（36B），GM 行主序同元素偏移 17（kK+1）；每块 16×8 float＝512B，2×2 块共 512 float＝2048B。注：aMat 为显式模板参数，两侧同构；TileLeft 别名差异影响的是 TMOV 目的 aTile（见 I3） |
| B8 | **跨代际布局差异实证：TileLeft 的 BFractal 按代际不同** | `pto_tile.hpp:1706` `#if defined(PTO_NPU_ARCH_A2A3) \|\| defined(PTO_NPU_ARCH_KIRINX90)` 分支内 `using TileLeft = Tile<TileType::Left, …, BLayout::RowMajor, …>`（L1708）；`:1718` `#if (!defined(PTO_NPU_ARCH_A2A3) && !defined(PTO_NPU_ARCH_KIRINX90)) \|\| defined(__CPU_SIM)` 分支内 `TileLeft = Tile<…, BLayout::ColMajor, …>`（L1720）。即同一 `TileLeft` 名字，A2A3 代是 RowMajor、CPU-SIM/其他代是 ColMajor——虚拟 ISA 抹平差异的实例，正文可作为"差异被收进类型别名"的例证 |
| B9 | `__PTO_AUTO__` 惰性分配（CPU-SIM + COSTMODEL 下 data_ 为指针，首次访问 resize） | `pto_tile.hpp` Tile 内：`#if (defined(__CPU_SIM) && defined(__PTO_AUTO__)) \|\| defined(__COSTMODEL)` → `TileDType& data() { if (!data_) { internalBuffer.resize(Rows * Cols / …); data_ = internalBuffer.data(); } … }`；注释 `// CPU Sim: data_ is a pointer that TASSIGN can redirect to shared NPU memory` |

## C. 指令面：一条指令如何构成程序

| # | 论断 | 证据 |
|---|------|------|
| C1 | 事件返回值与 WaitEvents 变参是“可选项”而非所有指令的共性：`TASSIGN` 返回 void；`TLOAD/TMOV/TMATMUL` 返回 `RecordEvent` 且 WaitEvents 可空 | `pto_instr.hpp:28` `PTO_INST void TASSIGN(T& obj, AddrType addr)`（无事件参与）；`:218` `RecordEvent TLOAD(TileData& dst, GlobalData& src, WaitEvents&... events)`、`:656` `RecordEvent TMATMUL(...)`、`:1305` `RecordEvent TMOV(...)`——主例 gemm_demo 调用均未传 ev、未接返回值 |
| C1a | 真实设备侧事件链示例（与主例分开引用，不拼接） | `kernels/manual/a2a3/moe_combine/moe_combine_kernel.cpp:537` `pto::Event<pto::Op::TAXPY, pto::Op::TLOAD> axpyToNextLoad;`；`:547-552` `loadToAxpy = TLOAD(...); axpyToNextLoad = TAXPY(..., loadToAxpy);`；`:549/:556` `axpyToNextLoad.Wait();`——事件对象跨循环迭代传递依赖 |
| C2 | 主例指令序列（gemm_demo 单 tile 数据旅程） | `demos/cpu/gemm_demo/gemm_demo.cpp`：TASSIGN L103、TLOAD L109（GM→tile）、TMOV L111、TMATMUL L114/L118、TSTORE L121（tile→GM）；`kDiffThreshold` L62；退出判定 L142（循环边界） |
| C3 | TLOAD 之外还有预取类：注释明说"stage 进 L2" | `pto_instr.hpp:235` 附近注释：`// Stages a contiguous GlobalTensor region into L2 cache so subsequent TLOADs…`（cache 预热指令，名字以该行所在函数为准） |
| C4 | Manual 范式=同一指令集+显式流水线 | `kernels/manual/a2a3/gemm_performance/gemm_performance_kernel.cpp`：头部注释 L18–34 流水线说明（TLOAD GM→L1、TEXTRACT L1→L0、TMATMUL Cube、TSTORE L0C→GM）；双缓冲 L80–90/L198；`SetFlag/WaitFlag` L38–46 配对（PIPE_MTE1/MTE2/M） |
| C5 | Auto/Manual 职责分工 | `docs/mkdocs/src/manual/02-machine-model_zh.md`：Host/Device/Core 三代理、Tile 粒度、"程序顺序/事件顺序/内存可见性"三个顺序域、Auto 与 Manual 各自职责段（写作时按节引用，不再逐行） |

## D. 同步模型与 CPU-SIM 边界

| # | 论断 | 证据 |
|---|------|------|
| D1 | `Event<SrcOp,DstOp>` 仅设备侧存在 | `docs/coding/Event_zh.md`：`Event<SrcOp, DstOp>` 定义处注明仅 `__CCE_AICORE__`（设备编译）可见 |
| D2 | CPU-SIM 中 TSYNC 是 no-op；set_flag/wait_flag 空实现；官方文档明言“单线程程序顺序验证语义” | `include/pto/common/cpu_stub.hpp:118-119` `inline void set_flag(pipe_t,pipe_t,int){}` / `wait_flag` 同；`docs/coding/Event_zh.md:7`：「CPU 仿真后端通常将 TSYNC 视为 no-op，并依赖单线程的普通程序顺序来验证语义」、`:43` `TSYNC_IMPL` no-op；`docs/coding/cpu_sim_zh.md` 全同步执行节 |
| D3 | CPU-SIM 流水线常量仅是编号：`PIPE_M=5` 等 | `include/pto/common/cpu_stub.hpp:50` `const pipe_t PIPE_M = 5;`（纯常量，无流水线语义；对照 `costmodel/perf_sim/pipe_model_queue_impl.inl:122` 才有队列模型）——正文写明“仿真中流水线常量退化为编号” |
| D4 | `AICORE` 在 CPU 侧定义为空宏 | `include/pto/common/cpu_stub.hpp:29` `#define AICORE`（空）；设备侧 `include/pto/common/type.hpp:14` `#define AICORE [aicore]` |
| D5 | CPU-SIM 模拟 UB/L1/L0A/L0B/L0C，每线程独立；代际枚举只有 A2A3/A5 | `include/pto/cpu/NPUMemoryModel.hpp:39` `enum class NPUArch { A2A3, A5 };`；A2A3 容量自 L63 起；A5 容量自 L78 起，含注释 `// placeholder - verify actual A5 spec`（未定稿实证） |
| D6 | CPU-SIM 原子加有互斥锁（真并发语义仅此一处可见） | `pto_tile.hpp` `AddToElement`：`std::lock_guard<std::mutex> lock(cpu::AtomicAddMutex());`（`__CPU_SIM` 分支内） |
| D7 | 编译宏边界：CPU-SIM 构建定义 `-D__CPU_SIM -D__PTO_AUTO__` | `/tmp/ascend-book-pto-gemm/CMakeFiles/gemm_demo.dir/flags.make`：`CXX_DEFINES = -D__CPU_SIM -D__PTO_AUTO__`；`CXX_FLAGS = … -std=gnu++23 -O3 -DNDEBUG -O2`（2026-10-10 本轮实测） |

## E. 后端矩阵与 NPU 实现

| # | 论断 | 证据 |
|---|------|------|
| E1 | NPU 后端按代际分目录：a2a3、a5；平台面由 README badge 与新闻条目背书 | `include/pto/npu/{a2a3,a5}/` 目录实测；平台声明见 A3（badge L10、A5 新闻 L18），不引“根 README 可能还有”类模糊源 |
| E2 | a6 目录存在但文档未述——**不得据此写"支持 A6"** | `include/pto/npu/a6/` 目录存在；全部 docs 无 a6 章节内容（rg 'a6' docs/ 仅路径级命中）。正文只可写"仓库内存在 a6 目录，文档未描述" |
| E3 | 设备/仿真共用同一套 PTO 头：以宏切换实现 | `pto_tile.hpp` 内 `#if defined(__CPU_SIM)` / `#ifdef __PTO_AUTO__` / `PTO_NPU_ARCH_A2A3` 分支贯穿（B8/D7 已引）；`type.hpp:14` 设备侧 `[aicore]` |
| E4 | COSTMODEL 是第三种编译形态（和 CPU-SIM 并列出现在分支里） | `pto_tile.hpp`：`#if defined(__CPU_SIM) \|\| defined(__COSTMODEL)`（头部 include 区）与 `#ifdef __COSTMODEL` `float cycle; SetCycle/GetCycle`（Tile 成员）。CostModel 行为本章不展开，仅注记存在 |
| E5 | comm 指令在 ISA 索引中独立成目录 | `docs/isa/comm/`：TPUT/TGET/TASYNC/TNOTIFY/TWAIT/TTEST 等 12 项（A2 同）；NPU 侧 comm 行为本章不断言（见 §G 未闭） |

## F. 复现链（执行证据；均不构成 NPU 验证）

| # | 内容 | 证据 |
|---|------|------|
| F1 | 经理记录（2026-10-09）：cmake configure/build/run，M=32 K=16 N=32 float，`max_abs_diff=1.19209e-07` | `management/validation/PTO-CPU-GEMM.md`；日志 `management/validation/pto-gemm-{configure,build,run}.log` |
| F2 | 本轮复跑（2026-10-10）：**直接执行既有二进制（非重编译）** `/tmp/ascend-book-pto-gemm/gemm_demo`，输出 `max_abs_diff=1.19209e-07` 与记录一致；全文存档 `management/validation/ch24-cpusim-gemm-rerun.log`（含 demo 自带 perf 行，仅为 CPU-SIM 参考） | 会话执行记录；构建目录 `flags.make` 见 D7 |
| F2a | 工具链版本回源现有记录核实 | `management/validation/PTO-CPU-GEMM.md:5`：「g++ 16.2.1 20260810，CMake 4.4.2」；本轮 `g++ --version`/`cmake --version` 输出同一版本串，已附于 rerun 日志末尾 |
| F3 | 工具链版本与记录相符 | g++ 16.2.1、CMake 4.4.2（`g++ --version`/`cmake --version` 会话实测；与 PTO-CPU-GEMM.md 记录一致） |
| F4 | 复现命令（正文 24.x 引用，含勘误后路径） | `cmake -S /mnt/SATASSDEXT4/cann/pto-isa/demos/cpu/gemm_demo -B <build> && cmake --build <build> && <build>/gemm_demo`；亦可 `tests/run_cpu.py --demo gemm`（A4） |
| F5 | 措辞纪律 | CPU-SIM 运行=CPU 仿真验证，**不等于 NPU 上验证**；正文写"仿真通过"而非"验证正确"（任务书要求，D5/D7 支撑边界描述） |

## G. 文档勘误与未闭清单（正文只注记，不展开）

1. **getting-started 路径过时**：`docs/getting-started_zh.md:429` 仍写 `tests/cpu/demos/`，实际目录为 `demos/cpu/`（ls 实测）。正文复现节按实际路径写，可脚注勘误。
2. **A5 容量是 placeholder**：`NPUMemoryModel.hpp:78` 起，注释 `// placeholder - verify actual A5 spec`（D5）。正文不得把 A5 容量写成定论。
3. **a6 后端无文档**（E2）。
4. **comm 指令 NPU 侧行为未核**（E5）：本章只写 ISA 面貌，不写其 NPU 语义。
5. **CostModel 语义未核**（E4）：只注记 `__COSTMODEL` 编译形态存在。
6. **性能数字**：本章不虚构；如需引用仅限 README/厂商公开实践并注明出处；A3 24 核等拓扑数字无源码依据，不写。
7. **指令总数只写 README 口径“90+”（A2）**；ISA 索引去重计数不进正文。
8. **设备侧 TMATMUL 合同（I2）**：可写“a2a3 静态检查表含 float,f,f 组合、动态维度 [1,4095]”；a5 同有 `MMAD_MAX_SUPPORT_LENGTH=4095`（L20）但 dtype 表未逐条核，不写“a5 同表”。
9. **可移植性措辞**：仿真可用 ≠ 设备支持；TileLeft 分支只证明别名映射按代际不同，不证明整程序免改跨代（I3）。

## H. 写作纪律映射（→ STYLEGUIDE / ACCEPTANCE / 任务书）

- 每图一问、图前自然问句、图后「读图：」——提纲 `CH24-OUTLINE.md` §图规划已按此写明，正文执行。
- 脚注 `[^n]` 双向闭环；代码/路径脚注给仓库内完整相对路径（`pto-isa/include/...`），不写裸文件名。
- 无证因果禁写：B8 的代际差异只陈述"别名按代际不同"，不写"因为硬件要求 Zn/Zz 所以…"（源码无此注释）；TSYNC no-op 只陈述事实，不推断"因为全同步所以安全"以外文档原话。
- 复现节措辞：「仅 CPU 仿真验证；未在 NPU 设备上运行」（F5）。
- 字数：按任务书豁免同 CH23 口径——主例（gemm_demo 单 tile 旅程）完整优先，不为字数加变体。

## I. CLOSE 补证：有效区域语义 · 设备 TMATMUL 合同 · 可移植性边界

| # | 论断 | 证据 |
|---|------|------|
| I1 | 有效区域非“自动遮罩”：每条指令各自显式处理 | TLOAD 先填满容量再只抄 valid（B7a）；CPU TMATMUL `TMatmulNzZn` 以 `M/K/N = GetValidRow/Col` 为计算边界（`cpu/TMatmul.hpp:51-57`）；TSTORE 只写 valid 但先断言容量≥validRow×validCol（NZ 布局要求精确相等，`cpu/TStore.hpp:22-37`） |
| I2 | 设备侧（a2a3）TMATMUL 的 dtype/形状合同，统一记作 (A,B,C) | `npu/a2a3/TMatmul.hpp:78-96` `CheckStaticMad` 四组：(A=int8,B=int8,C=int32)、(half,half,float)、(float,float,float)、(bf16,bf16,float)；`:17` `MMAD_MAX_SUPPORT_LENGTH = 4095`；`:157-167` `TMATMUL_IMPL` 取 m/k/n 自 valid 并 `CheckDynamicMad`（界 [1,4095]）。主例 float 32×16×32 落于表内界内——**静态检查结论，非设备实跑**；a5 仅 `:20` 同界，dtype 表未逐条核 |
| I3 | 可移植性边界与“两次搬运”的区分 | 主例 TLOAD 目的 aMat 是**显式** `BLayout::ColMajor` 模板（B7），两侧同构——不能从 TileLeft 别名分支推出“TLOAD 布局因代际而变”；别名差异出现在**第二次搬运** TMOV 的目的 aTile（`TileLeft`：A2A3=RowMajor 块、CPU-SIM=ColMajor 块，B8），即同一 aMat 数据经 TMOV 后的物理次序随代际不同，各由自身 `GetTileOffset` 自洽消费。正文措辞：“仿真验证程序结构与数值；设备支持性以 I2 合同为准，未实机验证；CPU 对拍通过不是 NPU 数值精度/时序证明” |
| I4 | NPU 侧 TLOAD 存在（结构对称），本章不展开实现 | `npu/a5/TLoad.hpp:923` 等处 `TLOAD_IMPL`；只注存在 |

## 图规划数据齐备性核对（R1 后实况：①③ mermaid 内嵌、②手绘 SVG `docs/figures/ch24-tile-layout.svg`，生成器 `validation/ch24-fig2-gen.py`；三图均以 624px 正文宽截图验收）

| 图 | 需要的数据 | 状态 |
|----|-----------|------|
| ①数据旅程（A/B 双支路，TB） | GM stride A(kK,1)/B(kN,1)、TLOAD/TMOV/TSTORE 搬运与 TMATMUL 计算分标 | B7/C2；齐（624px 内 scale 1.0） |
|②三层结构|手绘 SVG：32×16 全貌块序编号＋块#0 放大格高亮，elem(1,1)＝块(0,0)内(1,1)偏移 9、GM 同元素 17；动态 valid 注非主例 | B1/B2/B3/B5/B7b/I1；齐（偏移由 `ch24-tile-offset-compute.{py,log}` 背书） |
|③事件两向 vs CPU 顺序|loadToAxpy 前向/axpyToNextLoad 反向＋收尾 Wait；CPU-SIM 无事件、对拍仅本样例 | C1a/D2；齐（624px 内 scale 0.85、有效字号≈13.7px） |
