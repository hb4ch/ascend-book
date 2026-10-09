# CH23-R3 修订回应（候审）

日期：2026-10-10 ｜ 对 `reviews/CH23-R3.md` 七项，全部改在正文并以 rg 复核终态（非仅报告）。终态 4,470 字（中文 3,361）。未提交、仅 CH23。

## 逐项改句与 rg 核验（`grep -c` 于最终 `docs/05-comm/ch23-supernode.md`）

**①跨代保证删除＋4-bit 旁支移除**——950 段现文：「950 对照：arch35 内核按 for 循环 Wait 共主块轮数次，与文档字面一致，另有 CC tiling 内嵌与固定 workspace 中转——这是另一条已核路径，两代的多 handle 结论本书均未证明，不能互推[^7]。」`两代最终保证相同`=0；4-bit 旁支正文删除（`4-bit`=0，fp4x2 注释保留于[^7] arch35 条目）。

**②MoE 限定四张量**——现文：「README 把限定范围划在四个辅助张量：`expandIdx`、`epRecvCounts`、`tpRecvCounts`、`expandScales` 在不同产品、算法、版本间元素可能不同，须原样传给 combine 对应参数，其他业务逻辑不得依赖其值（[^8]）；token 数据本身的结果不在此限。」旧全称句 `两者必须配套，且官方明言其输出`=0。

**③分片记号**——「x 按列拼 `x=[x0 x1]`（x0、x1 各 M×K/2），W 按行上下分 W0/W1（各 K/2×N，K 取偶），两卡各算 y0=x0W0 与 y1=x1W1，则 y=y0+y1」；`x=[x0;x1]`=0。

**④23.3 判据回源**——开头改「Host 侧的 tiling 与任务生成共同准备三个决定」；窗口条件按 `setUseBufferType`（L238-256）＋kernel L54-58 重写：「非 910B 形态、非仅算 debug、reuse 开启、张量非空，且两轮发送量之和小于窗容量；kernel 侧另要求 determinism≠1 才改指窗」；表条件行同步；算例改「容量条件满足，其余各项须同真」。`还须非 910B 形态等其余条件`=0（反写句删）。另注：确定性判断实为 kernel 侧 `context->config.determinism!=1`（base.h L56），host tiling 无 determinism 字段——本轮据 `setUseBufferType` L238-256 与 base.h L54-58 回源改写。

**⑤图③时序／图①尺寸**——图③删「（与轮1传输并行）」（=0），块2 行改「MM 块2、续、齐」，读图首句「本图只表**计数账目**，不表执行时刻」，仅作计数示例；图①删点线边、S1 改横排，自然尺寸 988×125→**605×214，站点 1:1 无缩放**（此前 624/988≈0.63 缩放致 9px 字）。

**⑥脚注全路径**——[^9] 现为 `.../aiv_comm/all_to_all/all_to_all_udma_get.h` 与 `.../aiv_comm/all_gather/all_gather_udma_put.h` 两条全路径（`aiv_comm/all_gather/all_gather_udma_put.h`=1）；[^8] layered_aicpu 全路径 R2 已补，复查在。

**⑦评审语气清除**——`依赖已全`、`编造成因`、`L40-42 实核`、`粒度依次变细`、`本书不补因果` 均=0；对应句改直述事实（「本图只画局部数据依赖……不是执行时序」「其余约束照抄 README：…」「见[^6]」；粒度句整句删）。

## 校验与图证

- `npm run verify`=0 FAIL：`management/validation/ch23-r3-verify.log`（4,470 字/中文 3,361）。
- `bash -n` ok：`ch23-r3-bashn.log`（块 `ch23-r3-fence.sh`）。
- 三图重截 `ch23-r3-fig{1,2,3}.png`（606×215 / 624×86 / 624×515；墨水 2.6/8.7/2.5%），并按 R2 同法对渲染后 SVG textContent 逐标签核对：图①8 键、图②6 键、图③8 键（含 Commit①②提交计数、轮①②完成计数、已等=1、旋等、单 handle）**全部命中**，pageerror=0。
