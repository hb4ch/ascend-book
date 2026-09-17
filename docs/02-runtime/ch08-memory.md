---
title: 第8章 内存与数据通路
description: 内存层级（GM/L1/UB）、分配模型、N-DMA 多维搬运、对齐/带宽/乒乓、零拷贝与数据复用、AIPP，以及为性能编铺路
status: 已成稿（M2，第二编）
---

# 第8章 内存与数据通路

> 前几章你学会了「点单、排队、送菜」。这一章回答另外一半：**菜放在哪、怎么从锅里搬上桌**。昇腾算子性能的天花板往往不在「算」，而在「搬」——数据在 GM、L1、UB 之间来回倒腾的带宽和延迟，决定了你到底是「算得快」还是「被搬运卡死」。本章只讲一件事：**把「数据怎么流动」这条通路讲清楚**，并把最值得掌握的 N-DMA 当作主角。读完你会理解为什么算子优化的第一课是「减少搬动」。

## 8.1 内存层级：从「大而慢」到「小而快」

第2章说过 AI Core 有存储单元。这一章把它落到「程序员看得见的层级」上。昇腾 AI Core 的存储从使用位置上分两大类[^memlay]：

- **Global Memory（GM）**：Device 侧全局存储，大、但离算力远。是数据搬入/搬出的主要来源和目的地。
- **Local Memory**：AI Core **片内**存储，小、但离算力近。暂存从 GM 搬入的数据分片、保存计算输出和中间结果，Vector/Cube 高效访问它。

Local Memory 内部再分级，最常用的是 **UB（Unified Buffer）** 和 **L0/L1**。L1 喂矩阵计算（Cube）用的 L0A/L0B，UB 喂矢量计算（Vector）用的数据分片[^memlay]。

把这层关系画成一条「从远到近」的线：

| 存储 | 离算力 | 典型用途 | 谁在用 |
|---|---|---|---|
| GM | 最远 | 大块数据、模型权重 | 搬运单元存取 |
| L2 Cache | 中 | GM 读写的缺省缓存，按 Cache Line 加载（128/256/512B） | 搬运单元 |
| L1 Buffer | 近 | 喂 Cube 的分片中转 | MTE 搬运 |
| UB | 最近 | Vector 计算的输入/输出分片 | Vector/Cube |
| L0A/L0B/L0C | 最近 | Cube 矩阵输入/输出 | Cube |

「谁在用」这列其实对应到几个**物理搬运单元**：MTE1（L1→L0A/L0B）、MTE2（GM→{L1, L0A/B}、GM→UB）、MTE3（UB→GM、L1→GM）、FixPipe（L0C→{GM/L1}，可随路做格式/类型转换）[^mte]。想「搬得快」的第一步，就是看清你的数据该由哪个单元搬、要不要经过 L1 中转。

以矩阵计算（Cube）为例，数据流长这样[^mte]：

```
GM → L1 → L0A/L0B → Cube → L0C → FixPipe → GM   （一次算完回 GM）
GM → L1 → L0A/L0B → Cube → L0C → FixPipe → L1 → GM  （中间结果回 L1 继续）
```

注意到没有——**L1 是 Cube 的「粮仓」**，矩阵数据先经 MTE2 进 L1，再经 MTE1 进 L0A/L0B 喂 Cube。所以一个矩阵算子效率高不高，往往看 L1 利用率，而不只看 GM 带宽。

这里有个关键设计：**所有经搬运单元读写 GM 的数据都缺省被 L2Cache 缓存**，按 Cache Line 加载，Cache Line 大小视硬件规格（128/256/512 Byte 不等）[^memlay]。这解释了为什么「对齐」如此重要——如果数据没对齐到 Cache Line，一次加载可能多搬半条线，白耗带宽。

### 8.1.1 API 层的分配：`aclrtMalloc` 三兄弟

在 Host 侧，程序员用 ACL 接口向 runtime 要 GPU 内存。第4章你见过 `aclrtMalloc`，这里补全它的「家族」[^aclmem]：

- `aclrtMalloc(ptr, size, policy)`：最常用，`policy` 决定分配策略。
- `aclrtMallocAlign32(ptr, size, policy)`：**32 字节对齐**版本——专为满足搬运对齐要求而设。
- `aclrtMallocCached(ptr, size, policy)`：带缓存属性的分配。
- `aclrtMallocWithCfg / aclrtMallocForTaskScheduler`：进阶配置（大页、任务调度器专用）。

`policy` 的可选项直击「要不要大页」：`ACL_MEM_MALLOC_HUGE_FIRST`（优先大页）、`ACL_MEM_MALLOC_HUGE_ONLY`（只用大页）、`ACL_MEM_MALLOC_NORMAL_ONLY`（只用普通页）[^aclmem]。大页能减少 TLB 缺页、提升大块搬运效率；所以「要性能就用大页」不是玄学，是分配策略层面的选择。

