# CH18 主线缺口精确追踪（CH18-TRACE）

> 2026-10-09，对应 `tasks/CH18-FINAL-GAPS.md` 五点。**固定锚定模板**：arch35 非量化训练 **Nd 布局主路径**（`FANoQuantBlockVecBase/Cube`，非 fp8/int8、非 Nz/Dn 特化、无 pse/mask/drop 分支）。所有摘录为源码原文短引；仅代码证据，无数学替代。

## 1. 末块归一化：除 sum 与 cast 的真实符号

**入口**（vec_base L1420-1446 区，ProcessVec2 尾部）：

```cpp
LocalTensor<float> sumUb = this->softmaxSumBuf[runInfo.multiCoreIdxMod3].template Get<float>();
FlashUpdateLastNew<T, INPUT_T, OUTPUT_T, dTemplateAlign64, false, isMlaFullQuant>(
    vec2ResUb, mmRes, vec2ResUb, expUb, pScaleUb, sumUb, runInfo.vec2S1RealSize, ...);
...
LastDivNew<T, INPUT_T, OUTPUT_T, dTemplateAlign64, isMlaFullQuant>(
    vec2ResUb, vec2ResUb, sumUb, runInfo.vec2S1RealSize, (uint16_t)dTemplateAlign64, deSCaleVValue);
...
GetDerived()->CopyOutAttentionOut(runInfo, constInfo, vec2ResUb, 0, vec2CalcSize);
```

**FlashUpdateLastNew 契约**（vf_flashupdate_new.h L79-85）：
```cpp
static_assert(IsSameType<T, float>::value, "VF FlashUpdateLast, T must be float");
```
→ **dst/cur/expMax/sum 全程 fp32 视图**；末块先做一次带 exp 更新的 FlashUpdateLast（加末块贡献），**再** `LastDivNew` 做除法。

**LastDivNewVF 除法真码**（vf L397-438）：
```cpp
LoadAlign<T, MicroAPI::LoadDist::DIST_BRC_B32>(vreg_exp_sum, expSumUb + i * REDUCE_SIZE);  // REDUCE_SIZE=1 每行广播
LoadAlign(vreg_input_cur, curUb + i * d + j * floatRepSize);
...（fp8/int8 才有 Muls deScale；fp16 主路径无）
Div(vreg_div, vreg_add, vreg_exp_sum, preg_all);   // O = 累计和 / l
StoreAlign<T, ...>(dstUb + ..., vreg_div, preg_all);
```
即 **除 sum 显式为 `Div(vreg_div, vreg_add, vreg_exp_sum)`，原地写回 vec2ResUb**。`__ubuf__` 指针均 `(float*)`（`__ubuf__ float *dstUb/curUb/expSumUb`，LastDivNew L431-433）。

**dtype 链终答**：vec2ResUb 累计全程 **fp32**；`LastDivNew` 后仍 fp32；`CopyOutAttentionOut`（vec_train L305-313）一行转发 `Bmm2DataCopyOut`——**fp32→OUTPUT_T 的 cast 点在该函数内部/GM 写侧**（本次未逐行展开，非主线机制，正文表述「除 sum 后经输出通路写 GM」并如前标 U-t）。mm2 结果 `mmRes` 视图类型随 `bmm2Write2Ub`：GM 路径经 `mm2InBuf` 32KB 分层搬入（vec_base L2174 注释原文「bmm2结果在Gm，vector2开启多层循环，每次处理32KB」），进 VF 前**已转 fp32 视图**（`Get<T>` T=float 由 `static_assert` 锁定）。

## 2. 固定 shape 的 Tiling 选择链（结构走查，非自动选择已证）

**决策真码**（op_host/arch35/`flash_attention_score_tiling_basic.cpp` L55-124，条件链）：
```cpp
dBasicBlock = AlignUp(dSize + dSizeRope, D_TEMPLATE_SPLIT_SIZE);   // 64 分档
if (dBasicBlock > 256) → 768
...
} else if ((inputDtype==HIFLOAT8 && 无mask/pse/drop/rope)) { s1=128; s2=512; }
else if ((d==64 && dV==64 && s1%128==0 && ...))            { s1=128; s2=256; }   // dn
else if (dSize > 256) { fp32? 64 : 128; s2=128; }
else { s1TemplateType=ALIGNED_128; s2TemplateType=ALIGNED_128; s1BasicBlock=128; s2BasicBlock=128; }
```

**S1=S2=2048、D=128、fp16、无 pse/mask/drop/rope** 落入**最末 else → s1BasicBlock=s2BasicBlock=128**（`dBasicBlock=128≤256` 且非 hif8、非 d=64、非 d>256）。上游前提（L38 附近）：`inputDtypeBytes != FP32 && != FP8 && dBasicBlock<=256` 才进本函数特化链——**满足**。

