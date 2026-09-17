---
title: 第一编 · 昇腾平台全景
description: 从芯片家族到软件栈主链路
---

# 第一编 昇腾平台全景

对应全书目标 1（建立全局认知）。本编回答三个问题：**平台上有什么**（芯片与软件栈）、**硬件长什么样**（AI Core 与内存/互连拓扑）、**一次算子调用如何穿越整个软件栈**（执行主链路）。

- [第1章 昇腾平台与生态总览](../01-platform/ch01-overview.md)（M0 已试写，作为全书样章）
- [第2章 昇腾硬件体系结构](../01-platform/ch02-hardware.md)（A2/A3/A5，AI Core 组成，HBM→L1→UB→reg，互连与超节点）
- [第3章 软件栈执行主链路](../01-platform/ch03-exec-path.md)（torch_npu/aclnn → ACL → runtime → queue_schedule → TSD → 驱动 → AI Core）

**主要来源**：`asc-devkit`、`runtime`、`pto-isa`、`cann-learning-hub`（详见各章「本章来源」与附录D 来源映射表）。
