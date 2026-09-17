---
title: 附录B 术语表
description: 全书术语唯一源（由根目录 glossary.md 同步生成，勿手改）
---

# 附录B 术语表

<!-- 自动由 npm run sync:glossary 生成；修改请在仓库根目录 glossary.md -->

# 术语表（glossary）

> 全书术语的**唯一事实源**。中英对照、一义一译、全书统一。`check:terms` 依据本表校验正文高频术语用词一致。
> 本站同步进「附录B 术语表」，构建期自动复制。新增术语→先在此登记→再全书替换。

约定：**加粗**为推荐译法；「不译」表示正文直接使用英文。

## 平台与芯片

| 英文 | 中文 | 说明 / 出处 |
|---|---|---|
| Ascend / 昇腾 | 昇腾 | 华为 AI 处理器品牌 |
| AI Core | AI Core（不译） | 昇腾 AI 处理器的计算单元（昇腾910/950 系列上的 vector+cube 计算核） |
| Cube Core | Cube（不译） | AI Core 内矩阵计算单元（MMAD） |
| Vector Core | Vector（不译） | AI Core 内矢量计算单元（SIMD） |
| Scalar | 标量（不译） | AI Core 内标量/控制单元 |
| AICPU | AICPU（不译） | 昇腾片内通用 CPU 核，承担标量重的算子任务同步逻辑 |
| MTE2 | MTE2（不译） | 内存搬运引擎（数据搬入/搬出团簇） |
| MTE3 | MTE3（不译） | 内存搬运引擎（面向 L2/外存路径） |
| MTE1 | MTE1（不译） | 内存搬运引擎（L1→L0 等核内路径） |
| AIV（AI Vector） | AIV 矢量核 | 昇腾950 代称 AI Vector |
| AIC（AI Core） | AIC 计算核 | 昇腾950 代称 AI Compute |
| GM / HBM | 全局内存 / 高带宽内存 | 片外大容量内存 |
| SMEM | SMEM 共享内存 | 昇腾950 引入的核间共享内存机制 |
| URMA | URMA（不译） | 昇腾950 引入的统一远程内存访问通信机制 |
| 910B / 910C | — | 昇腾910 系列两代，分别对应 Atlas A2/A3 |
| Ascend 950 / 950PR / 950DT | — | 昇腾950 系列（A5 平台）及 950PR/950DT |
| SOC | 片上系统 | 芯片整体 |
| die / multi-die | 芯粒 / 多芯粒 | 950 平台多芯粒封装 |

## 内存与数据

| 英文 | 中文 | 说明 |
|---|---|---|
| GM | 全局内存 | 通常映射 HBM，host 可见地址空间 |
| L1 Buffer | L1 缓冲 | 紧邻 Cube 的高速缓冲 |
| L0A / L0B / L0C | L0A/L0B/L0C | Cube 计算两级输入/一级输出缓冲 |
| UB（Unified Buffer） | 统一缓冲 | Vector 单元的数据缓冲，通常 192KB 上下 |
| L2 | L2 | 片中二级缓存（带 Cache 一致性域） |
| Register | 寄存器 | MTE/Vector 的寄存器文件 |
| Tiling | 分块/切块（tiling 不译更常见，保留英文） | 按片上内存容量拆分大数据块 |
| TilingKey | TilingKey | 运行时动态切块的 key 机制（tilingkey_template_programming 博文） |
| ping-pong | 乒乓 | 双缓冲交替搬运/计算 |
| bank | bank | UB/缓存内部的多体访问 |
| bank conflict | bank 冲突 | 多 bank 同时访问冲突 |
| Address Space | 地址空间 | 950 SIMT 编程中的地址空间抽象 |
| N-DMA | N-DMA | 数据搬移引擎（scalar 侧） |

## 运行与调度

| 英文 | 中文 | 说明 / 出处 |
|---|---|---|
| runtime | 运行时（不译更常见） | CANN 的设备管理/任务调度库 |
| ACL / AscendCL | AscendCL | 华为昇腾计算语言接口层 |
| ACLNN | ACLNN 算子接口 | 基于 Tensor 描述（aclnnTensor）的算子调用接口 |
| aclnn | aclnn | 算子调用运行时（aclnn 系列函数实现） |
| Stream | 流（不译更常见，保留英文） | 算子执行串行化载体 |
| Task | 任务 | 一次可调度执行单元 |
| Event | 事件 | 流间同步原语 |
| Notify | 通知 | 片上同步轻量原语（aclrtCntNotify 等） |
| SQE | SQE（Submission Queue Entry 任务描述符） | 任务描述符，runtime 将任务转成 SQE 提交 |
| TSD | TSD（任务调度模块） | 片上任务调度/执行器，runtime 与设备的通信服务 |
| queue_schedule | 队列调度 | 用户态队列调度模块（BQS） |
| aicpu_sched | AICPU 调度 | AICPU 任务调度模块 |
| Host | Host（不译） | 控制侧（通常是 x86/鲲鹏服务器） |
| Device | Device（不译） | 昇腾设备侧 |
| H2D / D2H / D2D | — | host↔device / device↔device 拷贝方向 |
| CMO | CMO（cache management operation） | 片上缓存一致性操作（aclrtCmoAsync 系列） |
| SQ / CQ | 提交队列 / 完成队列 | 设备侧任务环：Host 将 SQE 写入 SQ，设备完成回报 CQ |
| DFX | 维测子系统 | 可维测性设计：msprof / adump / log / trace / error_manager 子模块 |
| tprt | 传输运行层（不译） | 跨主机/跨设备传输的平台抽象（跨卡链路差异收口），涉及 URMA 等 |

