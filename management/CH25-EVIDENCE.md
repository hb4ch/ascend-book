# CH25 证据集 —— PyPTO：Python DSL 到 PTO 的编译栈（第 25 章）

rev2（2026-10-10，EVIDENCE-CLOSE 修订）。任务：`management/tasks/CH25-RESEARCH.md`、`CH25-EVIDENCE-CLOSE.md`。
相对 rev1 的修正：E4/E6/F1/F5 按实测门控收窄（tile-tensor 开关、BUILD_WITH_CANN/ASCEND_HOME_PATH 门、LaunchKernelTorch≠真设备、SIM 两路分离）；新增 §J 运行门控矩阵、§K abs→TAbs 落地链与尾块语义、§L 复现纪律。环境与运行类结论以 2026-10-10 实测为准（§H）。
纪律：只陈述"源码/文档怎么说"；DSL 语义（§B）、编译器实现（§C–E）、运行边界（§F–J）分账；未实测不写、不推断。

---

## A. 仓库定位与自述

| # | 论断 | 证据 |
|---|------|------|
| A1 | 定位：Python DSL → tile 层，经 CodeGen 生成 PTO 虚拟指令 | `README.md:20`「编译结果通过 CodeGen 生成底层 PTO 虚拟指令代码」；四层架构 `docs/zh/tutorials/introduction/introduction.md`；官方编译流程图说明 `docs/zh/tutorials/debug/debug.md`「Tensor Graph、Tile Graph、Block Graph 阶段会经历多个 Pass 的优化，最终通过 Execute Graph 阶段整合图信息，编程生成最终的硬件执行图」「具体 Pass 列表请参见：framework/src/passes/pass_mgr/pass_manager.cpp」 |
| A2 | 三大块：python 前端 / framework C++ / examples·docs | 顶层实测（rev1 不变） |
| A3 | Tile Graph 语义（官方）：Tensor 按 TileShape 展开为 Tile/TileOp，自动推导存储位置并插入搬运（TILE_COPY_IN/OUT）；Block Graph 切到单核并做指令编排/片上内存分配/同步插入 | `debug.md` 图编译流程节四条 bullet 原文 |

## B. DSL 语义层（不变，rev1 已核）

B1 主例 `elementwise_ops.py:76-80`（4 行有效代码：装饰器+def+set_vec_tile_shapes+赋值）；B2 `[]` 注解=不校验形状（`entry.py:690`）；B3 dtype 强校验；B4 out 约定无返回值；B5 `set_vec_tile_shapes` 用户侧提示；B6 RunMode NPU=0/SIM=1（`runtime.py:38`）且可被环境倒逼；B7 标量参数独立通道；B8 `@frontend.function` 内联。均见 rev1 摘要与原文件，行号未变。

## C. 编译入口与 Python 侧管线（不变）

C1 惰性编译（`entry.py:1219` defer）；C2 首调即编、`new_ir=True` 为代码默认（`entry.py:1144`，docstring"False"过时）；C3 new-IR 七步 `compile_pipeline.py:29-45`；C4 IR dump `LogTopFolder()/TensorGraph/IR`；C5 旧 Parser 通路；C6 缓存键；C7 `_set_config_option` 六组透传；C8 `CompStage` 六阶段 Python/C++ 对齐（`config.py:24-31`、`config_manager_ng.h:73-82`）。

## D. C++ Pass 流水线（不变）

D1 `PVC2_OOO` 43-pass 全序（`pass_manager.cpp:80-126`）；D2 策略注册/按架构过滤；D3 阶段哨兵 `ExpandFunction→CS_TENSOR_GRAPH`、`SubgraphToFunction→CS_TILE_GRAPH`（`pass_manager.cpp:287-288`）+ codegen 侧 `CS_CODEGEN_INSTRUCTION` 截断；D4 注册表/RunPass/断点续跑；D5 三层 pass 目录、`insert_sync.h:468`；D6 依赖静态校验。**正文呈现方式按 OUTLINE rev2 精简，不逐项列表。**

## E. CodeGen 与 PTO 连接（rev2 修正）

