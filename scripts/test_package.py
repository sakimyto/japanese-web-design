import copy
import importlib.util
import io
import os
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('skill_package', Path(__file__).with_name('package.py'))
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = PACKAGE.load_catalog()

    def test_every_rule_has_valid_sources(self):
        self.assertIs(PACKAGE.validate(self.data), self.data)
        for section in self.data['sections']:
            for rule in section['rules']:
                self.assertIn(f"## {rule['id']} ", PACKAGE.render(self.data)[f"references/{section['id']}.md"])

    def test_each_required_field_rejects_missing_and_empty_variants(self):
        cases = 0
        for section_index, section in enumerate(self.data['sections']):
            for rule_index, rule in enumerate(section['rules']):
                for field in ('id', 'title', 'advice', 'example', 'exception', 'check', 'when', 'sources', 'kind', 'scope'):
                    for empty in (None, ''):
                        data = copy.deepcopy(self.data)
                        changed = data['sections'][section_index]['rules'][rule_index]
                        if empty is None:
                            changed.pop(field)
                        else:
                            changed[field] = empty
                        with self.subTest(rule=rule['id'], field=field, empty=empty):
                            with self.assertRaises(ValueError):
                                PACKAGE.validate(data)
                        cases += 1
        self.assertEqual(cases, 1280)

    def test_semantically_broken_catalogs_are_rejected(self):
        variants = []
        data = copy.deepcopy(self.data)
        data['sources'].pop(0)
        variants.append(data)
        data = copy.deepcopy(self.data)
        data['sections'][1]['rules'][0]['id'] = data['sections'][0]['rules'][0]['id']
        variants.append(data)
        data = copy.deepcopy(self.data)
        data['sections'][0]['id'] = '../outside'
        variants.append(data)
        data = copy.deepcopy(self.data)
        data['sources'][0]['url'] = 'file:///private/source'
        variants.append(data)
        data = copy.deepcopy(self.data)
        data['sources'][0]['url'] = 'https://user:password@example.com/'
        variants.append(data)
        for index, variant in enumerate(variants):
            with self.subTest(variant=index):
                with self.assertRaises(ValueError):
                    PACKAGE.validate(variant)


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.data = PACKAGE.load_catalog()
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / PACKAGE.SKILL_NAME
        shutil.copytree(PACKAGE.SKILL, self.root)

    def test_actual_archive_matches_only_skill_files(self):
        result = PACKAGE.archive(self.data, self.root)
        with zipfile.ZipFile(io.BytesIO(result)) as bundle:
            expected = set(PACKAGE.STATIC_FILES) | set(PACKAGE.render(self.data))
            self.assertEqual(set(bundle.namelist()), {f'{PACKAGE.SKILL_NAME}/{name}' for name in expected})
            for entry in bundle.infolist():
                self.assertEqual(bundle.read(entry), (self.root.parent / entry.filename).read_bytes())

    def test_archive_is_identical_after_timestamp_changes(self):
        first = PACKAGE.archive(self.data, self.root)
        for file in self.root.rglob('*'):
            if file.is_file():
                os.utime(file, (1234567890, 1234567890))
        self.assertEqual(first, PACKAGE.archive(self.data, self.root))

    def test_extra_file_is_rejected(self):
        (self.root / 'unreviewed.txt').write_text('not part of the skill')
        with self.assertRaisesRegex(ValueError, 'extra='):
            PACKAGE.archive(self.data, self.root)

    def test_missing_file_is_rejected(self):
        (self.root / 'LICENSE.txt').unlink()
        with self.assertRaisesRegex(ValueError, 'missing='):
            PACKAGE.archive(self.data, self.root)

    def test_symlink_is_rejected(self):
        (self.root / 'assets' / 'linked.css').symlink_to(self.root / 'assets' / 'starter.css')
        with self.assertRaisesRegex(ValueError, 'Symlink rejected'):
            PACKAGE.archive(self.data, self.root)

    def test_stale_reference_is_rejected(self):
        (self.root / 'references' / 'typography.md').write_text('outdated advice')
        with self.assertRaisesRegex(ValueError, 'Generated file differs'):
            PACKAGE.archive(self.data, self.root)

    def test_local_link_outside_package_is_rejected(self):
        skill = self.root / 'SKILL.md'
        skill.write_text(skill.read_text() + '\n[outside](../outside.md)\n')
        (self.root.parent / 'outside.md').write_text('outside')
        with self.assertRaisesRegex(ValueError, 'Invalid local link'):
            PACKAGE.archive(self.data, self.root)

    def test_version_mismatch_is_rejected(self):
        skill = self.root / 'SKILL.md'
        skill.write_text(skill.read_text().replace('version: "1.0.0"', 'version: "0.0.0"'))
        with self.assertRaisesRegex(ValueError, 'metadata does not match'):
            PACKAGE.archive(self.data, self.root)


if __name__ == '__main__':
    unittest.main()
