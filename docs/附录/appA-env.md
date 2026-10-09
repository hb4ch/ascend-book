---
title: 附录A 环境搭建
description: 按读者起点分流——从纯阅读复现到真机验证的四条路径
---

# 附录A 环境搭建

> 本机（写作环境）无 NPU 硬件。本书各示例的验证层级以该章自己的声明为准；本附录回答一个问题——**以你的起点，走到下一层需要装什么、验什么**。

## A.0 先分流：你在哪一档

| 起点 | 你想做什么 | 去哪节 | 需要什么 |
| --- | --- | --- | --- |
| ① 只读+CPU 复算 | 复现书中 CPU 数学参考、读 PTO 头文件与 ISA 语义 | A.2 | 按脚本而定（见该节），无需任何昇腾组件 |
| ② PTO CPU-SIM | 编译运行 PTO 的 CPU 仿真示例（含本书已验证的 GEMM） | A.3 | gcc/cmake，无 NPU 可完成 |
| ③ CANN 工具链 | 在宿主或仿真模式编译 asc-devkit 类算子工程 | A.4 | CANN toolkit；无卡可装可编 |
| ④ 真机 | 在 NPU 上运行与调优 | A.5 | ③之外再加驱动固件与所选场景组件 |

②与③是**并列分支**，不是先后的安装台阶：只跑 PTO CPU-SIM 不需要 CANN；要编 asc-devkit 才进入③。**CPU 模式、sim 模式与真机是三条验证路径**，构建系统接受某种模式不等于具体样例在该模式下可跑通——支持条件先查样例自身 README，实际结果仍需运行验证；本书实测覆盖见 A.6。本附录基于源码固定快照写作，**不构成对当前版本安装方案的推荐**；任何安装前请以官方安装指南核对组件与包名[^1]。

## A.1 通用检查：设备识别与版本留痕

```bash
# 有卡且装好驱动时：输出设备信息即驱动可识别设备（asc-devkit quick start「环境验证」节）
npu-smi info
# CANN 是否安装及版本：版本信息文件存在与否（同节；默认路径，非 root 将 /usr/local 换 $HOME）
cat /usr/local/Ascend/cann/$(uname -m)-linux/ascend_toolkit_install.info
```

这两招只回答「设备被识别」「版本文件在」，**不等于后续计算正确**——计算正确性永远由具体程序的结果比对给出。环境变量：默认路径 `source /usr/local/Ascend/cann/set_env.sh`，指定路径 `source ${install_path}/cann/set_env.sh`[^1]。

## A.2 路径①：只读与 CPU 复算（无 CANN）

PTO 头文件与 ISA 语义的阅读（第 24 章及 PTO 各章）不需要任何安装——直接翻仓内 `include/` 与文档。CPU 数学复现的依赖**按脚本区分**：第 27 章两个脚本（golden 冒烟、独立对拍）需 `numpy` 与 CPU 版 `torch`，两者导入的 golden 模块中，dtype 表用 `tensorflow-cpu` 的 bfloat16[^2]；不需要 torch_npu。本书留痕：pyenv 3.12+CPU 版 torch/tf；脚本以 `sys.dont_write_bytecode` 避免在源码树落缓存。**边界**：CPU 复算只证数学层；第 24 章实测覆盖仅下节的单个 GEMM，不外推。

## A.3 路径②：PTO CPU-SIM——从本书已验证的 GEMM 走通

**已验证主例**（第 24 章实测，日志与命令存档于本书仓库）[^2]：

```bash
# 将下行替换为你的 pto-isa 固定快照路径
PTO_SOURCE=/path/to/pto-isa
# 工作目录任意；构建产物写入源码树之外
cmake -S "$PTO_SOURCE/demos/cpu/gemm_demo" \
  -B /tmp/ascend-book-pto-gemm -DCMAKE_BUILD_TYPE=Release
cmake --build /tmp/ascend-book-pto-gemm -j2
/tmp/ascend-book-pto-gemm/gemm_demo
```

