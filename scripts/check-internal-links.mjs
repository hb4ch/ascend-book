// check-internal-links: 校验站点内部链接（相对/绝对 /路径）都能解析到 docs 下的文件。
// 不校验外部 http(s)（那是 markdown-link-check 的活）。零网络依赖。
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs'
import { join, dirname, extname, resolve, relative } from 'node:path'

const DOCS = resolve('docs')
const files = []
const walk = (d) => {
  for (const n of readdirSync(d)) {
    const p = join(d, n)
    if (n.startsWith('.vitepress')) continue
    if (statSync(p).isDirectory()) walk(p)
    else if (extname(p) === '.md') files.push(p)
  }
}
walk(DOCS)
const mdSet = new Set(files.map((f) => relative(DOCS, f).replace(/\.md$/, '')))
const existsTarget = (base, href) => {
  href = href.split('#')[0].split('?')[0]
  if (!href) return true
  if (/^https?:\/\//.test(href)) return true
  const p = href.startsWith('/') ? join(DOCS, href) : resolve(dirname(base), href)
  return existsSync(p) || mdSet.has(relative(DOCS, p).replace(/\.md$/, ''))
}
let bad = 0
for (const f of files) {
  const text = readFileSync(f, 'utf8')
  for (const m of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
    const href = m[1].replace(/^</, '').replace(/>$/, '')
    if (href.startsWith('mailto:') || href.startsWith('#')) continue
    if (!existsTarget(f, href)) {
      bad++
      console.log(`[FAIL] ${relative(DOCS, f)}: 站内链接不解析 -> ${href}`)
    }
  }
}
if (bad) { console.log(`共有 ${bad} 个站内链接无法解析`); process.exit(1) }
console.log(`[check-internal-links] OK: ${files.length} 个文件站内链接全部可解析`)
