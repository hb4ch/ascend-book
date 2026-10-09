# CH25 提纲 —— PyPTO：Python 内核如何落到芯片（rev2 精简版）

rev2（2026-10-10，EVIDENCE-CLOSE 收敛）。证据：`management/CH25-EVIDENCE.md` rev2（下称 EV§x）。
**可读性优先，不强制 8k**；主线只保留 4 个机制：**前端约定 → 两级编译（IR/切图）→ 生成 CCE 调 PTO → 三种执行路径**。单主角 `abs_kernel`（4 行有效代码，EV§B1），全文不再出现第二套术语体系；43-pass 全表、七步 IR 全表、六阶段矩阵、标量参数/内联函数旁支全部降为一句带过或脚注。

主例（唯一代码主角，`examples/01_beginner/compute/elementwise_ops.py:76-80`）：

```python
@pypto.frontend.jit(runtime_options={"run_mode": ...})
def abs_kernel(x: pypto.Tensor([], pypto.DT_FP32), out: pypto.Tensor([], pypto.DT_FP32)):
    pypto.set_vec_tile_shapes(2, 8)
    out[:] = pypto.abs(x)
```

---

## 25.1 这四行代码的旅程（开篇即主线，~1.5k 字）

问句开篇：「`abs_kernel(x, out)` 敲下之后，这四行代码要经过哪些站台才能变成芯片上的指令？」按时间给五站，每站一句结论，文件:行全部入脚注：

1. **装饰期**：只包一层 wrapper，不编译（惰性，首调才编，EV§C1）。
2. **校验**：torch 张量、连续、dtype 按注解强校验；`[]` 形状注解=不锁形状（EV§B2/B3/G4）。
3. **前端编译**：Python 侧 IR 管线把函数降为 IR（EV§C3，只讲"降级+若干规范化+定型"一句，步骤清单入脚注）。
4. **后端编译**：C++ pass 流水线完成切图（Tensor→Tile/TileOp）、内存分配、插同步，最后码生成（EV§A1/D1/A3；pass 名举 2-3 个例子，不全列）。
5. **执行**：按 run_mode 三选一（25.5）。

图①（主图，mermaid LR）：**五站管线**。节点写动作（"包装不编译""降为 IR""切 Tile/插同步""拼 CCE 调 TileOp""按模式执行"），文件与长符号只放脚注/图注；624px 验收。

## 25.2 前端约定：注解、out 与 tile 提示（~1k 字）

只讲三件读者写内核必须知道的事：

- `Tensor([], DT_FP32)`：空 shape 不校验、dtype 强校验（`entry.py:690` 跳过分支，EV§B2/B3）；动态维写法一句带过（EV§G1）。
- 无返回值：`out[:] =`，框架 docstring 原文「returns None; caller holds output tensors」（EV§B4）。
- `set_vec_tile_shapes(2, 8)` 是**提示不是结果**：tile 会被钳到张量实际形状（resolver 原文 "clamped to the operand's own shape"，EV§K4）；官方约束尾轴 32B 对齐、切分比过高会编译失败（EV§K6）。shape(3,) 配 (2,8) ⇒ 单块、容量 8 有效 3——边界靠"有效形状"表达，正是第 24 章 Tile 容量/有效二象性的回响（一句桥接，不重讲）。

## 25.3 编译：从 Python 到可执行图（~1.2k 字）

两层各一段，**讲机制不点名清单**：

- Python 前端：AST→IR→规范化→定型，产物可 dump（`TensorGraph/IR/ir_dump_*.txt`，EV§C4）；编译缓存键含源码+选项+闭包+标量实参（EV§C6，一句：换 tiling 会重编的原因）。
- C++ 后端：`PassManager::RunPass("PVC2_OOO")` 串起 40+ pass（EV§D1）；三个阶段哨兵让用户可在 Tensor Graph/Tile Graph/Codegen 后停下的取中间图（EV§D3/C8）；`compile_debug_mode=1` 的四层 json 样例（EV§F6）。**官方四层图语义引 A3（Tensor/Tile/Block/Execute 各一句）**，本章不再自造分层名词。

## 25.4 生成代码解剖：CCE 壳 + TileOp + PTO（~1.2k 字）

