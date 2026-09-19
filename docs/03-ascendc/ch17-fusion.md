---
title: 第17章 实战Ⅳ：融合算子
description: Cube-Vector 融合（matmul_gelu）、随路量化（quant_group_matmul）、融合决策面与 UB 交接面设计
status: 提纲预览
---

# 第17章 实战Ⅳ：融合算子

> 本章为提纲预览，正文将随写作推进逐步填充。已迁移第 14 章 v1 版的相关初稿（含图 14-3 草稿），成稿时扩写至 ≥4k 中文字。

## 本章来源

- 📦 源码/📄 资料: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/03_fusion_compute/matmul_gelu_high_performance/`
- 📦 源码/📄 资料: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/03_fusion_compute/quant_group_matmul_high_performance/`
- 📦 源码/📄 资料: `ops-nn/vfusion/`

> 完整来源映射见 [附录D 来源映射表](../附录/appD-source-map.md)。

## 1 CV 融合标准姿势：matmul_gelu

<!-- TODO: 初稿迁移——AIC 完成 Matmul 后经 Fixpipe 输出到 GM 或 UB，AIV 从 UB/GM 读入做 GELU；第8章「零拷贝」动机的算子级实现：中间结果不出 AI Core，省一次 GM 往返。支持 A2/A3/950。 -->

## 2 随路量化：quant_group_matmul

<!-- TODO: 反量化随路进矩阵乘；第13章 quant 矩阵的融合视角 -->

## 3 融合决策面

<!-- TODO: 图 14-3 mermaid 草稿迁移——
两段计算、第二段逐元素？→ 否：两级 kernel + 图模式；是：第二段吃得下第一段分块节奏？→ 能：CV 融合（Fixpipe 出 UB→AIV 接力）；不能（全局规约）：退回两级+图模式；还有随路机会（量化/格式转换）：Fixpipe NZ2DN（第11章11.6）。
融合的本质：让两段计算共享同一块 AI Core 的 UB 交接面。 -->

## 4 ops-nn/vfusion 域导览

<!-- TODO: 库侧融合算子族 -->

## 陷阱与注意

（待补充）

## 进一步阅读

（待补充）
