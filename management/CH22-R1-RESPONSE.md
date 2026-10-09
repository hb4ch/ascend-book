# CH22 R1 RESPONSE——逐条实改（2026-10-09）

对象：`docs/05-comm/ch22-hixl.md`（修订后 **10,277 字 / 中文 7,860**）＋`CH22-EVIDENCE.md` rev4。verify 0 FAIL（`management/validation/ch22-r1-verify.log`）；复现块 bash -n 通过（`ch22-r1-fence.sh`/`ch22-r1-bashn.log`）。逐条：

**1. 性能错列与伪因果**：22.7.3 重写——读数表（A3 单机 FabricMem D2rD：16K/128K/1M/2M × AICPU 16.113/125.744/170.514/165.513、Host展开 2.874/22.602/**175.102**/181.431），156.698 标明为 rD2D；**170.514/16.113≈10.58 倍**（原「四十倍」删）；**1M/2M Host 展开反超、差距集中 16K–256K**。删「近一个量级/结构直接投影/框架应尽量 device 组织/开销固定/聚合对策」等因果，改「表只证明格子读数，不反推规律」；22.8.1 同步订正。EVIDENCE §13.8 存实核行号（performance.md L25/L30/L43）。

**2. 批量空 client 与 ret/status**：22.6 三层表与正文逐分支重写——①client==nullptr→**仅 erase+continue 无结果**（原「FAILED+erase」错）；②入 `disconnected_engines` 的条件=**查询调用 ret≠SUCCESS**，≠status==FAILED、≠断链成功，且 AutoDisconnect 返回值 `(void)` 忽略（显式模式空转也入集合）；③单条：**调用失败才 AutoDisconnect（返回值被检查），status FAILED 仅 erase**（原「FAILED→AutoDisconnect」笼统句删）。三推论段重写：去「永远诚实/唯一账本/任何层不认识」，改成分支事实表述。EVIDENCE §13.5 同步 rev4。

**3. 自动模式重试**：22.5 重写——「失败后直接重试成立」句删；重建前提改五分项（对象重建/在途访问/注册有效/数据一致性/重放策略），**「老指针通常可行」「重传整块最简单」删**；心跳句改「10 秒为默认间隔，非检测上界，不断言次序」；TIMEOUT 复用句改「应用核对前不得假设，策略应用定」。

**4. quickstart 收尾**：22.3.2 删「能工作靠经验错开」「预期非故障」（22.3.3 观测点段同步改中性「可见表现」）；建议段仅留「Disconnect 成功后额外 TCP 确认」并**明标非源样例**；**GetAsyncConnectStatus 轮询建议删**（新增证据：它只读本端连接池 `task_result_`，hixl_impl L173-176/connect_pool_executor L128-133，观察不到 server 入站——EVIDENCE §13.8）；mermaid 收尾改 `par/and` 并行区表达窗口。

**5. 范围与无证归因**：22.6 开头加「限 CS DIRECT，UB/legacy 不外推」；「不产 TIMEOUT」加同限；「省守护线程设计出发点」改「与实现一致，取舍无陈述不归因」；reserved「版本演进兼容策略」意图句改「仓内未说明，不作推断」。

**6. 泛化修正**：HCOMM 改「以集合通信为主（亦含单边，见 ch21）」；LLM 默认后端改三分句（pull 默认 adxl/push 默认 HCCL——cpp/README L79/L93 原文行号入脚注；接口文档仅承诺可选；A5 仅 CS+UB）；「各层状态独立」改限定语。RegisterMem 快照论断限定为**已核 CS 链**（Engine→server+mem_map_；client 视图=建链时 SetLocalMemInfo 快照+GetRemoteMem prefetch+BatchValidateMemoryAccess 双端校验，均具名），不以 rg 无命中证全局。

**7. 复现与脚注**：复现块加「记录 `$WK`、两终端同一副本」与「bash -n 仅语法」注；frontmatter→`待审（R1 修订中）`；脚注全展开——^L 三处目录引用改实文件（含中文名博客 md 实核、python/README.md），^J fabric_mem 目录改三个实文件头；全文无 `.../` 省略路径（脚本核过）。

**8. 自相矛盾与示意代码**：陷阱 8 重写为三分类（调用失败/终态 FAILED/未终态 WAITING 可再查；消费后再查=新错误 PARAM_INVALID）；22.6 示意查询块加注释「先查提交/查询返回码；FAILED≠可立即重试（见 22.5 五分项）」，去失败即重试暗示。
