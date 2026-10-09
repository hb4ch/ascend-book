# 第24章 PTO 源码研究与读者提纲

第23章由经理独占收尾，你停止修改CH23及其交付。保持当前GLM模型、现有会话，不提交推送。
阅读PLAN-COMPLETION、STYLEGUIDE、management/ACCEPTANCE、SOURCE-BASELINE、docs/06-backend/ch24-pto-isa.md及management/validation/PTO-CPU-GEMM.md。只读固定基线/mnt/SATASSDEXT4/cann/pto-isa，研究第24章。
交付management/CH24-EVIDENCE.md与CH24-OUTLINE.md：以一个简单tile计算例子解释PTO解决什么问题、数据布局/有效形状/指令/同步如何组成程序、CPU-SIM与NPU后端边界；先具体例子再抽象，避免接口字典。设计2–3幅真正帮助理解的图，解释各图回答的问题。追踪一个可复现CPU-SIM例子，复用既有真实执行记录但核对命令与版本，不把仿真当NPU验证。说明硬件代际差异与未闭证据；每条关键论断给完整路径、符号、行号及证据摘录。不要仅凭目录名推断产品支持，不虚构性能。暂不写正文，研究完成候审。
