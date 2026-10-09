# CH24-EVIDENCE-CLOSE 回应（2026-10-10）

逐项对照 `management/tasks/CH24-EVIDENCE-CLOSE.md`。核验方式：改动后对终态文件 rg 实测（附计数）；日志落 `management/validation/`。

## 1. B7 布局分层（GM 行主序 vs BLayout 分形块）

- EV B7 重写：`GlobalA` stride 末两维 `(kK,1)`＝行主序（gemm_demo.cpp:83，kM=32/kK=16 实值）；`TileMatA` 的 `BLayout::ColMajor` 仅指 512B 分形块排布，块内 `SLayout::RowMajor` 另论——三层不混同。
- TLOAD 转换语义新立 B7a：`cpu/TLoad.hpp:127` `TLOAD_TILE_IMPL` 先 `std::fill` 填满容量（L142）再按 valid 双循环 `GetElement/SetElement`（L151-157）。
- 偏移实算：`management/validation/ch24-tile-offset-compute.log`（脚本内嵌）——elem(1,1)：GM 行主序偏移 17，tile 存储偏移 9；容量 512 float=2048B=4×512B 块。
- 提纲 24.2 相应改写；图②数据来源改真实配置。

## 2. C1 收窄＋主例/设备例分离

- C1 重写：`TASSIGN` 返回 void（pto_instr.hpp:28）；`TLOAD/TMOV/TMATMUL` 返回 `RecordEvent` 且 WaitEvents 可空；明写"主例未用 ev"。
- 新 C1a 设备真实事件例：`kernels/manual/a2a3/moe_combine/moe_combine_kernel.cpp:537/547-556`（`Event<TAXPY,TLOAD>`→TLOAD→TAXPY→Wait），与主例分开引用，未拼接。
- 提纲 24.4 拆为"主例无事件（仿真便利）"与"设备两真相（事件链/流水屏障）"。

## 3. 图②实配置＋valid 语义

- 图②改主例 aTile：32×16 float、容量 2048B、16×8×512B 分形；有效区域用 hypothetical 动态 valid 并标注；弃 16×16=1024B 与 8×8 假想格（EV 图规划②行、提纲 24.3）。
- 新 §I1：TLOAD 填 pad 抄 valid／CPU TMATMUL `TMatmulNzZn` m,k,n=GetValid（cpu/TMatmul.hpp:51-57）／TSTORE 容量≥valid 积断言（cpu/TStore.hpp:22-37， NZ 精确相等）——"valid 非自动遮罩，逐指令合同"。
- 复算脚本+输出：`management/validation/ch24-tile-offset-compute.log`。

## 4. 可移植性不承诺

- 新 §I2：a2a3 `CheckStaticMad`（TMatmul.hpp:78-96）dtype 四组含 (float,float,float)；`MMAD_MAX_SUPPORT_LENGTH=4095`（L17）；`TMATMUL_IMPL` m/k/n 取 valid+CheckDynamicMad（157-167）。注明**静态检查结论，未实机**；a5 仅 L20 同界、dtype 表未核。
- 新 §I3：TileLeft 分支只证别名映射；两侧物理次序不同（Zz 系 vs Nz 系）由各自 GetTileOffset 自洽。正文措辞收窄（G9、提纲 24.6）。

## 5. 引文与计数纠错

- A1 重引：README_zh.md:7 原文「PTO（Parallel Tile Operation）是昇腾 CANN 定义的……虚拟 ISA」，"AI OCR/Pangu"旧句弃。
- A2 收窄：只留 README"90+"口径（L23/L28）与 comm 三类存在（L30），139 去重计数与 12 指令清单删（G7）。
- B1 去参数计数，改"含有效形状参数、默认等于容量维"。
- E1 改引 badge L10＋A5 新闻 L18，删"或根 README"。

## 6. 复跑与措辞

- 复跑输出存档：`management/validation/ch24-cpusim-gemm-rerun.log`（含工具链版本尾注）；明确**既有二进制复跑、非重编译**（F2/F2a）。
- 工具链回源：PTO-CPU-GEMM.md:5「g++ 16.2.1 20260810，CMake 4.4.2」与本轮输出一致。
- 提纲全篇改"本书环境实测（CPU-SIM）"，删"刚在你的 CPU 上跑/NPU 运行"句。

## rg 终态核验（写后实测，2026-10-10）

- `rg -c 'AI OCR|Pangu' CH24-EVIDENCE.md` → 0（无输出）
- `rg -c '139' CH24-EVIDENCE.md` → 仅 1 处＝`pto_tile.hpp` L1395 行号引用，去重计数句已删
- `rg -c '刚在你' CH24-OUTLINE.md` → 0；`rg -n 'NPU 运行' 两文件` → 仅提纲头部纪律句（引任务书措辞）1 处
- `rg -c 'dst, src, ev' CH24-OUTLINE.md` → 0
- `rg -c 'ch24-tile-offset-compute\.log|ch24-cpusim-gemm-rerun\.log' CH24-{EVIDENCE,OUTLINE}.md` → 各 3
- `rg -c 'hypothetical|假设动态'` → EVIDENCE 1、OUTLINE 2
- `ls validation/ch24-*` → `ch24-cpusim-gemm-rerun.log`、`ch24-tile-offset-compute.log`（rerun 尾注含 g++ 16.2.1 20260810 / CMake 4.4.2，与 PTO-CPU-GEMM.md:5 一致）

交付物：`CH24-EVIDENCE.md`（rev2）、`CH24-OUTLINE.md`（rev2）、本回应、上述两日志。未动 23 章正文，未提交。
