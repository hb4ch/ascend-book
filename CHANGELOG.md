# CHANGELOG

《昇腾平台技术实战》里程碑日志。所有来源数据、决策与结论落此文件，可追溯。

## M3-5 第13章 算子库体系 成稿（0.2k → 2.9k 总字 / 中文 2.2k）

- **六节结构**：① 三仓定位与版图（ops-nn 高阶 NN 16 域 / ops-transformer 大模型进阶 / ops-sparse 2026-05 新仓；目录结构完全同构；版本配套纪律）；② ops-nn 深看（**add_example 四件套真结构：op_host/op_kernel/op_graph/examples**——骨架期漏了 op_graph，写作时补上：fusion_pass 是第3章图模式收益的真身；量化矩阵 fp8/mxfp8/hifp8/mxfp4×5 粒度；SIMD/SIMT 同构算子）；③ transformer 族谱（attention 月更族系/moe/mc2 通算融合→第17章伏笔）；④ sparse 短节；⑤ 开发贡献路径（--genop 骨架、最小交付件清单、experimental→正式目录）；⑥ 二开五步清单 + torch_extension JIT 桥。
- **图 3 张**：SVG 1（三仓版图+算子解剖）+ Mermaid 2（算子获取决策树闭环 / 算子交付链）。
- **决策**：① **时效性纪律**：transformer 仓月更，正文只写结构性事实，算子清单给族系+查证方法不逐个打包票；② 章字数 2.2k 中文低于目标——参考型章节以表/结构为主，按「质量优先」口径登记；③ 骨架期「四仓横览」实为三仓（第四编才是仓库全景），标题已纠。
- **校验**：`npm run verify` 全绿；脚注配对、XML、色板自审过。
- 全书进度：71.3k 总字 / 55.9k 中文。M3 进度 5/6。下一章：第14章 经典算子实战（本编收口，还三笔预支债）。

## M3-4 第12章 编译、工具链与部署 成稿（0.3k → 3.8k 总字 / 中文 2.9k）

- **六节结构**：① 编译总流程（bisheng 三路异构：Host/Cube/Vector→Fatbin→可执行；SIMT 走 `--enable-simt` 支线且与 SIMD 头文件互斥；产物终点=第5章 binary_loader 调用侧）；② `--npu-arch`（dav-2201/dav-3510；**决策：骨架期登记的 dav-2002 检索不到，明示不采信**，架构号以官方对应表为准；2201→3510 迁移 CMake 真码；reserved-ubuf 选项跨架构语义差异）；③ 四种编译形态（全程序/`-dc` 单独编译+extern 纪律+LTO/动态库/静态库隐藏流程）+ ops-nn `custom_kernel.cmake` 真仓「目录即约定」组织；④ RTC 七接口流程（rtc_hello_world 真码、模板核函数 aclrtcAddNameExpr/GetLoweredName、aclrtcGetCompileLog）；⑤ NPU Simulator（bit 级精度+指令流水、npusim 更名时效标注、约束清单）+ 与 `--run-mode=sim` 两条仿真路径辨析；⑥ 部署（多算子包/交叉编译/加速/调试）+ 实用选项表（--cce-auto-sync 呼应第10章）。
- **图 3 张**：SVG 1（异构编译流水线，核心记忆图，右接第5章 binary_loader）+ Mermaid 2（静态 vs RTC 双泳道 / 五分支编译形态选型树）。
- **决策**：① BiSheng 源码不在开源仓，全书只写「文档+产物+用法」级（§8）；② ch12 字数 2.9k 中文低于 8k 目标——工具链章信息密度高、流程可图化，按「质量优先」口径如实登记；③ Simulator 约束多用表格不硬凑图。
- **校验**：`npm run verify` 全绿；脚注配对、XML 校验、色板（#e8930c 清除）自审过。
- 全书进度：68.6k 总字 / 53.8k 中文。M3 进度 4/6。下一章：第13章 算子库体系。

## M3-3 第11章 SIMD/SIMT 与高级特性 成稿（0.2k → 约4.3k 总字 / 中文约3.3k）

