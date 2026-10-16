"""Synthetic repository integration tests; never touch the user's checkout or HOME."""
import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/executable_migrate-ai-cli-workflow'


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='migration-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / 'home'
        self.home.mkdir()
        self.repo = self.home / 'linux-config'
        self.remote = self.root / 'remote'
        self.state = self.root / 'private-state'
        self.review = self.root / 'review.json'
        self.env = dict(os.environ, HOME=str(self.home), GIT_CONFIG_NOSYSTEM='1',
                        GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                        GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        for directory in (self.repo, self.remote):
            self.git('init', '-b', 'main', str(directory), cwd=self.root)
            (directory / 'file.txt').write_text('original\n')
            (directory / '.chezmoiignore').write_text('scripts\n')
            (directory / 'dot_gitconfig.tmpl').write_text('[user]\nname = {{ .name }}\n')
            (directory / 'dot_codex').mkdir()
            (directory / 'dot_codex/config.toml').write_text('model = "fixture"\n')
            (directory / 'dot_config/chezmoi').mkdir(parents=True)
            (directory / 'dot_config/chezmoi/chezmoi-template.toml.tmpl').write_text('[data]\n')
            (directory / 'scripts').mkdir()
            auditor = directory / 'scripts/executable_audit-public-history'
            auditor.write_text('#!/bin/sh\nexit 0\n')
            auditor.chmod(0o755)
            self.git('add', '.', cwd=directory)
            self.git('commit', '-qm', 'fixture: initial', cwd=directory)
        (self.repo / 'old-only.txt').write_text('old history marker\n')
        self.git('add', 'old-only.txt')
        self.git('commit', '-qm', 'fixture: private history marker')
        self.git('remote', 'add', 'origin', 'https://example.invalid/old-private.git')
        self.old_head = self.git('rev-parse', 'HEAD')
        self.review.write_text('{"files": {}}')

    def git(self, *args, cwd=None):
        result = subprocess.run(['git', *args], cwd=cwd or self.repo, env=self.env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def invoke(self, *args, ok=True, url=None, config=False):
        result = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(self.repo),
                                 '--home', str(self.home), '--url', url or self.remote.as_uri(),
                                 '--state-dir', str(self.state), '--review', str(self.review),
                                 '--allow-local-fixture', *([] if config else ['--skip-config']), '--plain', *args],
                                env=self.env, text=True, capture_output=True)
        self.assertNotIn("can't open file", result.stderr)
        self.assertNotIn('Traceback (most recent call last)', result.stderr)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def approve(self, path):
        source = self.repo / path
        destination = self.remote / path
        self.review.write_text(json.dumps({'files': {path: {
            'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'base_sha256': hashlib.sha256(destination.read_bytes()).hexdigest() if destination.exists() else None,
        }}}))

    def configure_live_fixture(self):
        if not shutil.which('chezmoi'):
            self.skipTest('chezmoi required for configuration integration')
        local = self.home / '.config/chezmoi/chezmoi.toml'
        local.parent.mkdir(parents=True)
        local.write_text('sourceDir = ' + json.dumps(str(self.repo)) + '\n[data]\nname = "Fixture"\n')
        smtp = self.home / '.config/msmtp/config'
        smtp.parent.mkdir(parents=True)
        smtp.write_text('host smtp.fixture.invalid\nport 587\ntls_starttls on\nfrom user' + '@' + 'fixture.invalid\n')
        mutt = self.home / '.config/neomutt/neomuttrc'
        mutt.parent.mkdir(parents=True)
        mutt.write_text('set realname = "Fixture User"\n')
        calendar = self.home / '.calcurse/caldav/config'
        calendar.parent.mkdir(parents=True)
        calendar.write_text('[General]\nHostname = calendar.fixture.invalid\nPath = /calendar/fixture\n[Auth]\nUsername = fixture-user\n')
        (self.home / '.codex').mkdir()
        (self.home / '.codex/config.toml').write_text('model = "working-private-model"\n')
        (self.home / '.gitconfig').write_text('[user]\nname = Working Identity\n')
        auditor = self.remote / 'scripts/executable_audit-public-history'
        auditor.write_text('#!/usr/bin/env python3\nraise SystemExit(0)\n')
        self.git('add', '.', cwd=self.remote)
        self.git('commit', '-qm', 'fixture: python auditor', cwd=self.remote)
        return local

    def test_config_apply_preserves_private_settings_and_rollback(self):
        local = self.configure_live_fixture()
        (self.home / 'file.txt').write_text('working previous file\n')
        original_local = local.read_bytes()
        original_codex = (self.home / '.codex/config.toml').read_bytes()
        original_git = (self.home / '.gitconfig').read_bytes()
        self.invoke('--apply', config=True)
        self.assertEqual((self.home / 'file.txt').read_text(), 'original\n')
        self.assertEqual((self.home / '.codex/config.toml').read_bytes(), original_codex)
        self.assertEqual((self.home / '.gitconfig').read_bytes(), original_git)
        self.assertIn('mailAddress', local.read_text())
        self.assertIn('calendarUsername', local.read_text())
        self.invoke('--verify', config=True)
        self.invoke('--rollback', config=True)
        self.assertEqual(local.read_bytes(), original_local)
        self.assertEqual((self.home / 'file.txt').read_text(), 'working previous file\n')

    def test_missing_local_identity_data_stops_before_cutover(self):
        self.configure_live_fixture()
        (self.home / '.config/msmtp/config').unlink()
        self.invoke('--apply', config=True, ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)

    def test_config_apply_preserves_working_claude_integrations(self):
        self.configure_live_fixture()
        names = ['.claude.json', '.claude/settings.json', '.claude/context-mode.mcp.json',
                 '.claude/code-review-graph.mcp.json', '.claude/token-savior.mcp.json']
        originals = {}
        for name in names:
            target = self.home / name
            target.parent.mkdir(parents=True, exist_ok=True)
            originals[name] = b'{"localIntegration": "keep-working"}\n'
            target.write_bytes(originals[name])
            source = self.remote / ('dot_' + name[1:])
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text('{"neutralIntegration": true}\n')
        self.git('add', '.', cwd=self.remote)
        self.git('commit', '-qm', 'fixture: neutral Claude integrations', cwd=self.remote)
        self.invoke('--apply', config=True)
        for name, content in originals.items():
            self.assertEqual((self.home / name).read_bytes(), content, name)
        self.invoke('--verify', config=True)
        self.invoke('--rollback', config=True)
        for name, content in originals.items():
            self.assertEqual((self.home / name).read_bytes(), content, name)

    def test_neutral_project_contract_does_not_replace_working_local_contract(self):
        self.configure_live_fixture()
        target = self.home / '.project-contract'
        target.write_text('PROJECT = "working-local-project"\n')
        source = self.remote / 'dot_project-contract'
        source.write_text('PROJECT = "ExampleProject"\n')
        self.git('add', '.', cwd=self.remote)
        self.git('commit', '-qm', 'fixture: neutral project contract', cwd=self.remote)
        self.invoke('--apply', config=True)
        self.assertEqual(target.read_text(), 'PROJECT = "working-local-project"\n')

    def test_binary_render_verifies_raw_bytes_and_rollback_restores_original(self):
        self.configure_live_fixture()
        intended = b'\x89PNG\r\n\x1a\n\x00\xff\x80binary-fixture'
        original = b'\x89previous-binary\x00\xfe'
        target = self.home / '.binary-fixture.png'
        target.write_bytes(original)
        (self.remote / 'dot_binary-fixture.png').write_bytes(intended)
        self.git('add', '.', cwd=self.remote)
        self.git('commit', '-qm', 'fixture: binary rendered file', cwd=self.remote)
        self.invoke('--apply', config=True)
        self.assertEqual(target.read_bytes(), intended)
        journal = json.loads((self.state / 'state.json').read_text())
        self.assertEqual(journal['private_config_hash'], hashlib.sha256((self.state / 'chezmoi.toml').read_bytes()).hexdigest())
        self.invoke('--verify', config=True)
        self.invoke('--rollback', config=True)
        self.assertEqual(target.read_bytes(), original)

    def test_chezmoi_scripts_externals_and_removals_are_excluded(self):
        self.configure_live_fixture()
        sentinel = self.home / 'keep-this'
        sentinel.write_text('keep me\n')
        (self.remote / 'run_before_fixture.sh').write_text('#!/bin/sh\ntouch "$HOME/hook-ran"\n')
        (self.remote / '.chezmoiremove').write_text('keep-this\n')
        (self.remote / '.chezmoiexternal.toml').write_text('["external-download"]\ntype = "file"\nurl = "https://invalid.invalid/never-download"\n')
        self.git('add', '.', cwd=self.remote)
        self.git('commit', '-qm', 'fixture: excluded side effects', cwd=self.remote)
        self.invoke('--apply', config=True)
        self.assertFalse((self.home / 'hook-ran').exists())
        self.assertFalse((self.home / 'external-download').exists())
        self.assertEqual(sentinel.read_text(), 'keep me\n')

    def test_external_template_does_not_evaluate_network_functions(self):
        self.configure_live_fixture()
        (self.remote / '.chezmoiexternal.toml.tmpl').write_text('{{ fail "external template must remain unevaluated" }}\n')
        self.git('add', '.', cwd=self.remote)
        self.git('commit', '-qm', 'fixture: offline external template', cwd=self.remote)
        self.invoke('--apply', config=True)
        self.assertTrue((self.state / 'archive/.git').exists())
        self.invoke('--verify', config=True)

    def test_template_render_failure_keeps_original_checkout_and_live_files(self):
        local = self.configure_live_fixture()
        original_local = local.read_bytes()
        (self.remote / 'dot_broken.tmpl').write_text('{{ .missingRequiredFixtureKey }}\n')
        self.git('add', '.', cwd=self.remote)
        self.git('commit', '-qm', 'fixture: render failure', cwd=self.remote)
        self.invoke('--apply', config=True, ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)
        self.assertEqual(local.read_bytes(), original_local)
        self.assertFalse((self.home / '.broken').exists())

    def install_wrapper(self, command, body):
        real = shutil.which(command)
        directory = self.root / 'test-bin'
        directory.mkdir(exist_ok=True)
        wrapper = directory / command
        wrapper.write_text('#!' + sys.executable + '\nimport os, pathlib, signal, subprocess, sys\n' +
                           'REAL = ' + repr(real) + '\n' + body + '\nos.execv(REAL, [REAL, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        self.env['PATH'] = str(directory) + os.pathsep + self.env['PATH']

    def test_partial_live_apply_failure_automatically_restores_files(self):
        local = self.configure_live_fixture()
        original_local = local.read_bytes()
        (self.home / 'file.txt').write_text('before partial apply\n')
        token = 'gh' + 'p_' + 'B' * 36
        self.install_wrapper('chezmoi',
            'if "--force" in sys.argv and "apply" in sys.argv:\n'
            '    subprocess.run([REAL, *sys.argv[1:]], check=True)\n'
            '    sys.stderr.write(' + repr(token) + ')\n'
            '    sys.exit(7)')
        output = self.invoke('--apply', config=True, ok=False)
        self.assertNotIn(token, output)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)
        self.assertEqual(local.read_bytes(), original_local)
        self.assertEqual((self.home / 'file.txt').read_text(), 'before partial apply\n')
        self.assertEqual(json.loads((self.state / 'state.json').read_text())['phase'], 'rolled_back')

    def test_interrupted_cutover_recovers_from_journal(self):
        nested = self.repo / '.worktrees/feature'
        self.git('worktree', 'add', '-b', 'nested', str(nested))
        (nested / 'file.txt').write_text('keep interrupted worktree edit\n')
        marker = self.root / 'interrupted-once'
        self.install_wrapper('git',
            'if "repair" in sys.argv and not pathlib.Path(' + repr(str(marker)) + ').exists():\n'
            '    pathlib.Path(' + repr(str(marker)) + ').touch()\n'
            '    os.kill(os.getppid(), signal.SIGKILL)\n'
            '    sys.exit(0)')
        self.invoke('--apply', ok=False)
        self.assertTrue((self.state / 'archive/.git').exists())
        self.invoke('--rollback')
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)
        self.assertEqual((nested / 'file.txt').read_text(), 'keep interrupted worktree edit\n')
        common = self.git('rev-parse', '--path-format=absolute', '--git-common-dir', cwd=nested)
        self.assertEqual(Path(common).resolve(), (self.repo / '.git').resolve())

    def test_index_stat_refresh_does_not_refuse_unchanged_checkout(self):
        source = self.repo / 'file.txt'
        info = source.stat()
        os.utime(source, ns=(info.st_atime_ns, info.st_mtime_ns + 5_000_000_000))
        index_before = (self.repo / '.git/index').read_bytes()
        self.install_wrapper('git',
            'if "clone" in sys.argv:\n'
            '    subprocess.run([REAL, "-C", ' + repr(str(self.repo)) + ', "update-index", "--refresh"], check=True, stdout=subprocess.DEVNULL)')
        self.invoke('--apply')
        archive = self.state / 'archive'
        self.assertEqual((archive / 'file.txt').read_text(), 'original\n')
        self.assertNotEqual((archive / '.git/index').read_bytes(), index_before)

    def test_concurrent_staging_only_change_is_recorded_and_refused(self):
        source = self.repo / 'file.txt'
        source.write_text('already dirty working bytes\n')
        self.install_wrapper('git',
            'if "clone" in sys.argv:\n'
            '    subprocess.run([REAL, "-C", ' + repr(str(self.repo)) + ', "add", "file.txt"], check=True)')
        output = self.invoke('--apply', '--details', ok=False)
        self.assertIn('index entries changed', output)
        state = json.loads((self.state / 'state.json').read_text())
        self.assertIn('initial_checkout', state)
        self.assertEqual(state['checkout_changes']['files'], [])
        self.assertTrue(state['checkout_changes']['index'])
        self.assertEqual(source.read_text(), 'already dirty working bytes\n')

    def test_concurrent_assume_unchanged_flag_change_refuses_cutover(self):
        self.install_wrapper('git',
            'if "clone" in sys.argv:\n'
            '    subprocess.run([REAL, "-C", ' + repr(str(self.repo)) + ', "update-index", "--assume-unchanged", "file.txt"], check=True)')
        output = self.invoke('--apply', '--details', ok=False)
        self.assertIn('index entries changed', output)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)

    def test_concurrent_intent_to_add_becoming_staged_refuses_cutover(self):
        (self.repo / 'empty-addition.txt').write_text('')
        self.git('add', '--intent-to-add', 'empty-addition.txt')
        self.install_wrapper('git',
            'if "clone" in sys.argv:\n'
            '    subprocess.run([REAL, "-C", ' + repr(str(self.repo)) + ', "add", "empty-addition.txt"], check=True)')
        output = self.invoke('--apply', '--details', ok=False)
        self.assertIn('index entries changed', output)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)

    def test_concurrent_resolve_undo_change_refuses_cutover(self):
        self.git('checkout', '-b', 'conflict-side')
        (self.repo / 'file.txt').write_text('side version\n')
        self.git('add', 'file.txt')
        self.git('commit', '-qm', 'fixture: side')
        self.git('checkout', 'main')
        (self.repo / 'file.txt').write_text('main version\n')
        self.git('add', 'file.txt')
        self.git('commit', '-qm', 'fixture: main')
        conflict = subprocess.run(['git', 'merge', 'conflict-side'], cwd=self.repo,
                                  env=self.env, capture_output=True)
        self.assertEqual(conflict.returncode, 1)
        (self.repo / 'file.txt').write_text('resolved version\n')
        self.git('add', 'file.txt')
        head = self.git('rev-parse', 'HEAD')
        self.install_wrapper('git',
            'if "clone" in sys.argv:\n'
            '    subprocess.run([REAL, "-C", ' + repr(str(self.repo)) + ', "update-index", "--clear-resolve-undo"], check=True)')
        output = self.invoke('--apply', '--details', ok=False)
        self.assertIn('index entries changed', output)
        self.assertEqual(self.git('rev-parse', 'HEAD'), head)

    def test_dry_run_refuses_material_change_without_creating_journal(self):
        source = self.repo / 'file.txt'
        self.install_wrapper('git',
            'if "worktree" in sys.argv and "list" in sys.argv:\n'
            '    pathlib.Path(' + repr(str(source)) + ').write_text("external editor change\\n")')
        output = self.invoke('--dry-run', '--details', ok=False)
        self.assertIn('files changed: 1', output)
        self.assertFalse(self.state.exists())
        self.assertEqual(source.read_text(), 'external editor change\n')

    def test_concurrent_dirty_source_change_refuses_cutover(self):
        source = self.repo / 'file.txt'
        source.write_text('pending before clone\n')
        self.install_wrapper('git',
            'if "clone" in sys.argv:\n'
            '    subprocess.run([REAL, *sys.argv[1:]], check=True)\n'
            '    pathlib.Path(' + repr(str(source)) + ').write_text("concurrent source edit\\n")\n'
            '    sys.exit(0)')
        self.invoke('--apply', ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)
        self.assertEqual(source.read_text(), 'concurrent source edit\n')

    def test_concurrent_dirty_worktree_change_refuses_cutover(self):
        nested = self.repo / '.worktrees/feature'
        self.git('worktree', 'add', '-b', 'nested', str(nested))
        source = nested / 'file.txt'
        source.write_text('pending worktree before clone\n')
        self.install_wrapper('git',
            'if "clone" in sys.argv:\n'
            '    subprocess.run([REAL, *sys.argv[1:]], check=True)\n'
            '    pathlib.Path(' + repr(str(source)) + ').write_text("concurrent worktree edit\\n")\n'
            '    sys.exit(0)')
        self.invoke('--apply', ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)
        self.assertEqual(source.read_text(), 'concurrent worktree edit\n')

    def test_rollback_refuses_subsequent_live_setting_change(self):
        self.configure_live_fixture()
        self.invoke('--apply', config=True)
        (self.home / 'file.txt').write_text('later live user edit\n')
        self.invoke('--rollback', config=True, ok=False)
        self.assertEqual((self.home / 'file.txt').read_text(), 'later live user edit\n')
        self.assertTrue((self.state / 'archive/.git').exists())

    def test_interrupted_cutover_rollback_refuses_later_checkout_edit(self):
        external = self.root / 'external-worktree'
        self.git('worktree', 'add', '-b', 'external', str(external))
        marker = self.root / 'interrupted-once'
        self.install_wrapper('git',
            'if "repair" in sys.argv and not pathlib.Path(' + repr(str(marker)) + ').exists():\n'
            '    pathlib.Path(' + repr(str(marker)) + ').touch()\n'
            '    os.kill(os.getppid(), signal.SIGKILL)\n'
            '    sys.exit(0)')
        self.invoke('--apply', ok=False)
        (self.repo / 'file.txt').write_text('checkout edit after interruption\n')
        self.invoke('--rollback', ok=False)
        self.assertEqual((self.repo / 'file.txt').read_text(), 'checkout edit after interruption\n')
        self.assertTrue((self.state / 'archive/.git').exists())

    def test_interrupted_live_apply_rollback_refuses_later_live_edit(self):
        self.configure_live_fixture()
        (self.home / 'file.txt').write_text('before interrupted apply\n')
        self.install_wrapper('chezmoi',
            'if "--force" in sys.argv and "apply" in sys.argv:\n'
            '    os.kill(os.getppid(), signal.SIGKILL)\n'
            '    sys.exit(0)')
        self.invoke('--apply', config=True, ok=False)
        self.assertEqual(json.loads((self.state / 'state.json').read_text())['phase'], 'applying')
        (self.home / 'file.txt').write_text('live edit after interruption\n')
        self.invoke('--rollback', config=True, ok=False)
        self.assertEqual((self.home / 'file.txt').read_text(), 'live edit after interruption\n')
        self.assertTrue((self.state / 'archive/.git').exists())

    def test_interrupted_rollback_retries_worktree_pointer_repair(self):
        nested = self.repo / '.worktrees/feature'
        external = self.root / 'external-worktree'
        self.git('worktree', 'add', '-b', 'nested', str(nested))
        self.git('worktree', 'add', '-b', 'external', str(external))
        (nested / 'file.txt').write_text('dirty nested before rollback\n')
        self.invoke('--apply')
        marker = self.root / 'rollback-killed-once'
        self.install_wrapper('git',
            'if "repair" in sys.argv and not pathlib.Path(' + repr(str(marker)) + ').exists():\n'
            '    pathlib.Path(' + repr(str(marker)) + ').touch()\n'
            '    os.kill(os.getppid(), signal.SIGKILL)\n'
            '    sys.exit(0)')
        self.invoke('--rollback', ok=False)
        self.assertTrue((self.repo / '.git').exists())
        self.invoke('--rollback')
        self.assertEqual((nested / 'file.txt').read_text(), 'dirty nested before rollback\n')
        for worktree in (nested, external):
            common = self.git('rev-parse', '--path-format=absolute', '--git-common-dir', cwd=worktree)
            self.assertEqual(Path(common).resolve(), (self.repo / '.git').resolve())

    def test_successful_noop_apply_is_rejected_and_rolled_back(self):
        local = self.configure_live_fixture()
        original_local = local.read_bytes()
        (self.home / 'file.txt').write_text('existing working file\n')
        self.install_wrapper('chezmoi',
            'if "--force" in sys.argv and "apply" in sys.argv:\n'
            '    sys.exit(0)')
        self.invoke('--apply', config=True, ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)
        self.assertEqual((self.home / 'file.txt').read_text(), 'existing working file\n')
        self.assertEqual(local.read_bytes(), original_local)

    def test_staged_only_changes_are_all_reported_quarantined(self):
        staged = self.repo / 'staged-only-added.txt'
        staged.write_text('staged addition\n')
        (self.repo / 'file.txt').write_text('staged modification\n')
        self.git('add', 'staged-only-added.txt', 'file.txt')
        staged.unlink()
        (self.repo / 'file.txt').write_text('original\n')
        self.git('rm', 'old-only.txt')
        self.invoke('--apply')
        state = json.loads((self.state / 'state.json').read_text())
        self.assertTrue({'staged-only-added.txt', 'file.txt', 'old-only.txt'}.issubset(state['quarantined']))
        self.assertIn('staged-only-added.txt', self.git('ls-files', cwd=self.state / 'archive').splitlines())

    def test_dry_inventory_does_not_run_status_filters_or_mutate_git(self):
        marker = self.root / 'unexpected-git-hook'
        hook = self.root / 'fsmonitor-hook'
        hook.write_text('#!/bin/sh\ntouch ' + str(marker) + '\nprintf "fixture\\0"\n')
        hook.chmod(0o755)
        self.git('config', 'core.fsmonitor', str(hook))
        self.git('config', 'filter.fixture.clean', 'touch ' + str(marker) + '; cat')
        (self.repo / '.gitattributes').write_text('file.txt filter=fixture\n')
        (self.repo / 'file.txt').write_text('dirty content to trigger clean filter\n')
        gitdir = self.repo / '.git'
        before = {str(path.relative_to(gitdir)): (path.read_bytes(), path.stat().st_mode)
                  for path in gitdir.rglob('*') if path.is_file()}
        self.invoke('--dry-run')
        after = {str(path.relative_to(gitdir)): (path.read_bytes(), path.stat().st_mode)
                 for path in gitdir.rglob('*') if path.is_file()}
        self.assertFalse(marker.exists(), 'read-only inventory ran fsmonitor or content filter')
        self.assertEqual(after, before)
        self.assertFalse(self.state.exists())

    def test_rollback_refuses_postcutover_ignored_user_file(self):
        (self.remote / '.gitignore').write_text('ignored-user-file\n')
        self.git('add', '.', cwd=self.remote)
        self.git('commit', '-qm', 'fixture: ignored user file', cwd=self.remote)
        self.invoke('--apply')
        ignored = self.repo / 'ignored-user-file'
        ignored.write_text('later ignored user work\n')
        self.invoke('--rollback', ok=False)
        self.assertEqual(ignored.read_text(), 'later ignored user work\n')
        self.assertTrue((self.state / 'archive/.git').exists())

    def test_real_shortcut_rehearsal_matches_generated_outputs_and_backs_up_live(self):
        self.check_shortcut_rehearsal(already_sourced=False)

    def test_shortcut_rehearsal_preserves_existing_home_source_without_duplicates(self):
        self.check_shortcut_rehearsal(already_sourced=True)

    def check_shortcut_rehearsal(self, already_sourced):
        helper = self.remote / 'scripts/executable_sync-shortcuts'
        shutil.copy2(SCRIPT.parent / 'executable_sync-shortcuts', helper)
        self.state.mkdir(mode=0o700)
        rendered = {
            'aliases/key_dirs': {'type': 'file', 'contents': 'go /tmp/fixture-directory\n', 'perm': 0o644},
            'aliases/key_files': {'type': 'file', 'contents': 'cfg /tmp/fixture-file\n', 'perm': 0o644},
            'aliases/key_aliases': {'type': 'file', 'contents': 'hello "echo fixture"\n', 'perm': 0o644},
        }
        bashrc = self.home / '.bashrc'
        source_line = 'source ' + str(self.home / 'aliases/.key_aliases')
        bashrc.write_text('# existing working shell configuration\n' + (source_line + '\n' if already_sourced else ''))
        for name, entry in rendered.items():
            path = self.home / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(entry['contents'])
        loader = importlib.machinery.SourceFileLoader('migration_refresh_test', str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        migration = importlib.util.module_from_spec(spec)
        loader.exec_module(migration)
        args = argparse.Namespace(home=self.home, state_dir=self.state, allow_local_fixture=False, plain=True)
        state = {'backups': {}, 'intended_live': {}}
        before = bashrc.read_bytes()
        migration.prepare_refresh(self.remote, args, state, rendered)
        self.assertEqual(bashrc.read_bytes(), before, 'rehearsal changed live shell configuration')
        self.assertTrue(state['refresh_reviewed'])
        self.assertEqual(len(state['intended_live']), 7)
        backup = state['backups'][str(bashrc)]
        self.assertEqual((self.state / backup['backup']).read_bytes(), before)
        # Chezmoi creates these target directories before the refresh helper runs.
        for name in state['intended_live']:
            Path(name).parent.mkdir(parents=True, exist_ok=True)
        # Exercise the real generator on the isolated HOME and compare its observable files.
        result = subprocess.run(['bash', str(helper)], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for name, intended in state['intended_live'].items():
            self.assertEqual(migration.snapshot(Path(name)), intended, name)
        self.assertIn('abbr go', (self.home / '.config/fish/key_abbr.fish').read_text())
        self.assertEqual(bashrc.read_text().splitlines().count(source_line), 1)

    def test_dry_run_does_not_write(self):
        (self.repo / 'file.txt').write_text('pending safe edit\n')
        before = self.git('status', '--porcelain')
        self.invoke('--dry-run')
        self.assertFalse(self.state.exists())
        self.assertEqual(self.git('status', '--porcelain'), before)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)

    def test_cutover_transfers_reviewed_edits_and_quarantines_others(self):
        (self.repo / 'file.txt').write_text('reviewed functionality\n')
        (self.repo / 'personal-note.txt').write_text('private unreviewed note\n')
        self.approve('file.txt')
        self.invoke('--apply')
        archive = self.state / 'archive'
        self.assertEqual((self.repo / 'file.txt').read_text(), 'reviewed functionality\n')
        self.assertFalse((self.repo / 'personal-note.txt').exists())
        self.assertEqual((archive / 'personal-note.txt').read_text(), 'private unreviewed note\n')
        self.assertEqual((archive / 'file.txt').read_text(), 'reviewed functionality\n')
        self.assertEqual(self.git('remote', 'get-url', 'origin'), self.remote.as_uri())
        self.assertEqual(self.git('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'), 'origin/main')
        self.assertFalse((self.repo / '.git/objects/info/alternates').exists())
        old_object = subprocess.run(['git', 'cat-file', '-e', self.old_head], cwd=self.repo,
                                    env=self.env, capture_output=True)
        self.assertNotEqual(old_object.returncode, 0, 'old history leaked into sanitized clone')
        self.assertEqual(self.state.stat().st_mode & 0o077, 0)
        self.assertEqual((self.state / 'state.json').stat().st_mode & 0o077, 0)
        self.invoke('--verify')
        self.invoke('--apply')
        self.invoke('--dry-run')

    def test_reviewed_untracked_safe_file_is_transferred(self):
        (self.repo / 'safe-helper.txt').write_text('safe useful addition\n')
        self.approve('safe-helper.txt')
        self.invoke('--apply')
        self.assertEqual((self.repo / 'safe-helper.txt').read_text(), 'safe useful addition\n')

    def test_verify_accepts_only_canonical_sanitized_remote_forms(self):
        self.invoke('--apply')
        journal = self.state / 'state.json'
        state = json.loads(journal.read_text())
        state['url'] = 'https://github.com/Kevin-Mok/ai-cli-workflow'
        journal.write_text(json.dumps(state))
        for origin in (
                'git' + '@' + 'github.com:Kevin-Mok/ai-cli-workflow.git',
                'ssh://git' + '@' + 'github.com/Kevin-Mok/ai-cli-workflow.git',
                'https://github.com/Kevin-Mok/ai-cli-workflow.git',
                'https://github.com/Kevin-Mok/ai-cli-workflow'):
            with self.subTest(origin=origin):
                self.git('remote', 'set-url', 'origin', origin)
                self.invoke('--verify')
        for origin in (
                'git' + '@' + 'github.com:Kevin-Mok/wrong-repo.git',
                'git' + '@' + 'example.invalid:Kevin-Mok/ai-cli-workflow.git',
                'https://github.com/Other-Owner/ai-cli-workflow',
                'https://github.com/Kevin-Mok/ai-cli-workflow/extra'):
            with self.subTest(origin=origin):
                self.git('remote', 'set-url', 'origin', origin)
                output = self.invoke('--verify', ok=False)
                self.assertIn('Origin no longer targets sanitized repository', output)

    def test_nested_and_external_dirty_worktrees_remain_attached_to_archive(self):
        nested = self.repo / '.worktrees/feature'
        external = self.root / 'external-worktree'
        self.git('worktree', 'add', '-b', 'nested', str(nested))
        self.git('worktree', 'add', '-b', 'external', str(external))
        (nested / 'file.txt').write_text('nested pending\n')
        (external / 'untracked.txt').write_text('external pending\n')
        self.invoke('--apply')
        moved = self.state / 'archive/.worktrees/feature'
        self.assertEqual((moved / 'file.txt').read_text(), 'nested pending\n')
        self.assertEqual((external / 'untracked.txt').read_text(), 'external pending\n')
        for worktree in (moved, external):
            common = Path(self.git('rev-parse', '--path-format=absolute', '--git-common-dir', cwd=worktree))
            self.assertEqual(common.resolve(), (self.state / 'archive/.git').resolve())
        self.invoke('--verify')
        self.invoke('--rollback')
        self.assertTrue(nested.exists())
        self.assertEqual((nested / 'file.txt').read_text(), 'nested pending\n')
        self.assertEqual(Path(self.git('rev-parse', '--path-format=absolute', '--git-common-dir', cwd=external)).resolve(), (self.repo / '.git').resolve())

    def test_secret_review_is_rejected_without_logging_value(self):
        token = 'gh' + 'p_' + 'A' * 36
        (self.repo / 'safe-helper.txt').write_text('token = ' + token + '\n')
        self.approve('safe-helper.txt')
        output = self.invoke('--apply', '--details', ok=False)
        self.assertIn('safe-helper.txt', output)
        self.assertNotIn(token, output)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)
        if self.state.exists():
            for path in self.state.rglob('*'):
                if path.is_file() and path.suffix in ('.log', '.json'):
                    self.assertNotIn(token, path.read_text())

    def test_protected_template_review_is_rejected(self):
        (self.repo / 'dot_gitconfig.tmpl').write_text('[user]\nname = Private Person\n')
        self.approve('dot_gitconfig.tmpl')
        self.invoke('--apply', ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)

    def test_changed_review_hash_is_rejected(self):
        (self.repo / 'file.txt').write_text('approved\n')
        self.approve('file.txt')
        (self.repo / 'file.txt').write_text('changed after review\n')
        self.invoke('--apply', ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)

    def test_wrong_destination_hash_is_rejected(self):
        (self.repo / 'file.txt').write_text('approved\n')
        self.approve('file.txt')
        review = json.loads(self.review.read_text())
        review['files']['file.txt']['base_sha256'] = '0' * 64
        self.review.write_text(json.dumps(review))
        self.invoke('--apply', ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)

    def test_review_cannot_read_outside_repository(self):
        outside = self.root / 'outside.txt'
        outside.write_text('must not copy outside checkout\n')
        self.review.write_text(json.dumps({'files': {'../../outside.txt': {
            'sha256': hashlib.sha256(outside.read_bytes()).hexdigest(),
            'base_sha256': None,
        }}}))
        self.invoke('--apply', ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)
        self.assertEqual(outside.read_text(), 'must not copy outside checkout\n')

    def test_reviewed_symlink_cannot_copy_private_target(self):
        outside = self.root / 'outside.txt'
        outside.write_text('must not follow private link\n')
        (self.repo / 'safe-helper.txt').symlink_to(outside)
        self.approve('safe-helper.txt')
        self.invoke('--apply', ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)

    def test_reviewed_destination_symlink_ancestor_cannot_write_outside_candidate(self):
        loader = importlib.machinery.SourceFileLoader('migration_destination_test', str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        migration = importlib.util.module_from_spec(spec)
        loader.exec_module(migration)
        outside = self.root / 'outside'
        outside.mkdir()
        sentinel = outside / 'file.txt'
        sentinel.write_text('preserve outside content\n')
        (self.remote / 'linked').symlink_to(outside, target_is_directory=True)
        source = self.repo / 'safe-helper.txt'
        source.write_text('reviewed safe content\n')
        self.review.write_text(json.dumps({'files': {'linked/file.txt': {
            'source': str(source),
            'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'base_sha256': hashlib.sha256(sentinel.read_bytes()).hexdigest(),
        }}}))
        with self.assertRaises(migration.MigrationError):
            migration.reviewed_transfer(self.repo, self.remote, self.review, True)
        self.assertEqual(sentinel.read_bytes(), b'preserve outside content\n')

    def test_reviewed_destination_non_directory_ancestor_is_refused(self):
        loader = importlib.machinery.SourceFileLoader('migration_destination_parent_test', str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        migration = importlib.util.module_from_spec(spec)
        loader.exec_module(migration)
        source = self.repo / 'safe-helper.txt'
        source.write_text('reviewed safe content\n')
        self.review.write_text(json.dumps({'files': {'file.txt/nested/helper.txt': {
            'source': str(source),
            'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'base_sha256': None,
        }}}))
        before = (self.remote / 'file.txt').read_bytes()
        with self.assertRaises(migration.MigrationError):
            migration.reviewed_transfer(self.repo, self.remote, self.review, True)
        self.assertEqual((self.remote / 'file.txt').read_bytes(), before)

    def test_snapshot_regression_source_passes_actual_transfer_guard(self):
        content = (SCRIPT.parents[1] / 'tests/test_second_brain_config_snapshot.py').read_bytes()
        (self.repo / 'safe-helper.txt').write_bytes(content)
        self.approve('safe-helper.txt')
        self.invoke('--apply')
        self.assertEqual((self.repo / 'safe-helper.txt').read_bytes(), content)

    def test_failed_clone_preserves_active_checkout(self):
        (self.repo / 'file.txt').write_text('pending\n')
        self.invoke('--apply', url=(self.root / 'missing-remote').as_uri(), ok=False)
        self.assertEqual((self.repo / 'file.txt').read_text(), 'pending\n')
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)

    def test_retry_after_rollback_reports_new_state_directory(self):
        self.invoke('--apply', url=(self.root / 'missing-remote').as_uri(), ok=False)
        output = self.invoke('--apply', ok=False)
        self.assertIn('new --state-dir', output)
        self.assertTrue((self.state / 'state.json').exists())

    def test_rollback_restores_original_dirty_checkout(self):
        (self.repo / 'file.txt').write_text('original dirty work\n')
        self.invoke('--apply')
        self.invoke('--rollback')
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.old_head)
        self.assertEqual((self.repo / 'file.txt').read_text(), 'original dirty work\n')
        self.assertEqual(self.git('remote', 'get-url', 'origin'), 'https://example.invalid/old-private.git')

    def test_rollback_refuses_to_overwrite_subsequent_user_change(self):
        self.invoke('--apply')
        (self.repo / 'file.txt').write_text('later user edit\n')
        self.invoke('--rollback', ok=False)
        self.assertEqual((self.repo / 'file.txt').read_text(), 'later user edit\n')
        self.assertTrue((self.state / 'archive/.git').exists())


if __name__ == '__main__':
    unittest.main()
