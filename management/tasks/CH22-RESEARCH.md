# CH22 HIXL 研究与提纲
保持当前GLM模型和原会话，不提交。停止修改CH21，经理接管收尾。只写management/CH22-EVIDENCE.md、CH22-OUTLINE.md及必要CH22研究报告，暂不写正文。
先读PLAN-COMPLETION、ACCEPTANCE、SOURCE-BASELINE、docs/05-comm/ch22-hixl.md。源仓只读，hixl固定9ed283b27309463ed0faa490b79c0dc9ddef6377。
选择一个真实C++或Python样例从Init、内存注册、交换元信息/建链、传输、完成查询或等待、断链/注销/销毁跟完整源码。记录每个API真实签名、方向（调用端/源端/目的端）、内存类型、注册前提、返回与完成/可复用语义；单边不是无需对端准备，零拷贝不是从无中转。
区分D2D/D2H/H2D、直传/中转/FabricMem路径，按平台与协议条件实际分支，不从文件名推可用性；异步超时和失败后的资源释放/重试必须依据实际实现。HIXL与HCOMM SymWin分开讲，LLM-DataDist/KVCache若属另层或仓外必须注明，别串API版本。
证据3–5主锚点+完整repo/path符号行区，区分代码事实/源文/推导/未证。列现存benchmark口径及条件，无硬件不编造数据或运行。目标核心章8k–12k提纲，以真实数据流与生命周期为主，性能范围明确。复现命令核README/CMake/脚本，源仓副本工作目录和环境配置齐全；本轮不运行硬件、不下载。交付研究后等待经理。
