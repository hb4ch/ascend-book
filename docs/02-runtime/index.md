---
title: 第二编 · 运行时、驱动与维测底层
description: ACL API、runtime 核心实现、驱动边界、DFX、内存与数据通路
---

# 第二编 运行时、驱动与维测底层

对应全书目标 3（深入底层）。本编逐层翻开 `runtime` 仓：先给编程接口（ACL），再剖内部实现（模块划分、任务构建、队列调度、TSD 通信），而后界定用户态驱动与内核驱动的边界，最后落到维测（DFX）与内存/数据通路——后两者为算子性能编打基础。

- [第4章 ACL 编程接口](./ch04-acl.md)
- [第5章 运行时核心实现](./ch05-runtime-impl.md)
- [第6章 驱动与系统软件协同](./ch06-driver.md)
- [第7章 维测子系统 DFX](./ch07-dfx.md)
- [第8章 内存与数据通路](./ch08-memory.md)

**主要来源**：`runtime`（`src/runtime`、`src/queue_schedule`、`src/tsd`、`src/aicpu_sched`、`src/cmodel_driver`、`include/external/acl`、`example/`、`docs/zh`）。内核驱动源码不在开源仓范围，第6章按「分层+边界+API」级写作并明示。
