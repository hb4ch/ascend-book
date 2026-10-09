# CH24 正文与图表
补证已读，经理亲核CPU TLOAD及a2a3 CheckStaticMad，进入正文。保持模型，仅24章正文/本章图和证据报告；不提交。23章经理独占。
按修订提纲，以gemm_demo一个tile旅程为主例，先输入/实际指令/结果，再解释容量、有效区、GM与块布局、事件与CPU-SIM边界。3幅图须正文宽度可读，实际渲染。不要硬凑字数、目录字典或引入无关复杂变体。源码片段真实注明省略。
写前同步修正补证余项：I2 dtype三元组顺序混乱，统一(A,B,C)，则i8,i8,i32 / half,half,float / float,float,float / bf16,bf16,float。I3不要从TileLeft推TLOAD布局改变：主例TLOAD目的aMat显式固定ColMajor，TileLeft差异出现在TMOV目的aTile；分清两次搬运。图②“16×8×512B”错误，16×8个float合512B，共4块2048B。图用aMat真实配置，别混aTile平台别名。valid假设须与模板静态valid/动态valid相容；若另造动态例须写明非主例。
浮点CPU对拍通过不是NPU数值精度/时序证明。NPU float路径若转换精度须按源文限定，不保证与CPU一致。不要引用CPU perf行作设备性能。复算脚本保留可复现文件，不只有输出。
交付正文docs/06-backend/ch24-pto-isa.md、3图、更新证据、CH24-REPORT.md、verify日志、命令bash-n、图截图。最终读取实际文件逐项自查，报告不得声称未完成的修改。
