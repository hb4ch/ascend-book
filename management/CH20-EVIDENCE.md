# CH20 证据表（CH20-EVIDENCE）2026-10-09 补闭版

固定源只读。基线 commit：asc-devkit `28e7aba2f62e0940e4240442fa3acb794ae4e4d2`、runtime `681ef7610df13c8128982901142a2c869ddbb53e`（SOURCE-BASELINE 2026-08-22）。**各样例仅标「支持版本」（nd2nz：950≥CANN 9.1.0、A2≥9.0.0；README L8-12），实际测量 CANN 版本未标，未知**。类型 S=源码/API 文档/D=样例实测表/B=博客经验断言。

## 一、文件级锚点（7，全路径）

| # | 路径（仓库内完整路径） | 角色 |
|---|---|---|
| A | `asc-devkit/examples/01_simd_cpp_api/05_best_practices/04_memory_access/bank_conflict_nd2nz/README.md` | 决策①主案例：shape **8192×8192 half**（L35-40），仅 case1/2；A2 表 L205-214、**950 表 L371-380 与 L445-455**；950=**Reg 编程 `__simd_vf__`+StoreAlign**（L325 区），A2=Copy 路径 |
| A2 | `.../bank_conflict_nd2nz/bank_conflict_nd2nz.asc`（190 行） | 真码：Ping/Pong 四 buffer、`dstNzC0Stride=(SCENARIO==1)?tileH:tileH+1`（L168 区）、Copy 调用 L167-177、MTE3 回写 `srcStride=dstNzC0Stride−actualTileH`（L148-150）、950 S2 bank8 偏移（L55-70 注） |
| B | `.../04_memory_access/data_copy/README.md`＋`data_copy_ub.h` | 决策②：错序 L336-356 真码＋ub.h L104-106；**纯读 benchmark（仅 DataCopyPad GM→UB，无写回 tensor，ub.h L28/89-112）** |
| C | `.../04_memory_access/bank_conflict_ub/README.md`、`.../bank_conflict_3510/README.md` | 冲突分类；3510 拓扑 16 bank/8 group/512 行、**每 group 两读或一读一写** |
| D | `asc-devkit/include/basic_api/kernel_struct_data_copy.h` L414-427＋`asc-devkit/docs/zh/api/SIMD-API/basic_api/memory_vector_compute/data_move/Copy_UBToUB_mask_highdim_split.md` L82-90 | **Copy/CopyRepeatParams 契约**：dstStride uint16、单位 DataBlock（32B）、∈[0,65535]；dstRepeatSize∈[0,4095] |
| E | `asc-devkit/docs/zh/api/SIMD-API/basic_api/cube_compute_ISASI/cube_compute_load/LoadDataWithSparse.md`＋`.../mmad_compute/MmadWithSparse.md`＋样例 `asc-devkit/examples/01_simd_cpp_api/03_basic_api/03_matrix_compute/mmad_with_sparse/mmad_with_sparse.asc` | 稀疏全链（S+真调用） |
| F | `asc-devkit/docs/zh/guide/operator_practice/simd_operator_impl/matrix_advanced_api/feature_scenarios/mx_matmul_scenario.md`＋`.../01_matrix_compute/matmul_mxfp4_basic_api_high_performance/README.md`＋`.../docs/zh/api/SIMT-API/math_functions/fp8_type/fp8_data_type_intro.md`＋`asc_950_feature_guide.md` | MX/FP8 权威表 |

## 二、决策①nd2nz bank stride（补闭后）

- **shape/切分**：8192² half；A2=6 行×8 列=48 block、950=8×8=64 block（A L44）；tile 144×128；**8192=56×144+128→57 个行 tile，尾块 actualTileH=128**（L44 原文「通过 actualTileH 处理尾块」；asc L119）。
- **两平台双表（源文，测量版本未知）**：
  - A2：case1 vec 47.790→case2 **7.133μs（6.70×）**，Task 151.42→144.00，mte2 113.856→115.405。
  - 950：case1 vec 45.25→case2 **9.14μss（~4.95×，A L380 原文倍数）**，Task 141.691→140.403，mte3 104.571→116.921。**两平台实现不同**：A2 走 `ComputeTileNd2nzWithCopy`（Copy），950 走 `ComputeTileWithRegVF`（Reg LoadAlign/StoreAlign，VEC_LOAD/VEC_STORE 子流水，**非 MTE**——A L373-377 ⚠️框原文：「常规 MTE 类 bank-conflict 计数器看不到」）。
