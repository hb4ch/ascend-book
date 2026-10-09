# CH22 最终验收

2026-10-09：通过源码与文稿审查，未NPU编译、运行或实测。本记录优先于历史研究、R1–R4响应；历史报告曾与正文不一致，保留作过程记录，不能用作最终事实来源。

经理独立核对quickstart双进程READ、done先于Disconnect、Finalize忽略返回码；AutoConnect/AutoDisconnect门控；CS DIRECT三层查询与批量各分支；HostAsync提交重试、HostSync计时起点、ACL超时映射；共享slot按client、常量按device池、完成flag先于error检查；性能原表175.102/170.514及10.58倍率。回源修复错误后正文约9.1k中文。

验证：ch22-manager-verify.log及最终ch22-release-verify.log；ch22-manager-bashn.log为三段语法检查；git diff --check。经理已实际查看ch22-diagram.png，图清楚呈现并行收尾窗口；章首页面渲染正常。CLI深锚截图为空白但Playwright截图正常，无法仅凭空白判页面缺陷；不将具体浏览器paint原因当已证。宽表在不同渲染环境可能换行或横向滚动，不能由页面无横溢出断言所有单元格都无溢出。

限制：无NPU执行；kernel内部notify协议在二进制缺口内，不能从Host flag反证全部设备逻辑；状态登记消失不等于在途访问已结束；失败重放由应用一致性策略决定；query语义限定CS DIRECT不外推UB/legacy；源仓性能环境软件版本未知；样例收尾窗口未实测。后续全书审查继续检查跨章术语与排版。
