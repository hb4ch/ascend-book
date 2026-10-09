保持原GLM模型与会话，不重启不提交。第22章由经理验收收口，不再修改。
下一任务：为docs/05-comm/ch23-supernode.md研究源码并交CH23-EVIDENCE.md/CH23-OUTLINE.md，暂不写正文。遵循SOURCE-BASELINE只读源仓。
主线从ops-transformer/mc2选一个真实GEMM+AllReduce或AllGather+Matmul算子，追Host API/注册→Tiling→核函数→通信启动/计算/Wait/Finalize→输出。区分A2/A3/950实现，不因目录名推支持。结合asc-devkit MC2指导与第21章已审契约，明确buffer就绪/复用和跨核同步；融合不等于消除GM中转。MoE另选有源码的dispatch/combine或AlltoAll实例，不能用宣传图代替完成语义。
SuperPod/PD/RL按本仓实有文档证据限定，仓外依赖明确，不虚造端到端案例。PTO gemm_ar可作为独立对照，不能把不同后端拼成同一调用链。性能数字需平台、shape/dtype、方向、单位及来源；无NPU不声称运行。提供可核真实构建运行命令与依赖缺口、3–5主锚及完整文件路径、论断/证据/未知项账本。先研究候审，遇证据断点写清，不猜补桥。
