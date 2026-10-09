# CH18 证据表（CH18-EVIDENCE）

> 2026-10-09。任务 CH18-RESEARCH.md。全部行号亲验自本地快照（SOURCE-BASELINE 同批）；类型 S=源码/D=文档/推=推导；平台列严守 A2(arch22)/950PR(arch35) 区分；未证条件集中 §五。只读研究。

## 一、文件级锚点（5＋3 辅）

| # | 文件（ops-transformer/attention/ 下） | 行数 | 角色 |
|---|---|---|---|
| A | `flash_attention_score/op_kernel/arch35/flash_attention_score_kernel_train.h` | 579 | **四级软件流水主循环**（训练/前向） |
| B | `flash_attention_score/op_kernel/arch35/flash_attention_noquant_kernel_base.h` | 816 | Kernel 基类：缓冲策略/跨核同步枚举/编译期分岔 |
| C | `flash_attention_score/op_kernel/arch35/flash_attention_noquant_block_vec_base.h` | 2420 | Vec1/Vec2 全部向量侧实现 |
| D | `common/op_kernel/arch35/vf/vf_flashupdate_new.h` | 735 | **online 重缩放 VF 真码**（FlashUpdateNew 系） |
| E | `flash_attention_score/docs/FA算子设计介绍.md` | 281 | 官方设计文档：配比/流水/多模板（D 级） |
| a1 | `.../op_kernel/arch22/`（8 文件，如 flash_attention_score_s1s2_bn2gs1s2_b.h） | — | A2 世代实现（对照用，未深读→U4） |
| a2 | `.../op_host/flash_attention_score_tiling.cpp`＋`common/.../flash_attention_score_tiling_regbase_arch35.h` | 441+ | host tiling（arch35 regbase，值未全录→U5） |
| a3 | `.../examples/test_aclnn_flash_attention_score{,_v2_fp32,_varlen_v4_fp32}.cpp`；仓根 `build.sh` | — | 调用样例与构建入口 |

## 二、关键机制证据

