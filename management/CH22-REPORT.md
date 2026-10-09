# CH22 REPORT——正文交付（rev1，2026-10-09）

任务：`CH22-WRITE.md`。交付 `docs/05-comm/ch22-hixl.md`（**9,695 字 / 中文 7,399**，工具口径同 ch21 10,988/7,846）＋无新增图文件（采用 1 幅 mermaid 时序图，符合 STYLEGUIDE「优先 mermaid」）。未动 CH21、未提交。

## 覆盖对照（任务书逐条）

1. **auto_connect_ 门控与重试语义（先修后写）**：EVIDENCE 已升 rev3（§13.4 订正）；正文 22.5 两分支真码（节选标注〔示意代码〕）＋两侧世界对照表＋四层限定（自动/显式、AutoDisconnect 门控空转、自动断链可失败、**对象复位≠可安全重放/timeout 可能部分写/重试决策归用**，不承诺幂等或完成）。
2. **主线**：quickstart 双进程两终端、READ 主轴、全生命周期（22.3 mermaid 时序，行号锚）；**done 先于 Disconnect 与 server 收尾窗口严格保留**（22.3.2：`HixlCSServer::Finalize` L273-320 不等待任何 client；改进建议标「本书设计未执行」）；复现命令=真跑 quickstart 两角色（`--role=server/client`），非 d2rd；源仓 mktemp 副本；环境/设备/目录齐备，全程〔需真机验证〕、本书未执行。
3. **异步三层状态表**：22.6 五行表（CS/handler/engine 单条/engine 批量/同步包装）＋Status≠status 辨析＋WAITING 保留/终态消费/批量过滤与连带 FAILED/使用者保存 req·user_data 姿势（〔示意代码〕）。**限定 CS DIRECT**，UB/legacy 不外推（22.4.1 末段明示两代引擎断层；UB lazy 仅一句带过标不展开）。
4. **host_flag**：22.4.3 五步链＝同 stream D2H 常量 1（dev_const_one），核内 notify 二进制缺口明确（`libcann_hixl_kernel.json`，U 标注）；**sync 仅 SUCCESS 才完成**（22.6 末）。
5. **协议/引擎两层选路**：22.4.1 阶梯＋候选优先级∩双端交集，明确「候选≠选中」。
6. **FabricMem/BUFFER_POOL/LLM-DataDist 边界与版本条件**：22.7.2/22.8（互斥、HDK 25.5 特例、A2 HCCS 仅 D2D、v1.2/v1.3 引擎分叉、950 UB）；性能列全条件（引擎×方向×块×AICPU/Host 展开×平台），**测量 CANN 版本仓内未注明→正文如实标「版本未知」**，未挑极值当保证。
7. **标签纪律**：仅〔示意代码〕/〔需真机验证〕两种（本书允许四类，本篇按需用二）；脚注 `[^A]–[^L]` 12 条全 repo 相对路径，**24 个文件路径逐一 `test -f` 实核通过**；正文无内部 C/D/U 编号、无管理文件引用、无返修史。
8. **图**：1 幅 mermaid sequence（真实双端时序含收尾窗口标注），无文字盒充调用流。

## 超出任务书的增量（供裁量）

- **22.4.4 内存视图快照**：Engine RegisterMem 仅 server 侧＋mem_map_，无增量推送→**建链后新注册对既有链路不可见**（校验双端 region 表 `BatchValidateMemoryAccess` 实证）——任务书未要求，属「注册时机」必要结论，已入陷阱 15。
- 22.9 性能验证路径（bench 用法＋测量三纪律）。
- 选型决策段与「两代引擎心智模型」警示（22.1/22.4.1/陷阱 14）。

## 限制与未证（正文已声明）

- kernel 内部 notify/数据落地保障（CANN 二进制内）——仅到 host 侧证据链。
- 收尾窗口实际竞争是否可观、UB handler/FabricMem engine 内部——未逐行。
- 全部命令与性能数字未真机执行/测量；`npm run verify` 0 FAIL（log：`management/validation/ch22-write-verify.log`，含 word-count 行 `9,695 字 (中文 7,399)`）。

## 字数裁量备案

中文 7,399 低于 8k 名义下限：覆盖 8 节主线+3 图表载体（表/码/时序），密度对齐 ch21（7,846）；差额主要让位于「表格与代码承载事实、正文不复述」的写法。**请 PM 按ACCEPTANCE 裁量**；如需补足，候选扩写点：22.4.2 UB 路径对照、22.6 notify 机制、22.8 LLM fsm 状态全表。
