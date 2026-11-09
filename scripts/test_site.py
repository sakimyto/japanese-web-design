import copy
import json
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_site import build, install_command, rule_html
from package import load_catalog


class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rules = []
        self.ids = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'details' and 'rule' in attrs.get('class', '').split():
            self.rules.append(attrs)
        if tag == 'script':
            self.scripts.append(attrs)


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
        self.assertIn('href="/for-ai/"', content, 'Dedicated AI entrance')
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
                self.assert_landing_contract(content.replace('href="/for-ai/"', 'href="/"'))
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
                self.assertIn(f'href="{href}"', content)
            self.assertIn('rel="canonical" href="https://japanese-design.sakimyto.com/for-ai/"', content)
            self.assertNotIn('src="/app.js"', content, 'Do not initialize guide controls on a resource page')
            self.assertIn('https://japanese-design.sakimyto.com/for-ai/', (output / 'sitemap.xml').read_text())

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
