# APPA 证据集 —— 附录A 环境指南

rev1（2026-10-10）。任务 `APPA-RESEARCH.md`。基线 `SOURCE-BASELINE.md`；**本轮零安装零源仓写入**（仅只读 cat/grep；无新验证脚本，已有管理验证复读）。现有 `docs/附录/appA-env.md` 逐条审查结论如下——**「仓内可证」与「外网/惯例」分开，不把未证项写成事实**。

## A. 现有 appA 逐条审查（✇=须改/补出处，✓=仓内可证）

| 现有陈述 | 审查 | 仓内证据 |
|---|---|---|
| A.2 driver `./Ascend-hdk-*.run --full` | ✇ 仓内无此命令模式；runtime README 只写「驱动固件安装见官方指南」(`runtime/README.md` L90-94)，无 run 命令。须降为「见官方安装指南」或标注非仓内出处 | `runtime/README.md` L90-94/L120-133 |
| 下载 URL hiascent 社区/mirror | ✇ 外网 URL 本任务不核验：`https://www.hiascend.com/...`、master 镜像站 `ascend.devcloud.huaweicloud.com/...`（`runtime/README.md` L99/L122、`asc-devkit/docs/zh/quick_start.md` L121-124 有出现）——**可引「仓内 README 所指」，不证可达** | 同左；留缺口声明 |
| A.3 `quay.io/ascend/cann:latest` | ✇ **仓内无 quay.io 镜像**；各仓实际引用 `swr.cn-south-1.myhuaweicloud.com/ascendhub/cann:<tag>`（asc-devkit quick_start L57 示例 tag `9.0.0-beta.2-910b-ubuntu22.04-py3.11`；hixl build.md A3 `9.0.1-...-py3.12-devel` x86/arm 双；pypto prepare L~40 `9.1.0-beta.1-910b-openeuler24.03-py3.12-devel`）。设备挂载参数表齐全（--device davinci0/davinci_manager/devmm_svm/hisi_hdc + driver 挂载） | quick_start L42-103；`hixl/docs/zh/build.md` 头部；`pypto/docs/zh/install/prepare_environment.md` |
| A.4 runtime `install_deps.sh`+`build.sh` | ✓；依赖 gcc≥7.3.0/python3-dev/cmake/ccache/autoconf/gperf/libtool/make（L74-84 apt/yum 两套）；联网自动拉 3rd party 或 `python download_3rd_party.py` 后 `--cann_3rd_lib_path`；产物 `build_out/cann-npu-runtime_<version>_linux-<arch>.run` | `runtime/README.md` L74-89/L160-181 |
| A.4 asc-devkit `build.sh`（CPU 静态核对说法） | ✓ 存在；**须 CANN**：`ASCEND_HOME_PATH` 或 `--cann_path`（build.sh L589-590）；`CMAKE_ASC_RUN_MODE` 支持 **npu/cpu/sim** 三值，默认 npu（`cmake/asc/asc_modules/CMakeASCInformation.cmake` L163-172）——「CPU 模式编译核对」有构建系统依据，但**仍需先装 CANN 包**；「无 NPU 可编译+仿真运行」官方明示（quick_start L16） | 左述两处 |
| A.4 pto-isa `setup.py/pyproject` | ✓ 存在：name pto-isa version 9.1.0、requires-python≥3.9、build 需 setuptools≥45+wheel（`pyproject.toml` L12-22）；**「pip 装完带 CPU-Simulator 与工具链」须收窄**：CPU-SIM 走 `tests/run_cpu.py`（gtest 二进制编译执行），前置=Ubuntu20.04+ `build-essential cmake ninja-build`（`docs/getting- started_zh.md` L57-59）或 Windows VS2022/WinLibs；venv 只需 numpy（L77-81）。pip 包装的是头文件（`data_files→share/pto-isa/include`，setup.py L17-27） | 左述三处 |
| A.4 pypto `setup.py` 需 pto-isa+llvm | ✓ setup.py 存在（CMake 构建集成，editable 支持）；✇ **「llvm 工具链」仓内未见**——官方依赖单：编译态=CANN toolkit+gcc/g++≥7.3.1+cmake≥3.16.3+make+pybind11≥2.13.6+patch+python3-dev；运行态另需驱动固件+ops 包+**PyTorch/TorchNPU（三者 Python 版本一致，先 toolkit 后 TorchNPU）**（`pypto/docs/zh/install/prepare_environment.md` L138/L150-160 区段）；version 0.2.1、requires≥3.7、dev extras pytest 系（pyproject L19/L29-52）。**修正 llvm 表述** | 左述 |
| A.4 hcomm/hixl/ops build.sh | ✓ 存在；hixl 编译须先装 Toolkit，跑样例须驱动固件，python 样例加 ops 包（`hixl/docs/zh/build.md` 头部）；Docker 路线 A2/A3/A5、仅 Ubuntu；hixl `requirements.txt`：numpy/pyyaml/decorator/sympy/scipy/attrs/protobuf/psutil/setuptools≥59/wheel/coverage | 左述 |
| A.5 NPU-Simulator「CANN 官方需 Toolkit 配套」 | ✇ 仓内未见该产品名文档；可证的是 asc-devkit `RUN_MODE=sim`（仿真编译，L168-172 支持值含 sim，另有 sim 模式 arch 映射 dav-2002…）与 kernel_direct_call `--run-mode npu/cpu`（appendix/kernel_direct_call_from_sample.md L384-404）。**改写为构建系统 sim 模式**，产品名留缺口 | 左述 |
| A.6 五步验证流 | 与 ch14 相呼应，正文层面处理，不属本证据范围 | —— |

