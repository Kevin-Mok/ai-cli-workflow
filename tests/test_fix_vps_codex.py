"""Run the real SSH payload against disposable homes and external-service fakes."""

import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/executable_fix-vps-codex.sh"


def executable(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    path.chmod(0o755)


class RepairTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vps-codex-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home with spaces"
        self.home.mkdir()
        self.bin = self.base / "bin"
        self.bin.mkdir()
        self.events = self.base / "events"
        self.events.write_text("")
        self.env = os.environ.copy()
        for key in list(self.env):
            if key.lower().startswith("npm_config_") or key in ("NVM_DIR", "FNM_DIR"):
                del self.env[key]
        self.env.update(HOME=str(self.home), SHELL="/bin/bash",
                        PATH=f"{self.bin}:/usr/bin:/bin", TEST_BASE=str(self.base),
                        XDG_CONFIG_HOME=str(self.home / ".config"),
                        PYTHONDONTWRITEBYTECODE="1")
        # Bash is real; skip host /etc/profile so this fixture is machine-independent.
        self.shell = self.bin / "bash"
        executable(self.shell, """#!/bin/bash
if [[ ${1:-} == -lic ]]; then
  shift
  for p in .bash_profile .bash_login .profile; do
    if [[ -f $HOME/$p ]]; then source "$HOME/$p"; break; fi
  done
  exec /bin/bash --noprofile --rcfile "$HOME/.bashrc" -ic "$1"
fi
exec /bin/bash "$@"
""")
        self.env["SHELL"] = str(self.shell)
        self.runtime = self.base / "system"
        self.make_runtime(self.runtime)
        self.env["PATH"] = f"{self.bin}:{self.runtime / 'bin'}:/usr/bin:/bin"
        self.registry = self.base / "registry.json"
        self.registry.write_text(json.dumps({"version": "1.2.3", "engines": {"node": ">=16"}}))
        # The SSH fake is only transport. It runs the actual received Python program.
        executable(self.bin / "ssh", f"#!{sys.executable}\n" + r'''
import contextlib, io, json, os, pathlib, shlex, sys, urllib.request
base = pathlib.Path(os.environ['TEST_BASE'])
with (base / 'events').open('a') as log:
    log.write(json.dumps(['ssh', *sys.argv[1:]]) + '\n')
if os.environ.get('SSH_FAIL'):
    sys.exit(255)
def urlopen(url, *args, **kwargs):
    if not isinstance(url, str):
        url = url.full_url
    if os.environ.get('DOWNLOAD_FAIL'):
        raise OSError('simulated network failure')
    if 'registry.npmjs.org' in url:
        path = base / 'registry.json'
    elif url.endswith('index.json'):
        path = base / 'index.json'
    elif url.endswith('SHASUMS256.txt'):
        path = base / 'SHASUMS256.txt'
    else:
        path = base / url.rsplit('/', 1)[-1]
    return contextlib.closing(io.BytesIO(path.read_bytes()))
urllib.request.urlopen = urlopen
sys.argv = shlex.split(sys.argv[-1])[1:]
payload = sys.stdin.read()
exec(compile(payload, '<remote-payload>', 'exec'), {'__name__': '__main__'})
''')

    def make_runtime(self, prefix, version="v22.15.0"):
        executable(prefix / "bin/node", f"#!/bin/sh\nprintf '%s\\n' '{version}'\n")
        npm = prefix / "lib/node_modules/npm/bin/npm-cli.js"
        executable(npm, f"#!{sys.executable}\n" + r'''
import json, os, pathlib, sys
base = pathlib.Path(os.environ['TEST_BASE'])
home = pathlib.Path(os.environ['HOME'])
args = sys.argv[1:]
with (base / 'events').open('a') as log:
    log.write(json.dumps(['npm', *args]) + '\n')
settings = {}
if (home / '.npmrc').exists():
    for line in (home / '.npmrc').read_text().splitlines():
        if '=' in line and not line.lstrip().startswith(('#', ';')):
            key, value = line.split('=', 1)
            settings[key.strip()] = os.path.expandvars(value.strip())
default = str(pathlib.Path(__file__).resolve().parents[4])
prefix = os.environ.get('npm_config_prefix', settings.get('prefix', default))
cache = settings.get('cache', str(home / '.npm'))
if args == ['--version']:
    print('10.9.0')
elif args[:2] == ['config', 'get']:
    print({'prefix': prefix, 'cache': cache, 'userconfig': str(home / '.npmrc')}[args[2]])
elif 'install' in args:
    if '--prefix' in args:
        prefix = args[args.index('--prefix') + 1]
    if os.environ.get('NPM_FAIL') or not prefix.startswith(str(home) + '/'):
        print('EACCES: permission denied, rename system Codex', file=sys.stderr)
        sys.exit(13)
    package = pathlib.Path(prefix) / 'lib/node_modules/@openai/codex'
    package.mkdir(parents=True, exist_ok=True)
    (package / 'package.json').write_text('{"version":"1.2.3"}')
    binary = pathlib.Path(prefix) / 'bin/codex'
    binary.parent.mkdir(parents=True, exist_ok=True)
    binary.write_text('#!/bin/sh\nprintf "codex-cli 1.2.3\\n"\n')
    binary.chmod(0o755)
else:
    sys.exit('unexpected npm call: ' + repr(args))
''')
        (prefix / "lib/node_modules/npm/package.json").write_text('{"version":"10.9.0"}')
        if (prefix / "bin/npm").is_symlink():
            (prefix / "bin/npm").unlink()
        (prefix / "bin/npm").symlink_to(npm)

    def run_script(self, *args, ok=True, **env):
        result = subprocess.run(["/bin/bash", str(SCRIPT), *args], env={**self.env, **env},
                                text=True, capture_output=True, timeout=30)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def snapshot(self):
        return {str(p.relative_to(self.home)): (p.lstat().st_mode,
                os.readlink(p) if p.is_symlink() else p.read_bytes() if p.is_file() else None)
                for p in self.home.rglob('*')}

    def test_help_and_invalid_args_never_connect(self):
        self.assertIn('--dry-run', self.run_script('--help').stdout)
        for args in [("--port", "0"), ("--port", "65536"), ("--host", "-oops"),
                     ("--host", "a;touch /tmp/oops"), ("--identity",), ("--wat",)]:
            self.run_script(*args, ok=False)
        self.assertEqual(self.events.read_text(), '')

    def test_dry_run_has_no_remote_writes_or_npm_calls(self):
        (self.home / '.npmrc').write_text('prefix=/usr\n//registry.npmjs.org/:_authToken=secret\n')
        before = self.snapshot()
        result = self.run_script('--dry-run')
        self.assertEqual(before, self.snapshot())
        self.assertNotIn('["npm"', self.events.read_text())
        self.assertNotIn('secret', result.stdout + result.stderr)
        self.assertIn('/usr', result.stdout)

    def test_system_prefix_fixed_and_normal_update_verified_in_second_ssh(self):
        (self.home / '.npmrc').write_text('prefix=/usr\n# keep me\n')
        result = self.run_script()
        self.assertIn('SUCCESS', result.stdout)
        config = (self.home / '.npmrc').read_text()
        self.assertIn('# keep me', config)
        self.assertNotIn('prefix=/usr', config)
        events = [json.loads(line) for line in self.events.read_text().splitlines()]
        self.assertEqual(len([e for e in events if e[0] == 'ssh']), 2)
        self.assertIn(['npm', 'install', '-g', '@openai/codex'], events)
        self.assertTrue(list(self.home.glob('.local/state/fix-vps-codex/*/rollback.py')))

    def test_second_run_keeps_configuration_identical(self):
        self.run_script()
        files = [self.home / '.npmrc', self.home / '.profile', self.home / '.bashrc']
        before = {p: p.read_bytes() for p in files}
        self.run_script()
        self.assertEqual(before, {p: p.read_bytes() for p in files})

    def test_bash_existing_profile_and_rollback(self):
        original = b'# user login customizations\n'
        profile = self.home / '.bash_profile'
        profile.write_bytes(original)
        self.run_script()
        self.assertFalse((self.home / '.profile').exists())
        restore = next(self.home.glob('.local/state/fix-vps-codex/*/rollback.py'))
        restored = subprocess.run([sys.executable, str(restore)], text=True, capture_output=True)
        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assertEqual(profile.read_bytes(), original)
        self.assertFalse((self.home / '.npmrc').exists())

    @unittest.skipUnless(shutil.which('fish'), 'fish is not installed')
    def test_real_fish_config_late_path_override(self):
        config = self.home / '.config/fish/config.fish'
        config.parent.mkdir(parents=True)
        config.write_text(f'set -gx PATH "{self.runtime / "bin"}" $PATH\n')
        result = self.run_script(SHELL=shutil.which('fish'))
        self.assertIn('SUCCESS', result.stdout)

    @unittest.skipUnless(shutil.which('fish'), 'fish is not installed')
    def test_fish_cursor_sequence_does_not_break_shell_probes(self):
        config = self.home / '.config/fish/config.fish'
        config.parent.mkdir(parents=True)
        config.write_text("printf '\\033[6 q'\nprintf 'missing desktop file\\n' >&2\n")
        result = self.run_script(SHELL=shutil.which('fish'))
        self.assertIn('SUCCESS', result.stdout)

    def test_bash_banner_without_newline_does_not_break_shell_probes(self):
        (self.home / '.bashrc').write_text("printf 'hello without a newline'\n")
        result = self.run_script()
        self.assertIn('SUCCESS', result.stdout)

    def test_manager_runtime_reused_without_npmrc_prefix(self):
        managed = self.home / '.local/share/fnm/node-versions/v22.15.0/installation'
        self.make_runtime(managed)
        self.run_script(PATH=f'{self.bin}:{managed / "bin"}:/usr/bin:/bin')
        self.assertFalse((self.home / '.npmrc').exists())
        self.assertTrue((managed / 'bin/codex').exists())

    def test_symlinked_config_is_rejected_without_replacing_it(self):
        target = self.base / 'real-npmrc'
        target.write_text('prefix=/usr\n')
        (self.home / '.npmrc').symlink_to(target)
        self.run_script(ok=False)
        self.assertTrue((self.home / '.npmrc').is_symlink())
        self.assertEqual(target.read_text(), 'prefix=/usr\n')

    def test_ssh_failure_preserves_exit_status(self):
        result = self.run_script(ok=False, SSH_FAIL='1')
        self.assertEqual(result.returncode, 255)
        self.assertIn('SSH', result.stderr)

    def test_install_failure_does_not_change_shell_routing(self):
        result = self.run_script(ok=False, NPM_FAIL='1')
        self.assertFalse((self.home / '.profile').exists())
        self.assertFalse((self.home / '.bashrc').exists())
        self.assertNotIn('unknown host', result.stderr)

    def prepare_runtime_download(self, corrupt=False):
        archive = self.base / 'node-v24.1.0-linux-x64.tar.gz'
        runtime = self.base / 'download-runtime'
        self.make_runtime(runtime, 'v24.1.0')
        # Node's official npm link is relative; keep the fixture portable after extraction.
        (runtime / 'bin/npm').unlink()
        (runtime / 'bin/npm').symlink_to('../lib/node_modules/npm/bin/npm-cli.js')
        with tarfile.open(archive, 'w:gz') as tar:
            tar.add(runtime, arcname='node-v24.1.0-linux-x64')
        digest = '0' * 64 if corrupt else hashlib.sha256(archive.read_bytes()).hexdigest()
        (self.base / 'SHASUMS256.txt').write_text(f'{digest}  {archive.name}\n')
        (self.base / 'index.json').write_text(json.dumps([
            {'version': 'v24.1.0', 'lts': 'Fixture', 'files': ['linux-x64']}
        ]))
        self.make_runtime(self.runtime, 'v14.0.0')

    def test_old_node_uses_verified_user_runtime(self):
        self.prepare_runtime_download()
        result = self.run_script()
        self.assertIn('SUCCESS', result.stdout)
        self.assertIn('v14.0.0', subprocess.check_output([str(self.runtime / 'bin/node'), '--version'], text=True))

    def test_bad_checksum_does_not_change_shell_or_npm_config(self):
        self.prepare_runtime_download(corrupt=True)
        result = self.run_script(ok=False)
        self.assertIn('checksum', result.stderr.lower())
        self.assertFalse((self.home / '.npmrc').exists())
        self.assertFalse((self.home / '.profile').exists())

    def test_download_failure_is_actionable_without_config_changes(self):
        result = self.run_script(ok=False, DOWNLOAD_FAIL='1')
        self.assertIn('network', result.stderr.lower())
        self.assertEqual(self.snapshot(), {})

    def test_codex_function_cannot_fake_success(self):
        (self.home / '.bashrc').write_text('codex() { echo "codex-cli 0.0.1"; }\n')
        result = self.run_script(ok=False)
        self.assertIn('shadow', result.stderr.lower())
        self.assertNotIn('SUCCESS', result.stdout)

    def test_retry_after_runtime_install_then_npm_failure(self):
        self.prepare_runtime_download()
        self.run_script(ok=False, NPM_FAIL='1')
        result = self.run_script()
        self.assertIn('SUCCESS', result.stdout)

    def test_external_state_symlink_is_not_written(self):
        outside = self.base / 'outside-state'
        outside.mkdir()
        (self.home / '.local').mkdir()
        (self.home / '.local/state').symlink_to(outside)
        self.run_script(ok=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_unwritable_cache_is_replaced_with_user_cache(self):
        (self.home / '.npmrc').write_text('prefix=/usr\ncache=/var/cache\n')
        self.run_script()
        content = (self.home / '.npmrc').read_text()
        self.assertIn('cache=' + str(self.home / '.cache/codex-npm'), content)
        self.assertNotIn('cache=/var/cache', content)

    def test_dry_run_does_not_execute_shell_startup(self):
        (self.home / '.bash_profile').write_text('touch "$HOME/should-not-exist"\n')
        before = self.snapshot()
        self.run_script('--dry-run')
        self.assertEqual(before, self.snapshot())

    def test_connection_options_reach_ssh_without_shell_interpolation(self):
        key = self.base / 'my key'
        key.write_text('fixture, not a real key')
        self.run_script('--dry-run', '--host', 'example-alias', '--port', '2222', '--identity', str(key))
        call = json.loads(self.events.read_text().splitlines()[0])
        self.assertIn('StrictHostKeyChecking=yes', call)
        self.assertIn('BatchMode=yes', call)
        self.assertEqual(call[call.index('-p') + 1], '2222')
        self.assertEqual(call[call.index('-i') + 1], str(key))
        self.assertEqual(call[-2], 'example-alias')

    def test_rerun_preserves_user_lines_after_managed_block(self):
        rc = self.home / '.bashrc'
        rc.write_text('export BEFORE=1\n')
        self.run_script()
        with rc.open('a') as file:
            file.write('export AFTER=2\n')
        self.run_script()
        self.assertIn('export BEFORE=1\nexport AFTER=2\n', rc.read_text())

    def test_archive_cannot_write_through_symlink_parent(self):
        self.prepare_runtime_download()
        archive = self.base / 'node-v24.1.0-linux-x64.tar.gz'
        root = 'node-v24.1.0-linux-x64'
        with tarfile.open(archive, 'w:gz') as tar:
            for name, target in [('a', '.'), ('a/b', '../outside')]:
                member = tarfile.TarInfo(root + '/' + name)
                member.type = tarfile.SYMTYPE
                member.linkname = target
                tar.addfile(member)
            member = tarfile.TarInfo(root + '/a/b/escaped')
            member.size = 1
            tar.addfile(member, io.BytesIO(b'x'))
        (self.base / 'SHASUMS256.txt').write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n')
        result = self.run_script(ok=False)
        self.assertIn('unsafe', result.stderr.lower())

    def test_archive_cannot_replace_symlink_with_duplicate_member(self):
        self.prepare_runtime_download()
        archive = self.base / 'node-v24.1.0-linux-x64.tar.gz'
        root = 'node-v24.1.0-linux-x64'
        with tarfile.open(archive, 'w:gz') as tar:
            for name, target in [('a', '.'), ('b', 'a/../outside')]:
                member = tarfile.TarInfo(root + '/' + name)
                member.type = tarfile.SYMTYPE
                member.linkname = target
                tar.addfile(member)
            member = tarfile.TarInfo(root + '/b')
            member.size = 1
            tar.addfile(member, io.BytesIO(b'x'))
        (self.base / 'SHASUMS256.txt').write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n')
        result = self.run_script(ok=False)
        self.assertIn('unsafe', result.stderr.lower())


if __name__ == '__main__':
    unittest.main()
