# APPA 提纲 —— 附录A 环境指南（rev1）

主线按**读者起点**分流，每条路径四拍：前提→装什么（命令+仓内出处）→验证→本书走到哪层。全部命令标注来源与依赖；外网/可达性留缺口声明（EVIDENCE §C）。**不写无出处命令；quay.io 镜像名纠正为仓内 swr 域名。**

- **A.0 怎么读本附录**：层级表（公告/指南/样例/运行）回收 28 章方法；「仓内可证 vs 官方外链 vs 本书留痕」三色；全部基于 SOURCE-BASELINE 快照。
- **A.1 路径一：只读书+CPU 数学复现**（零安装底线）：python+numpy/torch-cpu（+tf-cpu 仅 ch27 golden）；本书留痕=ch27 两脚本与日志、ch24 gemm 复跑 log；边界=CPU 数学≠NPU、24章单样例不泛化。
- **A.2 路径二：PTO CPU-SIM 样例**：pto-isa getting-started 全链（Ubuntu apt 五件套/Windows VS2022；venv+numpy；`python3 tests/run_cpu.py [--testcase …]`）；pip install pto-isa 只装头文件（9.1.0，py≥3.9）不等于装 SIM——**纠正现 appA A.4**；已验证=ch24 gemm；其余用例未跑声明。
- **A.3 路径三：CANN 工具链编译/仿真（可无卡）**：官方明示编译+仿真不需驱动（quick_start L16）；master 包安装（toolkit 必选/ops 按需，soc=910b/A3/950 对表）；`RUN_MODE=npu/cpu/sim` 三值构建（CMakeASCInformation L163-172）+asc-devkit 需 `ASCEND_HOME_PATH`；验证=install.info/`npu-smi`（有卡）；Docker/DevContainer/云环境三替代，**镜像 swr 域名+tag 示例，不证可达**。
- **A.4 路径四：真机**：驱动固件→官方指南（不编 run 命令）；容器挂载清单表（davinci0/manager/devmm_svm/hisi_hdc/driver…）；runtime 自建产物；pypto 运行态依赖全列（torch/torch_npu 版本一致约束）；hixl/ops 各自前置。
- **A.5 各仓构建速查表**：仓×入口脚本×关键依赖×产物×本书验证状态（ch24 cpusim log/ch27 cpu golden/无）；含 `download_3rd_party.py` 离线补包与 hixl requirements 清单。
- **A.6 缺口与验证声明**：外网不核验清单；本书未装驱动未跑 NPU；后续验证建议（/tmp 隔离边界）。

图表：1 张分区路径表（A.0 处）+1 张各仓速查表（A.5）；命令块逐个带出处脚注。篇幅~2.5-3.5k 中文（附录非重点章，ACCEPTANCE 个案裁量）。不改 appD/其他附录；不动 28 章。