| # | 论断 | 证据 |
|---|------|------|
| E1 | CodeGen 按代际分派 | `codegen_factory.h:38-42`：`DAV_2201/DAV_3510`→cloudnpu，`IsLiteNPU`→litenpu |
| E2 | 生成 CCE 骨架 | `codegen_npu.cpp GenInclude`：`#include "TileOpImpl.h"` + `#include "tilefwk/aicpu_common.h"`；`GenFuncHeader`：`extern "C" [aicore] void <magic>_<hash>_<sub>_<tiling>(GM_PARAM_TYPE_FOR_DYN* param, int64_t GMStackBase, __gm__ int64_t* hcclContext, __gm__ TaskStat* taskStat)`；内核名确定性位域（`codegen_npu.h:44-58`） |
| E3 | **CCE 落盘与 bisheng 编译有双门** | `codegen_npu.cpp GenCode`：`#ifdef BUILD_WITH_CANN` 且 `getenv(ASCEND_HOME_PATH)` 才 `GenCodeToBinaryTask`（.cpp 落盘在其中的 `DumpCode`）与 `ExecuteParallelCompile`（生成 `Makefile_<magic>_<hash>.compile` + `make -j`）。`PrepareCmd`：`bisheng -c -O3 -g -x cce -std=c++17` + `-D__AIC__/-D__AIV__` + `-D__DAV_V220/-D__DAV_V310` + `--cce-aicore-arch=dav-c{220,310}-{cube,vec}`。`BuildIncludes`：`-I <pto?> -I …/tilefwk -I …/tileop -I …/tileop/arch32 -I …`。**无 CANN 环境连 .cpp 都不落盘**；`BUILD_WITH_CANN` 为 CMake option 默认 ON（`CMakeLists.txt:193` 附近「Need to install CANN package and set corresponding environment variables」）。`CS_CODEGEN_INSTRUCTION` 阶段只出 cpp 不编译（`CompileCode`） |
| E4 | **PTO 头注入是条件性的（tile-tensor 模式）** | `GetPtoTileLibPathByEnv()` 首句 `if (!…GetCodeGenConfig(KEY_CODEGEN_SUPPORT_TILE_TENSOR, false)) return "";`（`config_manager.h:93`「if true, gen code with layout mode」，默认 false）。开启后：优先级 1 `PTO_TILE_LIB_CODE_PATH`（`codegen_npu.h:36`）——**env 值 = pto-isa 仓库根（含 `include/` 的目录）**，`envPath=homePath+"/include"` 且断言 `IsPathExist(envPath+"/pto")`；优先级 2 `ASCEND_HOME_PATH+"/include"` 同要求；否则 assert「Pto-isa path not found. please install pto-isa properly.」 |
| E5 | pto 头被设备层头链包含 | `tileop_common.h:39` `#include "pto/pto-inst.hpp"`（被 `arch32/dynamic/{vector_dyn,mte_dyn,cube_dyn,aicpu_call}.h`、`distributed/common.h` 包含）；`tileop_shmem.h:26` `#include "pto/comm/pto_comm_inst.hpp"`；`vector/unary.h:18` `#include "pto_tile.h"`。设备 tileop 层：`interface/tileop/{vector/,cube/,arch32/}`。**whl 安装面**：`CMakeLists.txt:180-186` 注释「tileop/tilefwk 目录……均为运行时编译 aicpu/aicore 所需二进制依赖」，`install(DIRECTORY framework/src/interface/tileop/ DESTINATION …/lib/include/tileop)`；**pto-isa 自身不在该 install 清单**（是否随 CANN 包分发未在 pypto 仓内核实——不写死） |
| E6 | 内存落点 `get_imm`；AICPU 编码为操作码流 | （rev1 不变）`GenAlloc`：`UB_S<start>_E<end> = …get_imm(0x…)// size`；`HandleForAICpuSubFunc` op→int 编码 |

## F. 运行时三分支（rev2 修正表述）

