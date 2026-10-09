# 第16章证据账本（CH16-EVIDENCE）

> 2026-10-09 采集（基线：management/SOURCE-BASELINE.md 所记各仓 HEAD）。所有行号已在 `mmad.asc`/README 原文亲验；「证据类型」：S=源码直接事实、D=官方文档陈述、A=作者推导（须标注）。
> 架构缩写：2201=Atlas A2/A3 系（dav-2201）、3510=Ascend 950PR/DT（dav-3510）。

## 主要锚点（文件级，5 组）

| # | 锚点文件 | 角色 |
|---|---|---|
| A1 | `asc-devkit/examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_high_performance/{README.md,matmul.asc,matmul.h}` | 高阶 API 九级优化阶梯（Case 0-8），性能数据主来源 |
| A2 | `asc-devkit/examples/01_simd_cpp_api/05_best_practices/01_matrix_compute/matmul_basic_api_high_performance/{README.md,mmad.asc}` | 基础 API（Mmad）显式四级流水，还债②核心；645 行 |
| A3 | `asc-devkit/examples/01_simd_cpp_api/05_best_practices/04_memory_access/` 下四例各自的 `README.md` 与 `.asc`（`data_copy/data_copy.asc+README.md`、`bank_conflict_ub/{bank_conflict_ub.asc,README.md}`、`bank_conflict_3510/{bank_conflict.asc,README.md}`、`bank_conflict_nd2nz/{bank_conflict_nd2nz.asc,README.md}`） | 搬运收口四例（还债②收口） |
| A4 | `cann-learning-hub/tutorials/ascendc_operator_development/04_matmul_basic/`（04.02/04.03 notebook + answer/） | 教科书路线：逻辑位置体系、高阶 API 五步、TCubeTiling |
| A5 | `asc-devkit/docs/zh/api/SIMD-API/basic_api/cube_compute_ISASI/cube_compute_store/{Fixpipe_L0CToGM,L0C_memory_structure_intro}.md` + `asc-devkit/docs/zh/asc_950_feature_guide.md` | L0C/Fixpipe 机制与 950 差异 |

依赖补充：`asc-devkit/docs/zh/api/.../cube_compute_store/Fixpipe_L0CToL1.md`（NZ2DN 限制条目）、`ops-nn/matmul/`（§5 对照，仅目录级）。

## 提纲 × 证据对照

### §1 两条路线与数据流总图

- **学习顺序**：先教程（A4，高阶 API 五步：创建 Matmul 对象→REGIST_MADMUL_OBJ 初始化→SetTensorA/B/Bias→Iterate/IterateAll+GetTensorC→End）后性能样例（A1/A2）。**两者不是同一套代码**：教程面向 ascend910b1（A4 cell10 `msopgen gen -c ai_core-ascend910b1`），性能样例要求 A2/A3≥CANN 9.0.0、950≥9.1.0（A1/A2 README「产品及CANN版本」表）——正文须写明这是**仓内样例的版本要求，非全平台兼容矩阵**（经理 P0-CHECKS 提示）。
- **逻辑位置体系**（A4 04.02 cell1）：A1/B1/C1（整块，类比二级缓存）、A2/B2/C2（切分小块，类比一级缓存）、CO1/CO2（Cube Out）、VECCALC（临时）；A 矩阵数据流 GM→A2、GM→A1→A2、VECOUT→A1→A2。【D】
- **基础 API 数据流**（A2 README「数据流路径」图）：GM─MTE2 DataCopy→L1─MTE1 LoadData→L0A/L0B─Cube Mmad→L0C─Fixpipe→GM。【D+S】
- 与第 8 章图 8-2（MTE 四单元分工）衔接：ch08 已画单元级，本章画**带缓冲位与事件名的实例化版**。

### §2 高阶 API 九级阶梯（A1）

