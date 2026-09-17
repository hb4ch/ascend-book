// check-terms: 术语一致性检查（v2）
// 1) 从 glossary.md（附录B）抽取术语表中的英文词。
// 2) 对整个站点统计每个术语的出现（粗略覆盖度，提示哪些术语已登记但全书未用）。
// 3) 仅对「高置信度误用词」告警（如 '昇腾C'）。
// 本工具是 advisory：始终 exit 0（结论需人工确认），不阻断构建。
// 用法: node scripts/check-terms.mjs
import { readFileSync, readdirSync, statSync } from 'node:fs'
import { join, extname } from 'node:path'

const ROOT = '.'
const FILES = []
const walk = (d) => {
  for (const name of readdirSync(d)) {
    const p = join(d, name)
    if (name.startsWith('.vitepress') || name.startsWith('node_modules')) continue
    if (statSync(p).isDirectory()) walk(p)
    else if (extname(p) === '.md') FILES.push(p)
  }
}
walk('docs')

const full = FILES.map((f) => readFileSync(f, 'utf8')).join('\n')
const body = full.replace(/^---[\s\S]*?---/gm, '')

// 1) glossary 术语收集（表格第一列）
const glossary = readFileSync('glossary.md', 'utf8')
const terms = new Set()
for (const line of glossary.split('\n')) {
  const m = line.match(/^\|\s*([^*|]+?)\s*\|/)
  if (m) terms.add(m[1].trim())
}

// 2) 覆盖度统计
const neverUsed = []
for (const t of terms) {
  const esc = t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  // 避免把空词或纯中文抓进来
  if (!/[A-Za-z0-9]/.test(t)) continue
  if (!new RegExp(esc, 'i').test(body) && !glossary.includes(t) === false) {
    neverUsed.push(t)
  }
}
console.log(`[check-terms] 术语表 ${terms.size} 条；其中纯中文/无需在正文计入的不统计。`)
if (neverUsed.length) {
  console.log('[check-terms] 提示（登记但正文未出现，确认是否有意保留）:', neverUsed.join('、'))
}

// 3) 高置信误用
const MISUSE = [
  ['昇腾C', 'Ascend C'],
  ['昇腾 C', 'Ascend C'],
  ['PYPTO', 'PyPTO'],
  ['hccL', 'HCCL'],
]
let warnings = 0
for (const [bad, good] of MISUSE) {
  let count = 0
  const re = new RegExp(bad.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')
  while (re.exec(body)) count++
  if (count > 0) {
    warnings++
    console.log(`[warn] 出现「${bad}」${count} 处，应统一为「${good}」`)
  }
}
console.log(warnings ? `误用告警 ${warnings} 类（请修复）` : '[check-terms] 无高置信误用词')
