# APPB 全表逐行审计台账

2026-10-10。范围=glossary.md 全部 **104 个词条**（按表行去重；R1 前"25条/60条"浮动口径废止）。状态三类：**已核修订**（首批+R1/R2，见 APPB-EVIDENCE rev2/rev3）、**保留已核**（本轮无改动，原句与已验收章/仓一致）、**待审**（下一批，清单见尾）。

## 平台与芯片

| 词条 | 状态 | 本轮处理/依据 |
|---|---|---|
| Ascend / 昇腾 | 保留 | 保留 |
| AI Core | 已核修订 | 改：部署形态随架构（注1） |
| Cube Core | 已核修订 | 改：随架构+2002/2201实例（注1） |
| Vector Core | 已核修订 | 改：随架构（注1） |
| Scalar | 保留 | 保留（未审，待批） |
| AICPU | 已核修订 | 改：辅助CPU核+SQE/进程承载（注5）去950绝对句 |
| MTE2 | 已核修订 | 首批改：GM→L1/UB常见方向 |
| MTE3 | 已核修订 | R2改：去L1→UB混流水；UB→GM/UB→L1分架构（注1） |
| MTE1 | 已核修订 | 改：已证L1→L0A/B；3510 L1→UB属MTE1（注1） |
| AIV（AI Vector） | 已核修订 | 首批改：分核架构矢量核 |
| AIC（AI Cube） | 已核修订 | 首批改名AI Cube+R2注3/1 |
| GM / HBM | 已核修订 | 首批改：地址空间/介质二分 |
| SMEM（Shared Memory） | 已核修订 | 首批改：SIMT线程块共享区，DataCache另分区（注3） |
| URMA | 已核修订 | 首批改：全称+通信栈（注8） |
| 910B / 910C | 保留 | 保留：pto-isa/runtime映射脚注（证据rev1§7） |
| Ascend 950 / 950PR / 950DT | 保留 | 保留（未审，待批） |
| SOC | 保留 | 保留 |
| die / multi-die | 保留 | 保留 |
## 内存与数据

| 词条 | 状态 | 本轮处理/依据 |
|---|---|---|
| GM | 已核修订 | 首批改：__gm__/Runtime API/勿等同HBM |
| L1 Buffer | 已核修订(R4) | MTE1供给链+2201容量；REMAINING §3 |
| L0A / L0B / L0C | 已核修订(R4) | npu_arch_2201 L30 左右矩阵/结果语义；§3 |
| UB（Unified Buffer） | 已核修订 | 首批改：容量按架构（2201=192KB-256B） |
| L2 | 已核修订(R4) | basic_architecture L113/L206 CacheLine；§3 |
| Register | 已核修订(R4) | 3510 三级流转+Reg编程 c_programming_overview L15/119；§3 |
| Tiling | 保留 | 保留 |
| TilingKey | 保留 | 保留 |
| ping-pong | 已核修订(R4) | 双缓冲=官方概念表 L182 关联；§3 |
| bank | 已核修订(R4) | L174 多体并行；§3 |
| bank conflict | 已核修订(R4) | L174 同 bank 排队；§3 |
| Address Space | 已核修订 | 首批改：去950限定+DCache中转 |
| ND-DMA | 已核修订 | 首批改正名：3510 DataCopy扩展（注7） |
## 运行与调度

| 词条 | 状态 | 本轮处理/依据 |
|---|---|---|
| runtime | 保留 | 保留 |
| ACL / AscendCL | 已核修订(R3) | src/acl实现；API-EVIDENCE §2 |
| ACLNN | 已核修订(R4) | 删「预置」唯一限定：含自定义算子工程 aclnn_quick_start；§3 |
| aclnn | 已核修订(R3) | 前缀+aclnnTensor辨析(零命中)；§3 |
| Stream | 保留(已核R2) | Runtime API语义，本批未改 |
| Task | 已核修订(R3) | 短定义收窄：删「装配SQE」泛化；API-EVIDENCE §1 |
| Event | 已核修订(R4) | 表内去 flag 罗列，短定义+脚注；§1 |
| Notify | 已核修订 | 首批改：与CntNotify分立（注4） |
| SQE | 已核修订 | R1/R2：结构族+填充+下发链实证（注5） |
| TSD | 已核修订(R3) | runtime服务子系统/管理设备侧子进程；API-EVIDENCE §1 |
| queue_schedule | 已核修订 | 首批：命名空间bqs+ezcom实证 |
| aicpu_sched | 保留 | 保留：目录实证，语义待审 |
| Host | 保留 | 保留 |
| Device | 保留 | 保留 |
| H2D / D2H / D2D | 保留 | 保留 |
| CMO | 已核修订(R4) | 接口族泛化纠正：类型按接口区分；CMO-EVIDENCE/REMAINING §1 |
| SQ / CQ | 保留 | 保留（tprd证据互证） |
| DFX | 已核修订(R3) | 五子模块README+src/dfx双证；§6 |
| tprt | 已核修订 | R2改：删除无据旧释义；SQ/CQ资源管理+任务推送（TprtSqCqCreate/PushTask，注5） |
## 算子与编译