| # | 论断 | 位置 | 类型 | 平台/限制 |
|---|---|---|---|---|
| E1 | **四级软件流水**：主循环对每 s2 迭代依次 `IterateBmm1(AIC)→ProcessVec1(AIV)→IterateBmm2(AIC)→ProcessVec2(AIV)`，用 `taskId` 与 `runInfo[4]` 环（`taskId&3/(taskId+1)&3/...`）错相三拍启动；`notLastThreeLoop/notLastTwoLoop/notLast` 逐级收敛收尾 | A L160-330（尤其 L302-341） | S | 训练模板 `FlashAttentionScoreKernelTrain`；前 3 拍为流水填充 |
| E2 | **AIC/AIV 分工**：同一循环体 `if ASCEND_IS_AIC/AIV` 各执 2 级；Cube 侧只发 mm1/mm2，Vector 侧只做 softmax/P 与更新 | A L304-341；B L63 基类 `CubeBlockType/VecBlockType` 双策略类 | S | 两代同构（arch22 为旧 API 世代，结构对照 U4） |
| E3 | **缓冲策略编译期选型**：`BuffersPolicy3buff<GM,CROSS_CORE_SYNC_FORWARD> bmm2ResGmBuffers`（mm2 直写 GM 三缓冲）、`BuffersPolicyDB<UB,CROSS_CORE_SYNC_BOTH> bmm1Buffers`、`bmm2Write2Ub` 常量分岔 `if constexpr` | B L130-135、L286-291 | S | 950 arch35；A2 无此 regbase 套件 |
| E4 | **跨核同步原语**：`CrossCoreWaitFlag<SYNC_MODE,PIPE_S>(15)`（Init 段）、Buffer 携带 `SyncType` 自动 `Wait/SetCrossCore`（如 `bmm1ResBuf.WaitCrossCore()/SetCrossCore()`）；`WaitFlag<HardEvent::MTE3_V>` 单元内自同步 | B L202；C L307-315（ProcessVec1 首行 WaitCrossCore）、L1324；C L394 附近 V_MTE3 | S | flag id 15 语义未见文档→U6 |
| E5 | **Vec1＝softmax+P 生成**：入口 `WaitCrossCore`→按 `useDn/Nz` 分派；`ProcessVec1Vf<…,GT_0_AND_LTE_256/GT_256_AND_LTE_512,…>` 按 s2 区间模板特化；`sumUb/maxUb` 为 **half**（`softmaxSumBuf[runInfo.multiCoreIdxMod3]`）；VF 内 Reg 级 max/exp/sum | C L307-326、L337-359 区间特化、L346-347 half buffer | S | half 精度设计意图未注→U7；s2>512 分支未录 |
| E6 | **P 写 L1（CV 交接①）**：`stage1CastTensor`（INPUT_T=half）经 `DataCopy` 入 `mm2AL1Tensor`，偏移含 `subBlockIdx*vec1HalfS1BaseSize*…`——**双 AIV 各写半块、直接落 L1 供 mm2 的 A 矩阵** | C L391-399、L614-629 | S | P 布局按 64 对齐 s2（`(s2RealSize+63)>>6<<6`） |
| E7 | **Vec2＝online 重缩放**：`ProcessVec2` L1320；`s2LoopCount==0` 首块直接拷；否则 `FlashUpdateNew(vec2ResUb, mmRes, vec2ResUb, expUb,…)`——**dst=cur 复用同 buffer**，末块走另一重载（含输出 cast）；`s2≤128 且 !isRowInvalid` 走 `ProcessVec2NoGlobalUpdate` 短路（单 KV 块免全局重缩放） | C L1320-1420（关键 L1345-1347、L1390-1400） | S | isFp8 deScale 分支繁多，正文只讲主路 |
| E8 | **重缩放 VF 真码**：`FlashUpdateBasicVF(__ubuf__ dst/pre/cur/expMax/rowMax,…)`——RegTensor `vreg_input_pre/cur/exp_max/row_max`+`vreg_mul/add`：`out = pre·exp(max_pre−max_cur)+cur·…` 型递推，`REDUCE_SIZE=1`、`floatRepSize=64`、`dLoops=srcD/64` | D L182 起、L16-40 结构 | S | 完整指数式未抄全→U8；isUpdatePre 两版 |
| E9 | **softmaxMax/Sum 副产物输出**：`softmaxMaxGm/softmaxSumGm`（fp32），格式 `(B,N,Sq,8)` 或 TND `(T,N,8)`——LSE 可取 | vec_train L52-53、L112-113、L250-251 注释 | S | 8=按 8 对齐？未注→并入 U7 |
| E10 | **CV 配比与基本块（官方数值）**：CV 基本块≈512KB；Vector 块 fp32 8×1024；Cube 块 fp16 128×128；**nRatio=8 使 C:V 数据量 1:16（128×1024）**；「S1 方向开配比，S2 同长」；核内再切（Cube 32KB/L0 双缓、Vec 32KB） | E §3 L30-57、§5.1 L182-186 | D | 设计意图，非运行时测量 |
| E11 | **preload 次数架构差**：A2（C:V=1:2）Cube 双发 preload 2——「MTE2 耗时足以覆盖 Vector→奔 MTE2 bound」；**950PR/DT preload 3（三次 mm1 后才开 mm2）**，「优化启动段 CV 流水」 | E §4.2 L77-84 | D | 引用须注明设计目标而非实测 |
| E12 | **多模板体系**：按 shape 特征/输入布局/确定性/空 tensor/流水特化（例：`s1s2_bn2gs1s2_b`、`empty_tensor`、RCM 确定性模板）；TilingKey 模板选择 `flash_attention_score_template_tiling_key.h` | E §5；arch22/35 文件名清单；B/C `template_tiling_key.h` | S/D | 正文只导览不穷举 |
| E13 | **mask/pse/drop 挂点**：Vec1 内 `attenMaskUb/pseUb` 参与VF（前/后加由 pseType 定，README 公式两式）；dropMask 独立 TQue+index；`isRowInvalid`/`AA_INVALID_LINE_HIGH_PRECISION` 特化；`learnableSink`/prefix/padding 变长 | C L347-359 模板参、L334-341；vec_train L48-50；B L77-78 参数表 | S | mask 尾块逐分支未读全→U9 |
| E14 | **变长/TND 分核**：`splitCoreMode==1` 时 TND 正倒序循环（`varlenCycleCoreNums=2×coreNum`）或对称分核（halfN 上半顺序/下半镜像）——防长尾负载不均 | A L160-200 | S | 仅训练模板显式；推理路径未读→U10 |
| E15 | **推理/训练分野**：`isInfer` 模板参贯穿（RunInfo/ConstInfo `<isInfer>`）；`ProcessVec2NoGlobalUpdate` 仅推理+短 s2；infer 另有 `infer_flash_attention_comm_arch35.h` | B/C 全程模板参；C L1363-1376 | S | prefill/decode 产品矩阵未逐一核对→U11 |
| E16 | **产品支持**：950PR/DT✓、A3 训练✓、A2 训练✓、A2/A3 推理✗（README 表）；dtype 面含 BF16/F16/F32/F8E5M2/E4M3/HIFLOAT8 | `flash_attention_score/README.md` 头两表 | D | 推理场景走 `fused_infer_attention_score` 等独立算子（目录在列） |
| E17 | **构建/调用入口**：仓根 `build.sh`（RELEASE_TARGETS=ophost/opapi/opgraph/onnxplugin）；样例 `examples/test_aclnn_flash_attention_score{,_v2_fp32,_varlen_v4_fp32}.cpp` 走 aclnn C++ API；UT 目标另列 | build.sh L15；examples 三文件 | S | 无 NPU 侧运行记录→全书按「未实测」口径 |