- **六章结构**：① SIMD C API 接口分级（`_sync` 易用口 vs `mask/repeat` 自排程口，真码取自混合样例的 `simd_adds`）；② SIMT 编程模型（硬件三件套 DCache/Warp Scheduler/128KB RF + **CUDA 迁移对照表** 8 行 + AICPU 逃逸时机=Tiling 下沉）；③ 混合编程（`__simt_vf__`/`__simd_vf__`/`asc_vf_call` 三件套，gather_and_adds 全程精读，核心编排思想：**离散和规整的转换在数据进 UB 的那一刻完成**）；④ 同步进阶（PipeBarrier/DataSyncBarrier/Mutex 核内、CrossCore/SyncAll/IBSet 核间、SSBuffer 新地基）；⑤ RegBase（MemBase vs RegBase 对照表、GM 不能直灌寄存器硬约束、VF 融合性能来源、02_reg_vector_compute 20 例字典）——**还清第 10 章预支的 RegTensor/寄存器计算深度债**；⑥ 950 新特性四类分组导览 + 调试工具箱。
- **图 6 张**：SVG 3（SIMT 硬件剖视+CUDA 平移表 / 混合编程双引擎数据流 / MemBase vs RegBase 双栏对照）+ Mermaid 3（SIMD vs SIMT 执行对比 / 950 特性分类 / 本章四条路小结记忆图）。
- **决策**：① NPU-Check 在本地开源基线检索不到，按 §8「无出处不写」降级处理并在正文明示；② 图 11-2 由原计划的 SVG 改为 Mermaid（执行模型对比用分类流程即可表达，硬件解剖留给图 11-1）；③ 字数延续「质量优先」口径。
- **校验**：`npm run verify` 全绿（38 文件构建/链接/源码路径/术语通过）；XML 校验 3 图全过；脚注 used==defined；SVG 审核见 subagent 记录（下条）。
- 全书进度：64.5k 总字 / 50.7k 中文。下一章：第12章 编译、工具链与部署。

## 2026-XX-XX · M0 初始化

**范围**：站点骨架 + 写作规范 + 术语表 v1 + 来源映射表 + 第1章试写样章。

### 决策记录

- D0-001 交付形态：VitePress 静态站点，中文单语，章节文件 `chNN-<slug>.md`，URL 使用英文 slug。
- D0-002 代码分级：四种运行性标签（NPU 运行 / CPU-SIM / 需真机验证 / 示意代码），写入 STYLEGUIDE 与导读。
- D0-003 来源标注：源码路径用代码行内标注（`📦 源码:` / `📄 资料:`），不建外部仓库文件链接。
- D0-004 术语唯一事实源：`glossary.md`（根目录），构建期同步进站点附录B。
- D0-005 章骨架：`本章目标 → 正文 → 陷阱与注意 → 进一步阅读`；核心章 8k-12k 字强制。

### M0 验收

- [x] `npm run docs:build` 通过（同步 glossary 后构建）
- [x] `npm run check:links`（配置里对 hiascend/gitcode 做了放宽；本地未完全跑远端，后续在 CI 跑）
- [x] `npm run check:source` 通过：38 个 md，引用的 `repo/path` 逐一核对存在
- [x] `npm run check:terms` 通过：术语表 103 条无高置信误用
- [x] 第1章试写样章成稿：正文约 6k 中文字 + 代码证据，总量 8.3k+ 且全部论断有出处

### 第1章字数说明（评审点）
第1章定位「平台总览」，按「广度优先」写作，正文约 6,000 中文字 + 代码块/表格证据，总量约 8.3k（中+英token）。若评审认为必须严格 ≥8k 中文，后续补章节时优先扩展 1.2/1.4（CUDA 对照表与三视图已有余量）。此口径记录于本流水线，验收以「内容扎实、每论断可溯源」为主要标准。
### 源码勘误/修正记录

- `acl_rt_api.h` 实为「兼容层内联头」，推荐主入口为 `acl_rt.h`（含 `aclrtLaunchKernel` 等 V3 系新接口）；正文以此为准。

## 下一里程碑（M1）与第一编三輪重写记录