::: tip 内存分配三问
**要大块、要高带宽 → 优先 HUGE_FIRST；要 32B 对齐 → 用 MallocAlign32；常被复用的小缓冲 → 用 MallocCached。** 别一上来裸用 `aclrtMalloc` 不管策略——这一步就决定了你后面搬运的效率。
:::

## 8.2 N-DMA：把「搬 + 变」一步做完

第1章我们说数据搬运走 DMA。这一章的主角是它的升级版：**NDDMA（N-Dimensional DMA，多维直接内存访问）**。一句话定义：能在搬运过程中**硬件自动完成 Padding / Transpose / Broadcast / Slice 等变换**，一次 API 调用完成原来几十行循环的活[^nddma]。

### 8.2.1 一维 DataCopy vs 多维 N-DMA

传统 `DataCopy` 是**一维连续搬运**——搬完想变换，还得自己写循环算地址。NDDMA 是**硬件加速的多维变换**。对比一下[^nddma]：

| 对比项 | 一维 DataCopy | NDDMA |
|---|---|---|
| 支持维度 | 只能一维连续 | 最高 6 维（API 约束 dim∈[1,5]） |
| 数据变换 | 搬完软件循环处理 | 搬运 + 变换一步完成 |
| 代码量 | 多层循环算地址 | 配参数，一次调用 |
| 性能 | 软件循环开销大 | 硬件自动处理，3~5 倍 |

它的核心思想极其简单，一句话：**不同变换 = 对「步长（Stride）」的不同配置**。转置=交换源/目的步长；广播=被广播维的源步长设 0（重复读同一位置）；切片=源长度设成切片大小；Padding=配置左右 padding。记不住套路没关系，记住这个「步长即变换」的指针就抓住了灵魂。

### 8.2.2 一个 Padding 例子：参数怎么配

以官方样例 `data_copy_gm2ub_nddma` 的场景 1（Padding）为例。输入 `[16, 32]` 矩阵四周填 0，输出 `[32, 64]`[^nddma2]：

```cpp
// [示意代码] 场景1：Padding，输入[16,32] → 输出[32,64]（四周填0）
AscendC::NdDmaLoopInfo<2> loopInfo{
    {1, 32},   // 每个维度的源步长
    {1, 64},   // 目的维步长
    {32, 16},  // 源数据总长度
    {15, 13},  // 左/上 padding
    {17, 3}    // 右/下 padding
};
AscendC::NdDmaParams<float, 2> params{loopInfo, 0};  // padding 值 0
AscendC::DataCopy<float, 2>(xLocal, xGm, params);
```

`NdDmaLoopInfo<dim>` 的 5 组参数是 N-DMA 的「调参面板」：`loopSrcStride`（源步长）、`loopDstStride`（目的步长）、`loopSize`（每维长度）、`loopLpSize`（左/上 padding）、`loopRpSize`（右/下 padding）。模板参数 `dim` 是维度，取值 **[1,5]**；`NdDmaParams` 还有一个 `constantValue`，是不使能最近邻填充时的 padding 常数[^nddma3]。

再看**转置（Transpose）**——这是 N-DMA 最能省心、也最能体现「步长即变换」的场景[^nddma2]：

```cpp
// [示意代码] 场景3：转置，输入[16,64] → 输出[64,16]（关键：交换源/目的 stride）
AscendC::NdDmaLoopInfo<2> loopInfo{{1, 64}, {16, 1}, {64, 16}, {0, 0}, {0, 0}};
AscendC::NdDmaParams<float, 2> params{loopInfo, 0};
AscendC::DataCopy<float, 2>(xLocal, xGm, params);
```

你要做的只是把 `loopSrcStride` 和 `loopDstStride` **对调**（`{1,64}` 与 `{16,1}`），硬件自动按转置后的步长读数据。换成手动写，得算出每个元素的偏移、再逐个搬——又长又易错，这就是 N-DMA 的意义所在。

再看**最近邻填充（Nearest Padding）**，它跟「填0」的区别只在一处配置——`NdDmaConfig` 的 `isNearestValueMode=true`，padding 区域会取边界值而不是 0[^nddma2]：

```cpp
// [示意代码] 场景2：最近邻填充，填充区取边界值
static constexpr AscendC::NdDmaConfig dmaConfig = {true};  // 开启最近邻填充
AscendC::DataCopy<float, 2, dmaConfig>(xLocal, xGm, params);
```

### 8.2.3 五种场景速查

记一张「变换 → 关键配置」对照表，用的时候照着配[^nddma2]：

