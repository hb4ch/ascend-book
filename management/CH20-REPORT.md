# CH20 交付报告（CH20-REPORT）2026-10-09

## 交付物
- 正文 `docs/04-perf/ch20-opt-topics.md`（word:count **6,256 字／中文 4,446**）
- 图 `docs/figures/ch20-opt-decisions.svg`（三决策同构地图＋验证五元组/闸门带；**渲染验证**：rsvg-convert PNG `validation/ch20-svg.png` 四色块像素统计 2606/2552/2499/4936 全非零——**存在性检查，布局目检留经理**）
- 数学核验 `validation/ch20-bank-sim.{py,log}`（**按 CH20-WRITE 约束先修后跑**：idx 0..7、baseDb 参数化 950 bank8、H∈{144,128} 双枚举、assert 边界/覆盖/GM 末端；结论措辞「八个不同组，非周期预测」；exit 0）
- verify `validation/ch20-verify.log`（0 FAIL）；build 过；脚注 5/5 配对（oA–oE）、HTML fn=7/img=1

## 写作硬约束逐项覆盖
| # | 约束 | 落实 |
|---|---|---|
| 1 | RegAPI≠SIMT；混编真决策点 | 20.1 明写「A2 Copy→950 Reg 是 **SIMD 内部实现差异**」；混编证据另立 **20.5 FloorMod case2→3 线程映射**（ch11 未用之样例，真码＋四 case 全表），范围声明回指 ch11 |
| 2 | 950 S2 三处改动；UB 账分列 | 20.1 明列 stride＋bank8 偏移＋pong padding 三处；A2/950 总账分开（147456/148480B），「+256B 每 nz buffer、950 另两处」原文级；分配表达式 `nzBufBaseOffset` 作准 |
| 3 | 脚本 0..7/baseDb/H 枚举/assert；措辞 | 已改并实跑（输出「八个不同组」无拍数断言；assert 覆盖尾块/跳 pad/GM 末端） |
| 4 | Task 差正数 | **7.42／1.288**（旧 6.7/4.4 已废）；全算术脚本/正文对账 |
| 5 | data_copy 措辞 | 「只读 benchmark＋地址合法性/覆盖前提三件（整除/mod 非零/组内置换）」；「访问同一输入是有意设计」明写；−39.05%/−1.94% 精确值 |
| 6 | 4:2 语义；sparse 真链；dtype/架构 | 「每 4 最多 2 非零」原定义；A 全尺寸/B 预压缩/索引作用按 API；int8/A2A3 限定＋950 U8；真调用四步 |
| 7 | MX/FP8/HiFloat8 分立；无博客倍数；scale 开销假设标注；格式/同步仍在 | G2 表三系分立（e5m2 也入）；博客数字仅存 EVIDENCE；压缩比带「不含 packing 对齐」假设句；「同 K block 节奏」流水约束原文级 |
| 8 | 命令真实；可写副本；SVG 真结构 | 20.6 验证矩阵（目录/编译维/采集/判读四列）；副本＋build-caseN 承 19.5；SVG 表达已证结构（三层面同构+闸门），无装饰 |

## 未覆盖/裁剪声明（ACCEPTANCE 核心章 8k 目标）
中文 **4,446＜8k**：已按「论证密度优先」写满三决策五元组＋误用警示×5＋闸门表；**未展开**：LoadData3D v2Pro 参数差异、稀疏索引生成算法、3510 样例逐场景、950 nd2nz Reg 逐指令——均 U 号存 EVIDENCE。**请 PM 裁量**：接受现状或指定扩写方向（候选：20.1 拓扑算术例题化／20.4 索引编码图解）。

## 验证汇总
verify 0 FAIL；build complete；脚本 exit 0 且含 assert；SVG 渲染像素验证（非目检）。CH16–19/appD/全局零改动；git status 仅 ch20 相关＋本报告。

## 状态
**待审**。等经理；不自验收、不提交。