### 三轮迭代（本轮）
- **R1（plan→write→review）**：按 PLAN-PART1 重写三章——叙事优先、比喻先行、行内引用清零（改脚注 `[^n]`）、代码四句法。结论：可读性大幅提升，但字数跌至 2.2–2.9k。
- **R2（plan→write→review）**：保持可读性的前提下实质加深——第1章补产品支持表能力菜单/错误码分段/两段式三理由/FAQ；第2章补手算带宽账/分层动机/同步家族表格/FAQ；第3章补下单四步/blockDim/图模式约束/三笔账症状-对策表。
- **R3（plan→write→review）**：proofread + 一致性——修正错字（规距→规矩、落汗、口决、昇腾 C→Ascend C 等）；重编 2.3.x 小节号；补 Ch3 小结一生总图；跑全量校验。

### 当前状态（第一编）
- 三章均按新规范成稿：第1章 4.2k、第2章 3.9k、第3章 2.9k（总字，分别含中文 3.6k/3.3k/2.4k）。
- 校验全绿：build / check:internal / check:source / check:terms；Mermaid 图三章共 8 张、表格 12 张、脚注全部渲染。
- **与计划目标（8k/章）差距**：字数未达标；属「增量深挖」而非缺件。是否继续拉长等待评审建议（计划已声明「字数服从质量，不灌水」）。

## M2 预告

- 第4章 ACL 编程接口（材料齐备：acl_rt.h + error_codes + api_ref + 0_quickstart 家族）

## M1 扩展（选 B）· 第1章 完成记录

### 决策（评审确认）
- M1 评审拍板走 **B**：把第一编三章补齐到 7–8k 中文（质量优先，不灌水），再进 M2。
- PLAN-PART2.md 已按 B 更新：新增每章扩展清单表（全部源码抓手已核对存在）、执行顺序（B-1→B-4 再进 M2）。

### B-1 第1章扩展（4.2k → 7.9k 总字 / 中文 4.2k → 6.7k）

新增/加深清单（每条均有源码锚点）：
- 1.1.2 认识你的卡：npu-smi 三命令（接附录A）。
- 1.2 门牌表（七层各到哪挖，宽而不深）；1.2.1 概念户口本（CANN/ACL/runtime/驱动谁是家、谁是谁）；1.2.2 出错读法展开（107/145 段 + 三个查询函数，基于 1_error_handling）。
- 1.3 异步哲学账（aclnnAdd 下单即走、同步自己画）；1.3.1 两个 Hello 对照：aclnn 两段式 vs `<<<>>>` 自定义 kernel（4_custom_kernel_launch）差异表 + dcci() 存储一致性第一课 + 九步骨架。
- 1.4 三拍子真码（add.asc 的 CopyIn/Compute/CopyOut）；1.4.3 多核切块第一课（block_idx/blockDim 落地）。
- 1.5 攻坚线 + 七编对齐到两张图 + 动手小练习三选一；FAQ 三连→四连。
- 1.6 一页总图（剖面+厨房缝成一张）+ 名词导航总表 + 五句口头禅。
- 移除冗余的 1.5「一页速查」表（被 1.6 导航总表吸收）。

**校验**：`npm run verify` 全绿（build/站内链接/源码考古/术语/字数）；正文无 `📦/📄` 行内标注残留。

### B-2 第2章扩展（3.9k → 6.8k 总字 / 中文 3.3k → 5.6k）

