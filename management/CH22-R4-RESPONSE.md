# CH22 R4 RESPONSE——逐条实改（2026-10-09）

对象：`docs/05-comm/ch22-hixl.md`（**11,779 字 / 中文约 9,045**）＋EVIDENCE §13.11（rev7）。verify 0 FAIL（`ch22-r4-verify.log`）；3 bash 块 `bash -n` 过（`ch22-r4-fence.sh`/`-bashn.log`）；脚注 `[^A–L]` 闭环。**本报告以最终正文 rg 实测为准**（文末附核验计数）。逐条：

**1. 批量分支表逐行重排（对 `hixl_engine.cc` L264-310）**：erase 条件=`status!=WAITING`→**WAITING 永不 erase**；表扩为 B1–B7——B1 client 空/B2 已在集合（跳过查询）/B3 调用失败（status 强制 FAILED→erase＋出元素）/B4 **COMPLETED 正常终态（新增）**/B5 FAILED 正常终态/B6 **WAITING 保留注册，`skip_waiting`（L307-309）只过滤元素与登记无关**/B7 截断。正文列表、读表三点（B2/B3/B4/B5）、三成因（B1/B6/B7）同步改号；层表行改「B1–B7，逐行对 hixl_engine.cc L264-310」。

**2. 同步 TIMEOUT 三路＋清理分写**：表 TIMEOUT 列改「①HostSync deadline／②DeviceSync ACL 映射／③提交链 `TransferWithRetry` 经 HostAsync 透传｜清理逐分支不统一」；产生点①补源码次序——`BatchTransferHostSync` **先 `HIXL_CHK_STATUS_RET(BatchTransferHostAsync…)`（L958-959，③经此透传）再进 deadline 轮询**（消除与本段调用链的自相矛盾）；新增⑤「同步包装 TIMEOUT 两源：HostSync=①或③（句柄未必建立）、DeviceSync=②」；复用纪律改「**按分支对待，不统一承诺清理状态**：①release handle／③提交链内清理／②slot Abort；共同点仅『写没写完不可证』」。

**3. 复现脚本**：构建块现含 `set -e   # 任一步失败即停`（R3 报告虚报，本次实测在文 L127）＋`test -d`＋cp/cd 分行＋**echo 只打 WK 根目录**（`echo "WK=$WK"`，注释「下两终端 cd 时自行拼 /hixl」，消除双拼）；两终端 `test -d "$WK/hixl"` 与 `cd "$WK/hixl"` **分成独立命令**（注释：&& 短路不触发 set -e），占位注明「替换为构建块 echo 的 WK 根目录」。

**4. 删伪封装**：「小型状态封装」整块（含全部示意 cpp）已删（rg：`小型状态封装`0、`inflight`0），改四条原则——签名（hixl.h L143-145 五参＋wrapper 前置检查 L374-382/L393-397；`TransferArgs{user_data,reserved[120]}`、`TransferResult{req,user_data,status,reserved[108]}`）；提交（返回码先查；**上下文要经 `optional_args.user_data=&ctx` 传入，不传入就别指望结果携带**）；查询（返回码先查；单轮未完成者离开作用域前须仍可安全再来一轮）；对账收束（三成因；**`PARAM_INVALID` 只证明「无登记」——表项 erase≠在途访问结束，不能单独用作可释放证明**；释放=终态＋应用核对）。

**5. Finalize 次序与打印**：22.3.2 收尾窗口段后新增一段——quickstart `Finalize`（L120-137）次序 close socket→DeregisterMem（**返回码忽略**）→打印 done→aclrtFree（忽略）→engine.Finalize→ResetDevice；「`DeregisterMem done` 只证明调用已返回，不证明解注册成功」；收尾窗口下**不得以该打印作成功验证**。脚注 ^C 补次序链。

## 核验（rg 实测）
`set -e`×3 块（L127/141/152）＋注释 2；`test -d "$WK/hixl"`×2；`echo "WK=$WK"` 根目录×1；`永不 erase`×1；`HIXL_CHK_STATUS_RET(BatchTransferHostAsync…)`×1；`不统一承诺清理状态`×1；`小型状态封装`/`inflight`×0；`只证明「调用已返回」`×1。

范围仅 CH22 两文件（正文＋EVIDENCE）；CH21 未动；未提交。候审。
