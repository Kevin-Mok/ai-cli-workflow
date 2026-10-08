"""Independent sessions timer installation and calendar behavior."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HELPER = REPO / 'scripts/executable_setup-second-brain-sessions-timer'
UNITS = REPO / 'dot_config/systemd/user'


class SessionsTimerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / 'home'
        self.home.mkdir()
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.runtime_lib = self.root / 'runtime-lib'
        self.runtime_lib.mkdir()
        codex = self.runtime_lib / 'codex.js'
        codex.write_text('#!/usr/bin/env node\n// synthetic Codex; never execute\n')
        codex.chmod(0o755)
        (self.bin / 'codex').symlink_to(codex)
        node = self.bin / 'node'
        node.write_text('#!/bin/sh\nexit 99\n')
        node.chmod(0o755)
        self.log = self.root / 'calls'
        self.log.touch()
        fake = '''#!/usr/bin/env python3
import json, os, pathlib, shutil, sys
args = sys.argv[1:]
name = pathlib.Path(sys.argv[0]).name
with open(os.environ['CALLS'], 'a') as log:
    log.write(json.dumps([name, *args]) + '\\n')
repo = pathlib.Path(os.environ['REPO'])
if name == 'chezmoi' and args[0] == 'source-path':
    target = pathlib.Path(args[1])
    if target.name == 'second_brain': source = repo / 'scripts/second_brain'
    elif target.name == 'second-brain': source = repo / 'scripts/executable_second-brain'
    elif target.name in ('codex_search_index.py', 'codex_search_runtime.py'): source = repo / 'scripts' / target.name
    else: source = repo / 'dot_config/systemd/user' / target.name
    print(source)
elif name == 'chezmoi' and args[0] == 'apply':
    for value in args[1:]:
        target = pathlib.Path(value)
        if target.name == 'state.py':
            target.unlink(missing_ok=True)
            continue
        if target.name == 'second-brain': source = repo / 'scripts/executable_second-brain'
        elif target.suffix == '.py': source = repo / 'scripts/second_brain' / target.name
        else: source = repo / 'dot_config/systemd/user' / target.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
'''
        for name in ('chezmoi', 'systemctl', 'systemd-analyze'):
            path = self.bin / name
            path.write_text(fake)
            path.chmod(0o755)
        self.env = {**os.environ, 'HOME': str(self.home),
                    'XDG_STATE_HOME': str(self.root / 'state'),
                    'PATH': f'{self.bin}:{os.environ["PATH"]}',
                    'CALLS': str(self.log), 'REPO': str(REPO),
                    'PYTHONDONTWRITEBYTECODE': '1'}

    def run_helper(self, action):
        return subprocess.run(['python3', str(HELPER), action], env=self.env,
                              capture_output=True, text=True, check=False)

    def calls(self):
        import json
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def install_dependencies(self):
        target = self.home / 'scripts'
        target.mkdir(exist_ok=True)
        for name in ('codex_search_index.py', 'codex_search_runtime.py'):
            shutil.copy2(REPO / 'scripts' / name, target / name)

    def test_enable_refuses_missing_parser_runtime_dependencies_before_activation(self):
        result = self.run_helper('--enable')
        self.assertEqual(result.returncode, 2)
        self.assertIn('digest dependency', result.stderr)
        self.assertFalse(any('enable' in call or 'apply' in call for call in self.calls()))

    def test_enable_refuses_stale_runtime_dependency_before_activation(self):
        self.install_dependencies()
        (self.home / 'scripts/codex_search_runtime.py').write_text('# stale runtime\n')
        result = self.run_helper('--enable')
        self.assertEqual(result.returncode, 2)
        self.assertIn('digest dependency is stale', result.stderr)
        self.assertFalse(any('enable' in call or 'apply' in call for call in self.calls()))

    def test_enable_installs_only_sessions_units_and_enables_one_timer(self):
        self.install_dependencies()
        result = self.run_helper('--enable')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(['systemctl', '--user', 'enable', '--now',
                       'second-brain-sessions.timer'], self.calls())
        installed = self.home / '.config/systemd/user'
        self.assertEqual({p.name for p in installed.iterdir() if p.is_file()},
                         {'second-brain-sessions.service', 'second-brain-sessions.timer'})
        self.assertFalse(any(arg.endswith(('second-brain-checkpoint.timer',
                                           'second-brain-checkpoint.service',
                                           'second-brain-deferred.timer',
                                           'second-brain-deferred.service'))
                             for call in self.calls() for arg in call))
        result = self.run_helper('--check')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_enable_pins_original_codex_bin_for_service_without_running_inference(self):
        self.install_dependencies()
        result = self.run_helper('--enable')
        self.assertEqual(result.returncode, 0, result.stderr)
        dropin = self.home / '.config/systemd/user/second-brain-sessions.service.d/runtime-path.conf'
        self.assertTrue(dropin.is_file(), 'scheduled Codex runtime PATH was not installed')
        import configparser
        import shlex
        config = configparser.ConfigParser(interpolation=None)
        config.read(dropin)
        setting = shlex.split(config['Service']['Environment'])[0]
        self.assertTrue(setting.startswith(f'PATH={self.bin}:'), setting)
        self.assertNotIn(f'PATH={self.runtime_lib}:', setting)
        self.assertEqual(dropin.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.run_helper('--check').returncode, 0)

    def test_check_refuses_pinned_runtime_when_node_is_missing(self):
        self.install_dependencies()
        self.assertEqual(self.run_helper('--enable').returncode, 0)
        (self.bin / 'node').unlink()
        self.log.write_text('')
        result = self.run_helper('--check')
        self.assertEqual(result.returncode, 2)
        self.assertIn('runtime', result.stderr)
        self.assertFalse(any('enable' in call for call in self.calls()))

    def test_enable_refuses_no_active_codex_without_guessing_default_node(self):
        self.install_dependencies()
        (self.bin / 'codex').unlink()
        self.env['PATH'] = f'{self.bin}:/usr/bin:/bin'
        result = self.run_helper('--enable')
        self.assertEqual(result.returncode, 2)
        self.assertIn('runtime', result.stderr)
        self.assertFalse(any('enable' in call or 'apply' in call for call in self.calls()))

    def test_disable_needs_no_source_install_and_touches_only_sessions_timer(self):
        result = self.run_helper('--disable')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), [
            ['systemctl', '--user', 'show-environment'],
            ['systemctl', '--user', 'disable', '--now', 'second-brain-sessions.timer']])
        self.assertFalse((self.home / 'scripts').exists())

    def test_stale_installed_unit_fails_check_without_activation(self):
        self.install_dependencies()
        result = self.run_helper('--enable')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.log.write_text('')
        target = self.home / '.config/systemd/user/second-brain-sessions.timer'
        target.write_text('[Timer]\nOnCalendar=daily\n')
        result = self.run_helper('--check')
        self.assertEqual(result.returncode, 2)
        self.assertIn('stale', result.stderr)
        self.assertFalse(any('enable' in call for call in self.calls()))

    def test_calendar_resolves_toronto_across_daylight_saving(self):
        timer = UNITS / 'second-brain-sessions.timer'
        self.assertTrue(timer.exists(), 'sessions timer is not implemented')
        import configparser
        config = configparser.ConfigParser(interpolation=None)
        config.read(timer)
        self.assertTrue(config.getboolean('Timer', 'Persistent'))
        calendar = config['Timer']['OnCalendar']
        for base, expected in (('2026-07-01 12:00:00 UTC', '20:00:00 UTC'),
                               ('2026-12-01 12:00:00 UTC', '21:00:00 UTC')):
            result = subprocess.run(['systemd-analyze', 'calendar',
                                     f'--base-time={base}', calendar],
                                    env={**os.environ, 'TZ': 'UTC'},
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(expected, result.stdout)
        service = configparser.ConfigParser(interpolation=None, strict=False)
        service.read(UNITS / 'second-brain-sessions.service')
        self.assertEqual(service['Service']['ExecStart'],
                         '/usr/bin/env %h/scripts/second-brain sessions refresh --format json')
        self.assertEqual(service['Service']['UMask'], '0077')
        self.assertNotIn('notify', service['Service']['ExecStart'])


if __name__ == '__main__':
    unittest.main()
