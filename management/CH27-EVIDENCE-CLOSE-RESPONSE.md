# CH27 补证回应 —— CH27-EVIDENCE-CLOSE.md 六条逐项

rev2（2026-10-10）。EVIDENCE 已升 rev2、OUTLINE 同步小修；未写正文。所有行号本轮亲读复核；两脚本+log 在 `management/validation/`。

**1 PrintOutResult/资源生命周期**——证实：定义于 example L45-56（含 D2H memcpy），**全文件无调用**（rg 仅定义处）。真实时序已全程读毕并写入 EVIDENCE C1：launch L216→`aclrtSynchronizeStream` L220→`aclDestroyTensor`×11→`aclrtFree`×9+workspace→DestroyStream/Context/ResetDevice/Finalize。「回读打印」说法废止；正文将明确 example 不读回不对拍。

**2 dtype 混写**——已改逐张量表（EVIDENCE A）：q/k/v/out/rope=fp16；sparseIndices=int32（host `iota 0..2047`）；softmaxMax/Sum=fp32（infertype 尾注亦显式 DT_FLOAT，C4）；actSeq=int32。rev1「全部 ACL_FLOAT16」错误收回。

**3 host→kernel 闭合**——不再以「三件套/2295 行」搪塞：亲读 op_api 包装（C2）、def 三 soc 配置（C3）、infershape 尾注（C4）、tiling 关键路径 DoOpTiling→GenTilingKey（位字段：pageAttention/layout/perfMode/gSize>64，C5）、perfMode 判据 blockSize≤4（C6）、kernel 入口+`__CCE_AICORE__==310`架构门控+fp16 `if constexpr` 分支+模板参与 tilingKey 一一对应（D1-D4）。主例 TND fp16 子路径追到 `op.Init(...tiling)/op.Process()`；**三处无法静态闭合的边（Inner 实现体/soc↔宏映射/tilingKey→bin 选择）明确列为虚线断点（C7）**，图①照此画。

**4 CPU 参考范围**——拆双路线（E）：E1=BSND 冒烟降级为「链路可跑」并注明未种子化；新增 **E2 同主例条件缩小版独立对拍**：TND/fp16/mode0/D512+rope64，numpy 独立实现（含索引收集/-1 终止/截断、平移 softmax），seed=20261010，shape+有限值断言，结果 max abs 2.48e-4（容差 5e-2，源于 golden bmm2 前 fp16 cast）PASS。**两个新发现如实入文**：golden 用未种子 randperm 重生成 sparse_indices 覆盖输入（L467-505）；v 被,k[..., :512] 顶替（L688，隐含 D=512——D=16 触发 shape 不一致实测）。均值/方差不再作为任何判据；无 NPU 不称闭环。

**5 源仓只读/依赖**——两脚本顶部 `sys.dont_write_bytecode=True`＋终跑 `env -u PYTHONPYCACHEPREFIX`；首跑产生的 `tests/pytest/**/__pycache__` 已全清（末态 0，`git status`=0），写入与清理记录于 H1，不以 git 干净证明零写入。tensorflow 留痕：`pip install tensorflow-cpu`→2.21.0 入 pyenv 3.12 site-packages（H2）；后续不再装环境。

**6 与 18 章的关系**——改为「关注集合」表述：稀疏注意力=索引/掩码改变参与的 K/V 子集（选择+mask 语义），非「差异不在数学」；O(Lk) 仅限选定子集后的注意力，索引器/选择开销另计（F 节收窄）。

附：`bash -n`/`py_compile` 校验过两脚本（COMPILE_OK）；源仓两仓 worktree 干净。
