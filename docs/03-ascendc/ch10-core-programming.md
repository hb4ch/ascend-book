---
title: 第10章 核心编程能力详解
description: TPipe/TQue 范式与队列同步、Tensor 体系（Global/Local/Reg）、计算 API 家族、搬运 API 与 N-DMA 实操
status: 已成稿（第三编）
---

# 第10章 核心编程能力详解

> 第 9 章选定了入口，这一章把 **Tpipe/Tque 框架层**的工作机制拆开：队列为什么能替你管同步、Tensor 到底封装了什么、计算与搬运 API 家族怎么检索、以及第 8 章预支的 N-DMA 实操债在这里还上。

## 本章目标与阅读指引

- **底层**：理解 TPipe/TQue 的队列管道原理——`EnQue/DeQue`、`AllocTensor/FreeTensor` 两组 API 底下各封了一对什么硬件同步指令（10.1、10.2）。
- **实操**：掌握 Tensor 体系（GlobalTensor/LocalTensor/RegTensor）与基础 API 的自主管理路线（10.3）。
- **实操**：会检索计算 API 家族，会用 Matmul 高阶 API 表达 Cube 流程（10.4）。
- **实操**：读懂 N-DMA 的配置方式（本章详解 Padding/Transpose 两类场景，其余同构），兑现第 8 章的搬运 API 债（10.5）。

**本节要点**：本章锚定「三组配对 API + 一张 TPosition 地图」：`EnQue/DeQue`、`AllocTensor/FreeTensor`、`SetFlag/WaitFlag`。读懂它们，`kernel_operator.h` 里上千个接口就有了检索骨架。

## 10.1 TPipe/TQue：把流水线装进队列

第 9 章的四步法在框架层被固化为标准范式：**CopyIn → Compute → CopyOut 三段式流水**[^paradigm]。它的设计思想是经典的**队列管道（Queue Pipeline）**：任务拆成多个 Stage（阶段），Stage 之间用线程安全队列传递数据，从而「阶段解耦、队列互联」[^principle]。

```mermaid
flowchart TB
    subgraph stages["三个 Stage（每个 AI Core 各跑一份，SPMD）"]
        direction TB
        CI["CopyIn：DataCopy GM→UB(VECIN)＋EnQue"]
        CP["Compute：DeQue→计算→EnQue"]
        CO["CopyOut：DeQue→DataCopy UB(VECOUT)→GM"]
    end
    CI -->|"TQue&lt;VECIN&gt; EnQue/DeQue"| CP
    CP -->|"TQue&lt;VECOUT&gt;"| CO
    TP["TPipe 资源管理器（管内存＋事件）"] -.供给.- stages
```
*图 10-1 三段式流水与两大组件分工：**TPipe 管资源，TQue 管通信**[^principle]。*

下面片段是**教学改写**：结构取自范式文档，类型/数值统一到本章真实 Add 例（`blockLength=2048` 个 `float`），**初始化与循环骨架按范式省略**——先看它，再对照 10.3 真码[^paradigm]：

```cpp
// [需真机验证] 摘自 asc-devkit/docs/zh/guide/programming_guide/programming_model/
//   ai_core_simd_programming/tpipe_tque_programming/tpipe_tque_paradigm.md（官方范式伪代码）
AscendC::TPipe pipe;                                 // 全局资源管理器
AscendC::TQue<AscendC::TPosition::VECIN, 1> queIn;  // CopyIn 阶段队列（头文件枚举全大写；官方范式文档排版作 VecIn）
AscendC::TQue<AscendC::TPosition::VECOUT, 1> queOut; // CopyOut 阶段队列
pipe.InitBuffer(queIn, 2, blockLength * sizeof(float));  // 2=缓冲块数(乒乓)；每块 8KB 装 2048 float
pipe.InitBuffer(queOut, 2, blockLength * sizeof(float)); // 队列深度=模板参数1：连续入队一次
for-loop {
    {   // CopyIn 阶段
        auto tensor = queIn.AllocTensor<float>();    // ① 申请一块（2048 float 容量足够）
        AscendC::DataCopy(tensor, xGm, blockLength); // ② GM → UB 搬 2048 个 float
        queIn.EnQue(tensor);                         // ③ 入队（发同步信号）
    }
    {   // Compute 阶段
        auto tensor = queIn.DeQue<float>();          // ④ 出队（等同步信号）
        auto tensorOut = queOut.AllocTensor<float>();
        AscendC::Abs(tensorOut, tensor, blockLength); // ⑤ 计算（范式原文 Abs 例；单位已与 Add 例统一）
        queIn.FreeTensor(tensor);                    // ⑥ 释放输入内存
        queOut.EnQue(tensorOut);
    }
    {   // CopyOut 阶段
        auto tensor = queOut.DeQue<float>();
        AscendC::DataCopy(zGm, tensor, blockLength); // ⑦ UB → GM 搬回 2048 float
        queOut.FreeTensor(tensor);
    }
}
```