**诚实声明**：以上是**读码推演的选择链**，未运行 host tiling 验证 2048² 实际 TilingKey；且 L44-52 另有 `s2Size>1024 && 无mask/pse/drop → s2=256` 先行分支（2048>1024 成立！）——**需确认该分支归属哪个场景类**（grep 示 L40-44 在某 override 内）。故正文采用**「假设已选定 s1=s2=128 模板参数」的结构走查**：入口=`GetTilingKey()` 编码 S1/S2/D Template 位段（template_tiling_key.h L44-46）→kernel `FlashAttentionNoQuantKernelBase` 静态参；约束=UI_LIST 枚举{16,64,128,256}/{16..512}；**不声称自动选择已证，s2=128/256 两支均注明**。

## 3. 数据面共享 buffer 同步矩阵（mm1→vec1→mm2→vec2）

**原语语义**（common/op_kernel/`buffer.h` L348-421，fa_base_matmul）：
- `WaitCrossCore`：**UB/GM**（AIC 生产→AIV 消费）：AIC `Wait<PIPE_FIX>(id1)`×2 等**两 AIV 释放**；AIV `Wait<PIPE_V>(id0)`（reuse 变体 MTE3）。**L1**（AIV 生产→AIC 消费）：AIC `Wait<PIPE_MTE1>(id0)`×2；AIV 若 BOTH 再 `Wait<PIPE_MTE3>(id1)` 等 AIC 用毕。
- `SetCrossCore` 对称：UB/GM AIC `Set<PIPE_FIX>(id0)`×2 生产就绪、AIV `Set<PIPE_V>(id1)`（消费毕释放）；L1 AIC BOTH 才 `Set<PIPE_MTE1>(id1)`×2、AIV `Set<PIPE_MTE3>(id0)`。
- `id0_`=正向（生产通知/消费等待）、`id1_`=反向（释放回执）——**成员注释原文** L416-417。

| # | buffer（声明处） | 介质/环 | 生产者→消费者 | 就绪同步 | 释放同步 | 环索引 |
|---|---|---|---|---|---|---|
| 1 | `bmm1Buffers` UB DB（base L130-131，`CROSS_CORE_SYNC_BOTH`） | UB×2 | AIC mm1 Fixpipe（`QF322F16_PRE`，cube L1440-1470）→ AIV ProcessVec1 | AIC `Set<PIPE_FIX>(id0)`；AIV `Wait<PIPE_V>(id0)`＝**vec1 首行 `bmm1ResBuf.WaitCrossCore()`（L307/315 前置）** | AIV `Set<PIPE_V>(id1)`＝**vec1 尾 `bmm1ResBuf.SetCrossCore()`（L601）**；AIC 下轮 `Wait<PIPE_FIX>(id1)`×2 | `taskIdMod2`（DB 双缓冲，runInfo L?`stage1Offset=taskIdMod2` L447） |
| 2 | `mm2A L1`（`outputBuf` 参数，`CROSS_CORE_SYNC_FORWARD`；实际 buffer 由 `l1BufferManager` 分配，cube L365/385 Init） | L1 | AIV vec1 `DataCopy(stage1Cast→mm2AL1Tensor，subBlockIdx 半块偏移)`（L391-399/614-629）→ AIC mm2 A 侧 | AIV `Set<PIPE_MTE3>(id0)`；AIC `Wait<PIPE_MTE1>(id0)`×2（**两 AIV 各写半，AIC 等齐**） | **FORWARD 无 AIC→AIV 回执**：AIC 用毕不通知，AIV 覆写前无 Wait id1——**复用安全性由 1:16 配比下 AIC 消费先于 AIV 下轮生产保证（设计约定，未见断言）→标 U-t′** | vec1HalfS1BaseSize 偏移区分半块，无环（每 CV 块新分配经 manager） |
| 3 | `bmm2ResGmBuffers`×3（base L286-287，GM `CROSS_CORE_SYNC_FORWARD`；`bmm2Write2Ub=false` 主路径） | GM×3 | AIC mm2 直写 GM → AIV ProcessVec2（经 `mm2InBuf` 32KB 分层搬 UB） | AIC `Set<PIPE_FIX>(id0)`；AIV `Wait<PIPE_V>(id0)`＝**`bmm2ResBuf.WaitCrossCore()`（vec2 L1629）** | AIV `Set<PIPE_V>(id1)`；AIC `Wait<PIPE_FIX>(id1)`×2 覆写前等两 AIV——**3 缓冲=流水深度 3 的释放环** | `multiCoreIdxMod3`/slot 由 mm2ResPos 三态轮转（base L286 声明 3 buff） |
| 4 | `vec2ResUb`（ProcessVec2 内 Alloc，**单 AIV 私有**） | UB | AIV 自己：首块 DataCopy 直装（L1361-62）→后续 FlashUpdateNew 原地 →末块 LastDivNew | 无跨核——**同核程序序** + VF 内部 HardEvent（V_MTE3 等，L394 区） | 无（消费于 CopyOut 后生命周期止） | 无环（每 (s1块,CV块) 新分配） |
| 5 | `softmaxExpBuf[3]`（L167/2160-62，256B `[64,1]`） | UB×3 | vec1 `UpdateExpSumAndExpMax<T>` 写 exp 因子 → vec2 `expUb` 读入 FlashUpdateNew | **无 CrossCore/HardEvent 显式同步**——同 AIV、`taskIdMod3` 错相 3 拍，靠软件流水「写者领先恰 2 级」不变量（**约定无断言→U-t″**） | 覆写由 3 深环+同不变量 | `taskIdMod3` |
| 6 | `softmaxMax/SumBuf[3]`（L165-66/2150-59，256B）＋GM 副产物 | UB×3＋GM | vec1 写（fp32 视图，见 §4）→ vec2 LastDivNew 读 `sumUb`；末块 `SoftmaxDataCopyOut(sumUb,maxUb)`（L650 区）写 GM `(B,N,Sq,8)/(T,N,8)` | 同 #5 程序序；GM 侧无回读 | 同 #5 | `multiCoreIdxMod3`（**注意与 #5 索引基不同：multiCoreIdx vs taskId**——两 AIV 分摊 s1 时各配 3 深环） |

