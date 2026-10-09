# 第17章经理预查

2026-10-09。供研究及正文使用，源仓只读。

1. `matmul_gelu_high_performance/mmad_gelu.asc`可见AIC在CopyOutAic后发mode2 flag0x8，AIV等待；未见相对方向的CrossCore回执。不得写“mode2天然具备释放回执”或据此断言源码已证明通用无竞态。应核查其他编译/运行保证，无法证实时明示样例边界。
2. CrossCoreSetFlag_ISASI.md第31–40行及key_features.md模式2：是按flagId的通知计数；AIC通知后各AIV分别Wait消费；反向则需所有AIV发Set，AIC再Wait。两种方向分别编码，不隐含另一方向。950 Wait模板参数生效，旧架构模板mode/pipe不生效、阻塞范围不同，引用需按平台。
3. `quant_group_matmul_custom.asc`第320–329行：cubeTaskIdx>=PIPELINE_DEPTH时等待SYNC_AIV_TO_AIC=3，再写循环workspace slot并通知5；slot地址含(coreIdx + taskIdx%depth*CORE_NUM)。第372–396行：AIV等待5，加载workspace到UB、调度计算输出后，在PIPE_MTE2上发回执3。**回执的流水完成条件是MTE2对共享workspace的读取完成，不是Vector计算/最终GM输出完成**。第404–418行PostCompute排空剩余min(tasks,depth)个回执。
4. BUFFER_NUM=2是UB队列缓冲数，PIPELINE_DEPTH=1/4是GM workspace环形槽数，不能混称同一双缓冲。Scenario0/1/2分别1AIV深1、2AIV深1、2AIV深4。
5. 量化README同时声明A2/A3>=9.0.0、950PR/DT>=9.1.0，这是最低运行要求；不能当作性能测量版本。性能表仅明确A2和950PR，不能把950PR实测扩大到950DT。
6. 量化Task：A2 583.512/353.887/299.286us；950PR 282.717/224.125/204.129us。比较倍数须同架构同shape同dtype，不把aic_mac_ratio当峰值实现率。Scenario1到2时A2 vector time几乎不变但Task变短，适合解释重叠收益与单单元加速的区别。