把这段伪码按**数据生命周期**走一遍，比记 API 更重要——输入 x 与输出 z 走的是**两条独立的生命周期**：

- **输入缓冲（x）**：`AllocTensor`（从 queIn 取一块，底层 `Wait` 等该块旧数据所有读完成）→ `DataCopy` 搬入 → `EnQue`（底层 `Set`，宣告写完）→ Compute 侧 `DeQue`（`Wait` 到写完信号）→ 参与计算 → `FreeTensor`（`Set`，宣告可覆写）——之后这块缓冲即可被再次 `Alloc`，循环复用[^principle]。
- **输出缓冲（z）**：另一次 `AllocTensor`（来自 queOut，与 x 互不相干）→ 写入结果 → `EnQue`/`DeQue`/搬出后 `Free`。**切勿把「输入缓冲直接 EnQue 进输出队列」**——x 与 z 是两个队列里的两块不同内存。

在此基础上再看两个容易看漏的参数，**它们是两件事**：

| 参数 | 含义 | 与乒乓的关系 |
|---|---|---|
| `InitBuffer` 的 **num**（例中 2） | 该队列挂**几块缓冲**；num=2 即第 8 章的**乒乓（Double Buffer）**——CopyIn 搬第 1 块时 Compute 可算第 0 块[^paradigm] | **num 才是缓冲数** |
| `TQue<TPosition, depth>` 的 **depth**（模板参数） | **连续 EnQue 的次数**（中间无 DeQue）——与 double buffer 无关，深度 1 也可开乒乓；非原地场景深度 1 有编译器优化、官方推荐 1[^queuedep] | 不是缓冲数 |

交叠能否发生，还取决于数据依赖、调度与资源——时序表（下）只是示意，不承诺实测重叠。**临时变量用 TBuf**：不参与队列流转的中间空间用 `TBuf` 申请，只能算、不能 EnQue/DeQue，生命周期更简单[^paradigm]。

满足依赖与资源条件时，多个分片可以形成下面的交叠时序——同一分片按依赖先后执行，不同分片可能重叠[^paradigm]：

| 时刻 → | t0 | t1 | t2 | t3 |
|---|---|---|---|---|
| **CopyIn** | 分片 0 | 分片 1 | 分片 2 | … |
| **Compute** | （等分片 0） | 分片 0 | 分片 1 | … |
| **CopyOut** | （等分片 0） | （等分片 0） | 分片 0 | … |

*表 10-1 双缓冲流水时序**示意**：同一分片串行（依赖合法）、不同分片并行依赖调度与资源，是否满负荷交叠以实机为准；「乒乓」来自 num=2，与队列深度无关*

## 10.2 同步语义：两组 API 底下的 Set/Wait

异步并行的核心难点是数据依赖。Ascend C 把依赖归成两类，各给一组配对 API；**原理文档以底层 `Set`/`Wait` 硬件同步指令解释其语义**（具体每条 API 在各优化配置下的指令生成以实现为准）[^principle]：

```mermaid
flowchart TB
    subgraph raw["先写后读 RAW（数据就绪）：EnQue / DeQue"]
        direction TB
        E1["EnQue（生产者收尾）：Set 标记写完、唤醒下游"]
        W1["DeQue（消费者起始）：Wait 阻塞至收到 Set"]
        E1 --> W1
    end
    subgraph war["先读后写 WAR（内存复用）：AllocTensor / FreeTensor"]
        direction TB
        A1["AllocTensor（申请）：Wait 等此块所有读完成"]
        F1["FreeTensor（释放）：Set 通知可安全覆写"]
        A1 --> F1
    end
    W1 ~~~ A1
```
*图 10-2 两类数据依赖与两组成对 API：原理层以 Set/Wait 解释二者语义；实际指令生成随优化配置，以实现为准[^principle]。*

