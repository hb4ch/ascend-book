# CH18最终验收

2026-10-09。通过源码与文稿审查，未进行NPU编译、运行或性能测量。此记录优先于CH18研究稿及R1/R2/R3响应中的历史结论。

经理独立核查固定ops-transformer e75072d7e7519405025d05a98cf1b2f106ad3874：train四级门控；IsDn/UbOutCondition/GetC2Position的带mask、half、128/128、D=Dv256组合；NdL0Split 1173/1177与Vec1 312/1226的分数缓冲握手；Vec1 1292的P就绪与Cube752的等待；主线Bmm2 846的UB条件等待及888就绪；GM Vec2 1629起的搬入、互斥首/中/末块和无反向Set调用；共享buffer方法与实际调用区别；Bmm2DataCopyOut的cast及API V2样例执行/流同步顺序。

纠正了Nd/Dn/Nz出口精度和模板串支、t=2四级齐、错配事件方向、fp16缩放参数推断、性能频漂保证及源码脚注。SVG末行文字错位和越界已修复，rsvg-convert渲染后实际查看，图为逻辑拍，非测量时间轴。

验证：ch18-manager-final-verify.log含全书构建、站内链接、来源和术语通过（后续全局账本更新另记录ch18-release-verify.log）；数学脚本输出fp64最大误差2.220e-16，仅验证递推；git diff --check。约5.7k中文超过FA 5k下限，低于8k目标，覆盖上述机制和API边界，接受当前范围，未扩写fp8/Nz/推理及arch22流水细节。

限制：未执行host Tiling，不能保证自动选择条件案例；L1/GM三环与softmax环的完整覆写安全证明尚未闭合，正文明确不由“无回执”推出源码存在竞态，也不由测试未失败推出安全。数学对拍不模拟half P舍入；API样例D128不等于正文条件案例D256。无NPU性能结果。全书最终复核保留这些边界，不可宣称全书完成。
