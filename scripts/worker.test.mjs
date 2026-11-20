import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'
import worker, { legacyResponse } from '../worker/index.js'

const config = JSON.parse(readFileSync(new URL('../site.config.json', import.meta.url), 'utf8'))
const primary = `${config.origin}${config.basePath}`
const legacy = `https://${config.legacyHost}`
const release = 'https://github.com/sakimyto/japanese-web-design/releases/download/v1.0.0'

// Every path that answered 200 on the legacy host on 2026-11-20, plus the slashless AI page.
const livePaths = {
  '/': `${primary}/`,
  '/for-ai/': `${primary}/for-ai/`,
  '/for-ai': `${primary}/for-ai`,
  '/llms.txt': `${primary}/llms.txt`,
  '/catalog.json': `${primary}/catalog.json`,
  '/sitemap.xml': `${primary}/sitemap.xml`,
  '/style.css': `${primary}/style.css`,
  '/app.js': `${primary}/app.js`,
  '/japanese-web-design-1.0.1.zip': `${primary}/japanese-web-design-1.0.1.zip`,
  '/japanese-web-design-1.0.1.zip.sha256': `${primary}/japanese-web-design-1.0.1.zip.sha256`,
  '/japanese-web-design-1.0.0.zip': `${release}/japanese-web-design-1.0.0.zip`,
  '/japanese-web-design-1.0.0.zip.sha256': `${release}/japanese-web-design-1.0.0.zip.sha256`,
}

const segments = ['', 'for-ai', 'nope', '..', '%2e%2e', 'evil.example', 'japanese-web-design']
const queries = ['', '?q=IME', '?next=https://evil.example/', '?a=1&b=%E3%81%82']

function boundaryUrls(origin) {
  const urls = []
  for (const first of segments) {
    for (const second of segments) {
      for (const tail of ['', '/']) {
        for (const query of queries) urls.push(`${origin}/${first}/${second}${tail}${query}`)
      }
    }
  }
  return urls
}

function assertLegacyContract(respond) {
  for (const [path, location] of Object.entries(livePaths)) {
    assert.deepEqual(
      respond(new URL(`${legacy}${path}`)),
      { status: 301, location },
      `Legacy path has its destination: ${path}`,
    )
  }
  assert.deepEqual(
    respond(new URL(`${legacy}/?q=IME#T04`)),
    { status: 301, location: `${primary}/?q=IME` },
    'Query is kept and the fragment is dropped',
  )
  assert.equal(respond(new URL(`${legacy}/robots.txt`)).status, 200)
  assert.equal(
    respond(new URL(`${legacy}${config.basePath}/for-ai/`)).location,
    `${primary}/for-ai/`,
    'Already prefixed paths keep one prefix',
  )
  let checked = 0
  for (const url of boundaryUrls(legacy)) {
    const result = respond(new URL(url))
    assert.equal(result.status, 301, url)
    const target = new URL(result.location)
    assert.equal(target.origin, config.origin, url)
    assert.ok(
      target.pathname === config.basePath || target.pathname.startsWith(`${config.basePath}/`),
      `${url} -> ${result.location}`,
    )
    assert.equal(target.search, new URL(url).search, url)
    checked += 1
  }
  assert.equal(checked, 392)
  for (const url of [...boundaryUrls(config.origin), `${primary}/`, `${primary}/for-ai/`]) {
    assert.equal(respond(new URL(url)), null, `Primary host is never redirected: ${url}`)
  }
}

test('every legacy URL has one destination on the primary origin', () => {
  assertLegacyContract(legacyResponse)
})

test('broken mappers are rejected by the same contract', () => {
  const dropsPrefix = (url) =>
    url.hostname === config.legacyHost
      ? { status: 301, location: `${config.origin}${url.pathname}${url.search}` }
      : null
  const redirectsEveryHost = (url) =>
    legacyResponse(new URL(`${legacy}${url.pathname}${url.search}`))
  const forgetsRetiredRelease = (url) => {
    const result = legacyResponse(url)
    return result?.location?.startsWith(release)
      ? { status: 301, location: `${primary}${url.pathname}` }
      : result
  }
  const dropsQuery = (url) => legacyResponse(new URL(url.origin + url.pathname))
  const doublesPrefix = (url) =>
    url.hostname === config.legacyHost && url.pathname.startsWith(`${config.basePath}/`)
      ? { status: 301, location: `${primary}${url.pathname}${url.search}` }
      : legacyResponse(url)
  // Each variant must fail at the check that names its defect, not at an unrelated one.
  for (const [broken, reason] of [
    [dropsPrefix, 'Legacy path has its destination: /'],
    [redirectsEveryHost, `Primary host is never redirected: ${config.origin}//`],
    [forgetsRetiredRelease, 'Legacy path has its destination: /japanese-web-design-1.0.0.zip'],
    [dropsQuery, 'Query is kept and the fragment is dropped'],
    [doublesPrefix, 'Already prefixed paths keep one prefix'],
  ]) {
    assert.throws(
      () => assertLegacyContract(broken),
      (error) => error.message.split('\n')[0] === reason,
      reason,
    )
  }
})

test('the worker redirects the legacy host and serves the primary host from assets', async () => {
  const served = []
  const env = {
    ASSETS: {
      fetch: async (request) => {
        served.push(request.url)
        return new Response('asset')
      },
    },
  }
  const moved = await worker.fetch(new Request(`${legacy}/for-ai/?q=1`), env)
  assert.equal(moved.status, 301)
  assert.equal(moved.headers.get('location'), `${primary}/for-ai/?q=1`)
  const robots = await worker.fetch(new Request(`${legacy}/robots.txt`), env)
  assert.equal(robots.status, 200)
  assert.equal(await robots.text(), 'User-agent: *\nAllow: /\n')
  assert.match(robots.headers.get('content-type'), /^text\/plain/)
  assert.deepEqual(served, [])
  const asset = await worker.fetch(new Request(primary), env)
  assert.equal(await asset.text(), 'asset')
  assert.deepEqual(served, [primary])
})