## 三、性能数字现状

仓内**无统一性能表**（README/设计文档均无 us 级数据；`docs/*.md` 为接口文档）——ch18 性能节只能：①引 E10/E11 的结构性论述（不涉数值）；②标注「本书未实测，无 NPU」；③U12：如需数字须另寻来源（ascend 公开资料），**不得自造**。此前各章「不推导未经测量的加速比」纪律沿用。

## 四、未证清单（写作前闭/正文标注）

| # | 事项 | 处置建议 |
|---|---|---|
| U1 | bmm1 输出精度路径：C L48 `mmRes` half vs `stage1CastTensor INPUT_T`——mm1 累加 fp32→输出 half 的确切组合随模板参变化 | 读 `flash_attention_noquant_block_cube.h` IterateBmm1 的 Matmul 模板参后定稿；正文按「fp32 累加、P 以 INPUT_T 写 L1」表述并标注依模板 |
| U2 | FlashUpdateNew 完整指数式与末块重载差异 | 补读 D L100-180/L400+；正文给主路递推即可 |
| U3 | s2>512 的 Vec1 分支与 GT_256 上界来源 | 补读 C L360-470 |
| U4 | arch22（A2）世代结构差异深度（API 风格/流水同异） | 至少目录级+入口函数对照，正文声明「以 arch35 regbase 为讲解主线」 |
| U5 | tiling 关键数值（s1BaseSize/s2BaseSize 实际取值、nRatio 落点） | 读 `flash_attention_score_tiling_regbase_arch35.h` 常量；走查需要 |
| U6 | `CrossCoreWaitFlag<SYNC_MODE,PIPE_S>(15)` 的 15 与 SYNC_MODE 值 | grep common 定义处 |
| U7 | sum/max 以 half 存储的精度设计（舍入策略）与 (…,8) 尾维含义 | 谨慎表述「half 存储」+标 U |
| U8 | FlashUpdateBasicVF 完整指数式 | 补抄后入正文（唯一数值递推，值得全录） |
| U9 | mask 尾块/bool→u8 转换/前缀 sparse 细节 | 按需补读；正文给挂点即可 |
| U10 | 推理模板主循环差异（非 train 基类） | 定 `infer` Process 位置后补 |
| U11 | prefill/decode 产品矩阵（哪算子管 decode） | 以目录（fused_infer_attention_score 等）+README 界定，不深挖 |
| U12 | 性能数字来源 | 另找官方资料或留白 |

