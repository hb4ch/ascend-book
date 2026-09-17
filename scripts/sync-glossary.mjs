// sync-glossary: 将根 glossary.md 同步为站点 附录B（保持 frontmatter 与链接正确）
import { readFileSync, writeFileSync } from 'node:fs'

const HEADER = `---
title: 附录B 术语表
description: 全书术语唯一源（由根目录 glossary.md 同步生成，勿手改）
---

# 附录B 术语表

<!-- 自动由 npm run sync:glossary 生成；修改请在仓库根目录 glossary.md -->

`
const body = readFileSync('glossary.md', 'utf8')
writeFileSync('docs/附录/appB-glossary.md', HEADER + body, 'utf8')
console.log('[sync-glossary] 已同步 glossary.md -> docs/附录/appB-glossary.md')
