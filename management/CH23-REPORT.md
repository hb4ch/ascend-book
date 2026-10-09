# CH23-WRITE 报告（候审）

日期：2026-10-09 ｜ 写手：pi（未换模型、未 commit）

## 交付物

- 正文：`docs/05-comm/ch23-supernode.md` —— **9,639 字（中文 8,022，`npm run verify` 口径）**，frontmatter `status: 待审`。
- 图：3 幅 mermaid（①23.1 串行/切块流水 flowchart；②23.2 host/device/跨卡三层数据流；③23.5 Wait/Finalize 计数时序 sequenceDiagram），每幅图前问题＋图后带读；表格 2 张（23.3 落点决策、23.6 同步三范式）。
- 截图（站点真实渲染，Playwright，`pageerror=0`）：`management/validation/ch23-fig{1,2,3}.png`（svg 尺寸 624×171 / 324×900 / 624×570；墨水率 3.2/4.0/2.7%，行列投影确认非空白）。另 mmdc 独立渲染通过（fig1 13.9KB/fig2 17.0KB/fig3 24.3KB）。
- 校验：`management/validation/ch23-write-verify.log`（**verify=0，无 FAIL**）；`management/validation/ch23-write-bashn.log`（`bash -n` 通过，块提取 `ch23-write-fence.sh`）。

## 主线覆盖（对照 rev2 提纲 7 节）

23.1 为何切块（图①）→ 23.2 主例 `aclnnMatmulAllReduce`（图②；A2/950 非量化、A3×按 README 产品表）→ 23.3 Host 三决定（切分 commOrder/落点三分/`aicpu kfc server` 缺省＋ccu 例外、消息区字段、padM、走例 33.6MB<200MB）→ 23.4 设备主循环（notifyFlag 单核、窗口 remap、repeat 登记、Mc2SyncAll=ON_CUBE_AND_VECTOR、PostProcEachTurn 加法双屏障）→ 23.5 完成判定（三本账、Wait 步进条件、queueNum 早退、**A2 单 Wait 只押 1 轮、收敛在 Finalize Query**、sync 三重守卫仅末 handle、950 逐轮 Wait 对照、HCCL_MSG_CNT 环形、apiStats 旁账）→ 23.6 MoE 推拉（950 纯 AIV 无 HCCL API、状态字 0x3F800000 编码、dataState 翻转非清零、combine=UB Muls/Add 向量归约、A2 layered 入口存目、TP 参数预留）→ 23.7 URMA flag 注入＋同通道免二次 Wait＋dcci、PTO 双流 ready queue＋fence、系统场景只写构成×行为 → 23.8 复现（mktemp 副本＋`test -d`＋独立命令行、`[需真机验证]`）＋入口地图＋观测点＋未证清单。

## 任务专项纪律逐条

1. **Wait 增量**：正文与脚注均写「stepSize 非零仅新 tiling＋AllToAllV；主线恒 0→+1；`queueNum!=0` 直接成功」——`hccl_aicpu_impl.h` L416-433/L450-451 实核（本回合复验 L450-451 原句）。
2. **Finalize 边界**：只写「sync 分支旋等 `curHandleId_`（最后 handle）」；tile＋tail 双 handle 时前序收敛标注「未证（server 消费顺序），账本未知①」；三重守卫（sync/存在 handle/非仅算）已写。
3. **SyncAll 按实例**：主线 `ON_CUBE_AND_VECTOR`（`arch22/...cpp` L123 `INVOKE...ON_CUBE_AND_VECTOR` 实核），纯 AIC 才 flag。
4. **MoE 状态复位**：写「翻转写回＋dcci＋双 buffer 轮转，无显式清零」；未引用任何 L24 行号；dispatch/combine 不称镜像（推/拉+UB 加法归约分述）。
5. **运行命令**：真实路径 `/mnt/SATASSDEXT4/cann`→mktemp 副本、`build.sh --pkg --soc=... --ops=...`；无 NPU 仅 `bash -n`，标注 `[需真机验证]`。
6. **无虚构数字**：全章无自测性能数；33.6MB 走例标注「纯示形」；608QPM/11 节点注明厂商实践无复现脚本。

## 未证边界（正文已收窄＋23.8 清单）

AICPU server 消费循环、CCU 内部算法、A2 layered MoE 协议、950 UB Memory 内核实现；另两处「文档契约 vs 实现」缝隙（单 Wait、末 handle）已显式处理而非掩盖。

## 遗留

- 图② svg 偏窄高（324×900，TB 三层堆叠所致），内容经投影验证完整；若经理要求可改横排。
- 章名维持提纲 rev2 待裁定项之一，未自行收窄。