| Case | 机制（README 原文） | 关键参数/结果（A2 芯片 910B1，M=N=K=8192） |
|---|---|---|
| 0 单核基础 | baseM=baseN=baseK=64 | 759363.98μs，mac_ratio 18.7% |
| 1 单核 Tiling | base=[128,256,64]；**访存计算比** 96 vs 256 byte/cycle（(128×64×2+256×64×2)/512cycle） | 249467.08μs（3.04×） |
| 2 多核 2×12 | 24 核，singleM=4096/singleN=683/尾块 679 | 12541.22μs（60.55×），mte2 占比 81.2% 成瓶颈 |
| 3 多核 4×6 | 同 24 核不同切分 | 12283.84μs（61.82×） |
| 4 MDL 模板 | CFG_MDL，大包搬运减 MTE2 次数 | 5039.86μs（150.67×），mte1 占比升至 52% |
| 5 +L1Cache | depthA1=16, stepKa=8 用满 L1 | 4156.76μs（182.68×） |
| 6 +L2Cache | A 矩阵 M 轴切分（Process 循环 2 次） | 4088.36（185.74×） |
| 7 +常量 Tiling | `CONSTANT_CFG = GetCustomConstantCFG<...>()`，编译期算完，运行时免 Scalar | 4053.44（187.34×），scalar_ratio 26.4%→? |
| 8 +UnitFlag | 计算搬运并行 | **4012.44μs（189.25×），mac_ratio 86.4%** |

- **推荐 base 块**（A1 Case1 💡）：A2/A3 L0A=L0B=64KB、L0C=128KB；b16→[128,256,64]，b8→[128,256,128]。【D】
- **Cube 理论时间**（A1）：`M×N×K/(16×16×16×core×freq)`；A2：8192³/(16³×24×1.85GHz)=3022.92μs，对比 Case8 **aic_mac_time=3076.396μs** 误差 1.77%（注意：对比对象是 Cube 时间，不是 Task Duration 4012.44μs；mac_ratio=86.4% 是 Cube 时间占 AI Core 时间比例，**不等于峰值算力实现率**，官方 README 行文有混用，引用时须分开表述）；MTE2 理论 2672.42μs（HBM 1.8TB/s + L2 5TB/s 模型），Case8 实测误差 28.56%，归因 L2 实际 192MB + ND2NZ 场景 L2 带宽下降。【D，含推导模板】
- **950PR 对照表**（A1 尾节）：32 核、baseM=256、主频 1.65GHz；Case8=2558.155μs（428.68×），mac_ratio 99.7%、误差 0.30%。**两表不得混用**。
- matmul.asc 结构（S）：三分类 `MatmulKernel`（Case0-5，isMdl/isL1Cache 模板参）`MatmulKernelL2Cache`（Case6）`MatmulKernelMdlL2CacheConstant`（Case7/8，useUnitFlag 模板参，L64/76）；Tiling API `SetSingleShape/SetFixSplit`（L104-112）。

### §3 基础 API 显式流水（A2，还债②主菜）

