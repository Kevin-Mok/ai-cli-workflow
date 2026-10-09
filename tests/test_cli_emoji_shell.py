"""Run real, non-mutating shell entry points to verify decoration modes."""
import os
from pathlib import Path
import subprocess
import unittest
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HELP_SCRIPTS = (
    'setup-neovim-python-completion.sh', 'fix-aux-speaker-audio',
    'setup-mosh.sh', 'Voice Contributor-intro', 'sync-design-skills', 'codex',
    'backup-ubuntu-h7', 'fix-codex-fnm.sh', 'harden-phone-ssh.sh',
    'update-chrome.sh', 'setup-second-brain-state', 'fix-vps-codex.sh',
    'setup-aerc-mail.sh', 'install-tmux-tpm.sh', 'setup-phone-ssh.sh',
    'doctor-phone-ssh.sh', 'unmount-pixel-9', 'setup-termux-mosh.sh',
    'update-vesktop.sh', 'sync-superpowers-release', 'mount-pixel-9',
    'setup-st.sh',
)

class ShellEmojiTests(unittest.TestCase):
    def test_help_is_decorated_and_plain_escape_preserves_text(self):
        # Removing decoration or leaking it into CLI_PLAIN breaks this contract.
        for script in HELP_SCRIPTS:
            with self.subTest(script=script):
                args = ['bash', str(ROOT / 'scripts' / ('executable_' + script)), '--help']
                env = dict(os.environ, CLI_PLAIN='0')
                normal = subprocess.run(args, env=env, capture_output=True, text=True, timeout=10)
                plain = subprocess.run(args, env=dict(env, CLI_PLAIN='1'), capture_output=True, text=True, timeout=10)
                self.assertEqual(normal.returncode, 0, normal.stderr)
                self.assertEqual(plain.returncode, 0, plain.stderr)
                self.assertIn('📖', normal.stdout)
                self.assertNotIn('📖', plain.stdout)
                self.assertEqual(normal.stdout.replace('📖 ', '', 1), plain.stdout)

    def test_additional_shell_and_embedded_help(self):
        for name in ('hdd-init-wizard.sh', 'executable_backup-pc'):
            with self.subTest(script=name):
                args = ['bash', str(ROOT / 'scripts' / name), '--help']
                normal = subprocess.run(args, env=dict(os.environ, CLI_PLAIN='0'), capture_output=True, text=True, timeout=10)
                plain = subprocess.run(args, env=dict(os.environ, CLI_PLAIN='1'), capture_output=True, text=True, timeout=10)
                self.assertEqual(normal.returncode, 0, normal.stderr)
                self.assertIn('📖', normal.stdout)
                self.assertEqual(normal.stdout.replace('📖 ', '', 1), plain.stdout)

    def test_backup_excludes_remain_machine_readable(self):
        args = ['bash', str(ROOT / 'scripts/executable_backup-pc'), 'excludes']
        normal = subprocess.run(args, env=dict(os.environ, CLI_PLAIN='0'), capture_output=True, text=True, timeout=10)
        plain = subprocess.run(args, env=dict(os.environ, CLI_PLAIN='1'), capture_output=True, text=True, timeout=10)
        self.assertEqual(normal.returncode, 0, normal.stderr)
        self.assertEqual(normal.stdout, plain.stdout)
        self.assertIn('/proc/*', normal.stdout)

    def test_generated_termux_helpers_keep_runtime_plain_escape(self):
        # Generated scripts must honor the mode when run, not just when installed.
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            (base / 'bin').mkdir()
            (base / 'home').mkdir()
            pkg = base / 'bin/pkg'
            pkg.write_text('#!/bin/sh\nexit 0\n')
            pkg.chmod(0o755)
            env = dict(os.environ, HOME=str(base / 'home'), PATH=str(base / 'bin') + ':' + os.environ['PATH'], CLI_PLAIN='1')
            setup = subprocess.run(['bash', str(ROOT / 'scripts/executable_setup-termux-mosh.sh'), '--host', 'example.net', '--user', 'fixture', '--ssh-port', '2222', '--bin-dir', str(base / 'helpers')], env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(setup.returncode, 0, setup.stderr)
            for helper in ('pc-push', 'pc-pull', 'pc-sync-to-pc', 'pc-sync-from-pc'):
                with self.subTest(helper=helper):
                    args = ['bash', str(base / 'helpers' / helper)]
                    normal = subprocess.run(args, env=dict(env, CLI_PLAIN='0'), capture_output=True, text=True, timeout=10)
                    plain = subprocess.run(args, env=env, capture_output=True, text=True, timeout=10)
                    self.assertEqual(normal.returncode, 1)
                    self.assertIn('📖', normal.stderr)
                    self.assertEqual(normal.stderr.replace('📖 ', '', 1), plain.stderr)

    def test_usage_error_is_decorated_without_changing_exit_code(self):
        for script in ('apply-pywal-theme', 'rsync-media-date'):
            with self.subTest(script=script):
                args = ['bash', str(ROOT / 'scripts' / ('executable_' + script))]
                normal = subprocess.run(args, env=dict(os.environ, CLI_PLAIN='0'), capture_output=True, text=True, timeout=10)
                plain = subprocess.run(args, env=dict(os.environ, CLI_PLAIN='1'), capture_output=True, text=True, timeout=10)
                self.assertNotEqual(normal.returncode, 0)
                self.assertEqual(normal.returncode, plain.returncode)
                self.assertIn('📖', normal.stderr)
                self.assertEqual(normal.stderr.replace('📖 ', '', 1), plain.stderr)

if __name__ == '__main__':
    unittest.main()