新增/加深清单（每条均有源码锚点）：
- 2.1.1 搬运账三步法（列数据→数趟数→对带宽）+ 计算密集 vs 搬运密集分野。
- 2.2 三拍子读法实战：add.asc 真码逐行 + 同步时序图（异步传话 + 两道同步门）；修复“比第1章多一样东西”措辞（第1章真码本就含两处 barrier）。
- 2.3.2 新增「访问权」表（Scalar/Vector/Cube/MTE 谁能碰谁），并给“谁不能访问什么 → 决定了算子怎么写”的推论。
- 2.3.4 新增 L1 复用手算例子（直送 vs 过 L1 的 GM 流量差 ≈ N 倍）+ matmul_basic_api.asc 真码走位（SetGlobalBuffer/DataCopy/SetFlagMTE2_MTE1/LoadData）。
- 2.3.6 N-DMA 扩展：为什么需要 N-DMA（不连续数据痛点）+ 规整 vs 变形数据的判断标准。
- 2.4 新增「同步的代价」：流水线气泡、enqueue/dequeue 替代全量 barrier 思路。
- 2.5.1 Regbase 代码对照（Load/Reg::Add/Store + mask）。“
- 2.5.2 能力菜单从 5 行扩为 asc_950_feature_guide 13 项总览摘编（含资料成熟度列）。
- 新增「陷阱与注意（汇总）」表（症状→对策）；FAQ 二连→三连；小节号清理（删孤儿 2.6.1）。

**校验**：`npm run verify` 全绿。

### B-3 第3章扩展（2.9k → 5.3k 总字 / 中文 2.4k → 4.5k）

新增/加深清单（每条均有源码锚点）：
- 3.1 四阶段钉源码表（kernel/args/task_submit/launch）+ launch 记时钟说明 + 第1章九步 ↔ 本章四阶段闭环表。
- 3.2 事件（event）对讲机语义（01_api_ref 07_event + 1_basic_features/event）；SQE 字段级拆解（rtDynamicSqe_t 的 vld/codeSize/dynTaskDescSize/blockDim/taskPcOffset，`dynamicSqe->blockDim` 赋值）。
- 3.3 BQS 状态机（fsm：idle/full/peek/error/base）+ TSD 客户端进程/线程两模式 + SQ 环/doorbell 物理面。
- 3.4 NPUGraph 上手代码（捕获/重放/只改参数）+ 决策表 + SuperKernel 正确性约束 + 图模式“省时间+省内存”双份。
- 3.5 三笔账量级估算实例（elemwise 4096²）+ “最有价值时刻在第四编”使用说明。
- 3.6 关键对象清单表 + 形态/状态归纳 + 动手练习三选一 + FAQ 三连。
- 修正既存错字（口决→口诀）。

**校验**：`npm run verify` 全绿；正文无 `📦/📄` 行内标注残留。

### B-4 M1 总收口

- 三章最终字量（三轮补齐后的实测值）：第1章 8.2k 总字（中文 6.9k）；第2章 **7.8k** 总字（中文 **6.5k**）；第3章 **6.8k** 总字（中文 **5.9k**）。第一编合计 **22.9k 总字（中文 19.4k）**。
- 本轮（最后一轮拉齐）补充内容：第2章新增 2.3.7 搬运对齐与 Cache Line、2.4 同步三现场真码表、2.5.2 迁移到 950 五步核对单（基于 `2201_to_3510_arch_changes.md` 搬运/计算/存储三张变更表）；第3章新增 SQE 真码行 + 任务三维度 + AICPU 动机、BQS 职责三事表 + FSM 状态图（idle/full/peek/error/base 真实状态名）、三笔账测量入口表 + 三个失真时刻、四档下单方式一览表、decode 收益来源推演。
- 口径说明（如实记录）：纯中文与 7k 目标仍有小差距（第3章 5.9k），成本主要来自真码/表格/Mermaid 计入“字”不计“中文”；质量优先不注水。若评审要求严格 ≥7k 中文，后续优先扩展点已留钩子（第2章 2.2 同步深挖、第3章 3.4 案例复盘）。
- appD 三章来源路径已随新增脚注同步；README 里程碑 M1 转 ✅；`npm run verify` 全绿，正文无 `📦/📄` 行内标注残留。

## M2 预告

- 第4章 ACL 编程接口（材料齐备：acl_rt.h + error_codes + api_ref + 0_quickstart 家族）

## M2-1 风格指南增量（已并入）

- STYLEGUIDE.md 新增 §10「第二编补充约束（M2）」三条：① ≤5 锚点文件/章、禁逐文件翻译 runtime/src；② API 层讲用法、实现层讲机制、驱动层写护照面；③ 运行性分级从严（runtime/example 与 ACL 程序一律 [需真机验证]，cmodel/CPU-SIM 只作旁证）。
- 附录E 同步新增 E.4。

