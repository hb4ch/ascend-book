# CH18-R3 响应（残留清除＋模板选择闭）

> 2026-10-09。verify→`validation/ch18-r3-verify.log`（中文见 log）；SVG 渲染 PNG 存 `validation/ch18-svg-render.png`。

## 1 模板选择补闭（GetC2Position/UbOutCondition 真码）

`common/op_kernel/arch35/flash_attention_score_common_regbase_arch35.h`：
- `UbOutCondition`（L163-89）：可选输入（pse/atten/drop）全无时 `!isS2Base64||isFp32→true`（另有 fp8/int8+rope、fp8+mask 前支）。
- `GetC2Position`（L191-216）：`d≤Aligned128→VECCALC`；`d≤Aligned192∧UbOut→VECCALC`；`isNdS2Size256→VECCALC`；**否则 GM**。调用点 cube L153-158 实参：`UbOutCondition<INPUT_T>(isFloat,pseMode,hasAtten,hasDrop,hasRope,s1BaseSize==64)`、`isNdS2Size256=(s2Base==256&&s1==64)`。

**推导（主线 fp16/PSE_NONE/无 atten·drop·rope）**：`ContainOptionalInput=false→UbOutCondition=(!isS2Base64)`。
- s1=s2=128：isS2Base64=false→UbOut=true，且 d=128≤128→**VECCALC（UB）——原「128/128/D128 走 GM」不成立**。
- **GM 可满足组合（本章新主线）：D=256（Aligned256）**——`d≤128` 假、`ubOut∧d≤192` 假（256>192）、isNdS2Size256 假→**GM 恒成立**（与可选输入无关）。次选：D=192＋含可选输入且 s1Base≠64。
- useDn：`IsDn` 要求 `!isS1Base64∧d≤Aligned256∧无rope`——D=256 边界内可成立，但 **dn 与主线 Nd 互斥**（正文主线 Nd 不受影响）；useNz/splitD 均非本组合（splitD 另岔）。

**正文落点**：§18.5 重载段整段重写为上述真码＋推论，**「假设 bmm2OutPort 未考证」删除**；主线明定 **fp16/s1=s2=128/D=256→GM（已证）**；D≤128 恒 UB 提示读者转 OnUb。§18.9 走查改 D=256（vec2 切片 8192/256=32 行/轮）。

## 2 残留逐处（改前→改后）

| 位置 | 改前 | 改后 |
|---|---|---|
| §18.7 已证条 | 「级1/级3 的释放回执闭环（BOTH 语义…）」 | 「级1 UB 释放闭环（双向齐）；级3 GM 仅就绪向——**无释放调用可证，不存在『释放已证』**」 |
| §18.7 两代范式段 | 「级3…即范式Ⅱ的释放环」「两范式的回执都存在（FA 级1/级3 的 AIV 均须 Set id1）」 | 整段重写：级1＝范式Ⅰ式双向四调用；级3＝**仅就绪半边、非范式Ⅱ**（slot＋双向 flag 不存在），轮转充分性未证；级2 同仅就绪 |
| §18.7 表后 | 「任何一级漏发，流水…停摆」（泛化释放） | 「**就绪向**漏发→Wait 永挂；GM 释放向无调用，不存在漏发释放问题」 |
| §18.7 表 #1 | vec 释放引 L601 | 改 **Nd 尾 L1292**（注明 L601 系 Dn 分支勿混）；「双向齐」改「就绪向齐＋释放向亦齐（级1 真闭环）」 |
| §18.7 表 3b 行 | 「未逐行核」当正文 | **整行删除** |
| §18.9 步4 | 「覆写槽前等两 AIV 的 id1 回执」 | 「尾 Set id0 就绪——**无释放回执步骤**，槽位轮转 3buff」 |
| §18.3 职责表级3 | 无同步注记 | 补「Set id0 就绪（无释放调用）」 |
| SVG 注记 | 「3 深释放环」（更早已改）/「无回执」措辞 | 统一「无释放回执——3 深轮转，充分性未证」；xml+渲染复验 |

全文 `grep '释放环|释放回执|双向|已证'` 复查：剩余命中均为级1 真闭环/能力≠调用/未证清单语境，无 GM 释放闭环残留。

## 3 SVG 渲染

`rsvg-convert` 出 PNG（`validation/ch18-svg-render.png`，920×560）：像素统计绿块 rows 200-220 存在、三错相首块 x≈245/335/425 递增——**渲染级验证**；R2 报告「SVG 同步」措辞于此更正为「XML 校验＋本次渲染核验」。

## 4 验证

`npm run verify`→`validation/ch18-r3-verify.log`；脚注/vitepress build 同前绿。未动 ch17；未提交。
