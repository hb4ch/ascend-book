# CH24 R1 回应（2026-10-10）

逐项对照 `management/reviews/CH24-R1.md`。核验：改后对终态正文/证据 rg 实测（文末）；verify 与 bash-n 日志更新；最终复现命令三步实跑留痕。

## 1. 复现命令（P1）——已按最终正文同款命令实跑

正文 24.8 命令块改为：**`cmake -S /mnt/…/pto-isa/demos/cpu/gemm_demo -B $WK/build`**（只读源仓目录，`-B` 写临时目录，不改源；CMakeLists 经 `../../..` 回溯仓库根，注释说明单拷目录会找不到 include）。三步实跑日志：

- `validation/ch24-r1-configure.log`（Configuring done；`CXX_INCLUDES = -I/mnt/.../pto-isa/include` 摘录另存 `ch24-r1-flags.log`）
- `validation/ch24-r1-build.log`（Built target gemm_demo）
- `validation/ch24-r1-run.log`（`max_abs_diff=1.19209e-07`；WK=`/tmp/tmp.6jK8n60Haw` 记于 `ch24-r1-wk.log`）

非既有 binary 复跑：构建目录为本次新建（`ch24-r1-wk.log` 留痕）。[^11] 同步改写。

## 2. 开篇引入——去无证断言

删「第16章/第22章/hixl」「换代逃不开重写」rg=0。改为仓库内实证：`TileLeft` 别名 A2A3=RowMajor 块 vs CPU-SIM=ColMajor 块（`[^4]` L1706-1728）＋`set_flag/wait_flag` 设备屏障 vs 仿真空函数，具体差异引入。

## 3. 24.2 代码与表述

- 代码块补全真实五维 `Stride<1*kM*kK, 1*kM*kK, kM*kK, kK, 1>`，注释标「照抄源码/从略」。
- GM 表述改「同一行相邻列连续、跨行步长 kK，即按行存放」，并补 B 末两维 `(kN,1)`。
- 「转置式重排」→「重排进分形布局（坐标映射而非数学转置）」。
- 图①重画：A/B 双支路 TB、A(kK,1)/B(kN,1) 分标；读图改「搬运三次（TLOAD/TMOV/TSTORE），TMATMUL 是计算不是搬运」；「数据面＝一次绑定+四步」。

## 4. 图②重画（手绘 SVG）

新 `docs/figures/ch24-tile-layout.svg`（生成器 `validation/ch24-fig2-gen.py` 可复现）：左＝32×16 全貌按 ColMajor 块序编号 #0-#3（Nz 公式块序），高亮 elem(1,1)；右＝块#0 放大 8×16 格，高亮块内 (1,1)、偏移 1×8+1=9；底注 GM 同元素 1×16+1=17。正文相应改「块坐标 (0,0)、块内 (1,1)」，删「虚线以下」（rg=0）。原四段纵排文字框废弃。

## 5. 事件方向两条（P1）

24.4 重写并节录真实代码（L537-556 标注）：`loadToAxpy: Event<TLOAD,TAXPY>` 由 TLOAD 返回、传入 TAXPY（前向：搬完才算）；`axpyToNextLoad: Event<TAXPY,TLOAD>` 由 TAXPY 返回、下一轮 TLOAD 前 Wait（反向复用）；循环出口 L556 收尾 Wait 单独强调「不能漏」。旧「只声明后一类型却接 TLOAD」混淆消除。

## 6. 图③重画——事件两向 vs CPU 顺序

新图：左 subgraph=设备侧 moe_combine 依赖链 TLOAD→(loadToAxpy)→TAXPY→(axpyToNextLoad, Wait)→下一轮 TLOAD；右=主例无事件、按书写顺序＋「本样例 CPU 参考对拍通过（仅此样例）」。删「同名指令照跑结果一致」「同一行代码两后端」措辞（rg=0）；读图与收尾段明写「主例未在 NPU 运行、对拍仅限本样例 CPU 参考」。原两堆术语框删除。

## 7. 字节数与对齐约束

「累加器 tile 1024B 容量」改为「**单分形块** 1024B（内部 16×16 float），cTile 32×16 float 计 512 float＝2048B 恰两块」；对齐约束改「按组合各自成立」（RowMajor+NoneBox 查 Cols、ColMajor 查 Rows、boxed 查整除），明写「不能一条泛化所有 tile」。24.7「手工上限」→「手工编排示例，非经性能验证」。

## 8. 正文宽度可读性（P1）

按正文宽 **624px** 验收三图：①natural 378×750 scale1.0（有效字号 16px）；②SVG 620×452 scale1.0；③731×702→624 scale0.854（有效字号≈13.7px）。截图 `validation/ch24-{fig1,fig2,fig3}.png` 即 624 容器实渲染，非 1400px 画布缩印；textContent 关键词全命中（①TLOAD/TMOV/TMATMUL/TSTORE/kK,1/kN,1…②块#0-#3/elem(1,1)/9/17…③loadToAxpy/axpyToNextLoad/仅此样例）。

## 校验与终态

- `npm run verify` 0 FAIL → `validation/ch24-r1-verify.log`（4,186 字/中文 2,911）。
- bash 块 `bash -n` ok → `ch24-r1-bashn.log`/`ch24-r1-fence.sh`；12 脚注闭环（逐条≥2）。
- rg 终态：`hixl|第16章|第22章|5次搬运|同名指令照跑|手工上限|虚线以下` 正文 0 处（「数学转置」仅存于「而非数学转置」澄清句）；`行主序`正文 0 处（改按行存放表述，EVIDENCE 历史引文不动）。
- EVIDENCE 图规划表更新为 R1 实况（rev3 头注）。
- 未动 23 章；未提交；未换模型。
