# CH19-R1 响应（CH19-R1-RESPONSE）2026-10-09

逐项 13 条；每条给「原句→新句/删除」定位（行号为本响应自检时 grep 所得，正文行号以编辑后文件为准）与回源。**真实 diff**：`git diff HEAD -- docs/04-perf/ch19-perf-analysis.md`＝237 insertions/24 deletions（含 R1 前未提交底稿与本轮修订的合计；本轮针对 R1 的净改动见各项引文）。**未改 CH18**（本轮零触碰 `docs/03-ascendc/`，前轮 build 修复已由经理知悉，本响应不再主张）。

## P1 可回源错误

**1. simulator 命令/产物**（原 L47 区）
- 原：`msopprof --simulation ./demo`…`simulator_data{ts}/…summary.csv`＋「无真实 DDR/L2 竞争、频率模型化」。
- 新：**`msopprof simulator --soc-version=Ascendxxxyy ./add_custom`**（performance_tuning.md L206-209 原文）；产物 `OPPROF_{ts}_XXX/`：`dump/`＋`simulator/{core*.cubecore0,core*_code_exe.csv,core*_instr_exe.csv,trace.json,visualize_data.bin}`（L210-233 表 4）；前提=仿真编译（L199-201 `bisheng --run-mode=sim`）＋环境变量/`-g`（表 1 注）＋**soc 占位须替换**；「无 DDR/L2 竞争」模型保证句**删除**，改「仿真-真机对应关系本书无数据（U5），性能结论须上板复测」。
- 表 1 行同步补全（命令/前提/产物三列真码）。

**2. ProfConfig 与「一族」推断**
- `PROF_MAX_DEVICE_NUM`→**`PROF_MAX_DEV_NUM + 1`**（prof_acl_api.h L18/L49-56 真码，=`64+1`）。
- 原「一次采集只带一个…不能一次采全」**降级**为「该库配置字段为单值枚举，**只证明库侧配置形态**；msopprof 各模式行为以《用户指南》为准（仓外，新增未证项 U6）」。

**3. 带宽不一致与 950**
- 原「0.0007 差为舍入」→**「case5 复算 2.2878 vs 总表 2.2755（差 0.0123）、case6 2.3463 vs 2.3456——源文表与公式复算不一致，原因未确定（输入取整？分母取列有异？），两组数并存，不归一为舍入」**。
- 950：**删除无据复算**——950 表无 mte time 列，同公式不可复算；case3=1.454/case2=1.184 直接引用。原正文 1.456 系误用 A2 数据，已改。
- 复算落真脚本 **`management/validation/ch19-offline-calc.py`**（可复跑，exit=0）＋log 为其输出；正文 pfH 同步改。

**4. 数字逐列**
- 0→1 段原「scalar 1233742→vec 231（5341×）」混列→改 **Task 1239689.1→6909.6（源表 179.4×，复算一致）**，实现内 scalar 指标 1233742→231.166、vec 761.65（11%）分列陈述；「mte2 占 87%成瓶颈」→「接棒成主要耗时项（观察，瓶颈判定须带宽佐证）」。
- 读表段「6700×」→**源表 6718.5×＋精确复算 6718.53 并列**。
- case0 深读「效率 0.02%」**名义删除**→「实现级落差 4357×＝scalar 实现耗时/向量理论，**不称硬件效率**（scalar 本不用 Vector 单元）」。

**5. 编译链**
- 原「一行箭头完整命令」→**完整工作流代码块**：副本内样例绝对相对路径、`mkdir build&&cd build`、cmake/make/`gen_data.py`（仓内 scripts 实名核实）/`./demo`/`verify_result.py output/golden 双参`/`msopprof`；环境前提 `source set_env.sh`＋架构按真机替换；「切换须清 cache」**降级**——README 仅 RUN_MODE 切换要求清 cache（L632 区），SCENARIO_NUM 清不清未验证（新增 U8），「无须按序编译」明示。

## P1 口径冲突重写

**6. 四层框与差额句**：L1 改「**任务级**…**非完整用户端到端**」；「L1−L2=调度尾、L2−L3=等待重叠」→「跨层差值只是**待验证候选解释**——须时间锚点（OpTime 双对）或分布证据」。19.3 校验④「稳定则视为调度常数」→「稳定则可作**候选证据**（仍须锚点确认）」；19.5 读表段「差=调度+收尾/更多核=更多同步尾」→「差额放大是观察，成因待 19.4 双锚点/分布验证」；19.6「Task 远大均值⇒尾核」→「**提示**尾核，确认须 per-core 分布，差额不构成证明」。

