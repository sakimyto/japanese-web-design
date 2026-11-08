export function normalizeQuery(value) {
  return value.normalize('NFKC').toLocaleLowerCase('ja-JP').trim()
}

export function matchesRule(rule, query, category) {
  const words = normalizeQuery(query).split(/\s+/u).filter(Boolean)
  return (
    (category === 'all' || rule.section === category) &&
    words.every((word) => normalizeQuery(rule.search).includes(word))
  )
}

if (typeof document !== 'undefined') {
  const search = document.querySelector('#search')
  const rules = Array.from(document.querySelectorAll('.rule'))
  const filters = Array.from(document.querySelectorAll('[data-category]'))
  const count = document.querySelector('#results')
  let category = 'all'

  function filter() {
    let visible = 0
    for (const element of rules) {
      const match = matchesRule(element.dataset, search.value, category)
      element.hidden = !match
      if (match) visible += 1
    }
    count.textContent = `${visible}件を表示`
    document.querySelector('#no-results').hidden = visible !== 0
  }

  document.querySelector('#guide-controls').hidden = false
  search.addEventListener('input', filter)
  for (const button of filters) {
    button.addEventListener('click', () => {
      category = button.dataset.category
      for (const other of filters) {
        const active = other === button
        other.classList.toggle('active', active)
        other.setAttribute('aria-pressed', String(active))
      }
      filter()
    })
  }
  document.querySelector('#reset').addEventListener('click', () => {
    search.value = ''
    filters[0].click()
    search.focus()
  })

  function revealHash() {
    const id = location.hash.slice(1)
    const target = rules.find((rule) => rule.id === id)
    if (!target) return
    search.value = ''
    filters[0].click()
    target.open = true
    target.scrollIntoView({ block: 'start' })
  }
  window.addEventListener('hashchange', revealHash)
  revealHash()

  for (const button of document.querySelectorAll('[data-copy]')) {
    button.addEventListener('click', async () => {
      const content = document.getElementById(button.dataset.copy)
      const status = document.querySelector('#copy-status')
      try {
        await navigator.clipboard.writeText(content.textContent)
        status.textContent = `${button.dataset.copy === 'prompt' ? '依頼文' : '導入コマンド'}をコピーしました。`
      } catch {
        const selection = window.getSelection()
        selection.removeAllRanges()
        const range = document.createRange()
        range.selectNodeContents(content)
        selection.addRange(range)
        status.textContent = 'コピーできませんでした。選択したテキストを手動でコピーしてください。'
      }
    })
  }
}