这解释了 10.1 范式代码的纪律：**`AllocTensor`/`EnQue`/`DeQue`/`FreeTensor` 一个都不能少、顺序不能乱**——漏一个 `FreeTensor` 不只是泄漏，而是内存复用信号丢失；漏一个 `EnQue` 则下游永远等不到「写完」信号。

框架层之外还有**手工同步层**，即 `SetFlag/WaitFlag`。真实样例（N-DMA 回传场景）的 `Process()` 实际行序是：先 `CopyIn`（内部 DataCopy GM→UB，MTE2 单元），**随后** `SetFlag`（发起完成标记）、`WaitFlag`（阻塞至 MTE2 真正完成），之后才发起 UB→GM 的搬出（MTE3 单元）——「先 Set 后 Wait 紧邻」不是无意义并列，而是**发起与确认**一对动作[^nddma]：

```cpp
// [需真机验证] 摘自 asc-devkit/examples/01_simd_cpp_api/03_basic_api/00_data_movement/
//   data_copy_gm2ub_nddma/multidimensional_data_movement.asc
// MTE2 -> MTE3 同步：确保 GM 数据搬运到 UB 后，才能将 UB 上的数据搬运到 GM
AscendC::SetFlag<AscendC::HardEvent::MTE2_MTE3>(EVENT_ID0);  // 发起：MTE2 搬入完成标记
AscendC::WaitFlag<AscendC::HardEvent::MTE2_MTE3>(EVENT_ID0); // 确认：阻塞至 MTE2 完成
AscendC::DataCopy(yGm, xLocal, dstTotalLength);              // 之后才放行 MTE3 搬出
```

`HardEvent::MTE2_MTE3` 直译就是「等 MTE2（搬入单元）的活干完，再放行 MTE3（搬出单元）」——第 2 章的搬运单元分工在这里变成了同步事件的粒度。按同步范围，官方把全部同步接口分成三类[^syncdoc]：

| 类别 | 代表接口 | 用途 |
|---|---|---|
| 核内同步 | `SetFlag/WaitFlag`、`PipeBarrier`、`DataSyncBarrier`、`Lock/Unlock` | 同核多流水之间（如 MTE 与 Vector）的时序 |
| 核间同步 | `CrossCoreSetFlag/WaitFlag`、`SyncAll`、`IBSet/IBWait` | 多个 AIC/AIV 之间的协同（如全核汇总） |
| 任务间同步 | `SetNextTaskStart`、`WaitPreTaskEnd` | SuperKernel 子核函数间的流水重叠 |

多核协作类算子（如需要全核汇总再继续的场景）会用到第二行，第 11 章写 SIMT 多线程协作时再展开；本章先记住：**队列托管的是其事件能表达的依赖**（生产/消费就绪、缓冲复用）；**队列之外的依赖——如同节手工例的「搬入→搬出」跨流水——仍须手工接口**。一套 API 够不够，按具体依赖判断，不按「常规/非标准」贴标签。另有一个解除方向的接口：当**产品在同 TPosition 上的 Buffer/队列配额用尽**（TQue 对象数与 Buffer 数是两本账，上限按产品×同 TPosition 计）时，对**已使用完毕**的队列调 `FreeAllEvent` 释放其全部事件，方可再申请新队列——它是「清账」手段，不是 `FreeTensor` 那样的逐块释放[^queuedep]。

## 10.3 Tensor 体系：从地址到对象

Tensor 的本质是**基于数组的编程抽象**：把原始内存地址封装成对象，从「地址操作」升到「对象管理」[^tensor]。按所在存储层级分三类：