| # | 论断 | 证据 |
|---|------|------|
| F1 | Python 侧分派（`entry.py _execute_kernel`，L638 起）：①`CAMODEL_LOG_PATH` 存在→强制 run_mode=SIM；②run_mode==NPU→`pypto_impl.LaunchKernelTorch`；③else：`accuracy_level==2 且 ASCEND_HOME_PATH`→`get_torch_npu()+LaunchKernelTorch`；否则 `DeviceInit()+compile+_run_with_cpu` | 原文实测（rev1 引文不变）。**注意②③同名入口 `LaunchKernelTorch`，设备行为由 C++ 侧 `CFG_RUN_MODE` 决定（§J2），入口名≠设备事实** |
| F2 | CPU cost-model 路径 | `_run_with_cpu`（L1063）→`_cost_model_run_once_data_from_host`（L29 import）→C++ `CostModelAgent`（`framework/src/cost_model/simulation/backend.cpp:33+ BuildCostModel/SubmitToCostModel/RunCostModel`），入口 `ExecuteSimulation` 带 platform 开关 `KEY_ENABLE_COST_MODEL`（默认 true）；参数含 `-a accLevel`（`GetSimConfig(KEY_ACCURACY_LEVEL, 2)`，backend.cpp:38） |
| F3 | NPU 执行链 | `GetWorkSpaceSize→torch.empty(uint8)→OperatorDeviceRunOnceDataFromDevice(…stream, ws_ptr, ctrl_cache)`；`_run_with_npu` 跨设备切换（rev1 不变） |
| F4 | run_mode 常量 | `config_manager_ng.h:74-77` `CFG_RUN_MODE`/`CFG_RUN_MODE_NPU=0`/`CFG_RUN_MODE_SIM=1` |
| F5 | SIM 两路语义（官方文档原义） | `docs/zh/tutorials/debug/debug.md` CPU 仿真节：**性能仿真=核内流水数据（泳道图 merged_swimlane.json），无设备可用**；**精度仿真=CPU 上获取运算结果，依赖 CANN 软件包**；「若仅需要运行仿真……请勿安装 TorchNPU，否则可能运行失败」；run_mode 选择逻辑：显式 SIM→先性能仿真，检测到 CANN 再精度仿真；自动识别（无 CANN）→仅性能仿真、有 CANN→真硬件优先。950 系经 `cannsim record`：CostModel（任务级，泳道图）/CAModel（指令级，`trace_core*.json`+chrome://tracing，`accuracy_level=2`）两档；两档均「精度仿真与 NPU 执行一致」（文档原句，设备等价性为文档声明，非本书实测） |
| F6 | 调试档位 | `config_manager_ng.h:96-101`：compile_debug 0/1/2(fixed CCE)、runtime_debug 0-4（1 swimlane/2 AICORE_MODEL/3 依赖校验/4 GM 越界→`GenDDRChecker`+`GenGmCheck` 生成 `CheckInvalidAccessOfDDR…trap()`）；`debug.md` NPU 上板调试节：`compile_debug_mode:1` 产出 `Pass_<NNN>_<name>/{Before,After}_….json` 四层图样例（Tensor/Tile/Block/Execute） |

## G. 适用边界（rev1 不变）

G1 动态 shape 链（SymbolicScalar/DYN→dynamic_axis→finalize_dynamic_function/DYN_ATTR_TO_STATIC/INFER_DYN_SHAPE→`GET_PARAM_*_BY_IDX`）；G2 dtype 显式才校验+FP4 ×2；G3 NZ 仅 NPU 校验/uint8 豁免；G4 连续/禁 DTensor；G5 同步=INSERT_SYNC pass+设备 sync op；G6 内存=pass 分配+`get_imm`；G7 `[]` 不锁形状。

## H. 本机环境实测（2026-10-10）

| # | 事实/检查 | 证据 |
|---|------|------|
| H1 | python 3.11.9、torch 2.8.0+cu128；无 CANN（无 `ASCEND_HOME_PATH`/`/usr/local/Ascend`）、无 pybind11、`python/pypto/lib/` 不存在 | rev1 实测不变 |
| H2 | 已做：`PYTHONPYCACHEPREFIX=/tmp/ch25-pycache python3 -m py_compile examples/01_beginner/{compute/elementwise_ops,basic/basic_ops}.py` → OK；pyc 全落 /tmp，源树零写入 | `management/validation/ch25-evidence-close-check.log`（含 `git status` 干净、`git log -1`=883e7df） |
| H3 | 结论：本机不能跑 NPU/SIM/编译链；运行类表述转述文档+代码，不冒充实测。源树 `examples/**/__pycache__/` 系前次（无前缀）检查遗留，按"不清理源仓"纪律保留未动 | H2 日志 |
| H4 | **复现纪律（rev2）**：①不在只读源仓内 build——先 `cp -a pypto /tmp/pypto-build`（或 git clone 本地路径）再在副本 `python3 build_ci.py …`/`pip install -e . --no-build-isolation`；②语法检查一律 `PYTHONPYCACHEPREFIX=<tmp> python3 -m py_compile …`；③`git -C <源仓> status` 只读核对；④SIM 运行命令（`elementwise_ops.py abs::test_abs_basic --run_mode sim`）须在构建成功的副本环境，本机未满足→只给出不贴输出 | `CMakeLists.txt` option 注释、`build_ci.py -h`、H2 |

