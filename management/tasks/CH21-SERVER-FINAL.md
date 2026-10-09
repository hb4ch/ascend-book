# CH21 服务端实现最终补证
保持模型，仅CH21，不提交。R2“实现定义未找到”不能作为缺仓结论，经理rg已找到全部路径。
读取asc-devkit/impl/adv_api/detail/hccl/impl/hccl_impl_def.h、hccl_impl.h、common/hccl_base.h、common/hccl_aicpu_def.h、common/hccl_aicpu_impl.h、impl/platform_v310/hccl_ccu_v0_def.h、hccl_ccu_v0.h与ccu/hccl_ccu_v0_prepare.h。头文件引用链开始，说明__NPU_ARCH__3510包含什么特化，CCU=5模板如何落入实际实现；AICPU在3510下是否拒绝/何种分支，仅按实际代码。源码基线不变，不运行。
重点追AllReduce->InitV2/SetCcTilingV2->Commit/Wait/Finalize实际分支，分别A2/A3与950。不要求扩写算法内核，但不能把实际可查的实现写不存在。头注OnlyAICPU与实际CCU特化冲突应标头注过窄，而非自创API形态解释。为21.6写准确平台限定和例子，补完整文件脚注。
检查当前SVG：中间框长行明显越框、三范围共同汇入暗示已证且legacy框纳入CCU新路径。分行缩短并区分legacy选路与标准数据面；不以像素四色检查代替可读性。完成交付CH21-SERVER-RESPONSE、更新正文/证据/图，运行verify，待经理。
