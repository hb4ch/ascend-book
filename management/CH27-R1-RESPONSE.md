# CH27 R1 修订回应

rev4 正文（4,979 字/中文 3,856）；status→**待审**。逐条对账如下；行号均本轮对最终正文实读复核。

**1 同步主线与双向握手**——27.4 重写为五阶段+双向握手专段：`MergeKv` 前 `WaitFlag(3)`→工作区写毕 `SetFlag(syncV0C1)`（V→C 就绪）；Cube `ComputeMm2` 用毕 `SetFlag(3)`×4（L889-893 区段）→下一轮 `MergeKv` 前 `Wait(3)`（L879）——**同一组缓冲的释放回执**，两方向生产/消费行号齐备。同 flag 生产/消费配对全部改写明：syncC1V1=Cube mm1 产/Vector Vec1 用；syncV1C2=Vector 产/Cube mm2 用；不再混对。图②补两条 `旗标3 复用回执` 虚线回边（MM2→M、MM2→S3），渲染确认 dotted path 与标签存在。「保证流水不悬挂」删除，改「该流水按此协议推进的代码证据，不是全部内存访问无竞态的证明」。

**2 纯 host**——27.2 改「按接口职责读」：校验/规划/答 workspace 尺寸/出 executor；**明写不能断言纯 host**（Inner 在算子目录外未闭合，是否触设备未追）。27.3 开头改「组织归属陈述，非已证运行时调用顺序」；「水位标记」→「模板选择键」；图① B 节点改「校验与规划」。

**3 资源释放**——改为 9 笔数据缓冲＋条件 workspace 一笔；**actSeq 两缓冲未显式释放**如实写出并注明「样例此处有省略，完善版应补 aclrtFree 与逐返回值检查，不宜照抄为完整范本」；代码块头标「调用顺序示意，据样例删节并省略错误处理」。

**4 核数与缓冲下标**——「双核」→「两类核」（Cube/Vector），1:2 配比不写死；mm1 环下标 `loop % preLoadNum`、mm2 `bn2IdxInCurCore % preLoadNum` **分别照实写并注明不是同一表达式**；两层环形组合时序未证亦写明。

**5 golden 限定**——所有 golden 结论限定「实际走过的 `compute_cpu→_t_increattention_bnsd` 路线」；「唯一权威」删除，改「就本书证据而言，NPU 侧 pytest 对比是验证途径（本书未执行）」，并加前提句：对拍成立以**独立参考与接口语义一致**为前提（逐条对齐但解释仍有出错空间）。

**6 复现**——27.7 重写为读者操作：两条可复制命令（书仓根相对路径 `management/validation/ch27-sfa-tnd-refcheck.py` 与 `management/validation/ch27-sfa-cpu-golden.py`）＋**依赖口径改「两条路径相同：numpy/torch/tensorflow」**（E1 经 golden 链同样导入 tf，已核）；pip 表述改「无版本钉，装入 2.21.0」（脚注 ^7 同步，与 EVIDENCE H2 一致）；阈值句加「针对本次输入的经验上限，换输入须重测，非通用误差界」。

**7 脚注**——^2–^6 补全 `ops-transformer/attention/sparse_flash_attention/` 前缀（^1 本有；全章前缀出现 6 处）；^8 中文顿号改实存目录名 `dense_lightning_indexer_{grad_kl_loss,kl_loss_grad}` 等＋「名字以仓内实存为准」。正文「三断点虚线」改「文字标注未追溯，不画进图」——图内本无这些边，不再谎称。

**8 可读性**——「章首一句：」标签删；「正文必须交代」改平叙；源树 pyc 管理史退出正文（仅存 `CH27-KERNEL-CLOSE-RESPONSE.md`/EVIDENCE H0）；27.4 长段拆 5 阶段+握手+边界三段；27.7 攤读者操作；status 待审；选型评审口吻无残留（27.1 直入参数）。

**验证**——`npm run verify` 直接重定向 `/tmp` 后查真实 exit：**EXIT=0**（build/internal-links/source/terms/word 全过；「昇腾 C」warn 仍系 ch24「昇腾 CANN」历史匹配），日志存 `management/validation/ch27-r1-verify.log`。图①②重渲染+重截图（fig2 624×584css，2x DPR），几何审计边距≥11px 无越界；宿主无法目检图像，请经理过图。源仓零写入零清理（status=0，HEAD e75072d）；未提交。
