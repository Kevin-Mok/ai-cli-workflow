"""Safety regressions: removing guards or verification must lose these checks."""
import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/executable_home-storage-offload'


class OffloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if SCRIPT.exists():
            loader = importlib.machinery.SourceFileLoader('offload', str(SCRIPT))
            spec = importlib.util.spec_from_loader(loader.name, loader)
            cls.mod = importlib.util.module_from_spec(spec)
            loader.exec_module(cls.mod)

    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'home offload helper is not implemented')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / 'home'
        self.usb = Path(self.tmp.name) / 'usb'
        self.home.mkdir()
        self.usb.mkdir()
        self.src = self.home / 'Videos'
        self.src.mkdir()
        (self.src / 'movie').write_bytes(b'video\x00payload')
        (self.src / 'relative').symlink_to('movie')
        self.mod.PLAIN = True

    def test_cli_requires_explicit_destination(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('--destination', result.stderr)

    def test_cli_passes_selected_destination_to_preflight(self):
        with patch.object(sys, 'argv', [str(SCRIPT), '--destination', str(self.usb), '--plain']):
            with patch.object(self.mod, 'preflight', side_effect=RuntimeError('preflight reached')) as preflight:
                with self.assertRaisesRegex(RuntimeError, 'preflight reached'):
                    self.mod.main()
        preflight.assert_called_once_with(Path.home(), self.usb)

    def test_selected_moves_leave_ollama_local(self):
        models = self.home / '.ollama'
        models.mkdir()
        (models / 'model').write_bytes(b'local model')
        for name in self.mod.FOLDERS:
            self.mod.relocate(self.home / name, self.usb, True)
        self.assertFalse(models.is_symlink())
        self.assertEqual((models / 'model').read_bytes(), b'local model')
        self.assertFalse((self.usb / '.ollama').exists())

    def test_preview_does_not_copy_or_link(self):
        self.mod.relocate(self.src, self.usb, False)
        self.assertFalse((self.usb / 'Videos').exists())
        self.assertFalse(self.src.is_symlink())

    def test_real_copy_preserves_data_and_links_then_rerun_skips(self):
        self.mod.relocate(self.src, self.usb, True)
        self.assertTrue(self.src.is_symlink())
        self.assertEqual((self.src / 'movie').read_bytes(), b'video\x00payload')
        self.assertEqual((self.usb / 'Videos/relative').readlink(), Path('movie'))
        self.mod.relocate(self.src, self.usb, True)
        self.assertFalse((self.home / 'Videos.offload-original').exists())

    def test_existing_destination_refused_without_touching_source(self):
        (self.usb / 'Videos').mkdir()
        with self.assertRaises(RuntimeError):
            self.mod.relocate(self.src, self.usb, True)
        self.assertEqual((self.src / 'movie').read_bytes(), b'video\x00payload')

    def test_verification_failure_retains_source(self):
        real = self.mod.run
        def corrupt_after_copy(args, label):
            output = real(args, label)
            if label.startswith('Copy'):
                (self.usb / 'Videos/movie').write_bytes(b'corrupt')
            return output
        with patch.object(self.mod, 'run', side_effect=corrupt_after_copy):
            with self.assertRaises(RuntimeError):
                self.mod.relocate(self.src, self.usb, True)
        self.assertFalse(self.src.is_symlink())
        self.assertEqual((self.src / 'movie').read_bytes(), b'video\x00payload')

    def test_usb_identity_change_retains_original(self):
        with patch.object(self.mod, 'identity', side_effect=[(1, 1), (1, 2)]):
            with self.assertRaises(RuntimeError):
                self.mod.relocate(self.src, self.usb, True)
        self.assertFalse(self.src.is_symlink())
        self.assertEqual((self.src / 'movie').read_bytes(), b'video\x00payload')

    def test_link_failure_restores_original(self):
        with patch.object(Path, 'symlink_to', side_effect=OSError('injected link failure')):
            with self.assertRaises(OSError):
                self.mod.relocate(self.src, self.usb, True)
        self.assertFalse(self.src.is_symlink())
        self.assertEqual((self.src / 'movie').read_bytes(), b'video\x00payload')

    def test_unmounted_destination_refused(self):
        with self.assertRaises(RuntimeError):
            self.mod.preflight(self.home, self.usb)

    def test_wrong_symlink_refused(self):
        self.src.rename(self.home / 'other')
        self.src.symlink_to(self.home / 'other')
        with self.assertRaises(RuntimeError):
            self.mod.relocate(self.src, self.usb, True)


if __name__ == '__main__':
    unittest.main()
