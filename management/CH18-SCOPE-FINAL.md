# CH18 最终主线条件核查（CH18-SCOPE-FINAL）

> 2026-10-09。只读核查，未动正文/图/appD。结论：**R3 的 fp16/128/128/D256 确系 useDn=true（经理对）**；真 Nd+GM 组合见 §二，代价是**必须带 mask（hasAtten=true）**。mm1 出口 dtype 亦随路线反转（§四）：**Nd 出口 fp32 NoQuant，QF322F16 系 Nz 路径**——此前正文 18.4 的精度链叙述需按本报告重写（待经理指示）。

## 一、三个谓词逐式代入（真码行号）

`common/.../arch35/flash_attention_score_common_regbase_arch35.h`：
- `IsDn`（L172-88）：`(!isFp32∧!ContainOptional)∥(isValidFp8∧…) ∧ !isS1Base64 ∧ d≤Aligned256 ∧!rope`
- `UbOutCondition`（L163-79)：可选输入全无时 `!isS2Base64∥isFp32→true`；**有可选输入→false（fp16 非8/rope 支均假）**
- `GetC2Position`（L191-216):`d≤128→UB；ubOut∧d≤192→UB；isNdS2Size256→UB；else GM`

调用点（cube L147-58）：`useDn=optionalDn||IsDn((isFloat||isFp8),(isFp8&&s2==256),pseMode,hasAtten,hasDrop,s1==64,dTemplate,hasRope,enableKVPrefix,isInfer,isHiFp8)`；`bmm2OutPos=GetC2Position(dVTemplate,UbOutCondition<INPUT_T>(isFloat,…,s1==64),(s2==256&&s1==64),isMlaFullQuant,false,optionalDn)`；`splitD=(dV>256)`；`useNz=isHiFp8∧!infer`。

**R3 组合复核（fp16,128/128,D256,无可选）**：`!isFp32∧!Contain=T`、`!isS1Base64=T`、`d≤256=T`、`!rope=T`→**IsDn=T（dn 非 Nd，经理对）**；UbOut=`!isS2Base64`=T→`d≤128?否;ubOut∧≤192?256>192 否`→**GM**。即 dn+GM——非 Nd。

## 二、真 Nd＋GM 组合（唯一干净族：fp16＋可选输入）

**引入 hasAtten=true（其余无可选）**：
- `ContainOptionalInput(PSE_NONE,atten=T,drop=F)=T`→IsDn 第一支 `!isFp32∧!Contain`=F；第二支需 fp8——**IsDn=false→Nd** ✓
- `UbOutCondition`：Contain=T→中支跳过；fp8/int8 rope、fp8 mask 支假→**false**
- `GetC2Position(Aligned256,false,s2==256&&s1==64?=F,false,…)`: `256≤128`F、`false∧…`F、isNdS2Size256 F→**GM** ✓
- `splitD`：dV=D=256，`256>256`F→false ✓；`useNz`：hiFp8 才 T→F ✓；`optionalDn` 未用 F

### 实参总表（本章主线终版候选）

| 项 | 值 | 依据 |
|---|---|---|
| INPUT_T/T/OUTPUT_T | **half/float/half**（entry L116 `KernelTrain<half,float,half,…>`） | 入口显式实例 |
| s1Base/s2Base/dBase | 128/128/256 | 模板参（host 选择未验，走查前提） |
| pseMode/hasDrop/hasRope | PSE_NONE/F/F | 主线圈定 |
| **hasAtten** | **true（如 causal sparseMode 的 uint8 mask）** | IsDn=false 的关键 |
| useDn/useNz/splitD/bmm2Write2Ub | **F/F/F/F（Nd＋GM）** | 上列代入 |
| isInfer | false（训练） | KernelTrain |

**限制声明**：host 侧对该组合的自动选择未运行验证；hasAtten=true 须真实传入 attenMask（非占位）。

## 三、mask 的真实 vf/copy 路径（该组合）

- 搬运：`ProcessVec1Nd` 内 `AttenMaskCopyIn<hasAtten=true,isFd,enableKVPrefix>(attenMaskInQue[taskIdMod2],[1-taskIdMod2],attenMaskGmInt,…)`（vec_base L1015-22 区双队列）→`attenMaskUb=…DeQue<uint8_t>`；非 Mla 路径（MlaAttenMaskCopyIn 是 isMlaFullQuant 支）。
- 消费：`attenMaskUb` 入 `ProcessVec1Vf<…,hasAtten=true,…>` 模板参（L347-59 区四调用），VF 内逐元素与分数合成；窗口裁剪仍由 s2LoopLimit/s2StartIdx 决定（L441 判定 `s2EndIdx−s1Base<s2Base∨…`）。

## 四、mm1 出口实况（Nd≠Nz，dtype 链更正）

- **Nd 出口＝`FixpipeBmm1NdToUb`（cube L973-1003）**：`FixpipeParamsC310<ROW_MAJOR>`，**无 quantPre 设置→默认 `NoQuant`**（kernel_struct_fixpipe.h L156），`dualDstCtl=1`（**单次调用双目标按 M 拆**，非两次单目标）；`Fixpipe<T,T,PFA_CFG_ROW_MAJOR_UB>`，**T=float（入口实例）→fp32 直落 UB**。
- **QF322F16_PRE＋两次单目标拆分系 `IterateBmm1Nz`（L1330/L1440-66，fp8/Nz 路）**——此前误植主线。
- vec1 侧对应：**`mmRes=bmm1ResBuf.GetTensor<T>`＝float 视图（L1085-86 区），`stage1CastTensor=AllocTensor<INPUT_T>`=half**——softmax fp32 入、P cast half 出，链内**无 fp16 中转的 mm1 结果**。
- mm2 出口：`Fixpipe<T,T,ROW_MAJOR(GM)>` fp32 写 GM（cube L2220 区，bmm2Write2Ub=F 支 dstStride=dSizeV）；vec2 `Get<T>`=float——**全链 fp32 直至 P cast 与出口 cast**。
- Dn 出口（对照，非主线）：`IterateBmm1Dn`→另 Fixpipe 路径，本报告未展开（主线非 dn）。

## 五、入口/出口汇总（该组合）

| 站点 | 符号 | 行为 |
|---|---|---|
| mm1 出口 | `FixpipeBmm1NdToUb`（cube L973） | fp32、NoQuant、dualDst=1 拆半→UB BOTH |
| vec1 入口 | `ProcessVec1→ProcessVec1Nd`（L307/930） | Wait id0；mask 经 `AttenMaskCopyIn` |
| vec1 出口 | P：`stage1Cast`→L1（L1292 Set id0）；exp/m/l 入环 | half/fp32 混合见 §四 |
| mm2 出口 | cube L2220 区 `Fixpipe`→GM＋`SetCrossCore`(id0) | fp32 ROW_MAJOR |
| vec2 入口 | `ProcessVec2`GM 版 L1625/L1629 Wait id0 | 32KB/切片搬运→四分支 |
| vec2 出口 | `LastDiv/FlashUpdateLast`→`Bmm2DataCopyOut` `Cast CAST_ROUND`→half GM | L2022 区 |

## 六、待经理决断

1. 正文 18.4 精度链/双拆表述按本报告改（Nd=fp32 NoQuant+dualDst1；QF322F16 归 Nz）——**待令**。
2. 主线是否接受「必须 hasAtten」？若要无可选输入的 Nd+GM：无解（无可选→IsDn=T 或 ubOut=T→UB），**只能 UB 重载**——两难需 PM 定主线（带 mask 的 GM vs 无 mask 的 UB）。