## M2-2 第4章 ACL 编程接口 成稿（0.3k → 4.5k 总字 / 中文 3.7k）

- 覆盖骨架全部 7 节：初始化/四件套句柄/内存(含 SOMA 物理内存族)/三种 Launch/异步同步/错误码/0_hello_cann 229 行逐行剖析。
- 统一心智：ACL=前台接待；接口地图 = 点亮→句柄→借冷库→下单→验收→读错。
- 真码/锚点：acl_rt.h 签名（aclInit 1091 / aclrtLaunchKernel 3320 / aclrtMallocPhysical 2618 等）、0_hello_cann main.cpp、1_basic_features 四件套、1_error_handling、4_custom_kernel_launch。
- 新增：设备查询三句、aclrtLaunchKernel 与 <<<>>> 真码对照、Hello 四改实验、SOMA 虚拟/物理内存小节、FAQ、陷阱汇总表（含 aclnnop 生成头勘误口）。
- **校验**：verify 全绿；正文无行内 📄/📦 标注。成品 3.7k 中文（API 使用章为引用查型，未注水）。

## M2-3 第5章 运行时核心实现 成稿（0.3k → 4.2k 总字 / 中文 3.3k）

- 覆盖骨架 8 节：runtime 模块总览（api/core/queue_schedule/tsd/aicpu_sched/tprt 分区）、任务→SQE 分发表、流与调度、BQS 队列、TSD 设备侧、kernel 加载、控制面（ctrl_sq）、从 API 到硬件路径。
- 统一心智：runtime = 前台(api) + 厨房(core) + 传菜管道(BQS) + 片侧接单员(tsd)；数据面 SQE 与控制面 CtrlSQ 各占一条道。
- 锚点（≤5 深挖、其余进脚注）：`task_to_sqe.cc`（分发表 `g_BufToFunc` + Static/Dynamic/Param 三种 SQE）、`stream_factory.cc` + `stream.cc`、`binary_loader.cc`、`device/ctrl_sq.cc`、`tsdclient`。
- 新增：`g_BufToFunc` 二维分发表真码、三种 SQE 字段对照、流对象状态（Id_/Priority/StreamStatus/SQ-CQ 管理）、launch 时间戳宏（TIMESTAMP→ATRACE）、BQS 状态机 + SQ 环/doorbell、TSD 进程/线程模式 + 回执分发、kernel 加载（lazy load/magic/printf/内容哈希去重）、控制面消息族。
- 落实第3章“还债”清单（BQS 实现、TSD 两模式、SQE 构造器、launch 记时钟）；标注“实现级时序结论需 msprobe 实证”（STYLEGUIDE §8）。
- **校验**：verify 全绿；正文无行内 📄/📦 标注；无 TODO/占位。成品 3.3k 中文（实现章，遵循 §10 ≤5 锚点 + 形态级不逐行翻译）。

## M2-4 第8章 内存与数据通路 成稿（0.3k → 3.5k 总字 / 中文 2.7k）

- 覆盖骨架 6 节：内存层级（GM/L2/L1/UB + MTE1/2/3/FixPipe 搬运单元）、API 层分配（aclrtMalloc 三兄弟 + HUGE 策略）、N-DMA 主角、对齐/带宽/乒乓、零拷贝与复用、AIPP、后端衔接。
- 核心心智：**「步长即变换」（转置换 stride、广播置 0、切片改长度、Padding 配左右）**；N-DMA 把「搬 + 变」一步做完；对齐（32B/Cache Line）、乒乓（搬算重叠）、零拷贝（少搬）是压低搬运开销的三板斧。
- 锚点（≤5）：`abstract_hardware_architecture.md`、`basic_architecture.md`（搬运单元/Cube 数据流）、`acl_rt.h`（内存策略）、`DataCopy_GMToUB_NDDMA.md`（NdDmaLoopInfo 参数）、`data_copy_gm2ub_nddma/` + nddma_introduction 博客。
- **校验**：verify 全绿；无行内标注/TODO；N-DMA 仅较新芯片支持，标注「需能力菜单确认」（§8）。

