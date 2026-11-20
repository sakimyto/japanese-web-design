import config from '../site.config.json' with { type: 'json' }

const GUIDE = `${config.origin}${config.basePath}`
const RELEASES = 'https://github.com/sakimyto/japanese-web-design/releases/download'
const ARCHIVE = /^\/japanese-web-design-(\d+\.\d+\.\d+)\.zip(?:\.sha256)?$/
// Files of the retired static guide. The guide is now a page of sakimyto.com.
const RETIRED = new Set(['/style.css', '/app.js', '/sitemap.xml'])
const ROBOTS = 'User-agent: *\nAllow: /\n'

/** Answer for a URL on the legacy host, or null when the URL belongs to another host. */
export function legacyResponse(url) {
  if (url.hostname !== config.legacyHost) return null
  if (url.pathname === '/robots.txt') return { status: 200, body: ROBOTS }
  const archive = url.pathname.match(ARCHIVE)
  if (archive) return { status: 301, location: `${RELEASES}/v${archive[1]}${url.pathname}` }
  const prefixed =
    url.pathname === config.basePath || url.pathname.startsWith(`${config.basePath}/`)
  const path = prefixed ? url.pathname.slice(config.basePath.length) : url.pathname
  // The site's canonical URLs have no trailing slash; send each visitor there in one hop.
  const page = RETIRED.has(path) ? '' : path.replace(/\/+$/, '')
  return { status: 301, location: `${GUIDE}${page}${url.search}` }
}

export default {
  async fetch(request) {
    const answer = legacyResponse(new URL(request.url))
    if (!answer) return fetch(request)
    if (answer.status === 200) {
      return new Response(answer.body, {
        headers: {
          'content-type': 'text/plain; charset=utf-8',
          'x-content-type-options': 'nosniff',
        },
      })
    }
    return new Response(null, { status: 301, headers: { location: answer.location } })
  },
}
