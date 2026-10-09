# CH22-VISUAL 独立图形验证报告（2026-10-09）

范围：仅本地构建站点 `http://127.0.0.1:8767`（`python3 -m http.server 8767 --directory docs/.vitepress/dist`，经理进程）。**未改正文、未改站点配置、未提交**；源码只读。

## 结论先行

1. **第22章 mermaid 生命周期图渲染正常**——非 mermaid 语法问题，正文无需修改。
2. **「带锚点截图空白」＝chrome-headless `--screenshot` 的截图时机伪象**，非页面缺陷：真实浏览器（Playwright 真实等待）下锚点页面内容完整。
3. **API 宽表不靠横向滚动**：容器内自动换行，无截断、无页面级横向溢出——比「可横向滚动」更优，无需修复。

## 证据与方法（命令实录）

### A. mermaid 已渲染（静态 DOM 两查）

```bash
google-chrome-stable --headless=new --disable-gpu --no-sandbox --virtual-time-budget=8000 \
  --dump-dom 'http://127.0.0.1:8767/05-comm/ch22-hixl.html'
# → class="mermaid" data-processed="true"><svg id="mermaid-157" width="100%" ...
```

带锚点 URL 同样 `data-processed="true"`——DOM 层 mermaid 均已处理（dist 为 21:58 最新构建，与 md 同刻）。

### B. 空白复现与定位（像素统计，非目测）

```bash
google-chrome-stable --headless=new ... --virtual-time-budget={10000,20000} --screenshot=...
```

- 无锚点：546 KB，内容像素分布正常（`ch22-top.png`）。
- 带 `#_22-3-生命周期主线...` 锚点：15 KB，**整幅 2400px 均为均匀背景色 (27,27,31)**，即纯空白（`ch22-anchor-raw.png`）；budget 提到 20s 仍空白。
- 同站对照：ch16 带 22.3 类似深度锚点**正常着色**；ch22 带 `_22-1` 浅锚点正常、`_22-3-2`/`fn3` 深锚点空白→**与滚动深度相关的一次性 paint 时机问题**（headless `--screenshot` 在虚拟时间预算内未完成滚动后重绘），非 ch22 内容缺陷。

### C. 真实浏览器复核（Playwright 1.61 + 系统 Chromium，真实等待非虚拟时间）

- 无锚点：`body.scrollHeight=25462`，`.mermaid svg` 存在，**console/pageerror 均为空**；
- 带锚点：`scrollY=3052`（正落于 22.3 标题 y≈3162 上沿），mermaid svg 存在，无任何报错；
- 两态截图（`pw-top.png`/`pw-anchor.png`）像素统计均为内容非空白。

### D. 图尺寸实测

`.mermaid svg` bounding box **688×959 px**（y≈3426，紧随 22.3 标题）。交付截图：

```
management/validation/ch22-diagram.png   # 768×1039，墨水覆盖率 13.9%，含 mermaid 主题色块（255,245,173 等）
```

以 Playwright `locator('.mermaid svg').bounding_box()` 定位后 clip（周边留 40px）截取——**可实际阅读**，非空白。

### E. API 宽表（「组/方法/一句话」等 7 表全查）

| 表 | 表宽/容器宽 | 单元格 | 结果 |
|---|---|---|---|
| #0 API 总表 | 688/688 px，右缘=容器右缘 1072 | `scrollWidth==clientWidth`（551），长行换行至 ~113px 行高 | 完整换行显示 |
| #2 状态层表 | 同上 | 同上（rowH≈67） | 完整换行显示 |

`documentElement.scrollWidth==innerWidth==1440`：**无页面级横向滚动条**；所有单元格 `scrollWidth==clientWidth`＝无内容剪切。即宽表以**换行**消化宽度，不出现横向滚动也不截断——优于「仅正常横向滚动」的及格线，无需加 overflow 包装。

## 残留说明

- chrome-headless `--screenshot` 深锚点空白属工具性note，经理如需复现稳定截图，建议改用 Playwright 真实等待（本报告 C 节脚本逻辑）或先无锚加载再 `scrollIntoView` 后截图；**不需要改任何正文或站点配置**。
- 本机无真机，以上均为 dist 静态站渲染验证；mermaid 图内容与正文的语义一致性由 R1–R4 文字评审覆盖，不在本次图形验证范围。

交付物：`management/validation/ch22-diagram.png`（主）、`pw-top.png`/`pw-anchor.png`（对照）、`ch22-top.png`/`ch22-anchor-raw.png`（空白伪象证据）。