- **源码位置**：仓内 `demos/cpu/gemm_demo/`（`gemm_demo.cpp`+`CMakeLists.txt`，原样编译未改）。
- **构建行为**：CMake 按编译器版本选 C++20/23（GCC≥14 走 23），并给目标加 `__CPU_SIM` 与 `__PTO_AUTO__` 宏——CPU 仿真语义由这两个宏进入（见其 CMakeLists L15-26）[^3]。
- **结果**（本书实测，g++ 16.2.1/CMake 4.4.2）：`M=32 K=16 N=32` float，`max_abs_diff=1.19209e-07`（示例阈值 1e-3 内）；日志中的耗时/GFLOPS 只描述该 CPU 仿真过程，不是 NPU 性能。
- **前提**：CMake≥3.16，以及支持该工程所选 C++20/23 标准和头文件的 C++ 工具链；这里仅验证了上述宿主环境，未验证所有编译器或主机架构。**无需 CANN、无需卡**。

同目录还有 `flash_attention_demo`、`mla_attention_demo` 等示例，构建方式同理，本书未逐一运行。**更全的测试入口**是仓内 `tests/run_cpu.py`（编译并运行 `tests/cpu/st` 用例，支持 `--testcase`/`--gtest_filter`，前置 build-essential/cmake/ninja）——注意 getting-started 文档末尾提到的 `tests/cpu/demos/` 路径已不存在，示例实际在 `demos/cpu/`（本书已核对并以实测路径为准）[^3]。这些入口本书未跑，仅作参考；CPU-SIM 结果亦非 NPU 结果。

## A.4 路径③：CANN 工具链编译与仿真（可无卡）

asc-devkit 官方 quick start 写明：仅编译源码加仿真环境运行算子，**不要求主机有 NPU，可跳过驱动固件**——先装 CANN 包即可[^1]。安装方式按你所选版本定：

- **已发布版本**：从所选版本的官方安装指南，按产品型号与主机 CPU 架构确定包名和安装步骤。ops 算子包仅在需要跑（真机或仿真）样例时按产品加装，型号映射见 runtime README 对照表（A2→`910b`、A3→`A3`、950PR/DT→`950`）——**这是 runtime 仓样例的前提，不是所有仓所有样例的通则**[^4]。
- **容器**：asc-devkit quick start 引用 `swr.cn-south-1.myhuaweicloud.com/ascendhub/cann:<tag>` 形态镜像（文中示例 `9.0.0-beta.2-910b-ubuntu22.04-py3.11`，为快照时点写法）；DevContainer 路线只挂驱动（只读），CANN 包容器内自装。tag 选择与时效请以昇腾镜像仓库页面与官方安装指南为准[^1]。

进 asc-devkit 工程后：`build.sh` 经 `ASCEND_HOME_PATH`（或 `--cann_path`）定位 CANN；构建模式 `CMAKE_ASC_RUN_MODE` 取 `npu/cpu/sim`（默认 npu）[^5]。**已核个例**：`matmul_mxfp4_high_performance` 的 README 同时给出 npu 与 sim 两行 cmake 命令（`dav-3510`）——该样例文档层面声明可按 sim 跑；其他样例请各自查 README，本书未代为归纳。无卡环境先核对版本文件和环境变量，再按选定样例验证编译与仿真；不要求执行 `npu-smi`。

## A.5 路径④：真机

在 ③ 之上加两层，均以官方安装指南为准：

- **驱动固件**：仓内 README 统一指向《CANN 软件安装指南》的「准备软件包/安装 NPU 驱动和固件」章节；具体包名与版本搭配**从你所选版本在该指南中确定**，本附录不代拟。
- **运行态组件，按需且按仓**：runtime 自建样例需对应产品 ops 包（见 A.4 对照表）；PyPTO 运行态需 PyTorch 与 torch_npu，且与 PyPTO 三者 Python 版本一致、先装 toolkit 再装 torch_npu（其 prepare 文档原文）[^6]；hixl 编译需 Toolkit、跑样例加驱动固件、Python 样例另加 ops 包（分层前提见其 build 文档）[^6]。
- **容器挂载**：真机容器需按 quick start 参数表挂 `davinci*`/`davinci_manager`/`devmm_svm`/`hisi_hdc` 与驱动库等项，逐项释义以该表为准[^1]。

验证：A.1 两招证明「设备被识别、版本就位」；**计算正确性由各仓自带 tests/样例的比对结果给出**。

## A.6 各仓入口速查与本书实测边界

