# CH27 正文任务：从库调用到稀疏注意力与核验
保持现有模型/会话，源仓完全只读（包括缓存和清理），依赖不装用户环境；不提交，不改26章。先修订研究内部矛盾，再写docs/06-backend/ch27-case.md。
经理已独立核查kernel ComputeMm1/Mm2、ProcessBalance及ProcessBalance inner阶段：syncC1V1生产、syncV1C2消费、syncC2V2与syncC2V1产生可证；L874 AIC等待syncV0C1，L879 AIV等待flag3、MergeKv后Set syncV0C1，L889–895 Mm2后AIC Set flag3。这是一对“数据就绪/可复用”的真实例子。写作重点解释该对，不把全部flag号堆给读者，不称全内存安全已证明。
主线：读者用一个库算子需要提供什么→两段API为何先计划再执行→稀疏索引如何进入一次QK/softmax/PV→输出怎样核验。去掉“可选”、全部提纲占位。开头不写候选评审历史。主例A是未运行C++TND样例，CPU参考B是不同shape/scale的数学复算，必须明确区分；样例实际没有读回或对拍。
固定分支用arch22编译条件，不未经证实映射产品。op_api Inner实现/运行时选bin断点如实标明，禁止直接把OpDef、infershape、tiling串成逐步调用。README产品支持表另述，不等于本书分支运行验证。参数表按张量分类dtype，scale值保留，不套1/sqrt512（该例含rope）。
2–3幅短图或图表：库调用生命周期、一个稀疏块经过核间阶段和就绪/释放、CPU与NPU核验区别。图解释数据或控制流，不能只有项目名字。主例索引为0..2047，数学上选择全量，需明确“稀疏接口不代表此输入真的稀疏”；CPU B才有子集。避免重复18章推导。
CPU脚本现2e-3阈值和2.48e-4差异仅所选输入；-1终止/越界/空选集未覆盖。不把golden独立复算当NPU或example正确性；golden覆写索引和v取key的语义解释清楚。源树写入违规仅管理记录留痕，不把它编成读者教程。修EVIDENCE H3与H0冲突、OUTLINE还残留“正确性来自CPU”句。
图表之外写连贯短段，源码全路径和行号放脚注，不写审稿术语堆砌。不强制字数，足够解释案例。DSA复杂度只限子集attention，索引/选择开销另计；不写无数据性能收益。
交付正文、CH27-REPORT.md、证据修订，npm run verify日志，CPU脚本最终日志；图在真实站点正文宽度渲染，无法目检如实说明，经理会检查。完成候审。
