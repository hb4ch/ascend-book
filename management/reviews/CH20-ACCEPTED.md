# CH20 最终验收

2026-10-09，通过源码与文稿审查，未NPU编译/运行/实测。本记录优先于历史研究稿、报告及R1–R3响应；这些文件保留评审过程，不是最终事实来源。

经理独立回源核查ND2NZ的144/145列距、A2/950分支、bank8/pong偏移、双缓冲容量、整块/尾块和MTE3跳距；data_copy原始性能表、L2两平台公式、只读benchmark及组内置换前提；FloorMod索引与性能数据；稀疏API/数据准备、MX支持格式、UnitFlag置位和搬出范围。修复源文之外的传统量化两次往返/MX免同步泛化、数字和语义错误。

五段复现命令保持gen_data/demo/verify在同一build目录；来源README/CMake与nd2nz实际相对input/output访问已核。只做bash -n语法检查，不能等同NPU编译。SVG去除GM/L2共用UB bank模型的错误，并经rsvg-convert实际查看，文字可读。

验证日志：ch20-release-verify.log（构建/链接/来源/术语/字数），ch20-manager-calc.log（Python地址和算术），ch20-manager-bashn.log（5段语法）；git diff --check。路径校验不是事实验证。

约5.3k中文低于8k目标，接受当前覆盖：三个具体访问优化案例、地址与容量约束、平台分账、性能口径、反例、指令/低比特边界和复现链。没有为凑字重写前章Cube、融合和分析工具；LoadData3D v2Pro与950 Reg逐指令细节未展开，已就地说明。

限制：无NPU精度/性能验证；源文测量CANN版本未知；纯数学脚本不能证明bank周期、同步安全或性能因果；MX和稀疏没有本书实测收益；所有推广需按平台/shape重新核查。第21章未验收、不纳入本章提交。
