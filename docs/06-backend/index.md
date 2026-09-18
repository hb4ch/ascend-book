---
title: 第六编 · 现代编译后端与编程范式
description: PTO 虚拟 ISA、PyPTO 框架、生态与前沿、全栈案例
---

# 第六编 现代编译后端与编程范式

![第六编扉页插图：高级语言光雾经编译管道逐级收窄为规整指令网格落入芯片（part divider art: language mist funneled into an orderly instruction grid）](../figures/art/part6-backend.png)

*第六编 现代编译后端与编程范式 · 编扉页配图（AI 生成概念插图，非技术图）*

对应全书目标 4。昇腾近年最重要的开源动作之一是把「编译后端」开放出来：`pto-isa` 定义了跨代际的虚拟 ISA，`pypto` 在其上构建了 Python 编译前端。本编带读者读懂这两层，再回到生态（PyAsc/tilelang/torchair/npugraph_ex）做横向比较。

- [第20章 PTO 虚拟 ISA](./ch20-pto-isa.md)
- [第21章 PyPTO 框架深入](./ch21-pypto.md)
- [第22章 生态与前沿编译技术](./ch22-ecosystem.md)
- [第23章 全栈综合案例（可选）](./ch23-case.md)

**主要来源**：`pto-isa`、`pypto`、`cann-learning-hub/blogs/*`。第20/21章以 pto-isa CPU-Simulator 实际跑通 demo 佐证。