## 算子与编译

| 英文 | 中文 | 说明 |
|---|---|---|
| Ascend C | Ascend C（不译） | CANN 提供的算子开发语言（多层级 API） |
| Tpipe / Tque | — | Ascend C 框架编程 API（内存/同步托管） |
| basic API | 基础 API | Ascend C 单指令抽象 C++ API |
| SIMD / SIMT API | 语言扩展层 | C 接口：SIMD 矢量、SIMT 类 CUDA 编程 |
| PyAsc | PyAsc | Ascend C Python 前端 |
| RegBase | RegBase | 寄存器文件底座编程模型（语扩展） |
| Launcher | 启动器 | 算子 host 侧入口 |
| Tiling 结构体 | tiling 结构体 | host 侧计算的切块参数 |
| AOT Compile | 离线编译 | 编译成可执行产物（AOT） |
| JIT / RTC | 运行时编译 | 运行时实时编译（RTC） |
| IR | IR（中间表示） | 编译器中间表示 |
| GE | 图引擎 | 计算图编译调度引擎 |
| Graph / 图模式 | 图模式 | 整图捕获与执行 |
| aclGraph | aclGraph | CANN 图下发/捕获重放机制 |
| npugraph_ex | npugraph_ex | 基于 torch.compile/FX 的 NPU 图优化组件 |
| AOT Superkernel | AOT Superkernel | 超级核离线编译整图执行（学习营博文） |
| Kernel Launch | 核启动 | 向设备提交一次 kernel 执行 |
| BLOCK_DIM | block dim | 启动核数（block 数） |

## 通信与并行

| 英文 | 中文 | 说明 |
|---|---|---|
| HCCL | HCCL | 昇腾集合通信库（Huawei Collective Communication Library） |
| HCOMM | HCOMM | HCCL 开源仓/库名（hcomm） |
| HIXL | HIXL | 昇腾单边通信库 |
| RDMA / RoCE | — | 远程直接内存访问/融合以太网 RDMA |
| HCCS | HCCS | 昇腾芯片互连高速串口 |
| UBoE | UBoE | UNified Bus over Ethernet 统一总路线（昇腾以太互连） |
| MC2 | 通算融合 | 通信与计算融合（如 GEMM+AllReduce） |
| MoE | 专家混合 | Mixture-of-Experts |
| AllReduce / AllGather / ReduceScatter | 归约 / 全收集 / 分段归约开销，**英文不译** | 集合原语 |
| P2P | 点对点 | 单边/双边点对点通信 |
| 单边通信 | 单边（one-sided） | one-sided communication，如 HIXL |
| supernode / superpod | 超节点/SuperPod | 大规模训练集群形态 |
| PD 分离 | PD 分离 | Prefill/Decode 分离部署 |
| KV Cache | KV 缓存 | 推理时的键值缓存 |
| D2D 直传 | D2D 直传 | device 到 device 直接传输 |

## 编译后端生态

| 英文 | 中文 | 说明 |
|---|---|---|
| PTO | PTO（昇腾通用编程库） | 跨代际高性能数学库与虚拟 ISA（PTO Virtual ISA） |
| PTO Virtual ISA | PTO 虚拟 ISA | 90+ 条指令集合，屏蔽 A2/A3/A5 差异 |
| PyPTO | PyPTO | PTO 的 Python 前端框架 |
| MPMD | MPMD | 多程序多数据执行调度（PyPTO 调度模型） |
| Execution Graph | 执行图 | PyPTO 中间表示层级之一 |
| Tile | Tile（分块） | 计算分块（本处取英文） |
| Block | Block | PyPTO 表达层级之一 |
| TileLang | tilelang | 通用 tile 语言（社区） |
| tilelang-ascend | tilelang-ascend | tilelang 的昇腾后端 |
| torch.compile | torch.compile（不译） | PyTorch 编译 API |
| torchair | torchair | torch 到 GE 图的编译对接组件 |
| autofuse | autofuse | 自动融合组件（TensorFlow 侧） |
| vLLM / SGLang | — | 推理服务框架 |
| Mooncake | Mooncake | KV 池化传输框架 |

## 维测

| 英文 | 中文 | 说明 |
|---|---|---|
| msprof | msprof | 性能采集分析工具 |
| adump | adump | 算子/模型数据 dump 机制 |
| ms_sanitizer | ms_sanitizer | CANN 内存/越界检测组件 |
| DumpTensor | DumpTensor | 数据 dump 指令 |
| npu_sim / Simulator | 仿真器 | CPU Simulator |
| Error Manager | 错误管理器 | 错误码/L2L3 管理 |
| trace | trace（不译） | 过程跟踪 |
