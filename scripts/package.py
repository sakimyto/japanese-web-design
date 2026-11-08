"""Validate the catalog, render references, and build an offline skill archive."""

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = 'japanese-web-design'
SKILL = ROOT / 'skills' / SKILL_NAME
KINDS = {
    'specification': '技術仕様・標準の解説',
    'practice': '公開実践（適用範囲を確認する）',
    'hypothesis': '編集上の仮説（実画面で比較する）',
}
SCOPES = {'japanese': '日本語', 'mixed': '日本語で差が出やすい共通事項', 'shared': '全言語に共通'}
STATIC_FILES = ('SKILL.md', 'LICENSE.txt', 'references/evaluation.md', 'assets/starter.css', 'references/recipes.md')


def required_text(obj, key):
    if not isinstance(obj, dict):
        raise ValueError('Expected object')
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'Missing text: {key}')
    return value


def validate(data):
    if not isinstance(data, dict):
        raise ValueError('Catalog must be an object')
    if not re.fullmatch(r'\d+\.\d+\.\d+', required_text(data, 'version')):
        raise ValueError('Invalid version')
    date.fromisoformat(required_text(data, 'reviewedAt'))
    sources = data.get('sources')
    sections = data.get('sections')
    if not isinstance(sources, list) or not sources or not isinstance(sections, list) or not sections:
        raise ValueError('Nonempty sources and sections required')
    source_ids, section_ids, rule_ids = set(), set(), set()
    for source in sources:
        sid = required_text(source, 'id')
        if not re.fullmatch(r'[a-z][a-z0-9-]*', sid) or sid in source_ids:
            raise ValueError(f'Invalid or duplicate source: {sid}')
        source_ids.add(sid)
        required_text(source, 'title')
        required_text(source, 'limits')
        date.fromisoformat(required_text(source, 'reviewedAt'))
        url = urlsplit(required_text(source, 'url'))
        if url.scheme != 'https' or not url.hostname or url.username or url.password:
            raise ValueError(f'Invalid source URL: {sid}')
    for section in sections:
        sid = required_text(section, 'id')
        if not re.fullmatch(r'[a-z][a-z0-9-]*', sid) or sid in section_ids:
            raise ValueError(f'Invalid or duplicate section: {sid}')
        section_ids.add(sid)
        required_text(section, 'title')
        rules = section.get('rules')
        if not isinstance(rules, list) or not rules:
            raise ValueError(f'Empty section: {sid}')
        for rule in rules:
            rid = required_text(rule, 'id')
            if not re.fullmatch(r'[A-Z][0-9]{2}', rid) or rid in rule_ids:
                raise ValueError(f'Invalid or duplicate rule: {rid}')
            rule_ids.add(rid)
            if rule.get('kind') not in KINDS or rule.get('scope') not in SCOPES:
                raise ValueError(f'Invalid evidence classification: {rid}')
            for key in ('title', 'when', 'advice', 'example', 'exception', 'check'):
                required_text(rule, key)
            refs = rule.get('sources')
            if not isinstance(refs, list) or not refs:
                raise ValueError(f'Missing sources: {rid}')
            if any(not isinstance(ref, str) or ref not in source_ids for ref in refs):
                raise ValueError(f'Unknown source: {rid}')
    return data


def load_catalog():
    return validate(json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8')))


def render(data):
    validate(data)
    sources = {source['id']: source for source in data['sources']}
    result = {}
    for section in data['sections']:
        parts = [f"# {section['title']}", '',
                 f"版: {data['version']}。資料確認日: {data['reviewedAt']}。", '',
                 'catalog.jsonから生成。数値の目安と公開実践は、用途に合わせて比較する。', '']
        for rule in section['rules']:
            links = '、'.join(f"[{sources[ref]['title']}]({sources[ref]['url']})" for ref in rule['sources'])
            parts += [f"## {rule['id']} {rule['title']}", '',
                      f"根拠の種類: {KINDS[rule['kind']]}。対象: {SCOPES[rule['scope']]}。", '',
                      f"使う場面: {rule['when']}", '',
                      rule['advice'], '', f"例: {rule['example']}", '',
                      f"例外・注意: {rule['exception']}", '', f"確認: {rule['check']}", '',
                      f'出典: {links}', '']
        result[f"references/{section['id']}.md"] = '\n'.join(parts)
    parts = ['# 参照資料と限界', '', f"資料確認日: {data['reviewedAt']}。原文の転載ではなく、自作の説明から参照する。", '']
    for source in data['sources']:
        parts += [f"## {source['id']}", '', f"[{source['title']}]({source['url']})", '', source['limits'], '']
    result['references/sources.md'] = '\n'.join(parts)
    return result


def sync(data, root=SKILL, check=False):
    for name, content in render(data).items():
        target = root / name
        if check:
            if target.is_symlink() or not target.is_file() or target.read_text(encoding='utf-8') != content:
                raise ValueError(f'Generated file differs: {name}')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')


def archive(data, root=SKILL):
    generated = render(data)
    expected = set(STATIC_FILES) | set(generated)
    if root.is_symlink():
        raise ValueError('Skill directory must not be a symlink')
    actual = set()
    for entry in root.rglob('*'):
        if entry.is_symlink():
            raise ValueError(f'Symlink rejected: {entry.relative_to(root)}')
        if entry.is_file():
            actual.add(entry.relative_to(root).as_posix())
    if actual != expected:
        raise ValueError(f'Package manifest differs: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}')
    sync(data, root, check=True)
    skill = (root / 'SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith(f'---\nname: {SKILL_NAME}\n') or f'version: "{data["version"]}"' not in skill:
        raise ValueError('Skill metadata does not match catalog')
    for filename in expected:
        if filename.endswith('.md'):
            content = (root / filename).read_text(encoding='utf-8')
            for link in re.findall(r'\]\(([^)]+)\)', content):
                if urlsplit(link).scheme or link.startswith('#'):
                    continue
                target = (root / filename).parent / link.split('#')[0]
                resolved = target.resolve()
                if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                    raise ValueError(f'Invalid local link in {filename}: {link}')
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as bundle:
        for name in sorted(expected):
            info = zipfile.ZipInfo(f'{SKILL_NAME}/{name}', date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, (root / name).read_bytes())
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('render', 'check', 'pack'))
    args = parser.parse_args()
    data = load_catalog()
    if args.command == 'render':
        sync(data)
    else:
        result = archive(data)
        if args.command == 'pack':
            destination = ROOT / 'dist'
            destination.mkdir(exist_ok=True)
            name = f'{SKILL_NAME}-{data["version"]}.zip'
            (destination / name).write_bytes(result)
            (destination / f'{name}.sha256').write_text(f'{hashlib.sha256(result).hexdigest()}  {name}\n')
    count = sum(len(section['rules']) for section in data['sections'])
    print(f'{args.command}: OK ({count} rules, {len(data["sources"])} sources)')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError) as error:
        print(f'package: {error}', file=sys.stderr)
        sys.exit(1)
