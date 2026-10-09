# CH25 补证与提纲收敛
保持模型，仅研究，暂不正文，不改24章，不提交。
经理已读提纲及主例、证据关键链。先修以下矛盾：
1. 用户可读性要求适用本章，不强制8k–12k。单abs主例为主，删除43-pass逐项/七步逐项/六阶段大矩阵/无关标量与内联旁支。优先解释输入→中间表示→切块→生成调用→执行，保留3–5主要机制。图节点写动作，文件/长符号移脚注。
2. F1称SIM完整compile，E6称bisheng/PTO头，而F5称cost_model无需CANN。必须追compile_stage/run_mode实际门控与构建依赖，区分运行时无NPU、无CANN、无bisheng三件事，不能由CPU执行推无工具链依赖。回源记录具体分支，未证明就不保证无需CANN。
3. 亲查GetPtoTileLibPathByEnv原函数，环境变量到底指repo根还是include；错误变量不要在命令里猜。主例是4行代码别反复称9行。单例shape3与tile(2,8)如何对应、尾块如何裁切需追关键IR/算子语义，不凭名称说自动正确。
4. 精度模拟accuracy_level2走LaunchKernelTorch不自动等于真实NPU执行，检查CAMODEL及runtime配置是否拦截；区分入口函数名与执行设备事实。SIM数值/性能能力按文档原义，不笼统说都不提供。
5. 最终复现不得建议在只读源仓运行build_ci --clean。复制到临时工作区或单独构建目录；py_compile输出定向/tmp防止源仓__pycache__写入。补已执行检查日志与源码git status只读核对，不清理源仓。
交付修订证据、精简提纲和CH25-EVIDENCE-CLOSE-RESPONSE，论断给实际摘录。
