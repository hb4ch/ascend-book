# CH25 R1 回应

2026-10-10。逐条对应 `management/reviews/CH25-R1.md`；每条给**终态实际改句**（引号内为正文原文）与回源行号。仅动 `docs/06-backend/ch25-pypto.md`（status 已改 `待审`）与本回应；未提交。

## 1. cpp/门控逻辑重构（P1）

删除原「无 bisheng 不等于无 cpp 在这里不成立」绕口句。25.4 现按内存文本/文件/二进制三层分述：

> 「**文本、文件、二进制，三层分开看。**CCE 文本始终拼入内存缓冲（`GenCode` 内 `leafKernelFunc`，无任何门，codegen_npu.cpp:281-283）；`#ifdef BUILD_WITH_CANN` 且 `ASCEND_HOME_PATH` 已设时才进 `GenCodeToBinaryTask`（:293-298）……`DumpCode` 另受 `KEY_FORCE_OVERWRITE`——默认 true，fixed-cce 模式例外——控制，文件已存在可不重写」
> 「**文件落盘不等于二进制成功**：`DoCompileCmd` 失败会 ASSERT 并打印完整命令（:490-499），此时 cpp 已在、`.o` 没有——缺的也可能是编译器而非门。」

CS_CODEGEN_INSTRUCTION 门控归属已写明：

> 「`COMPILE_STAGE=CS_CODEGEN_INSTRUCTION` 的语义是**门内截断**：`CompileCode/ExecuteParallelCompile` 入口直接返回（:492、:835），前提是外层门已让 cpp 落盘；门关闭时连这一步都没有。」

回源：`codegen_npu.cpp` L270-315（GenCode）、L370-383（Task）、L385-417（Dump/ForceOverwrite）、L490-499/L833-835（CS 截断+ASSERT）。图①同步改为显式门判断节点＋「文本止于内存」否臂。

## 2. 配轴论断收窄（P1）

- 主例注释：`# tile 形状提示：末轴 8 个 float` → `# 切分粒度提示（最终配轴见 25.2）`。
- 25.2 结句改为（删「3≤8 落一块」推导）：

> 「但 resolver 注释是通用规则，**本例两个 tile 值最终落到哪些轴、钳制后各是多少，必须看到切图后的 IR 才能确证——本书未生成该 IR，不给数字，也不推断单块还是多块**；能核的只有约束侧：8 个 float 恰为 32B，满足尾轴对齐要求」

## 3. run_mode 顺序与 env 语义（P1）

25.5 改为谓词链时序＋覆盖语义：

> 「先看 `CAMODEL_LOG_PATH`，非空**当场把 run_mode 覆写为 SIM**……覆盖发生在判定链最前」
> 「run_mode 的初值在此前已定：用户显式选择，或按 `ASCEND_HOME_PATH` 推断（此时还要求 `torch.npu.is_available()`……）——CAMODEL 覆写发生在执行入口、后于初值」
> 「代码里 `cann_is_configed` 这类命名只检查**环境变量存在**：env 在 ≠ CANN 完整安装 ≠ 编译工具链可用，代码未做更深探测。」

回源：`entry.py` L641-643（CAMODEL 首行覆写）→L648（NPU 判）→L651-656（acc2&&env→LKT）→L657-663（else cost model），顺序与正文/图①一致。

## 4. UnaryCompute 真实分支（P1）

25.4 整段重写为回源结果（不再用 TSinh/TCosh 类比，rg=0）：

> 「`TAbs`（:400-405）转发 `UnaryCompute<UnaryOp::ABS>`（:124-156）。后者先读目的操作数布局的前三维，任一为 0 直接返回（:126-131）；随后分两叉——若 `IsConstContinous<T0,T1>()`（**编译期**判定：静态布局且外层 stride 等于非首轴合并尺寸，`utils/layout.h:349-367`）成立，单次 `TASSIGN` 绑定定长 tile 后直接计算，**无循环**（:135-142）；否则进三重循环，循环边界 `shape0/1/2` **运行期**取自 dst 布局——动态 shape 时即有效形状……两叉殊途同归进 `UnaryComputeImpl` 的 ABS 分支（:62）：`PTO_WITH_LAST_USE(pto::TABS(dst, src), n1, n2)`」
> 「**主例走哪个叉取决于模板实参的编译期判定，本书未生成 IR，不断言**；此前『循环次数 pass 期已定』的旧说一并收回——通用叉的循环边界是运行期形状。」

