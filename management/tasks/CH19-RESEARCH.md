# 第19章性能分析研究

CH18条件报告已收到，经理选带有效mask、fp16/float/half、128/128/D256的Nd+GM条件案例并接管全部CH18正文图和appD收尾。你停止修改CH18相关交付。
保持GLM-5.3-Flash，不重启，不提交推送。读取PLAN-COMPLETION、ACCEPTANCE及ch19提纲，以固定源基线研究真实性能采集和瓶颈分析链。
交付management/CH19-EVIDENCE.md、CH19-OUTLINE.md，暂不写正文。先找真实文件再选锚点：runtime profiling上报/时间戳/字段、asc-devkit调优文档与真实样例性能表、pto相关优化文档。区别msprof/msprof op/msopprof命令及工具安装范围，必须有本地文档证据，不臆造CLI。
重点：Task Duration/核耗时/各流水活动时间/ratio/频率/带宽/峰值的分母与单位；重叠不代表各列可相加；采集扰动、warmup、重复、中位数、时钟频率、相同shape/dtype/版本；时间线事件与算子定位；多核负载和扩展性。选一个已核实样例走完“观测→候选解释→需补证→实验变量”，不将相关性当因果。无NPU只设计复现步骤，不能报实测；可对仓内数字做明确的离线计算并留日志。不重复ch16–18正文。
证据逐文件/符号/短摘录，记录未知项，完成后等经理。