```mermaid
flowchart LR
    GM["GM 全局内存<br/>容量大 · 延迟长<br/>aclrtMalloc 分配(第4章)"] --- GT["GlobalTensor"]
    UB["片上缓冲<br/>UB / L1 / L0A/L0B/L0C<br/>TPipe·AllocTensor 分配"] --- LT["LocalTensor"]
    REG["寄存器<br/>Reg 面接口的数据载体（950 起显式可编程）"] --- RT["RegTensor"]
```
*图 10-3 三类 Tensor 与**所讨论 Vector 接口的数据载体**对应——**不是把芯片存储整体划成三级**；寄存器一直存在，950 起 Reg 面接口才将其显式暴露为可编程载体（此前 Vector 计算经 UB）[^tensor]。RegTensor/MaskReg 与 `reg_data_load`/`reg_data_store` 属 9.1「Reg 编程面」，详见第 11 章[^regapi]。*

**基础 Tensor 与扩展 Tensor 的分野**是本节最重要的增量信息[^tensor]：

- **基础 Tensor**（不带 Layout）只封装指针和大小：搬运、计算都要**手动传 size/count**、自己算偏移步长。`AscendC::Add(zLocal, xLocal, yLocal, blockLength)` 里的 `blockLength` 就是这笔手工账。
- **扩展 Tensor（Tensor API）**额外封装 **Shape 和 Stride**：接口自动推导搬运长度、计算元素数，一行 `AscendC::Te::Copy(l1ATensor, gmATensor)` 完成搬运，且获得编译期类型安全。当前能力先赋能 **Cube 矩阵计算**（接口统一走 `AscendC::Te` 命名空间），Vector 侧后续演进[^tensor]。

一句话：**Layout 进 Tensor，参数账就进了编译期**——这与第 8 章「步长即变换」是同一件事在类型系统上的投影：stride 不再是你手算的数字，而是对象携带的、可被编译器检查的属性。

自主管理路线（第 9 章「基础 API」）的真实 Add 样例[^pairadd]——**不建 `TPipe`，同步自己插**，依赖一点不少：

```cpp
// [需真机验证] 摘自 asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/add/add.asc
// （语义未改动；blockLength 为模板常量 2048，本书未编译）
template <uint32_t blockLength>
__vector__ __global__ void add_custom(__gm__ float* x, __gm__ float* y, __gm__ float* z) {
    AscendC::InitSocState();
    AscendC::GlobalTensor<float> xGm, yGm, zGm;               // 各核只看自己的分片
    xGm.SetGlobalBuffer(x + block_idx * blockLength, blockLength);
    // …… yGm/zGm 同式……
    AscendC::LocalMemAllocator<AscendC::Hardware::UB> ubAllocator;
    AscendC::LocalTensor<float> xLocal = ubAllocator.Alloc<float, blockLength>();
    AscendC::LocalTensor<float> yLocal = ubAllocator.Alloc<float, blockLength>();
    AscendC::LocalTensor<float> zLocal = ubAllocator.Alloc<float, blockLength>();

    AscendC::DataCopy(xLocal, xGm, blockLength);   // 手动传 size
    AscendC::DataCopy(yLocal, yGm, blockLength);
    AscendC::PipeBarrier<PIPE_ALL>();              // 同步①：搬入完成，才可计算
    AscendC::Add(zLocal, xLocal, yLocal, blockLength);
    AscendC::PipeBarrier<PIPE_ALL>();              // 同步②：计算完成，才可搬出
    AscendC::DataCopy(zGm, zLocal, blockLength);
    AscendC::PipeBarrier<PIPE_ALL>();              // 原样例在写回后也保留屏障
}
```

对比 10.1 的框架路线：**少了队列（同步自己插 `PipeBarrier`），少了 TPipe（自己分配/释放）**——注意样例在每段之间**显式插了屏障**：直接照抄「无同步版」会读到大搬家未完的错序数据。换来的控制权正是第 9 章决策树里「极致性能 + C++ Tensor」路径的底气。仓库里两种路线的成对样例：`examples/01_simd_cpp_api/00_introduction/01_add/{add_tpipe_tque, add}/`[^pairadd]。

## 10.4 计算 API 家族与 Matmul 高阶 API

