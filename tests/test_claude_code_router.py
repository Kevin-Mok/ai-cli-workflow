"""Installer boundary checks; all network/package operations use strict fixtures."""
import json
import os
import shutil
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / 'run_onchange_after_install-claude-code-router.sh.tmpl'
WRAPPER = ROOT / 'dot_local/bin/executable_ccr'


class RouterInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.bin = self.home / 'fixtures'
        self.bin.mkdir()
        self.env = dict(os.environ, HOME=str(self.home), PATH=f'{self.bin}:/usr/bin:/bin')
        self.prefix = self.home / '.local/share/claude-code-router'
        self.package = self.prefix / 'lib/node_modules/@musistudio/claude-code-router'
        self.tool('node', '''#!/usr/bin/python3
import json, os, sys
if sys.argv[1] == '--version': print(os.environ.get('NODE_VERSION', 'v22.15.0'))
elif sys.argv[1] == '-p': print(json.load(open(sys.argv[-1]))['version'])
else: print(json.dumps({'args':sys.argv[1:], 'catalog':os.environ.get('CCR_MODEL_CATALOG_PATH'), 'host':os.environ.get('CCR_WEB_HOST')}))
''')
        self.tool('curl', '''#!/usr/bin/python3
import os, sys
from pathlib import Path
assert sys.argv[1:5] == ['--fail', '--location', '--silent', '--show-error']
assert 'https://registry.npmjs.org/@musistudio/claude-code-router/-/claude-code-router-3.1.3.tgz' in sys.argv
Path(sys.argv[sys.argv.index('--output')+1]).write_bytes(b'fixture')
''')
        self.tool('sha512sum', '''#!/usr/bin/python3
import os, sys
assert sys.argv[1:] == ['--check', '--status']
line=sys.stdin.read()
assert line.startswith('7551d1bbd49bff11bd760afc9c7266bdde57548439cab11e2a63283d410173dc6d83291f453db3efa35123e7f29697a2333602eb4cfabeb57ac7fdc8639da9be  ')
sys.exit(int(os.environ.get('BAD_HASH', '0')))
''')
        self.tool('npm', '''#!/usr/bin/python3
import json, os, sys
from pathlib import Path
assert sys.argv[1:4] == ['install', '--global', '--prefix']
assert sys.argv[5:7] == ['--no-audit', '--no-fund']
assert sys.argv[-1].endswith('/router.tgz')
home=Path(os.environ['HOME'])
with (home/'npm-calls').open('a') as f: f.write('install\\n')
if os.environ.get('NPM_FAIL'): sys.exit(23)
p=Path(sys.argv[4])/'lib/node_modules/@musistudio/claude-code-router'
(p/'dist/main').mkdir(parents=True,exist_ok=True)
(p/'package.json').write_text(json.dumps({'version':'3.1.3'}))
(p/'dist/main/cli.js').touch()
(p/'dist/models.json').write_text('{}')
''')

    def tool(self, name, body):
        path = self.bin / name
        path.write_text(body)
        path.chmod(0o755)

    def install(self, *args):
        self.assertTrue(INSTALLER.exists(), 'router installer is missing')
        return subprocess.run(['/bin/bash', str(INSTALLER), *args], env=self.env,
                              text=True, capture_output=True, timeout=20)

    def test_pinned_private_install_and_second_run_no_network(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads((self.package/'package.json').read_text())['version'], '3.1.3')
        self.assertFalse((self.home/'.claude-code-router').exists())
        self.assertFalse((self.home/'.claude').exists())
        self.assertFalse((self.home/'.codex').exists())
        self.tool('curl', '#!/bin/sh\nexit 81\n')
        self.tool('npm', '#!/bin/sh\nexit 82\n')
        second = self.install()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual((self.home/'npm-calls').read_text(), 'install\n')

    def test_old_node_skips_before_download(self):
        self.env['NODE_VERSION'] = 'v20.19.0'
        result = self.install()
        self.assertEqual(result.returncode, 0)
        self.assertIn('Node.js 22', result.stderr)
        self.assertFalse(self.prefix.exists())

    def test_missing_npm_skips_without_writing(self):
        (self.bin/'npm').unlink()
        self.env['PATH'] = str(self.bin)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('npm missing', result.stderr)
        self.assertFalse(self.prefix.exists())

    def test_integrity_failure_never_installs(self):
        self.env['BAD_HASH'] = '1'
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.home/'npm-calls').exists())

    def test_npm_failure_is_actionable_and_nonzero(self):
        self.env['NPM_FAIL'] = '1'
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('failed', result.stderr.lower())
        self.assertFalse((self.package/'package.json').exists())

    def test_plain_output_and_no_startup(self):
        self.env['CLI_PLAIN'] = '1'
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stderr.isascii())
        self.assertIn('3.1.3', result.stderr)

    def test_wrapper_forces_offline_catalog_and_loopback(self):
        self.install()
        self.assertTrue(WRAPPER.exists(), 'router launcher is missing')
        self.env.update(CCR_MODEL_CATALOG_PATH='/wrong', CCR_WEB_HOST='0.0.0.0')
        result = subprocess.run(['bash', str(WRAPPER), '--help'], env=self.env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['catalog'], str(self.package/'dist/models.json'))
        self.assertEqual(data['host'], '127.0.0.1')
        self.assertEqual(data['args'], [str(self.package/'dist/main/cli.js'), '--help'])

    def test_wrapper_version_does_not_launch_upstream(self):
        self.install()
        self.assertTrue(WRAPPER.exists(), 'router launcher is missing')
        result = subprocess.run(['bash', str(WRAPPER), '--version'], env=self.env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), '3.1.3')

    @unittest.skipUnless(shutil.which('chezmoi'), 'chezmoi not installed')
    def test_chezmoi_seed_maps_to_private_config_and_preserves_existing(self):
        source = self.home / 'source'
        source.mkdir()
        shutil.copytree(ROOT/'dot_claude-code-router', source/'dot_claude-code-router')
        destination = self.home / 'destination'
        destination.mkdir()
        base = ['chezmoi', '--source', str(source), '--destination', str(destination),
                '--config', '/dev/null', '--config-format', 'toml',
                '--cache', str(self.home/'cache'), '--persistent-state', str(self.home/'state')]
        target = destination/'.claude-code-router/config.json'
        dump = subprocess.run(base+['dump', '--format', 'json', str(target)],
                              capture_output=True, text=True)
        self.assertEqual(dump.returncode, 0, dump.stderr)
        metadata = json.loads(dump.stdout)['.claude-code-router/config.json']
        self.assertEqual(metadata['perm'], 0o600)
        config = json.loads(metadata['contents'])
        self.assertFalse(config['profile']['enabled'])
        self.assertEqual(config['profile']['profiles'], [])
        self.assertFalse(config['observability']['requestLogs'])
        self.assertEqual(config['observability']['requestLogBodyCapture'], 'none')
        target.parent.mkdir()
        target.write_text('{"existing-user-config":true}\n')
        target.chmod(0o600)
        diff = subprocess.run(base+['diff', str(target)], capture_output=True, text=True)
        self.assertEqual(diff.returncode, 0, diff.stderr)
        self.assertEqual(diff.stdout, '')
        self.assertEqual(target.read_text(), '{"existing-user-config":true}\n')


if __name__ == '__main__':
    unittest.main()
