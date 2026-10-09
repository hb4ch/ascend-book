# CH24 补证与提纲纠偏
经理已读证据/提纲并亲读gemm_demo.cpp83–121、pto_tile.hpp1706–1728。暂不正文，保持模型，仅CH24。
1. B7称A矩阵按列存错误：GlobalA stride末两维kK,1，GM是行主序；Tile的BLayout是分形块布局，不能混同GM或块内SLayout。解释TLOAD完成何种转换并追CPU实现，用实际offset数值验证。
2. C1泛称所有指令返回RecordEvent需收窄。提纲说gemm_demo L103–121有TSTORE(dst,src,ev)，实际只有TSTORE(cGlobal,cTile)，无ev。明确主例没有显式事件，另选真实设备事件例，不拼成同一代码。
3. 图②16×16 float=1024B，不是整个512B；8×8 float=256B。基于真实BLayout/SLayout/FractalSize配置画容量、有效区域、分形块，附脚本复算偏移与元素总字节数。有效区不等于所有指令都自动遮罩，核主例TLOAD/TMATMUL/TSTORE各约束。
4. 不承诺同一float CPU示例不改就跑所有NPU：核NPU TMATMUL dtype/形状，注明仿真可用不等于设备支持。TileLeft分支只证明别名选择，不能证明整程序跨代兼容。
5. A1引文AI OCR疑误抄，回读README原文纠正；B1模板六参数不准确，避免计数；E1“或根README”不是证据；A2指令计数非主线删去。不要逐个列12通信指令凑信息。
6. F2复跑输出保存日志，既有binary复跑不要叫重编译。工具链版本回源现有记录核实。正文不对读者说“刚才在你的CPU跑了”或“NPU运行”，只称本书环境实测CPU-SIM。
交付修订证据与提纲、CH24-EVIDENCE-CLOSE-RESPONSE.md及复算/运行日志。先具体例子，减少抽象名词堆叠。不得改23章或提交。