基础 API 的计算接口按功能归档在 `docs/zh/api/SIMD-API/basic_api/memory_vector_compute/` 下，检索先看目录树[^apitree]：基本算术（`basic_arithmetic`）、规约（`reduction_compute`）、类型转换（`type_conversion`）、比较选择、逻辑计算、掩码、排序合并、scatter/gather、数据布局转换、`data_move`（搬运，10.5 详述）等。矩阵侧另有 `cube_compute_TensorAPI` 等。全部接口在 `include/kernel_operator.h` 汇总出口[^apitree]。

**Cube 路线直接给了高阶封装**——`Matmul` 对象把 CopyIn/Compute/CopyOut 三段压成三个调用[^paradigm]：

```cpp
// [需真机验证] 摘自 tpipe_tque_paradigm.md 矩阵编程范式（Matmul 高阶 API）
typedef MatmulType<TPosition::GM, CubeFormat::ND, half> aType;   // 位置/格式/类型
typedef MatmulType<TPosition::GM, CubeFormat::ND, half> bType;
typedef MatmulType<TPosition::GM, CubeFormat::ND, float> cType;
typedef MatmulType<TPosition::GM, CubeFormat::ND, float> biasType;
Matmul<aType, bType, cType, biasType> mm;
REGIST_MATMUL_OBJ(&pipe, GetSysWorkSpacePtr(), mm, &tiling);      // 初始化（tiling 进来）
mm.SetTensorA(gm_a);  mm.SetTensorB(gm_b);  mm.SetBias(gm_bias);  // CopyIn
while (mm.Iterate()) {                                            // Compute（逐基块迭代）
    mm.GetTensorC(gm_c);                                          // CopyOut
}
mm.End();
```

注意 `REGIST_MATMUL_OBJ(..., &tiling)`——**第 9 章 9.4 说的「host 算 tiling、device 用 tiling」在这里兑现**：tiling 结构体一路传进 Matmul 对象，驱动 `Iterate()` 按基块（base block）迭代。矩阵编程的 TPosition 地图也在此展开——**逻辑位置到物理 Buffer 的完整映射**如下[^paradigm]，与第 2 章 2.1 的 Cube 数据流完全对上：

| TPosition | 物理对应 | 存什么 |
|---|---|---|
| A1 / B1 | L1 Buffer | 左矩阵 / 右矩阵（整块） |
| C1 | L1 Buffer 或 UB | Bias（偏置） |
| A2 / B2 | L0A / L0B Buffer | 切成小块的左/右矩阵 |
| C2 | BT Buffer 或 L0C | 小块 Bias |
| CO1 | L0C Buffer | 矩乘结果分块 |
| CO2 | GM 或 UB | 最终矩阵计算结果 |
| VECIN / VECCALC / VECOUT | UB | 矢量输入 / 临时变量 / 输出 |

**融合算子**（Vector + Cube 混合）的范式是上述两套的拼接：Cube 输出可作 Vector 输入（CO2→VECIN），Vector 输出也可回喂 Cube（VECOUT→A1→A2）[^paradigm]。注意范式图里这些箭头是**数据流向的资格**，不是「自动接通」：跨 Cube/Vector 流水的衔接仍须队列事件或同步接口，且**各架构、各接口的支持要按产品核对**，不可当全平台硬件连线。第 8 章说「kernel 融合的动机是少搬一次」；范式层的表达是**让数据沿 TPosition 链流转**——但**能否不落 GM 取决于接口/架构/实现**（CO2 本就允许 GM 或 UB），不由 TPosition 命名保证。

## 10.5 搬运 API 与 N-DMA 实操（还第 8 章的债）

搬运接口族谱在 `memory_vector_compute/data_move/`：连续搬运 `DataCopy_GMAndUB_continuous`、高维切分 `highdim_split`、切片 `slice`、填充 `DataCopyPad_GMToUB/UBToGM`、格式转换 `ND2NZ/NZ2ND`、片上 `Copy_UBToUB`，以及主角 **N-DMA（`DataCopy_GMToUB_NDDMA`）**[^datamove]。第 8 章讲透了「步长即变换」的道理，这里看真码怎么写——仓库样例把五个场景做成了编译期开关[^nddma]：

