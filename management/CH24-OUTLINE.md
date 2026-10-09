# CH24 提纲 —— PTO 虚拟 ISA（第 24 章，rev2）

rev2（2026-10-10）：按 `management/tasks/CH24-EVIDENCE-CLOSE.md` 纠偏——B7 布局分层重述、主例与设备事件例分离、图②改真实配置、可移植性措辞收窄、F2 复跑口径。证据引用一律指 `management/CH24-EVIDENCE.md` rev2（下记 EV§）。

读者设定与总原则：**先具体后抽象**。全章以 `demos/cpu/gemm_demo` 一个 tile 的旅程为主线：先看程序在 CPU-SIM 上真实跑通，再逐层追问"它凭什么也能映射到 NPU"。**本书环境实测仅 CPU-SIM；不写"在你的 CPU 上跑设备代码"、不写"NPU 运行"。** 字数沿 CH23 豁免口径，目标 4.5k–6k。

---

## 24.1 一个问题：同一份 GEMM，两代芯片（≈400 字）

- 读者问题：**不重写 kernel，怎么让它跨 A2/A3/A5？**
- 从 ch16/ch22 的代际断层引入；给出 PTO 的回答（EV A1，引文以 rev2 为准：「面向 tile 编程的虚拟 ISA……在不同昇腾代际之间更平滑地迁移」；平台面 EV A3）。
- 方法声明：全程 CPU 仿真求证，设备侧只读静态合同，不做性能断言、不实机验证（EV F5/I3）。

## 24.2 主例：30 行的 tile 级 GEMM（≈800 字）

- 读者问题：**PTO 程序长什么样？数据从哪来到哪去？**
- `gemm_demo.cpp` 全景：kM=32/kK=16/kN=32 → `GlobalA` stride 末两维 `(kK,1)`＝**GM 行主序**；`TileMatA/TileLeft` 的 `BLayout::ColMajor` 只描述 **512B 分形块的排布次序**，与 GM 布局、块内 `SLayout` 是三件事（EV B7）。
- 指令序列 TASSIGN/TLOAD/TMOV/TMATMUL/TSTORE（EV C2）；**主例不出现事件对象**（EV C1）。
- **TLOAD 的转换语义**（EV B7a/B7b）：显式两步——容量先填 pad、再按 valid 区域用 GM stride 逐元素 `SetElement` 写入分形布局；配偏移实算：elem(1,1) GM 偏移 17 vs tile 存储偏移 9（`management/validation/ch24-tile-offset-compute.log`）。
- 复现：cmake→build→首次构建；**本轮为既有二进制复跑**，`max_abs_diff=1.19209e-07`（EV F1/F2，日志 `ch24-cpusim-gemm-rerun.log`）；`flags.make` 的 `-D__CPU_SIM -D__PTO_AUTO__` 证 CPU-SIM 形态（EV D7）。措辞：「本书环境实测（CPU-SIM）」。

## 24.3 数据的形状：Tile 三层结构（≈700 字，图②）

- 读者问题：**容量形状、有效区域、物理布局各管什么？"有效区域"是自动遮罩吗？**
- 五属性（EV B1）；32B 对齐/512B 分形常量与 static_assert（EV B3/B4）；`GetTileOffset` Nz/Zn/Zz 三族（EV B5）。
- **图②改用主例 aTile 真实配置**：32×16 float，容量 2048B＝4 个 16×8×512B 分形块；有效区域子块用**假设动态 valid（标注 hypothetical）**演示收缩与 pad 填充。总字节数、偏移全部由复算脚本背书（EV B7b），不再用 16×16=1024B 或 8×8 假想格。
- **有效区域≠自动遮罩**（EV I1）：TLOAD 填 pad+抄 valid；CPU TMATMUL 以 valid 为 m/k/n 计算边界；TSTORE 写 valid 但断言容量≥valid 积——每条指令的合同要读实现才知道，正文逐一给锚。

## 24.4 指令与同步：依赖要显式写（≈700 字，图③左半）

