# CH21 源码研究与提纲（暂不正文）

保持当前GLM模型及原会话。停止修改CH20所有文件，经理接管收尾。仅产出management/CH21-EVIDENCE.md、CH21-OUTLINE.md及必要CH21研究报告；不提交不推送不改全局文件。
读PLAN-COMPLETION、ACCEPTANCE、SOURCE-BASELINE与docs/05-comm/ch21-hccl.md。源仓/mnt/SATASSDEXT4/cann只读，hcomm固定1581d1608fd8840bbd46bcbe3f357b1d08460b6a。核对提纲路径，旧目录不存在需记录正确替代。
选3–5主锚点，建立从公开HCCL接口→通信域/资源→算法选路→数据传输→完成与释放的真实调用链。主线选择一个真实集合原语及可定位样例，精确记录输入输出buffer、rank/count/dtype、stream、异步返回与完成条件。说明HCCL和HCOMM名称/接口关系，不把不同层API混为同一个。算法选择必须证到条件，不能以目录名称推断一定执行ring/tree。
分清A2/A3与950等源码真实支持矩阵、Host/AICPU/AICore执行路径；PCIe/HCCS/RDMA/RoCE物理层与协议关系仅按来源陈述。核查init/destroy顺序、跨rank一致性、notify/wait以及buffer生命周期，不能从单向通知推断完整释放。
自定义P2P和高精度ReduceScatter是否真实可支持教学主线：给完整源路径、符号及引用行区，不能先接受旧提纲承诺。与CH22单边HIXL、CH23通算融合分工明确。本轮不跑多卡/不编造性能或真机验证。
提纲按读者问题链，目标核心章8k–12k中文。证据区分直接代码/源文声明/推导/未证，记录每项适用边界。给可复现样例的完整编译执行条件及命令来源；无硬件只列所需环境。不写正文，完成等待经理。
