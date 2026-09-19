---
title: 第15章 实战Ⅱ：向量算子——Softmax 与 GELU
description: softmax Case 0-5 六级优化阶梯逐级细讲、VF 融合/循环优化/指令双发、UpdateMask 与主尾块、连续非对齐
status: 提纲预览
---

# 第15章 实战Ⅱ：向量算子——Softmax 与 GELU

> 本章为提纲预览，正文将随写作推进逐步填充。已迁移第 14 章 v1 版的相关初稿，成稿时扩写至 ≥4k 中文字。

## 本章来源

- 📦 源码/📄 资料: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/02_reg_compute/softmax_high_performance/`
- 📦 源码/📄 资料: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/02_reg_compute/gelu_high_performance/`
- 📦 源码/📄 资料: `asc-devkit/docs/zh/guide/operator_practice/simd_operator_optimization/vector_compute/vf_optimization/{vf_fusion_optimization.md,vf_loop_optimization.md,dual_issue_optimization.md}`

> 完整来源映射见 [附录D 来源映射表](../附录/appD-source-map.md)。

## 1 Softmax 六级优化阶梯（Case 0-5 逐级细讲）【还债①】

<!-- TODO: 成稿时按下列初稿扩写，真码行级 diff -->

**已核实材料**（softmax_high_performance/README.md，仅 950，CANN ≥9.1.0）：
- Case 0 → 1：MemBase → RegBase API（寄存器级计算）
- Case 1 → 2：循环融合 + ExpSub 融合指令 + UpdateMask 尾块处理
- Case 2 → 3：外层循环展开（UpdateMask 模式）
- Case 2 → 4：主尾块模式（main-tail block）
- Case 4 → 5：主尾块 + 外层循环展开 + ExpSub 全家桶
- 六版本同文件 `softmax.asc` 并排，diff 式学习；前置阅读：Reg 矢量计算编程、指令双发、VF 融合、VF 循环四篇

## 2 GELU：连续非对齐与指令双发

<!-- TODO: gelu_high_performance（高ium性能版与 eltwise 版）；dual_issue_optimization 落地 -->

## 3 VF 优化三法总结

<!-- TODO: 融合 / 循环优化 / 双发的适用面与组合；对照第11章 11.5 RegBase 原理 -->

## 4 搬运协同（供第16章引出的伏笔）

<!-- TODO: 向量算子的搬运瓶颈从何而来，引出第16章 -->

## 陷阱与注意

（待补充）

## 进一步阅读

（待补充）