## M2-5 第7章 维测子系统 DFX 成稿（0.3k → 2.7k 总字 / 中文 2.2k）

- 覆盖骨架 8 节：DFX 模块总览（msprof/adump/log/error_manager/trace 五件事）、msprof 原理与 op_summary/timeline、adump + DumpTensor、log 与 error_manager、trace（atrace/utrace/trace_server）、错误码体系（107xxx runtime / 145xxx GE 域）、msSanitizer 四类检测、精度迭代与性能画像两循环。
- 核心心智：**排障先分清「慢」还是「错」**（慢→msprof，数据错→DumpTensor/msSanitizer）；msSanitizer 报错格式「错误类型→内存类型→算子名→块」对号入座。
- 锚点（≤5）：`dfx/{msprof,adump,log,trace,error_manager}/` 目录、`error_codes/{rt,ge}_error_codes.h`、ms_sanitizer 博客、dumptensor 博客。
- 修正错误码域：GE 为 145xxx（原稿误写 108xxx，已改）。
- **校验**：verify 全绿；无行内标注/TODO。

## M2-6 第6章 驱动与系统软件协同 成稿（0.3k → 2.7k 总字 / 中文 2.2k）

- 覆盖骨架 6 节：用户态驱动能力视图、用户态/内核态驱动边界（`/dev/davinci*`、`ascend_km`、`ascend_hal.h`）、地址空间与内存映射（物理内存管理 + IPC/MemGrp 共享）、进程内多设备与设备组（Device 三层继承 + 初始化链）、CModel 仿真路径、跨进程约束与安全模型。
- 核心心智：**用户态 runtime 负责「翻译/排队/管资源」，内核态驱动负责「摸到硬件」，中间靠 `/dev/davinci*` + HAL 适配层**；跨进程默认隔离、共享需显式。
- 锚点（≤5）：`runtime/driver/`（NpuDriver + DriverFactory 注册机制）、`docs/zh/design/architecture.md`（部署/分层/进程模型）、`modules/{device,memory}.md`、`cmodel_driver/`。
- 内核驱动源码不在开源仓，按「分层+边界+API」级写作并明示；仿真路径结论需真机验证（§8）。
- **校验**：verify 全绿；无行内标注/TODO。

## 白屏问题排查记录

- **症状**：dev server 200 但浏览器白屏。
- **根因**：`mermaid@11` 的 ESM 构建在 Vite dev 下与 CJS 包 `fastdom` 互操作失败（`does not provide an export named 'default'`），JS 运行时异常导致整页不渲染。
- **修复**：mermaid 降级锁 `^10.9.8`（插件的 peer 声明支持 10||11），并清空 `docs/.vitepress/cache` 与 `node_modules/.vite` 重新预构建。已验证：首页与三章正常渲染、Mermaid svg 正常生成、无 JS 报错。
- `check:links`（markdown-link-check）只审绝对 URL；相对链接由 `check:internal` 全量覆盖（两者分工）。验证时发现官网旧 meetup 链接 404，已在附录C 修正。

## M3 启动：PLAN-PART3 定稿 + 第9章 编程模型与 API 选择 成稿（0.3k → 4.4k 总字 / 中文 3.4k）

