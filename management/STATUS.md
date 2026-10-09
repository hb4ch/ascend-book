# 全书执行状态

更新时间：2026-10-09 13:05（北京时间）。项目经理：当前Codex任务；主要执行者：tmux ascend-book-pi，模型(dgx) GLM-5.3-Flash-EXL3，禁止切换。

## 当前任务

CH17已通过源码与文稿审查，准备按章提交推送；最终依据reviews/CH17-ACCEPTED.md，旧响应报告只保留为过程记录。CH18原pi正在按tasks/CH18-WRITE.md写正文，保持GLM-5.3-Flash。经理负责后续独立审查；不得修改活动文件。用户已授权验收后推送origin/main。

## 已完成

- 源仓10个完整commit和dirty状态：SOURCE-BASELINE.md。
- 验收标准：ACCEPTANCE.md，经理已同步STYLEGUIDE和README。
- 来源检查脚本修复及2项回归测试，当前42文件236引用298展开模式通过；ch24两处后缀修复。
- ch11 UB bank容量与设备/流同步范围修复，SVG已渲染检查，npm run verify通过。
- PTO CPU GEMM真实执行通过，最大绝对误差1.19209e-07；validation/PTO-CPU-GEMM.md与三个日志。未进行NPU验证。
- P0证据已评审并提出7项修正：reviews/P0-REVIEW.md。方向通过，正文仍需独立验收。

## CH16历史评审要点（已收口，最终以CH16-ACCEPTED为准）

- pi已修正文档中的主要口径，但CH16-EVIDENCE和P0-REPORT仍有残留：表内“六对事件”、bank判据“更严/问号”、报告“16 bank×8组”。不要把研究报告自称全部修复当成验收证据。
- 严格区分4类HardEvent与6个反向预置flag实例（分属2类）；设备路径输出GM不经过UB。
- Cube理论3022.92us对比aic_mac_time3076.396us；Task Duration4012.44us是另一指标；86.4%为Cube时间占比，不是峰值算力率。
- 输入B已在gen_data.py转置，DataCopyInB编译期分支控制布局参数，API没有isTrans运行时参数。
- 注意笔记中新出现的“256行×64KB→256行×64B”等编辑痕迹须清理；需要实际查看相关源文件。
- pi完整交付后检查正文脚注/图表与命令，再运行verify；报告在CH16-REPORT.md，日志validation/ch16-verify.log。

## 后续

CH17研究后写融合正文，再CH18（FA），之后按PLAN-COMPLETION阶段推进。下一章重要风险：融合不必然消除GM中转；matmul_gelu README与代码有Scenario1 GM中转和Scenario2 UB直通，按架构范围表述。不要把“共享UB”泛化。
按章本地提交；验收后及时push到origin/main（用户已授权并知悉会触发站点发布）。pi已被要求不自行commit/push，由经理验收后处理。

## 调度操作

写任务文件后，用单行 `tmux send-keys -t ascend-book-pi -l '请读取...并执行...'` 再单独发送Enter。不要直接多行paste任务（首轮只显示标题，已用单行补发）。正在工作时必要纠正会进入steering队列，避免重复催促。
默认exec沙箱在本会话遇到 `bubblewrap mountinfo path is not absolute`，已通过 require_escalated 的自动审查执行授权的只读/工作区操作；若再次发生按实际权限处理，不绕过拒绝。
图片view_image也遇同一错误；已通过rsvg-convert输出PNG并读取图片完成视觉检查。
所有调度进度写回本文件。仅章节完成/重大问题/失败/用户需行动时通知，正常等待保持安静。

## 本轮评审结论

R1独立核查确认流水图提前写回、UnitFlag控制模式混为flag值、性能数据跨架构混用、错误LoadData分支、错误2046B写成2022B、构建脚本不存在及关键脚注未引用。详见CH16-R1.md。本轮未验收、未提交正文，不进入CH17。

## 13:10 调度检查

pi仍正常Working，模型未变；正文已增修至约34.7KB，正在重画R1要求的流水图，尚无CH16-R1-RESPONSE.md。未重复派发、未打断、未覆盖活动文件，待完整交付再审。

## 最新收口

CH16 R1后经理收尾已验收，前述退修信息保留为历史。第17章重点待核：matmul_gelu是否存在UB复用反向握手，不能从单向通知推断通用无竞态；按CrossCore文档核查并陈述样例边界。

## Git与远端授权更新

用户已要求按章使用git并及时推送remote，取代此前不自动推送偏好。2026-10-09尝试推送已验收提交4e583b0、0a7e569到origin（git@github.com:hb4ch/ascend-book.git）的main分支，被自动审批以具体目的地与数据范围未明确授权拒绝。已请求用户确认该仓库与已验收提交范围；确认前不重试、不绕过。CH17工作区未提交，不包含在本次推送中。

## 远端推送确认

用户在明确具体仓库与main分支后再次授权推送。已成功正常推送26ed47f..0a7e569到git@github.com:hb4ch/ascend-book.git main，包含4e583b0及0a7e569。前述审批阻断已解除；后续由经理在验收后按章提交并及时正常推送，不强推，不纳入活动未审文件。持续调度规则已同步。

## 13:47 CH17首次评审

完整交付约6049中文，独立阅读发现quant场景误写UB直通、性能错列及无依据归因、GELU公式/指令错误、行切分错误、同步复用未证却写成无症状、来源脚注不完整。已派reviews/CH17-R1.md退修，未验收未推送本章。等待CH17-R1-RESPONSE及修订验证。

## 13:57 CH17 R1复审

R1已交付，场景串用已改；实际正文仍有重复错误因果、最优断言、单tile建议等残留，并新增伪真码和shell目录错误。经理已回源并发reviews/CH17-R2.md，待R2逐项摘录对账与验证，尚未验收推送。

## 14:07 R2交付与任务交接

R2已交付但仍有残余：GELU标准式误写xσ(x)、报告声称复制全函数而正文仍仅指令列表；BroadCast维度被误写Brcb广播轴；环图深1被绝对称无重叠。经理接管CH17正文/图/appD收尾并独立验收，未验收未推送。原pi已派tasks/CH18-RESEARCH.md，仅研究18章，避免与经理写入冲突。

经理已修复GELU定义并复制真实完整函数、BroadCast维数/轴、深1重叠图示和shell变量缺失防护；ch17-manager-verify.log中构建/链接/来源/术语通过。仍需完整收尾审阅和SVG渲染后才验收，当前未推送。

## 14:17 调度

CH18研究已交付，主线仍有12项未闭，已派tasks/CH18-EVIDENCE-CLOSE.md补闭精度/同步/Tiling/递推并实际执行数学对拍；暂不派正文。CH17经理继续收尾，补纠基础Mmad与高阶配置混淆、负分组无依据支持、地址MiB算例和时序图措辞。

两幅SVG已实际渲染查看：ring可读；mix一行标签越框，已缩短并澄清4+2为flag实例。CH17尚待最终全文审查、重跑验证及提交，未宣称验收。

## 14:27 调度

CH18补证已交付，但末块归一化、固定模板选择与数据面buffer释放仍缺实际链路，已派tasks/CH18-FINAL-GAPS.md精确追踪，不接受自行标成非主线。数学脚本已读，未将数学等价当kernel验证。CH17来源路径已完整化，继续最终验证。

14:27经理重跑：CH17 verify通过（252引用、333展开路径、0无效；约6651中文），diff检查通过；CH18 NumPy数学对拍独立重跑PASS，日志validation/ch18-online-softmax-manager.log。CH17最终验收记录与提交尚未完成，保持待审。