```cpp
// [需真机验证]（仅支持 Ascend 950PR/950DT）摘自
//   asc-devkit/examples/01_simd_cpp_api/03_basic_api/00_data_movement/data_copy_gm2ub_nddma/
//   multidimensional_data_movement.asc
// 场景1：2D Padding——xGm [16,32] 搬入后变 xLocal [32,64]，四周填 0
AscendC::Duplicate<T>(xLocal, 0, dstTotalLength);           // 先把目标区填 0
AscendC::NdDmaLoopInfo<2> loopInfo{{1, 32}, {1, 64}, {32, 16}, {15, 13}, {17, 3}};
//  五个字段依次是（按维度给出）：
//  loopSrcStride={1,32}   源行距 32：xGm 每行 32 个元素
//  loopDstStride={1,64}   目标行距 64：xLocal 每行 64 个元素
//  loopSize={32,16}       每维搬运的元素数（不含 Padding）
//  loopLpSize/RpSize={15,13}/{17,3}  各维左/右 Padding 个数
AscendC::NdDmaParams<T, 2> params{loopInfo, 0};             // padding 值 = 0
AscendC::NdDmaDci();                                        // 刷新 cache
static constexpr AscendC::NdDmaConfig dmaConfig;            // 默认参数（也可不传）
AscendC::DataCopy<T, 2, dmaConfig>(xLocal, xGm, params);    // 一次搬运完成搬+变
```

```cpp
// 场景3：2D Transpose——xGm [16,64] 搬成 xLocal [64,16]（新作用域，重新定义 loopInfo）
AscendC::NdDmaLoopInfo<2> loopInfo{{1, 64}, {16, 1}, {64, 16}, {0, 0}, {0, 0}};
//  srcStride={1,64}：源按行存放，第 1 维行距 64
//  dstStride={16,1}：目标第 0 维步长 16——源元素 (i,j) 落到目标下标 j*16+i，行列换位即转置
//  搬运调用同场景 1：DataCopy<T, 2, dmaConfig>(xLocal, xGm, params)
```

对照第 8 章 8.2 的口诀逐项验收：**Padding 配左右**（loopLpSize/loopRpSize）、**转置换 stride**（场景 3 的 loopDstStride 从 1 改 16）、**广播置 0**（场景 4 的 loopSrcStride 置 0——源行距为零，同一行被反复读取）、**切片改长度**（场景 5 的 loopSize 只取子块）——四个变换全是 loopInfo 里几个数字的事。样例里还有两个**该样例语境下**的步骤：搬入前 `Duplicate` 清零（此处保留原样例操作，不据此推导padding必须预先清零）与 `NdDmaDci()` 刷新 cache（具体缓存作用域与要求以接口文档为准）——二者是本样例的选择，**不是一切 N-DMA 通用纪律，也不是缓存一致性的通用保证**；搬入→搬出间依赖见 10.2 的 Set/Wait[^nddma]。

样例 README 明确标注 N-DMA **仅支持 Ascend 950PR/950DT**[^nddma]——第 8 章「需能力菜单确认」的钩子在此落地：**旧型号上这段代码不是慢，是没有**。迁移前先查第 2 章 2.5 的能力菜单与 `--npu-arch` 对应关系（dav-3510 才有）。

### 10.5.1 实战第一坑：非对齐尾部与 DataCopyPad

N-DMA 之外，**最常遇到的是非 32B 对齐的搬运**——真实张量的最后一行往往不整齐。专用接口是 `DataCopyPad`：blockLen 非 32 字节对齐时，每个数据块都会被填充至 32B 对齐[^pad]：

- **填什么**：`isPad=true` 用 `paddingValue`；不配置时硬件自动在**每块右侧**填 dummy；也可用 `SetPadValue` 接口外部配置；
- **填多少**：`leftPadding/rightPadding` 按元素个数指定，**两侧都不能超过 32 字节**；
- **Compact 模式**（仅 950PR/950DT）：不逐块补齐，把所有块拼成一条连续块、只在**整块末尾**补齐——省掉中间的填充开销[^pad]。

