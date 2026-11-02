"""Exercise reserved directory abbreviations through interactive Fish; never execute them."""
import os
import pty
import signal
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

REPO = Path(__file__).resolve().parents[1]

class ReservedShortcutTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def generate(self):
        home = self.root / 'home'
        for sub in ('aliases', '.config/fish', '.config/ranger'):
            (home / sub).mkdir(parents=True, exist_ok=True)
        for name in ('key_dirs', 'key_files', 'key_aliases'):
            (home / 'aliases' / name).write_text(
                'or /mnt/usb-8tb/concerts/olivia-rodrigo\n' if name == 'key_dirs' else '')
        subprocess.run(['bash', str(REPO / 'scripts/executable_sync-shortcuts')],
            env={**os.environ, 'HOME': str(home)}, check=True, capture_output=True)
        subprocess.run(['fish', '-n', str(home / '.config/fish/key_abbr.fish')], check=True)

    def test_reserved_or_expands_only_on_fresh_command_line(self):
        self.generate()
        home = self.root / 'home'
        capture = self.root / 'capture'
        ready = self.root / 'ready'
        pid, master = pty.fork()
        if pid == 0:
            os.execvpe('fish', ['fish', '--no-config', '--interactive'],
                {**os.environ, 'HOME': str(home), 'TERM': 'xterm'})
        def wait_for(path):
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if path.exists(): return path.read_text()
                time.sleep(.02)
            self.fail('interactive Fish did not capture command line')
        try:
            setup = (f"source {home}/.config/fish/key_abbr.fish; "
                     f"bind \\cg 'commandline > {capture}; commandline \"\"'; "
                     f"touch {ready}\n")
            os.write(master, setup.encode())
            wait_for(ready)
            for typed, expected in [
                ('or ', 'cd /mnt/usb-8tb/concerts/olivia-rodrigo '),
                ('false; or ', 'false; or '),
                ('echo or ', 'echo or '),
            ]:
                capture.unlink(missing_ok=True)
                os.write(master, typed.encode() + b'\x07')
                self.assertEqual(wait_for(capture).rstrip('\n'), expected)
        finally:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
            os.close(master)

if __name__ == '__main__': unittest.main()
