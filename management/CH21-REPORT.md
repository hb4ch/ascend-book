# CH21 交付报告

日期：2026-10-09　写手：pi (GLM-5.3-Flash)　状态：待验收

## 交付物
- 正文 `docs/05-comm/ch21-hccl.md`：9,574 字（中文 7,104，R1 退修后；`npm run verify`）。**低于核心章 8k 下限，声明 PM 裁量**：本章为「边界与结构」章（三层证据分立＋条件式选择），未注水目录化；如需扩充方向已在正文「读 SelectAlg 的正确姿势/走查一例/词表」给出可续写锚点。
- 图 `docs/figures/ch21-hccl-layers.svg`：三证据范围＋服务端汇流结构图；无数据数字（免重渲染义务）；渲染像素验证 `management/validation/ch21-svg.png`（940×360，四色块 5326/5387/5465/11137 采样命中）。
- 复现矩阵：21.8 命令链为本书整理（R2 后：set -e→source set_env→MPI_HOME 可配→环境检查→mktemp 副本→make/test），流程依据 01 README/Makefile；未运行→〔需真机验证〕；`bash -n` 存证 `ch21-r2-bashn.log`（exit 0）＋verify log `ch21-verify.log`（0 FAIL）。脚注路径经逐文件 `test -f` 实核（R2）。
- 需求落实：AllReduce 结果=按元素 N·j（N=2→[0,2]）手算声明；isMesh/isMeshTopo 变量映射（L299-341 区注＋陷阱②）；三范围不互证（21.1 warning 框＋各节脚注锚）；U 号就地化（21.4 断点段/21.7.3 仓外声明）；无新增性能表（量纲只给源码常量）。

## 覆盖
21.1 三层证据/名词表→21.2 创建三路径+拓扑模型+v1/v2→21.3 Host 主线（参数/异步/生命周期/入口层）→21.4 legacy 选择（链/两级/910B 全式/走查/覆写/平台表）→21.5 四引擎+二分语义+签名→21.6 Device API（五步/两编排/950CCU/A3 注/MC2 衔接）→21.7 notify 闭环+词表+精度二案例→21.8 复现/维测/平台速查/陷阱 7 条。

## 未覆盖/限制
- 950 AIV URMA 共享内存通信（525 行博客）→ ch23；SymWin/HIXL 对照与单边集合通信 → ch22；MC2 完整工程 → ch23。
- Host L1 算子实现、`04_custom_ops_p2p` 参考工程、hccl_vm 北极星：仓外未核，正文已声明。
- legacy 仅 910B 分支全式展开；910A/310P 选择器未逐条（正文声明同法可查）。
- 多机无实测；notify 多轮环槽无证明（正文仅一次交接）。

## 自检
verify 0 FAIL；build 过；脚注 oA-oH 双向闭合（HTML fn=28）；图 1 幅像素验证过；内联 C/D/I/U 标与脚注组映射见 21.1 warning 框。
（R1 退修后字数更新见 CH21-R1-RESPONSE。）