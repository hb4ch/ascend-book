# CH18 交付报告

> 2026-10-09。正文 `docs/03-ascendc/ch18-flash-attention.md`＋图 `docs/figures/ch18-fa-pipeline.svg`＋TRACE/REPORT；verify 见 `management/validation/ch18-verify.log`。

## 覆盖与自审

- **主线**：arch35 非量化训练 Nd 全程；fp8/Nz/推理仅岔路表（§18.8）点名；arch22 仅入口级对照。
- **经理四点落实**：①末块三分支互斥结构按真码重写（§18.5），并**明文修正 TRACE §1 的「先 Last 后 LastDiv」连续误读**；②输出 cast=`Cast(…,CAST_ROUND)` 于 Bmm2DataCopyOut（§18.6 真码），不再标「非主线」；③buffer 语义按分支重述——**UB/GM 的 FORWARD 亦双向 Wait/Set、仅 L1 反向受 BOTH、双 AIV 独立 id+OFFSET 计数**（§18.7 三条实证），L1 复用/三环不变量降为「已见同步未证复用」，不依赖耗时关系；④Tiling 走查为「假设已选 128/128」，s2=256 先行分支未证归属如实双列。
- **字数**：见 verify log；word:count 口径中文 5.0k（**达 5k 底线、低于 8k 深度目标**——覆盖声明：未写 84 算子族谱（属 ch13 已有导览，仅回指）、未写三件套拆分（原提纲删，因主线收紧后非本章机制）、fp8/Nz/推理特化按岔路处理。由 PM 裁量。
- **脚注**：8 枚举（faa–faMath），正文引用→章末定义一一对应（verify 核对）。
- **图**：1 幺 SVG（四级流水+缓冲账+控制面注记，示意标注）；渲染待 dist 抽查。
- **未证边界**：L1 覆写保护、exp/sum 三环不变量、s2=256 分支归属、输出 cast 下游（PostQuant 细节）、数据面 flag 具体 id、2048² 自动选择——均正文标 U 或「未证」。
- **性能**：零数字，仅采集方法＋结构性论述（标设计目标非实测）；build.sh/examples 入口标未运行。

## 未动

ch17 全部、appD（待 PM）、README、全局计划；无 commit/push。