## I. 写作纪律映射

I1 先例后抽象；I2 PTO 连接只引 E4/E5（含条件门控，不写"必须常备"）；I3 无性能数字；I4 与 ch24 桥=E4/E5/E6，TileConfig/TLOAD 不重讲；I5 docstring 矛盾注明；**I6（新增）用户可读性优先，不强制 8k：机制保留输入→IR→切图→生成调用→执行主线，旁支与长符号入脚注**。

## J. 运行门控矩阵（EVIDENCE-CLOSE 核心增补）

| # | 门 | 证据 |
|---|------|------|
| J1 | **C++ 侧按 `CFG_RUN_MODE` 分派，同一 `LaunchKernelTorch` 入口两种设备事实** | `kernel_binary.cpp`（`machine/runtime/runner/`）构造器：`if (CFG_RUN_MODE == CFG_RUN_MODE_SIM) { EslModelMemoryUtils esl{true,true}; DeviceLauncher::FillDeviceKernelArgs(esl,…); } else { DeviceMemoryUtils…; }`（约 L82-96）；`InitDeviceArgs` once-call 内 `if (CFG_RUN_MODE != SIM) { LoadAicpuOp…; DevicePerf…; AdumpRegExceptionDump(); }`（约 L573）——SIM 跳过真设备 AICPU 内建 op 加载与性能 dump。launcher 家族实测目录：`emulation_launcher/eslmodel_launcher/aicore_model_launcher/device_launcher/launcher_router` |
| J2 | **accuracy_level=2 分支的设备事实** | `entry.py:651` 仅要求 `ASCEND_HOME_PATH` 存在（CANN **已安装**，非设备在场）+`get_torch_npu()`；真跑真仿由 C++ `CFG_RUN_MODE`+CAMODEL/cannsim 外层决定：`_execute_kernel` 开头 `CAMODEL_LOG_PATH`→run_mode=SIM（cannsim record 包装器注入，`simulation.md` 配置参考 `framework/src/cost_model/simulation/config/`）。**结论：`LaunchKernelTorch` 不自动等于真实 NPU 执行；判设备看 run_mode 与是否 cannsim 包装，不看出入口名** |
| J3 | **run_mode 三来源优先级（实测代码序）** | ①用户 `runtime_options.run_mode`（校验∈{NPU,SIM,0,1}，`_set_run_mode` L890+）；②未给时 `ASCEND_HOME_PATH`→NPU（并要求 `torch.npu.is_available()`，无设备即 `FeError("NPU is not available.")`）否则 SIM；③`_execute_kernel` 内 `CAMODEL_LOG_PATH` 存在→覆写 SIM（L641-643 `cannsim_is_configed`） |
| J4 | **compile 是否落 CCE/调 bisheng 与 run_mode 无关，与 BUILD_WITH_CANN+ASCEND_HOME_PATH 持钩** | E3；即"CPU 跑通 cost-model"不蕴含"无需 CANN 工具链"——纯 host cost-model（F2）确不需 bisheng，但精度仿真/Esl 仿真（J1）与任何 .cpp 产物需要。**不得由 CPU 执行反推无工具链依赖** |
| J5 | SIM 设备仿真的载体 | `KernelBinary` SIM 分支用 `EslModelMemoryUtils`/`EmulationLauncher`（J1）；`BuildControlFlowCache` 走 `EmulationLauncher::BuildControlFlowCache`（host 侧）——仿真非"纯解释"，走 launcher/内存模型栈，依赖已构建的 `devProgBinary/kernelBinary`（编译产物） |

## K. abs→TAbs 落地链与尾块语义（EVIDENCE-CLOSE 核心增补）

