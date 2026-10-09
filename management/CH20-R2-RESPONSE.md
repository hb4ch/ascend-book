# CH20-R2 退修响应（改前→改后对账）2026-10-10

正文 `docs/04-perf/ch20-opt-topics.md`（7,526 字/中文 5,100）；verify `validation/ch20-r2-verify.log` 0 FAIL；build 过（fn7/img1/bash块4）；脚本未改（R1 版复用，未重跑）。SVG 无数字未改，重渲染备案。

**1. 20.6 重写为可复制 bash**：改前＝编号散文＋虚构 `bash build.sh -v dav-2201 -n…`/`verify_result.sh`/「以 CMakeLists 为准」搪塞。改后＝四个 **bash 代码块**，命令逐字取自各 README（nd2nz L533-536：`cmake -DSCENARIO_NUM=1 -DCMAKE_ASC_ARCHITECTURES=dav-2201 ..;make -j;`＋gen_data/demo/verify_result.py 三连；data_copy L410-417：`SCENARIO_NUM/COPY_DST/ASC_ARCH` 三环境变量＋cmake 全参＋gen_data 带参＋`msopprof --ai-core=on --aic-metrics=L2Cache ./demo`（L449 原句）；FloorMod：`cmake -DCMAKE_ASC_RUN_MODE=npu -DSCENARIO_NUM=… -DCMAKE_ASC_ARCHITECTURES=dav-3510`＋verify_result.py；mmad_with_sparse L73-78：`cmake ..;make`；mxfp4 注释块全命令）。副本改 `WK=$(mktemp -d); cp -r <repo> "$WK/" && cd "$WK/<name>"`——目标必为新目录，源仓只读。删「搪塞」句。

**2. 标签**：改前自创「只用[源码]/[未运行]承 ACCEPTANCE」。改后：20.6 首段明写四标签体系并使用——三处代码块标 **[示意代码]**（20.1 Copy 段「bank_conflict_nd2nz.asc Copy 调用段未删节」；data_copy「process_data_copy() 节录关键 4 行」；case3「floor_mod_simt_contiguous 全函数未删节」），四个复现链标 **[需真机验证]＋「本书未运行」**；自创段删除。

**3. 脚注**：全部去 `/mnt/SATASSDEXT4/cann/`与本机前缀→repo 相对（`asc-devkit/...`）；「同目录」短名全展开为完整路径（asc/h 各自全路径）；oD「同目录上级 01_matrix…」逻辑错改**全路径** `examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_mxfp4_basic_api_high_performance/README.md`；LoadData_3D/bank-sim.log 亦全路径；oE 注明「本书侧非源仓」。

**4.** 误用①改「**C0Cols=8 时仅 8 个落点：A2 占 16 组中 8 组、950 占满 8 组**；C0Cols=16 时…」；「漏一处即越界/静默错位」拆分：漏扩 nzBuf/漏 pong pad→越界、漏 bank8 偏移→冲突依旧不越界、漏 MTE3 srcStride→数据污染非崩溃（各按真实后果）。

**5. unitFlag**：改前「=3 翻转」泛化。改后：=2 占用保持（K 迭代连续写）、=3 **Mmad 写后置 1/Fixpipe 读后置 0**；新增**多 K 约束**（前 kRound−1 用 2、末次 3；搬出量=Mmad 量，部分搬出可能异常须 SetFixPipeConfig 重置——L19/L42/L50 原文）；标明 **ISASI 版**、TensorAPI 不外推。

**6.** case2/3 索引式分写（`tid*8+i` vs `tid+i*blockDim`，README 总结 1024 形态；函数内 threadIdx.x 步进等价）；case0「反证」改「样例分析转录」；20.2 删「64 核分 8 组拥挤轻」臆测；「首轮应全命中」改「先录现象再究因」。

**7.** 稀疏：逻辑索引条目（K/2 个 uint2）与打包 uint8（K/4 个）分开计数（gen_uint2_zn_idx 句）；误用①改「host 脚本生成（gen_data.py）、kernel 只消费」消除与上文矛盾。

**8. U 号**：正文 4 处 U 标全部就地化（U6/U7/U8/U7→散文边界），“见 management 才知道”句保留一处指路（细节存 EVIDENCE）但边界已就地；「本书核验」重复段合并为一句。未扩新主题；报告级声明见本文件（正文片段级改动以上已列，不敢称全绿）。

字数 7,526/5,100 中文。只动 ch20 五文件内正文与响应；未提交。**待经理复审。**