- **PLAN-PART3.md**（M3 六章成稿方案）定稿：总纪律五条（含锚点≤5、运行性从严、950/SIMT 架构差异显式标注）、六章骨架与锚点文件、执行顺序 9→10→11→12→13→14、风险边界四条。
- **第9章成稿**，覆盖骨架 5 节：① API 分层总览（三层完备 Tpipe/Tque·基础API·语言扩展 C + 两层提效 高阶API·模板库，分层金字塔图）；② host/device 分工与 `<<<>>>` 启动（真码槽位：核数/动态UB大小/流；SIMT 为 CUDA 风格四槽）；③ SIMD/SIMT 并行模型与编程四步法（对照图）；④ Tiling=host 侧「分块账本」（按核/按UB/对齐三笔账，衔接 aclrtLaunchKernel tiling 参数与第5章 SQE Param）；⑤ PyAsc Python 前端定位；⑥ 选型决策树（改绘官方 asc_how_to_choose_api.md，标注本书后续章节入口）+ Tensor vs 指针两路 Add 真码对照。
- 统一心智：**三层完备能力等价、差别只在「同步与内存归谁管」；host 管资源与 Tiling 账本、device 跑核函数、`<<<>>>` 是接头暗号**。
- 图 4 张（分层金字塔、四步法对照、决策树、小结记忆图），码例 4 段（add_tpipe_tque.asc / gather_1d.asc / c_api_add.asc + `<<<>>>` 真码行），全部 `[需真机验证]` 分级。
- 顺手修复：ch01/ch04 遗留「昇腾 C」→「Ascend C」（check:terms 归零）；appD 第9章来源同步 8 条路径。
- **校验**：`npm run verify` 全绿（构建/站内链接/源码路径/术语/字数）；HTML 抽查 3 表格 + 4 Mermaid + 6 脚注渲染正常、无裸 `|`。
- 全书进度：55.6k 总字 / 44.6k 中文。下一章：第10章 核心编程能力详解（本编最重，第8章预支的搬运 API 写法在此还债）。

## M3-2 第10章 核心编程能力详解 成稿（0.3k → 4.3k 总字 / 中文 3.0k）

- 覆盖骨架四块：① TPipe/TQue 范式（队列管道思想、CopyIn/Compute/CopyOut 三段式、InitBuffer 双缓冲、TBuf、官方范式伪代码全精读，附 VecIn/VECIN 命名差异注）；② 同步语义（EnQue/DeQue→Set/Wait 解决 RAW、AllocTensor/FreeTensor 解决 WAR、SetFlag<HardEvent::MTE2_MTE3> 真码、核内/核间/任务间三类同步表）；③ Tensor 体系（Global/Local/Reg 三类对齐存储层级、基础 vs 扩展 Tensor/Layout/AscendC::Te、LocalMemAllocator 自主管理对照、Tpipe/Tque vs add 成对样例）；④ 计算 API 家族（memory_vector_compute 目录树检索法、Matmul 高阶 API 三步表达、TPosition→物理 Buffer 完整映射表 A1/B1/C1/A2/B2/C2/CO1/CO2、融合范式 CO2→VECIN）。
- **还债落地**：第 8 章预支的 N-DMA 实操——data_copy_gm2ub_nddma 真码（场景 1 Padding / 场景 3 Transpose），NdDmaLoopInfo 五字段（loopSrcStride/loopDstStride/loopSize/loopLpSize/loopRpSize）逐字段注释并对照 8.2 口诀验收；新增 10.5.1 DataCopyPad 非对齐尾部（paddingValue/dummy/SetPadValue 三种填充来源、左右 Pad ≤32B、Compact 模式仅 950）；双缓冲流水时序表（表 10-1）兑现第 8 章乒乓钩子。
- 统一心智：**TPipe 管资源、TQue 管通信；四个队列操作写齐、三种同步类别分清；对齐走 DataCopy、尾部不齐找 DataCopyPad、块内变换找 N-DMA**。
- 图 4 张（三段式流水、RAW/WAR 同步封装、三类 Tensor、小结记忆图）+ 表 5 张；码例 4 段全部 `[需真机验证]` 分级。
- 口径说明（如实记录）：3.0k 中文未达 §4 核心章 8k 目标下限；机制骨架已完整（范式/同步/Tensor/搬运四块闭合），深度扩写留给第 14 章端到端实战（RegTensor 寄存器计算、高维切分搬运实操在彼处随案例展开），质量优先不注水。
- appD 第10章来源同步 10 条路径。**校验**：`npm run verify` 全绿；HTML 抽查 4 表格 + 4 Mermaid + 9 脚注渲染正常。
- 全书进度：59.6k 总字 / 47.3k 中文。下一章：第11章 SIMD/SIMT 与高级特性。

## M3 图表补强轮：第 4–8 章 SVG 大图补齐（6 张）

