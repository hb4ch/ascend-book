# APPB剩余术语：基础内存与生态批次
原模型、源仓只读，不提交。当前API批已读，先纠经理回源发现：CMO“当前接口仅开放PREFETCH”只适用于aclrtCmoAsync，11-06同文的WithBarrier参数明确INVALID+barrierId并配WaitBarrier，不能推广接口族。术语仅写Cache操作，类型支持依具体接口/产品；证据逐接口列。ACLNN也含自定义算子，删“预置”唯一限定。Event表内不要列满flag，留短定义+脚注。
脚注4等依旧目录前缀只给首个文件，后续basename无法校验，全部改成完整路径。ms_sanitizer待审放管理台账，不把“待批”写读者表；搜索asc-devkit/learning-hub实际调试文档而非只看runtime目录名。
本批回源所有仍保留未核的基础内存与生态/通信术语：L1/L0/UB/L2/Register/bank conflict/Double Buffer，PTO/PTO Virtual ISA/Tile/Block，HCCL/HCOMM/HIXL/HCCS/RoCE/MC2/PD/KVCache，AOT Superkernel/npugraph_ex/AutoFuse/TorchAir/TileLang/Mooncake/vLLM。按固定源码README/实现或仓内官方文章定位，区别原项目实现与文章转述。删除无支持的指令数量/屏蔽所有代际差异等绝对句。可用前述已验收证据定位，但必须实际读所需原文件。
新增APPB-REMAINING-EVIDENCE.md，短定义修glossary后sync；逐行审计台账列明确文件/证据状态，未找到的不要强行记已核。基础常识只需适当出处，无需过度扩写；本轮范围外未核列清单。每个长表定义尽量一句话，图表可读性重于研究细节。
真实verify退出码和新截图（旧图不代表新文稿），候审。
