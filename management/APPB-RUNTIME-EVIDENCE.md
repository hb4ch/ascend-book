# APPB-RUNTIME-EVIDENCE —— 运行时术语第二批回源

2026-10-10。任务：APPB-R1 第 6 条（继续回源余下术语，分组可核验）。基线 SOURCE-BASELINE（runtime `681ef76`/2026-08-22）。本文件只收**运行时族**；每条：术语→源证（完整路径:符号）→术语表处理建议→剩余不确定。**未回源不下结论。**

## 1. SQE（任务描述符）——已闭合（rev3 R3-1 摘要＋补充）

- 结构族（按架构）：`runtime/src/runtime/core/inc/sqe/v200_base/stars_david.hpp`（`RtDavidStarsAicAivKernelSqe` L148、`RtDavidStarsAicpuKernelSqe` 见 `aicpu_sqe.h` L114、Notify L231/FunctionCall L209/HostfuncCallback L98）；`.../sqe/arch5162/stars_sqe.hpp`（`RtStarsAicAivKernelSqe` L106、`RtFftsPlusKernelSqe` L357）；公共助手 `runtime/src/runtime/inc/sqe/aic_aiv_sqe_common.hpp`（`ConfigSqeDieFriendly` L22、`ConstructAivSqePart` L85）。
- 填充链：`core/src/task/task_info/davinci/davinci_kernel_task_v201.cc` L27-36（AICPU SQE type 常量 `RT_DAVID_SQE_TYPE_AICPU_D`）、L45-50（`UpdateDavidAICoreSqeForDavinciTask`：aivSimtDcuSmSize=RT_SIMT_STL_UB_SIZE）、L70+（模板显式实例化）；`davinci_kernel_task_v200_base.cc` L283/307/320。
- 下发链：`tprt/inc/external/tprt_type.h` `TprtTaskSendInfo_t{sqeAddr,sqId,sqeNum}`→SQ；aclgraph 重建例 `feature/aclgraph/capture_model.cc` L589-608（`RebuildAllExternalTaskSqes`）。
- **术语表**：已按此改（首批 R1 轮）。剩余：arch5162 与 v200 差异、CQ 回报路径未追（不写）。

## 2. TSD——职责实证（设备子进程编排）

- `runtime/src/tsd/tsdclient/inc/tsd_event_interface.h` L26-38 `TsdSubProcessType`：PROCESS_HCCP/COMPUTE(aicpu_schedule)/CUSTOM_COMPUTE(aicpu_cust_schedule)/QUEUE_SCHEDULE/UDF/NN/PROXY/BUILTIN_UDF/ADPROF——**TSD 编排的设备子进程清单（枚举注释原文）**。
- `tsd_process_controller.h/.cc`：`Open(rankSize)`/`OpenAicpuSd()`；日志「start hccp and computer process success」「skip to start aicpu-sd process」（L48/125）——子进程启停编排。
- `common/basic_define.h` L17 `HDCServiceType{FRAMEWORK,TDT,TSD}`——host↔设备 HDC 通道上的服务身份。
- **术语表**：已改「设备侧服务子系统：经 HDC 通信、编排设备子进程（含 aicpu/queue_schedule）」；**「任务调度器」旧概括不恢复**。剩余：TSD 与 TDT 分工、设备内侧实现未读。

## 3. Stream/Task

- Stream 接口族：`runtime/docs/zh/api_ref/06_stream_management.md`（与 07/08/09 同目录序列；创建/销毁/同步/WaitEvent 组合）。
- Task 构建链实体：`core/src/task/task_info/`（davinci v200/v201 KernelTask→SQE 装配，见 §1）；task 抽象与调度队列衔接经 tprt SQ。
- **术语表建议**（待批）：Stream=host 侧任务执行序列抽象，经 runtime→tprt 映射到设备 SQ；Task=一次可调度执行单元，构建期装配为 SQE。**本轮不改**（Stream→SQ 绑定未逐行，留第二批收尾）。

## 4. AICPU

- 编程入口 950 限定：`asc-devkit/.../ai_cpu_programming.md` L8-12。
- 设备侧任务载体：AICPU SQE（`aicpu_sqe.h`；v201 `RT_DAVID_SQE_TYPE_AICPU_D`）；调度进程=`PROCESS_COMPUTE(aicpu_schedule)`/`CUSTOM_COMPUTE`（TsdSubProcessType）；调度实现目录 `runtime/src/aicpu_sched/{aicpu_cust_schedule,aicpu_kernel,aicpu_processer,aicpu_prof}`。
- **术语表**：现条「片内通用 CPU 核…」保留＋可补「任务经 AICPU 类 SQE 下发、由 aicpu_schedule 进程承载」——**待批，本轮未改**。