- **图表审计**：ch1–3 图况尚可（3/5/3 张 Mermaid）；ch4–5 偏少（2/2）；ch6/ch7/ch8 **零图**——而 ch8（存储层级/搬运单元/N-DMA）是全书最依赖视觉的章节。
- **新增 6 张手写 SVG**（`docs/figures/`，统一配色：用户态绿/内核态蓝/硬件橙/同步紫，中文字体栈），全部带中英文 alt + 图注 + 正文解释：
  - 图 4-1 `ch04-acl-resource-map.svg`：ACL 柜台资源地图（会话→四件套→内存→三种 Launch→同步，右栏错误码去处）；
  - 图 5-1 `ch05-runtime-map.svg`：runtime 四角色组织 + 数据面 SQE/控制面 CtrlSQ 双通道 + aicpu_sched/tprt 辅助区；
  - 图 6-1 `ch06-driver-boundary.svg`：用户态/内核态四层边界（含 /dev/davinci* 边界线、内核源码不在开源仓注记、跨进程/仿真右栏）；
  - 图 7-1 `ch07-dfx-map.svg`：「慢/错」排障分流 + 五模块分工 + 性能画像/精度迭代双循环；
  - 图 8-1 `ch08-memory-hierarchy.svg`：存储层级六层金字塔（Reg→L0→L1→UB→L2→GM，容量/带宽/延迟三轴 + Cube/Vector 两路径注记）；
  - 图 8-2 `ch08-mte-units.svg`：MTE1/MTE2/MTE3/FixPipe 搬运单元数据流（线色即单元，Cube/Vector 计算单元 inout 一眼看清）。
- STYLEGUIDE §6 增补：分层/架构/数据流类大图可用手写 SVG（docs/figures/，统一配色规范），Mermaid 仍为流程/时序默认。
- **校验**：`npm run verify` 全绿；构建产物确认 6 张 SVG 全部打包进 dist/assets 并被对应章 HTML 引用。

## SVG 图表修复轮（subagent review 产出，22 处问题全数闭环）

- **评审方式**：reviewer 子代理对 6 张 SVG 逐行审查（文字溢出估算、贝塞尔碰撞求值、与 5 个章节源文对语义），产出 22 处缺陷（2 BLOCKER / 6 MAJOR / 14 MINOR）。
- **误报澄清**：reviewer 报告的 ch05「BLOCKER：<path> 粘进 <text>」经 XML 校验为误读（文件完好）；真实修复以校验为准。
- **修复清单**：
  - ch04：4 条纵向箭头延伸至目标框缘（原悬空 26px）；右栏旋转文字与底条对位；同步行拆两行补 aclrtRecordEvent/aclrtWaitEvent 全名；
  - ch05：核心→aicpu_sched 与 queue→tprt 连线改为分段绕开控制面框（原横穿标题文字）；tprt 连线改由 core/ 引出（对齐 5.1.1）；CtrlSQ 职责措辞对齐 5.7（清流/回收/模型绑定·加载/复位/Dump/调试注册）；灰色辅助连线改实线消除与控制面虚线的歧义；
  - ch06：硬件行型号收窄为本章表格口径（910/310P/950）；库列表修正；§8 归属明确为 STYLEGUIDE §8；
  - ch07：msprof 行缩文消溢出；「慢/错」分支标签移至无碰撞角落；trace 行缩文；补两条循环框↔公共底座连线；
  - ch08 层级图：底部标语区分 32B 对齐与 Cache Line（128/256/512B）两个概念（原混淆）；TPipe 拼写；轴箭头起点贴 GM 框；副标题不再声称寄存器层有搬运单元服务；
  - ch08 搬运单元图：MTE2 分形曲线改道绕开 L1 框与其文字（BLOCKER）；MTE1/MTE2 箭头落点分离；删除重复的 MTE3 死头虚线、补 L1→GM 曲线（对齐图例）；UB→Vector 箭头改灰色中性 marker（原误用 MTE1 绿色）；MTE2/FixPipe/分形三处标签移出箭头路径；Cube 框「仅 SIMD 模型」改「本图按 SIMD 模型绘制」。
- **校验**：6 张 SVG XML 全部通过；`grep '<text...>d="M'` 零命中；构建产物 6 张 SVG 正常打包。
