# CH27 交付报告 —— 第27章 全栈综合案例：一次稀疏注意力的库调用与核验

2026-10-10。任务：`CH27-WRITE.md`。证据基线 `CH27-EVIDENCE.md` rev3（含 KERNEL-CLOSE 闭环）；回应链 `CH27-{EVIDENCE-CLOSE,KERNEL-CLOSE}-RESPONSE.md`。

## 交付物

| 项 | 路径 | 状态 |
|---|---|---|
| 正文 | `docs/06-backend/ch27-case.md` | 4,213 字（中文 3,217，`word:count`）；status 成稿；frontmatter 去「可选」 |
| 图① | 27.2 调用生命周期（mermaid TB，7 节点） | 渲染+几何审计通过 |
| 图② | 27.4 核间路径与同步对（mermaid TB 双 subgraph+旗标边） | 重排为纵向后 696→624px 适配；审计通过 |
| 表 | 参数分类表（27.1）/核验矩阵（27.5） | 单元格无裸 `\|` |
| verify | `management/validation/ch27-write-verify.log` | **全绿 EXIT=0**（build/internal/source/terms/word）；「昇腾 C」warn 系 ch24「昇腾 CANN」历史匹配，非本章 |
| CPU 脚本终版日志 | `validation/ch27-sfa-tnd-refcheck.log`（2e-3 阈值+coverage 两行）、`ch27-sfa-cpu-golden.log` | 与 EVIDENCE rev3 一致 |
| 截图 | `validation/ch27-fig{1,2}.png`（2x DPR） | **仅几何审计，未视觉目检**（宿主无读图）：fig1 墨迹 bbox 边距≥15px/无越界；fig2 同（≥13px）；墨占比 2.7/2.9% 无空洞。请经理目检 |

## 结构（对应任务主线四问）

27.1 要提供什么（参数按 dtype 分类的表；scale 保留原值不套 1/√D；**「索引 0..2047=全量选择，稀疏接口≠此输入稀疏」明示**）→ 27.2 两段式为何先计划后执行（+图①；example 真实时序止于 sync/释放、无读回无对拍、PrintOutResult 未调用）→ 27.3 host 分层（包装/注册/规划/内核门四层各锚点；**三断点虚线**：Inner 实现体、soc↔宏映射、运行时选 bin；README 支持表=文档陈述非运行验证）→ 27.4 核内一日（**重点讲 syncC1V1 就绪对**，其余旗标一笔带过不堆号码；首尾排空；flash 跨块更新；「一对握手≠全内存安全证明」）→ 27.5 核验（E1/E2 分明；golden 两语义：索引重生成覆盖输入、v:=k截断隐含 D512；**覆盖如实：-1 终止/越界/空选集未触达**；「CPU 对拍只证 golden 数学=独立复算」；NPU pytest 未执行列复现步骤）→ 27.6 DSA 一段（复杂度限子集）→ 27.7 做了/没做+复现三档+快照。陷阱 5 条。脚注 8 组全仓库相对路径+行号。

## 研究矛盾统一（写前修订，均已落 EVIDENCE/OUTLINE）

H3 与 H0 冲突消除（清理不再重复，改「今后亦不做」）；OUTLINE「正确性来自 CPU」句改为三分（golden 数学/example/算子实现各归各）；E2 阈值 5e-2→2e-3 可解释化；覆盖未触达项明示。

## 边界与未决（供验收抽查）

1 例 27.2 代码为删节示意+`[需真机验证]`标签——样例本书未运行；2 图②边 label syncV1C2 等**只画数据就绪语义，未画 MTE 子管道差异**（PIPE_FIX/MTE3 已在脚注）；3 arch22 表述不映射商品型号；4 无任何性能数字（含 DSA）；5 ch27 未进 sidebar 单列（挂在 06-backend/index 列表，PM 如需独立入口请示下）；6 appD 第27章行已更新为实际锚点；`docs/06-backend/index.md` 标题同步去「可选」。

## 流程记录

源仓全程只读零写入零清理（两 worktree status=0，HEAD e75072d 未动）；渲染产物在 `/tmp/ch27-fig`；用户环境无新装包。候审。