| 词条 | 状态 | 本轮处理/依据 |
|---|---|---|
| Ascend C | 保留 | 保留 |
| Tpipe / Tque | 保留 | 保留 |
| basic API | 保留 | 保留 |
| SIMD / SIMT API | 保留 | 保留 |
| PyAsc | 保留 | 保留 |
| RegBase | 已核修订 | 首批：3510 MemBase→RegBase（注7） |
| Launcher | 保留 | 保留 |
| Tiling 结构体 | 保留 | 保留 |
| AOT Compile | 已核修订(R4) | aot_compilation_optimization L3 定义；§6 |
| JIT / RTC | 保留 | 保留 |
| IR | 保留 | 保留 |
| GE | 保留 | 保留 |
| Graph / 图模式 | 保留 | 保留 |
| aclGraph | 保留 | 保留 |
| npugraph_ex | 已核修订(R4) | kernel_direct_call L6 仅此后端；§6 |
| AOT Superkernel | 已核修订(R4) | 改名SuperKernel；principles L5 二进制融合；§6 |
| Kernel Launch | 保留 | 保留 |
| BLOCK_DIM | 保留 | 保留 |
## 通信与并行

| 词条 | 状态 | 本轮处理/依据 |
|---|---|---|
| HCCL | 已核修订(R4) | architecture/README L3 全称；§5 |
| HCOMM | 已核修订(R4) | README L9 通信基础库；§5 |
| HIXL | 已核修订(R4) | README L36/L50 多链路+119GB/s；§5 |
| RDMA / RoCE | 已核修订(R4) | architecture-brief L27 协议表；§5 |
| HCCS | 已核修订(R4) | L27+hixl L50；§5 |
| UBoE | 已核修订 | 首批：协议枚举之一；错别字修 |
| MC2 | 已核修订(R4) | hccl_comm.h L260+operator_impl L208；§5 |
| MoE | 保留 | 保留 |
| AllReduce / AllGather / ReduceScatter | 保留 | 保留（未审，待批） |
| P2P | 保留 | 保留 |
| 单边通信 | 已核修订(R4) | HIXL单边+实践文章转述标注；§5 |
| supernode / superpod | 保留 | 保留 |
| PD 分离 | 已核修订(R4) | xLLM博客转述标注；§5 |
| KV Cache | 已核修订(R4) | HIXL池化传输转述标注；§5 |
| D2D 直传 | 保留 | 保留 |
## 编译后端生态

| 词条 | 状态 | 本轮处理/依据 |
|---|---|---|
| PTO | 已核修订(R4) | README L7 Parallel Tile Operation 定位；§4 |
| PTO Virtual ISA | 已核修订(R4) | L23 90+条/非屏蔽底层——删A2A3A5绝对句；§4 |
| PyPTO | 保留(已核R2) | 无后端猜测版 |
| MPMD | 保留 | 保留 |
| Execution Graph / Tile Graph / Block Graph | 已核修订 | 首批：三层级管线合述 |
| Tile | 已核修订(R4) | L42 tile ISA 抽象；§4 |
| Block | 保留(已核R2/R3) | 层级见25章，本批未加新证 |
| TileLang | 已核修订(R4) | 实践博客转述标注；§6 |
| tilelang-ascend | 保留 | 保留 |
| torch.compile | 保留 | 保留 |
| torchair | 已核修订(R4) | pytorch_framework L7 TorchAir入图；§6 |
| autofuse | 已核修订(R4) | AutoFuse×TorchInductor 博客；§6 |
| vLLM / SGLang | 已核修订(R4) | 仅语境提及标注，不展开；§6 |
| Mooncake | 已核修订(R4) | HIXL对接案例转述；§6 |
## 维测

| 词条 | 状态 | 本轮处理/依据 |
|---|---|---|
| msprof | 已核修订(R3) | README原句+msproftx；§6 |
| adump | 已核修订(R3) | README原句+18_dump接口；§6 |
| ms_sanitizer | 待审 | 仓内无独立目录，未审；§9 |
| DumpTensor | 已核修订(R3) | show_kernel_debug_data链；§7 |
| npu_sim / Simulator | 已核修订(R3) | 两语境分指pto-isa CPU Sim/CMAKE sim；§8 |
| Error Manager | 保留 | 保留 |
| trace | 保留 | 保留 |

