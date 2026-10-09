# 第18章源码研究

经理接管第17章正文、图、附录D及报告收尾；从现在停止修改这些文件。保持现有GLM-5.3-Flash，不重启、不提交推送。
读取PLAN-COMPLETION、ACCEPTANCE、第18章提纲及SOURCE-BASELINE。研究本地CANN快照中的Flash Attention实际实现，先发现真实路径再选择3–5主锚点。交付management/CH18-EVIDENCE.md及CH18-OUTLINE.md，不写正文。证据必须具体到文件/符号与适用平台，区分源码事实、文档说明和推导。
重点：QK与PV两次矩阵乘、online softmax的m/l及输出重缩放递推、mask和尾块、布局dtype/累加精度、Tiling、Cube/Vector交接与完整缓冲生命周期、跨核同步、流水排空；训练/推理、prefill/decode及不同产品不能混用。所有性能数字给相同shape/dtype/架构/口径及来源；无NPU不得称真机实测。核对真实构建与测试入口。不要只抄README或逐API罗列。提出读者可复演的一个固定shape逐块走查以及未证条件。完成后等经理评审。