- **145 机理两平台原文**：A2「144=16 整数倍→同 group 8 拍」；950「**145=16×9+1，物理 bank 索引+1，8 落点=bank8..15（因 nzBuf 起步 bank8），分属 8 group**」——950 S2 另有 **nzBuf 起始偏移 256B 到 bank8** 使 V_LOAD(bank0-7)/V_STORE(bank8-15) 不相交（asc L55-60 注＋A「补充」节）。
- **Copy 参数契约（D 真码）**：`CopyRepeatParams{dstStride,srcStride,dstRepeatSize,srcRepeatSize}` 全 uint16；**dstStride 单位=DataBlock(32B)、∈[0,65535]**（Copy_UBToUB L88）；样例 `copyParams.dstStride=dstNzC0Stride; srcStride=1; dstRepeatSize=1; srcRepeatSize=tileW/C0`（asc L167-171）；Copy 寻址 `nzBuf[k*vecLenDbs*dstNzC0Stride*C0_ELEMS]`。
- **stride 变更的连带核验（纯数学，`validation/ch20-bank-sim.{py,log}` 扩核）**：
  - UB 写覆盖：列 k∈0..7 最大偏移 `7×stride+(actualTileH−1)`——stride144 需 1136≤1152✓、stride145 需 1143≤1160✓（尾块 128 亦安全）。
  **GM 读回跳 padding**：`outParams.srcStride=dstNzC0Stride−actualTileH`（asc L148）→非尾块 0/1、尾块 16/17——**stride=145 时非尾块也跳 1 db**，GM 侧 `dstStride=totalM−actualTileH`、`dstBlockOffset=tileRowStart+(tileColStart/C0)×totalM`，末行 56×144+128=8192=totalM 边界闭合✓。**上述为地址算术自洽，非硬件行为证明**。
- **UB 占用（A 原文）**：单 buffer nz 1152→1160 db（+256B）；**双缓冲总账 S1=147456B/144KB、S2=148480B≈145KB（含 2×256B bank8 偏移）<256KB**——**256B 是每 nz buffer 的 padding，总计含两处**；回答「单 buffer 还是总分配：两者皆有陈述，总约束按 145KB 核」。
- **风险**：nzBuf 越界须多申请一行＋950 额外 bank8 偏移常量；数据值不变 verify 不变（A 未单列 verify 差异，U5）。
- **不可支持**：倍数外推他 shape；Task 差额（6.7/4.4μs）归因；950 case1↔A2 case1 跨表比较（实现与核数均不同 48/64）。

## 三、决策②data_copy 错序与 L2（补闭后）

- **性质限定（B 真码）**：场景 7/8 为**只读 benchmark**——`KernelDataCopyPadGm2Ub` 仅 `srcGlobal.SetGlobalBuffer`＋DataCopyPad 入 UB，**无输出/写回 tensor**（ub.h L28、L89-112）。故「无正确性影响」精确表述：**纯读序置换、零数据依赖、无写侧，正确性不可触碰**；非「对任意算子安全」的推广。
- **置换良构前提（ub.h L104-106 真码）**：`blockGroupStart=(mBlockIdx/numBlocks)*numBlocks; cur=blockGroupStart+(mBlockIdx+blockIdx)%numBlocks`——组内置换要求 **fullMBlockCount 为 numBlocks 整数倍**（场景：A2 6144/128=48=blk、950 8192/128=64=blk✓）；**numBlocks>1**（mod 非零）；每核仍遍历全部组→覆盖不变。若 fullMBlockCount%numBlocks≠0 需另行论证（样例未及，U6）。
- **精确相对变化**：A2 case7→8 Task 539.42→328.88μs=**−39.05%**（mte2 474.717→307.380=−35.25%）；950 342.29→335.64=**−1.94%**——同改动跨平台收益差 20 倍，**统计显著性无重复采样数据，只陈述两点单值差**。
- **L2**：命中率公式两平台不同（B L303 原文）；整块 0.005%/0.35% vs 切4 75.00%/66.64%；Task 828.06→365.74（A2）。**工作集 301.99MB vs L2 192MB(A2)/128MB(950PR)**——「写替换致低命中」为 B 解释。
- 非对齐：12288→12287 尾块 blockLen 变化（B L179-187）；粒度三档表（564.84/233.54/215.82，+148.3%/+170.5% 为表值）。

## 四、决策③指令选择（改用真码/API，博客降为线索）

- **博客 D 只作导航**；能力逐条回源：
  - unitflag 512B 流水：`matmul_basic_api_high_performance/README.md` L236-238（S/D）。
  - Fixpipe 随路量化：ch16 已证链（FixpipeParamsC310 quantPre 等）——引用不重述。
  - LoadDataWithTranspose/3DV2：`asc-devkit/docs/zh/api/SIMD-API/basic_api/cube_compute_ISASI/cube_compute_load/`（存在性已核，参数未全读 U7）。
- **博客数字（30%/2–4×/5–10×/10–20%）不入选正文**，仅存档本节。

## 五、稀疏全链（E，S 级＋真调用）

