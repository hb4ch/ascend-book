# CH28 报告 —— 正文交付

2026-10-10。任务 `CH28-WRITE.md`；证据 rev3（`CH28-EVIDENCE.md`）、提纲 `CH28-OUTLINE.md` 不变。**未改 ch27/appD/共享文件**；源仓零写入；未提交。

## 交付物

- `docs/07-outlook/ch28-roadmap.md` 全新正文（2,861 字/中文 2,244，任务不设字数线），占位全删，status `成稿`。
- frontmatter 三键（title/description/status）；`docs/07-outlook/index.md` 原链接行无需改动（未动该文件）。

## 结构（对照提纲）

28.1 目标与三条日期纪律（公告/合入/快照三分；快照逐仓 08-21~23）→ 28.2 时间线图①（纯公告节点，无证据标签无版本串塞入）→ 28.3 变化一 Tensor API（**新在 Layout/Shape/Stride 抽象、非 LocalTensor 新生**；老范式对照样例；「当前仅 Cube、Vector 后续」按 overview 原文；3510 限定 SIMD 视角；950 且 >9.1.0、`dav-3510`；本书仅实读未编译未运行）→ 28.4 变化二 VF 调试（**核体≠host 已按经理亲读纠正**：L72 `__global__ __vector__` 核体内 `AscendC::printf` 是设备侧打印；净新增=VF 路径补齐，NPU Check 仍公告级、ch11 降级注记继续成立；逐样例架构绑定如实）→ 28.5 变化三 通信公告（FabricMem 零带宽数字；issue=公告级不证互通）→ 28.6 反面清单（四不预测+不虚构路线条目）→ 28.7 收束三问（证据/条件/波及）+**全书验证边界如实**（NPU 缺位已声明、前 15 章未复核、不宣告验证完成）。陷阱 5 条、脚注 5 组全路径。仅一处 6 行短码例（Te::MakeTensor/Slice，标「需真机验证」）。

## 经理纠错的落实（VF 打印层次）

EVIDENCE B2 升 rev3：原文「host/核函数侧 AscendC::printf」误称已改为——**L72 核体签名内 L76-77 `AscendC::printf`/`GetBlockIdx()` 为设备侧打印；host 侧仅 main 的 aclInit 流程**；`__simd_vf__` 子函数经 `asc_vf_call` 由核体调用。正文 28.4 按此表述。

## 验证（真实 exit，直接重定向）

```
npm run verify >/tmp/ch28-verify2.log 2>&1; echo $? → 0
```
全绿：build 12.5s／internal-links 42 文件 OK／source-check **456 引用 0 无效**（ch28 脚注含 8 条源路径全过）／terms 106 条（唯一 warn「昇腾 C」1 处位于 **ch24 脚注既有文本**`昇腾 CANN`子串，非本章；未动他章）／word-count 正常。首跑 tee 管道 exit 不可信，已按规程重跑直接重定向核真值（`/tmp/ch28-verify2.log`）。

## 图①渲染与审计（宿主不能目检，如实声明）

- `fig1.mmd` 提取→mmdc（puppeteer.json 指向本机 chromium-1243）→`fig1.svg`（viewBox 936×103）→Playwright HTML 内嵌+JS 显式设 width/height→`management/validation/ch28-fig1.png`（1872×206 @2x）。
- **仅几何审计**：svg getBBox=[12,12,920,87]（viewBox 936×103 内含）；png 非白内容 bbox x[14,1864] y[14,199]，边距 L14/R7/T14/B6 设备像素（≈7/3.5/7/3 CSS px），无越界裁切迹象。**像素内容是否美观、文字是否溢出节点，宿主无法目检，留 PM 视觉验收**；页面实渲染效果以站点构建产物为准。

## 边界与留待

- appD 第 28 章行、「进一步阅读」类外链、index description——按任务留给经理收口阶段；ch27 未动一行。
- EVIDENCE rev3 变更仅两处：B2 核体表述修正+头部 rev 说明；OUTLINE 未动。
