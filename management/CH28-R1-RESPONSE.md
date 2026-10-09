# CH28 R1 修订回应 —— reviews/CH28-R1.md 逐项

正文 `docs/07-outlook/ch28-roadmap.md` 重写（status 待审）；EVIDENCE 升 rev4。仅动 28 章与证据/报告；源仓只读零缓存；未提交。逐项：

**1 PTO 路线图事实纠错**：实读 `pto-isa/README_zh.md` L177-192 路线图表（10 行×功能/描述/范围/进度）。正文 28.5 改为：以该表为**带目标时间的正式计划**实例，取两条 2026 Q2 项——集合通信扩展（Ccu/Roce 异步指令、TPREFETCH AIV 直驱）与 CPU-SIM 同步构建——讲「目标季度≠完成，完成看 ReleaseNote 后续版本条目」，并引其 master↔CANN 版本提示；「持续演进/规划中」条目=无目标时间只当方向。**废止**rev3「Unreleased 空白→记录纪律」推断与「pto-isa 无 dated 路线图」错误；PyPTO 改为「仅核对到 README 版本公告序列，未做全仓检索，不下无路线图结论」。EVIDENCE E2′ 同步重写。

**2 降密度**：开头拆三短段（问题→层级表→日期纪律）；全篇删【码】【发布】【推】标签，改 5 行小表（发布说明/官方指南/样例调用/实现细节/运行结果×本书走到哪层）；粗体仅存关键动词；「工业化/净新增/抽象层换算」等口号删除；每段一意。

**3 VF 表述**：改「公告新增 VF 路径打印/dump 接口+样例如何调用（核体内 `AscendC::printf`、`asc_vf_call` 进子函数）」，删「把 SIMT 能力补到 SIMD」沿革句；NPU Check 只写「本章仅据公告、未实现核验，快照内未见独立文档/样例」，不称全仓仅一句；删「host 仅 aclInit」绝对句，只说核体与 VF 子函数都在设备侧；CPU Debug 条件**准确列出** 950≥9.1.0/A3≥9.0.0/**A2≥9.0.0**（README L11-13）并注明仍需 CANN 工具链（`dav-2201/3510`）。

**4 代码块**：标「按样例简化的示意，非独立可编译程序；变量名与实参见原文件」；正文补「依赖由显式 `Mutex::Lock/Unlock` 与各级缓冲配对释放完成——抽象换掉指针运算，没换掉同步责任」；产品条件逐 README：tensor_api 版 **>9.1.0** vs 老范式 **≥9.1.0**（一个符号之差，各自 README 为证），不再用「样例族」。

**5 图**：改 `flowchart TD` 纵向五短节点（最长 14 字）；图注「按时间自上而下，相邻不代表依赖因果」。**真实页面截图**：vitepress build 后经本地静态服务用 Playwright 打开 `dist/07-outlook/ch28-roadmap.html` 实渲染页，svg 实测 232×411 CSS px（<624），5 节点 foreignObject 标签文本逐一提取核对、0 溢出，640px 视口 docScrollWidth=640 无横向溢出→`validation/ch28-fig1-page.png`（466×824@2x）；**像素文字可读性宿主不能目检，如实留 PM 视验**（DOM/几何层已核）。另存独立渲染 `ch28-fig1.png` 备查。

**6 脚注**：重排——^1 基线、^2 公告+指南+两 matmul 样例（各自 README 条件）、^3 VF/dump/cpu_debug 三样例全路径+条件、^4 书内 ch11 对账、^5 hixl/pto-isa/pypto；**全部完整路径无省略号**（`…/02_dump` 类缩写也展开为 `examples/01_simd_cpp_api/01_utilities/02_dump/...` 全拼）；PTO 发布说明写作 `pto-isa/ReleaseNote_zh.md`；FabricMem 标「适用 Atlas 800T A3 超节点」。正文锚点与脚注内容一一对应（调试段引 ^3/^4 已核）。

**7 结尾**：删「前段章节复核待后续」内部状态句；不承诺「每句话可溯源」；改为「各章示例可靠度以该章自己的验证声明为准；NPU 真机结果普遍缺位且如实标注；CPU 侧与 PTO 仿真仅覆盖各自声明范围；本章样例全部止于源码实读」——不扩大覆盖口径。

**验证**：`npm run verify >/tmp/ch28-r1-verify.log 2>&1`，**EXIT=0**（build 12.3s 首跑+复跑核真值；internal 42 文件 OK；source 463 引用 0 无效；terms 唯一 warn 在 ch24 既有文本非本章）。字数 3,147/中文 2,465（word-count 实测）。
