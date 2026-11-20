import config from '../site.config.json' with { type: 'json' }

const PRIMARY = `${config.origin}${config.basePath}`
const RELEASE_1_0_0 = 'https://github.com/sakimyto/japanese-web-design/releases/download/v1.0.0'
// The build publishes only the current version, so the first release moves to its GitHub Release.
const RETIRED = {
  '/japanese-web-design-1.0.0.zip': `${RELEASE_1_0_0}/japanese-web-design-1.0.0.zip`,
  '/japanese-web-design-1.0.0.zip.sha256': `${RELEASE_1_0_0}/japanese-web-design-1.0.0.zip.sha256`,
}
const ROBOTS = 'User-agent: *\nAllow: /\n'

/** Answer for a URL on the legacy host, or null when the URL belongs to the primary host. */
export function legacyResponse(url) {
  if (url.hostname !== config.legacyHost) return null
  if (url.pathname === '/robots.txt') return { status: 200, body: ROBOTS }
  if (RETIRED[url.pathname]) return { status: 301, location: RETIRED[url.pathname] }
  const prefixed =
    url.pathname === config.basePath || url.pathname.startsWith(`${config.basePath}/`)
  const path = prefixed ? url.pathname.slice(config.basePath.length) : url.pathname
  return { status: 301, location: `${PRIMARY}${path}${url.search}` }
}

export default {
  async fetch(request, env) {
    const answer = legacyResponse(new URL(request.url))
    if (!answer) return env.ASSETS.fetch(request)
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
