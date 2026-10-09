# CH27 验收记录
2026-10-10。经理完整读稿与R1/R2，独立核查example数据类型/无读回/释放遗漏、kernel ProcessBalance/PreloadPipeline与ComputeMm1/Mm2、vector输出和cube结果缓冲索引、golden实际路径。纠正flag3开局四次/循环一次/尾部四次混用，移除虚构Vec1回边，重绘同步图。
验证：CPU脚本已独立读取并重跑，ch27-manager-refcheck.log记录最大绝对差2.480e-4；后续脚本阈值收紧2e-3、覆盖记录见ch27-sfa-tnd-refcheck.log。文稿最终verify见ch27-release-verify.log，bash语法见ch27-release-bashn.log。真实站点两图ch27-manager-fig1/2.png已目检可读无遮挡。git diff --check通过。
范围：只追arch22一个条件分支，未运行NPU或源码构建；CPU参考不同于C++主例，golden覆写索引和以key取V的语义不推广全部分支，未覆盖-1/越界/空选择。Inner实现、soc宏映射及运行时二进制选路未闭合。研究期源仓pyc生成/删除和用户环境安装tensorflow违规已记入CH27-EVIDENCE，不因git干净抹除。历史报告错误以最终文稿为准。
