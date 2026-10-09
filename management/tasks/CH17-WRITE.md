# 第17章正文任务

研究交付后直接执行本任务，不等待用户确认。保持当前GLM-5.3-Flash模型，不重启。先读CH17-EVIDENCE、CH17-OUTLINE、reviews/CH17-PRECHECK、ACCEPTANCE及STYLEGUIDE。

## 先修证据，再写正文

经理实查发现：ops-nn/vfusion共8个目录项，其中一个是CMakeLists.txt，实际7个算子目录；名称是multi_scale_deformable_attn_function、scaled_masked_softmax_grad_v2等，按真实名字，不用臆造花括号。证据表要修。
quant文件610–685行已有完整host实参：M=N8192,K1024,BASE_N256,BASE_K128,SINGLE_N1024；2201 SINGLE_M=BASE_M128,24核；3510 SINGLE_M=BASE_M256,32核；workspace=depth*BASE_N*BASE_M*4*CORE_NUM。补闭U3。自行核实GetTaskRation契约和FasterGelu，必要时把API约束与样例值分开。
反向flag3在PIPE_MTE2上发出，只保证此前该流水读取workspace完成，不等于Vector或最终输出完成。证据与正文都必须明确。不要把未证实的UB复用保护写成确定安全，也不要猜测自然错位会保证安全。CrossCore mode/pipe的有效范围逐平台引用，勿泛写所有架构一致。

## 正文范围

交付docs/03-ascendc/ch17-fusion.md、必要的ch17专属图、附录D对应ch17映射、management/CH17-REPORT.md以及validation/ch17-verify.log。不得修改ch16、README、全局计划或提交推送；经理处理全局进度。
正文目标8k–12k中文，最低4k不等于完成；围绕机制和可复演推导，不堆API和重复第16章。status写待审。清除现有提纲和错误假设（如所有平台零拷贝、反量化随路进矩阵乘）。

必须讲清：
1. 融合的收益条件、launch/中间流量/重叠三种收益，GM中转和UB直通按架构分别说明。
2. matmul_gelu的Cube/Vector分工、固定tile走查、双AIV切分与尾块限制，单向就绪通知和未证实的复用条件。
3. quant的int8×int8→int32→两种scale→FasterGelu→half完整公式、分组M调度和跨group余数，实际固定参数；不要称为Fixpipe随路反量化。
4. GM环形workspace生命周期：depth1/4与UB队列BUFFER_NUM2区别，地址算例、产生/通知/读取/回执/复用、两AIV回执配对与最终排空。给准确图示。
5. 同架构同shape性能对比；最低支持版本不是测量版本，README未给出的测量环境如实记录未知。Task Duration、单流水时间、ratio和理论峰值不混。不得从独立kernel数字相加声称实测端到端加速。
6. 两个样例的实际构建与数据/校验命令：逐个读CMakeLists和scripts，禁止臆造脚本或CLI参数。无NPU明确未执行。短代码标示意，完整命令标需真机验证。
7. 生产库导览只选真实算子路径和能证明的事实；融合不适用条件、数值误差与读者实验。

所有核心断言给文件级标准脚注，来源固定SOURCE-BASELINE。自审脚注使用/定义、图与代码同步、性能单位和真实源参数，运行npm run verify并保存日志。完成报告列实际检查、未验证事项、残余问题，不自称经理验收。完成后留在原会话等待经理评审。

## 提纲交付后的经理修正（优先于提纲）

- 删掉「本样例未显现错覆」：我们没运行，不能声称观察不到错误。只能说源码未显式给出反向保护证据。
- GM接口与L2缓存不是两条独立编程通路；按GM中转（可能利用L2，README这样解释观测）和UB直通两条路径组织。不能保证所有读取总命中L2。
- 提纲17.6的「F322F16随路 vs Cast」无源证据且和fp32输出冲突，删除，回源核对Fixpipe字段后再讲实际类型转换。
- 不要将Task≈max(各流水活动时间)当作一般等式；仅理想重叠模型，实际受依赖/填充排空/搬运影响。不能仅凭vec<mac宣告不存在Vector瓶颈，明确是README对应样例分析。
- 提纲GetTensorC调用参数错了：代码是mmOutGlobal[workSpaceOffset], 0, true，不是把workspace偏移作为第二参数。原码引用须逐字符核对。
- FasterGelu API文档为 docs/zh/api/SIMD-API/adv_api/activation_functions/Gelu_interface/FasterGelu.md，明确sharedTmpBuffer不能与当前src/dst重叠。样例复用此前已消费的dequant/pertoken区域，与当前mulsResult/actResult不同，解释这个区别。
- 图示使用实际depth1/4，避免另造depth2/3增加读者对照负担。
