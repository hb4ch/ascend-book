# CH25 EVIDENCE-CLOSE 回应

2026-10-10。逐项对应 `management/tasks/CH25-EVIDENCE-CLOSE.md`；所有"已改"均以终态文件 rg 实测为准（文末计数）。未动 24 章任何文件；未 commit。

## 1. 可读性优先、精简提纲 → `CH25-OUTLINE.md` rev2 重写

- 删除：43-pass 逐项表、new-IR 七步逐项表、CompStage 六阶段矩阵图、标量参数旁支（B7）、`@frontend.function` 内联旁支（B8）、独立"MPMD/工具链"节。
- 保留机制恰 4 个：前端约定（25.2）／两级编译与切图（25.3）／生成 CCE 调 PTO（25.4）／三路执行（25.5）；主线单例 abs_kernel（正文统一称**4 行有效代码**，`grep -c '9 行\|九行' CH25-OUTLINE.md` = 0）。
- 图 3→2；节点写动作，文件/长符号入脚注（OUTLINE 图规划表与 25.1 注明）。
- 篇幅目标改 4.5k–6k，明写"不强制 8k"。

## 2. F1/E6/F5 矛盾 → 实门控回源（EV §E3/E4/J）

- **bisheng/落 cpp 双门**：`codegen_npu.cpp GenCode` 内 `#ifdef BUILD_WITH_CANN` + `getenv(ASCEND_HOME_PATH)` 才 `GenCodeToBinaryTask`（.cpp 落盘在其 `DumpCode`）——无 CANN 连 cpp 不落；`BUILD_WITH_CANN` 默认 ON 但属构建选项（CMakeLists 注释「Need to install CANN package…」）。已写入 E3。
- **"SIM 完整 compile"改口**：compile 阶段是否产 CCE 与 run_mode 无关、只随 BUILD_WITH_CANN/ASCEND_HOME_PATH（EV§J4）；纯 host cost-model 路（`_run_with_cpu`→`CostModelAgent`，backend.cpp:33+，platform 开关 `KEY_ENABLE_COST_MODEL`）不需 bisheng——但**不得由 CPU 跑通反推无工具链依赖**，已按此措辞。
- **三件事分账**（EV§J3）：run_mode 三来源优先级（用户显式→`ASCEND_HOME_PATH`判定→`CAMODEL_LOG_PATH`覆写 SIM，`entry.py` L641-643 `cannsim_is_configed` 实测）；无 NPU（torch.npu 不可用即 `FeError`）/无 CANN（自动 SIM 仅性能仿真）/无 bisheng（无 cpp 产物）各自独立。
- **C++ 侧同入口不同设备**：`kernel_binary.cpp` 构造器 `CFG_RUN_MODE==SIM→EslModelMemoryUtils` else `DeviceMemoryUtils`；`InitDeviceArgs` SIM 跳过 LoadAicpuOp/DevicePerf/Adump——`LaunchKernelTorch`≠真设备（EV§J1/J2）。

## 3. GetPtoTileLibPathByEnv 亲查 + 主例表述修正

- **env 语义**：原函数首句 `if (!…GetCodeGenConfig(KEY_CODEGEN_SUPPORT_TILE_TENSOR, false)) return "";`——**PTO include 注入仅在 tile-tensor 布局模式（默认 false）**；其后 `envPath = homePath + "/include"` 且断言 `…/include/pto` 存在 ⇒ **环境变量指 pto-isa 仓库根（含 include/ 的目录），非 include 目录本身**。E4 重写，另补 whl install 证据（`CMakeLists.txt:180-186` tileop/tilefwk 整目录装运；pto-isa 不在 pypto 安装清单，是否随 CANN 分发未核——如实注明）。
- **行数**：全文改"4 行有效代码"。
- **shape3×tile(2,8) 尾块**：新增 EV§K——`tile_shape_resolver.h:23-26`"clamped to the operand's own shape (elementwise)"；码期三层形状 `shape=dynamicValidShape / stride=BuildStride(rawShape)`（`codegen_op_npu.cpp UpdateTileTensorShapeAndStride`）＋设备侧 exec-tile（`AssignElementwiseOperandExecTile`）＝**容量 tile+有效收缩**表达尾块，与 ch24 合同同构；约束侧引 tiling.md（尾轴 32B 对齐、(T/S)×(1+输入)<18000、维数≤5）。tile 两维对一维的精确配轴**未逐行核，EV§K4 明注不写映射式**。
- 落地链补全：`pypto.abs`→`pypto_impl.Abs`（op/math.py）→`OP_ABS→GenUnaryOp`（codegen_op_npu.cpp）→`OP_TILE_OP_ABS TAbs`（tileop/vector/unary.h:400）→`pto::TABS`（EV§K1-K3）。

## 4. accuracy_level=2 ≠ 真实 NPU

- `entry.py:651` 分支仅要求 `ASCEND_HOME_PATH`（CANN **安装**）+`get_torch_npu()`；设备事实由 C++ `CFG_RUN_MODE`+CAMODEL 包装决定：`_execute_kernel` 开头 `CAMODEL_LOG_PATH→run_mode=SIM`。EV§J2 给全链；正文 25.5 以"同一入口、三种设备事实"组织并点题。
- SIM 能力按文档原义分述（EV§F5）：性能仿真=泳道图无设备；精度仿真依赖 CANN；950 cannsim 两档（CostModel 泳道/CAModel trace_core+chrome://tracing）；"精度仿真与 NPU 执行一致"标注为文档声明非本书实测。不再写"都不提供"类笼统话。

## 5. 复现纪律 → EV§L 重写 + 检查日志

- `build_ci --clean` 明写**副本目录**（`cp -a … /tmp/pypto-build`）执行，不在只读源仓。
- py_compile 统一 `PYTHONPYCACHEPREFIX=/tmp/ch25-pycache`，pyc 不落源树。
- 已执行检查留痕：`management/validation/ch25-evidence-close-check.log`——`git status --short` 干净、`git log -1`=883e7df、py_compile OK（pyc 树根 `home/mnt` 于 /tmp 下）；源树遗留 `examples/**/__pycache__/` 系前次检查产生，按"不清理"保留。
- 未清理源仓任何文件。

## 终态 rg 自查（ascend-book/management/）

```
rg -c '9 行|九行' CH25-OUTLINE.md                       → 0
rg -c '43-pass 逐项|六阶段矩阵' CH25-OUTLINE.md          → 1（仅"删除说明"句）
rg -c 'PTO_TILE_LIB_CODE_PATH' CH25-EVIDENCE.md          → 2（E4/L 无？实为 E4；L 无 env）
rg -c 'BUILD_WITH_CANN' CH25-EVIDENCE.md                 → 3（E3/J4/L）
rg -c 'clamped' CH25-EVIDENCE.md                         → 2（K4）
rg -c 'PYTHONPYCACHEPREFIX' CH25-EVIDENCE.md             → 2（H2/L）
rg -c 'LaunchKernelTorch' CH25-EVIDENCE.md               → 4（F1/J1/J2/F3 关联）
rg -c 'TAbs' CH25-EVIDENCE.md                            → 3（K2/K3）
rg -c '不强制 8k' CH25-OUTLINE.md                        → 1
```
（以上为撰写时计数，终态以文件为准；关键项已复核。）
