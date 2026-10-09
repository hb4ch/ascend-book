# PTO CPU GEMM 实际验证

日期：2026-10-09。执行者：Codex 项目经理。
源码：本地 pto-isa 固定快照（见 ../SOURCE-BASELINE.md），`demos/cpu/gemm_demo/gemm_demo.cpp`；原样编译，未修改源码。
环境：Linux，g++ 16.2.1 20260810，CMake 4.4.2；CMake自动选择C++23，定义 __CPU_SIM 和 __PTO_AUTO__。

```bash
cmake -S /mnt/SATASSDEXT4/cann/pto-isa/demos/cpu/gemm_demo \
  -B /tmp/ascend-book-pto-gemm -DCMAKE_BUILD_TYPE=Release
cmake --build /tmp/ascend-book-pto-gemm -j2
/tmp/ascend-book-pto-gemm/gemm_demo
```

配置、编译、运行成功。M=32、K=16、N=32，float，max_abs_diff=1.19209e-07（示例阈值1e-3）。
日志：pto-gemm-configure.log、pto-gemm-build.log、pto-gemm-run.log。
运行日志中的耗时与GFLOPS只描述本机CPU仿真过程，不能用作NPU性能数据或跨架构性能比较。
文档提示：getting-started_zh.md 末尾仍提及已不存在的 tests/cpu/demos，实际示例在 demos/cpu；写作应使用已验证路径。
