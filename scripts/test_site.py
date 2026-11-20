import copy
import hashlib
import json
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_site import BASE_PATH, LEGACY_HOST, ORIGIN, SITE, build, install_command, rule_html
from package import ROOT, load_catalog


class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rules = []
        self.ids = []
        self.scripts = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'details' and 'rule' in attrs.get('class', '').split():
            self.rules.append(attrs)
        if tag == 'script':
            self.scripts.append(attrs)
        self.links.extend(attrs[name] for name in ('href', 'src') if attrs.get(name))


def links_outside_base(content):
    parsed = Elements()
    parsed.feed(content)
    return sorted({link for link in parsed.links if link.startswith('/') and not link.startswith(BASE_PATH + '/')})


class SiteTests(unittest.TestCase):
    def test_install_command_pins_a_tree_url_instead_of_a_skill_suffix(self):
        import shlex
        from urllib.parse import urlsplit
        for version in ('1.0.0', '1.0.1', '2.5.8'):
            command = shlex.split(install_command(version))
            self.assertEqual(command[:3], ['npx', 'skills', 'add'])
            parsed = urlsplit(command[3])
            self.assertEqual(parsed.netloc, 'github.com')
            self.assertEqual(parsed.path, f'/sakimyto/japanese-web-design/tree/v{version}/skills/japanese-web-design')
            self.assertEqual(command[4:], ['--skill', 'japanese-web-design'])

    def test_all_rules_render_exactly_once_and_match_data(self):
        data = load_catalog()
        with tempfile.TemporaryDirectory() as temporary:
            output = build(temporary)
            content = (output / 'index.html').read_text()
            parsed = Elements()
            parsed.feed(content)
            rules = [rule for section in data['sections'] for rule in section['rules']]
            self.assertEqual({rule['id'] for rule in rules}, {rule['id'] for rule in parsed.rules})
            self.assertEqual(len(rules), len(parsed.rules))
            self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
            self.assertNotIn('{{', content)
            self.assertNotIn('0.1.0', content)
            self.assertEqual(json.loads((output / 'catalog.json').read_text()), data)
            self.assertTrue((output / f'japanese-web-design-{data["version"]}.zip').is_file())
            self.assertIn('https://sakimyto.com/lab/japanese-web-design', content)

    def assert_landing_contract(self, content):
        self.assertIn('いつものデザインスキルに、日本語の調整を。', content)
        self.assertLess(content.index('id="use"'), content.index('id="guide"'), 'Install before reference')
        self.assertLess(content.index('id="scope-title"'), content.index('id="guide"'), 'Explain before reference')
        self.assertIn(f'href="{BASE_PATH}/for-ai/"', content, 'Dedicated AI entrance')
        heading = content.split('<h1', 1)[1].split('</h1>', 1)[0]
        self.assertNotIn('<br', heading, 'Natural heading wrapping')

    def test_landing_explains_and_installs_before_the_full_reference(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = build(temporary)
            content = (output / 'index.html').read_text()
            self.assert_landing_contract(content)

    def test_landing_contract_detects_missing_entrance_and_wrong_priority(self):
        with tempfile.TemporaryDirectory() as temporary:
            content = (build(temporary) / 'index.html').read_text()
            self.assert_landing_contract(content)
            with self.assertRaisesRegex(AssertionError, 'Dedicated AI entrance'):
                self.assert_landing_contract(content.replace(f'href="{BASE_PATH}/for-ai/"', f'href="{BASE_PATH}/"'))
            moved = content.replace('id="use"', 'id="temporary"').replace('id="guide"', 'id="use"').replace('id="temporary"', 'id="guide"')
            with self.assertRaisesRegex(AssertionError, 'Install before reference'):
                self.assert_landing_contract(moved)

    def test_ai_entrance_links_data_and_preserves_a_human_return(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = build(temporary)
            page = output / 'for-ai' / 'index.html'
            self.assertTrue(page.is_file(), 'Dedicated AI page must be published')
            content = page.read_text()
            for href in ('/catalog.json', '/llms.txt', '/#guide', '/#use'):
                self.assertIn(f'href="{BASE_PATH}{href}"', content)
            self.assertIn(f'rel="canonical" href="{SITE}/for-ai/"', content)
            self.assertNotIn('app.js"', content, 'Do not initialize guide controls on a resource page')
            self.assertIn(f'<loc>{SITE}/for-ai/</loc>', (output / 'sitemap.xml').read_text())

    def test_site_is_published_under_the_sakimyto_com_path(self):
        self.assertEqual((ORIGIN, BASE_PATH, SITE), ('https://sakimyto.com', '/japanese-web-design', 'https://sakimyto.com/japanese-web-design'))
        with tempfile.TemporaryDirectory() as temporary:
            output = build(temporary)
            pages = {name: (output / name).read_text() for name in ('index.html', 'for-ai/index.html', '404.html')}
            for name, content in pages.items():
                with self.subTest(page=name):
                    self.assertEqual(links_outside_base(content), [], 'BASE: local links stay under the base path')
            index = pages['index.html']
            self.assertIn(f'<link rel="canonical" href="{SITE}/">', index)
            self.assertIn(f'<meta property="og:url" content="{SITE}/">', index)
            self.assertIn(f'"url": "{SITE}/"', index)
            self.assertIn('"isPartOf": "https://sakimyto.com/lab/japanese-web-design"', index)
            self.assertIn(f'<loc>{SITE}/</loc>', (output / 'sitemap.xml').read_text())
            self.assertIn(f'({SITE}/for-ai/)', (output / 'llms.txt').read_text())
            self.assertIn(f'({SITE}/catalog.json)', (output / 'llms.txt').read_text())
            self.assertFalse((output / 'robots.txt').exists(), 'robots.txt is only read at the host root')
            self.assertTrue((output / '_headers').read_text().startswith(f'{BASE_PATH}/*\n'))
            published = sorted(path.relative_to(output).as_posix() for path in output.rglob('*') if path.is_file())
            archive_name = f'japanese-web-design-{load_catalog()["version"]}.zip'
            self.assertEqual(published, sorted([
                '404.html', '_headers', 'app.js', 'catalog.json', 'for-ai/index.html', 'index.html',
                archive_name, f'{archive_name}.sha256', 'llms.txt', 'sitemap.xml', 'style.css',
            ]))
            for path in output.rglob('*'):
                if path.is_file() and path.suffix != '.zip':
                    with self.subTest(file=path.name):
                        self.assertNotIn(LEGACY_HOST, path.read_text(), 'ORIGIN: the legacy host is not published')

    def test_rebuilding_removes_files_from_an_earlier_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = build(temporary)
            first = sorted(path.relative_to(output).as_posix() for path in output.rglob('*') if path.is_file())
            (output / 'robots.txt').write_text('Sitemap: https://japanese-design.sakimyto.com/sitemap.xml\n')
            (output / 'japanese-web-design-1.0.0.zip').write_bytes(b'stale')
            (output / 'old').mkdir()
            (output / 'old' / 'index.html').write_text('stale')
            build(temporary)
            second = sorted(path.relative_to(output).as_posix() for path in output.rglob('*') if path.is_file())
            self.assertEqual(second, first, 'A deploy publishes only what the current build wrote')

    def test_deploy_builds_before_publishing(self):
        scripts = json.loads((ROOT / 'package.json').read_text())['scripts']
        self.assertTrue(scripts['deploy'].startswith('bun run build && '), 'Never publish a stale dist')

    def test_missing_base_path_is_detectable(self):
        with tempfile.TemporaryDirectory() as temporary:
            content = (build(temporary) / 'index.html').read_text()
            self.assertEqual(links_outside_base(content), [])
            self.assertEqual(links_outside_base(content.replace(f'href="{BASE_PATH}/style.css"', 'href="/style.css"')), ['/style.css'])
            self.assertEqual(links_outside_base(content.replace(f'href="{BASE_PATH}/for-ai/"', 'href="/japanese-web-designer/"')), ['/japanese-web-designer/'])

    def test_worker_routes_match_the_site_config(self):
        config = json.loads((ROOT / 'site.config.json').read_text())
        self.assertEqual(config, {'origin': ORIGIN, 'basePath': BASE_PATH, 'legacyHost': LEGACY_HOST})
        wrangler = json.loads((ROOT / 'wrangler.jsonc').read_text())
        host = ORIGIN.removeprefix('https://')
        self.assertEqual(wrangler['routes'], [
            {'pattern': f'{host}{BASE_PATH}*', 'zone_name': host},
            {'pattern': LEGACY_HOST, 'custom_domain': True},
        ])
        assets = wrangler['assets']
        self.assertEqual(assets['base_path'], BASE_PATH)
        self.assertEqual(assets['run_worker_first'], ['/*', f'!{BASE_PATH}/*'], 'Guide files are served with _headers, without the script')
        self.assertEqual((wrangler['main'], assets['binding'], assets['not_found_handling']), ('worker/index.js', 'ASSETS', '404-page'))

    def test_released_archive_keeps_its_published_hash(self):
        evidence = json.loads((ROOT / 'docs' / 'release-evidence.json').read_text())
        published = {item['sha256'] for item in evidence['deployment']['results'] if 'sha256' in item}
        self.assertEqual(len(published), 1)
        with tempfile.TemporaryDirectory() as temporary:
            output = build(temporary)
            name = f'japanese-web-design-{evidence["version"]}.zip'
            self.assertEqual({hashlib.sha256((output / name).read_bytes()).hexdigest()}, published)
            self.assertEqual((output / f'{name}.sha256').read_text(), f'{published.pop()}  {name}\n')

    def test_catalog_text_cannot_introduce_markup_or_attributes(self):
        data = load_catalog()
        section = data['sections'][0]
        sources = {source['id']: source for source in data['sources']}
        original = section['rules'][0]
        for field in ('title', 'when', 'advice', 'example', 'exception', 'check'):
            for payload in ('<script>alert(1)</script>', '"><img src=x onerror=alert(1)>', '<a href="javascript:alert(1)">link</a>'):
                changed = copy.deepcopy(original)
                changed[field] = payload
                rendered = rule_html(changed, section, sources)
                with self.subTest(field=field, payload=payload):
                    self.assertNotIn('<script>', rendered)
                    self.assertNotIn('<img ', rendered)
                    self.assertNotIn('<a href="javascript:', rendered)
                    self.assertIn('&lt;', rendered)

    def test_broken_unescaped_renderer_is_detectable(self):
        data = load_catalog()
        rule = copy.deepcopy(data['sections'][0]['rules'][0])
        rule['title'] = '<script>alert(1)</script>'
        broken = f'<summary>{rule["title"]}</summary>'
        self.assertIn('<script>', broken)
        correct = rule_html(rule, data['sections'][0], {source['id']: source for source in data['sources']})
        self.assertNotIn('<script>', correct)


if __name__ == '__main__':
    unittest.main()
