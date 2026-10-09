# CH18-R2 响应（逐项：正文摘录×源符号×核查）

> 2026-10-09。verify→`validation/ch18-r2-verify.log`（中文 5,512）；build 绿；SVG 同步重注记。

## P1 GM 释放握手（核心）

**回源结论**：经理读源属实——
- vec2 GM 版：`sed 1625,1785` 全函仅 L1629 `bmm2ResBuf.WaitCrossCore()`，**无 SetCrossCore**（尾 `SetFlag<MTE3_V>` 后 `return`，L1762-64）。
- cube `IterateBmm2`：L2174-76 `if constexpr(bmm2Write2Ub){outputBuf.WaitCrossCore();}`——**GM 不 Wait id1**；但函数尾 L2220 区**有 `outputBuf.SetCrossCore()`**（就绪 id0，无条件）。
- `buffers_policy.h L178-91 Get()`：纯 a/b/c flag 轮换，无自动 Set/Wait。

**正文修订**（摘）：§18.7 第1条改「**方法能力≠调用闭环**」；第2条改「实际调用核查」——级1 UB＝**两侧四调用齐真闭环**（cube IterateBmm1Nd L1698 `Wait`→L1700 `Set`；vec L307`Wait`/L601`Set`）；级3 GM＝**仅就绪向**（cube 尾 Set id0／vec 入口 Wait id0），「GM 全路径无任何 id1 调用」。表重构为四列：**实际就绪调用｜实际释放调用｜软件环/生命周期**，GM 行明写「两侧均无 id1→无释放握手，复用靠 3buff 轮转错相，充分性未证」——**未画不存在的回执**。另 #2 行补证：vec1 就绪 Set 实为 **Nd L1292／Dn L406 区 `outputBuf.SetCrossCore()`**（P 就绪 id0），cube L598 `mm2A.WaitCrossCore()`——就绪向闭环、释放同样无。
**复用关系**：未跳「竞态」结论——写「轮转错相为已见机制、充分性本编尚未完成分析」（§18.7 未证①同改）。

## 1 事件方向/循环上界

伪码改 `Set<V_MTE2>/Wait<MTE2_V>（搬完→V）`并注「跨轮 bmm2Ub 复用由 `MTE3_V/MTE2_V` 守护（L1756 区）」；正文 L1666-84 描述同步改；循环 `for(vec2S1Idx=0; …<vec2LoopLimit; ++)` 不含端点——原文「0..limit」已改。

## 2 isUpdatePre

删「true 仅 fp8」「主线恒传 1.0」外推。正文现文：「`isUpdatePre=true` 变体在 **count==1 对 fp16 同样实例化**（GM L1726/UB L1406 `if(count==1)…true`）；`deScaleVPre` 仅 `if constexpr(INPUT_T∈{fp8,int8,hif8})` 才入 `Muls`（vf 门控原文），fp16 下参数无效——1.0 是调用值非变体专属性」。EVIDENCE §六.3 同。

## 3 bmm2Write2Ub 假设

§18.5 重载段加：「主线**假设 `bmm2OutPos=GM`**；TilingKey 位段定值条件本编未逐条考证，若实选 UB 则整体换 OnUb 重载」——机制条件案例明示，不称必然。

## 4 cast/PostQuant

改「**cast 后若无 PostQuant 即 V 域最后一拍**；PostQuant 启用时钩子在其后仍占 V——仅无条件量化输出成立，不泛化」。

## 5 全文清「FORWARD 闭环」

摘要句、陷阱2、兑现表行、SVG 三缓冲注记（「仅就绪 id0（无释放握手!）」）全部改为调用点口径；§18.7「已证」清单改「级1 双向已证／级3 仅就绪向」；**历史更正**：EVIDENCE 增「§六 R2 更正」节声明与前文冲突处以该节为准（非改写历史）。

## 附：核对脚本摘录

```bash
V=…/arch35/flash_attention_noquant_block_vec_base.h
sed -n '1625,1785p' $V | grep -n SetCrossCore   # →仅 5:1629 WaitCrossCore?实为Wait;SetCrossCore 0 处→GM 无释放
awk 'NR>=1625&&NR<=1785' $V | grep -c SetCrossCore  # 0（除空块短路在 OnUb）
grep -n bmm2Write2Ub …block_cube.h  # L2174-76 Wait 仅 UB 分支；L2220 区 SetCross 无条件
```
