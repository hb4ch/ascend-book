# 第14章验收
经理全文阅读，独立核对AddExample host平台查询、UB六块预算、dtype到TilingKey及kernel float/int32分支；限定输入和npusim950范围，节选补返回及省略边界。
实际查看ch14-r2-page-journeymap-w640.png与mermaid-w640.png：八站两行、回路纵向，文字可读，无遮挡。独立npm run verify进程86358已由write_stdin取得真实exit_code=0；日志ch14-manager-r2-final.log，随后再次读取末尾确认完整结束；指定文件diff --check退出0。
验收范围：本章正文与ch14-journey-map.svg。无NPU或仿真执行；源样例非整除末核行为未验证，正文已明确。全书最终一致性另审。
