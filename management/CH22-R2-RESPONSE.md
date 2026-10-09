# CH22 R2 RESPONSE——逐条实改（2026-10-09）

对象：`docs/05-comm/ch22-hixl.md`（**10,764 字 / 中文 8,238**）＋EVIDENCE rev5。verify 0 FAIL（`ch22-r2-verify.log`）；3 个 bash 块 `bash -n` 过（`ch22-r2-fence.sh`/`ch22-r2-bashn.log`）。**每条附正文实际新句**（引号内为现文原文）。

**1. 错误主句实删（全文 rg 核）**
- 22.5 原「『失败后直接重试』只在自动模式成立」整段重写为按模式分列：「**自动模式**：…重建是下次传输的行为，不是本次返回的承诺；重连后的链路是全新对象。／**显式模式**：…重试前置条件是应用先显式 `Disconnect`→`Connect`」。rg `失败后直接重试`=0 命中。
- 22.3.3 原「属预期而非故障」删，新句：「两支并行的先后不构成正确性判据，结果须按 22.3.2 的窗口语义理解」。rg=0。

**2. 示意代码**：新块五段——提交 `if (st != SUCCESS) {handle_submit_error; return;}`；FAILED→`enter_consistency_check`（**plan_retry 删**）；注释④明写两分：「a. WAITING 被过滤：仍在册；b. owner 已消失被静默 erase：**不在册且无结果**——库不区分，应用凭自记台账对账，不可假设未出结果=都在册」；另加 `inflight` 应用侧登记。

**3. 批量 FAILED 列全**：表行改三路——「①owner 消失→静默 erase 无结果；②调用失败→FAILED+erase+出结果+AutoDisconnect(void)；③集合连带→免查询 FAILED；另有 **ret=SUCCESS 且 status=FAILED 的正常终态**同 erase+出结果（无 AutoDisconnect）」；正文③改「**跳过查询、直接写 FAILED**」、②改「**该 req 有被查询**，只是调用未成功」；推论②改「仅②③未经成功查询」。

**4. TIMEOUT**：设计意图句删（「是给上层封装预留的词汇」→「检测函数无一处赋值」实证书写）；绝对句改具名三产生点并补 **HostAsync 内联重试链源码证据**（L508-516→L495-501→L452-487，L480/L968）：「提交返回的 `Status TIMEOUT` 是提交失败，**不是**查询态 `TransferStatus::TIMEOUT`——同名异层不得混写」。EVIDENCE §13.9 存行号。

**5. 协商/版本/往返**：「协商就落到次选」→「**交集为空则协商失败、建链不成立**——不存在自动落次选的保证」；版本双轨明归 d2rd（「quickstart **无**此参数，经 protocol_desc 直接选定」）；「一次额外往返」→「**单向的额外确认**（client→server 一条消息），并非对称的一往返握手」。

**6. 复现块拆三**：构建／终端1 server／终端2 client 各自独立块；每终端 `cd "$WK/hixl"`+各自 `source set_env.sh`；构建块注「可执行在 `build/examples/cpp/`（cpp/README L49），`build_out/` 仅 run 包（build.sh L15/L78/L215）」——CMake 输出已实核；「预期」改「观测点（仅描述打印次序，**不构成成功承诺**）」。

**7. 评价语清除**：「社区代码里最常见的病」→「两套模型不可互换」；「送分错误」→「写成普适结论都会错」。本 RESPONSE 各条均附现文新句，无未发生的声称。

范围：仅 CH22；CH21 未动；未提交。
