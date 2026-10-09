# 附录A验收
2026-10-10，经理全文/命令审查通过。核对asc-devkit quick_start、PTO GEMM CMakeLists和既有实测日志、CH27对拍脚本导入依赖。删除无据驱动通配安装与镜像推荐，按纯阅读/CPU数学、PTO CPU-SIM、CANN工具链、真机分流；GEMM给源码外构建命令，限定已测工具链和单例结果。
本轮未安装或重新执行设备示例；GEMM结果沿用已留痕验证，不作为NPU性能。安装配套以所选版本指南为准，不宣称当前镜像可达。
验证appa-manager-verify.log真实exit0，git diff --check通过；分流表appa-r1-tblA0.png和修正后命令appa-manager-gemm.png均实际目检，文本完整可读。附录B活动内容排除提交。
