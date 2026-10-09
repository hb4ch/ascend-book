# CH21 提纲 v1（研究定稿版）2026-10-09

> 读者问题链组织；目标核心章 8k–12k 中文。每节标注证据锚（对应 CH21-EVIDENCE §）与可运行性标签。**正文不写，本稿仅提纲。**

## 21.1 为什么集合通信是扩展瓶颈＋HCCL/HCOMM 名实关系
- 训练环 F→B→AllReduce→Update（arch-brief §1.1 图）；HCCL=集合通信库/HCOMM=其通信基础库，dlsym 解耦、独立演进〔E§0〕
- L1–L3/CCU 接口分层表〔E§0〕；**本机边界声明**：HCCL 算子仓不在本地，host 实现不可引，device 侧 `AscendC::Hccl`（asc-devkit hccl.h）可引全〔E§0〕
- 陷阱框：把 `HcclAllReduceInner`（pkg_inc/legacy）当公开 AllReduce——错层

## 21.2 通信域：创建、拓扑与资源（问题：rank 是什么、域从哪来）
- 主线样例 01：MPI 多进程＋rootInfo 广播＋Config（BufferSize/Deterministic/OpExpansionMode）＋InitRootInfoConfig〔C，E§1A1〕
- rank_table.json 路线（样例 02，字段表）〔C〕；产品支持矩阵五平台〔D〕
- 控制面目录学：coll_communicator_mgr{communicator/rank_graph/resource_mgr}；Node/Endpoint/Edge/Link/Fabric/netLayer（Layer0 HCCS/Layer1 RoCE）〔D，E§1A2〕——**与 NCCL 术语辨析一句**
- 陷阱：rootInfo 4108B 魔数；config 字段缺省值

## 21.2b Host→选择器真实调用链与边界（新增，据 EVIDENCE §7.2）
- 全 legacy 链图：HcclAllReduceInner→(V2)→Communicator::AllReduce→ExecOp→GetAlgOperator→SelectAlg→Orchestrate；旁路 HcomSelectAlg（OPS_KERNEL_INFO_LIB）辨析
- **断点声明**：910 侧 HcAllReduceV2 weak、HCCL 仓缺——**不宣称样例必经 legacy 选择器**，改独立案例讲「选择如何发生」
- 910B AIV 布尔式**全式**（OR/排除/量纲）＋**isMesh(IsAlgTypeLevel0Mesh)≠isMeshTopo 变量映射**〔C〕

## 21.3 算法选择：从拓扑条件到 executor（问题：凭什么是 ring）
- 两级选择：AlgConfigurator（拓扑级）→ Operator::SelectAlg（deviceType 分派→910B 条件链**全式见 21.2b**、FFTS 重定向 HD）〔C〕
- `HCCL_ALGO` 环境变量语法与覆盖点〔C〕；引擎平台支持**文档范围 vs legacy 条件分列表**（E§7.3）
- executor 命名→HCCL_ALGO_LEVEL1_NAME_MAP→newTag 拼装（trace 可读）〔C〕
- **纪律框：目录名≠执行路径；给「条件→算法」判定表而非目录列举**
- 950/A2/A3 分叉汇总表（DevType 映射、legacy 语义、AICPU 仅 A3/300I、AIV dtype/op 白名单）〔C，E§2〕

## 21.4 数据面：引擎、协议与一次 AllReduce 的真实旅程
- 四引擎对照（AICPU_TS/CPU_TS/AIV/CCU＋Thread 抽象＋适用）〔D，E§1A4〕
- 内存语义 vs 网络语义原语；Write/Read/Reduce±Notify/Nbi 真名清单〔C〕
- cclBuffer GetIn/Out、零拷贝 HcclCommSetMemoryRange（aclrtReserveMemAddress 前置）〔C/D〕
- 协议仅照录（UBC/UB_RTP/UBoE/RoCE/HCCS/UB_MEM）——**不推断硬件时序**
- device 侧并行世界：`AscendC::Hccl` Prepare/Commit/Wait/Query（repeat 语义、AICube/AIVector 选择、仅核 0 写 msgArea）〔C，hccl.h 注释〕——与 host API **同名不同物**辨析

## 21.4b Host/Device 契约分立（新增，E§7.1）
- **Host 契约只引 host 证据**（main.cc＋comm_mgr_c 文档）；device `AscendC::Hccl` 头注不证 Host 语义——同名不同层辨析框
- 样例参数实录：count=卡数/buffer=count×4B×2+host/**结果按元素 N·j（N=2→[0,2]）手算非实测**；**rank↔device 映射=单机样例假设，通用看 rank_table**
- 销毁序样例真序；多轮槽复用安全〔U〕

## 21.5 完成、同步与生命周期（问题：什么时候算完）
- host：入队≠完成→aclrtSynchronizeStream〔C〕；async error 接口；Barrier 语义〔D〕
- device：Wait 同序约束/Query 轮询〔C〕
- notify 双向配对**两端 timeline 表（t0-t3，各 buffer 何时可动）**〔D，E§7.4〕；**单向通知≠释放；多轮环槽未证**；原语签名实证 HcommWriteOnThread（异步/返回 0）〔C〕
- 销毁序样例真序＋「后果无文档断言」边界〔C/U〕
- 陷阱框：确定性两档（hcclDeterministic/STRICT 混合组网不支持）

## 21.6 自定义通信算子：AICPU P2P 全链（问题：能否自己写通信）
- 八篇 dev guide 流程图→控制面/数据面职责〔D〕
- blog 四步同步协议＋API 对应 data_plane_api 目录〔C/D，E§3〕
- build：`--vendor=cust --ops=p2p`；**样例仓外声明〔U〕**
- 精度二开案例：RS 原四步→Cast→AIV 融合（blog）∥CCU LocalReduce 升精度——**两独立实现不拼接**；LocalReduce UINT8 表 vs INT8 例源文不一致照录〔C，E§7.5〕
- 与 21.3 呼应：自定义算子同样走 alg selection/资源管理（复用证据）

## 21.7 A2/A3/950 差异速查＋维测入口
- 平台×引擎×算法矩阵（汇总 21.3/21.4）；950 AIV-URMA 新路径概览一句（细节 ch23）
- 维测：dfx 目录/HcclGetCommAsyncError/algtype trace tag〔C/D〕；北极星工具点名（PDF 未核〔U〕）

## 21.8 本章小结＋来源
- 一句话：**通信=拓扑条件→算法→引擎→原语→notify 闭环；每步有真名可查**
- 脚注聚合（appD 已有行＋本章新增 hcomm 文档行号）

## 字数与验收预估
8 节；21.3/21.4/21.6 为深度节（各≥1.5k）；代码块≤10 段全部〔C〕可指行号；标签：源码节录〔示意代码〕、样例命令〔需真机验证〕（本书未运行，不预标已验证）。**无 CPU-SIM 路径**（U，报告声明）。
