// word-count: 统计各 md 文件正文字数（含中文/英文/代码），输出每章与合计。
// 用法: node scripts/word-count.mjs [dir]
import { readdirSync, statSync, readFileSync } from 'node:fs'
import { join, extname } from 'node:path'

const root = process.argv[2] ?? 'docs'
const files = []
const walk = (d) => {
  for (const name of readdirSync(d)) {
    const p = join(d, name)
    if (name.startsWith('.vitepress')) continue
    if (statSync(p).isDirectory()) walk(p)
    else if (extname(p) === '.md') files.push(p)
  }
}
walk(root)

const CHINESE_RE = /[\u4e00-\u9fff]/g
const WORD_RE = /[A-Za-z0-9_]+/g
let total = 0
let grand = 0
let grandCjk = 0
const rows = files.sort().map((f) => {
  const text = readFileSync(f, 'utf8')
  const body = text.replace(/^---[\s\S]*?---/, '') // strip frontmatter
  const cjk = (body.match(CHINESE_RE) || []).length
  const words = (body.match(WORD_RE) || []).length
  const n = cjk + words
  total += n; grandCjk += cjk; grand += n
  return { f, n, cjk }
})

const dirs = {}
for (const { f, n, cjk } of rows) {
  const dir = f.split('/').slice(0, 2).join('/')
  dirs[dir] = dirs[dir] || { n: 0, cjk: 0 }
  dirs[dir].n += n; dirs[dir].cjk += cjk
}

console.log('== 目录汇总 ==')
for (const [d, { n, cjk }] of Object.entries(dirs)) {
  console.log(pad(d, 32) + `${pad(n.toLocaleString(), 8)} 字 (中文 ${cjk.toLocaleString()})`)
}
console.log('\n== 分文件 ==')
for (const { f, n, cjk } of rows) console.log(pad(f, 50) + `${pad(n.toLocaleString(), 7)} 字 (中文 ${cjk.toLocaleString()})`)
console.log(`\n总字数(含英文代码标记等): ${grand.toLocaleString()}  纯中文: ${grandCjk.toLocaleString()}`)

function pad(s, n) { s = String(s); return s.length >= n ? s : s + ' '.repeat(n - s.length) }
