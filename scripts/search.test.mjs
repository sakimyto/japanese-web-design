import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'
import { matchesRule, normalizeQuery } from '../site/app.js'

const data = JSON.parse(readFileSync(new URL('../catalog.json', import.meta.url), 'utf8'))
const rules = data.sections.flatMap((section) =>
  section.rules.map((rule) => ({
    id: rule.id,
    section: section.id,
    search: ['id', 'title', 'when', 'advice', 'example', 'exception', 'check']
      .map((key) => rule[key])
      .join(' '),
  })),
)

test('every category and rule ID uses the intersection, including full-width input', () => {
  let combinations = 0
  for (const rule of rules) {
    for (const category of ['all', ...data.sections.map((section) => section.id)]) {
      const fullwidth = rule.id.replace(/[A-Z0-9]/g, (character) =>
        String.fromCharCode(character.charCodeAt(0) + 0xfee0),
      )
      for (const query of [rule.id, fullwidth]) {
        assert.equal(
          matchesRule(rule, query, category),
          category === 'all' || category === rule.section,
        )
        combinations += 1
      }
    }
  }
  assert.equal(combinations, 1152)
})

test('empty, multiword, unknown, and injection-like queries behave as text', () => {
  assert.equal(rules.filter((rule) => matchesRule(rule, '  ', 'all')).length, rules.length)
  assert.equal(rules.filter((rule) => matchesRule(rule, 'unknown-no-match', 'all')).length, 0)
  assert.equal(rules.filter((rule) => matchesRule(rule, '<script>', 'all')).length, 0)
  const example = { section: 'forms', search: 'F01 日本語のIME 変換確定Enter' }
  assert.equal(matchesRule(example, 'IME Enter', 'forms'), true)
  assert.equal(matchesRule(example, 'IME missing', 'forms'), false)
  assert.equal(matchesRule(example, 'IME', 'layout'), false)
  assert.equal(normalizeQuery(' ＩＭＥ '), 'ime')
})

test('a broken union condition would be rejected by the same expected outcomes', () => {
  const example = { section: 'forms', search: 'IME' }
  const broken = (rule, query, category) => rule.section === category || rule.search.includes(query)
  assert.equal(broken(example, 'IME', 'layout'), true)
  assert.equal(matchesRule(example, 'IME', 'layout'), false)
})
