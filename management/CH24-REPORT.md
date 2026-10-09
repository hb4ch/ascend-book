# CH24 报告（写书轮，2026-10-10）

交付：正文 `docs/06-backend/ch24-pto-isa.md`（3,526 字/中文 2,420，verify 0 FAIL）；图①–③ mermaid 内嵌正文＋PNG 截图 `management/validation/ch24-fig{1,2,3}.png`；证据 `CH24-EVIDENCE.md`（rev2）；回应 `CH24-EVIDENCE-CLOSE-RESPONSE.md`。

## 写前纠偏落实（对照 CH24-WRITE.md 逐项）

1. **I2 dtype 三元组统一 (A,B,C)**：EVIDENCE I2 现为 `(A=int8,B=int8,C=int32)、(half,half,float)、(float,float,float)、(bf16,bf16,float)`（rg 实测 L105）。正文 24.6 同口径。
2. **I3 两次搬运分清**：正文 24.6 明写——TLOAD 目的 aMat 为显式 `BLayout::ColMajor`，两侧同构，**不能**由 TileLeft 别名推「TLOAD 布局因代际变」；别名差异落在第二次搬运 TMOV 的目的 aTile；并补「A2A3 TMOV 是否额外重排未逐行核」。EVIDENCE I3/B7b 同步改。
3. **图②字节数**：正文 24.3 与图②均为「每块 16×8 float＝512B、2×2 块共 2048B」；旧「16×8×512B」表述已从 EVIDENCE 清除（rg=0）。图②用 aMat 真实配置（非 aTile 别名）；动态 valid 标注「非主例」且写明须 DYNAMIC 模板＋SetValidShape（正文另引 L1610-1626 static_assert 相容性）。
4. **数值/性能措辞**：24.5 明写「CPU 对拍证明结构与数值，非设备时序」「demo gflops 为 CPU 仿真参考值，不得当设备性能」；24.6 设备精度「以源码与官方文档限定为准，不保证与 CPU 对拍一致」；全程无 CPU perf 冒充设备数据。
5. **复算脚本可复现**：`validation/ch24-tile-offset-compute.py`（脚本）＋`.log`（输出）分离存档。

## 结构（对应补证提纲 rev2）

24.1 问题与边界声明 → 24.2 主例五步＋TLOAD 转换语义＋偏移对照（图①）→ 24.3 三层形状＋valid 逐指令合同（图②）→ 24.4 事件/屏障双机制＋CPU-SIM no-op（图③）→ 24.5 仿真边界（A5 placeholder 等）→ 24.6 别名双分支＋设备合同＋两次搬运 → 24.7 Manual 上限/comm 一瞥 → 24.8 复现（CPU-SIM 已复跑；设备未验）。12 脚注全路径、闭环（rg 每条 ≥2 处）。

## 图（mermaid 内嵌；mmdc 渲染 SVG＋Playwright 截图）

| 图 | 尺寸(px) | textContent 核签 |
|----|---------|-----------------|
| ①数据旅程 | 1356×93 | TLOAD/TMOV/TMATMUL/TSTORE/行主序/valid 全命中 |
| ②三层形状 | 662×1376 | 32×16/2048B/512B/ColMajor/SetValidShape 全命中 |
| ③双轨依赖 | 1177×505 | Event/Wait/SetFlag/TSYNC/程序顺序 全命中 |

foreignObject 高 48px＝2 行×24px 行高，无截断；节点文字 nowrap 由 `<br/>` 分行。图①③注「不画时序/逻辑示意」；图②注 hypothetical 非主例。

## 校验记录

- `npm run verify` → 0 FAIL：`management/validation/ch24-write-verify.log`（含字数行）。
- bash 语法：正文唯一 bash 块 `bash -n` 通过 → `ch24-write-bashn.log`；块存档 `ch24-write-fence.sh`。复现块注释明示「CPU-SIM 已复跑；设备未验」，无「需真机」误导（本章复现不需 NPU）。
- 偏移复算重跑一致（elem(1,1)：GM 17 / tile 9；2048B）。
- CPU-SIM 复跑二进制直接执行（非重编译），日志 `ch24-cpusim-gemm-rerun.log` 尾注工具链与 `PTO-CPU-GEMM.md` L5 一致。

## 自查声明（读回实文后）

- 正文无「AI OCR/Pangu」旧句、无 139 计数、无「在你的 CPU 上跑/NPU 运行」措辞、无 `TSTORE(dst,src,ev)` 拼接（rg 均 0/符合）。
- 未核事项如实入文（24.6/24.8）：a5 dtype 表、CostModel、comm 设备行为、a6、A2A3 TMOV 重排细节。
- 未动 23 章及其它章；未提交；未换模型。遗留：PM 验收后按意见修订。
