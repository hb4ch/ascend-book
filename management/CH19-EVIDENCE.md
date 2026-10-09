# CH19 证据表（CH19-EVIDENCE）

> 2026-10-09。固定源基线（SOURCE-BASELINE 同批快照）。类型 S=源码/D=文档；性能数字全部**仓内引用或离线算术**，无实测。ch16–18 已述内容只回指不重复。

## 一、文件级锚点（5）

| # | 文件 | 行数 | 角色 |
|---|---|---|---|
| A | `runtime/src/dfx/msprof/`（collector/dvvp analyze+profimpl、inc/prof_acl_api.h） | 库 | **msprof 服务侧**：采集/解析/频率/枚举（S） |
| B | `asc-devkit/docs/zh/guide/programming_guide/debug_and_tuning/performance_tuning.md` | 233 | msopprof 上板/仿真流程与 csv 族权威描述（D） |
| C | `asc-devkit/examples/01_simd_cpp_api/05_best_practices/00_vector_compute/add_high_performance/README.md` | ~420 | **7-case 调优链＋全指标表**（观测→解释范式，本章主案例） |
| D | `asc-devkit/examples/01_simd_cpp_api/01_utilities/04_profiling/`（README＋msprof.asc＋torch_library_report_tensor） | — | 工具边界/安装前提/timeline 关联 Tensor 的 API（aclprofTensorInfo 族） |
| E | `pto-isa/docs/coding/opt_zh.md` | 149 | 阶段化性能模型与调优纪律（TLOAD/Transform/Compute/STORE） |

辅助：`runtime/.../dvvp/analyze/inc/data_struct.h`（hwts/OpPMU/TsProfile 结构）、`analyzer_base.{h,cpp}`（频率换算）、`config_manager.{h,cpp}`（频率表）、`FixpipeOut.h` 无关；`simd_simt_high_performance/README`（SIMT 指标表，AIC/AIV 分列佐证）。

## 二、工具三分与命令（均有本地文档证据，不臆造 CLI）

| 工具 | 定位 | 证据 |
|---|---|---|
| **msprof**（服务/框架） | runtime 采集框架：`aclprofStart/Stop`＋`ProfAicoreMetrics` 9 项枚举（`PROF_AICORE_{ARITHMETIC_UTILIZATION,PIPE_UTILIZATION,MEMORY_BANDWIDTH,L0B_AND_WIDTH,RESOURCE_CONFLICT_RATIO,MEMORY_UB,L2_CACHE,PIPE_EXECUTE_UTILIZATION,MEMORY_ACCESS}`，prof_acl_api.h L27-40） | A S |
| **msopprof**（单算子上板） | `msopprof ./demo`；可选 `--aic-metrics=PipeTimeline`（matmul_gelu README L320 同款）→`OPPROF_{ts}_XX/`csv 族 | B L20-46/C L336 |
| **msopprof simulator** | 仿真流水（**仅 SIMD，SIMT 不支持**，B L127）；产物 `visualize_data.bin/trace.json` | B L230 |

安装边界：msOpProf **需 CANN 商用/社区版**（C/04_profiling README L72 引官方安装指南链接）——本书未安装未运行。

**csv 族字段（B L42-58 原文）**：`ArithmeticUtilization`(cube/vector cycle占比)、`L2Cache`(命中率)、`Memory`(UB/L1/主存 GB/s)、`MemoryL0`、`MemoryUB`、`OpBasicInfo`、`PipeUtilization`(计算/搬运耗时占比)、`ResourceConflictRatio`(bank group/conflict)、`dump/`。**指标枚举↔csv 对应**：PIPE_UTILIZATION 版本分岔——`CHIP_V4_1_0` 时映射 `PipeUtilizationExct`（config_manager.cpp L102-06）。

## 三、指标口径：分母与单位（全部 S 级）

| # | 条目 | 证据 |
|---|---|---|
| E1 | **Task Duration＝调度到加速器＋执行＋响应结束**（C add_high_perf 表；simd_simt README L77 同）——**非纯核时间**；`aiv_time` 才是核上执行。二者差=调度/响应开销 | C L62/D |
| E2 | **除 Task Duration 外全部指标=所有 Thread Block 平均**（simd_simt README L88 原文）——多核均值掩盖核间方差；负载不均须另看 timeline | D 系 |
| E3 | **ratio 分母=total cycle**（「xx cycle数在 total cycle数中的占比」C L69-77）——各 ratio**可>1 和**（重叠），**不可相加为 1**；实例：case4 `0.973+0.33+0.05+0.011>1`（C 数据行） | C |
| E4 | 时间单位换算：`op time=(syscnt/frequency)`，frequency 由 `ConfigManager::GetFrequency()/1000→GHz`（analyzer_base.cpp L74-85 注释原文「syscnt*(1/ghz)=ns」）；**频率是平台查表非实测**：`FREQUENCY_TYPE`（config_manager.h L53-72，如 CLOUD=100、MINI_V3=48 等，单位 MHz） | A S |
| E5 | **AIC 频率另表**`AIC_TYPE`（同 h L76-99，CLOUD=800/MINI_V3=1250…）且运行时经 `DrvGeAicFrq(devId)` 实测覆盖（op_analyzer.cpp L85-91「aic and aiv with the same frequency」）——**配置表 vs 实测两套，档位差异须在正文声明** | A S |
| E6 | 核级事件=hwts Type01/02（`HwtsProfileType01/2`：taskId+syscnt+blockId，64B；START=0/END=1，data_struct.h L118-46）——**timeline 的原子是每核 start/end 对**，Task Duration 由其聚合；`OpPMU{start,end,totalCycle,pmu[8]}`（L57-61） | A S |
| E7 | **时间线事件↔算子定位**：host 侧 `aclprofRangePushEx`＋`aclprofTensorInfo`（input/output 类型/Format/shape）→msopprof `PipeUtilization.csv` 展示 tensor（04_profiling/torch README L63-80 原文 API 名）——**timeline 上认算子靠显式打点，非自动** | D S |

