# CH18 证据收口报告（对应 tasks/CH18-EVIDENCE-CLOSE.md）

> 2026-10-09。主线机制已闭，正文可开工；残项均非主线并已在证据表标注。

## 已闭（U1/U2/U5/U6/U7/U8/U9 → 见 EVIDENCE §四′）

- **U1 精度**：mm1 fp32 累加→`QF322F16_PRE` Fixpipe→fp16 UB；双 AIV 经两次单目标 Fixpipe 拆行（cube L1440-1470 真码摘录）。
- **U2/U8 递推**：`dst=pre·expMax+cur`（vf L14 注释＋BasicVF 逐指令）；expMax 经 `softmaxExpBuf[taskIdMod3]` 三缓冲跨级；**NumPy 对拍通过**（fp64 误差 2.22e-16，tol 1e-12）——`validation/ch18-online-softmax.{py,log}` 存档；**仅数学验证非 NPU/kernel 验证**（脚本头注明）。
- **U5**：块尺寸=TilingKey 模板选择（S1 16..256/S2 16..512/D..768，`s1BaseSize=(uint32_t)s1TemplateType`）；场景值残 U5′。
- **U6**：`SYNC_MODE=4`＋flag15=kfc host 消息（ssbuf 拷 CVSharedParams 前置），数据面同步在 Buffer SyncType。
- **U7**：中间 half/GM fp32 双层；尾维 8=对齐槽位（注释原文），非头数；half 舍入策略残 U7′。
- **U9**：mask 挂点确认，尾块分支保持挂点级。

## 未闭（非主线，正文标注即可）

U2′ 末块归一化除法精确行位；U3 s2>512 分支；U4 arch22 深对照（已按任务要求做入口级：arch22 无 regbase 套件、入口 `flash_attention_score_s1s2_bn2gs1s2_b.h` 旧 API 世代——主线声明以 arch35 为准）；U5′ 场景模板值；U10/U11 算子边界已在 E16/E15 明示（推理走 fused_infer_attention_score 等独立算子）；U12 性能留白（无来源不凑）。

## 数学对账记录

- 形状 S1=S2=4、D=2（Q/K/V 4×2），KV 块=2；全量 vs online 最大差 2.220e-16（O）、0（P）；逐步 m/corr/l 迹见 log——**可直入正文 18.1/18.5 作数值例**（blk2 corr=[0.2882,0.6967,1,0.376] 展示重缩放非平凡性）。
- 脚本断言失败即非零退出；seed 固定 20261009 可复跑。

未动 ch17/appD/正文；未提交。