- 码生成产物骨架（EV§E2）：`#include "TileOpImpl.h"` + `extern "C" [aicore] void <magic>_<hash>…`；片上地址 `UB_S0_E…=…get_imm(0x…)`（EV§E6）。
- **abs 的落地链（本章最实的三跳，EV§K1-K3）**：`pypto.abs`→`OP_ABS`→`GenUnaryOp`→设备侧 `TAbs`（`tileop/vector/unary.h:400`）→`pto::TABS`——**第 24 章的指令在这里被实例化**。
- PTO 头从哪来（条件版，EV§E4/E5）：tile-tensor 模式下码生成追加 `-I <pto-isa>/include`（env `PTO_TILE_LIB_CODE_PATH` 给**仓库根**，或 CANN 包内）；tileop 头链 `#include "pto/pto-inst.hpp"`。明确写出"该模式关闭时不走此注入"——不写无条件依赖。
- bisheng 双门（EV§E3/J4）：`#ifdef BUILD_WITH_CANN && getenv(ASCEND_HOME_PATH)` 才落 .cpp 并编译——无 CANN 连 cpp 都没有；`CS_CODEGEN_INSTRUCTION` 只出 cpp。

图②（25.3/25.4 合用或单独）：**一段生成 CCE 的分层剖面**——kernel 壳→TileOp 调用（TAbs）→pto 指令，右栏标来源文件；节点写动作。

## 25.5 执行：三条路，别看入口名看开关（~1.2k 字）

以"同一个 `LaunchKernelTorch` 入口、三种设备事实"组织（EV§F1/J1/J2/J3）：

1. **真 NPU**：run_mode=NPU（或 CANN+设备在场自动），C++ 走 `DeviceMemoryUtils`+真设备初始化（EV§J1）；workspace 查询→分配→下发（EV§F3）。
2. **性能仿真（无设备可用）**：`_run_with_cpu`→cost model（`CostModelAgent`，EV§F2）；官方：泳道图核内流水；无 CANN 自动进此路、**仅性能仿真**（EV§F5）。
3. **精度仿真**：依赖 CANN（文档原句）；`accuracy_level=2` 或 cannsim record（950：CostModel/CAModel 两档）——仍经 `LaunchKernelTorch`，但 C++ 按 `CFG_RUN_MODE` 走 Esl/Emulation launcher（EV§J1/J2/J5）。**点题：判设备看 run_mode+是否 cannsim 包装，不看出入口名**（回应任务第 4 点）。
- 收尾一段门控小结表（3 行：run_mode 来源优先级／compile 落 CCE 的门／SIM 两路差异），全部 EV§J 编号。

## 25.6 边界与复现（~0.8k 字）

- 边界四条（EV§G/K，各一句+脚注）：动态 shape 全链自动（IR 定型→码期 `GET_PARAM_*` 宏）；dtype/format 校验范围；输入必须连续 torch 张量；同步/内存由 pass+码生成包办，用户层无手写事件（对比 23/24 章定位，一句）。
- 复现（EV§L 原样收编）：只读核对→`PYTHONPYCACHEPREFIX` 语法检查（已验）→**副本目录**构建（明写"不在只读源仓 build"）→SIM 运行（标注本机未跑）；IR/图 dump 开关两行。
- 延伸一段：tiling/transform 例与官方调试文档入口；0.2.0 变化回指。无性能数字、无未核实特性。

---

## 图规划（2 幅，624px 验收 + textContent 核签；节点=动作，文件/符号入脚注）

| # | 图 | 位置 | 形式 |
|---|----|------|------|
| ① | 四行代码五站旅程（包装→校验→IR→切图/码生成→执行） | 25.1 末 | mermaid LR，纵向分段（前端/后端/运行时三段着色），子图间 `~~~` |
| ② | 生成 CCE 分层剖面（壳→TAbs→pto::TABS，旁注 bisheng 门与 pto include 条件） | 25.4 | mermaid 或 SVG；若 SVG 手绘须 textContent 全核 |

（rev1 的图②六阶段矩阵、图③三图合并/删除；`CompStage` 六阶段只以一句+脚注出现。）

## 篇幅与自查

目标 4.5k–6k 中文字；每节末自检：是否出现目录式列表（>6 行的 pass/阶段枚举→移脚注）、是否引用未实证行为（对照 EV§H3/I3）、图是否 624px 可读。
