# CH22 R3 RESPONSE——逐条实改（2026-10-09）

对象：`docs/05-comm/ch22-hixl.md`（**11,371 字 / 中文 8,645**）＋EVIDENCE §13.10（rev6）。verify 0 FAIL（`ch22-r3-verify.log`）；3 bash 块 `bash -n` 过（`ch22-r3-fence.sh`/`-bashn.log`）。逐条（引号=现文）：

**1. ACL 错误映射**：22.6 TIMEOUT 段②重写——「仅 `ACL_ERROR_RT_STREAM_SYNC_TIMEOUT` 映射 `hixl::TIMEOUT`，其余 ACL 错误原值 `static_cast<Status>` 透传（hixl_checker.h L116-125）——『同步失败』≠TIMEOUT、更≠FAILED」；同步包装表行改「错误透传非归并」；复用纪律加「其余同步失败（ACL 原值）清理程度逐分支不同，同样按未证对待」。hixl_checker.h 入脚注 ^G（L116-125 全语义）。

**2. 提交≠完成／计时起点／20min per-call**：④重写——「重试返回后 HostAsync **还须 Fence 排序＋对端 flag ReadNbi（L535 区）方返回 handle**：提交返回≠传输完成，提交期长阻塞只是『提交可等待重试』，完成判定仍归 CheckStatus 读 flag」；①补「deadline 在 HostAsync 返回之后才起算，timeout_ms 不覆盖提交阶段（源码次序推导，非实测）」；③改「**每次调用各自起表，非整批共享总窗**」。原「内联执行全部传输与重试」句已替换。

**3. 复现**：构建块加 `set -e`＋`echo "WK=$WK"`＋`test -d`；两角色块各 `set -e`＋`WK=/tmp/tmp.XXXXXXXX  # ←占位：替换（独立 shell 不继承）`＋`test -d "$WK/hixl" && cd`＋各自 source；`set -e` 计 2 处、`test -d` 2 处；bash -n 过。

**4. 批量分支表**：新增 B1–B6 表（条件/是否查询/返回元素/登记与断链四列）——**owner 消失移出 FAILED 结果列（B1 无结果）、正常 FAILED 独立 B4、补 B6 截断未遍历**；层表 engine 批量行改「分支表见下」；正文同步 B1–B6 编号；「未出结果」=三成因。读表三点②③改引 B2/B3/B4。

**5. 示意代码**：提交/查询均检查公开 wrapper 返回码（`qs != SUCCESS→handle_query_error`），注释明「前置检查 impl_ 空即 FAILED（L374-382/L393-397），恒 SUCCESS 仅引擎内部层」；签名改真实五参 `(remote, op, descs, TransferArgs, req&)`；结果字段 `{req,user_data,reserved[108]}`（hixl_types L87-91）；`inflight` 生命周期注释「与 ctx 同生命周期、函数退出前收尾，不留悬挂 user_data」。

**6. 去绝对断言＋结束条件**：「库不区分只能自记台账」改三成因分别处理＋「终态确认可辅单条 GetTransferStatus（PARAM_INVALID=已消费或不存在）」；新增⑤「收束：循环终止=inflight 空或余项得终态/PARAM_INVALID；无结束条件的继续查不是完整设计」——不再保留未完成伪封装主体，仅原则+示意。

范围仅 CH22；CH21 未动；未提交。候审。
