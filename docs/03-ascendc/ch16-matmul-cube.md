---
title: 第16章 实战Ⅲ：矩阵算子——MatMul Cube 全路径
description: MatMul 教程展开、NZ 分形、双缓冲流水重叠、L0C 驻留、Fixpipe、bank_conflict_nd2nz 单参数调优
status: 提纲预览
---

# 第16章 实战Ⅲ：矩阵算子——MatMul Cube 全路径

> 本章为提纲预览，正文将随写作推进逐步填充。已迁移第 14 章 v1 版的相关初稿，成稿时扩写至 ≥4k 中文字。

## 本章来源

- 📦 源码/📄 资料: `cann-learning-hub/tutorials/ascendc_operator_development/04_matmul_basic/`
- 📦 源码/📄 资料: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_basic_api_high_performance/`
- 📦 源码/📄 资料: `asc-devkit/examples/01_simd_cpp_api/05_best_practices/04_memory_access/`
- 📦 源码/📄 资料: `ops-nn/matmul/`

> 完整来源映射见 [附录D 来源映射表](../附录/appD-source-map.md)。

## 1 MatMul 数据流实战：GM→L1→L0A/B→Cube→L0C→UB/GM

<!-- TODO: 第8章图8-1 的实战版，每跳对应 API -->

## 2 NZ 分形与双缓冲流水重叠

<!-- TODO: A/B 按 NZ 驻 L1（第8章8.3）；搬运与 Cube 计算的流水重叠 -->

## 3 搬运收口：data_copy 与 bank_conflict 三例【还债②】

<!-- TODO: 初稿迁移——
- data_copy：GM→UB、GM→L1 搬运行为观察台——分块粒度、非对齐搬运（DataCopy vs DataCopyPad，第8章 32B 对齐纪律的代价实测）、L2Cache 复用、同地址访问冲突规避。第10章 N-DMA 的「自由配置维度与 stride」在这里变成可量化性能对比。
- bank_conflict_ub：UB 读写 bank 冲突的产生与规避。
- bank_conflict_3510：950 新 UB 结构（8 组 × 16KB）下的冲突新形态（第8章伏笔兑现）。
- bank_conflict_nd2nz：8192×8192 half ND→紧凑 NZ 转换，整个调优只动 dstNzC0Stride 一个参数（case 1→2）。
- 心法：满载、对齐、不撞 bank；做不到就改切分。
-->

## 4 L0C 驻留与 Fixpipe 随路

<!-- TODO: L0C 复用（950 L0C→UB 直通，第11章11.6）；Fixpipe NZ2DN -->

## 5 ops-nn 的 matmul 算子对照

<!-- TODO: ops-nn/matmul 真仓实现对照（quant_batch_matmul_v4 等的 Cube 侧组织） -->

## 陷阱与注意

（待补充）

## 进一步阅读

（待补充）