## 四′、收口补记（2026-10-09，任务 CH18-EVIDENCE-CLOSE；U1/U2/U5/U6/U7/U8/U9 处置）

| # | 结论（均附源证） | 状态 |
|---|---|---|
| U1 | **mm1 精度链闭**：`IterateBmm1Nd` 出口 `FixpipeParamsC310<CO2Layout::NZ>`＋**`quantPre=QuantMode_t::QF322F16_PRE`**（cube L1452/1466），且 **Vec0/Vec1 两次 Fixpipe 按 mSize 对半拆**（`s1RealSize>>1 对齐`）分别写两 AIV 的 `mmResUb`——fp32 累加→**fp16 存 UB**（`mmRes` half 与 C L48 一致）；dualDstCtl=0 单目标×2 次。**注意与 matmul_gelu 的 dualDst 直接拆分不同实现**。| ✅闭（残：fp8/int8 deq 分支不入主线） |
| U2 | **FlashUpdateNew 数学闭**：头注原文 `dstTensor = preTensor * expMaxTensor + curTensor`（vf L14）——**未归一化累计**；`FlashUpdateBasicVF` 逐指令：`Mul(vreg_mul, vreg_exp_max, vreg_input_pre)+Add(vreg_add, vreg_mul, vreg_input_cur)`，expMax 由 **vec1 侧 softmaxExpBuf[taskIdMod3] 三缓冲**跨级传递（C L167/2160-2162，256B=[64,1]）；`rowMax` 仅 isUpdatePre/fp8 变体用。**归一化除 l 在输出阶段（末块重载）**——未逐行定位除法点→残 U2′（非主线，正文表述「累计未归一化，输出时除 l」即可） | ✅闭（残 U2′） |
| U5 | **块尺寸=模板选择非定值**：TilingKey `S1TemplateType∈{16,64,128,256}`、`S2TemplateType∈{16,32,64,128,256,512}`、`DTemplateType…768`（template_tiling_key.h L44-46 UI_LIST）；`s1BaseSize=(uint32_t)s1TemplateType`（vec_base L55）、`vec1HalfS1BaseSize=s1BaseSize>>1`。**具体场景取值由 host tiling 决策**——正文走查须先声明「假定 S1=128/S2=128 模板」（常见支路，host 选择逻辑未逐支核实→残 U5′） | ✅闭（残 U5′） |
| U6 | **flag15=host 消息同步**：`SYNC_MODE=4`（base L124 常量）；`CrossCoreWaitFlag<4,PIPE_S>(15)` 注释原文「**wait kfc message**」——其后从 `__ssbuf__` 0 地址拷 `CVSharedParams`（L203-209）。**数据面同步不走此 flag**，全靠 Buffer 模板参 `SyncType`（CROSS_CORE_SYNC_FORWARD/BOTH）自动 Set/Wait | ✅闭 |
| U7 | **max/sum dtype**：VF softmax 路径 `sumUb/maxUb` 为 **half**（C L346-347 `LocalTensor<half>`）；但 `softmaxMaxGm/softmaxSumGm`GM 输出 **fp32**（vec_train L52-53）。**尾维 8**：`tndSoftmaxOut=1→(T,N,8)；=0→(B,N,Sq,8)`（vec_train L250-251 注释原文）——8 为按 8 对齐的每 query 标量槽位，**非 8 头**；half 中间值的舍入策略源码未注→残 U7′（正文按「中间 half/GM fp32」陈述） | ✅闭（残 U7′） |
| U8 | **递推式闭**（见 U2）：完整链=vec1 exp（按新 max）/corr 与 FlashUpdateNew 合成；**与 NumPy 对拍一致（fp64 误差 2.2e-16，`validation/ch18-online-softmax.{py,log}`）**——数学验证非 kernel 验证，正文标注 | ✅闭 |
| U9 | **mask 挂点确认**：`attenMaskUb/pseUb` 入 VF 模板参（C L347-359）；块级裁剪经 `s2LoopLimit`（train L296）；bool→u8 与尾块分支未逐条读——**保持挂点级陈述** | ➜非主线，正文标 U |

