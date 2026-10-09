# CH21 补证：调用链不能跨层拼接
保持模型，只改CH21研究文件，暂不正文，不改CH20。
1. 主线Host HcclAllReduce的异步/完成证据用Host样例main.cc与对应接口文档，不能用AscendC::Hccl设备侧头注证明Host契约。样例count=devCount、各rank输入i、FP32 SUM→结果rankSize*i，列出实际buffer大小及销毁代码；核实rank与deviceID映射是样例单机假设而非通用规则。
2. all_reduce_operator.cc实际在hcomm/src/legacy/ascend910/algorithm/impl/operator/，不能短路径掩盖legacy。列出公开Host入口到该选择器调用链，若本地缺上层则承认无法证明样例实际走它，改独立legacy选路案例。完整展开910B AIV布尔式实际符号和每个阈值定义，明确按总字节/每rank计算；不得用“五连∧”压掉OR/排除条件。
3. AICPU仅A3/300I来自legacy特定配置分支，不能外推所有HCOMM AICPU引擎平台支持。分别查新标准目录引擎支持和legacy选择，列表区分文档范围/实际源码条件。
4. P2P四步需要两端timeline，指出每个notify保护何buffer何时可复用。只凭博客单次流程不能称无限轮环槽安全已证。API目录名不是签名证据，读取Write/Read/Fence/Notify实际文档，至少一条具体原语列签名、引擎、返回与完成语义。
5. LocalReduce文档本身输入表列UINT8但示例INT8→FP32；这属于源文不一致，不能当已证完整支持矩阵，更不能与AIV高精度ReduceScatter拼成同一实现。两例独立，保留源文歧义。
6. HCOMM SymWin不等于HIXL，CH22可对照但别转移本章通信域必要解释。所有路径完整repo相对，研究日期改2026-10-09。源码节录标签[示意代码]，未运行样例[需真机验证]，不要预标已验证NPU。
补证交付清晰边界和提纲修订，等待经理。
