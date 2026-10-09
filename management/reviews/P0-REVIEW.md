# P0 评审：修订后进入 ch16 正文

2026-10-09，项目经理。
源码快照和执行标准总体可用；第16章提纲方向通过，但证据表存在以下需要先修的问题：

1. CH16-EVIDENCE采集日期误写2026-09-09，改2026-10-09。主要锚点写成5组文件可以，但不能声称只有5个文件；A3含不存在的data_readme=README.md，改真实路径，不使用伪路径。
2. **同步种类与数量混淆**：mmad.asc主流水明确4类HardEvent：MTE2_MTE1、MTE1_MTE2、MTE1_M、M_MTE1。反向预置为6个flag实例，分属2类事件（A/B L1四个，L0两个）。不是“六对事件/反向三类”。证据、报告及正文全部修正。
3. **性能口径**：3022.92us理论Cube时间对比的是aic_mac_time=3076.396us，误差1.77%；不是对比Task Duration=4012.44us。mac_ratio=86.4%是Cube时间/AI Core时间，不能直接等同峰值算力实现率。官方README即使有混用也应明确区分，不能照抄为无条件事实。
4. B矩阵说明不能写“DataCopy有isTrans=true参数”：实际DataCopyInB使用IS_B_TRANSPOSE编译期分支和Nd2Nz尺寸/步长，转置状态来自输入布局及后续LoadData。先读gen_data.py和DataLoadB，讲清逻辑与物理布局。
5. 报告“16 bank×8组”是新错误。统一16个bank，每bank16KB，8组×每组2bank，总256KB。3510冲突判据直接引用准确条件，不保留问号式猜测；不要写“更严”这种方向不明的比较。
6. 补读U1–U5及实际源码后再写对应段；未知的容量数字宁可不写，不从文件名存在推导支持范围。性能引用补half输入/half输出、float累加等dtype和量纲。
7. ACCEPTANCE运行性标签来自STYLEGUIDE第3节，不是第2节。

满足以上修订后可直接执行 management/tasks/CH16.md，不必再停下来征询用户。