**新增锚点**：`flash_attention_noquant_block_cube.h` L1440-1470（Fixpipe 双拆精度链）；`template_tiling_key.h` L38-60（TPL 常量表）；base L124/L196-210（SYNC_MODE/kfc）。

## 五、可复演走查设计（供提纲直接采用）

**固定 shape 数值走查（微型可手算）**：S1=S2=4、D=2 → **Q/K/V 均 4×2 矩阵**、fp16 语义、无 mask；KV 按 2 分两块；演示①mm1 得 4×4 分数→②softmax 首块（s2 前 2）得 m0/l0/P0→③次块 online：m1=max(m0,rowmax)、l1=l0·e^(m0−m1)+…、P1 重缩放（E8 公式代入真数）→④mm2 加权——**每步 2×2 数字全手算**，对应代码挂点（E5/E7/E8）。主流水走查另配：s2Loop=0..3 的四级任务表（AIC1/AIV1/AIC2/AIV2 错拍），标「示意」。

**真实 shape 结构走查（不跑只推）**：B=1、N1=2、S1=S2=2048、D=128、fp16、A2 参数：CV 块 128×1024（E10）→s1 方向 2048/128=16 块×n2？核数分配、s2 循环 2048/1024=2 次 CV 交互？——**须 U5 tiling 值落实后定稿**，先按 E10 配比推演并标注。


## 六、R2 更正（2026-10-09，review CH18-R2；与前文冲突处以本节为准）

1. **GM 主路径无释放握手**：vec2 GM 版（L1625-1770）仅入口 `WaitCrossCore`（L1629），**无 `bmm2ResBuf.SetCrossCore()`**（尾部仅 `SetFlag<MTE3_V>` 后返回）；cube `IterateBmm2` GM 路径尾部 `outputBuf.SetCrossCore()`（L2220 区，就绪 id0），`WaitCrossCore` 仅 `bmm2Write2Ub` 分支（L2174-76/L1545）——**就绪单向；两侧均无 id1 调用**。 buffers_policy `Get()` 仅轮换 a/b/c，不自动 Set/Wait。级1 UB BOTH 两侧四调用齐（cube L1698/L1700＋vec L307/L601）＝真闭环——**此前「FORWARD 亦双向＝闭环」的表述作废**。
2. P 缓冲＝`l1PBuffers` 3buff（base L139/L362），vec1 尾 `SetCrossCore`（Nd L1292/Dn L406 区）就绪 id0；cube `mm2A.WaitCrossCore()`（L598）。释放同 GM：无回执，靠 3 深轮转，**充分性未完成分析**。
3. `isUpdatePre=true` 在 count==1 对 fp16 亦实例化（GM L1726/UB L1406），deScale 门控在 VF `if constexpr(INPUT_T…)`（vf_flashupdate_new.h）——非 fp8 专用。
4. vec2 GM 搬运事件实为 `Set<V_MTE2>/Wait<MTE2_V>` 对（V 消费）＋跨轮 `MTE3_V/MTE2_V` 守护；循环上界 `<vec2LoopLimit`。
5. `bmm2Write2Ub` 取值由 TilingKey 位段定，host 决策条件未逐条考证——主线按「假设 GM」表述。
