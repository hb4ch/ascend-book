# CH21-R1 退修响应

日期：2026-10-09　写手：pi (GLM-5.3-Flash)。逐项实际修改；行号指 `docs/05-comm/ch21-hccl.md` 修订后（L 值以 `nl` 为准，正文 9,574 字/中文 7,104）。

## 1. 21.8 命令不可执行 → 重写独立 bash 块（L294-316 区）
- 删 `WK=$(mktemp -d && echo ok)`、注释式 cp、`RANK_TIME`。新块：`set -euo pipefail`＋`CANN_SRC=/mnt/SATASSDEXT4/cann`＋`N=8`（注释：01 README 950 系=2、其他示例 8，且须≤可用卡数）＋`test -n ASCEND_HOME_PATH/MPI_HOME`（对应 Makefile L1-10 强制检查，未设即退出并提示）＋`mktemp -d` 后**真实** `cp -r "$CANN_SRC/hcomm/examples/01_communicators/01_one_device_per_process" "$WK/"`＋`cd && make && make test N="$N"`。
- 验签改条件式：仅自编 tar 包按 build 文档「关闭验签」；直接用已装 CANN 运行样例无需关（README 无要求）。
- 头注声明「本书整理——封装、变量与前置检查为本章补齐…不冒称源文原文」，删「命令逐字出处」表述。
- `bash -n` 存证：`management/validation/ch21-r1-cmd.sh`＋`ch21-r1-bashn.log`（exit 0）。

## 2. 证据越界与链序 → 结构重排（L138-176 区）
- 21.3.4 整节**移入 21.4**：新 21.4.1「入口观察与已证链」，入口观察标注「legacy 入口行为，非 Host 契约证据」；删「值得全文抄录」「Host 契约与内部实现的接缝就在此函数」等接缝已证措辞，改「再往下跨 weak 断点，不画实线」。21.3 现只依样例＋C 接口页。
- 21.4.1 树重画：`HcclAllReduceInner ─L115→ HcclAllReduceV2 ✂ weak(op_base.h L89)`（并补旁证：910 树无 V2 实现、仅 950 树 op_base_v2.cc L1263 同名）→**已证链自 `HcclCommunicator::AllReduce(L3089)` 起**；ExecOp 内按调用点重排：**SelectAlg L4649 → PrepareZeroCopy → CalcResRequest L4679/4706 → PrepareCommInfo L4719 → Orchestrate L4809/4831**，并加「次序要点」段明说初稿误序。
- SVG 同步：层②文字改「Communicator::AllReduce→ExecOp：SelectAlg(L4649)→资源→Orchestrate(L4809)」＋「入口Inner→V2为weak断点(✂不画实线)」；层③补「Finalize 等最后任务」。重渲染像素验证 4 色块（ch21-svg.png）。

## 3. Device 生命周期补足（L246-272 区）
- Finalize：补接口页两处原文（机制节/L143）「客户端检测并等待最后一个通信任务执行结束」——非裸退出。
- 「无须 Wait」限定：仅先算后通编排；且**不等于可提前改写/释放任务缓冲**（源文未给更细承诺，本书不下结论）。
- repeat 契约新段：repeat=Commit 次数=Wait 次数（L159 原文）；ReduceScatter 实例两法（3×repeat1 或 repeat3+3Commit/3Wait）。
- SyncAll：`g_coreType==AIV` 分支＋源文注原文「防止0核…提前Finalize…其他核Wait卡死」（两处实例同注）＋适用条件（多核且有核在 Wait；单核无此问题）。
- SetCcTilingV2 签名按头文件核对：`__aicore__ inline int32_t SetCcTilingV2(uint64_t offset)`（hccl.h L274，Hccl 成员）——示意代码改 `hccl.SetCcTilingV2(…)` 并注明「文档早例裸调/后例成员调，以头文件为准，本书改写」；InitV2 签名核对一致（L293）。