| 场景 | 关键配置 |
|---|---|
| Padding（填常数） | `NdDmaParams` 的 `constantValue`；`isNearestValueMode=false` |
| Padding（最近邻） | `NdDmaConfig.isNearestValueMode=true` |
| Transpose 转置 | **交换**源/目的 stride |
| Broadcast 广播 | 被广播维的源 stride 设为 0 |
| Slice 切片 | 源长度设为切片大小 |

::: tip N-DMA 一句话
**「步长即变换」：转置换 stride、广播置 0、切片改长度、Padding 配左右。** 凡能交给 N-DMA 的变换就别写软件循环——这是算子性能的第一条金律。
:::

## 8.3 对齐、带宽与乒乓

N-DMA 和 DataCopy 都有**对齐要求**：不同数据类型不同，`float` 建议对齐到 **32 字节**；`b64` 类型有额外限制（如 `isNearestValueMode` 必须为 false、`constantValue` 必须为 0）[^nddma3]。为什么？回顾 8.1——L2Cache 按 Cache Line（128/256/512B）加载，GM 读写的**最小单位是 Cache Line**。数据不对齐，一次搬运要跨两三个 Cache Line，白搬一遍。

### 8.3.1 乒乓（Ping-Pong）：让「搬运」和「计算」重叠

算子内部，把「搬一块算一块」改成「搬两块、算一块、搬下一块」的**乒乓**策略，是隐藏搬运延迟的经典手段。它的价值一句话讲清：**CPU / 搬运单元和 Vector/Cube 是并行的两个引擎**，乒乓让它们同时忙——搬运在搬第 i+1 块时，计算在算第 i 块[^pong]。配多级队列（`TPipe::InitBuffer` 深一点）就是给乒乓预留缓冲。

### 8.3.2 带宽利用的本质

「充分利用带宽」说到底就是三件事：**数据连续**（stride 少跳空，缓存命中高）、**访问对齐**（不跨 Cache Line）、**单次搬运够大**（别把大搬运拆成几十次小 DMA，启动开销会吃掉收益）。这也是 N-DMA 的价值——它把多次小变换合并成一次大搬运[^nddma]。

## 8.4 零拷贝路径与算子间数据复用

「搬运」还有个更彻底的解法：**能少搬就少搬，最好不搬**。零拷贝路径指的是让数据在**不同算子 / 不同设备间共享**时，避免「搬出来 → 拷走 → 再搬进去」的重复拷贝。

- **片内**：UB 里算完的结果直接留在片内，供下一个算子用（`copy_ub2ub` 类搬运），别倒腾回 GM 再拿回来。
- **跨设备 / 跨主机**：这是第5章说的 `tprt` 与第2章 HCCS / 灵衢 URMA 的用武之地——**one-sided 零拷贝**，让对端直接读你的内存，而不是双端来回拷[^zerocopy]。

一句话：**数据复用是把「搬运次数」降下来的第一杠杆**。同一次搬运能喂多家就喂一家，能留片内就别回 GM。

## 8.5 AIPP 与预处理（片上的「免费变换」）

说到数据通路，AIPP（AI PreProcessing）值得一提[^aipp]：它把**图像预处理**（缩放、裁剪、色度转换、归一化等）下沉到**硬件 / DMA 随路**，而不是让 CPU 或 DSA 算子去算。对图像输入场景，AIPP 能在搬运的同时把预处理做了，避免单独跑一遍预处理算子——这又是一次「搬 + 算」的合并。启用时机与设备支持有关（不是所有型号都有独立 AIPP 通路），所以标注为「如适用」，需要按你的目标芯片能力菜单确认。

## 8.6 后端衔接：为性能编铺路

走到这，第二编逻辑上就闭环了。数据通路这一章，直接为第三编（算子开发）和性能编（第15、16章）埋了三根线[^next]：

1. **N-DMA 是写算子首先要摸清的工具**——第9章起你写 `DataCopy` / `DataCopyPad`，底层就是它。
2. **对齐与缓存**是性能分析的头号疑犯——第15章做 msprof 画像，若搬运带宽上不去，先查对齐、再查乒乓。
3. **零拷贝与数据复用**是 kernel 融合的动机——多算子合并成一个大 kernel，本质就是「多搬几次 vs 少搬一次」的权衡。

所以这一章不是终点，是给「写算子 / 调性能」做准备。

## 陷阱与注意（汇总）

