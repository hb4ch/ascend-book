# 全书执行状态

更新时间：2026-10-09。项目经理：当前Codex任务；主要执行者：tmux ascend-book-pi，模型(dgx) GLM-5.3-Flash-EXL3，禁止切换。

## 当前任务

**CH16 写作进行中**。任务文件：management/tasks/CH16.md。pi已完成P0源码基线及提纲，并补读U1–U5，正在生成完整正文和图。
请先观察tmux状态；Working期间不要重复派发、不要覆盖ch16文件。已创建持续调度 pi，每10分钟唤醒当前任务，读取本文件接续评审和派发。
本轮最新用户授权为“嗯，开始”，范围是完成全书及质量改善，无需每章询问用户继续。

## 已完成

- 源仓10个完整commit和dirty状态：SOURCE-BASELINE.md。
- 验收标准：ACCEPTANCE.md，经理已同步STYLEGUIDE和README。
- 来源检查脚本修复及2项回归测试，当前42文件236引用298展开模式通过；ch24两处后缀修复。
- ch11 UB bank容量与设备/流同步范围修复，SVG已渲染检查，npm run verify通过。
- PTO CPU GEMM真实执行通过，最大绝对误差1.19209e-07；validation/PTO-CPU-GEMM.md与三个日志。未进行NPU验证。
- P0证据已评审并提出7项修正：reviews/P0-REVIEW.md。方向通过，正文仍需独立验收。

## CH16评审须特别复查

- pi已修正文档中的主要口径，但CH16-EVIDENCE和P0-REPORT仍有残留：表内“六对事件”、bank判据“更严/问号”、报告“16 bank×8组”。不要把研究报告自称全部修复当成验收证据。
- 严格区分4类HardEvent与6个反向预置flag实例（分属2类）；设备路径输出GM不经过UB。
- Cube理论3022.92us对比aic_mac_time3076.396us；Task Duration4012.44us是另一指标；86.4%为Cube时间占比，不是峰值算力率。
- 输入B已在gen_data.py转置，DataCopyInB编译期分支控制布局参数，API没有isTrans运行时参数。
- 注意笔记中新出现的“256行×64KB→256行×64B”等编辑痕迹须清理；需要实际查看相关源文件。
- pi完整交付后检查正文脚注/图表与命令，再运行verify；报告在CH16-REPORT.md，日志validation/ch16-verify.log。

## 后续

CH16修订验收后派CH17（融合），再CH18（FA），之后按PLAN-COMPLETION阶段推进。下一章重要风险：融合不必然消除GM中转；matmul_gelu README与代码有Scenario1 GM中转和Scenario2 UB直通，按架构范围表述。不要把“共享UB”泛化。
按章本地提交；不自动push（main push会触发站点发布）。pi已被要求不自行commit/push，由经理验收后处理。

## 调度操作

写任务文件后，用单行 `tmux send-keys -t ascend-book-pi -l '请读取...并执行...'` 再单独发送Enter。不要直接多行paste任务（首轮只显示标题，已用单行补发）。正在工作时必要纠正会进入steering队列，避免重复催促。
默认exec沙箱在本会话遇到 `bubblewrap mountinfo path is not absolute`，已通过 require_escalated 的自动审查执行授权的只读/工作区操作；若再次发生按实际权限处理，不绕过拒绝。
图片view_image也遇同一错误；已通过rsvg-convert输出PNG并读取图片完成视觉检查。
所有调度进度写回本文件。仅章节完成/重大问题/失败/用户需行动时通知，正常等待保持安静。
