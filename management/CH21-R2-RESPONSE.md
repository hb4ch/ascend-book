# CH21-R2 退修响应

日期：2026-10-09　写手：pi (GLM-5.3-Flash)。逐句修复；行号指修订后 `docs/05-comm/ch21-hccl.md`（verify 实测 10,552 字/中文 7,797）。

## 1. Read/Write 方向（21.5「读向对照」段重写）
- 删「Read/Write 都由数据归宿端发起」矛盾句。改为逐页原句并列：Read=「接口调用方为 dst 所在节点」（异步）、Write=「接口调用方为 src 所在节点」（异步）、ReadNbi/WriteNbi 同向（非阻塞）——**读由归宿（dst）端发起、写由源头（src）端发起，方向按接口分立**。
- 补「单边≠对端无感」限定：调用页未声明对端零准备，通道/内存句柄由建链契约（21.2）覆盖，本文不额外断言。
- 脚注：四接口页（Read/Write/ReadNbi/WriteNbi）均入 oH 独立列名。

## 2. serverType 实现证据（21.6「serverType：证据到哪算哪」段重写）
- 新证据：`hccl_common.h` L65 枚举**两值** `HCCL_SERVER_TYPE_AICPU=0/HCCL_SERVER_TYPE_CCU=5`；`hccl.h` L49 模板注「Only …AICPU supported」；L414 `HcclImpl<serverType,config> impl_`——**HcclImpl 定义不在头文件（库实现），arch 分支/服务端选择无法本地追认**。
- 结论降级：头注（仅 AICPU）与使用页（950 仅 CCU）的适用范围差异**本章不闭**，删「模板选 API 形态∴不矛盾」的自行解释与「可用性开关」断言；改为「选型前查所用版本服务端矩阵与头注，不提供跨平台模板取值表」。
- 示意代码注释明确**按 A2/A3＋AICPU 形态书写，不暗示 950 直接套用**；前后两段统一为「证据未闭」口径（原「模板形态/可用性开关」两说已删一）。

## 3. repeat/Wait/Finalize 契约（21.6 重写段）
- 逐页录原文：Wait.md——计数=repeat（非细粒度）/步长换算（细粒度）＋**同序**＋默认全体核可单核指定；Commit.md——计数同；Finalize.md——①`Finalize<false>` 前须先同步否则「无法保证数据传输完成」＋多队列先 QueueBarrier；②终止语义：对象不可复用须重建 InitV2。
- 与「免 Wait」冲突消解：明写**计数约束只作用于选择 Wait 的路径（先通后算，ReduceScatter 实例属此）**；先算后通不走 Wait 不受该计数——按编排分立。例子作用范围标注「该实例（多核 AIV、核间 Wait）」，不推广普适收尾律。
- 未引入他章等0读1内容；「多核协同由框架 Tiling 保证」无证句删，改「核间分工保证方式本章无证据不展开」。

## 4. 主线/独立案例再接线与跨层断言（21.3/21.8）
- 32B 句删 AIV 归因：「输入规模属小数据量级，仅此而已」；并注明样例 `hcclDeterministic=1` 与 21.4 走查前提 DISABLE 取值不同、互不引用。
- 「Device 失败不能靠 Host…反之亦然」不可能断言删，改「各层错误走各层接口；跨层是否传播/如何传播本章无证据不下断言——分层逐查」。

## 5. 脚本路径与报告措辞（脚注 oA–oH 重写）
- 每个被引文件**独立完整 repo/path**（hcomm/…、asc-devkit/…、cann-learning-hub/…全前缀，无前缀+短路径、无目录下列文件代指）；逐文件 `test -f` 实核存在（脚本输出全 OK）。
- oF 修 `hccl_comm_host.cc` 真路径 `framework/communicator/hccl_comm_host.cc`（非 impl/ 下）；补 `hccl_communicator_device.cc` L1300。
- oH `HcommLocalCopyOnThread.md` 移至 **local_operations/**；补 ReadNbi/WithNotify/Fence 页、aicpu_quick_start.md（验签）。
- oG 补 Wait/Commit/Finalize/AllReduce 四页与 hccl_common.h。
- CH21-REPORT 措辞相应更新（见文末）：不再称「路径已全部展开」，改「逐文件 test -f 实核」。

## 6. 措辞与依据纠正（21.4）
- 「恒真」→「恒 false（device 编译单元版，hccl_communicator_device.cc L1300）；host 侧实现见 hccl_communicator_host.cc（读 config）」。
- 「不是函数」→「决策表型函数」。
- Level0/2 依据改**枚举注释实录**（common.h L48-77 逐项）：Level0 各拓扑注原文；Level2=WHOLE_RING/HD/RING/NHR/NB/PIPELINE，**「Level2=AHC 细分」无据已删**（AHC 细分在 Level1 AHC/AHC_BROKE）；不再从名字推断机间/机内。
- nicList 逐行（L113-117/L162-166 同式两处）：`!isStandardCard && deviceType!=910B && !isDiffDeviceType` ∧ `nicList!=8 && deviceNumPerAggregation==8 && algType0!=8P_RING` → ERROR+`HCCL_E_PARA`——**「配了 ring 却缺 8 网卡」的一致性校验**，非普遍强制；AHC 条件补 isConfigAHC/isNoARS/isNoAHC 精确组合（L87-96/L138-140 注原文）；310P 补「用户未配 level0/1（双 DEFAULT）才 WHOLE_RING，用户配置优先」。

## 7. 21.8 脚本与验签口径统一
- 脚本重排：**先 `set -e`（注释：不加 -u，厂商 set_env.sh 可能引用未定义变量）→ `source /usr/local/Ascend/cann/set_env.sh`（路径可改）→ `export MPI_HOME="${MPI_HOME:-/usr/local/mpich}"`**→环境检查→mktemp 复制→make/test；头部注明「本书无多机环境，未执行，仅 bash -n」。
- 验签双处统一到源文限定：21.7 与脚本注③均=「仅自编包（无签名头）按 aicpu_quick_start.md L66-74 关验签（npu-smi custom-op-secverify-*）；已装环境跑样例 README 无要求」。

## 验证
- `npm run verify`→`management/validation/ch21-verify.log`：0 FAIL。
- `npx vitepress build` 过（修复 `<false>` 裸 HTML 两处）；脚注 oA–oH 闭合（HTML footnote-ref=22）。
- `bash -n`：`management/validation/ch21-r2-bashn.log`（对 `ch21-r2-cmd.sh`）exit 0。
- 字数：verify 口径 10,552 字（中文 7,797），仍低于 8k 下限——PM 裁量声明延续（REPORT）。