## 4. 走查前提与伪码（L182-206 区）
- 走查前提**全列**：2 server 幂方、每聚合 8、`isSingleMeshAggregation_=false`（明示非单机聚合走 OR）、`multiModuleDiffDeviceNumMode_=false`、**`isOnlyAiv=false`（并注明若 true 则小数据 OR 恒过、走查失效）**、mesh、buffer≥16M、白名单、非 Barrier、GetAivModeConfig、确定性 DISABLE；结尾加「任何前提变动须重走全式」。
- 伪码头注改「**判定伪码：按 L299-341 改写（∈/≥/…为本书记法，非逐字源码）**」；21.4.1 入口块同标「按源码改写」。
- AIV 白名单改精确引用 device_capacity.cc L57-64：{FP32,FP16,INT8,INT16,INT32,BFP16}×{SUM,MAX,MIN}。
- 「恒真」笔误→「恒 false 实现（仅 device 编译单元）」。

## 5. 数据面语义（L216-244 区）
- Nbi：`HcommWriteNbiOnThread` 功能节原文「非阻塞接口」；950 约束全录（仅 Host CPU、engine=COMM_ENGINE_CPU、协议 RoCE/UB_CTP、**NBI 仅 RoCE 需 DPU/1825、不支持 UB_CTP**）。
- Fence：功能节原句「插入内存屏障…确保屏障前的通道读写操作在屏障后的…之前完成」——标注为排序保证非等待。
- WithNotify：功能节「写数据并向对端发同步信号（异步）」。Read：调用方=dst 所在节点（单边语义落地）。
- `HcommWriteOnThread` 完成契约：明写「本页未给完成通知语义，完成须显式配 notify 或 WithNotify 变体，不得拿 P2P Read 握手泛证」。
- 同域单引擎：补架构文档原句引用（architecture-brief L128）。
- 21.7.2 标题改「原语速览（非完整词表）」正文同改。

## 6. Suspend/Resume 与配置措辞（L70-96 区）
- 三件套页首「预留…不支持开发者使用」改为**全接口限制**；矩阵按页实录重排：Suspend 950 不支持/A3A2 支持；Resume 950 支持；GetStatus 仅 950 支持——并明「矩阵互缺，不作应用层故障恢复建议」。
- 矩阵速览表 6 行全部按接口页「产品支持」节实录（含 Destroy 全支持）。
- `hcclOpExpansionMode`「直接决定」→「配置输入…仍须过能力/条件判定（配置≠裁决）」，与 21.4 条件链不再矛盾。

## 7. 脚注与编号体系（L341-349 区）
- 行内〔Cn/Dn〕体系全删（22 处→0），改三级文字标注（源文/源码/推演）＋warning 框重写；内容型编号转括号（如 hccl.h L308-316）。
- 脚注 oA–oH 全重写：**每文件完整 repo/path**（hcomm/…、asc-devkit/…、cann-learning-hub/…全前缀），oF 以「hcomm/src/legacy/ascend910/ 前缀」声明后逐文件全路径；`…/hccl_comm_host.cc`、样例同目录 json 均展开。
- LocalReduce 表述：参数表 6 种「UINT8/INT16/INT32/FP16/FP32/BFP16」（两处重载同）vs 示例场景2 INT8→FP32，「首项 UINT8 的表与 INT8 的例并存，源文内部不一致照录」。
- 虚构字段自查：`hcclMsgArea`/`GetCommunicatorV2`/`StateGuard` 等均见源码/头注；`hccl_primitives.h`→正名 `hcomm_res_defs.h`（L1 表）。

## 8. 工程叙事与字数
- 21.2.2/21.2.3 拓扑名词重复合并为一节（21.2.2「拓扑模型与资源名词」）；`### 21.2.1` 序号补齐。
- 销毁序改「单样例顺序事实＋完成后释放前提，不得推广为 API 强制」（L146 区）＋陷阱 7 同步。
- 补实质（非目录凑字）：Host 返回/错误三件套与缓冲量纲推演（21.3）；Device Prepare 返回/调试注/产品行（21.6）；Read 单边语义、Write 全参数表、错误处理三层对照（21.5/21.8）；模板 serverType 头注原文（21.6）；config 字段逐项（21.2）。现 **9,574 字/中文 7,104**——仍低于 8k，维持 PM 裁量声明（REPORT 已载），未以重复边界段落注水。

## 验证
- `npm run verify`→`management/validation/ch21-verify.log`：0 FAIL，ch21 9,574 字。
- `npx vitepress build` 过；脚注 oA–oH 双向闭合（HTML footnote-ref=21）；图 1 幂渲染验证过。
- `bash -n`：`ch21-r1-bashn.log` exit 0。
