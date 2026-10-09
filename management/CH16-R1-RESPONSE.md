# CH16-R1 逐项响应（CH16-R1-RESPONSE）

> 2026-10-09。对应 reviews/CH16-R1.md 六组；每条给修改位置。正文 `docs/03-ascendc/ch16-matmul-cube.md`（7,375 字/5,069 中文）；图 `docs/figures/ch16-pipeline.svg`。

## R1-1 流水走查与图
- 正文 16.3 重写主循环骨架（L171-260 节选）：CopyOut 明确置于 k 循环后；A 大包 8 基块/B 大包 4 基块两套进度两套指针；删 `baseK/baseK` 残留与「四级各有两层缓冲」（L0C 单 CO1 cLocal）。
- SVG 时空面板重画：两级节奏（大包 K 链×基块循环）、Ping/Pong 标注、Fixpipe 仅在「K 循环后整块搬出·按块读复 0」；副标注「示意，非真实耗时比例」；删除「永远有活干」及图内外同类断言；图内 B 布局按已转置默认路表述。
- 走查段重写为「阶段化预取+K 循环」两段落，索引与源码一致（a1/b1 NextKChunkIdx 分立）。

## R1-2 UnitFlag
- 通读 UnitFlag.md 后新增 16.3 阶段③′专节：512B 块状态位 0/1；2=保持（写等 0 保持 0/读等 1 保持 1）、3=翻转（写置 1/读置 0）四行对照表；末次 Mmad 与 Fixpipe 按块交错、无整块串行点；L0C 复用防覆盖=读后复位；与 4 类 HardEvent 关系单列「两套机制」段。正文/陷阱表/小结全部改用新语义；图 alt 同步。

## R1-3 性能归因与跨架构
- Case2→3：改按 README L175/197-199——2×12 未 512B 对齐未均匀分核；4×6 singleM2048/singleN1536/tailN512 对齐＋同址冲突更小；删「尾块均衡/慢核」推断，Task 差 257μs 与 aicore 差值并陈不归因。
- 常量 Tiling scalar：A2 Case6→7 1753.463→968.616（Case8 1026.069）；950 Case6→7 765.125→426.398（Case8 412.29），注明不可横比。
- Case4 depthA1=4（ping/pong 各 2 基块）＋调优公式；Case5 depthA1=16=基本块份数；Case3→4 段不再出现 16/8。
- 删「架构越新…手工极限」「瓶颈永远 MTE2」「ratio 最高即瓶颈」；改「本例观察+待验证假设（WaitFlag 位点/带宽/关键路径结合）」于 16.2 末与 16.7。
- 19.89×等标注「官方 Task 数据相除」；表 16-1 新增 dtype/shape/版本矩阵，软件版本要求与实测环境分列（A2=910B1 1.85GHz）。

## R1-4 LoadData 分支表与 TPosition
- 2201 �路=LoadData2DParams（旧式）直搬；false→3D V2 enTranspose；3510 均 2D V2——正文 2×2 表与 16.4 速查表（DataLoadA/B 分行）双处修正；「V220=代际路标」句删，改「两代同用，勿以名断代」。
- TPosition 表重做：C2 单列（切分 Bias，教程 04.02），VECCAL 补官方文档脚注[^tpos]。

## R1-5 数字与复现
- blockLen 2046B/curCols 1023/srcStride 22526&22528；现象 A2 215.82→275.3（-21.6%）950 188.52→192.07（-1.8%）；「未隔离单变量，只陈述现象」。
- 新增真实复现入口：CMake `-DCMAKE_ASC_ARCHITECTURES=dav-2201 -DSCENARIO_NUM=n`（+sim 模式/清缓存注），gen_data→run→verify；`[需真机验证]`标注，未声称已运行。
- 删节片段统一「删节节选」明示；纯示意处 `[示意代码]`（高阶 API 形态段）。

## R1-6 闭环
- 11 个脚注 used/defined 双向核验（mmad/bank/guide950/tpos 补正文引用；脚本计数全≥2）。
- 表 16-1 已建并在 16.1 引用；16.4 回指改 16.5；来源给到文件级（mmatk 拆 notebook 文件名）；ops-nn 删「九成」猜测，改中性+脚注[^opsnn]。

## 深度与表达
- 新增 16.3「输出基块账本」演算（96 基块/12288 Mmad+A16/B32 大包/A1B1 128KB 形状互换/cLocal=L0C 容量反推 baseM）；高阶 API 摘录+[示意代码]标注+Iterate/IterateAll 与封装关系辨析；「机关/深水区/原子弹」等修辞清除；无 only/after 夹杂；内部【A】【D】标记清除（推导改行文注明）。

## 验证
verify 全绿（validation/ch16-verify.log）：内链 42 文件、check-source 243 引用 0 无效、术语无违例；字数见 npm run word:count（5,069 中文）；HTML 脚注/表格抽查见 CH16-REPORT 追节。