| # | 链节 | 证据 |
|---|------|------|
| K1 | 算子层：`pypto.abs(a)`→`pypto_impl.Abs(a)` | `python/pypto/op/math.py` `def abs`（docstring 例即 `[-1,-2,3]→[1,2,3]`）；`@op_wrapper` |
| K2 | 码生成层：`OP_ABS→GenUnaryOp()` | `codegen_op_npu.cpp` `unaryOps_` 表 `{Opcode::OP_ABS, [this](){ return GenUnaryOp(); }}`；TileOp 名经 `SUPPORT_TILETENSOR_OPS`/`tileOpName`（`UpdateTileTensorInfo`） |
| K3 | 设备 tileop：`OP_TILE_OP_ABS TAbs` | `interface/tileop/vector/unary.h:400-404`：`#define OP_TILE_OP_ABS TAbs` + `TILEOP void TAbs(T0 dst, T1 src)` → `UnaryCompute<UnaryOp::ABS,…>`；同类 Unary 实现可见模板：`pto::Tile<…, tileH, tileW, BLayout::RowMajor>`（`tileH/tileW = GetTensorTileShapeDim<DIM_4TH/DIM_5TH>`）+ 外层 `for (n0Index…shape0)` 遍历 + `TASSIGN(dstTile, dst.GetAddr()+GenTileOffset…)` + `AssignElementwiseOperandExecTile(srcExecTile, src, tileOffsets)`——**边界块经 exec-tile 有效形状表达（容量 tile + valid 收缩），与 ch24 Tile 容量/有效形状合同同构** |
| K4 | tile 形状对实参形状的钳制 | `interface/operation/tile_shape_resolver.h:23-26`：「the default returns the op-level tile shape **clamped to the operand's own shape (elementwise)**」；`GetInput/OutputTileShape`「real per-axis tile size (e.g. clamped to each input's own shape)」。**主例 shape(3,) 配 tile(2,8)：尾轴 8→钳到≤3 的语义由 resolver钳制+valid 承载；tile 两维对一维张量的具体配轴规则未逐行核（不写具体映射式）** |
| K5 | 码期三层形状 | `codegen_op_npu.cpp UpdateTileTensorShapeAndStride`：静态→`shape`直写+`stride=BuildStride(rawShape)`；动态局部张量→`shape=dynamicValidShape`、`stride=BuildStride(rawShape)`——**有效形状定取数范围、rawShape 定步长**；loop 内 `BuildTileTensorShapeInLoop` 取末 2 维（注释「Get last 2 dim of shape」） |
| K6 | 用户约束（官方） | `docs/zh/tutorials/development/tiling.md` 使用约束：TileShape 须匹配 Shape 维数、`TensorShape/TileShape ×(1+输入数)<18000`（防在线展开爆炸）、vec 维数≤5、**尾轴切分 32B 对齐**（8×f32=32B 合规）、cube kL0/kL1/nL0/nL1 32B 对齐；「通常设置不同 TileShape 不影响结果，影响运行时间」 |
| K7 | 循环边界来源 | pass 期 `loopAxes/dynloopAxes` attr（`GetLoopAxes`），码期 `forBlkMgr_ LoopStart/loopGroupEnd→Print` 成环——**循环展开次数在 pass 期已定，码期只翻译** |

## L. 复现命令（rev2 定稿，均不写源仓）

```bash
# 0) 只读核对（源仓不动）
git -C /mnt/SATASSDEXT4/cann/pypto status --short   # 2026-10-10 实测：干净，HEAD=883e7df
# 1) 语法检查（pyc 落 /tmp）
PYTHONPYCACHEPREFIX=/tmp/ch25-pycache python3 -m py_compile \
  /mnt/SATASSDEXT4/cann/pypto/examples/01_beginner/compute/elementwise_ops.py \
  /mnt/SATASSDEXT4/cann/pypto/examples/01_beginner/basic/basic_ops.py          # 已验，见 H2
# 2) 构建（副本！非只读源仓）
cp -a /mnt/SATASSDEXT4/cann/pypto /tmp/pypto-build && cd /tmp/pypto-build
python3 build_ci.py --clean --no_isolation        # 或 pip install -e . --no-build-isolation
# 3) 运行（需 2 成功；本机未满足，给命令不贴输出）
python examples/01_beginner/compute/elementwise_ops.py abs::test_abs_basic --run_mode sim
# 4) 中间结果：KEY_PRINT_GRAPH → <LogTopFolder>/TensorGraph/IR/ir_dump_*.txt；
#    compile_debug_mode=1 → output_*/Pass_<NN>_<name>/*.json（debug.md）
```
