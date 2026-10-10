# APPB-API-EVIDENCE —— API 与维测术语回源（第三批）

2026-10-10。任务：management/tasks/APPB-API-AUDIT.md。基线 SOURCE-BASELINE（runtime `681ef76` 2026-08-22 / asc-devkit `28e7aba2` 08-22）。每条：术语→源证（完整路径）→术语表处理。**未核不计已审**；统计见尾。

## 1. 两处残留收窄（任务令）

- **Task**：仅保留「一次可调度执行单元」，**删除 R2 加回的「构建期装配为 SQE 经流下发」泛化**（该链未逐行闭合，降级为 RUNTIME-EVIDENCE 观察记录）。
- **TSD**：删「设备侧服务子系统」开头限定→「runtime 服务子系统，管理设备侧子进程（…经 HDC 通道与 host 通信）」——host client 属子系统不再需要补丁句。
- PyPTO：未动（保持 R2 无后端猜测版）。

## 2. ACL / AscendCL

- 证：`runtime/README.md`「Runtime 组件：…用户编程接口」；实现目录 `runtime/src/acl/`（aclrt/aclrt_c/aclrt_impl 等）。
- 处理：说明补「（runtime `src/acl` 实现，Host 编程入口）」。

## 3. ACLNN / aclnn（含 aclnnTensor 辨析）

- 两段式：`asc-devkit/.../appendix/common_operations/develop_dynamic_input_operator.md` L75 签名 `aclnnAddNCustomGetWorkspaceSize(const aclTensorList*, const aclTensor*, uint64_t*, aclOpExecutor**)`；ops-transformer 算子文档同构（如 `aclnnRopeWithSinCosCache.md` L221 `const aclTensor*`）。
- **aclnnTensor 辨析**：runtime 仓 grep `aclnnTensor` 零命中（2026-10-10）——张量实体=`aclTensor`（`runtime/include/external/acl/` 头族；例程 `example/2_advanced_features/model_ri/model_utils.h` L24 `CreateAclTensor(..., aclTensor**)`）。「常见 aclnnTensor」旧说废止。
- 处理：ACLNN=两段式接口（GetWorkspaceSize→Execute）；aclnn=前缀＋「本书证据内未见 aclnnTensor 类型名」。

## 4. Stream / Event（含计时限制）

- Stream：`06_stream_management.md`（创建/销毁等待/失败模式/溢出开关）；ACL_STREAM_HUGE 容纳更多 Task（L168 附近）。
- Event flag 族（`07_event_management.md` L156/L257）：SYNC（多 Stream 同步）/TIME_LINE（时间戳；**「使能时间戳功能会影响 Event 相关接口的性能」原文**）/CAPTURE_STREAM_PROGRESS/EXTERNAL/IPC（950DT 限制）/DEVICE_USE_ONLY。
- 计时：`aclrtEventElapsedTime`「统计两个 Event 之间的耗时」——依赖 TIME_LINE flag；IPC Event 不支持 ElapsedTime/Timestamp（L257 明列）。
- 处理：Event 条按 flag 分化改写；「计时原语」改「计时（TIME_LINE+…）」；无「仅同 stream」断言（未证）。

## 5. CMO（非笼统「一致性」）

- `25-02_Enumerations.md` L856-859：`ACL_RT_CMO_TYPE_{PREFETCH(预取)/WRITEBACK(刷新留副本)/INVALID(丢弃)/FLUSH(刷新不留副本)}`——**四类 Cache 操作，非全是「一致性」**。
- 现状：`11-06_CMO_memory_operation.md` L55「当前仅支持 ACL_RT_CMO_TYPE_PREFETCH」；WithBarrier+INVALID 配 `aclrtCmoWaitBarrier`（L110）。
- 处理：术语改「Device 侧 Cache 内存操作四类；当前接口仅开放 PREFETCH」；全称更正 cache **memory** operation。

## 6. DFX / msprof / adump / trace / error_manager

- `runtime/README.md` L8-14：维测组件=性能调优（msprof）/精度调试（adump，单算子或模型每层输入输出+异常时 Workspace/Tiling）/日志（log，含 msnpureport）/错误记录。目录实证：`runtime/src/dfx/{msprof,adump,log,error_manager,trace}`（trace 下 atrace/awatchdog；error_manager 含 `error_code.json`+`error_manager.cc`）。
- 接口面：Dump 配置 `18_dump_configuration.md`（aclmdlInitDump/SetDump/acldumpRegCallback）；msproftx 扩展 `19-02_msproftx_extension_apis.md`。
- 处理：DFX 条列五子模块＋双证（README+src/dfx）；msprof/adump 按 README 原句收窄。

## 7. DumpTensor

- `asc-devkit/.../appendix/show_kernel_debug_data_tool.md` L3：`AscendC::DumpTensor`/printf/PrintTimeStamp/assert＋acl.json Dump 配置＋show_kernel_debug_data 离线解析；API 页 `api/SIMD-API/basic_api/debug_interface/onboard_print/DumpTensor.md`。
- 处理：由「数据 dump 指令」改为「设备侧打印/dump 接口＋配置与离线解析链」。

## 8. Simulator / npu_sim（≠笼统 CPU Simulator）

- 两个语境：pto-isa CPU Simulator（`pto-isa/README_zh.md` L45/L68「CPU 上功能验证与开发调试」）vs CANN 构建仿真（`asc-devkit/cmake/asc/asc_modules/CMakeASCInformation.cmake` L163-172 `CMAKE_ASC_RUN_MODE=npu/cpu/sim`）。
- 处理：词条改「仿真统称，按语境分指两物，勿混」。

## 9. ms_sanitizer

- 书内 ch7/11 按工具链引用；**runtime 仓内未单独审（dfx 无 sanitizer 目录）**——词条注明「仓内未单独审，待批」，不计已核源码。

## 统计与台账

- 本批**源码/文档实证并改写**：Task、TSD、ACL、ACLNN、aclnn、Event、CMO、DFX、msprof、adump、DumpTensor、Simulator/npu_sim = **12 条**。
- 仅注脚注化不改义：MTE1/MTE3/AIC/SMEM/URMA/ND-DMA/AICPU（注号替换）。
- ms_sanitizer：**待批**（仓内无独立实现目录）。
- 台账 `APPB-AUDIT.md` 已按本批刷新（状态列+源文件列）；「保留≠已审」——未核条目仍标记待审。
- 脚注 [^1]–[^12] 于 glossary 文末；表内引用全部 `[^n]` 标准脚注。