还有一个更隐蔽的前置坑：**连续搬重载 `DataCopy(dst, src, count)` 的 `count*sizeof(T)` 须 32B 对齐，未对齐时搬运量向下取整到 32B**——尾块会被静默截断（该语义以所核连续 count 重载及其目标产品文档为准，不外推其他搬运接口）[^pad2]。所以动手前先看长度能否整除 32B：能则 `DataCopy`，不能则 `DataCopyPad`，块内变换交给 N-DMA——三者各管一段，覆盖 GM↔UB 通路的日常场景。

## 陷阱与注意（汇总）

| 坑 | 症状 | 对策 |
|---|---|---|
| 漏 `FreeTensor` | UB 耗尽、后续 `AllocTensor` 卡死 | 四个队列操作配对写齐；Free 是复用信号不是「析构」（10.2） |
| 把队列深度当缓冲数 | 深度设大却没开乒乓，或反之 | **num=缓冲块数（=2 开乒乓）；depth=连续 EnQue 次数**，两者独立；交叠取决于依赖/调度/资源（10.1） |
| 连续搬运尾块被截断 | `DataCopy(dst,src,count)` 结果少一截 | `count*sizeof(T)` 未达 32B 向下取整；先整除判断，否则 DataCopyPad（10.5.1） |
| TBuf 上的内存拿去 EnQue | 编译报错 | TBuf 只参与计算，队列内存必须走 TQue（10.1） |
| 依赖没人管 | 搬算错序、读到半截数据 | 先列全依赖：队列事件管的交给队列；跨流水等未覆盖依赖用手工接口；混用前核对事件语义（10.2） |
| 高维变换手写循环 | 正确性易错、代码冗长 | 优先核对 N-DMA/Pad 是否覆盖该变换；性能与适用性按场景实测，本书未测（10.5、第8章） |
| 在 A2/A3 上编译 N-DMA 样例 | 不支持 | N-DMA 仅 dav-3510（950PR/950DT）；先查能力菜单（10.5） |
| Cube 结果直接当 Vector 输入 | 没走 TPosition 链、数据不知在哪 | 按 CO1→CO2→VECIN 流转，或用融合范式封装（10.4） |

## 本章小结

::: tip 本章小结
先沿一块缓冲追踪数据：谁写入、谁读取、何时允许复用。队列用就绪事件和复用事件表达这些依赖；没有被队列覆盖的依赖，仍需相应同步接口。

`InitBuffer` 的 num 决定缓冲块数，TQue 的 depth 表示连续入队所需的深度。选搬运接口时，再分别核对长度、地址对齐、布局和产品支持。
:::

```mermaid
flowchart TB
    AL["AllocTensor<br/>Wait：等此块读毕可覆写"] --> CP["CopyIn<br/>DataCopy GM→UB 写入"]
    CP --> EQ["EnQue<br/>Set：宣告写毕唤醒下游"]
    EQ --> DQ["DeQue<br/>Wait：阻塞至写毕"]
    DQ --> USE["Compute<br/>Add 读取此块"]
    USE --> FR["FreeTensor<br/>Set：宣告可覆写"]
    FR -.同一块缓冲循环复用.-> AL
```
*图 10-4 **一块输入缓冲（x）的生命周期**：实线为一次流转，虚线为复用回流；各环节标注底层 Set/Wait 语义（RAW 与复用 WAR 两类依赖分别落在 EnQue/DeQue 与 Alloc/Free 上）。本图**仅用于输入链**：输出 z 是另一缓冲、另一队列——它被写入后 CopyOut，不 CopyIn、不被 Add 读取，不走本图。*

本章四个落点收束：流水（10.1）、同步（10.2）、数据（10.3/10.4）、搬运（10.5）——下一步向语言扩展层下潜（第 11 章）。

## 本章来源与进一步阅读

