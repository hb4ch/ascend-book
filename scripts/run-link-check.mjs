// run-link-check: 枚举 docs 下全部 md（跳过 .vitepress），交给 markdown-link-check 检查。
// 外部链接（hiascend/gitcode 等）在 markdown-link-check.json 中做了策略配置。
import { spawnSync } from 'node:child_process'
import { readdirSync, statSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const BIN = join(__dirname, '..', 'node_modules', 'markdown-link-check', 'markdown-link-check')

const files = []
const walk = (d) => {
  for (const n of readdirSync(d)) {
    const p = join(d, n)
    if (n.startsWith('.vitepress')) continue
    if (statSync(p).isDirectory()) walk(p)
    else if (n.endsWith('.md')) files.push(p)
  }
}
walk('docs')

const r = spawnSync(process.execPath, [BIN, '-c', 'markdown-link-check.json', ...files], {
  stdio: 'inherit',
  cwd: process.cwd(),
})
process.exit(r.status ?? 1)
