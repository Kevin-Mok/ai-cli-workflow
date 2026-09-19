"""Verify actual chezmoi naming and executable deployment in an isolated home."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('chezmoi'), 'requires chezmoi')
class DownloaderInstallTest(unittest.TestCase):
    def test_installed_command_is_executable_and_current(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            destination = root / 'home'
            (source / 'scripts').mkdir(parents=True)
            destination.mkdir()
            config = root / 'config.toml'
            config.write_text('')
            candidates = list((ROOT / 'scripts').glob('*yt-dl'))
            self.assertEqual(len(candidates), 1)
            original = candidates[0]
            shutil.copy2(original, source / 'scripts' / original.name)
            result = subprocess.run([
                'chezmoi', '--config', str(config), '--source', str(source),
                '--destination', str(destination), '--persistent-state',
                str(root / 'state.boltdb'), 'apply', '--force',
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            target = destination / 'scripts' / 'yt-dl'
            self.assertTrue(target.is_file(), 'chezmoi did not install scripts/yt-dl')
            self.assertTrue(os.access(target, os.X_OK), 'installed command is not executable')
            self.assertEqual(target.read_bytes(), original.read_bytes())
            help_result = subprocess.run([str(target), '--help'], capture_output=True, text=True)
            self.assertEqual(help_result.returncode, 0, help_result.stderr)
            self.assertIn('--output-dir', help_result.stdout)
