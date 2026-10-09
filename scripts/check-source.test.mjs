import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { collectRefs, missingRefs } from './check-source.mjs'

test('standard, legacy, multiline footnotes and source labels; exclude examples', () => {
  const text = '[^a]: `runtime/a.cc`\n\n    continued `runtime/b.cc`\n- [^b]: `pypto/c.h`\n正文 `runtime/not-a-reference`\n📦 源码/📄 资料: `asc-devkit/d.h`\n```md\n[^fake]: `runtime/fake`\n```'
  assert.deepEqual(collectRefs(text), ['runtime/a.cc', 'runtime/b.cc', 'pypto/c.h', 'asc-devkit/d.h'])
})

test('every brace member must exist; glob suffix must match; reject traversal', () => {
  const root = mkdtempSync(join(tmpdir(), 'ascend-source-test-'))
  try {
    mkdirSync(join(root, 'runtime/sub'), { recursive: true })
    writeFileSync(join(root, 'runtime/a.cc'), '')
    writeFileSync(join(root, 'runtime/sub/b.cc'), '')
    assert.deepEqual(missingRefs('runtime/{a,missing}.cc', root), ['runtime/missing.cc'])
    assert.deepEqual(missingRefs('runtime/**/*.cc', root), [])
    assert.deepEqual(missingRefs('runtime/*/b.cc', root), [])
    assert.deepEqual(missingRefs('runtime/**/*.missing', root), ['runtime/**/*.missing'])
    assert.deepEqual(missingRefs('runtime/../outside', root), ['runtime/../outside'])
  } finally { rmSync(root, { recursive: true, force: true }) }
})
