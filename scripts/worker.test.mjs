import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'
import worker, { legacyResponse } from '../worker/index.js'

const read = (path) => readFileSync(new URL(path, import.meta.url), 'utf8')
const config = JSON.parse(read('../site.config.json'))
const version = JSON.parse(read('../catalog.json')).version
const guide = `${config.origin}${config.basePath}`
const legacy = `https://${config.legacyHost}`
const releases = 'https://github.com/sakimyto/japanese-web-design/releases/download'

// Every path the legacy host answered with 200 before the guide moved, plus the slashless AI page.
const livePaths = {
  '/': guide,
  '/for-ai/': `${guide}/for-ai`,
  '/for-ai': `${guide}/for-ai`,
  '/llms.txt': `${guide}/llms.txt`,
  '/catalog.json': `${guide}/catalog.json`,
  '/sitemap.xml': guide,
  '/style.css': guide,
  '/app.js': guide,
  '/japanese-web-design-1.0.1.zip': `${releases}/v1.0.1/japanese-web-design-1.0.1.zip`,
  '/japanese-web-design-1.0.1.zip.sha256': `${releases}/v1.0.1/japanese-web-design-1.0.1.zip.sha256`,
  '/japanese-web-design-1.0.0.zip': `${releases}/v1.0.0/japanese-web-design-1.0.0.zip`,
  '/japanese-web-design-1.0.0.zip.sha256': `${releases}/v1.0.0/japanese-web-design-1.0.0.zip.sha256`,
}

const segments = ['', 'for-ai', 'nope', '..', '%2e%2e', 'evil.example', 'japanese-web-design']
const queries = ['', '?q=IME', '?next=https://evil.example/', '?a=1&b=%E3%81%82']

function boundaryUrls() {
  const urls = []
  for (const first of segments) {
    for (const second of segments) {
      for (const tail of ['', '/']) {
        for (const query of queries) urls.push(`${legacy}/${first}/${second}${tail}${query}`)
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
    { status: 301, location: `${guide}?q=IME` },
    'Query is kept and the fragment is dropped',
  )
  assert.equal(respond(new URL(`${legacy}/robots.txt`)).status, 200)
  assert.equal(
    respond(new URL(`${legacy}${config.basePath}/for-ai/`)).location,
    `${guide}/for-ai`,
    'Already prefixed paths keep one prefix',
  )
  let checked = 0
  for (const url of boundaryUrls()) {
    const result = respond(new URL(url))
    assert.equal(result.status, 301, url)
    const target = new URL(result.location)
    assert.equal(target.origin, config.origin, url)
    assert.ok(
      target.pathname === config.basePath || target.pathname.startsWith(`${config.basePath}/`),
      `Destination stays under the guide: ${url} -> ${result.location}`,
    )
    assert.ok(!target.pathname.endsWith('/'), `Destination has no trailing slash: ${url}`)
    assert.equal(target.search, new URL(url).search, `Query is kept: ${url}`)
    checked += 1
  }
  assert.equal(checked, 392)
}

test('every legacy URL has one destination, in one hop', () => {
  assertLegacyContract(legacyResponse)
  for (const suffix of ['', '.sha256']) {
    const name = `japanese-web-design-${version}.zip${suffix}`
    assert.equal(
      legacyResponse(new URL(`${legacy}/${name}`)).location,
      `${releases}/v${version}/${name}`,
      'The current release is downloaded from its GitHub Release',
    )
  }
})

test('broken mappers are rejected by the check that names their defect', () => {
  const keepsTrailingSlash = (url) =>
    url.pathname === '/' ? { status: 301, location: `${guide}/${url.search}` } : legacyResponse(url)
  const dropsPrefix = (url) =>
    url.pathname === '/llms.txt'
      ? { status: 301, location: `${config.origin}/llms.txt` }
      : legacyResponse(url)
  const sendsArchiveToTheApp = (url) =>
    url.pathname.endsWith('.zip')
      ? { status: 301, location: `${guide}${url.pathname}` }
      : legacyResponse(url)
  const dropsQuery = (url) => legacyResponse(new URL(url.origin + url.pathname))
  const doublesPrefix = (url) =>
    url.pathname.startsWith(`${config.basePath}/`)
      ? { status: 301, location: `${guide}${url.pathname}${url.search}` }
      : legacyResponse(url)
  for (const [broken, reason] of [
    [keepsTrailingSlash, 'Legacy path has its destination: /'],
    [dropsPrefix, 'Legacy path has its destination: /llms.txt'],
    [sendsArchiveToTheApp, 'Legacy path has its destination: /japanese-web-design-1.0.1.zip'],
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

test('the worker answers every request with a redirect or robots.txt', async () => {
  const moved = await worker.fetch(new Request(`${legacy}/for-ai/?q=1`))
  assert.equal(moved.status, 301)
  assert.equal(moved.headers.get('location'), `${guide}/for-ai?q=1`)
  const robots = await worker.fetch(new Request(`${legacy}/robots.txt`))
  assert.equal(robots.status, 200)
  assert.equal(await robots.text(), 'User-agent: *\nAllow: /\n')
  assert.match(robots.headers.get('content-type'), /^text\/plain/)
})

test('a request for another host is passed on instead of redirected', async () => {
  // If the retired route sakimyto.com/japanese-web-design* still reaches this Worker,
  // a redirect to the guide would loop. The request goes on to the site instead.
  const original = globalThis.fetch
  const passed = []
  globalThis.fetch = async (request) => {
    passed.push(request.url)
    return new Response('site')
  }
  try {
    for (const path of ['', '/', '/for-ai', '/catalog.json', '?q=IME']) {
      const url = `${guide}${path}`
      assert.equal(legacyResponse(new URL(url)), null, url)
      const response = await worker.fetch(new Request(url))
      assert.equal(await response.text(), 'site', url)
    }
    assert.equal(passed.length, 5)
  } finally {
    globalThis.fetch = original
  }
})

test('the Worker is bound to the legacy host only and serves no assets', () => {
  const wrangler = JSON.parse(read('../wrangler.jsonc'))
  assert.deepEqual(wrangler.routes, [{ pattern: config.legacyHost, custom_domain: true }])
  assert.equal(wrangler.main, 'worker/index.js')
  assert.equal(wrangler.assets, undefined)
  assert.deepEqual(config, {
    origin: 'https://sakimyto.com',
    basePath: '/japanese-web-design',
    legacyHost: 'japanese-design.sakimyto.com',
  })
})
