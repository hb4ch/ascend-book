# CH22 正文任务
保持模型，停止任何CH21修改。仅docs/05-comm/ch22-hixl.md、专属图、CH22研究/报告/验证。不提交。按补证主线写8k–12k中文。
经理亲读hixl_engine.cc L383-433发现关键漏项，先订正账本再写：AutoConnect在!auto_connect_时只GetClient不重建；AutoDisconnect只在auto_connect_为true才Disconnect。不能写“失败后直接重试Transfer即可”！分自动/显式建链两种，自动断链还可能失败。对象复位不等于传输可安全重放，timeout可能部分写、源数据/远端注册需稳定，重试决策需应用确认，不能承诺幂等或完成。
正文以quickstart双进程/READ主线、完整双端生命周期为中心。严格保留done先于Disconnect与Server收尾窗口，不能替源样例假称无竞态；可提出应用额外握手的改进建议但标本书设计未执行。复现复制源仓临时副本，命令必须真正运行quickstart两角色，不用d2rd冒名；给环境/设备/目录、无真机未执行。
异步三层状态表：Status返回码≠TransferStatus输出，WAITING保留、终态消费、批量过滤/失败元素，使用者如何保存req/result。限定CS DIRECT路径，不推广UB/legacy。Host_flag=同stream D2H常量1，核内notify的二进制缺口明确标出；sync只有SUCCESS才完成。
协议与引擎选路分两层，候选优先级不等于选中。FabricMem/BUFFER_POOL/LLM-DataDist互相边界和版本条件明示；文档性能列完整shape/块/方向/引擎/单位/源版本，测量CANN未知即注明，不能挑极值当保证。无硬件不写实测。
代码[示意代码]或[需真机验证]，完整文件级repo/path脚注，不用前缀加略写。正文不用内部C/D编号、U号、管理文件依赖或返修历史。图表达真实双端/分支，不靠长文字盒代替调用流。完成CH22-REPORT覆盖与限制、verify/bashn实际日志，等待经理。
