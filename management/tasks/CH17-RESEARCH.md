# 第17章源码研究（与经理收尾第16章并行）

第16章R1已收到，项目经理接管其正文/图/报告收尾；你从现在起不要再修改任何ch16相关文件和appD。
保持GLM-5.3-Flash。请读取PLAN-COMPLETION、ACCEPTANCE、ch17草稿，研究第17章融合：matmul_gelu_high_performance、quant_group_matmul_high_performance、ops-nn/vfusion。
只交付 management/CH17-EVIDENCE.md 和 management/CH17-OUTLINE.md；暂不写正文、不提交推送。证据给真实文件、符号/行号、架构/限制，提纲要读者可复演，不能只做API列表。
重点：Scenario1 GM中转不等于零拷贝，Scenario2 L0C→UB须按支持架构区分；Cube/Vector逻辑分工、__mix__、核间通知、缓冲复用的完整生命周期；量化尺度和数据类型；融合失败/收益边界；所有性能数字统一基线/shape/dtype/版本，不能把占比当峰值率。源码无保证的地方如实注明，不从sample名字推导硬件。
读代码而不只读README；遇README与代码不一致记录差异。完成后等待经理，不询问用户。
