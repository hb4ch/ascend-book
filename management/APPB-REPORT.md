# APPB 报告 —— 第一批已核术语修订

2026-10-10。任务 `APPB-WRITE.md`；证据 rev2、提纲 rev2。**只改 `glossary.md`（16 条）→`npm run sync:glossary` 再生 appB**；未手改生成页；其他正文零改动；源仓只读零缓存；未提交。

## 修改项（原句→新句要点，全链证据见 APPB-EVIDENCE rev2 对应节）

| # | 条目 | 修订要点 |
|---|---|---|
| 1 | AI Core / Cube Core / Vector Core | 部署形态随架构（已审 2002 同核/2201 分核），删「AI Core 内」绝对表述 |
| 2 | MTE1/2/3 | 只写已证通路：MTE1=L1→L0A/B（三架构均证，3510 另有 L1→UB）、MTE2=GM→L1/UB、MTE3=UB→GM/L1（2201）与 UB→L1（3510）并注「精确通路见架构规格」；**不写含混"L1 内搬运"、不以对称推 MTE3** |
| 3 | AIV/AIC | AIC=**AI Cube**（官方释义出处已注）；删「950 代称」，改「分核架构（已审 2201/3510）中的××核」 |
| 4 | GM/HBM（两条） | 地址空间/介质二分；`__gm__`+Runtime API；**删「多数平台」「host 可见地址空间」** |
| 5 | SMEM | 单义项=SIMT 线程块共享内存区；**Data Cache 写为"UB 内另一分区，勿混"**（不并入定义）；删「950 核间机制」 |
| 6 | URMA | 全称+通信栈语境（CCU 搬运），删代际断言 |
| 7 | UB 容量 | 「通常 192KB 上下」→「按架构规格（已审 2201=192KB 预留 256B）」 |
| 8 | N-DMA→**ND-DMA** | 改 3510 DataCopy 多维扩展（特性#7），删无据「scalar 侧搬移引擎」 |
| 9 | Address Space | 去「950」限定，补 SIMT DCache 中转事实（3510 架构说明） |
| 10 | Event/Notify | host Runtime 层面分立；Notify 与 CntNotify 两族明示；**删「片上」** |
| 11 | TSD | **待审收窄**：HDC 服务类型之一（枚举实证），删「片上任务调度/执行器」概括；「具体职责边界本书未审」明示 |
| 12 | SQE | **待审收窄**：设备接口层提交结构、Rt 层使用/定义未回溯；**不写「runtime 转 SQE 提交」也不写「闭源」** |
| 13 | queue_schedule | 内部命名空间 `bqs`+ezcom client/server 实证；展开名未证不写 |
| 14 | RegBase | 3510 MemBase→RegBase（特性#1） |
| 15 | PyPTO/Execution Graph 族 | PyPTO=PTO 生态 Python 前端+多层抽象，**「码生成以 CCE 路径为主，PTO 调用为可选项」——不写开关控制全部 PTO 调用（另有不受控头链）、不写 host 分支后端结论**，参见第 25 章；Execution/Tile/Block Graph 三层管线明示 |
| 16 | UBoE | 「hixl 通信协议枚举之一（以太系）；展开名未证」，修「总路线」错别字 |

**未动**：910B/910C 映射、HCCL/HIXL/HCCS/RoCE、MPMD、Tile、通信与生态、维测诸条（无新证）。aicpu_sched 条未改——**目录结构不证调度语义，保持原句待审**（rev2 R2-4 结论），未以新猜测替换。

## 余下待审清单（第二批候选，未审不改）

AICPU（编程文档 950 限定未写入）、AIC 展开歧义（AI Core 读法）、3002 架构形态、910_93 含义、tprt、CMO 补接口名、TSD 子系统职责全集、SQE 定义回溯（Rt 非开源部分）、BQS 展开名、die/multi-die、SOC、DFX 子模块清单、ms_sanitizer/adump 粒度、AOT Superkernel/npugraph_ex/autofuse/torchair/TileLang/Mooncake/vLLM 等生态条、H2D/D2H、Host/Device、Stream/Task、aclnn 双条合并问题、tilingkey 博文出处格式。**不宣布全表审毕**——表头不变，审计覆盖以本报告两清单为准。

## 验证与截图

