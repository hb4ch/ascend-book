---
title: 第18章 实战Ⅴ：Flash Attention
description: FA 教科书精要、ops-transformer flash_attn 真仓解剖（op_api/arch35 kernel）、attention 84 算子族谱、三件套拆分设计
status: 提纲预览
---

# 第18章 实战Ⅴ：Flash Attention

> 本章为提纲预览，正文将随写作推进逐步填充。全书 Ascend C 编的皇冠章——第 9-17 章的所有机制在此合流。目标 ≥5k 中文字。

## 本章来源

- 📦 源码/📄 资料: `ops-transformer/attention/flash_attn/`（op_api 层 + op_kernel/arch35 层）
- 📦 源码/📄 资料: `ops-transformer/attention/{attention_update,attention_worker_combine,attention_worker_scheduler}/`
- 📦 源码/📄 资料: `ops-transformer/attention/{fused_infer_attention_score,sparse_flash_mla,lightning_indexer_v2}/`
- 📦 源码/📄 资料: `ops-transformer/docs/zh/ascend950_op_list.md`

> 完整来源映射见 [附录D 来源映射表](../附录/appD-source-map.md)。

## 1 FA 教科书精要（简述）

<!-- TODO: online softmax / tile 化（公共知识，简述不展开）；为何省 HBM 往返 -->

## 2 flash_attn 真仓解剖：op_api 层

<!-- TODO: aclnn_flash_attn 封装（op_api/flash_attn.cpp、aclnn_flash_attn_inner.cpp）——库算子的 API 层怎么组织，衔接第4章两段式 -->

## 3 flash_attn 真仓解剖：op_kernel/arch35 层

<!-- TODO: Cube/Vec 分块（flash_attn_block_cube_nd.h / block_vec_nd.h）、ND/DN 双布局 kernel（flash_attn_kernel_nd.h / _dn.h）、flash_decode 变体（block_vec_flashdecode.h）、template tiling key——第14章 Tiling 回路 + 第16章 Cube 路径在此合流 -->

## 4 attention 目录 84 算子族谱地图

<!-- TODO: fused_infer_attention_score（推理融合）/ sparse_flash_mla（DSV4 稀疏）/ lightning_indexer（TopK 筛选）/ paged KV cache 系列（gather_pa_kv_cache 等）；时效性纪律（13.1） -->

## 5 三件套拆分设计：attention_update / worker_combine / worker_scheduler

<!-- TODO: 为什么一个注意力拆成三个算子——粒度、复用、调度的权衡 -->

## 6 收官：全书 Ascend C 编闭环

<!-- TODO: FA 里每一个机制的前文出处对照表（Tiling 分形/双流水/RegBase/Cube/图模式）；回指第9章决策树 -->

## 陷阱与注意

（待补充）

## 进一步阅读

（待补充）
