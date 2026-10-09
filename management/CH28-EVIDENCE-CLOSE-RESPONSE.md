# CH28 补证回应 —— CH28-EVIDENCE-CLOSE.md 逐项

EVIDENCE 升 rev2、OUTLINE 同步；未写正文。源仓全程只读（asc-devkit/hixl status=0）；未提交。

**1 存在性→实现核验（两项实读，C1/C2 重做）**
- **Tensor API 样例**：`matmul_mxfp4_tensor_api_high_performance/mmad_mx.asc`（548 行）全文实读。关键链：`#include "tensor_api/tensor.h"`（L18，独立于 kernel_operator 老路径）→`Te::MakeTensor(MakeMemPtr, MakeFrameLayout<NDExtLayoutPtn/ScaleANDLayoutPtn…>)`（L71-84）→`.Slice(MakeCoord,MakeShape)`（L86-98）→`Te::Mmad(mmadAtom.with(params),…)`＋`MakeMmad(MmadOperation,MmadTraitMX)` 静态装配（L329/L452）、`fp8_e8m0_t`/`Location::L0ScaleA/B`（L52-56/150-157）、`Mutex::Unlock<PIPE_MTE1>` 双缓冲（L312-322）。**对照物**：同任务老范式 `matmul_mxfp4_high_performance/matmul_mx.h`（kernel_operator.h+matmul_intf.h 手工传参）——「新在哪」有实码对照。**未编译未运行**（950PR/DT 且 >9.1.0、dav-3510），「可编译示例存在≠已执行验证」全文分开表述。
- **VF printf/dump 样例**：`simd_vf_printf.asc`——`__simd_vf__ inline` 函数内直接 `printf`（int/uint/float/hex/ptr/str 各式）、host 侧 `AscendC::printf`+`GetBlockIdx()`、**`asc_vf_call<…>(__ubuf__ float*…)` UB 桥**、核签名 `extern "C" __global__ __vector__`+`InitSocState()`；`simd_vf_dump.asc`——`asc_dump_ubuf/asc_dump/asc_dump_reg`＋`AscendC::Reg::LoadAlign/Duplicate`。产品条件：**仅 950PR/DT ≥9.1.0**（两 README 产品表；同目录 `simple_printf` 才覆盖 A2/A3/950——能力-架构逐样例绑定）。`06_cpu_debug`：A3≥9.0/950≥9.1，GDB 断点不依赖 NPU（CPU 可入门项，如实分档）。

**2 无证趋势纠正**
- 「新学默认路径改变」**废止**：overview L19 自述基础 Tensor（指针+size）早已有——书 ch9/ch11 的 LocalTensor/GlobalTensor **并非 beta.1 新生物**；净新增=扩展 Tensor 的 Layout/Shape/Stride 自动推导＋`AscendC::Te` 命名空间，且 L21 明写**「当前能力赋能于 Cube 矩阵计算，后续逐步支持 Vector」**——正文改为「Cube/MX 新项目可评估；Vector 侧官方自述未覆盖」。
- 「打印靠 host 日志旧约束放松」**无证句废止**：对账书 ch11 L210 已写 SIMT `asc_printf`、L213 DumpTensor/msSanitizer——书中从未主张只能 host 打印；净新增精确为**SIMD VF 路径调试原语**（书 ch11 覆盖的是 SIMT 路径）。NPU Check 复核：基线内仍仅 CHANGELOG 句、无 doc/样例——ch11 L215 降级注记继续成立，正文只写「公告级」。
- **3510 三级层级**：限定「SIMD 编程视角（RegTensor 绑 3510，overview L19 括注）」，不替代芯片全局层级、不暗示旧代无寄存器——EVIDENCE B1 边界句已改。

**3 FabricMem/issue/日期**
- 带宽数字全部退出（20GB/s/百 GB 级不再现，22 章未完整口径不重复）；只留「统一编址、HCCS 直访远端」机制方向【文】。
- issue#275/138/#115 降为「公告/入口」，明写**不证明通用跨代互通已可用**。
- 快照日逐仓精确化（头部表：08-21 hub、08-22 五仓、08-23 ops-transformer），A 表「快照日」行同步；时间线要求公告时间与实现/代码证据分列（图①节点双标）。
- 发布日期定性「文档标注，本书未核打包行为」。

**4 计划缺材料**——不凑条目：EVIDENCE 新增 E2′节，正文 28.1 只写「如何读路线图」方法学（外链 issue 未读=未读；无 dated roadmap 的仓如实说）。

**保留的读者行动**（适用架构下读/验具体样例）：B1=950 用户可编译运行 mmad_mx 两对照样例；B2=950 用户跑 simd_vf_printf/dump、A3 用户 cpu_debug GDB 流程；均注明本书未执行。验证：本轮纯只读+管理文件，无 verify 需求（未动正文/站点文件）。候审。
