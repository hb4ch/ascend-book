# APPB下一批：API与维测术语回源
首批R2收到，MTE归属已纠正；仍未验收。保持原模型会话、源仓只读，不提交。
先直接收窄两处残留：Task只保留“一次可调度执行单元”，删除所有Task装配SQE的泛化；TSD删开头设备侧限定，写“runtime服务子系统，管理设备侧子进程”，无需一长段补host例外。PyPTO保持无后端猜测。
本批范围：ACL/AscendCL、ACLNN/aclnn、Stream/Task/Event/Notify、CMO、DFX/msprof/adump/ms_sanitizer/DumpTensor/npu_sim/Simulator/Error Manager/trace。实际读接口头/文档/实现，逐条原定义→源码证据→短定义。尤其aclnnTensor是否真实类型（常见实际aclTensor）、npu_sim是否等于CPU Simulator、CMO是否全是“一致性”操作、事件计时限制要查。不凭其他章节自证。
glossary只改本批核实项，同步生成appB；新增APPB-API-EVIDENCE.md，更新APPB-AUDIT逐行源文件与状态。仅“保留”不是已核，100%过目不等于100%审查，统计明确已核/待核数量，别把与已验收章一致计源码核验。
来源用标准Markdown脚注[^...]关联词条，不用“注1”纯文字；路径精确到文件且完整。短定义尽量一句，附录读者不看研究史。verify真实exit、报告和截图，候审。后续再审生态和基础内存条。