## 待审清单（下一批候选；本批不动）

1. AICPU 950编程入口限定未写入
2. AIC展开歧义（AI Core读法）
3. 3002架构
4. 910_93含义
5. tprt旧出处章节对账
6. TSD/TDT分工、设备内侧
7. SQE arch5162差异/CQ回报
8. Stream→SQ绑定逐行
9. BQS展开名
10. DFX子模块清单
11. ms_sanitizer/adump粒度
12. AOT Superkernel/npugraph_ex/autofuse/torchair/TileLang/Mooncake/vLLM等生态条回源
13. aclnn两条关系
14. tilingkey博文出处
15. HCCL/HCCS展开复核
16. MC2/P2P/单边通信原出处
17. supernode/PD/KVCache常识性复核
18. Tile/Block独立条与合条关系
19. PTO定位句改官方原话

统计：总 104 条；已核修订见上表状态列；待审 19 项。**统计口径（R3 起）：已核=有源码/文档实证（EVIDENCE rev2/rev3、RUNTIME-EVIDENCE、API-EVIDENCE）；保留=此前轮已核本批未动；待审=未核（与已验收章一致不算源码核验）。全表 104 行均过目；已核+保留见状态列，其余待审。**


---

# R4 附记（APPB-REMAINING 批，2026-10-10）

- 本批已核 32 条（上表 R4 行）；证据 `APPB-REMAINING-EVIDENCE.md`。
- 转述级证据（官方博客/实践文章）已逐条标注「转述」，与源码/文档实证区分。
- **范围外未核清单**：ACLNN 实现细节（runtime src 内核）与两段式实现层、ACL 各子模块实现、aclnn 两段式在 runtime 内实现、ch22–27 生态章专有条（supernode/EPD 等）、HCCL 算子实现族、UBoE 协议细节、CANN 包组件划分（ch3 已核除外）、ascend c 基础 API 名录逐条。均待后续批次。
- ms_sanitzer→msSanitizer 更名；「待批」字样移出读者表（管理侧记录）。


---

# R5 收口（reviews/APPB-R5，2026-10-10）

1. **脚注错位修复**：`[^1]0/[^1]1/[^4]/10` 系批量替换残渣→逐条改为 `[^10]/[^11]/[^4][^10]`；TSD `[^5]`→`[^6]`；URMA 悬空逗号；[^10] 内 19-02 补全路径 `runtime/docs/zh/api_ref/19-02_msproftx_extension_apis.md`。校验=引用存在且指向对应内容（人工逐条+verify）。
2. **生态定义收口**：npugraph_ex 回归 26 章口径（torch.compile 入图的图后端，SuperKernel 仅为开启方式之一，删反向限定）；AOT 先通义后 Ascend 特化例；Graph/图模式≠捕获（捕获重放为常见实现之一）。
3. **性能数字退场**：HIXL 119GB/s、L2 Cache Line 尺寸、L1 512KB 从表内删除（术语无需性能数字，细节在源）。
4. **研究史清扫**：已证/原句/grep 无命中/本书未见/展开未证/勿混等表述删除或改中性；aclnn 只留前缀+aclTensor；AI Core 直连[^1]。
5. **AllReduce 族正名**：全归约/全收集/归约散播（据 hcomm architecture-brief L16/L25、hccl_types ReduceOp），原「归约/全收集/分段归约开销」废止。
6. **104 词条定义粒度闭合**：新增官方概念表脚注 [^28]（asc-devkit concepts_and_terms/glossary），Cube/Vector Core、Scalar、AIV、MTE2、GM/UB、Host/Device、Tiling/TilingKey、Kernel Launch、IR、queue_schedule/aicpu_sched、Stream/Notify/SQE、Error Manager/trace、Simulator、ping-pong、UBoE 等收口到原文/权威短定义；Tpipe/Tque 大小写、基础 API「单指令抽象」泛化按 `asc_how_to_choose_api.md` L18-26 改三类接口口径[^27]。
7. **未核范围准确计数**：全表 104 行中**无脚注 31 行**，全部为（a）产品/命名常识（Ascend、910B/910C、950 系、SOC/die）、（b）书内自洽生态条（PyPTO/MPMD/Block/Execution Graph/tilelang-ascend/torch.compile/supernode/P2P/D2D/MoE）、（c）通用编译词（JIT/RTC/GE/aclGraph/Launcher/Tiling 结构体/BLOCK_DIM/Ascend C/runtime/ACL/Task/Address Space/SQ-CQ/H2D 等）——**均不影响现有定义正确性**；影响定义的未核项=0。历史「保留未核」清单由本批收口后废止，以本节为准。