| 坑 | 症状 | 对策 |
|---|---|---|
| 数据不对齐 | 带宽莫名低、性能上不去 | 用 `aclrtMallocAlign32`；确认数据对齐到 Cache Line（8.1、8.3） |
| 用一维 DataCopy 硬编变换 | 代码又长又慢 | 换成 N-DMA，交给硬件做变换（8.2） |
| N-DMA 参数配错 | 变换结果不对或搬错区 | 记住「步长即变换」，按 8.2.3 表配；维度别超 [1,5]（8.2.2） |
| N-DMA 后马上读 | 读到脏数据 | 搬运后要等完成/刷新 cache（`NdDmaDci`），再操作（8.2、8.3） |
| 搬运拆得太碎 | 启动开销吃掉收益 | 合并小搬运成一次大 N-DMA；用乒乓隐藏延迟（8.3） |
| 重复拷贝 | 内存带宽被白耗 | 能留片内留片内、能零拷贝就零拷贝（8.4） |
| 把 N-DMA 当全型号可用 | 在旧型号上行为怪 | 先查能力菜单；NDDMA 仅较新芯片支持（8.2、STYLEGUIDE §8） |

## 本章小结

::: tip 一句话总结
**内存层级（GM→L2→L1→UB）决定了「搬」要付费；NDDMA 用「步长即变换」把搬 + 变一步做完，是算子数据通路的主角；对齐（32B / Cache Line）、乒乓（搬算重叠）、零拷贝（少搬）是压低搬运开销的三板斧；AIPP 把预处理随路做掉。数据通路是第三编写算子与第15章性能分析的地基。**
:::

## 本章来源与进一步阅读

[^memlay]: 内存层级与搬运单元（Local/Global Memory、L1/L0/UB、L2Cache 按 Cache Line 加载 128/256/512B、MTE1/MTE2/MTE3/FixPipe、Regbase/Membase 架构差异）：`asc-devkit/docs/zh/guide/programming_guide/{programming_model/ai_core_simd_programming/abstract_hardware_architecture.md,advanced_programming/hardware_implementation/basic_architecture.md}`。
[^mte]: 搬运单元分工与 Cube 数据流（MTE1: L1→L0A/L0B、L1→BT；MTE2: GM→{L1,L0A/B}（分形、Cache Line 对齐）/GM→UB（Cache Line）；MTE3: UB→GM、L1→GM；FixPipe: L0C→{GM/L1}、L1→FP，随路格式/类型转换）：`asc-devkit/docs/zh/guide/programming_guide/advanced_programming/hardware_implementation/basic_architecture.md`。
[^aclmem]: 内存分配 API 与策略：`runtime/include/external/acl/acl_rt.h`（`aclrtMalloc` / `aclrtMallocAlign32` / `aclrtMallocCached` / `aclrtMallocWithCfg` / `aclrtMallocForTaskScheduler`；`aclrtMemMallocPolicy`：`ACL_MEM_MALLOC_HUGE_FIRST / HUGE_ONLY / NORMAL_ONLY`）。
[^nddma]: NDDMA 定义与对比（多维搬运 vs 一维 DataCopy、性能 3~5 倍、支持 Atlas 350 及后续）：`cann-learning-hub/blogs/operator/nddma_introduction/深入理解NDDMA多维数据搬运-昇腾算子开发性能优化利器.md`。
[^nddma2]: NDDMA 五场景与官方样例：同上前文 + `asc-devkit/examples/01_simd_cpp_api/03_basic_api/00_data_movement/data_copy_gm2ub_nddma/`（Padding / Nearest / Transpose / Broadcast / Slice 的参数配置）。
[^nddma3]: NDDMA 参数语义与对齐限制（`NdDmaLoopInfo<dim>` 的 srcStride/dstStride/loopSize/lpSize/rpSize，dim∈[1,5]；`NdDmaConfig` 的 `isNearestValueMode`/`loopLpSize`/`loopRpSize`(<256)/`unsetPad=0xffff`/`ascOptimize` 预留；b64 需 isNearestValueMode=false、constantValue=0；float 建议 32B 对齐）：`asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/DataCopy_GMToUB_NDDMA.md`。
[^pong]: 乒乓与多级队列（`TPipe::InitBuffer`）、搬算重叠：`asc-devkit/examples/01_simd_cpp_api/03_basic_api/00_data_movement/`、`asc-devkit/docs/zh/api/SIMD-API/`（DataCopy 系列）。
[^zerocopy]: 零拷贝 / one-sided 与跨设备传输：`runtime/src/tprt/`（传输运行层）、`runtime/src/runtime/core/src/device/`；跨设备零拷贝语义见第2章 HCCS / 灵衢 URMA（one-sided）。
[^aipp]: AIPP 预处理随路：`asc-devkit/docs/zh/guide/programming_guide/`（图像预处理相关章节）。
[^next]: 为第三编与第15章铺路（N-DMA/对齐/乒乓/零拷贝 → 算子开发与性能画像）：`asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/`、`cann-learning-hub/blogs/operator/nddma_introduction/`。
- 继续读：第9章起 Ascend C（`asc-devkit/examples/01_simd_cpp_api/`）、第15章性能分析（`runtime/src/dfx/msprof/`、第8章对齐/带宽/乒乓三大斧）。
