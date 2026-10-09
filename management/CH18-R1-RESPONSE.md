# CH18-R1 退修响应（逐项对照）

> 2026-10-09。正文修订＋SVG 重画＋本响应；verify→`validation/ch18-r1-verify.log`（中文 5,313）。status 保持「正文」待审。

**1 双重载/主线介质**：✅ §18.5 重写——明示主线=**ProcessVec2 内联 else（GM 版 L1630-1770）**，先 `vec2S1BaseSize=8192/dTemplateAlign64` 切 64 行、GM→UB `DataCopy/Pad`＋`MTE2_V`（L1666-84）再累计；UB 重载（`ProcessVec2OnUb` L1319，含尾 `DivCast`/`stage2OutBuf`）标注「本主线不启用，仅岔路标识」。原§18.5 引用（L1404-1445）系 UB 版行号，已双载并列（四分支表行号列 GM/UB）。「表 dtype 与 mm1 Fixpipe 的 useDn/useNz 条件」：四分支表与 dtype 链均按主线 fp16 Nd；Fixpipe 双拆处补「fp8 才有 deScale 合成（cube L1397）」，useDn 分支不混入。

**2 首块**：✅ 分支树重写为**四分支**（外层 `count==0→DataCopy 直装`先于 FlashUpdate 家族；④单块 LastDiv 仅 `count==limit==0`），正文伪码标[示意]；§18.9 数值例接线改为「两块例第二块即末块直接 LastNew，三块以上才有 New+Last 序列」；§18.1「三分支」→四分支。原「单块同时 Last 与 LastDiv」误读已由互斥表消除（④仅 count==0）。

**3 拍数**：✅ 门控骨架重写（`taskId>0/>1/>2`＋`notLast*`），明示 **t=2 三级、t=3 四级齐**；环索引 `(t+3)&3=t−1` 等代数给出；**删「四个独立硬件单元」**，改「AIC 两级共享 Cube/AIV 两级共享 V，软件错相非物理并行」；**删「环深=级距+1 通则」**，改「本实现选择，无一般通则」；新增 0–6 拍任务表；**SVG 重画**（级2/3/4 块整体右移一/二/三拍，注记改门控与共享单元），xml 校验通过。

**4 数据流**：✅ **mm2 的 B=V**（删「K 两次使用」及「重入便宜」因果）；**scale=级2**（`ProcessVec1Vf` 参 `static_cast<T>(scaleValue)`，vec_base L363-491；mm1 出口纯 QKᵀ）——18.3 职责表与 18.4 同步改；「512 恰两组」→「512 fp32＝8 组 64-lane，阈值动因未证不下因果」；「64 行」处处限定 s1=128（s1=64 则 32 行）。

**5 Tiling**：✅ 重写证据边界：**`CalcTotalSize()`（L35-48）真码**——`totalSize<aicNum`∧非AA/无rope/非fp32,f8/d≤256 时（再∧s2>1024 无mask/pse/drop→s2=256）**s1=64**；否则 else 链 128/128；**aicNum 平台值未查**明写；走查改双支条件式，陷阱8同步。

**6 同步/LSE**：✅ LSE 句改「存 m/l 本身，LSE=m+ln(l) 需自行组合」；删「省一次专门通知」——改「回执存在，合并于生产者覆写前 Wait id1，时点差异非省略」；#2缓冲改 **`l1PBuffers=BuffersPolicy3buff`（a/b/c flag 轮换，buffers_policy.h L178-91）3 深环**（原「无环」错）；未证处改「本编尚未完成该部分分析」，删耗时/缺断言推竞态措辞；同核 HardEvent 与跨核 id 对各自表述不混。

**7 复演/覆盖**：✅ 数学例补「输入输出见 log 各节＋仓根一键复跑＋断言行」（站点内不裸链 management）；`ascend info`→**msdebug `ascend info cores`**（npu_board_debug.md 佐证）＋「本编未运行」；构建入口改「build.sh 先 ophost/opapi 再 UT，样例随 examples 单独 cmake」；尾块/mask 具体化已在 18.4（AttenMaskCopyIn 预取＋`s2EndIdx−s1BaseSize<s2BaseSize` 窗口判定 L419-21/441 真码挂点）——另见 18.9 走查。性能无数字保持。

**8 文稿**：✅ 两处 cpp 块→`text`＋`[示意代码] 源码删节（含中文注）`；18.8 表后空行补；fac 脚注 cube **全路径**；开头「前八章/Cube 五级」→「前十章（ch9–17）/Cube 流水」；结尾「全书收官」段改「主线收束＋第19章起 ch19–28」；「TRACE 曾误读」改中性「常见误读」；口号句删。

**遗留（非本次范围）**：s2>512 分支、PostQuant 内部、flag id 具体值——正文已标 U/未证。
