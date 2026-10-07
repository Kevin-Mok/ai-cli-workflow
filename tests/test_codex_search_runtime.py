"""Recap CLI isolation contracts; fake app-server never contacts a model."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'scripts/codex_search_runtime.py'

FAKE = r'''
import json, os, pathlib, subprocess, sys, time, tomllib
args = sys.argv[1:]
if args[:2] == ['exec', '--help']:
    print('--ephemeral --ignore-rules --output-schema --strict-config --json --output-last-message')
    sys.exit(0)
assert 'app-server' in args, 'Only non-inference configuration probes are allowed'
fixture = json.loads(pathlib.Path(os.environ['RUNTIME_FIXTURE']).read_text())
config = fixture['config']
for i, arg in enumerate(args[:-1]):
    if arg == '-c':
        key, value = args[i+1].split('=', 1)
        value = tomllib.loads('value=' + value)['value']
        target = config
        parts = key.split('.')
        for part in parts[:-1]:
            target = target.setdefault(part, {})
        target[parts[-1]] = value
if fixture.get('unsafe_feature'):
    config['features'][fixture['unsafe_feature']] = True
for raw in sys.stdin:
    request = json.loads(raw)
    method = request['method']
    with open(os.environ['RUNTIME_LOG'], 'a') as log:
        log.write(method + '\n')
    if method == 'initialized':
        continue
    if method == 'initialize':
        result = {'userAgent': 'fake/1.0'}
    elif method == 'config/read':
        if fixture.get('delay'):
            if fixture.get('child'):
                child = subprocess.Popen([sys.executable, '-c', 'import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(30)'])
                pathlib.Path(os.environ['RUNTIME_PID']+'.child').write_text(str(child.pid))
                time.sleep(.1)
            pathlib.Path(os.environ['RUNTIME_PID']).write_text(str(os.getpid()))
            time.sleep(30)
        result = {'config': config, 'origins': {}, 'layers': [
            {'name': {'type': 'user', 'file': str(pathlib.Path(os.environ['CODEX_HOME'])/'config.toml')},
             'version': 'fixture', 'config': {}}]}
        if fixture.get('projected_tools'):
            result['layers'].insert(0, {'name': {'type': 'sessionFlags'}, 'version': 'fixture',
                                        'config': {'tools': config['tools']}})
            config['tools'] = {'web_search': None}
        if pathlib.Path('.codex/config.toml').exists():
            result['layers'].append({'name': {'type': 'project', 'dotCodexFolder': str(pathlib.Path.cwd()/'.codex')},
                                     'version': 'fixture', 'config': {}})
    elif method == 'hooks/list':
        result = {'data': [{'cwd': os.getcwd(), 'hooks': fixture.get('hooks', []),
                            'warnings': [], 'errors': []}]}
        if fixture.get('missing_hooks'):
            result['data'] = [{'cwd': os.getcwd()}]
    elif method == 'mcpServerStatus/list':
        result = {'data': [{'name': name, 'runtimeStatus': None, 'tools': {},
                            'resources': [], 'resourceTemplates': []}
                           for name in config.get('mcp_servers', {})], 'nextCursor': None}
        if fixture.get('mcp_tools'):
            result['data'][0]['tools'] = {'unsafe': {}}
    elif method == 'configRequirements/read':
        result = {'requirements': fixture.get('requirements')}
    else:
        raise AssertionError('Unexpected model or mutation method: ' + method)
    print(json.dumps({'id': request['id'], 'result': result}), flush=True)
'''


class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.is_file(), 'isolated recap runtime is not implemented')
        spec = importlib.util.spec_from_file_location('recap_runtime', MODULE)
        self.runtime = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.runtime)
        self.temp = tempfile.TemporaryDirectory(prefix='recap-runtime-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / 'codex'
        self.home.mkdir()
        self.config = self.home / 'config.toml'
        self.config.write_text('model="configured-model"\n')
        self.fixture = self.base / 'fixture.json'
        self.data = {'config': {'model': 'configured-model', 'model_provider': 'custom',
                               'mcp_servers': {'direct': {'command': '/never/run', 'enabled': True}}}}
        self.write_fixture()
        bindir = self.base / 'bin'
        bindir.mkdir()
        codex = bindir / 'codex'
        codex.write_text('#!' + sys.executable + '\n' + FAKE)
        codex.chmod(0o755)
        self.log = self.base / 'methods'
        self.pid = self.base / 'pid'
        self.env = patch.dict(os.environ, {'PATH': str(bindir) + os.pathsep + os.environ['PATH'],
                              'RUNTIME_FIXTURE': str(self.fixture), 'RUNTIME_LOG': str(self.log),
                              'RUNTIME_PID': str(self.pid), 'CODEX_THREAD_ID': 'parent-thread',
                              'CODEX_SESSION_ID': 'parent-session',
                              'CODEX_INTERNAL_ORIGINATOR_OVERRIDE': 'parent-origin'}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def write_fixture(self):
        self.fixture.write_text(json.dumps(self.data))

    def test_listing_resolves_model_without_process_or_guess(self):
        with patch.object(subprocess, 'Popen', side_effect=AssertionError('no subprocess')):
            self.assertEqual(self.runtime.resolve_model(self.home), 'configured-model')
            self.assertEqual(self.runtime.resolve_model(self.home, 'override'), 'override')
            self.config.write_text('model=42\n')
            self.assertIsNone(self.runtime.resolve_model(self.home))
            self.config.write_text('not TOML {')
            self.assertIsNone(self.runtime.resolve_model(self.home))

    def test_listing_profile_model_and_missing_profile_are_explicit(self):
        self.config.write_text('model="base"\nprofile="work"\n[profiles.work]\nmodel="profile"\n')
        self.assertEqual(self.runtime.resolve_model(self.home), 'profile')
        self.config.write_text('model="base"\nprofile="missing"\n')
        self.assertIsNone(self.runtime.resolve_model(self.home))

    def test_prepare_verifies_loaded_config_and_builds_ephemeral_command(self):
        runtime = self.runtime.IsolatedCodex(self.home)
        self.assertEqual(runtime.prepare(), 'configured-model')
        cwd = self.base / 'scratch'
        cwd.mkdir()
        schema = cwd / 'schema.json'
        schema.write_text('{}')
        output = cwd / 'output.json'
        argv, env = runtime.command(cwd, schema, output)
        self.assertIn('--ephemeral', argv)
        self.assertIn('--ignore-rules', argv)
        self.assertIn('--output-schema', argv)
        self.assertEqual(argv[argv.index('-C')+1], str(cwd))
        self.assertEqual(argv[argv.index('-m')+1], 'configured-model')
        self.assertEqual(argv[argv.index('-s')+1], 'read-only')
        self.assertIn('mcp_servers.direct.enabled=false', argv)
        self.assertEqual(env['CODEX_HOME'], str(self.home))
        self.assertFalse('CODEX_THREAD_ID' in env)
        self.assertFalse('CODEX_SESSION_ID' in env)
        self.assertFalse('CODEX_INTERNAL_ORIGINATOR_OVERRIDE' in env)
        self.assertEqual(argv[-1], '-')
        instructions = next(value.split('=', 1)[1] for value in argv
                            if value.startswith('model_instructions_file='))
        self.assertTrue(Path(json.loads(instructions)).is_file())
        methods = self.log.read_text().splitlines()
        self.assertIn('hooks/list', methods)
        self.assertIn('mcpServerStatus/list', methods)
        self.assertNotIn('turn/start', methods)

    def test_model_override_is_used_for_verification_and_command(self):
        runtime = self.runtime.IsolatedCodex(self.home, 'override-model')
        self.assertEqual(runtime.prepare(), 'override-model')

    def test_projected_plan_tool_setting_uses_highest_priority_layer_evidence(self):
        self.data['projected_tools'] = True
        self.write_fixture()
        self.assertEqual(self.runtime.IsolatedCodex(self.home).prepare(), 'configured-model')

    def test_command_requires_successful_preflight(self):
        runtime = self.runtime.IsolatedCodex(self.home)
        with self.assertRaises(self.runtime.RuntimeUnavailable):
            runtime.command(self.base, self.base/'schema', self.base/'output')

    def test_enabled_shell_effective_override_is_rejected(self):
        self.data['unsafe_feature'] = 'shell_tool'
        self.write_fixture()
        with self.assertRaisesRegex(self.runtime.RuntimeUnavailable, 'isolation'):
            self.runtime.IsolatedCodex(self.home).prepare()

    def test_legacy_javascript_execution_flag_is_explicitly_disabled(self):
        self.data['unsafe_feature'] = 'js_repl'
        self.write_fixture()
        with self.assertRaisesRegex(self.runtime.RuntimeUnavailable, 'isolation'):
            self.runtime.IsolatedCodex(self.home).prepare()

    def test_loaded_hooks_are_rejected(self):
        self.data['hooks'] = [{'event': 'SessionStart'}]
        self.write_fixture()
        with self.assertRaisesRegex(self.runtime.RuntimeUnavailable, 'hook'):
            self.runtime.IsolatedCodex(self.home).prepare()

    def test_missing_hook_inventory_is_not_treated_as_empty(self):
        self.data['missing_hooks'] = True
        self.write_fixture()
        with self.assertRaisesRegex(self.runtime.RuntimeUnavailable, 'hook'):
            self.runtime.IsolatedCodex(self.home).prepare()

    def test_repo_launcher_is_skipped_without_starting_graphiti(self):
        wrapper_dir = self.base/'wrapper'
        wrapper_dir.mkdir()
        wrapper = wrapper_dir/'codex'
        marker = self.base/'sidecar-started'
        wrapper.write_text('#!/bin/sh\n# CODEX_WRAPPER_GRAPHITI_CWD ensure_graphiti_running\n'
                           + 'touch '+str(marker)+'\nexit 88\n')
        wrapper.chmod(0o755)
        with patch.dict(os.environ, {'PATH': str(wrapper_dir)+os.pathsep+os.environ['PATH']}):
            self.assertEqual(self.runtime.IsolatedCodex(self.home).prepare(), 'configured-model')
        self.assertFalse(marker.exists())

    def test_mcp_tool_inventory_is_rejected_even_if_config_says_disabled(self):
        self.data['mcp_tools'] = True
        self.write_fixture()
        with self.assertRaisesRegex(self.runtime.RuntimeUnavailable, 'MCP'):
            self.runtime.IsolatedCodex(self.home).prepare()

    def test_unsupported_mcp_name_fails_closed_without_quoted_key_guessing(self):
        self.data['config']['mcp_servers'] = {'dotted.name': {'command': '/never/run'}}
        self.write_fixture()
        with self.assertRaisesRegex(self.runtime.RuntimeUnavailable, 'MCP'):
            self.runtime.IsolatedCodex(self.home).prepare()

    def test_configuration_drift_blocks_command(self):
        runtime = self.runtime.IsolatedCodex(self.home)
        runtime.prepare()
        self.config.write_text('model="changed"\n')
        with self.assertRaisesRegex(self.runtime.RuntimeUnavailable, 'changed'):
            runtime.command(self.base, self.base/'schema', self.base/'output')

    def test_final_generation_directory_is_verified(self):
        runtime = self.runtime.IsolatedCodex(self.home)
        runtime.prepare()
        cwd = self.base/'unsafe'
        (cwd/'.codex').mkdir(parents=True)
        (cwd/'.codex/config.toml').write_text('developer_instructions="injection"')
        with self.assertRaisesRegex(self.runtime.RuntimeUnavailable, 'project'):
            runtime.command(cwd, cwd/'schema', cwd/'output')

    def test_cancel_reaps_active_preflight(self):
        self.data['delay'] = True
        self.write_fixture()
        runtime = self.runtime.IsolatedCodex(self.home)
        failures = []
        def prepare():
            try:
                runtime.prepare()
            except self.runtime.RuntimeUnavailable as exc:
                failures.append(str(exc))
        thread = threading.Thread(target=prepare)
        thread.start()
        deadline = time.monotonic()+3
        while not self.pid.exists() and time.monotonic()<deadline:
            time.sleep(.01)
        self.assertTrue(self.pid.exists())
        pid = int(self.pid.read_text())
        runtime.cancel()
        thread.join(3)
        self.assertFalse(thread.is_alive())
        self.assertTrue(failures)
        with self.assertRaises(ProcessLookupError):
            os.kill(pid, 0)

    def test_cancel_stops_descendant_after_preflight_leader_exits(self):
        self.data.update(delay=True, child=True)
        self.write_fixture()
        runtime = self.runtime.IsolatedCodex(self.home)
        def prepare():
            try:
                runtime.prepare()
            except self.runtime.RuntimeUnavailable:
                pass
        thread = threading.Thread(target=prepare)
        thread.start()
        deadline = time.monotonic()+3
        while not self.pid.exists() and time.monotonic()<deadline:
            time.sleep(.01)
        self.assertTrue(self.pid.exists())
        child_pid = int(Path(str(self.pid)+'.child').read_text())
        try:
            runtime.cancel()
            thread.join(3)
            self.assertFalse(thread.is_alive())
            time.sleep(.05)
            proc = Path('/proc')/str(child_pid)/'stat'
            self.assertTrue(not proc.exists() or proc.read_text().split()[2] == 'Z',
                            'preflight descendant is still running')
        finally:
            try:
                os.kill(child_pid, 9)
            except ProcessLookupError:
                pass

    def test_attempt_deadline_bounds_preflight_and_prevents_expired_start(self):
        runtime=self.runtime.IsolatedCodex(self.home)
        self.assertTrue(hasattr(runtime,'set_deadline'),'runtime has no shared attempt deadline')
        runtime.set_deadline(time.monotonic()-.01)
        with self.assertRaisesRegex(self.runtime.RuntimeUnavailable,'timed out'):
            runtime.prepare()
        self.assertFalse(self.log.exists(),'expired preflight launched a subprocess')


if __name__ == '__main__':
    unittest.main()