- **四级流水**：DataCopyIn（GM→L1，Nd2Nz 随路）→ DataLoad（L1→L0）→ Compute（Mmad）→ CopyOut（Fixpipe L0C→GM）。【S，mmad.asc 函数名 L181/210/232/259】
- **Ping-Pong 双缓冲**：L1 与 L0 均 Ping/Pong（README「L1/L0 双缓冲」+ `a1LocalPing/Pong(TPosition::A1,...)`、`a2LocalPing/Pong(TPosition::A2,...)`）。【S+D】
- **同步体系：4 类 HardEvent**（MTE2_MTE1／MTE1_MTE2／MTE1_M／M_MTE1），按「正向=数据就绪、反向=缓冲释放」成对使用；flag 编号 0/1=A1 Ping/Pong、2/3=B1 Ping/Pong、L0 用 mte1DBFlag 0/1 交替。**反向预置共 6 个 flag 实例**（A1/B1 Ping-Pong 四个 MTE1_MTE2 + L0 Ping-Pong 两个 M_MTE1，mmad.asc L155-166），首次 WaitFlag 前不预置会死锁。【S+D】
- **Compute 细节**（mmad.asc L502-523 亲验）：尾块 curM/curN 区分；`cmatrixInitVal=(kBlockIdx==0)` 首块清累加器；`unitFlag=(kBlockIdx!=kLoopCount-1)?2:3` 中间块 2 末块 3。【S】
- **CopyOut**（L526-543 亲验）：`FixpipeParamsV220`，`quantPre=F322F16`（float 累加转 half 输出），**Fixpipe 直接写 GM，不经过 UB**；`unitFlag=3` 与末块 K 对齐。【S】
- **A1 搬入即转 NZ**（L348-357 亲验）：`Nd2NzParams`（ndNum=1/nValue/dValue/srcDValue=K/**dstNzC0Stride=baseM**/dstNzNStride=1）——GM 上的 ND 数据在进 L1 时由 MTE2 随路转 NZ，**这是「A/B 按 NZ 驻 L1」的机制真相：转格式发生在搬入侧，不是先搬 ND 再转换**。B 矩阵：**无运行时 isTrans 参数**——样例规格表的 isTrans=true 是问题语义（B 需转置参与计算），实现上是 DataCopyInB 走 `IS_B_TRANSPOSE` 编译期分支改变 Nd2Nz 的 nValue/dValue 与步长（L367-376），转置状态由输入布局与后续 LoadData 共同决定（详见 U2 补读）。【S，待 U2 补全】
- **架构参数分岔**（L576-598 亲验，禁止混写）：2201：baseM=128/stepKa=8/singleCoreN=1536/numBlocks=**24**；3510：baseM=256/stepKa=4/singleCoreN=1024/numBlocks=**32**；共同 baseK=64/baseN=256、M=K=N=8192。【S】

### §4 搬运收口四例（A3，还债②收口）

| 样例 | 架构 | 核心事实（README 亲验） |
|---|---|---|
| data_copy | A2/A3+950 | 四优化点：分块粒度／非对齐（DataCopy vs DataCopyPad）／重复搬运与 L2Cache 复用／多核同地址访问冲突规避；「不包含计算逻辑，纯观察 MTE2 行为」【D】 |
| bank_conflict_ub | **仅 A2/A3**（≥9.0.0；UB 192KB） | 8 scenario：无冲突/读读/读写/地址重叠；scenario4（同 bank，硬件优化）2389 cycles vs scenario5（读写冲突）3751——**同 bank 反而更快是硬件优化点**【D+S】 |
| bank_conflict_3510 | **仅 950**（UB 256KB） | **16 bank 组成 8 bank group**（每组 2 bank），每 bank 512 行×32B=**16KB**；18 位地址低位交织；读读冲突判据（原文照录）：「多个读操作同时访问同一个 bank，或两个以上读操作同时访问同一个 bank group」；A2 判据（原文）：「多个读操作同时访问同一个 bank group」。两判据并列陈述，不做方向性比较【D】 |
| bank_conflict_nd2nz | A2/A3+950 | 8192×8192 half→紧凑 NZ；**UB tile 144×128、尾块 128 行**；case1 `dstNzC0Stride=144`（=tileH，16 的倍数→8 个写落点全落同 bank group，单 copy 1 拍→8 拍）→ case2 改 **145**（tileH+1，多申请一行换 bank group 轮转）——**整个调优只动这一个参数**【D+S】 |

- 草稿及 ch11 的「8 组 × 16KB」**须精确化**：16 bank×16KB、8 组×(2 bank/组)、总 256KB；ch11 L92/L198 同样表述需在 P5 复核时统一。
- 2201 48 blocks / 3510 64 blocks（nd2nz README，经理抽查）；「内部 padding 不等于改变输出紧凑 NZ 布局」——正文写 case2 时须带这句，防止读者以为 145 改变了输出布局。

### §5 L0C 与 Fixpipe：驻留、随路与 950 直通（A5）

