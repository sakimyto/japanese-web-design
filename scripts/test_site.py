import copy
import json
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_site import build, rule_html
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
