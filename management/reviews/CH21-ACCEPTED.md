# CH21 最终验收

2026-10-09，通过源码与文稿审查，未NPU编译/运行/实测。本记录优先于历史研究与响应；历史文件保留返修过程，不能代替最终正文。

经理独立核查Host样例输入N*j、同步与释放次序；legacy weak入口断点、SelectAlg先于资源与编排、910B AIV全条件及量纲；Read/Write发起方向、Nbi产品限制与Fence排序；Device Hccl 2201/3510包含链、AICPU/CCU特化、InitWorkingFlag、Commit/Wait/Finalize及产品使用页。修复把代码存在当产品支持、仅核0泛化和拓扑枚举直接等同等问题。

SVG已渲染并实际目检。命令从只读源仓复制至临时目录，bash -n仅检查语法。最终日志ch21-release-verify.log及ch21-release-bashn.log；diff检查；源码路径通过不等于论断正确。

约7.9k中文，接受略低于8k目标：完整Host主线、独立legacy算法算例、HCOMM数据面、Device消息与完成链、平台矩阵及复现限制均覆盖，不以重复内容补字。

保留限制：无NPU实测；Host公开入口至legacy Communicator的weak连接未证，不能断言样例实际选路；3510 AICPU代码存在但产品使用页950仅CCU；LocalReduce UINT8参数表与INT8示例矛盾未裁定；notify案例只论单次交接，不证明通用环槽；未逐条展开所有算法/原语。第22章未验收，不随本章提交。
