# CH17 交付报告（CH17-REPORT）

> 2026-10-09。任务：management/tasks/CH17-WRITE.md；证据：CH17-EVIDENCE.md（含 PRECHECK 落实补记 §八）；提纲：CH17-OUTLINE.md（已按经理六条修正执行）。status=待审；未 commit/push；未动 ch16/README/全局计划。

## 交付物

| 文件 | 说明 |
|---|---|
| `docs/03-ascendc/ch17-fusion.md` | 正文，**8,544 字/6,049 中文**；8 节+陷阱表+小结 |
| `docs/figures/ch17-mix-core.svg` | 图 17-1 逻辑核解剖＋CrossCount 配对（XML 校验过） |
| `docs/figures/ch17-workspace-ring.svg` | 图 17-3′ 环形 slot 深度 1/4 对照（HTML 内联嵌入已验证） |
| `docs/附录/appD-source-map.md` | 仅替换第 17 章行为文件级路径（未动其他行） |
| `management/validation/ch17-verify.log` | verify 全绿：内链 42 文件/check-source 247 引用 0 无效/术语无违例 |

## 七项必讲落实对照

1. **收益条件/三收益/两通路分架构**：§17.1 三收益+自查三问+不适用四条；§17.4 GM 中转（L2=观测非契约）vs UB 直通（仅 950）。
2. **matmul_gelu 分工/走查/双 AIV/单向通知/未证复用**：§17.3 走查②②′②″②‴四级递进；xUB 复用全程「源码未显式给出保护证据」，无「未显现错覆」表述，无自然错位猜测断言。
3. **quant 公式链/分组调度/实际参数/非随路反量化**：§17.5 公式、host 实参全表（L611-637）、groupList/preCount 走查④④′；反量化明确为「UB 内五步指令链」非 Fixpipe 随路。
4. **环形 workspace 生命周期**：§17.5 走查⑤⑤′+地址算例+图 17-3/17-3′+mermaid 时序；回执=PIPE_MTE2 读毕（非计算/输出完成）三处一致；两 AIV 回执配对与 PostCompute 排空单独成段；BUFFER_NUM≠DEPTH 对照样。
5. **性能纪律**：§17.6 同架构同shape表×2；最低版本≠测量版本/950DT 无数据/测量 CANN 版本未知均如实；「Task≈max」标注为理想模型；vec<mac 判定标注「README 对该样例的判定」；无跨 kernel 相加加速声明。
6. **真实构建链**：§17.7 命令逐字取自 README/CMakeLists（demo/verify_result.py/sim/清缓存）；「本书未运行」明示；短码[需真机验证]标注、示意段删节说明。
7. **生产库**：仅 7 算子目录实名+「无 quant 类」事实；graph_fusion 分层辨析。

## 提纲修正六条落实

删「未显现错覆」✓；GM/L2 非两通路✓（17.4 重写）；F322F16 vs Cast 对比删除、实际类型转换按两样例分别陈述（fp32 出=Fixpipe ROW_MAJOR 直写；fp16 出=Cast 指令，无「随路量化」表述）✓；Task≈max 降级为理想模型✓；GetTensorC 实参逐字符（`mmOutGlobal[off],0,true`）✓；FasterGelu sharedTmp 重叠约束按文档 L91+「复用已消费区」解释✓；图示 depth 用实际 1/4✓。

## 自审检查记录

- 脚注 used/defined：7 枚举全≥2 次出现（定义+正文引用），HTML fn-ref 12=backref 12。
- 图文同步：2 SVG alt 中英双语、mermaid 4 处渲染、图号连读（17-1/17-2/17-3/17-3′/17-4）。
- 数字复核：workspace 容量 12MiB/32MiB、slot 128/256KB、A2 gelu 表 mte2 316.672→90.314?——**已按 README 原值 90.315 校正**；950 mte2 320.543/57.145/0.005 三处一致。
- 交叉引用仅指向 ch10/14/15/16 既有小节，未改动其内容。

## 覆盖情况声明（ACCEPTANCE：低于深度目标须声明）

**6,049 中文 < 8k 深度目标**。原因：两样例机制面（2×~700 行核心码）可证事实已全覆盖；继续扩将进入 U 级未证推测或重复 ch15/16。若经理判定须至 8k，建议扩容方向（预留于正文结构中）：①17.3 增加 2201/3510 CopyOut 全分支逐行对照表；②17.5 增加 AscendC 高阶 Matmul 对象生命周期（Init/UpdateTiling/End）与本例裁剪；③17.6 增加msOpProf 字段释义附表。请经理裁量。

## 未验证事项（正文已标注）

U2 xUB 复用保护（待真机/改造实验）；U4 GetTaskRation 契约（仅样例用法）；尾块奇数行整除；测量 CANN 版本；950DT 数据缺；两样例均未运行（无本机 NPU）——复现入口已给全。

## 残余问题

1. `CrossCoreSetFlag<0x2,…>` 模式位与 `CrossCoreWaitFlag` 无模板的配对细节在旧架构的精确阻塞范围，文档未给表——正文按「950 生效/旧架构不生效」二元表述，未细化到每代。
2. matmul_gelu A2 表 aiv_vec 174.327 与单独 236.506 的差额解释采信 README L2 观测口径，未独立验证。
3. STATUS.md 出现非本轮改动（PM 域），未触碰。

---

## 附录：R1 退修（2026-10-09）

八组全改，逐项见 `CH17-R1-RESPONSE.md`；证据表补 §九。正文 9,147 字/6,426 中文。verify 日志 `validation/ch17-r1-verify.log`（内链 42/check-source 250 引用 0 无效/术语无违例）；脚注 used/defined 复核 9 枚举全配对；图 alt 与正文同步（上下半块）。未真机验证项保持标注。仍待审，未提交。

## 附录：R2 复查收口（2026-10-09）

八组按实际正文修订：stride 去重、GELU 全函数真码、单向段猜测清除、同步计数表述、可复制命令（SRC 变量）、观测化措辞、950PR 限定、SVG 时序措辞。逐项摘录见 `CH17-R2-RESPONSE.md`；日志 `validation/ch17-r2-verify.log`。仍待审。
