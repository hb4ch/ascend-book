# APPA R1 修订回应 —— reviews/APPA-R1.md 逐项

`docs/附录/appA-env.md` 重写（2,306 字/中文 1,610，EXIT=0 见尾）；仅动 appA+本报告；源仓只读；零安装；未提交。

**1 已验证 GEMM 走主例**：A.3 重写为「从本书已验证的 GEMM 走通」——主例即 `demos/cpu/gemm_demo`（读 `PTO-CPU-GEMM.md` 核对）：三行 cmake 命令原样（`-S <快照>/demos/cpu/gemm_demo -B /tmp/...`），**写明工作目录任意/构建目录在 /tmp 不污染源码树**、源码位置、构建行为（CMakeLists L15-26：GCC≥14→C++23+`__CPU_SIM __PTO_AUTO__`）、实测结果（M32/K16/N32、diff 1.19209e-07、g++16.2.1）与耗时/GFLOPS「仅 CPU 仿真过程」限定。**`tests/run_cpu.py` 降为「更全的测试入口…仅作参考，本书未跑」**——不再与 GEMM 混同；另按 PTO-CPU-GEMM.md 提示注明 getting-started 的 `tests/cpu/demos` 路径已废、实际在 `demos/cpu/`（已核对）。

**2 去泛化**：删「从上往下依次加重」「CANN 全套」；②③改**并列分支**（A.0 表+A.0 段明写「只跑 PTO CPU-SIM 不需要 CANN」）；A.2 依赖**按脚本区分**（ch27 两脚本 numpy/torch-cpu、golden 另 tf-cpu；PTO 阅读零安装）；ops 依赖**限定出处**——「runtime 仓样例的前提，不是所有仓所有样例通则」（A.4），hixl 分层前提单独引其 build 文档（A.5）。

**3 删推荐化**：「master 包体验最新」改为「已发布版本：按所选版本官方指南取包装」；删全部通配安装操作（`Ascend-hdk-*` 已在上轮删，本轮复核无残留）；swr 镜像标「快照时点写法，tag 时效自查」；无卡编译/仿真只引 quick_start 原文+**已核个例**（matmul_mxfp4 README npu/sim 双命令行 1 处），「多数样例」断言删除。

**4 文风**：删「只这两招有出处/本书不代装/不在此倾倒/不构成可执行依据」等管理腔，换读者解释（如 A.1 改「只回答设备被识别/版本文件在，计算正确性由程序比对给出」）；「PTO 阅读 22–24 章」**改第 24 章**（22 是 HIXL，已核书目录）；脚注改平实来源描述，去逐行审计口吻。

**5 脚注/引用**：补全——`matmul_mxfp4_high_performance/README.md`（L232-241）、`kernel_direct_call...md` 改为**完整路径** `asc-devkit/docs/zh/guide/programming_guide/appendix/kernel_direct_call_from_sample.md`、management 脚本全路径（`management/validation/PTO-CPU-GEMM.md`、`ch24-cpusim-gemm-rerun.log`、`ch27-sfa-*.{py,log}`）；PyPTO 编译态依赖**直指其 prepare 文档**（不再「见 A.4」）；环境检查语义改「设备被识别/版本文件存在≠计算正确」（A.1/A.5 两处）。

**验证**：`npm run verify >/tmp/appa-r1-verify.log 2>&1` → **EXIT=0**（479 引用 0 无效；terms warn 仍在 ch24 既有文本）。字数 2,306/中文 1,610。

**局部截图**（替代整页万像素）：实渲染页截 A.0 分流表 `validation/appa-r1-tblA0.png`（1248×652@2x）与 A.3 GEMM 命令块 `appa-r1-gemm-cmd.png`（1312×334，内容宽 624px 内）；DOM 层 2 表/2 bash 块/9 个 h2 在位、0 资源 404。**像素文字可读性宿主不能目检，留 PM 视验。**

候审。
