# CH27 提纲 —— 全栈综合案例：一次 SFA 稀疏注意力的库调用全链（rev1）

2026-10-10。证据：`management/CH27-EVIDENCE.md`（下记 EV§x）。**场景固定**（EV§A，全章唯一）：`ops-transformer` 的 `sparse_flash_attention`，aclnn 两段式调用，q{1,16,512}/kv{2048,1,512}/sparseIndices{1,1,2048}、主体 fp16+indices int32+softmax fp32（逐张量表 EV§A）、TND、A2/A3/950。读者视角：**「我不想手写注意力，想用仓库现成算子并核验它对不对」**——与 ch18（手写稠密 FA）互为对照，不重复其推导。预计 4.5–6k 中文；2 图 2 表；无性能数字（NPU 实验只给可复现设计）。

## 27.1 选型：两个候选与一条被选的路（~0.6k）

开篇即亮比较表（EV§B）：SFA vs sparse_flash_mla——证据完整度逐项对，**选 SFA 的理由写实：多一轮本书独立数学对拍与内核路径闭合**；MLA 留一句替代入口。随后全章路线图：调用→host→kernel（闭合到一条真实执行路径）→核验。选型评审过程不进读者正文。

## 27.2 从参数到内核：host 侧调用链（~1.2k）

- 先摆场景代码：example 的 shape/dtype/layout 五行（EV§A）——读者可逐字对源码。
- **两段式 API** 的白话：先问工作区大小（GetWorkspaceSize，把 tiling/内存规划做掉），再正式执行；`extern "C"` 头与 op_host 三件套（def/infershape/tiling，2295 行只说规模【缺口】）（EV§C1）。
- 先摆 example 真实时序（EV§C1）：两段式 API→workspace 条件分配→launch→**sync→逐层销毁（无读回无打印，PrintOutResult 仅有定义未调用）**。
- **图①（主图）**：参数→example→op_api 包装→OpDef/infershape/tiling→GenTilingKey（位字段）→kernel（`__CCE_AICORE__` 门控 arch35/arch22、fp16 `if constexpr` 分支、MIX_AIC_1_2）→sync 收尾；**三处未闭合边（Inner 实现体/soc↔宏映射/tilingKey→bin）画虚线断点**；右支独立虚线框=本书 CPU 对拍。实线箭头逐条 EV 行号背书。

## 27.3 设备侧一瞥：模板化 kernel 与双架构（~0.8k）

只讲可锚定事实：架构门控与主例命中分支（EV§D）+ **一条闭合的执行路径（EV§K）**：AIV MergeKv 按 topk 索引收集稀疏 KV→AIC mm1(QK^T，Fixpipe mm1ResGm)→syncC1V1→AIV softmaxFlashV2(vec1ResGm)→syncV1C2→AIC mm2(PV，mm2ResGm)→syncC2V2→AIV 1e10掩码+RowDivs 归一→cast 写 attentionOutGm；首(AIC 预放 flag)尾(V 等 flag+extraLoop2)排空。**主例模板实值表**（FLASH_DECODE=0/V_TEMPLATE/TND/IS_SPLIT_G=0/mBase=16/s2Base=512）。宏范围声明：soc↔`__CCE_AICORE__` 映射未证，以「arch22 编译门内」叙述。仍未读：异常分支/Cube L1 全部 flag/arch35。与 ch18 关系：首先差异在**关注集合**（索引/掩码改变参与的 K/V 子集，EV§F），其次才是工程形态。

## 27.4 核验：两条 CPU 路线与它们的边界（~1.2k）

- example 无读回无对拍（EV§C1 实测）；对拍在 pytest：CPU golden→NPU 直调→精度对比（流程转述，未执行）。
- **E1 冒烟（BSND，另组输入）**：只证链路可跑；golden 内部 randperm 未种子化→数值逐次不同，均值/方差不是判据。
- **E2 独立数学对拍（同主例条件缩小版）**：numpy 独立实现，seed 固定，shape/有限值断言，本次输入 max abs 2.48e-4 < 阈值 2e-3（阈值依据：输出为 v 凸组合、softmax fp16 cast ~4.9e-4/权重；只声明本次输入不外推）（EV§E2）；**两个 golden 语义发现+覆盖如实**：indices 被重生成覆盖、v=k[,\:512] 隐含 D=512；-1 终止/越界截断/空选集本输入未触达（参考含分支≠覆盖）。
- **明标**：CPU 数学参考非 NPU 验证；对拍只证 golden 数学=独立复算，**不证 example/算子实现正确**；example 无读回无对拍，正确性结论只能来自 NPU pytest（未执行）或读者自跑；依赖 tensorflow 留痕；源树 pyc 写入/删除违规记录（H0）。
- **可复现 NPU 实验设计**（替代性能表）：按 pytest single 流程列步骤（环境→paramset→single→compare），读者有 A2/A3 即可执行；本书不代填结果。

## 27.5 它从哪来：DSA 与 DeepSeek 生态位（~0.5k）

一段+图②：DeepSeek V3.2-Exp 的 DSA（索引器+Top-k 选择，O(L²)→O(Lk)），讯飞×CANN 贡献入仓（EV§F1，博客转述）；SFA 公式与该结构的对应（选择后 attention，EV§F2）；仓内同族算子一句带过。**不写性能倍率**。

## 27.6 缺口、复现与边界（~0.5k）

「本书做了/没做」两栏表收束（EV§L/H）：做了=TND 独立对拍+host→kernel 单分支闭环（C5/D/K）+执行留痕；没做=NPU/构建/异常分支与 arch35/三处未闭合边。复现三档；10 条缺口入清单。结尾一句回扣全书：从 ch9 手写到现在库调用，读者手里已有「自己写」与「拿来用并验」的完整两极。

## 陷阱与注意（择四）

- example 无读回无对拍（PrintOutResult 未调用）——正确性结论只能来自 NPU pytest 对比（本书未执行）或读者自跑——本书 CPU 对拍只证 golden 数学可独立复算。
- golden 重生成 indices+v:=k 截断两条语义，复现时先读 EVIDENCE E2。
- dynamic 开关/内存池语义属图后端（ch26），与 aclnn 单算子无涉，勿混。
- V1/V2 差一个 sinks 参数，pytest 据此选 API——复现时先定版本。
- arch22/arch35 kernel 有行为差异可能（未核），跨代结论须分开验证。

## 图表

| # | 形式 | 节点数 | 证据 |
|---|------|------|------|
| 图① | mermaid 全链 | ≤10，两支（实线=源码调用链，虚线=本书 CPU 实跑） | EV§A/C/D 行号 |
| 图② | mermaid DSA 结构 | 4 | EV§F【文】转述声明 |
| 表×2 | markdown | 候选比较／做了-没做 | EV§B/G/H |
