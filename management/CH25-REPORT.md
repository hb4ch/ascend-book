# CH25 报告（写书轮，2026-10-10）

交付：正文 `docs/06-backend/ch25-pypto.md`（**4,927 字 / 中文 3,625**，verify 0 FAIL）；图①② mermaid 内嵌＋624px 实宽截图 `management/validation/ch25-{fig1,fig2}.png`；证据底稿 `CH25-EVIDENCE.md` rev2、回应 `CH25-EVIDENCE-CLOSE-RESPONSE.md`（前轮已交）。**未 commit、未动其他章、未换模型。**

## 结构（对应 OUTLINE rev2 精简版）

25.1 问题与四行主例（预期值标注非实测）＋图①四道工序 → 25.2 前端三约定（`[]`≠标量／out 无返回／tile 提示会被钳）→ 25.3 两级编译（Python 降 IR／C++ 切图，官方四层图原义，不列 pass 表）→ 25.4 生成码三层剖面（壳→TAbs→pto::TABS）＋PTO 头两渠道与 bisheng 门＋图② → 25.5 同一入口三种设备事实（`CFG_RUN_MODE` 定设备，非入口名）→ 25.6 边界/复现/未决清单 → 陷阱与注意 → 来源 13 条脚注全路径闭环（缺回链=0）。

## 任务书逐项落实（CH25-WRITE.md）

1. **单 abs 主例**：4 行有效代码开篇，输入 `[-1,-8,2]`、预期 `[1,8,2]` 明标「按 abs 语义推得的预期，本书未在本机执行」；断言仅 NPU 分支、CPU 仅打印（已回源 L84-104 核实）。
2. **尾块收窄**：只写机制（resolver「clamped to operand's own shape」＋容量/有效形状＋shape=有效/stride=原始），**明写「两 tile 值如何映射到一维、钳后各值需切图后 IR 确证，本书未生成该 IR，不给数字」**；3≤8 落有效区域标注为机制推演。
3. **cpp/编译分账**：文本拼接无条件、**落盘与 bisheng 编译同在 `#ifdef BUILD_WITH_CANN && ASCEND_HOME_PATH` 门内**（无 CANN 连 cpp 不落）；`CS_CODEGEN_INSTRUCTION` 只出 cpp 例外——「无 bisheng≠无 cpp」按实际分支限定表述。
4. **SIM 边界**：性能仿真无设备可跑／精度仿真依赖 CANN 分述；「SIM 无需硬件≠无需 CANN/工具链」点明；`LaunchKernelTorch` 双臂同名、设备事实由 `CFG_RUN_MODE`+CAMODEL 包装定（kernel_binary.cpp SIM→EslModelMemoryUtils 分支）。
5. **PTO include 两渠道**：显式注入受 `codegen_support_tile_tensor`（默认 false）门控、env=仓库根；头链（tileop_common.h:39 等）另述且明「不对所有模式泛化」；pto-isa 是否随 CANN 分发标注未核。
6. **路径完整**：脚注全部 `pypto/python/pypto/...`、`pypto/framework/src/...` 全前缀。
7. **本机边界**：正文与复现块明标①②已验（语法级）/③④⑤未执行；`PYTHONPYCACHEPREFIX` 定向 /tmp；构建只给副本流程（`cp -a` 后 build），无破坏源仓动作；遗留 ignored `__pycache__` 如实记录不清理。
8. **不罗列**：pass 全表/调试档位/CompStage 六值均一句带过入脚注。

## 图（mermaid 内嵌；mmdc 渲染＋Playwright 624px 实宽截图）

| 图 | viewBox→624 缩放 | 有效字号 | textContent 核签 |
|----|----|----|----|
| ①四道工序（TB 三段） | 675×1140→0.924 | ≈13.9px | 装饰/首调才编译/图优化 Pass/码生成门/run_mode+CAMODEL/三臂全命中 |
| ②三层剖面 | 678×596→0.920 | ≈13.8px | 内核壳/TAbs/OP_TILE_OP_ABS/exec-tile/pto::TABS/bisheng 门内全命中 |

截图像素校验：fig1 1800×1248（dpi2）、ink 1.0%，fig2 1090×1248、ink 2.7%，行列投影无空图；`extern "C"` 引号节点已改写避免 mermaid 解析错误（`["extern C aicore 签名"]`）。

## 校验记录

- `npm run verify` exit=0、0 FAIL：`management/validation/ch25-write-verify.log`（字数行 `4,927 字（中文 3,625）`）。
- bash 语法：唯一 bash 块 `bash -n` 通过，块存档 `ch25-write-fence.sh`。
- 脚注闭环：13 定义/42 回链、缺回链 0（脚本实测）。
- 事实回源抽查（本轮全部 rg/sed 实测）：L76 `global_run_mode`、`_peek_run_mode_from_argv` L33/L48、`assert_allclose(rtol=1e-3,atol=1e-3)`、entry.py:702/718 ValueError 与 :301 returns None、`KEY_ENABLE_COST_MODEL` backend.cpp:259、`UB_S0_E1024`/`get_imm` codegen_npu.cpp:448-483、`dav-c220-vec` :654、`TAbs` unary.h:400-405 四行宏+转发、pipeline 七步名、`RunMode` runtime.py:36-40、pybind11>=2.13.6（pyproject:13）、`--no_isolation`/`-c/--clean`（build_ci.py）。

## 终读自查（读回全文实文后）

- 终读发现并已修 4 处：`py.Tensor`→`pypto.Tensor`、`tileF`→`tileW`、`[^^12]`→`[^12]`、图② `extern \"C\" [aicore]` 节点致 mmdc 解析失败→改写；另 L76 注释补 `global_run_mode` 实名、CPU 分支措辞精确化、^2 行号精确化。
- 「四道工序」计数与节结构一致（前端约定/两级编译/码生成/分支执行）；无遗留 TODO/占位；无性能数字；无未实测冒充（预期/文档声明/推导三处均显式标注）。
- 未动 24 章及任何其他章；appD ch25 行已存在未改；源仓零写入（本轮检查全带 PYTHONPYCACHEPREFIX）。

## 遗留（等 PM）

- PM 验收正文；`new_ir` docstring 矛盾、pto-isa 分发、TAbs 专属展开、tile 配轴、精度仿真等价性五项未核已入正文 25.6 未决清单。
