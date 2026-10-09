"""Exercise fish presentation without networking or modifying live configuration."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS = ROOT / 'dot_config/fish/functions'


class FishEmojiOutputTest(unittest.TestCase):
    def run_fish(self, body, plain=False):
        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ, HOME=home, XDG_CONFIG_HOME=home)
            env.pop('CLI_PLAIN', None)
            if plain:
                env['CLI_PLAIN'] = '1'
            return subprocess.run(
                ['fish', '--no-config', '-c', f"set -p fish_function_path '{FUNCTIONS}'; {body}"],
                env=env, text=True, capture_output=True, check=False,
            )

    def test_phone_backup_failure_decorates_stderr_and_preserves_exit(self):
        body = 'function ssh; return 1; end; backup-phone-storage'
        pretty = self.run_fish(body)
        plain = self.run_fish(body, plain=True)
        self.assertEqual(pretty.returncode, 1)
        self.assertEqual(plain.returncode, 1)
        self.assertEqual(pretty.stdout, '')
        self.assertIn('❌ backup-phone-storage:', pretty.stderr)
        self.assertIn('💡 backup-phone-storage:', pretty.stderr)
        self.assertTrue(plain.stderr.isascii())
        self.assertIn('pkg install rsync', plain.stderr)

    def test_phone_backup_progress_keeps_downstream_data_clean(self):
        body = 'function ssh; return 0; end; function rsync; echo rsync-data; end; backup-phone-storage'
        pretty = self.run_fish(body)
        plain = self.run_fish(body, plain=True)
        self.assertEqual(pretty.returncode, 0)
        self.assertTrue(pretty.stdout.startswith('📱 backup-phone-storage:'))
        self.assertTrue(pretty.stdout.endswith('rsync-data\n'))
        self.assertTrue(plain.stdout.isascii())

    def test_network_dependency_error_preserves_status(self):
        body = 'set PATH /nonexistent; restart_ethernet'
        pretty = self.run_fish(body)
        plain = self.run_fish(body, plain=True)
        self.assertEqual(pretty.returncode, 127)
        self.assertTrue(pretty.stderr.startswith('❌ restart_ethernet:'))
        self.assertEqual(plain.returncode, 127)
        self.assertTrue(plain.stderr.isascii())

    def test_season_plain_flag_preserves_level_position(self):
        # Use the real date parser but fix "now" to a day within the season.
        body = '''function date
            if test "$argv[1]" = +%s
                command date -d '2026-10-09 12:00:00' +%s
            else
                command date $argv
            end
        end
        fn-progress --plain 100'''
        result = self.run_fish(body)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.isascii(), result.stdout)
        self.assertIn('Level 100 is ', result.stdout)
        self.assertIn('Fortnite C7S4 is ', result.stdout)
        self.assertEqual(result.stderr, '')

    def test_season_plain_environment_covers_ended_branch(self):
        body = '''function date
            if test "$argv[1]" = +%s
                command date -d '2026-12-01' +%s
            else
                command date $argv
            end
        end
        fn-progress'''
        pretty = self.run_fish(body)
        plain = self.run_fish(body, plain=True)
        self.assertEqual(pretty.returncode, 0)
        self.assertTrue(pretty.stdout.startswith('🎉 '))
        self.assertTrue(plain.stdout.isascii(), plain.stdout)
        self.assertIn('has ended!', plain.stdout)

    def test_server_status_has_emoji_and_ascii_fallback(self):
        body = '''function wget; echo '<title>unavailable</title>'; end
        function recode; cat; end
        server-pages'''
        pretty = self.run_fish(body)
        plain = self.run_fish(body, plain=True)
        self.assertEqual(pretty.returncode, 0, pretty.stderr)
        self.assertEqual(len(pretty.stdout.splitlines()), 7)
        self.assertTrue(all(line.startswith('❌ [FAIL] ') for line in pretty.stdout.splitlines()))
        self.assertTrue(plain.stdout.isascii(), plain.stdout)
        self.assertTrue(plain.stdout.startswith('[FAIL] example-user-mok.com'))

    def test_git_history_decorates_commits_and_preserves_plain_format(self):
        with tempfile.TemporaryDirectory() as repo:
            subprocess.run(['git', 'init', '-q', repo], check=True)
            subprocess.run(['git', '-C', repo, '-c', 'user.name=Fixture', '-c',
                            'user.email=fixture@example.invalid', 'commit', '-q',
                            '--allow-empty', '-m', 'Example message'], check=True)
            body = f"builtin cd '{repo}'; git-log-short --no-color -1"
            pretty = self.run_fish(body)
            plain = self.run_fish(body, plain=True)
        self.assertEqual(pretty.returncode, 0, pretty.stderr)
        self.assertTrue(pretty.stdout.startswith('📝 '), pretty.stdout)
        self.assertIn('Example message', pretty.stdout)
        self.assertTrue(plain.stdout.isascii(), plain.stdout)
        self.assertIn('Example message', plain.stdout)
        self.assertEqual(len(pretty.stdout.splitlines()), 1)

    def test_legacy_refresh_task_messages_are_decorated_without_live_changes(self):
        body = """mkdir -p $HOME/.codex $HOME/.config/fish
        echo 'model = "fixture"' >$HOME/.codex/config.toml
        echo '# fixture shortcuts' >$HOME/.config/fish/key_abbr.fish
        function chezmoi
            if test "$argv[1]" = source-path
                echo $HOME/copied-config.toml
            end
        end
        function sync-shortcuts; return 0; end
        refresh-config-task"""
        pretty = self.run_fish(body)
        plain = self.run_fish(body, plain=True)
        self.assertEqual(pretty.returncode, 0, pretty.stderr)
        self.assertEqual(len(pretty.stdout.splitlines()), 5)
        self.assertTrue(pretty.stdout.startswith('📋 Copied '), pretty.stdout)
        self.assertIn('✅ Applied chezmoi.', pretty.stdout)
        self.assertIn('🔄 Reloading fish.', pretty.stdout)
        self.assertTrue(plain.stdout.isascii(), plain.stdout)
        self.assertEqual(plain.returncode, 0, plain.stderr)

    def test_cd_invalid_arguments_keeps_message_and_exit_status(self):
        template = (FUNCTIONS / 'cd.fish.tmpl').read_text()
        # Both template branches parse when template directives are omitted;
        # this invalid-argument path returns before directory changes.
        source = '\n'.join(line for line in template.splitlines() if '{{' not in line)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'cd.fish'
            path.write_text(source)
            body = f"source '{path}'; cd one two"
            pretty = self.run_fish(body)
            plain = self.run_fish(body, plain=True)
        self.assertEqual(pretty.returncode, 1)
        self.assertTrue(pretty.stdout.startswith('❌ '), pretty.stdout)
        self.assertIn('Too many args', pretty.stdout)
        self.assertTrue(plain.stdout.isascii())


if __name__ == '__main__':
    unittest.main()
