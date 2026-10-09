// Validate source paths in standard/legacy footnotes and explicit source labels.
// This checks path existence, not whether the source supports the prose claim.
import { readdirSync, statSync, readFileSync, existsSync } from 'node:fs'
import { join, extname, resolve } from 'node:path'
import { pathToFileURL } from 'node:url'

const REPOS = ['asc-devkit', 'runtime', 'pto-isa', 'pypto', 'hcomm', 'hixl',
  'ops-nn', 'ops-transformer', 'ops-sparse', 'cann-learning-hub']

export function collectRefs(text) {
  const refs = new Set()
  let inFootnote = false
  let fence = null
  for (const line of text.split('\n')) {
    const fenced = line.match(/^\s*(`{3,}|~{3,})/)
    if (fenced) {
      if (!fence) fence = fenced[1]
      else if (fenced[1][0] === fence[0] && fenced[1].length >= fence.length) fence = null
      continue
    }
    if (fence) continue
    const definition = /^\s*(?:-\s+)?\[\^[^\]]+\]:/.test(line)
    if (definition) inFootnote = true
    else if (line.trim() && !/^\s{4}|^\t/.test(line)) inFootnote = false
    const label = /(?:📦\s*源码(?:\/📄\s*资料)?|📄\s*资料|源码|资料)\s*[:：]/.exec(line)
    if (!inFootnote && !label) continue
    const content = inFootnote ? line : line.slice(label.index + label[0].length)
    for (const match of content.matchAll(/`([^`]+)`/g)) refs.add(match[1])
    if (label && !content.includes('`')) {
      const first = content.trim().match(/^[^\s，。;；）)]+/)
      if (first) refs.add(first[0])
    }
  }
  return [...refs].filter(ref => REPOS.includes(ref.split('/')[0]))
}

export function expandBraces(pattern) {
  const m = pattern.match(/\{([^{}]+)\}/)
  if (!m) return [pattern]
  return m[1].split(',').flatMap(value => expandBraces(
    pattern.slice(0, m.index) + value + pattern.slice(m.index + m[0].length)))
}

// Resolve glob components explicitly: a prefix directory alone is not a match.
function matches(root, segments) {
  if (!segments.length) return existsSync(root)
  if (!existsSync(root) || !statSync(root).isDirectory()) return false
  const [part, ...rest] = segments
  if (part === '**') {
    if (rest.length && matches(root, rest)) return true
    return readdirSync(root, { withFileTypes: true }).some(entry =>
      rest.length === 0 || (entry.isDirectory() && matches(join(root, entry.name), segments)))
  }
  if (!part.includes('*') && !part.includes('?')) return matches(join(root, part), rest)
  const expression = new RegExp('^' + part.split('').map(c =>
    c === '*' ? '.*' : c === '?' ? '.' : c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('') + '$')
  return readdirSync(root).some(name => expression.test(name) && matches(join(root, name), rest))
}

export function missingRefs(ref, root) {
  return expandBraces(ref).filter(path => {
    const parts = path.split('/').filter(Boolean)
    return parts.includes('..') || !matches(root, parts)
  })
}

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    if (entry.name === '.vitepress') return []
    const path = join(dir, entry.name)
    return entry.isDirectory() ? walk(path) : extname(path) === '.md' ? [path] : []
  })
}

function main() {
  const root = process.env.CANN_ROOT || '/mnt/SATASSDEXT4/cann'
  if (!existsSync(root)) throw new Error(`CANN source root does not exist: ${root}`)
  const files = walk('docs')
  let bad = 0, count = 0, expanded = 0
  for (const file of files) {
    for (const ref of collectRefs(readFileSync(file, 'utf8'))) {
      count++
      expanded += expandBraces(ref).length
      for (const missing of missingRefs(ref, root)) {
        bad++
        console.log(`[FAIL] ${file}: 路径不存在或通配无匹配 -> ${missing}`)
      }
    }
  }
  console.log(`[check-source] ${bad ? 'FAIL' : 'OK'}: ${files.length} 个文件，${count} 条引用，展开 ${expanded} 条路径模式，${bad} 处无效。仅校验路径，不验证论断。`)
  if (bad) process.exitCode = 1
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) main()