- 读者问题：**设备上谁保证"load 完才 matmul"？**
- 主例：无事件、无屏障——顺序靠各指令默认依赖与 CPU-SIM 全同步（EV C1/D2），这是**仿真便利，非设备真相**。
- 设备真相之一：`RecordEvent` 返回值链——**真实设备例与主例分开引**：`moe_combine_kernel.cpp:537-556` `Event<TAXPY,TLOAD>` 声明→`loadToAxpy = TLOAD(...)`→`TAXPY(..., loadToAxpy)`→`.Wait()`（EV C1a）。
- 设备真相之二：manual 流水线 `SetFlag/WaitFlag` 配对（EV C4）——图③上半素材。

## 24.5 CPU-SIM：边界在哪里（≈600 字）

- 模拟了：分层内存/线程独立（EV D5）、原子互斥（D6）、`__PTO_AUTO__` 惰性分配（B9）。
  没模拟成真：流水线常量退化编号（D3）、`AICORE` 空宏（D4）、TSYNC no-op/set_flag 空实现（D2）。
- 结论句：**CPU-SIM 验证程序结构与数值，不验证时序与吞吐；仿真可用≠设备支持**（EV I3 措辞）。
- `NPUArch{A2A3,A5}` 与 A5 placeholder（D5/G2）。

## 24.6 跨代际：差异被收进哪里，边界在哪（≈600 字）

- 实证 `TileLeft` 双分支（EV B8）：**只证明"别名→布局"映射按代际不同**，用户代码不改写仍需设备侧合同成立。
- 设备侧合同（EV I2）：a2a3 `CheckStaticMad` dtype 表含 `(float,float,float)`；动态维度 [1,4095]（`MMAD_MAX_SUPPORT_LENGTH`，a5 L20 同界但 dtype 表未核，不写"同表"）。主例 32×16×32 落于表内界内——**静态检查结论**。
- 主例 TLOAD 两侧物理存储次序不同（a2a3=Zz 系、CPU-SIM=Nz 系，EV I3/B7b），各由自身 `GetTileOffset` 自洽消费——"虚拟"的代价与机制同页呈现。
- NPU 后端目录（EV E1）；a6 仅注记（E2）；三编译形态宏矩阵一段带过（E3/E4）。

## 24.7 延伸：Manual 上限与 comm 一瞥（≈300 字）

- manual gemm_performance 双缓冲/四段流水作"同一 ISA 的手工上限"注记（EV C4）。
- comm 扩展只述三类存在（EV A2），不列清单、不写 NPU 语义（G4）；性能数字纪律（G6）。

## 24.8 复现（≈300 字）

- 命令链（EV F4）＋勘误脚注（G1）；**明确"既有二进制复跑"与"首次构建"两句分开**（F2）。
- 结尾：「以上为 CPU 仿真验证；未在 NPU 设备上运行」（F5）。

---

## 图规划（3 幅；图前自然问句/图后「读图：」/一图一问；Playwright 截图＋SVG textContent 核签）

| # | 回答的问题 | 数据来源 |
|---|-----------|---------|
| ①存储旅程 | "TMATMUL 的 operands 与结果各经哪些层级、由哪条指令搬运？" | C4＋D5；注"层级名为仿真器内存模型" |
| ②三层结构 | "容量形状、有效区域、物理布局各控制什么？valid 是自动的吗？" | 主例真实配置 32×16/2048B/16×8 分形＋hypothetical valid；偏移与字节 `ch24-tile-offset-compute.log`；valid 语义差异引 I1 |
| ③双轨时间轴 | "同一依赖，设备侧与 CPU-SIM 各发生什么？" | C4 配对＋C1a 事件链 vs D2/D3 no-op；注"逻辑示意非实测时序" |

## 写作红线（自查）

1. 不写 A5 dtype 表定论、a6 支持、comm NPU 语义、CostModel 行为、无出处性能数字。
2. 设备侧只写"静态合同/实现存在"，实机不写"实测"；CPU-SIM 结论冠"仿真"。
3. B8/I3 只陈述别名与合同事实，不编硬件成因。
4. 脚注全路径；交付附 RESPONSE＋rg 核验。
