# 第18章关键证据收口

研究已收到，先闭合机制，不写正文。保持模型，不碰第17章/appD，不提交推送。
读取CH18-EVIDENCE与OUTLINE，补闭U1/U2/U5/U6/U7/U8/U9：限定一个明确arch35非量化训练模板和固定shape，逐项给模板实参、入口、Tiling条件、实际块尺寸、flag定义/方向/前置pipe/复用条件及收尾。在线softmax式逐步关联代码变量，区分未归一化累计与已归一化输出；不能泛写“cur乘某个因子”。max/sum的真实dtype与尾维8意义须回源，无法证实不猜。
给独立数学小例：S1=S2=4,D=2，则Q/K/V均4×2，不能研究中写成2×2矩阵。可用标准库Python实际计算全量softmax(QK^T/sqrt(D))V与逐KV块online递推，保留脚本和运行日志至management/validation/ch18-online-softmax.py及.log。明确仅数学验证，不是NPU或kernel验证。
U4至少选arch22入口与对应arch35做真实控制/数据路径对照；U10/U11仅明示算子边界即可，U12无性能数字可如实留白，无需外搜凑数。把剩余未证项缩至非主线；主线同步和精度未闭不能开始正文。
更新证据/提纲，并交付CH18-EVIDENCE-CLOSE.md（列已闭及未闭理由）。证据必须短摘录和真实路径，不能只行号和自称已证。完成等经理。
