"""Offline pinned skill staging and guarded rollback regression tests."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/metaprompt-selection-skill.py'


class PinnedSkillInstallTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'Pinned staging helper has not been implemented')
        spec = importlib.util.spec_from_file_location('selection_install_test_subject', SCRIPT)
        self.tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.tool)
        self.tmp = tempfile.TemporaryDirectory(prefix='selection-install-test-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'benchmark'
        self.package = self.root / 'candidates/demo'
        self.package.mkdir(parents=True)
        self.contents = {'SKILL.md': b'# Native demo\n', 'LICENSE': b'MIT fixture\n',
                         'references/guide.md': b'Keep facts grounded.\n',
                         'scripts/helper.py': b'print("offline")\n'}
        hashes = {}
        for name, content in self.contents.items():
            p = self.package / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(content)
            hashes['candidates/demo/' + name] = hashlib.sha256(content).hexdigest()
        self.source = {'schema_version': 1, 'candidates': [{'id': 'demo', 'eligibility': 'eligible',
                         'entrypoint': 'candidates/demo/SKILL.md', 'files': hashes}]}
        self.save_manifest()
        self.dest = self.base / 'native-demo'

    def save_manifest(self):
        (self.root / 'sources.json').write_text(json.dumps(self.source))

    def stage(self):
        return self.tool.stage('demo', self.dest, self.root)

    def rollback(self):
        return self.tool.rollback('demo', self.dest, self.root)

    def test_stage_copies_complete_verified_native_package(self):
        self.stage()
        actual = {str(p.relative_to(self.dest)): p.read_bytes() for p in self.dest.rglob('*') if p.is_file()}
        self.assertEqual(actual, self.contents)
        self.assertEqual(sorted(p.name for p in self.base.iterdir()), ['benchmark', 'native-demo'])

    def test_existing_destination_is_preserved(self):
        self.dest.mkdir()
        with self.assertRaises(ValueError):
            self.stage()
        self.assertEqual(list(self.dest.iterdir()), [])
        (self.dest / 'user.txt').write_text('preexisting')
        with self.assertRaises(ValueError):
            self.stage()
        self.assertEqual((self.dest / 'user.txt').read_text(), 'preexisting')

    def test_tampered_source_aborts_before_destination_creation(self):
        (self.package / 'SKILL.md').write_text('tampered')
        with self.assertRaises(ValueError):
            self.stage()
        self.assertFalse(self.dest.exists())

    def test_unsafe_inventory_path_is_rejected(self):
        self.source['candidates'][0]['files']['../outside'] = '0' * 64
        self.save_manifest()
        with self.assertRaises(ValueError):
            self.stage()
        self.assertFalse(self.dest.exists())

    def test_source_symlink_is_rejected(self):
        p = self.package / 'LICENSE'
        p.unlink()
        outside = self.base / 'outside-license'
        outside.write_bytes(self.contents['LICENSE'])
        p.symlink_to(outside)
        with self.assertRaises(ValueError):
            self.stage()
        self.assertFalse(self.dest.exists())

    def test_destination_symlink_parent_is_rejected(self):
        parent = self.base / 'linked'
        parent.symlink_to(self.base, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.tool.stage('demo', parent / 'native-demo', self.root)
        self.assertFalse(self.dest.exists())

    def test_rollback_removes_only_exact_verified_copy(self):
        self.stage()
        self.rollback()
        self.assertFalse(self.dest.exists())
        self.assertTrue((self.package / 'SKILL.md').is_file())

    def test_rollback_cannot_remove_the_pinned_source_package(self):
        with self.assertRaises(ValueError):
            self.tool.rollback('demo', self.package, self.root)
        self.assertTrue((self.package / 'SKILL.md').is_file())

    def test_rollback_preserves_modified_copy(self):
        self.stage()
        (self.dest / 'SKILL.md').write_text('user modified')
        with self.assertRaises(ValueError):
            self.rollback()
        self.assertEqual((self.dest / 'SKILL.md').read_text(), 'user modified')

    def test_rollback_preserves_extra_file_and_empty_directory(self):
        self.stage()
        (self.dest / 'notes.txt').write_text('user notes')
        with self.assertRaises(ValueError):
            self.rollback()
        (self.dest / 'notes.txt').unlink()
        (self.dest / 'extra-empty').mkdir()
        with self.assertRaises(ValueError):
            self.rollback()
        self.assertTrue((self.dest / 'extra-empty').is_dir())

    def test_uninventoried_source_file_is_not_silently_omitted(self):
        (self.package / 'unlisted.txt').write_text('unexpected native input')
        with self.assertRaises(ValueError):
            self.stage()
        self.assertFalse(self.dest.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
