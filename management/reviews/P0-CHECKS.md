# P0 管理者并行检查（2026-10-09）

## 验证基础设施

已修复 scripts/check-source.mjs：识别标准脚注、旧列表脚注、多行脚注和来源标签；花括号展开逐项检查；通配必须匹配完整模式；输出实际引用数量，并注明不验证论断正确性。
回归测试：node --test scripts/check-source.test.mjs，2项通过。
首次严格扫描：42文件、235条引用、297条展开路径模式；发现 ch24 两个漏写 .md 后缀的路径。已按实际文件修复，npm run verify 通过（日志 /tmp/ascend-book-p0-verify.log）。

## 第16章独立证据抽查

- matmul_basic_api_high_performance/README.md 明确支持 A2/A3（CANN>=9.0.0）和950PR/DT（>=9.1.0），这些是仓内样例要求，不代表全平台通用兼容矩阵。
- 同目录实现文件名为 `mmad.asc`。Compute 第502–523行：首个K块 cmatrixInitVal=true，其余累加；unitFlag 中间2、最后3。CopyOut第526–543行：Fixpipe直接写GM，float累加结果F322F16，不经过UB。
- 同文件第576–598行：固定8192三维，baseK=64/baseN=256，2201 baseM=128/stepKa=8/24 blocks，3510 baseM=256/stepKa=4/32 blocks；不得混合架构参数。
- 教程04_matmul_basic README对应高阶API及Notebook，基础API最佳实践对应显式流水。正文应解释两者学习顺序，而非当成同一套代码。
- bank_conflict_nd2nz README限定8192×8192 half，2201 48 blocks、3510 64 blocks，UB tile 144×128，尾块128行，dstNzC0Stride 从144改145。注意内部padding不等于改变输出紧凑NZ布局。

## 后续高风险提纲

ch17 旧提纲把“中间结果不出AI Core”“共享UB交接”泛化到A2/A3/950。需要沿具体架构分支核查实际融合样例，不得从融合名称推断没有GM中转。

## 后端验证预备

已实际编译运行PTO CPU GEMM，详见 management/validation/PTO-CPU-GEMM.md；后续ch24可引用执行记录，不得作为NPU性能。

## 第11章管理者直接修复

- 依据asc_950_feature_guide.md第27行与bank_conflict_3510/README.md第8–10行，修复正文、Mermaid、SVG及来源说明中“8组×16KB”漏掉每组2个bank的问题。
- 依据runtime/include/external/acl/acl_rt.h第1642–1650行设备同步声明，修复CUDA迁移表和SVG把设备级等待映射成流级等待的问题，补充同步范围脚注。
- 此处为独立文件修复，不与pi正在编辑的第16章冲突。

## 规范同步

经理已把验收字数口径同步到STYLEGUIDE，并修正README仍要求行内引用的旧说明，链接当前总计划与验收标准。历史里程碑不改写为本轮已验收。
