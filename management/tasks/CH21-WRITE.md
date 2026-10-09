# CH21 正文任务
保持现有模型。只改docs/05-comm/ch21-hccl.md、专属图、CH21证据/提纲/报告与validation/ch21-*。不改CH20/全局，不提交。按补证边界写8k–12k中文，深入主线，勿目录罗列。
经理亲读main.cc与SelectAlgfor910B后，以下必须先修研究记录再落正文：
- AllReduce按元素跨rank归约，输入每rank为[0,1,...,N-1]，输出第i元素=N*i，绝非Σi或N(N-1)/2标量。给N=2手算输出[0,2]，不是[1,1]。样例只打印、不校验；本书手算不是实测。
- isMeshTopo拓扑枚举与isMesh=IsAlgTypeLevel0Mesh(algType_.algoLevel0)不是一个变量！实际isAivMode用后者。不要自写伪码标未删节；复制真条件或明确伪码和变量映射。
- 主机接口、device API和legacy选路是三个证据范围，不画缺失weak链接成已证调用箭头。第一条主线只到Host样例完成/销毁；legacy选择作为独立内部实现案例。旧账本前文错句应删改而非仅尾部追加更正。
- LocalReduce输入表UINT8（不是UINT6）与INT8例保留源文不一致，不构造实际支持结论；与AIV RS案例分开。
- 所有API签名、产品矩阵按实际页；notify双向握手仅证明所示一次交接，不声称多轮无竞态。单机rank=device是样例选择，不泛化。
- 五要素性能，无硬件不新增性能表。旧提纲无法实现的承诺明确缩小范围，不能虚构仓外代码。正文不要写管理文件依赖、内部U号或评审历史。
- 命令逐个核README/Makefile，包括MPI、设备数、CANN环境、数据工作目录，提供只读源仓的临时副本方式，未知参数不猜。源码摘录[示意代码]；未本机验证运行[需真机验证]，不得称真机实测。
完成完整脚注和图、实际npm run verify日志、CH21-REPORT（覆盖/未覆盖/限制），待经理验收。