- **语义**：**4:2 结构化稀疏**（MmadWithSparse.md L31 原文「连续 4 个值最多 2 非零」）——**不是含糊的「2:4」以外变体；真实编码=4 选 2 索引**。
- **dtype（真码）**：`LoadDataWithSparse<T=int8_t,U=uint8_t>`（L50 enable_if）；dst=int8 L0B(B2)、src=int8 L1(B1)、**idx uint8 L1，分形 128B=16×32×2bit**（L69-71）；A 矩阵 L0A Zz int8、B 稠密化后 Zn int8（MmadWithSparse 表 L47-48）；**A 全尺寸入、计算中经 idx 稠密化；B 须用户预先稠密化＋索引在稠密化时生成**（L33 原文）。
- **uint2 打包**：每 uint8 装 4 个 uint2 索引、**逆序排布**（LoadDataWithSparse L39 例）；选择算法=MmadWithSparse L58-82 4 选 2 表。
- **真调用链（mmad_with_sparse.asc）**：host idx(GM uint8)→`DataCopy`入 B1（L77-81，`bSize/4`）→`SplitB`：`LoadDataWithSparse(b2,b1,idxB1,loadDataParams)`（L109，repeatTimes=kBlocks*nBlocks/2）→`MmadWithSparse(c,a2,b2,{m,n,k,false,0,...})`（L67）。**「专用 buffer」确切含义=Cube 内置索引 buffer，由 LoadDataWithSparse 填充、MmadWithSparse 消费，中间无用户可见地址**——执行链如上四步，非一词带过。
- **约束**：A2/A3 only（950 支持行未见，U8）；idx 布局=小 n 大 Z 与 B 同形。
- **不可支持**：稀疏度-收益曲线；950 路径；fp16 稀疏（dtype 表仅 int8）。

## 六、MX/FP8 量化（F，S 级）

- **FP8 不止 e4m3**：SIMT 侧三种 `float8_e4m3_t/float8_e5m2_t/hifloat8_t`（fp8_data_type_intro L3-8）；**MxMatmul 支持表（mx_matmul_scenario 表 1 原文）**：MXFP8=e5m2 **或** e4m3fn、MXFP4=e1m2 **或** e2m1（fp4x2 打包），scale 均 `fp8_e8m0_t`、Group=32——**博客只列 e4m3 系不全，以本表为准**。
- **压缩比自算（假设透明）**：对照 fp16=2B/elem。MXFP8：1B+（1/32）B scale≈1.031B→**省 48.4%**；MXFP4：0.5B+1/32≈0.531B→**省 73.4%**——与博客「约50%/75%」同量级但**本算不含 packing 对齐/scaleK 偶数约束的额外空间**（fp4x2 每字节 2 元素→K 须偶，matmul_mxfp4 README L62；scaleK=align_even(ceil(K/32)，2B 连续对齐 L62-63）。**正文引用须带假设句**。
- **scale 流水约束（真码级）**：matmul_mxfp4 README L67「A/B 与 scaleA/scaleB **必须按相同 K block 节奏进入计算流水**，否则 Cube 侧拿不到匹配缩放」——**即片内流水同步要求仍在**；「无需同步」仅指传统 per-group 的 AIC/AIV 两核协同被片内随路取代（blog 表述，架构机制=950 Mx 指令，A2 无）。**预量化/scale 生成在数据准备侧**（gen_data.py，host/离线），kernel 内无生成步骤。
- 版本：MxMatmul/量化场景**仅 950PR/DT**（mx_matmul_scenario L61 原文＋asc_mmad_mx 支持表）。

## 七、SIMD/SIMT 本章新增决策依据

- **950 Reg 编程 bank 规避**：`Reg::LoadAlign→VEC_LOAD/StoreAlign→VEC_STORE` 子流水（A ⚠️框）——SIMD RegAPI 下冲突藏于 vec 流水，**工具观测须 vec 周期数非 MTE 计数**（新工具知）；bank8 起始偏移技巧（asc L55-60）。
- 决策依据新增：**「Reg 路径 vs Copy 路径」选型本身**是 3510 上 Nd2Nz 的第一分叉（asc L136-139 `#if NPU_ARCH`），先于 bank 优化——ch20 可作 SIMD 内部层次化案例（A2 Copy→950 Reg），**不回指了事**。

## 八、未证项/边界（重整）

U1 msopprof csv 生成器不在仓；U2 A/B「稠密化/索引生成」host 算法细节未逐行（仅引 MmadWithSparse L33 与 4 选 2 表）；U3 各样例测量 CANN 版本；U4 3510 样例（bank_conflict_3510）场景未逐条；U5 nd2nz verify 是否两 case 各自通过未单列（样例未声明差异）；U6 data_copy 错序在 fullMBlockCount 非 numBlocks 倍数时的行为；U7 LoadData3D/Transpose 参数未全读；U8 MmadWithSparse 950 支持行；U9 LoadDataWithSparse idx 的 B1 容量上限。

## 九、复现（承 19.5 工作流；可写工作副本、独立 build-caseN、不在源仓构建）

nd2nz：`-DSCENARIO_NUM={1,2}`×`-DCMAKE_ASC_ARCHITECTURES={dav-2201,dav-3510}` 四组合；data_copy：`SCENARIO_NUM`+`COPY_DST`；mmad_with_sparse/mxfp4：各 README 编译节。依赖=CANN 套件（950≥9.1.0）。本书未运行。
