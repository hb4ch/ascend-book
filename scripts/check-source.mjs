// check-source: 校验正文/脚注中引用的 `repo/path` 在 /mnt/SATASSDEXT4/cann/<repo>/... 真实存在。
// 覆盖两类来源：
//  1) 旧式行内标注（📦 源码: / 源码:）——历史文章兼容；
//  2) 章末脚注 `- [^n]: ... ` 包裹的 `repo/...` 路径（当前规范主力）。
// 支持 `*`（目录通配）与 `{a,b}`（花括号通配）标注。
import { readdirSync, statSync, readFileSync, existsSync } from 'node:fs'
import { join, extname } from 'node:path'

const CANN_ROOT = process.env.CANN_ROOT || '/mnt/SATASSDEXT4/cann'
const REPOS = ['asc-devkit', 'runtime', 'pto-isa', 'pypto', 'hcomm', 'hixl',
  'ops-nn', 'ops-transformer', 'ops-sparse', 'cann-learning-hub']

const walk = (d, out = []) => {
  for (const name of readdirSync(d)) {
    const p = join(d, name)
    if (name.startsWith('.vitepress')) continue
    if (statSync(p).isDirectory()) walk(p, out)
    else if (extname(p) === '.md') out.push(p)
  }
  return out
}

function collectRefs(text) {
  const refs = []
  // 1) 行内标注
  const inline = /(?:📦 源码|📄 资料|源码|资料)['"]?\s*[:：]\s*([^\s`,，。;；」)」]+)/g
  let m
  while ((m = inline.exec(text))) refs.push(m[1])
  // 2) 脚注内容里的反引号路径（限脚注行，避免误抓正文示例代码）
  for (const line of text.split('\n')) {
    if (!/^\s*- \[(\^)?[^\]]+\]:/.test(line)) continue
    const mm = line.match(/`([^`]+)`/g)
    if (mm) refs.push(...mm.map((x) => x.replace(/`/g, '')))
  }
  return refs
}

function checkRef(ref) {
  ref = ref.replace(/^[`'"(/[［]+|[`'")、\]。]+$/g, '')
  if (!ref || ref.includes('://')) return 'skip'
  const repo = ref.split('/')[0]
  if (!REPOS.includes(repo)) return 'skip'
  const p = join(CANN_ROOT, ...ref.split('/'))
  if (existsSync(p)) return 'ok'
  // 花括号通配：`path/{a,b}.md`
  const brace = ref.match(/^(.+\/)\{([^}]+)\}([^{}]*)$/)
  if (brace) {
    const base = brace[1]
    if (brace[2].split(',').some((n) => existsSync(join(CANN_ROOT, base, n + brace[3])))) return 'ok'
  }
  // 目录通配：`dir/*` 或 `dir/**`
  if (ref.includes('*')) {
    const dir = ref.slice(0, ref.indexOf('*')).replace(/[/]+$/, '')
    if (existsSync(join(CANN_ROOT, ...dir.split('/')))) return 'ok'
  }
  return ref // 返回 ref 表示坏路径
}

const files = walk('docs')
let bad = 0
for (const f of files) {
  const text = readFileSync(f, 'utf8')
  for (const ref of collectRefs(text)) {
    const r = checkRef(ref)
    if (r !== 'ok' && r !== 'skip') {
      bad++
      console.log(`[FAIL] ${f}: 路径不存在 -> ${ref}`)
    }
  }
}
if (bad) { console.log(`\n共有 ${bad} 处引用无效`); process.exit(1) }
console.log(`[check-source] OK: 校验 ${files.length} 个文件通过，全部 "repo/path" 引用存在`)