| 仓/资产 | 入口 | 前提（按其文档） | 本书实测 |
| --- | --- | --- | --- |
| pto-isa `demos/cpu/gemm_demo` | A.3 三行 cmake | g++/cmake | **已验证**：配置/编译/跑通，结果见 A.3[^2] |
| pto-isa `tests/run_cpu.py` | `--testcase`/`--gtest_filter` | build-essential/cmake/ninja | 未跑，仅文献 |
| 本书 CPU 脚本 | `management/validation/ch27-sfa-*.py` | numpy/torch-cpu/tf-cpu | **已跑**（CPU 数学层）[^2] |
| asc-devkit | `build.sh`+`CMAKE_ASC_RUN_MODE` | CANN（`ASCEND_HOME_PATH`） | 未编译；已核 sim 命令文档个例 1 处 |
| pypto | `pip install -e .`（CMake 集成） | 编译态 gcc≥7.3.1/cmake≥3.16.3/pybind11 等[^6] | 未装未编 |
| runtime/hixl/hcomm/ops 系 | 各自 `build.sh` | 见各仓 build 文档；hixl 另有 `requirements.txt` | 未编译 |

**边界**：本书未装驱动、未运行任何 NPU；实测仅上表两处「已验证/已跑」。外网可达性、镜像与包的现势状态、驱动版本匹配矩阵均不在本书核验范围——安装前以官方安装指南与镜像站点现状为准。

## 本章来源

[^1]: `asc-devkit/docs/zh/quick_start.md`——分流表与「仅编译+仿真不要求 NPU 驱动」、环境验证（`npu-smi`/`ascend_toolkit_install.info`）、环境变量两式、Docker 参数表与镜像示例（`swr.cn-south-1.myhuaweicloud.com/ascendhub/cann:9.0.0-beta.2-910b-ubuntu22.04-py3.11`）、master 包安装节；`runtime/README.md`——驱动固件指向官方指南、ops 包 soc 映射（A2→910b/A3→A3/950PRDT→950）、依赖清单与 `download_3rd_party.py` 离线流程、产物 `build_out/*.run`。
[^2]: 本书实测存档：`management/validation/PTO-CPU-GEMM.md`（GEMM 验证记录：源=`pto-isa/demos/cpu/gemm_demo/gemm_demo.cpp` 原样编译；命令三行；结果 M32/K16/N32、max_abs_diff=1.19209e-07；工具链 g++16.2.1/CMake4.4.2；「tests/cpu/demos 已不存在、实际在 demos/cpu」提示）及 `management/validation/pto-gemm-{configure,build,run}.log`；`management/validation/ch24-cpusim-gemm-rerun.log`（二进制复跑+工具链尾注）；`management/validation/ch27-sfa-cpu-golden.{py,log}`、`management/validation/ch27-sfa-tnd-refcheck.{py,log}`（CPU 数学层，numpy/torch-cpu/tensorflow-cpu bfloat16）。
[^3]: `pto-isa/demos/cpu/gemm_demo/CMakeLists.txt` L15-26（GCC≥14→C++23 否则 20；`target_compile_definitions(gemm_demo PRIVATE __CPU_SIM __PTO_AUTO__)`）；`pto-isa/demos/cpu/` 下另有 `flash_attention_demo`、`mla_attention_demo`；`pto-isa/docs/getting-started_zh.md`——apt 五件套/Windows 替代、venv numpy、`tests/run_cpu.py` 用法（L121 区段）、L429 `tests/cpu/demos` 提法（本书核对实际路径为 `demos/cpu/`）；`pto-isa/pyproject.toml`（9.1.0、py≥3.9）；`pto-isa/setup.py`（data_files→`share/pto-isa/include`，pip 装头文件）。
[^4]: `runtime/README.md` L120-133：ops 包按产品对应（仅该仓样例前提之明示）。
[^5]: `asc-devkit/build.sh` L589-590（`ASCEND_HOME_PATH`/`cann_path`→`ASCEND_CANN_PACKAGE_PATH`）；`asc-devkit/cmake/asc/asc_modules/CMakeASCInformation.cmake` L163-172（RUN_MODE 三值，默认 npu）；`asc-devkit/examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_mxfp4_high_performance/README.md` L232-241（npu/sim 双命令行，`dav-3510`）。
[^6]: `pypto/docs/zh/install/prepare_environment.md`——编译态/运行态定义、编译依赖（gcc/g++≥7.3.1、cmake≥3.16.3、pybind11≥2.13.6、python3-dev）、「先 toolkit 后 TorchNPU、PyTorch/TorchNPU/PyPTO 三者 Python 版本一致」；`hixl/docs/zh/build.md` 头部（Toolkit/驱动固件/ops 分层前提；Docker 仅 Ubuntu；A2/A3/A5）；`hixl/requirements.txt` 全列表；`pypto/pyproject.toml`（0.2.1、dev/test extras）。
