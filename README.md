# 《昇腾平台技术实战》

面向**实操型工程师**的昇腾（Ascend）全栈技术书。本书不是 API 文档的翻译合集，而是以 **CANN 开源仓源码**为第一手资料，逐层拆解「从 PyTorch 算子调用到 AI Core 上的执行」完整链路：平台全景 → 运行时与驱动 → 算子开发 → 性能优化 → 分布式通信 → 现代编译后端。

- **📖 在线阅读（HTML 站点）**：https://hb4ch.github.io/ascend-book/ —— 推送 main 后由 GitHub Actions 自动构建发布。

- **文档站点（推荐）**：`npm run docs:dev` 本地预览，`npm run docs:build` 产出静态站点（`docs/.vitepress/dist`）。
- **单页/PDF 导出**：见 `docs/导读` 说明；站点内容为 Markdown，可用 pandoc/pagedjs 等工具聚合导出。
- **GitHub 在线阅读**：全部章节为 Markdown，可直接从下方[目录](#目录在线阅读)点击进入；写作规范见 [STYLEGUIDE.md](./STYLEGUIDE.md)。

## 写作原则（务必阅读 [STYLEGUIDE.md](./STYLEGUIDE.md)）

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
| M3 | 第9–14章（Ascend C+算子库+实战） | 🔄 成稿中：[PLAN-PART3.md](./PLAN-PART3.md) 已定方案；第9章已成稿（4.4k总字/3.4k中文）；第10章已成稿（4.3k总字/3.0k中文，4图5表，还清第8章 N-DMA 债）；第11章已成稿（约4.3k总字/3.3k中文，6图，含 CUDA 迁移对照表，还清 RegTensor 债）；第12章已成稿（3.8k总字/2.9k中文，3图，编译流水线SVG核心图，dav-2002 证伪不采信） |
| M4 | 第15–16章（性能） | ⬜ 未开始 |
| M5 | 第17–19章（通信） | ⬜ 未开始 |
| M6 | 第20–23章（现代编译后端） | ⬜ 未开始 |
| M7 | 第24章 + 附录 + 全书校对 | ⬜ 未开始 |

> 详细进度、决策与变更记录见 [CHANGELOG.md](./CHANGELOG.md)；写作计划见 [PLAN-PART1.md](./PLAN-PART1.md) / [PLAN-PART2.md](./PLAN-PART2.md)。

## 目录（在线阅读）

> 点击章节标题直接跳转到对应 Markdown 源文件；各编导语见各编目录下 `index.md`。

- [导读：如何使用本书](./docs/index.md)
- **第一编 昇腾平台全景**（[编导语](./docs/01-platform/index.md)）：[第1章 平台与生态总览](./docs/01-platform/ch01-overview.md) · [第2章 硬件体系结构](./docs/01-platform/ch02-hardware.md) · [第3章 软件栈执行主链路](./docs/01-platform/ch03-exec-path.md)
- **第二编 运行时、驱动与维测底层**（[编导语](./docs/02-runtime/index.md)）：[第4章 ACL 编程接口](./docs/02-runtime/ch04-acl.md) · [第5章 运行时核心实现](./docs/02-runtime/ch05-runtime-impl.md) · [第6章 驱动与系统软件协同](./docs/02-runtime/ch06-driver.md) · [第7章 维测子系统 DFX](./docs/02-runtime/ch07-dfx.md) · [第8章 内存与数据通路](./docs/02-runtime/ch08-memory.md)
- **第三编 算子开发：Ascend C**（[编导语](./docs/03-ascendc/index.md)）：[第9章 编程模型与 API 选择](./docs/03-ascendc/ch09-api-map.md) · [第10章 核心编程能力详解](./docs/03-ascendc/ch10-core-programming.md) · [第11章 SIMD/SIMT 与高级特性](./docs/03-ascendc/ch11-simd-simt.md) · [第12章 编译、工具链与部署](./docs/03-ascendc/ch12-compile-tools.md) · [第13章 算子库体系](./docs/03-ascendc/ch13-operator-libs.md) · [第14章 经典算子实战](./docs/03-ascendc/ch14-op-practice.md)
- **第四编 性能优化方法论**（[编导语](./docs/04-perf/index.md)）：[第15章 性能分析与瓶颈定位](./docs/04-perf/ch15-perf-analysis.md) · [第16章 优化技术专题](./docs/04-perf/ch16-opt-topics.md)
- **第五编 分布式通信**（[编导语](./docs/05-comm/index.md)）：[第17章 HCCL 集合通信](./docs/05-comm/ch17-hccl.md) · [第18章 HIXL 单边通信](./docs/05-comm/ch18-hixl.md) · [第19章 通算融合与大规模系统](./docs/05-comm/ch19-supernode.md)
- **第六编 现代编译后端与编程范式**（[编导语](./docs/06-backend/index.md)）：[第20章 PTO 虚拟 ISA](./docs/06-backend/ch20-pto-isa.md) · [第21章 PyPTO 框架深入](./docs/06-backend/ch21-pypto.md) · [第22章 生态与前沿编译技术](./docs/06-backend/ch22-ecosystem.md) · [第23章 全栈综合案例](./docs/06-backend/ch23-case.md)
- **第七编 展望与总结**（[编导语](./docs/07-outlook/index.md)）：[第24章 路线图与展望](./docs/07-outlook/ch24-roadmap.md)
- **附录**：[A 环境搭建](./docs/附录/appA-env.md) · [B 术语表](./docs/附录/appB-glossary.md) · [C 资源索引](./docs/附录/appC-resources.md) · [D 来源映射表](./docs/附录/appD-source-map.md) · [E 风格规范](./docs/附录/appE-style.md)

## 目录结构

```
ascend-book/
├── package.json / [README.md](./README.md)   # 站点与书说明
├── [STYLEGUIDE.md](./STYLEGUIDE.md)          # 写作规范（风格指南）
├── [glossary.md](./glossary.md)              # 术语表（唯一事实源，作为附录B进入站点）
├── [CHANGELOG.md](./CHANGELOG.md)            # 里程碑日志
├── markdown-link-check.json      # 链接检查配置
├── docs/                         # VitePress 站点
│   ├── [index.md](./docs/index.md)           # 首页（导读）
│   ├── .vitepress/               # 配置、侧边导航
│   ├── 00-导读/ 01-platform/ ... 07-outlook/ 附录/  # 各编章节（见上方目录）
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

本书基于 CANN Open 系列开源仓（CANN Open Software License Version 2.0）与相关社区文档写作。书中复用的官方图均标注源文件路径与许可证；正文、自绘图与代码阐释部分版权归本书作者，遵循对应开源许可合规要求传播。
