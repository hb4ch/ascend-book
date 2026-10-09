# CH25 验收记录
2026-10-10。经理完整读稿与两轮修订，亲核entry.py执行顺序、codegen_npu.cpp代码生成门控、UnaryCompute及layout静态判据。修正AICPU提前返回例外、最终tile配轴未证、尾块策略泛化和图标题重叠。以abs单例解释分层，接受按理解需要控制篇幅。
验证：ch25-release-verify.log完整流程exit0；ch25-release-bashn.log exit0；git diff --check通过。真实站点1280px视窗两图实际目检可读无遮挡，ch25-manager-fig1/2.png。Python语法检查见ch25-evidence-close-check.log；不等于PyPTO可编译运行。
边界：未执行PyPTO编译链、SIM或NPU；未生成主例IR，不推断tile(2,8)具体配轴/分块/模板选路；pybind完整衔接与CANN包是否分发PTO未核。源仓曾有pi生成ignored pycache的历史，git clean不证明ignored目录未写；后续检查输出定向/tmp，未清理源仓。历史证据和响应保留追溯，错误以最终正文及本记录为准。
