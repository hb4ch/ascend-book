# 第12章验收（2026-10-11）
经理全文阅读最终正文，回源编译模式/LTO/静态库流程、basic_compile与RTC样例、npusim限制和custom_kernel扫描；本轮收紧动态升级、自包含与shape无锚表述。命令标注未编译/仿真，未声称NPU实测。
实际查看最终ch12-final-page-pipeline-w640.png（窄版三路/Fatbin/Host/RTC分明）和RTC Mermaid页面截图，图中文字可读，Host不进入Fatbin，RTC Device ELF独立加载。此前旧图小字失败已重排修复。
最终经理独立npm run verify session24193真实exit0，日志management/validation/ch12-manager-accept-verify.log；指定正文及SVG diff --check通过。验收仅正文、一幅SVG及本记录，其他活动章节不纳入。