## 5. BQS/queue_schedule

- `runtime/src/queue_schedule/{client,server,common,stub,pub_facility}`；`common/bqs_util.h` L11-20（include guard/namespace）；client `ezcom_client.h` L21 `namespace bqs`＋`proto/easycom_message.pb.h`。
- 被 TSD 编排（PROCESS_QUEUE_SCHEDULE）。
- **术语表**：现条已够；「BQS」展开名继续不写（无出处）。

## 6. tprt（新核）

- `runtime/src/tprt/inc/external/tprt_type.h`：`TprtSqCqPropType`（SQ_HEAD/TAIL/STATUS、`SQCQ_MAX_DEPTH=1024`）、`TprtTaskSendInfo_t`、`TPRT_ALLOC/FREE/QUERY SQ/CQ`——SQ/CQ 资源管理＋任务提交传输层。
- glossary 现条「跨主机/跨设备传输的平台抽象（跨卡链路差异收口），涉及 URMA 等」出处=书内前章；**源码实证句**（本条）待批后替换或并存。

## 7. Host/Device/H2D/D2H/D2D

- `runtime/docs/zh/api_ref/11-01_Device_memory...`、`11-02_host_memory...`（内存两族）；拷贝接口族见 11-x 系列——术语现条无冲突，不动。

## 8. DFX/CMO 等

- CMO：`11-06_CMO_memory_operation.md`（`aclrtCmoAsync` Device 侧 Cache 操作）——rev1 已证，术语条未加接口名，待批。
- DFX 子模块清单：书 ch7 依据；本轮未再回源。

## 汇总：术语表下一批候选改动（待批）

| 条 | 建议 | 依据节 |
|---|---|---|
| Stream/Task | 补「host 序列抽象→SQ」「构建期装配 SQE」 | §3 |
| AICPU | 补 SQE/进程承载句 | §4 |
| tprt | 换/并存源码实证句 | §6 |
| CMO | 补 `aclrtCmoAsync` | §8 |
| TSD/SQE | 首轮 R1 已改，本表存档 | §1/2 |

边界：纯只读；未动 glossary（本轮 R1 词条已于报告附录记录）；未安装。


---

# R2 补充（reviews/APPB-R2 后定稿）

## tprt（定稿，术语表已改）

接口面实读 `runtime/src/tprt/inc/external/tprt_api.h`：`TprtDeviceOpen/Close`、`TprtSqCqCreate/Destroy`、**`TprtSqPushTask(devId,TprtTaskSendInfo_t)`**、`TprtCqReportRecv`、`TprtGetSqState`；`tprt_type.h`：SQ 属性（HEAD/TAIL/STATUS）、`SQCQ_MAX_DEPTH=1024`、`TprtSqCqOpType`（ALLOC/FREE/QUERY/CONFIG）。**职责=SQ/CQ 资源管理+任务推送/完成回报**；旧「跨主机 URMA 平台抽象」释义无据已删（URMA 另条保留于通信语境）。

## TSD（补 host 侧）

`tsd_process_controller` 构造注入 `DeviceCommAgent/CapabilityManager/PackageManager/ProcessSharedContext`；`TsdSubProcessType` 含设备侧进程族。**子系统含 host client（tsdclient）——术语条已补「host 侧 client 亦属该子系统」，不限定设备侧。**

## Stream/Task（定稿，未加未证链）

Stream 按 Runtime API 语义定义（创建/销毁等待任务/失败模式/溢出开关，`06_stream_management.md`）；**不写「Stream→tprt→SQ」「所有 Task 均构建 SQE」一刀切链**（未逐行闭合）。Task 条只补「构建期装配为 SQE 经流下发」——该句由 v200_base/v201 填充链支撑（KernelTask→SQE 装配），但**不称唯一映射**。

## AICPU（去绝对句）

950 限定仅「编程入口文档」层面；**不写「仅 950」**；「设备侧经 AICPU 类 SQE 下发、aicpu 调度进程承载」由 `aicpu_sqe.h`+`TsdSubProcessType.PROCESS_COMPUTE` 支撑，已照此改。

## MTE3 更正记录（本轮 glossary 同步改）

rev3 曾把「L1→UB」混入 MTE3——3510 表 L1→UB 属 **PIPE_MTE1**（L133），UB→L1 才 MTE3（L134）。已改：MTE3=UB→GM（2002/2201 叙述）+UB→L1（3510）；MTE1=L1→L0A/B+3510 L1→UB。两行均单向、无混排。
