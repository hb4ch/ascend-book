# CH23-R1 修订回应（候审）

日期：2026-10-09 ｜ 执行 `management/tasks/CH23-R1.md`，逐条对 `reviews/CH23-R1.md`。正文终态 `docs/05-comm/ch23-supernode.md`＝**4,216 字（中文 3,204）**；8k 下限按任务豁免，未为字数新增字段/变体。未提交、未动其他章。

## 逐条修订（引实测句）

**①图①依赖与条件化**——图①重画：补 `b2[MM 块2] --> c2[Comm 块2]` 数据依赖边；点线改标「可与块2计算重叠」；图前问句改为条件式「**切开之后，什么条件下才真的省时间？**」（置于代码块前）；图后带读改为「重叠是机会而非保证，切分本身不省时间；条件由 23.3 的切法与 23.4 的交接共同创造」。原「图前的问题：」标签式写法全部废除，三图均改为图前自然问句、图后「读图：」。

**②23.2 无证因果整段删除**——原「x2 二维因为 TP 权重共享／all mesh 因窗口直写／卡数上限是窗口与环数函数、64 即超节点规模」一段删去，替换为矩阵分片主例：23.1 开篇「把权重沿归约维切成各卡的份额，每张卡用本地份额乘出一份**部分和**，再把所有部分和累加，才得到完整的 y=x@W……算子只保证：各卡部分和按 sum 累加，等于全量结果」；约束仅保留「照抄 README，本书不替它们编造成因」句式（[^2]）。

**③后端/生命周期/commTurn 表述统一**——23.2 改「执行后端由实现按平台与配置分派，23.3 展开」；原「device 侧只见句柄」「executor 托管生命周期」推测句删除，只留头文件实证「`const char *group`……头文件注为『标识列组的字符串』」（[^3] L33）；commTurn 统一为「注释看似用户旋钮；README 约束仅接受 0，实现里 0 换成内部切分常数（[^2] L551-554），**用户暂时不能借它调块**」，删另一处「旋钮」说法。

**④无证调用链删除、算例完整化**——23.3 原「HCCL_BUFFSIZE/FabricMem/RDMA 窗预算互相扣配额」「量化低比特系数」两段删；算例保留但全假设声明：「若 M=4096 切 3072/1024、N=4096、fp16 输出，两轮发送量 3072×4096×2B＋1024×4096×2B=32MiB……数字是假设，判据以 tiling 实现为准」。23.8 「错误只在两处藏身」排他句改为非排他「以及 23.5 的两处契约缝隙……均已显式处理」；「第 24 章集群时间轴」句删除（第 24 章为 PTO 后端，原类比不成立）。

**⑤结构精简**——23.2 一段一事（产品→接口→commTurn→约束），变体谱系段删；23.3 每决定「直观含义一句＋最少字段」，msgSnd/msgRcv/padM/notify 清单沉脚注 [^4][^5]；23.4 收敛为「算/齐/交/续」四拍，入口宏、地址算术、OOM、bias cast、addX3 双屏障细节移脚注 [^6]；23.5 保留 repeat=2 散文走查，apiStats 旁账、HCCL_MSG_CNT 环形、CCU 对比移脚注 [^7] 或删；通篇清除括号串/箭头串/加粗堆叠式「通俗」句。

**⑥图②重画、图③限定**——图②改横排四拍「本卡计算→本卡缓冲→跨卡归约→本卡结果」＋Host 虚线旁注（自然尺寸 756×103，站点 624×85，非纵向堆积）；Host 配置不进主数据链。图③末行注改「**单 handle：此处即全部收敛；多 handle 另论**」，正文同步「Finalize 只显式见证最后一个 handle……有尾块时前一个 handle 的完成未被独立见证，本章不下结论（未知①）」——不泛称全任务已证完成。

**⑦脚注全路径与复现如实**——[^8] 补 `ops-transformer/mc2/moe_distribute_dispatch_v2/op_kernel/arch22/moe_distribute_dispatch_a2_layered.h` 与 `..._layered_aicpu.h` 全路径（原 `moe_distribute_v2/op_kernel/arch22/` 目录式引用，verify 曾 FAIL）；[^9] 通信原语补全 `apace/core/aiv_comm/all_to_all/all_to_all_udma_get.h`、`all_gather/all_gather_udma_put.h`；[^10] `ready_queue.hpp/common.hpp` 补全 `pto-isa/kernels/manual/a2a3/gemm_ar/` 前缀。复现块按 `ops-transformer/docs/QUICKSTART.md`（编译→`build_out` run 包→安装→`LD_LIBRARY_PATH=${ASCEND_HOME_PATH}/opp/vendors/custom_transformer/op_api/lib`→`--run_example`）重写，**删除手写 `source /usr/local/ascend-toolkit/set_env.sh`**（build.sh 自带 `DEFAULT_TOOLKIT_INSTALL_DIR` 探测，L83-86）；补「样例运行需至少 2 卡设备可见并预建 HCCL 域」，并明确「本机无 NPU，仅语法级检查，安装与运行未执行」——不称完整复现。

## 校验与图证

- `npm run verify`＝0 FAIL：`management/validation/ch23-r1-verify.log`（本篇 4,216 字/中文 3,204）。
- `bash -n`：`management/validation/ch23-r1-bashn.log`（块存 `ch23-r1-fence.sh`）。
- 三图站点实渲染（Playwright，`pageerror=0`）：`management/validation/ch23-r1-fig{1,2,3}.png`，svg 自然尺寸 988×125 / 756×103 / 841×625；墨水投影 3.9%/8.7%/2.6% 多行带分布，非空白。

## 未尽事项（本轮非穷尽，留给后续源码复审）

23.6 状态字编码的槽位公式、A2 layered 协议、CCU Wait 内部仍属「未逐行」；图①重叠无定量（须实测，本书不出数）。