**7. case4/5/6 因果**：3→4 段重写——「重叠覆盖几乎全部活跃窗」「收益被 mte3 竞争吃掉」降为**作者候选解释，明标须 timeline/csv 验证**，数据内只说「占比结构大变而端到端几乎未动」。4→5「两指标反向才是机制成立的证据」→「同时出现也只是**与假设一致，非因果充分**（无该 csv，U9）」。5→6「冲突只拖计算不拖搬运」→观察级＋须 csv 佐证（U9）。19.3 同步：命中率句改「bypass 反而降低命中率却提速（观察）」。

**8. 带宽差值与机械规则**：「两者差值=非搬运时间」量纲错→「**分母窗口不同，不可相减或直接对照**」；「四条全过才准解释」→「校验不闭合先疑自己；闭合只证自洽不证解释」；「每跳必须换证据源」删除。

**9. 19.6 数值**：均值算例统一 **50 核=47×5＋3×50，均值 9.7μs**（19.6 首条与算例段一致，脚本同）；E-A 判据改「理想斜率 **−1**；偏离不设单值阈值，接校验④与差额分解」；case2→3 明标「**未变核数，非核数饱和证据**，仅同核下带宽未饱和旁证」；E-C「5%即止」→**作者示例＋须大于实验噪声带**。

**10. 19.4 证据边界**：整节重写——Type01/2/3 字段级真码（L129-160：01=taskId+streamId、2=+coreId/blockId、3=+warnStatus）；「每核 start/end 对」「Task Duration 由该类事件聚合」→**「analyzer_hwts.cpp L68-98 真码：仅 type=0/1 的 Type01 以 taskId+streamId 为键写 start/end——库内确有此构造路径」**＋两边界（Type 字段其余 7 值语义未文档化 U7；「analyzer 会构造」≠「msopprof csv 列由此生成」，csv 判读挂 README 字段表）。误读 1 的「恒定偏移/比例放大」判据**删除**（无数据支撑），改「先查键与 ageFlag，偏移模式不作正误判据」；「startAicore=首核事件」表述删（19.1①只保留「字段差分证实区间结构」）。

**11. 运行环境**：`npu-smi 确认独占`→「**查询≠独占保证**，独占须集群/环境管理配合并记录」；「预热与排空」拆**两条**——软件流水 warm-up/drain（被测对象结构，pto-isa 出处）vs 实验预热/重复采样（测量协议：≥5 次、中位数、报极差），「前者不能替代后者」。

## 完整性与图文

**12.** 脚注 `.../` 全部展开实际路径（pfA 7 条全路径＋基线 commit；pfE 改「驱动查询频率路径（查询返回值，非实验实测瞬时频率）」）；19.5 案例头补**五要素**（架构 dav/基线 commit `28e7aba2`/CANN 商用版/NPU 挡/口径 L1-L3 引用+L4 复算）；pfB/pfC/pfG 补 SOURCE-BASELINE commit（runtime `681ef761`、asc-devkit `28e7aba2`、pto-isa `dd3cb0fb`）；avp/dvvp「主流」→「分工从目录存在性不可断言，仅作代码位置陈述」。

**13.** 删重复：19.3 双引言合一；19.4 重复句/双「免费午餐」/重复脚注引用合并；19.7 模板双写合一（并补基线 commit 字段）；`19.8b`→**19.9**（原 19.9→19.10），交叉引用「19.8」改 19.7/19.8。frontmatter `status: 待审`。图 SVG 文字同步（「红线」→「待验证候选」；「每跳换证据源」→「源码结构与工具 csv 并列两源」）——**渲染验证**：rsvg-convert 出 PNG（`validation/ch19-svg.png`）＋按设计坐标的色块存在性检查（六区块 558–745 像素命中，全非零）；**此为色块存在性检查，非布局审查**——布局人工目检待 PM。

## 校验结果（真实命令与输出）
- `python3 management/validation/ch19-offline-calc.py`→exit 0；case5 diff **+0.0123**/case6 +0.0007（正文按此表述）。
- `npm run verify`→`management/validation/ch19-r1-verify.log`，**0 FAIL**，ch19 行 `8,474 字（中文 6,580）`。
- `npx vitepress build docs`→complete；HTML `footnote-ref`=25、`<img>`=1（SVG 内联）。
- 脚注配对 8/8（pfA–pfH，脚本核）。

## 状态
逐项已改；**未自验收**。等经理复审。U6/U7/U8/U9 已入 19.9 未证项清单。
