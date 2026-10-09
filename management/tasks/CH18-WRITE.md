# 第18章正文撰写

研究与TRACE已收到。保持原模型，不重启。先读ACCEPTANCE、STYLEGUIDE、CH18证据/提纲/TRACE，再边核查边写。目标8k–12k中文、最低5k；不以字数代替机制正确。
交付ch18正文、ch18专属图、CH18-REPORT及validation/ch18-verify.log。不要修改CH17、appD、README、全局计划，不提交推送。status待审。
主线限定arch35非量化训练Nd，数学小例与真实kernel结构走查分别标识。详讲QK→online softmax→PV→累计/末块归一化、dtype/布局、mask和尾块、四级流水、buffer生产消费就绪释放及排空；arch22仅依据实查作有限对照，不混入fp8/Nz或推理特化。没有可靠性能表就给采集方法，不凑数字。
必须先在写相关段落前核清：
- TRACE说末块先FlashUpdateLastNew再LastDivNew，实际是否互斥分支？逐分支回源，不能将代码省略拼成无条件连续调用。输出cast查Bmm2DataCopyOut内部，此处不准再声称非主线而略过。
- TRACE中L1安全“由1:16保证”、三环“领先2级保证”尚属猜测。若没有代码证明，写清已见同步及未证复用机制，不能将设计约定当证明。不要依赖耗时关系推导正确性。
- 经理核查buffer.h 355–425：UB/GM（非BACKWARD）即使标FORWARD也有双向Wait/Set；L1的反向才受BOTH条件控制。按实际分支及调用解释，不按枚举名字猜语义；两AIV使用id与id+AIV0_AIV1_OFFSET两个通知，不是同id等两次。
- 固定shape的自动Tiling选择未证，采用明确“假设已选模板参数”的结构走查即可，不同时声称2048²必落128。不要把s2先行分支未识别包装成已证。
- 训练主线max/sum是float，不能再从Nz/fp8搬half结论。
完整源码脚注；删节代码标示意，不臆造API。数学对拍只证数学递推；不代表CANN kernel或NPU验证。给真实API/构建入口和前提，无NPU明确未运行。图表需真实buffer/pipe/架构，渲染检查。完成跑verify与脚注核对，报告未证边界，等待经理。
