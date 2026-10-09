# CH27 研究补证，暂不正文
保持当前模型/会话，不提交，不改26章。经理独立核查发现研究不够支持“全链”：
1. example里的PrintOutResult定义不等于调用。亲读main全程并rg所有引用；当前launch后实际是aclrtSynchronizeStream再销毁/释放，证据C3回读打印可能虚构。明确所有资源生命周期和同步，不能省略。
2. “全部ACL_FLOAT16”错误：sparseIndices/actSeq为INT32，softmaxMax/Sum为FLOAT。逐张量核对表。
3. 不允许以目录存在/2295行未读代替host→kernel调用证据。针对例子TND fp16固定场景，实际读op_api包装、推导校验、tiling关键条件和tilingKey选择、kernel架构门控；至少追一个子路径到计算和同步，其他分支明确范围。无法闭合的边用虚线/断点，不把“三件套”画成直接调用。
4. CPU运行是另一组BSND输入，不是TND主例验证。明确分成样例A与CPU参考B，或者增加同主例条件的CPU参考。运行golden单独成功不验证golden数学正确，更不验证NPU；均值/标准差不是正确性判据。给小规模独立数学对拍（含稀疏索引和mask规则）、有限值与shape断言、固定seed，审查数值和特殊值语义。无NPU不要声称闭环正确性。
5. 源仓readonly：sys.path插入不防pyc。脚本在导入前设置sys.dont_write_bytecode=True，或者强制PYTHONPYCACHEPREFIX；记录真实执行方式，不以git干净证明零写入。不要再安装到用户环境，后续依赖仅已有环境或/tmp隔离环境；记录先前tensorflow安装实际位置和命令。
6. 稀疏注意力与18章稠密FA不是“差异不在数学”：索引/掩码改变关注集合。准确解释取子集与全量的区别。DSA复杂度O(Lk)只限选定子集后的注意力，索引器/选择开销另算，不能推广整网。
更新EVIDENCE/OUTLINE和补证回应，真实验证日志保留；候审。