**控制面（单独列）**：`SYNC_MODE=4`；`CrossCoreWaitFlag<4,PIPE_S>(15)`＝**kfc host 消息**（base L196-210，ssbuf→`CVSharedParams` 拷贝前置），仅启动期一次；**不承担上表任何数据面握手**。数据面 flag id 由 Buffer `SetCrossCoreID(id0,id1)` 注入（L348-353），具体数值出自动态分配（未逐一定值，U-t‴，不影响机制描述）。

**排空**：`notLastThreeLoop/TwoLoop/Last`（train L302-341）逐级少发一拍；AIC 侧对 #1 的 Wait id1×2 与 #3 的 Wait id1×2 在收尾由对应 AIV 末次 Set 满足；无额外 drain 例程（`CleanOutput` 仅清 GM 输出，base L196）。

## 4. U7 澄清：half 中间 sum/max 系路径混入，主路径为 fp32

- **Nd/Dn 主路径＝fp32**：ProcessVec1Dn L444-445 / ProcessVec1Nd L1030-1031 均 `Get<float>()`；`UpdateExpSumAndExpMax<T>`（L638/1295）T=float（主路径 T=float 由末块 static_assert 反锁）。
- **half 仅两处**：① ProcessVec1Nz（fp8 特化路径）L346-347 `Get<half>`＋L409 `UpdateExpSumAndExpMax<half,useNz>`；② SoftmaxDataCopyOut 前处理 L727：`useNz` 时 `maxTensor Get<half>`→`Cast(maxOutTensor,…,CAST_NONE)` 转 fp32 广播——**half 是 Nz/fp8 存储格式，非主路径**。
- InitBuffer 均 256B `[64,1]`（L2150-2162 注释原文），**TBuf 无类型、`Get<T>` 是视图**——先前「half 中间值」表述系把 Nz 特化误当主路径，**特此修正**：主路径 max/sum 全 fp32，half 仅 fp8/Nz 变体。产品/模板范围：本节结论限「非量化 fp16/bf16 训练 Nd 主路径」；fp8 走 Nz 特化的 half 精度损失未评估（残 U7″）。

## 5. 数学脚本正确性存档（仅 NumPy 对拍声明）

`management/validation/ch18-online-softmax.{py,log}`：seed=20261009 可复跑；**新增 Q/K/V/O 明文输出**（O_ref=O_online 逐元素、P_online 4×4 全矩阵入 log）供读者复演；脚本与 log 头部均声明「仅数学验证（NumPy fp64），非 NPU/kernel 验证」。关键迹：blk2 corr=[0.2882,0.6967,1.0,0.376]，最大误差 2.220e-16。

## 残项（主线已清，均单点小项）

| # | 事项 | 影响 |
|---|---|---|
| U-t | 输出 cast（fp32→OUTPUT_T）精确行位（Bmm2DataCopyOut 内部） | 正文一句带过即可 |
| U-t′ | #2 L1 FORWARD 无释放回执的覆写安全「设计约定」无断言 | 正文按机制描述+标约定 |
| U-t″ | #5/#6 三深环「写者领先 2 级」不变量无断言 | 同上；软件流水核心约定，值得正文点明 |
| U-t‴ | 数据面 flag id 动态分配具体值 | 不影响机制 |
| U-s2 | s2=256 先行分支（L40-44）归属场景类待认领 | 走查双支并列已处理 |
