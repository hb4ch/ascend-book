# APPC-REPORT —— 附录C 审查与改写（2026-10-10）

任务：management/tasks/APPC-REVIEW.md。证据：`APPC-EVIDENCE.md`（入口存在性逐条 ls＋旧版问题清单＋外链来源）。

## 改写要点

1. **按读者任务重组**：11 行任务入口表（认识 NPU/写算子/具体算子/硬件边界/性能诊断/调试/集合通信/单边传输/推理部署/后端 PTO/生产算子仓对照），每行=首选入口（本地完整路径）＋读什么＋先备（本书章节/前置文档）。
2. **本地/外链分置**：本地入口全部快照实 path；外链单列「仅来源说明」节（hiascend 徽章 asc-devkit README L7/L47、gitcode cann 组织、mssanitizer/asc-tools/release-management 页内引用），**均标「未核验」，不声称可达/最新**。本任务未联网。
3. **删除虚构/含糊**：pyasc/pyto-gym（仓内无实体）、工具杂列（VS Code 插件/pandoc/pagedjs）、meetup/B站无锚条目、blogs 省略号堆砌——全部清除或改为实路径。
4. **非安装文档**：全篇无安装命令；环境问题指向附录 A、证据映射指向附录 D。附录 D/E 未动；glossary/appB 未动（经理接管）。
5. **仓 README 一览表**：10 仓一句话定位（本书转述）＋对应章节，替代旧「GitCode URL 列表」。

## 验证

- `npm run verify >/tmp/appc-verify.log 2>&1` → **EXIT=0**（42 文件；536 引用 0 无效；warn 1 处 ch24 定版原文）。
- `docs:build` EXIT=0（两次：改 index.md 前后）。
- 附录索引页 `docs/附录/index.md` 同步更新标题与描述（一行）。
- **真实页面截图**：dist 重建后 8925 端口元素级——`management/validation/appc-{page-top,tbl-tasks,tbl-readme}.png`（页面 h2 结构：按任务入口/仓 README 一览/外部站点；服务已关）。
- 源仓只读（asc-devkit/learning-hub status=0）；未提交。

---

# APPC-R1 修订（reviews/APPC-R1，2026-10-10）

1. **域名**：hiascent→**hiascend**；外链 href 逐个取自本地仓内原文并注明 README 行号（asc-devkit L7/L47/L202、runtime L94/L133/L172、ops 三仓 clone 行、pto-isa getting-started L93、hub L42-43、npu_board_debug L60、show_kernel L3）；未联网，页面标「未在线核验」。
2. **假路径→实文件**：conv 教程实为 `01_conv_basic_operator_development/` 子课程（verify 抓出并修正）；`19-01/19-02` 全名；npugraph_ex/scalar 博文到具体 .md；**内容实读**（直调版/hccl 教程 README 原文摘引入提示）——非仅 ls。
3. **三列短表**（目标/入口/阅读提示）：Playwright 实测 `cols=3`；完整路径入脚注 [^1]–[^17]；正文短名+可点击外链（页面 https 链接 25 个、脚注区渲染正常）。
4. **「虚构」改口径**：pyasc 等改「本次未纳入核验，资源不在本地不代表不存在」（EVIDENCE R1 节）。
5. 验证：verify EXIT=0（555 引用 0 无效，含 appC 新脚注路径）；build EXIT=0；截图 `appc-r1-{page-top,tbl}.png`（8926 已关）。源仓只读；未提交；B/D/E 未动。

---

# APPC-R2 收口（reviews/APPC-R2，2026-10-10）

1. **深链化**：任务表 12 行入口全部改为**快照 commit 深链**（blob/tree，19 个；commit 取自本地 git rev-parse，与 SOURCE-BASELINE 一致），并明示「由本地路径构造、非原文绝对 URL、未在线核验」。逐链接脚本核验：18/18 路径存在且 commit 匹配（asc-tools 为原文 master 链，仅引用）。仓库主页链接不再承担文档入口（Playwright 实测主页型链接=0 于正文表）。
2. **伪路径清除**：脚注全文件名（npu_arch_2002/2201/3510 各自全拼；无 `...`）；conv 落子课程目录；hixl/npugraph 博文落 tree 目录（中文文件名避免 URL 编码噪音，文件名在脚注）。
3. **删 [^14]/[^15] 旧残**（截断 ai.gitcode URL、行号流水账）；ai.gitcode 在线体验不再单列（hub README 表内引用，未核验声明统一）。新脚注 [^1]–[^15] 全被引用（含 [^14] 修复未引用问题、[^15] commit 清单）。
4. **官方站点段**：4 短名可点链接，出处只记文件不记行号；hiascend 链接 5 个（原文 URL）。
5. **先备修正**：硬件行先备=第 2 章（原误 3 章）＋进阶 11；msSanitizer 限制（仅 SIMD）与验证边界（官方指南）保留原文。
6. 验证：verify EXIT=0（557 引用 0 无效）；build EXIT=0；截图 `appc-r2-{page,tbl}.png`（8928 已关；deep=19/homeOnly=0/fnFoot=true/hiascend=5 实测值）。源仓只读；未提交；D/E/B/index 未动。
