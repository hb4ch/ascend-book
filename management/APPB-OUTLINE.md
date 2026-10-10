# APPB 提纲 —— 术语表修订（rev2；证据 APPB-EVIDENCE.md rev2 为准）

依据 `APPB-EVIDENCE.md`（10 组审查）。**唯一改动面=根 `glossary.md`**；appB 由 sync 脚本再生；不改共享文件。原则：**短定义＋必要适用范围＋章内阅读入口**；表内不塞长段；无出处的不写，架构相关必注代际。

## 修订分组（按优先级）

1. **AIC/AIV 条重写**：AIC=AI Cube 核（非 AI Compute）、AIV=AI Vector 核；删「950 代称」，注「分核形态自 2201；2001/2002 同核」；出口→ch10/11、架构规格 npu_arch_2201。
2. **AI Core/Cube Core/Vector Core**：AI Core 条注两代部署形态一句；Cube/Vector 条加「部署随架构」限定；出口→ch10。
3. **MTE1/2/3**：只写常见方向（MTE1=L1→L0/L1 内、MTE2=GM→片内、MTE3=片内→GM/L1），**注明「精确通路随架构，见 npu_arch_*.md 带宽表」；已审架构=2002/2201/3510（3510 新增 L1↔UB/L0C→UB 差异）**；不写「2201 起」时间谱系；出口→ch10/15/16。
4. **GM/HBM**：GM=地址空间、HBM=介质，二者关系由架构规格定义（2201 实证）；host 按所用 API 访问，**无绝对句**；出口→ch4/8/10。
5. **SMEM**：单义项=SIMT 编程 UB 线程块共享区（+Data Cache），注语境防与通信侧混淆（快照内通信侧无 SMEM 实证，不设条）；出口→ch11。
6. **URMA**：补全称 Unified Remote Memory Access、限定 hcomm/hixl 通信栈语境；删绝对代际断言；出口→ch21-23。
7. **Event/Notify/Barrier 与运行时内部条**：Event/Notify/CntNotify 分立＋设备侧 CrossCore/Mutex/Barrier；**TSD 改「runtime 设备通信服务（HDC 服务类型之一）」去「片上」**、SQE 改「设备接口层提交结构（Rt 侧），本书未回溯定义」或删、BQS 只写命名空间实证、aicpu_sched 保留补子目录；出口→ch4-5。
8. **PTO 族**：PTO 定位句改官方原文；Tile/Block/Execution Graph=PyPTO 编译层级；**PyPTO 条补「码生成以 CCE 路径为主，PTO 调用=门控选项 `codegen_support_tile_tensor`（默认关）；host/SIM/NPU 三分派」——不写唯一后端**；出口→ch22-25。
9. **小修**：AICPU 注编程文档 950 限定；UB 容量改「按架构规格（2201=192KB-256B 预留）」；N-DMA→ND-DMA（3510 多维搬运指令）或删；CMO 补 `aclrtCmoAsync`；RegBase 注 3510 MemBase→RegBase；UBoE 去错别字+收敛为「协议枚举」表述。
10. **UBoE**：改「hixl 通信协议枚举之一（以太系）」，去无据展开与错别字。**11. 审计覆盖声明**：术语表加脚注——本表已审条目见 APPB-EVIDENCE（15 组）；其余条目沿承各章审记，未逐一回源。**12. 保留不动**：910B/C 映射（pto-isa/runtime 脚注）；HCCL/HIXL/通信与生态条。

## 流程与验证

改 `glossary.md`→`npm run sync:glossary` 再生 appB→`npm run verify`（check:terms 应仍 106 条级、0 误用）→真实 exit 记录。**每条改动在 APPB-REPORT 列「原句→新句→证据行」对照**；术语条数变化如实。不碰 28 章/附录A/appD；源仓只读。

## 版式

术语表保持三列（英文/中文/说明）；「说明」内用「适用：」前缀标架构范围，「见第 N 章」作阅读入口；**不新增长解释段**——超两行内容移脚注或正文。