- `npm run verify >/tmp/appb-verify.log 2>&1` → **EXIT=0**：build/internal 42 文件 OK/source 479 引用 0 无效/**check:terms 106 条**。更正首批报告一处不实：并非「仅改说明列」——实际另含**条目名改动 2 处**（`N-DMA`→`ND-DMA`、`AIC（AI Core）`→`AIC（AI Cube）`）与**Execution Graph 条扩为三层管线合述**；terms 输入不受影响（匹配键为英文列）已复核/warn 1 处仍在 ch24 既有文本。
- sync 再生 appB（48 行 diff，与 glossary 同步）。
- 实渲染页表格截图（元素级）：`validation/appb-tbl1-platform.png`（1248×2572，含 AIC=AI Cube×2 处、SMEM 线程块共享×1 DOM 断言）、`appb-tbl2-memory.png`（1248×1734）、`appb-tbl3-runtime.png`（1248×2558）；7 表 104 行在位。**像素文字可读性宿主不能目检，留 PM 视验。**

## 边界

未动 28 章/附录A/appD/任何正文；glossary 之外仅 appB 再生；源仓只读；零安装。候审。


---

# APPB-R1 修订附录（2026-10-10 第二轮）

1. **SQE 漏检纠正**：`runtime/src/runtime/inc/sqe/`实存（经理 rg 指出）；定义/填充/下发三链回源（EVIDENCE rev3 R3-1），glossary SQE 条改为实证句，「Rt 非开源/未回溯」无据说法废止。
2. **MTE 架构标签收敛**：2201 带宽表仅 2 行，L1→GM 系未标架构 overview——glossary MTE1/MTE3 改「已证通路+随架构而异」两段式（R3-2）。
3. **PyPTO** 再收窄：删「PTO 调用为可选项」后端概括，仅「Python 前端+多层图抽象，详见 25 章」；TSD 改职责实证句（进程编排），管理口吻清除。
4. **路径注记**：glossary 文末新增「来源与路径注记」7 组统一完整路径（架构规格/sqe/task/tprt/tsd 等），供术语「见××」回链；后续 path-check 可覆盖。
5. 首批报告不实处已更正（见上）。
6. **第二批回源**：`management/APPB-RUNTIME-EVIDENCE.md`（Stream/Task/AICPU/TSD/SQE/BQS/aicpu_sched/tprt 八条，含调用链），术语表本轮仅收 SQE/TSD 两条已闭合者，余待审。

**R1 轮验证**：`npm run verify >/tmp/appb-r1-verify.log 2>&1` → **EXIT=0**（479 引用 0 无效；terms 106 条；warn 仍 ch24 既有）。 glossary 文末新增「来源与路径注记」7 组统一完整路径；第二批回源独立成档 `APPB-RUNTIME-EVIDENCE.md`（8 条，术语表本轮仅收 SQE/TSD，余待批）。源仓只读；未提交。


---

# APPB-R2 修订（2026-10-10 第三轮）

1. **MTE3 混流水纠正**：L1→UB 属 PIPE_MTE1（3510 表 L133）——MTE3 条只留 UB→GM/UB→L1 单向对；MTE1 条 L1→UB 注明「同表 PIPE_MTE1」。两行无混合方向。
2. **tprd 定稿**：读 `tprt_api.h` 接口面（SqCqCreate/PushTask/CqReportRecv）→术语改「SQ/CQ 资源管理与任务推送」；**旧「跨主机 URMA 平台抽象」无据释义删除**（不并存）。
3. **TSD**：补「host 侧 client 亦属子系统」，去「设备侧」限定；Stream/Task 用 Runtime API 语义短定义，**不写未闭合的 Stream→SQ/全 Task→SQE 链**；AICPU 去「仅 950」与目录/进程绝对句（改「设备侧经 AICPU 类 SQE 下发、aicpu 调度进程承载」，均有点）。
4. **注记精确化**：来源注记改 8 组**关键文件完整路径**（含 stars_david.hpp/aicpu_sqe.h/tprt_api.h/tsd_event_interface.h 等 basename）；「语义务」错字修正为「语义」；SMEM/URMA/ND-DMA 直链注 3/8/7；表内以「注 N」关联，去长括号。
5. **全表台账**：`management/APPB-AUDIT.md`——**104 词条逐行**（按表行去重，浮动统计废止），三态（已核修订/保留/待审）+20 项下一批清单；**生态条未验证不改**单列。本批 glossary 另改：AICPU/Task/tprd/TSD 四条＋注号关联。
6. 验证：sync 再生；`npm run verify >/tmp/appb-r2-verify.log 2>&1` **EXIT=0**（479 引用 0 无效；terms 106）。源仓只读；未提交。


---

# APPB-R3（API/维测批，2026-10-10，据 tasks/APPB-API-AUDIT.md）

1. **残留收窄**：Task 只留「一次可调度执行单元」（删装配 SQE 泛化）；TSD 改「runtime 服务子系统，管理设备侧子进程」（删设备侧限定与 host 例外补丁）；PyPTO 不动。
2. **API 批 12 条实证改写**（`APPB-API-EVIDENCE.md`）：ACL(src/acl)、ACLNN/aclnn（两段式；**aclnnTensor 零命中→aclTensor**）、Event（flag 族+TIME_LINE 计时及性能注意+IPC 限制）、CMO（PREFETCH/WRITEBACK/INVALID/FLUSH 四类，现仅 PREFETCH 开放——非笼统一致性）、DFX/msprof/adump（README+src/dfx 双证）、DumpTensor（show_kernel_debug_data 链）、Simulator（pto-isa CPU Sim vs CMAKE_ASC_RUN_MODE 两语境）。
3. **ms_sanitizer 待审**：runtime 仓无独立目录，词条如实标「未单独审」；不计已核。
4. **脚注化**：glossary 全部来源改标准脚注 [^1]–[^12]（文件级完整路径），表内「注 N」文字引用清除；旧「来源与路径注记」编号节并入脚注。
5. **台账刷新**：`APPB-AUDIT.md` 本批 12 条状态/依据更新；统计口径改「已核/保留/待审」三态，**保留≠已审**、与已验收章一致不计源码核验。
6. 验证：sync 再生 appB；`npm run verify >/tmp/appb-r3-verify.log 2>&1` **EXIT=0**（502 引用 0 无效；terms 106）。源仓只读；未提交。截图：appB 表格三张此前轮已存 validation（本批无新增图表，文字/脚注改动）。


---

# APPB-R4（基础内存/生态批，2026-10-10，据 tasks/APPB-REMAINING.md）

1. **纠错三处**：CMO 接口族泛化（WithBarrier 支持 INVALID+barrier，类型按接口区分）；ACLNN 删「预置」唯一限定（自定义算子工程 aclnn_quick_start 亦产 aclnn API）；Event 表内去 flag 罗列改短定义+脚注。
2. **脚注路径全量完整化**：[^1]–[^26] 零 `.../` 省略；误植 tprd→复核目录后删除（tprt 仅 4 头文件）。
3. **msSanitizer 更名+实证**：devkit debug_and_tuning 文档（四子功能/仅 SIMD）；「待批」移出读者表入台账。
4. **基础内存 7 条**：L0A/B/C 按 2201 L30 语义；L2 去「一致性域」无据句；Register/bank 按 3510 三级与 L174；双缓冲挂官方概念表。
5. **PTO 族**：全称 Parallel Tile Operation 实证；「屏蔽 A2/A3/A5」绝对句废止（README L23 原文「不是隐藏底层能力」）；AOT Superkernel→SuperKernel 更名（principles L5 二进制融合）。
6. **生态通信 12 条**：HCCL 全称锚/HCOMM 原句/HIXL 多链路/协议表 L27/MC2 双证（hccl_comm.h+operator_impl）；PD/KV/Mooncake/TileLang/autofuse/vLLM 标「转述级」。
7. 台账 R4 行 32 条；范围外未核清单入台账附记。证据 `APPB-REMAINING-EVIDENCE.md`。
8. 验证与截图见尾。

**R4 验证**：`npm run verify`（/tmp/appb-r4-verify2.log）**EXIT=0**（534 引用 0 无效；terms 106；warn 1 处系 ch24 脚注引文「昇腾 CANN」原文，定版章不动）。`docs:build` EXIT=0；真实页面元素截图 7 张（appB 术语表 CMO/ACLNN/Event/MTE/PTO 族/通信族区块＋脚注区：`management/validation/appb-r4-{cmo,aclnn,event,mte,ptofam,comm,footnotes}.png`；dist 重建后 8923 端口元素级截图，服务已关）。源仓双仓 status=0 只读；未提交。

---

# APPB-R5（收口，2026-10-10，据 reviews/APPB-R5）

1. **脚注错位修复**：`[^1]0/[^1]1/[^4]/10`→`[^10]/[^11]/[^4][^10]`；TSD→[^6]；[^10] 19-02 补全路径；逐条「引用存在且指向正确内容」校对。
2. **生态定义**：npugraph_ex=图后端（SuperKernel 仅开启方式之一，删反向限定）；AOT 通义+Ascend 特化例；图模式≠捕获。
3. **数字退场**：119GB/s/CacheLine/512KB 出表；**AllReduce 族正名**（全归约/全收集/归约散播，architecture-brief+hccl_types）。
4. **研究史清扫**＋aclnn 收口；AI Core 直连[^1]。
5. **104 行闭合**：新增官方概念表[^28]，20+ 条收口到原文短定义；Tpipe/Tque 与基础 API 按 asc_how_to_choose_api 三类口径[^27]；未核影响定义项=0（无脚注 31 行均产品常识/书内生态/通用编译词，见台账 R5 §7）。
6. 验证：sync；verify **EXIT=0**（536 引用 0 无效；warn 1 处 ch24 定版原文）；build EXIT=0；新截图 7 张 `appb-r5-*.png`（8924 端口已关）。源仓双仓 status=0；未提交。