- **Fixpipe 族**（cube_compute_store/ 目录亲验）：`DataCopy_L0CToGM/L0CToL1/L0CToUB`、`Fixpipe_L0CToGM/L0CToUB`、`Fixpipe_L0CToL1`——L0C 出口远不止回 GM。【D，目录清单】
- **格式随路**（Fixpipe_L0CToL1.md L99 亲验）：`CO2Layout`：NZ（原样）/ROW_MAJOR（**NZ2ND**，默认）/COLUMN_MAJOR（**NZ2DN**）——**NZ2DN 仅 950PR/DT，A2/A3 不支持**；`isToUB` 指定目的为 UB。**草稿「Fixpipe NZ2DN」必须标注仅 950**。
- **L0C→UB 通路**：`Fixpipe_L0CToUB.md` 存在 + `dualDstCtrl/subBlockId 参数仅在 L0C→UB 通路下有效`（L124-125）——ch11 11.6「L0C→UB 直通」有据，**属 950 新通路**（950 feature guide 13 项表内）。A2 的 L0C 出口为 GM/L1（FixpipeParamsV220 路线，mmad.asc CopyOut 即证）。【D+S】
- **L0C 驻留**：A2 L0C=128KB（A1 Case1 💡），950 更大（待查 L0C_memory_structure_intro 精确值——**未解问题 U3**）。

### §6 ops-nn 真仓对照（§轻导览）

`ops-nn/matmul/` 34 个条目（gemm/gemm_v2/gemm_v3/mat_mul_v3/batch_matmul_quant/matmul_compress/fused_* 等）——只做目录级族谱导览 + 指出「库算子=第 13 章四件套+本章机制」的对应，**不逐库解剖**（P1 时间盒）。

## 草稿核实结论（ch16-matmul-cube.md 现存 TODO 逐条）

| 草稿断言 | 核实 | 修正 |
|---|---|---|
| GM→L1→L0A/B→Cube→L0C→UB/GM | ✓（A2/A5），但「→UB」**仅 950 直通**；A2 走 GM/L1 | 标架构 |
| A/B 按 NZ 驻 L1（第8章8.3） | ✓机制在**搬入侧随路 Nd2Nz**（mmad.asc L348），非先搬后转 | 措辞改「搬入即转」 |
| 双缓冲流水重叠 | ✓ L1/L0 双 Ping-Pong + 4 类 HardEvent（反向预置 6 个 flag 实例） | 补反向同步预置死锁细节 |
| L0C 复用（950 L0C→UB 直通，第11章11.6） | ✓ ch11 L190/L252 有据 | 补 Fixpipe 参数 dualDstCtrl 仅 UB 通路有效 |
| Fixpipe NZ2DN | ✓ 但**仅 950**（Fixpipe_L0CToL1.md L99「仅支持 Ascend 950PR/950DT」） | 标架构 |
| bank_conflict_ub/3510/nd2nz 三例 | ✓；「8 组×16KB」须改「16 bank×16KB 组成 8 组」 | 精确化 |
| nd2nz 单参数 case1→2 | ✓ 144→145（=tileH→tileH+1） | 补 8 拍机理与「padding≠改输出布局」 |
| data_copy 四优化点 | ✓ 与 README 优化点 1-4 一一对应 | 无修正 |

## 未解问题 → 已全部解决（2026-10-09 补读）

