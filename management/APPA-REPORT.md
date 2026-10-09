# APPA 报告 —— 附录A 正文交付

2026-10-10。任务 `APPA-WRITE.md`；证据 `APPA-EVIDENCE.md` rev1、提纲 `APPA-OUTLINE.md`。**只改 `docs/附录/appA-env.md` 与本报告/证据**；28 章未动；源仓只读零缓存；零安装零安装脚本；未提交。

## 交付

`docs/附录/appA-env.md` 全文重写：2,149 字/中文 1,454（附录非重点章，ACCEPTANCE 个案裁量口径），frontmatter 仅 title/description 两键——与原 appA 及其他附录先例一致（附录页无 status 键，全书 status 键仅用于正文章）；如需统一加 status 留 P5 收口。

## 结构（对照任务逐条）

- **A.0 分流表**：四起点①只读+CPU复算/②PTO CPU-SIM/③CANN编译仿真(可无卡)/④真机→A.2–A.5；「零安装≠numpy/torch/tf 天然已装」明写；**CPU/sim/真机三模式分开**+「模式枚举≠样例可跑证明」；历史快照命令一律「文档示例，本书未执行，配套以官方指南为准」。
- **PTO 已验证例子走最小路径**：A.3 完整给出 getting-started 链（apt 五件套→venv numpy→`run_cpu.py [--testcase]`），并**纠正「pip 装 pto-isa 带 CPU-SIM」旧说**（pip 只装 include 头文件，setup.py data_files 为证）；本书实测边界=ch24 单 GEMM 复跑。
- **不做依赖倾倒**：各仓细节收敛到 A.6 速查表（仓×入口×前提×产物×本书实测六列），深链交给仓内文档（脚注全路径）。
- **事实纠错落实**：删 `Ascend-hdk-*` 通配安装命令（→「见官方指南，历史文件名不构成可执行依据」）；删 `quay.io`（→仓内实引 `swr.cn-south-1...ascendhub/cann:<tag>` 且标「历史示例，时效自查」）；删 `torch_npu.npu_count()`（无出处）→环境检查只留 `npu-smi`+`ascend_toolkit_install.info` 两招（均 quick_start 原文）并**明写无卡不能拿 npu-smi 当判据**；虚构硬件/OS 组合删除（Windows 仅按 pto-isa 文档转述其官方支持面）。
- **不写评审史//tmp 流程**；实测仅 ch24 GEMM+ch27 CPU 对拍两处，A.6 表「本书实测」列如实。
- **脚注 6 组全路径**：quick_start/runtime README、本书 validation 留痕、pto-isa getting-started+pyproject+setup.py、runtime soc 映射、asc-devkit build.sh+CMakeASCInformation L163-172+样例双模式、pypto prepare/hixl build+requirements。

## 验证（真实 exit）

`npm run verify >/tmp/appa-verify.log 2>&1` → **EXIT=0**：build 通过；internal-links 42 文件 OK；source-check **475 引用 0 无效**（本附录 6 脚注全部路径过检）；terms warn 1 处仍在 ch24 既有文本；word-count 见上。

## 页面实渲染核验（非 bbox 替代）

verify 后以 vitepress 产物起本地静态服务，Playwright 打开 `附录/appA-env.html` 实渲染页：**2 表格+2 bash 代码块、9 个 h2（A.0–A.6+本章来源）DOM 层逐一在位；0 表格横向溢出；页面无 4xx 资源**；整页截图 `management/validation/appa-page-full.png`（2560×11522@2x，fullPage）。**像素文字可读性宿主不能目检，留 PM 视验**——DOM/几何审计如实声明。

## 边界

未动 ch28/其他附录/appD；未装任何包未跑安装脚本；源仓零写入。候审。