[^paradigm]: TPipe/TQue 编程范式（三段式流水、矢量/矩阵/融合三范式、InitBuffer 双缓冲、TBuf、TPosition 定义 A1/B1/A2/B2/CO1/CO2/VECIN/VECOUT/VECCALC、Matmul 高阶 API 示例）：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/tpipe_tque_programming/tpipe_tque_paradigm.md`（官方文档）。
[^principle]: TPipe-TQue 编程原理（队列管道思想、Stage 四步范式、EnQue/DeQue→Set/Wait 解决 RAW、AllocTensor/FreeTensor→Set/Wait 解决 WAR、指令发射异步流水）：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/tpipe_tque_programming/tpipe_tque_principles.md`（官方文档）。
[^tensor]: C++ Tensor 编程概述（Tensor=数组抽象、GlobalTensor/LocalTensor/RegTensor 三类、950 三级层级 GM→UB→Register、基础 vs 扩展 Tensor/Layout/`AscendC::Te`、LocalMemAllocator 自主管理示例、host 侧 aclrtMalloc/`<<<>>>` 全流程）：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/cpp_tensor_programming/cpp_tensor_programming_overview.md`（官方文档）。
[^apitree]: 计算 API 家族归档与汇总出口：`asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/`（子目录 basic_arithmetic/reduction_compute/type_conversion/scatter_gather/data_move 等）、`asc-devkit/docs/zh/api/SIMD-API/basic_api/basic_api_list.md`、`asc-devkit/include/kernel_operator.h`。
[^syncdoc]: 系统同步能力概述（核内 SetFlag/WaitFlag、PipeBarrier、DataSyncBarrier、Lock/Unlock；核间 CrossCoreSetFlag/WaitFlag、SyncAll、IBSet/IBWait；任务间 SetNextTaskStart/WaitPreTaskEnd）：`asc-devkit/docs/zh/api/SIMD-API/basic_api/sync_control/system_sync_overview.md`（官方文档）。
[^nddma]: N-DMA 真码样例（五场景编译期开关、NdDmaLoopInfo/NdDmaParams/NdDmaConfig 参数、NdDmaDci 刷新 cache、MTE2_MTE3 Set/Wait 同步、仅支持 Ascend 950PR/950DT）：`asc-devkit/examples/01_simd_cpp_api/03_basic_api/00_data_movement/data_copy_gm2ub_nddma/multidimensional_data_movement.asc` 及同目录 README（CANN Open 2.0）；参数语义详见 `asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/DataCopy_GMToUB_NDDMA.md`。
[^pairadd]: 两种路线的成对样例（Tpipe/Tque vs 基础 API 自主管理）：`asc-devkit/examples/01_simd_cpp_api/00_introduction/01_add/{add_tpipe_tque/add_tpipe_tque.asc,add/add.asc}`（CANN Open 2.0）。
[^pad]: DataCopyPad 非对齐搬运（blockLen 非 32B 对齐时逐块填充、paddingValue/SetPadValue/dummy 三种填充来源、left/rightPadding ≤32B、Compact 模式仅 950PR/950DT）：`asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/DataCopyPad_GMToUB.md`（官方文档）。
[^queuedep]: 队列深度/缓冲数两义与 FreeAllEvent 前提：`asc-devkit/docs/zh/api/SIMD-API/basic_api/resource_management/TQue/TQue_intro.md`（L29–38 深度定义与「与 double buffer 无关」、L91/138/147 FreeAllEvent 仅限已用完队列）、`asc-devkit/docs/zh/api/SIMD-API/basic_api/resource_management/TPipe/InitBuffer.md`（num=分配块数，2 开 double buffer）（官方文档）。
[^regapi]: Reg 编程面类型与搬入搬出接口：`asc-devkit/docs/zh/guide/programming_guide/programming_model/ai_core_simd_programming/cpp_tensor_programming/reg_vector_computation.md`（官方文档，另见本书 9.1）。
[^pad2]: 连续搬运 count 取整语义：`asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/DataCopy_GMAndUB_continuous.md`（「count * sizeof(T) 需要32字节对齐，若未对齐，搬运量会向下取整到32字节对齐」）（官方文档）。
[^datamove]: 搬运接口族谱（continuous/highdim_split/slice/DataCopyPad/ND2NZ/NZ2ND/UBToUB/NDDMA）：`asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/`（官方文档）。

- **下一站**：第 11 章「SIMD/SIMT 与高级特性」——下潜到语言扩展层：`asc_xxx` 指针路线、`_sync`/`repeat/stride` 接口分级、SIMT 线程模型与核间同步实战。
- **交叉引用**：乒乓与缓冲深度账见第 8 章 8.3；Cube 数据流与 L1/L0 见第 2 章 2.1；启动参数通道与任务 Param 段见第 4 章 4.5、第 5 章 5.2。