## 四、案例链（C：add_high_performance，7 case 全数字，本书仅离线复算）

数据行（Task Duration/aiv_time/vec/scalar/mte2/mte3，μs 与 ratio；C 原表）：

| case | 配置 | TaskDur | aiv_time | vec | scalar | mte2 | mte3 |
|---|---|---|---|---|---|---|---|
| 0 | 单核标量 | 1239689.1 | 同 | 0.015 | 1233742(.995) | 5916(.005) | 2485(.002) |
| 1 | 单核向量 | 6909.6 | 6909.14 | 761(.11) | 231 | 6208(.873) | 2613 |
| 2 | 多核48小块 | 306.58 | 297.14 | 15.9 | 8.2 | 215(.725) | 54 |
| 3 | 大块×4 | 268.5 | 261.5 | 12.8 | 2.8 | 184(.705) | 57 |
| 4 | +双缓冲 | 264.02 | 257.56 | 12.8 | 2.8 | **250(.973)** | 85(.33) |
| 5 | +L2 bypass | 187.68 | 185.15 | 12.8 | 4.5 | 176(.951) | 160(.866) |
| 6 | +防bank冲突 | **184.52** | 178.49 | 6.95 | 3.4 | 171(.961) | 121(.68) |

**观测→候选解释→需补证→实验变量**（本章范式演示，逐条标置信）：
- 0→1（**99.4%↓**）：scalar 1234ms→231μs——解释「向量单元并行度」**成立**（同数据同核）；需补证：无（同核同量对照）。
- 1→2（95.5%↓）：48 核并行——解释成立但**引出 E2**：306 vs 297 差=调度；mte2 6208→215 非 48 倍线性（每核数据÷48＋带宽摊薄）——**需补证**：Memory.csv 实测带宽曲线；实验变量：核数扫描。
- 2→3：大块搬运 mte2 215→184μs——README 归因「更大连续块利用带宽」**相关性成立、因果未证**（未给带宽数）；补证：Memory.csv 单调性＋L2 命中率；变量：块尺寸扫描。
- 3→4：双缓冲 mte2 ratio .705→**.973**但 Task 仅 268→264——**重叠增加≠时间等比降**（mte3 反升 57→85）：典型「占比挪移」，正文示例「重叠不代表列可加」。需补证：PipeTimeline 时间轴视觉。
- 4→5：L2 bypass 264→187μs——`SetL2CacheHint(CACHE_MODE_DISABLE)`（C L365-6 真码）；解释「一次读数据 bypass 直达」——**需补证** L2Cache.csv 命率对比；变量 bypass 开关。
- 5→6：bank 冲突消除 187→184.5（vec 12.8→6.95 减半）——`ResourceConflictRatio.csv` 直接对应；小幅 task 收益说明冲突非主瓶颈——**负结果也有价值**示范。

**离线算术演示（可留日志）**：case6 数据 8192²half×3（2 进 1 出）=402.7MB/184.52μs≈**2.18TB/s 有效**——**前提假设**：三流全计、无缓存重读；仅演示算式，非实测带宽（脚本+log 落 validation/）。

## 五、多核/扩展性与反模式（E 补）

- `pto-isa` 阶段模型：TLOAD/Transform/Compute/STORE 占比判读（feed-limited/Cube 饿/带宽饱和三诊型，E §1 原文）＋纪律：一次一杠杆、warmup/drain 剥离、同 shape 回归（E §2）——**方法论骨架**，引为 ch19 闭环节。
- 负载均衡：add case2 「均匀切分＋余数前置」防尾核（C L~215 原文）；SIMT 表（D 系）aiv_*单列——**AIC/AIV 指标前缀分核族**（aic_*表同构，matmul_gelu 已用 aiv_mte2）。
- 需补证/未知：①msopprof csv 生成器代码不在本仓（列名权威=README，解析实现 U）；②950PR/DT 对应 PlatformType→freq 表行未映射（CHIP_V4_1_0=50/800?待核，U）；③`DrvGeAicFrq` 运行时值无法离线知；④simulator 仅 SIMD；⑤`pmu[8]` 各计数语义未文档化（U）。

## 六、与 ch16–18 边界

ch16 表16-1 频率标注/四层口径、ch17 matmul_gelu msopprof 用法与 aiv_mte2 −82% 案例、ch18 性能采集方法——ch19 只**收编为口径引用**，新内容=工具链全图/字段字典/七 case 调优链/timeline 定位/多核扩展性方法论。
