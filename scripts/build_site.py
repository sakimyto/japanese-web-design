"""Build the static public guide from the same catalog as the skill."""

import hashlib
import html
import json
import shutil
from pathlib import Path

from package import KINDS, ROOT, archive, load_catalog

ORIGIN = 'https://japanese-design.sakimyto.com'
REPOSITORY = 'https://github.com/sakimyto/japanese-web-design'


def install_command(version):
    return f'npx skills add {REPOSITORY}/tree/v{version}/skills/japanese-web-design --skill japanese-web-design'


def rule_html(rule, section, sources):
    text = ' '.join(str(rule[key]) for key in ('id', 'title', 'when', 'advice', 'example', 'exception', 'check'))
    links = ' / '.join(f'<a href="{html.escape(sources[ref]["url"], quote=True)}">{html.escape(sources[ref]["title"])}</a>' for ref in rule['sources'])
    return f'''<details class="rule" id="{rule['id']}" data-section="{section['id']}" data-search="{html.escape(text, quote=True)}">
<summary><span class="rule-id">{rule['id']}</span><span class="rule-title">{html.escape(rule['title'])}</span><span class="rule-mark" aria-hidden="true">＋</span></summary>
<div class="rule-body"><p class="basis">{html.escape(KINDS[rule['kind']])}</p>
<p class="when">{html.escape(rule['when'])}</p><p>{html.escape(rule['advice'])}</p>
<dl><dt>たとえば</dt><dd>{html.escape(rule['example'])}</dd><dt>例外・注意</dt><dd>{html.escape(rule['exception'])}</dd><dt>確かめる</dt><dd>{html.escape(rule['check'])}</dd></dl>
<p class="sources">出典：{links}</p><a class="permalink" href="#{rule['id']}">この項目へのリンク</a></div></details>'''


def build(output=None):
    data = load_catalog()
    output = Path(output) if output else ROOT / 'dist' / 'site'
    output.mkdir(parents=True, exist_ok=True)
    sources = {source['id']: source for source in data['sources']}
    rules = [rule for section in data['sections'] for rule in section['rules']]
    categories = '<button type="button" class="filter active" data-category="all" aria-pressed="true">すべて</button>'
    categories += ''.join(f'<button type="button" class="filter" data-category="{section["id"]}" aria-pressed="false">{html.escape(section["title"])}</button>' for section in data['sections'])
    body = '\n'.join(rule_html(rule, section, sources) for section in data['sections'] for rule in section['rules'])
    install = install_command(data['version'])
    jsonld = json.dumps({
        '@context': 'https://schema.org', '@type': 'CreativeWork',
        'name': '日本語Webデザイン補助', 'url': ORIGIN + '/', 'inLanguage': 'ja',
        'version': data['version'], 'license': 'https://opensource.org/license/mit',
        'creator': {'@type': 'Person', '@id': 'https://sakimyto.com/#person'},
        'isPartOf': 'https://sakimyto.com/lab/japanese-web-design',
        'sameAs': REPOSITORY,
        'description': '既存のデザインスキルに重ねて使う、日本語の組版とUIのための補助スキルと出典付きガイド。',
    }, ensure_ascii=False).replace('<', '\\u003c')
    template = (ROOT / 'site' / 'index.html').read_text(encoding='utf-8')
    replacements = {'VERSION': data['version'], 'RULE_COUNT': str(len(rules)), 'SOURCE_COUNT': str(len(sources)),
                    'CATEGORIES': categories, 'RULES': body, 'INSTALL': html.escape(install), 'JSONLD': jsonld,
                    'SPEC_COUNT': str(sum(rule['kind'] == 'specification' for rule in rules)),
                    'PRACTICE_COUNT': str(sum(rule['kind'] == 'practice' for rule in rules)),
                    'HYPOTHESIS_COUNT': str(sum(rule['kind'] == 'hypothesis' for rule in rules))}
    for name, value in replacements.items():
        template = template.replace('{{' + name + '}}', value)
    if '{{' in template:
        raise ValueError('Unresolved template token')
    (output / 'index.html').write_text(template, encoding='utf-8')
    ai_template = (ROOT / 'site' / 'for-ai.html').read_text(encoding='utf-8')
    for name, value in replacements.items():
        ai_template = ai_template.replace('{{' + name + '}}', value)
    if '{{' in ai_template:
        raise ValueError('Unresolved AI template token')
    (output / 'for-ai').mkdir(exist_ok=True)
    (output / 'for-ai' / 'index.html').write_text(ai_template, encoding='utf-8')
    for name in ('style.css', 'app.js'):
        shutil.copyfile(ROOT / 'site' / name, output / name)
    bundle = archive(data)
    name = f'japanese-web-design-{data["version"]}.zip'
    (output / name).write_bytes(bundle)
    (output / f'{name}.sha256').write_text(f'{hashlib.sha256(bundle).hexdigest()}  {name}\n')
    (output / 'catalog.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    (output / 'llms.txt').write_text(f'''# 日本語Webデザイン補助 v{data['version']}

日本語の組版とUIを、既存のデザイン方針に合わせて調整する補助スキル。
技術仕様、公開実践、編集上の仮説を区別する。企業固有の数値を一律に強制しない。

- [AI向け資料]({ORIGIN}/for-ai/): 適用条件、スキル、カタログの入口。
- [スキル]({REPOSITORY}/blob/v{data['version']}/skills/japanese-web-design/SKILL.md)
- [カタログ]({ORIGIN}/catalog.json): 条件、根拠、例外、確認方法を持つ{len(rules)}項目。
- [導入と使い方]({REPOSITORY}#readme)
- [実験の記録](https://sakimyto.com/lab/japanese-web-design)

生成結果の美的な改善率、CVR向上、全環境での表示・IME対応は保証していない。
''', encoding='utf-8')
    (output / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
    (output / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{ORIGIN}/</loc></url><url><loc>{ORIGIN}/for-ai/</loc></url></urlset>\n')
    (output / '404.html').write_text('<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ページが見つかりません</title><h1>ページが見つかりません</h1><a href="/">ガイドに戻る</a></html>')
    (output / '_headers').write_text("""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'
  Permissions-Policy: camera=(), microphone=(), geolocation=()
""")
    print(f'site: OK ({len(rules)} rules, {len(sources)} sources, v{data["version"]})')
    return output


if __name__ == '__main__':
    build()