- ~~U1~~ ✓ `matmul.h` L257 `GetCustomConstantCFG()` 返回 `MatmulApiStaticTiling`（编译期常量 Tiling 结构）；L289 `constexpr static auto CONSTANT_CFG = GetCustomConstantCFG<...>`；类模板 `<uint32_t singleN, ..., bool isSplit,isMdl,isL1Cache,isL2Cache>`（L425-427）编译期选路；常量区 L27-44（M=N=K=8192/SINGLE_M=2048/L2CACHE=1024/BASE_N=256/BASE_K=64）。【S】
- ~~U2~~ ✓ DataLoadA（L396-427）：2201 用 `LoadData3DParamsV2`（l1H/l1W/channelSize/kExtension/mExtension），3510 用 `LoadData2DParamsV2`（mStep/kStep/srcStride/dstStride，按 CUBE_BLOCK 粒度）——**两代 API 形态完全不同**。DataLoadB（L430-495）：`IS_B_TRANSPOSE=true`（gen_data.py L43 已物理转置）直接按块搬；false 时 2201 `LoadData3D.enTranspose=true`、3510 `LoadData2D.ifTranspose=true` 随路转置。gmOffsetB 按 IS_B_TRANSPOSE 二分（L282/318）。【S】
- ~~U3~~ ✓ L0C bank 结构（L0C_memory_structure_intro.md）：通用 128KB=16 bank×8KB（128 行×64B），950=256KB=16 bank×16KB（256 行×64B），均 16 bank group×1 bank——**与 UB 的 8 组×2 bank 结构不同**。【D】
- ~~U4~~ ✓ data_copy 数字：场景 tile 表（GM→UB [1,64]=128B/[64,64]=8192B/[64,1024]=131072B；GM→L1 [64,64]/[64,256]=32768B）；非对齐 N 12288→12287，尾块 blockLen 2048B→2022B 级、A2 场景3 215.82μs 基线 aiv_mte2_ratio 0.969；L2Cache：A2 192MB/950PR 128MB，整块工作集 301.99MB>容量 vs 四分片 75.50MB；同地址错开（offset addr）在 A2/A3 UB/L1 与 950 L1 场景收益明显。【D】
- ~~U5~~ ✓ 950 表与 A2 表同构（Case0-8 同名），差异仅参数与核数（32 vs 24）、baseM（256 vs 128）；matmul.asc L64/76 模板参 singleN/baseM/depthA1/stepKa 编译期注入。【S】

---

## 附录：R1 审查修订记录（2026-10-09，对应 reviews/CH16-R1.md）

- **UnitFlag 机制重写**：据 `mmad_compute_key_features/UnitFlag.md` 全文——512B 块状态位 0/1；unitFlag 2=执行后保持（写等 0 写后保持 0/读等 1 读后保持 1）、3=执行后翻转（写置 1/读置 0）；末次 Mmad 与 Fixpipe 可按块交错；L0C 单 CO1 缓冲靠「读后复位」复用。正文 16.3 阶段③′新增专节+对照表；删「Fixpipe 等 3/末块 flag=3」旧表述。
- **LoadDataB 分支表修正**：2201 默认路（IS_B_TRANSPOSE=true）=**LoadData2DParams 旧式直搬**；false 才 LoadData3DParamsV2+enTranspose；3510 两路均 2D V2（ifTranspose）。正文 16.3 表+16.4 速查表分 DataLoadA/B 两行。
- **Case 归因改按 README**：Case2→3=512B 对齐+同址冲突（L175/197-199），删「尾块均衡」推导；Case4 depthA1=4 ping/pong 各 2 基块+公式 depthA1/(stepM·stepKa)=2；Case5 16=基本块份数；常量 Tiling scalar 严格分架构（A2 1753.463→968.616/Case8 1026.069；950 765.125→426.398/412.29）。
- **数据修正**：data_copy 非对齐 blockLen=2046B（curCols=1023）、srcStride 22526/22522→22528 双值、A2 -21.6%/950 -1.8%；删单因因果。
- **新增可复演演算**：16.3 末「输出基块账本」（96 基块/12288 Mmad/16+32 大包/A1B1 单缓冲两架构均 128KB 形状互换/cLocal=128KB=A2 L0C 容量→baseM 上限反推）。
- **构建入口**：CMake（`-DCMAKE_ASC_ARCHITECTURES/-DSCENARIO_NUM/-DCMAKE_ASC_RUN_MODE=sim`，切场景清缓存），非 build.sh。
