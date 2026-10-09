# CH21 服务端补证交付（CH21-SERVER-FINAL）

日期：2026-10-09　写手：pi (GLM-5.3-Flash)。按经理定位路径逐文件实读；仅 CH21 文件；未运行。

## 证据链（全部本地实核，路径见正文脚注 oI）

1. **分派**：`impl/hccl_impl_def.h` L20-26 按 `__NPU_ARCH__` 包 `hccl_v220_impl.h`/`hccl_v310_impl.h`；`impl/hccl_impl.h` L18-21——**2201 只 include platform_v220/hccl_aicpu.h（仅 AICPU）；3510 include platform_v310/hccl_aicpu.h＋hccl_ccu_v0.h（AICPU＋CCU 双特化）**。`hccl_v310_impl.h` 仅并两 def。外层模板只 DFX 包装→`impl_.template AllReduce<commit>`——真身在特化。
2. **3510 AICPU**：`common/hccl_aicpu_def.h` L21 声明＋`common/hccl_aicpu_impl.h` 实现（AllReduce L327→CommonPrepareImpl L250；Wait L416；Commit L457；Finalize L484）；平台覆写 InitV2（context=`OpResCtx`，platform_v310 L30-41）与 SendMsgToServer（L133-141 `#if 3510→AssembleHcclMsgV2`）。**AICPU 在 3510 无任何拒绝分支——完整可用**。
3. **3510 CCU**：`hccl_ccu_v0_def.h` L38 声明＋`hccl_ccu_v0.h` 实现（AllReduce L24→CommonPrepareImpl L338；InitV2 L200 识别 `INIT_TILING_CCU_NEW_VERSION→newCcuFlag_`；Commit L477 计数；Wait L499 assert `handleCommitCnt_>0`；Finalize L570）＋`ccu/hccl_ccu_v0_prepare.h`（AlltoAllV xn 组装）。
4. **2201**：仅 AICPU（InitV2 context=`HcclCombineOpParam`＋queueNum_，platform_v220 L147-160——**上下文结构随平台变**）；`platform_v220/` 无 CCU 文件→2201 编 `Hccl<HCCL_SERVER_TYPE_CCU>` 无实现可链（错误形态未证，不下结论）。
5. **AICube/AIVector 真机制**：`hccl.h` L73-74 note 的落点=模板二参 `HcclServerConfig{CoreType::DEFAULT/ON_AIV/ON_AIC, blockId}`（hccl_common.h L69-73；DEFAULT_CFG={DEFAULT,0} hccl.h L33）→`InitWorkingFlag`（hccl_aicpu_impl.h L68-80）`workingFlag_=(g_coreType==AIV/AIC && GetBlockIdx()==blockId)`——**编译期定核型与工作核号，非运行协商**。
6. **头注冲突裁定**：「Only …AICPU supported」（hccl.h L49）与 3510 双特化矛盾→**标头注过窄**（写定版本未注），不构造「API 形态」解释；serverType 适用矩阵以实现＋产品使用页为准。

## 正文修改（docs/05-comm/ch21-hccl.md）

- **新增 21.6.1「服务端实现：__NPU_ARCH__ 特化链」**：分派链＋3510 双特化对照表（声明/公共实现/平台覆写三行）＋2201 差异（context 类型、无 CCU）＋头注过窄结论。替换原 R2「serverType：证据到哪算哪…未闭」段——**未闭状态已被 impl 实证闭合**，不再说「无法追认」。
- **新增 21.6.2「AICube/AIVector 指定的真机制」**：CoreType/HcclServerConfig→InitWorkingFlag 编译期核指定；替代原「核型指定义务在调用方」的无机制陈述。
- 示意代码注释改指 21.6.1；「平台注意两则/两代机制差异」段保留为使用页视角，删除与 21.6.1 重复的合读句。
- **脚注 oI 新增**（impl 11 文件全路径＋行号）；oG 补 L33 DEFAULT_CFG/L73-74 note。
- 21.6.1 AllReduce 链补：两路特化同样以 `CommonPrepareImpl<commit>` 收口（AICPU L250/CCU L338 各自版本）——Prepare 语义同构、服务端分立。

## 图（docs/figures/ch21-hccl-layers.svg 重绘）

- 三框内长行全部拆短（≤45 字符/行），960×430。
- **②框**明写「legacy 独立案例…不涉 CCU 新路径；引擎=算法选择产物」——legacy 选路与标准数据面分立。
- **③框**纳入 impl 服务端实现（3510 双特化/2201 仅 AICPU/头注过窄）。
- 底部大框改「服务端执行形态（按范围分立陈述，跨范围汇流不画实线＝未证）」，三行分述①②③各自到达服务端的**证据形态**；另加两行图注：②legacy 与③impl 是两代两套代码不互证、①Host 无引擎可见性。
- 像素验证 `ch21-svg.png`（960×430；四色块 5598/5331/5449/17098）——**另按行宽人工复核无越框**（最长行 45 字符×11px≈495px＜框宽 840/292 内文 264px 上限…③框内最长行已缩至 42 字符）。非以像素检查替代可读性：行长/行数硬性约束已写入重绘规则。

## EVIDENCE

`management/CH21-EVIDENCE.md` 增 §7.7（服务端特化链全锚点＋四条结论）。

## 验证

- `npm run verify`→`management/validation/ch21-verify.log`：0 FAIL（10,814 字）。
- `npx vitepress build` 过；脚注 oA–oI 闭合。
- 未运行任何编译/核函数（任务要求不运行）；源码基线未动。
