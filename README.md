# 《昇腾平台技术实战》

面向**实操型工程师**的昇腾（Ascend）全栈技术书。本书不是 API 文档的翻译合集，而是以 **CANN 开源仓源码**为第一手资料，逐层拆解「从 PyTorch 算子调用到 AI Core 上的执行」完整链路：平台全景 → 运行时与驱动 → 算子开发 → 性能优化 → 分布式通信 → 现代编译后端。

- **文档站点（推荐）**：`npm run docs:dev` 本地预览，`npm run docs:build` 产出静态站点（`docs/.vitepress/dist`）。
- **单页/PDF 导出**：见 `docs/导读` 说明；站点内容为 Markdown，可用 pandoc/pagedjs 等工具聚合导出。

## 写作原则（务必阅读 STYLEGUIDE.md）

1. **以源码为准**：任何 API、行为、性能结论都必须能在开源仓中找到出处，正文用 `📦 源码:` / `📄 资料:` 行内标注精确路径。
2. **不写水货**：所有示例来自仓内 examples/docs，标注运行性分级（`[可在 NPU 运行]` / `[可用 CPU-SIM 运行]` / `[需真机验证]` / `[示意代码]`）。
3. **术语统一**：写作前查 `glossary.md`；新增术语先评审再使用。
4. **自我一致性**：每章成稿后运行 `npm run verify`（构建 + 链接 + 术语 + 字数）。

## 里程碑状态

| 里程碑 | 内容 | 状态 |
|---|---|---|
| M0 | 站点骨架 + 风格指南 + 术语表 v1 + 来源映射表 + 第1章试写样章 | ✅ 完成 |
| M1 | 第1–3章（平台全景） | ✅ 三轮重写 + 选B补齐（真码/图表/能力菜单13项/图模上手）：第1章 8.2k、第2章 7.8k、第3章 6.8k（总字；纯中文 6.9k/6.5k/5.9k）。`verify` 全绿已收口，见 CHANGELOG B-3/B-4 |
| M2 | 第4–8章（runtime/驱动/DFX/内存） | ✅ 已成稿：第4章 ACL（4.5k/3.7k）、第5章 runtime（4.2k/3.3k）、第6章驱动（2.7k/2.2k）、第7章 DFX（2.7k/2.2k）、第8章内存（3.5k/2.7k），verify 绿，全编 17.6k总/14.1k中文 |
| M3 | 第9–14章（Ascend C+算子库+实战） | ⬜ 未开始 |
| M4 | 第15–16章（性能） | ⬜ 未开始 |
| M5 | 第17–19章（通信） | ⬜ 未开始 |
| M6 | 第20–23章（现代编译后端） | ⬜ 未开始 |
| M7 | 第24章 + 附录 + 全书校对 | ⬜ 未开始 |

> 详细进度、决策与变更记录见 [CHANGELOG.md](./CHANGELOG.md)。

## 目录结构

```
ascend-book/
├── package.json / README.md      # 站点与书说明
├── STYLEGUIDE.md                 # 写作规范（风格指南）
├── glossary.md                   # 术语表（唯一事实源，作为附录B进入站点）
├── CHANGELOG.md                  # 里程碑日志
├── markdown-link-check.json      # 链接检查配置
├── docs/                         # VitePress 站点
│   ├── index.md                  # 首页（导读）
│   ├── .vitepress/               # 配置、侧边导航
│   ├── 00-导读/ 01-platform/ ... 07-outlook/ 附录/
├── figures/                      # 自绘图
└── scripts/                      # build、link-check、word-count、源码校验
```

## 常用命令

```bash
npm run docs:dev        # 本地开发预览
npm run docs:build      # 构建静态站点
npm run docs:preview    # 预览构建产物
npm run check:links     # 校验外部链接（需网络；hiascend/gitcode 策略化跳过）
npm run check:internal  # 校验站内链接（零网络）
npm run check:terms     # 术语一致性检查（advisory）
npm run check:source    # 源码路径引用核对
npm run word:count      # 各章字数统计
npm run verify          # 构建+站内链接+源码+术语+字数 一键执行
```

## 许可证

本书基于 CANN Open Open 系列开源仓（CANN Open Software License Version 2.0）与 related 社区文档写作。书中复用的官方图均标注源文件路径与许可证；正文、自绘图与代码阐释部分版权归本书作者，遵循对应开源许可合规要求传播。