图②重画为 码生成(host 文本)→外部编译(bisheng, 可失败仅剩 cpp)→设备侧真分叉（IsConstContinous?→单次/循环→ABS→TABS）；bisheng 移出设备层。`pto_tile.h:25-27`（last_use 宏两版）、`:306-343`（exec-tile）入脚注 9。

## 5. 全称收窄（P1）

- 「任何形状都能过」→「空 shape 只跳过形状比对这一项，连续性、输入个数等其余校验照常执行，本注解实际新增的约束只有 dtype」。
- 能力边界段拆为三个短段（动态形状/校验范围/同步内存），限定语「按已核路径陈述，不作全称」「已核链路……链上其余环节未逐一核」「此两点已核」；**FP4/NZ 清单整句删除**（细目存 `CH25-EVIDENCE.md` §G）。
- 「动态形状全链自动」「用户层不可见」等全称表述已随拆分消失（rg 验证）。

## 6. 两图重制

- 图①：删三段 `~~~`，改单一动作箭头链＋真实谓词节点（`BUILD_WITH_CANN 且 ASCEND_HOME_PATH?`／`CAMODEL_LOG_PATH?`／`run_mode==NPU?`／`acc==2 且 env 在?`）；**不写「SIM+精度→Esl」**——LaunchKernelTorch 节点标注「设备由 C++ CFG_RUN_MODE 定」，cost model 单列。mmdc 渲染过、624px 内（natural 594×1876）。
- 图②：如上重制（natural 560×1159）；长类型/位域标签（`UnaryComputeImpl` 模板参、位域）移脚注 9，节点只留短动作。
- 截图（全高、非视口截断）：`management/validation/ch25-fig{1,2}.png`（1188×3750 / 1118×2318 @2x；ink 1.39/1.76%，末行内容距底≥50px 非裁切）。

## 7. 路径/纪律/杂项

- 复现③改：`WK=$(mktemp -d) && echo "WK=$WK"`＋`cp -a … "$WK/pypto"`——不再固定 `/tmp/pypto-build`（嵌套复制坑）；「本机未满足依赖，仅给流程」保留。
- 正文删去 pycache 历史与「不清理源仓」纪律句（rg：正文仅余复现命令里的 `PYTHONPYCACHEPREFIX`）；此类记录只在报告/回应。
- 脚注短路径全展开：`pass_registry.h:36`→`pypto/framework/src/passes/pass_mgr/pass_registry.h` L36（同 pass_manager.h）；`codegen_npu.h`→`pypto/framework/src/codegen/npu/codegen_npu.h`；`tile_shape_verifier.h`→`pypto/framework/src/interface/operation/tile_shape_verifier.h`；`tileop_shmem.h`→`pypto/framework/src/interface/tileop/tileop_shmem.h`。新增 `utils/layout.h`、`vector/pto_tile.h` 全路径。
- frontmatter `status: 成稿`→`待审`。
- 未跑命令如实标注：③④⑤「本机未满足依赖，仅给流程」；预期输出标注「未在本机执行」。

## 校验记录

- `npm run verify` exit=0、0 FAIL：`management/validation/ch25-r1-verify.log`（字数 `5,265 字（中文 3,819）`）。
- bash-n：`management/validation/ch25-r1-fence.sh`（含 mktemp 版）通过。
- 定向语法检查：`PYTHONPYCACHEPREFIX=/tmp/ch25-pycache python3 -m py_compile docs/06-backend/ch25-pypto.md` OK（pyc 不落源树/书树）。
- 终读实文核对：`任何形状都能过`/`用户显式指定 >`/`3 ≤ 8`/`TSinh`/`[^^12]`/固定 `/tmp/pypto-build` 均 rg=0 或已改；`待审` 在 frontmatter。