## B. 按读者环境的证据分组（提纲主线直接取用）

1. **仅阅读+CPU 数学参考**（无任何昇腾组件）：本书已验证留痕=ch27 CPU golden/对拍脚本（`management/validation/ch27-sfa-{cpu-golden,tnd-refcheck}.{py,log}`，依赖 numpy/torch-cpu/tensorflow-cpu，pyenv 3.12 留痕，`sys.dont_write_bytecode` 防源树 pyc）；ch24 CPU-SIM 复跑日志（`ch24-cpusim-gemm-rerun.log`，g++16.2.1/cmake 4.4.2，二进制直执行）。**CPU 数学参考≠NPU 结果**，第24章单样例覆盖不泛化。
2. **PTO CPU-SIM 样例**（无 NPU）：pto-isa getting-started 全链（apt 五件套→venv numpy→`python3 tests/run_cpu.py [--testcase tadd]`）；Windows 替代 VS2022/WinLibs/MSYS2。**这是仓内文档明示的无 NPU 路径**；「已验证样例」=ch24 gemm 复跑，其他用例本书未跑。
3. **CANN 工具链编译/仿真**（无 NPU 亦可）：asc-devkit quick_start L16 明示「仅编译+仿真运行不要求 NPU 驱动」；装法=master 包（toolkit 必选+ops 可选，`.run --install`，soc 映射 910b/A3/950 见 runtime README L127-133）或 Docker/DevContainer；环境验证 `cat .../ascend_toolkit_install.info`+`npu-smi`（有卡时）；`source set_env.sh`（默认/自定路径两式，quick_start L184-187）。asc-devkit 另需 `ASCEND_HOME_PATH`（build.sh L589）。
4. **真机运行**：驱动固件（官方指南，仓内无 run 命令）→CANN 包→`npu-smi info` 验证；runtime 源码构建产物 run 包；pypto 运行态全依赖（上表）；容器挂载清单（quick_start L88-103 参数表）。**Docker 正确镜像名为 swr.cn-south-1...，非 quay.io**。

## C. 缺口与不核验声明（正文须带）

外网可达性、镜像 tag 时效、驱动版本匹配矩阵、CANNLab 现状、quay.io 是否存在——**本任务一律不联网核验**；下载地址只引「仓内 README 所指 URL」并注「未验证可达」。驱动 run 包命令模式无仓内出处，正文不得给具体文件名通配。

## D. 边界

本轮无新执行验证（复读既有 log）；若 WRITE 阶段需新验证，仅 /tmp 隔离+先声明；不装任何包、不生成/清理源仓缓存、不在源仓跑 Python 导入。
