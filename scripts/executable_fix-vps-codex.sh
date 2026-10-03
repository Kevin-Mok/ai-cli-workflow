#!/usr/bin/env bash
# Local SSH transport; the self-contained remote payload requires Python 3.8+.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: executable_fix-vps-codex.sh [OPTIONS]

Repair Codex npm permissions on a Linux VPS as its normal user, without sudo.
The default target is example-user@51.222.111.61. Run this script on your local PC.

  --host USER@HOST  SSH destination or configured alias
  --port PORT       Override the SSH port (otherwise use SSH configuration)
  --identity FILE   Select an SSH private key (otherwise use SSH configuration/agent)
  --dry-run         Read diagnostics and package metadata; do not repair or install
  --help, -h        Show this help

Requires local Bash/OpenSSH and remote Linux, Python 3.8+, and bash or fish.
The host key must already be trusted. SSH password prompts are disabled.
An apply backs up changed configuration and prints a remote rollback command.
It then uses a second SSH session to verify the ordinary npm update command.
EOF
}

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 2; }
host=example-user@192.0.2.10
mode=apply
ssh_options=(-T -o BatchMode=yes -o StrictHostKeyChecking=yes -o UpdateHostKeys=no
             -o ConnectTimeout=15 -o ServerAliveInterval=15 -o ServerAliveCountMax=3)
while (($#)); do
  case "$1" in
    --help|-h) usage; exit 0 ;;
    --dry-run) mode=dry-run; shift ;;
    --host|--port|--identity)
      (($# >= 2)) && [[ -n $2 ]] || fail "$1 requires a value"
      case "$1" in
        --host) host=$2 ;;
        --port)
          [[ $2 =~ ^[0-9]{1,5}$ ]] && ((10#$2 >= 1 && 10#$2 <= 65535)) || fail 'Port must be 1–65535'
          ssh_options+=(-p "$2") ;;
        --identity) [[ -r $2 ]] || fail "Cannot read identity file: $2"; ssh_options+=(-i "$2") ;;
      esac
      shift 2 ;;
    *) fail "Unknown argument: $1" ;;
  esac
done
[[ $host =~ ^[a-zA-Z0-9_][a-zA-Z0-9_.:@%+-]*$ ]] || fail 'Invalid SSH destination'
command -v ssh >/dev/null || fail 'OpenSSH client is required'

remote_payload() {
  cat <<'PYTHON'
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

HOME_DIR = Path.home()
STATE = HOME_DIR / '.local/state/fix-vps-codex'
REGISTRY = 'https://registry.npmjs.org'
BEGIN = '# >>> fix-vps-codex >>>'
END = '# <<< fix-vps-codex <<<'
mode = sys.argv[1]
env = os.environ.copy()
backup_dir = None


def fail(message):
    raise RuntimeError(message)


def run(args, *, capture=True, check=True, environment=None):
    result = subprocess.run(args, env=environment or env, cwd=HOME_DIR,
                            text=True, capture_output=capture, timeout=300)
    if check and result.returncode:
        # Do not echo arbitrary shell/npm output which can contain credentials.
        codes = ', '.join(sorted(set(re.findall(r'\b(?:EACCES|EPERM|EBADENGINE|ENOTFOUND|ETIMEDOUT|ECONNRESET)\b',
                                               result.stderr or ''))))
        fail('{} failed (exit {}{}). Check npm registry connectivity, file ownership, '
             'and shell configuration.'.format(Path(args[0]).name, result.returncode, ', ' + codes if codes else ''))
    return result


def user_path(path):
    path = Path(path)
    try:
        relative = path.resolve().relative_to(HOME_DIR.resolve())
        return bool(relative.parts)
    except ValueError:
        return False


def writable_tree(path):
    path = Path(path)
    if path.resolve() != HOME_DIR.resolve() and not user_path(path):
        return False
    while not path.exists():
        path = path.parent
    return path.stat().st_uid == os.getuid() and os.access(path, os.W_OK | os.X_OK)


def safe_config(path):
    if not user_path(path) or path.is_symlink():
        fail('Refusing configuration outside your home or a symlink: {}'.format(path))
    if path.exists() and (not path.is_file() or path.stat().st_uid != os.getuid()
                          or not os.access(path, os.W_OK)):
        fail('Configuration must be a writable file owned by you: {}'.format(path))
    if not writable_tree(path.parent):
        fail('Configuration parent is not writable: {}'.format(path.parent))


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read()
    except Exception as exc:
        fail('Network/download failed for {} ({})'.format(url, type(exc).__name__))


def npm_settings(path):
    values = {}
    if path.is_file():
        for line in path.read_text().splitlines():
            match = re.match(r'^\s*(prefix|cache)\s*=\s*(.*?)\s*$', line)
            if match:
                values[match[1]] = os.path.expandvars(match[2].strip('"\''))
    return values


def version_tuple(value):
    match = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)', value.strip())
    return tuple(map(int, match.groups())) if match else (0, 0, 0)


def login_run(shell, command):
    # Fish cursor controls and startup banners may not end in a newline.
    # Put our output on a fresh line without changing or suppressing startup.
    return run([shell, '-lic', "printf '\\n'; " + command])


def shell_environment(shell):
    # Read the environment after interactive login initialization. stdout may
    # contain banners; only consume the explicit JSON marker, never print it.
    keys = ['PATH', 'SHELL', 'XDG_CONFIG_HOME', 'NPM_CONFIG_PREFIX', 'npm_config_prefix',
            'NPM_CONFIG_USERCONFIG', 'npm_config_userconfig', 'NPM_CONFIG_CACHE', 'npm_config_cache',
            'NVM_DIR', 'FNM_DIR']
    code = 'import os,json;print("VPS_CODEX_ENV="+json.dumps({k:os.environ.get(k) for k in ' + repr(keys) + '}))'
    result = login_run(shell, shlex.quote(sys.executable) + ' -c ' + shlex.quote(code))
    records = [line[len('VPS_CODEX_ENV='):] for line in result.stdout.splitlines()
               if line.startswith('VPS_CODEX_ENV=')]
    if len(records) != 1:
        fail('Could not read the login shell environment; inspect shell startup output.')
    for key, value in json.loads(records[0]).items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = value


def npm_get(npm, key):
    return run([str(npm), 'config', 'get', key]).stdout.strip()


def describe(node, npm, prefix):
    print('Remote: {} / {} / user {}'.format(platform.system(), platform.machine(), os.getuid()), flush=True)
    if Path('/etc/os-release').is_file():
        for line in Path('/etc/os-release').read_text().splitlines():
            if line.startswith('PRETTY_NAME='):
                print('OS: ' + line.split('=', 1)[1].strip('"'), flush=True)
    print('Shell: {}'.format(env.get('SHELL', '(unknown)')), flush=True)
    for name, path in [('node', node), ('npm', npm)]:
        version = '(missing)'
        if path and name == 'node':
            result = run([str(path), '--version'], check=False)
            version = result.stdout.strip() if result.returncode == 0 else '(cannot run)'
        elif path:
            manifest = Path(path).resolve().parent.parent / 'package.json'
            if manifest.is_file():
                version = json.loads(manifest.read_text()).get('version', '(unknown)')
        print('{}: {} {}'.format(name, path or '(missing)', version), flush=True)
    print('codex path: {}'.format(shutil.which('codex', path=env.get('PATH')) or '(missing)'), flush=True)
    print('npm prefix (inferred from environment/config; apply checks npm): {}'.format(prefix), flush=True)
    for manager in [HOME_DIR / '.nvm', HOME_DIR / '.local/share/fnm']:
        if manager.is_dir():
            print('Existing runtime manager directory: {}'.format(manager), flush=True)
    for path in [Path(prefix), Path(prefix) / 'lib/node_modules/@openai/codex', HOME_DIR / '.npm']:
        if path.exists():
            info = path.stat()
            print('{}: uid={} mode={} writable={}'.format(path, info.st_uid,
                  oct(stat.S_IMODE(info.st_mode)), os.access(path, os.W_OK)), flush=True)


def download_node():
    arch = {'x86_64': 'x64', 'aarch64': 'arm64'}.get(platform.machine())
    if not arch:
        fail('Automatic Node installation supports Linux x86_64 or aarch64 only.')
    releases = json.loads(fetch('https://nodejs.org/dist/index.json'))
    release = next((r for r in releases if r.get('lts') and 'linux-' + arch in r.get('files', [])), None)
    if not release or not re.fullmatch(r'v\d+\.\d+\.\d+', release['version']):
        fail('No supported LTS Node release found in official metadata.')
    name = 'node-{}-linux-{}'.format(release['version'], arch)
    parent = HOME_DIR / '.local/share/codex-node'
    target = parent / name
    if not writable_tree(parent):
        fail('Cannot install a user-owned runtime at {}'.format(parent))
    url = 'https://nodejs.org/dist/{}/'.format(release['version'])
    sums = fetch(url + 'SHASUMS256.txt').decode()
    filename = name + '.tar.gz'
    expected = next((line.split()[0] for line in sums.splitlines()
                     if len(line.split()) == 2 and line.split()[1] == filename), None)
    if target.exists():
        marker = target / '.archive-sha256'
        if not writable_tree(target) or not marker.is_file() or marker.read_text().strip() != expected:
            fail('Existing runtime was not installed by this helper with the expected checksum: {}'.format(target))
        test_env = {**env, 'PATH': str(target / 'bin') + ':' + env.get('PATH', '')}
        if run([str(target / 'bin/node'), '--version'], environment=test_env).stdout.strip() != release['version']:
            fail('Existing runtime version disagrees with its download metadata.')
        run([str(target / 'bin/npm'), '--version'], environment=test_env)
        return target / 'bin/node', target / 'bin/npm'
    archive = fetch(url + filename)
    if not expected or hashlib.sha256(archive).hexdigest() != expected:
        fail('Node archive checksum mismatch; no configuration was changed.')
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.download-', dir=parent) as staging:
        staging_path = Path(staging)
        with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
            members = tar.getmembers()
            names = [Path(member.name) for member in members]
            if len(names) != len(set(names)):
                fail('Unsafe duplicate member in Node archive.')
            links = {Path(member.name) for member in members if member.issym()}
            for member in members:
                parts = Path(member.name).parts
                if not parts or parts[0] != name or '..' in parts or Path(member.name).is_absolute():
                    fail('Unsafe path in Node archive.')
                if not (member.isdir() or member.isfile() or member.issym()):
                    fail('Unsupported member in Node archive.')
                if any(parent in links for parent in Path(member.name).parents):
                    fail('Unsafe symlink parent in Node archive.')
                if member.issym():
                    destination = (staging_path / member.name).parent / member.linkname
                    try:
                        destination.resolve().relative_to(staging_path / name)
                    except ValueError:
                        fail('Unsafe link in Node archive.')
            # Check against links already extracted, including chained links.
            # This works on Python 3.8, before tar safety filters existed.
            for member in members:
                destination = staging_path / member.name
                try:
                    destination.resolve().relative_to(staging_path / name)
                except ValueError:
                    fail('Unsafe resolved member path in Node archive.')
                tar.extract(member, staging)
            for link in links:
                try:
                    (staging_path / link).resolve().relative_to(staging_path / name)
                except ValueError:
                    fail('Unsafe resolved link in Node archive.')
        staged = staging_path / name
        test_env = {**env, 'PATH': str(staged / 'bin') + ':' + env.get('PATH', '')}
        run([str(staged / 'bin/node'), '--version'], environment=test_env)
        run([str(staged / 'bin/npm'), '--version'], environment=test_env)
        (staged / '.archive-sha256').write_text(expected + '\n')
        staged.rename(target)
    print('Installed user Node {} at {}'.format(release['version'], target), flush=True)
    return target / 'bin/node', target / 'bin/npm'


def write_configs(changes):
    global backup_dir
    changes = {p: text for p, text in changes.items()
               if not p.exists() or p.read_text() != text}
    if not changes:
        return
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    backup_dir = Path(tempfile.mkdtemp(prefix=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-'), dir=STATE))
    records = []
    for index, (path, text) in enumerate(changes.items()):
        safe_config(path)
        saved = backup_dir / str(index)
        exists = path.exists()
        if exists:
            saved.write_bytes(path.read_bytes())
            saved.chmod(0o600)
        records.append({'path': str(path), 'backup': str(saved) if exists else None,
                        'mode': stat.S_IMODE(path.stat().st_mode) if exists else 0o600,
                        'after': hashlib.sha256(text.encode()).hexdigest()})
    restore = '''#!/usr/bin/env python3
import hashlib, os
from pathlib import Path
records = RECORDS
for item in records:
    path = Path(item['path'])
    if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['after']:
        raise SystemExit('Refusing rollback: file changed after repair: ' + str(path))
for item in records:
    path = Path(item['path'])
    if item['backup'] is None:
        path.unlink()
    else:
        path.write_bytes(Path(item['backup']).read_bytes())
        path.chmod(item['mode'])
print('Configuration restored. Reconnect SSH. User-installed packages remain on disk.')
'''.replace('RECORDS', repr(records))
    (backup_dir / 'rollback.py').write_text(restore)
    (backup_dir / 'rollback.py').chmod(0o700)
    print('Rollback on VPS: python3 {}'.format(shlex.quote(str(backup_dir / 'rollback.py'))), flush=True)
    written = []
    try:
        for item, (path, text) in zip(records, changes.items()):
            path.parent.mkdir(parents=True, exist_ok=True)
            written.append(item)
            path.write_text(text)
            path.chmod(item['mode'])
    except Exception:
        for item in reversed(written):
            path = Path(item['path'])
            if item['backup']:
                path.write_bytes(Path(item['backup']).read_bytes())
                path.chmod(item['mode'])
            else:
                path.unlink(missing_ok=True)
        raise


def shell_configs(shell, paths):
    if Path(shell).name == 'fish':
        config_home = Path(env.get('XDG_CONFIG_HOME') or HOME_DIR / '.config')
        files = [config_home / 'fish/config.fish']
        line = 'set -gx PATH {} $PATH'.format(' '.join(shlex.quote(str(p)) for p in paths))
    else:
        profile = next((HOME_DIR / p for p in ['.bash_profile', '.bash_login', '.profile']
                        if (HOME_DIR / p).exists()), HOME_DIR / '.profile')
        files = [profile, HOME_DIR / '.bashrc']
        line = 'export PATH={}:"$PATH"'.format(shlex.quote(':'.join(map(str, paths))))
    changes = {}
    for path in files:
        safe_config(path)
        text = path.read_text() if path.exists() else ''
        if text.count(BEGIN) != text.count(END) or text.count(BEGIN) > 1:
            fail('Malformed managed block in {}'.format(path))
        text, count = re.subn(r'^' + re.escape(BEGIN) + r'\n.*?^' + re.escape(END) + r'(?:\n|$)',
                             '', text, flags=re.S | re.M)
        if BEGIN in text or END in text:
            fail('Malformed managed block in {}'.format(path))
        changes[path] = text.rstrip('\n') + '\n' + BEGIN + '\n' + line + '\n' + END + '\n'
    return changes


def main():
    if sys.version_info < (3, 8) or platform.system() != 'Linux':
        fail('Remote Linux and Python 3.8+ are required.')
    if os.getuid() == 0:
        fail('Connect as your normal VPS user, not root; sudo is not needed.')
    shell = env.get('SHELL', '')
    if Path(shell).name not in ('bash', 'fish') or not Path(shell).is_file():
        fail('Supported login shells are bash and fish; found {}'.format(shell))
    if mode != 'dry-run':
        shell_environment(shell)
    node_name = shutil.which('node', path=env.get('PATH'))
    npm_name = shutil.which('npm', path=env.get('PATH'))
    node = Path(node_name).resolve() if node_name else None
    npm = Path(npm_name).resolve() if npm_name else None
    npmrc = HOME_DIR / '.npmrc'
    settings = npm_settings(npmrc)
    guessed = settings.get('prefix') or (str(node.parent.parent) if node else '/usr')
    prefix = env.get('npm_config_prefix') or env.get('NPM_CONFIG_PREFIX') or guessed
    describe(node, npm, prefix)
    if mode == 'dry-run':
        metadata = json.loads(fetch(REGISTRY + '/@openai%2fcodex/latest'))
        print('Latest Codex: {}; Node requirement: {}'.format(metadata['version'], metadata.get('engines', {}).get('node')), flush=True)
        print('DRY RUN: no repair writes or npm execution. Apply checks the initialized login shell, '
              'reuses compatible tools, repairs the user prefix/PATH, and verifies a normal update.', flush=True)
        return
    if mode == 'verify':
        expected = json.loads((STATE / 'expected.json').read_text())
        codex = shutil.which('codex', path=env.get('PATH'))
        if not codex or Path(codex) != Path(expected['prefix']) / 'bin/codex':
            fail('Fresh SSH PATH selects the wrong Codex: {}. Check aliases/startup PATH. Use the printed rollback if needed.'.format(codex))
        if not npm or npm_get(npm, 'prefix') != expected['prefix']:
            fail('Fresh SSH npm prefix disagrees with the repair; inspect shell/npm configuration.')
        for command in ['codex', 'npm']:
            result = login_run(shell, "printf 'VPS_CODEX_TYPE='; type -t " + command)
            if 'VPS_CODEX_TYPE=file' not in result.stdout.splitlines():
                fail('{} is shadowed by a shell alias/function. Remove the shadowing definition or use rollback.'.format(command))
        # Run the ordinary command through the real shell, including its functions.
        result = login_run(shell, 'npm install -g @openai/codex && codex --version')
        versions = re.findall(r'^codex-cli [^\r\n]+$', result.stdout, re.M)
        if not versions:
            fail('The ordinary update did not report a Codex version.')
        print('SUCCESS: {} updates without sudo in a fresh SSH session ({}).'.format(versions[-1], codex), flush=True)
        return
    for key in ['npm_config_prefix', 'NPM_CONFIG_PREFIX', 'npm_config_userconfig', 'NPM_CONFIG_USERCONFIG',
                'npm_config_cache', 'NPM_CONFIG_CACHE']:
        if env.get(key):
            fail('{} overrides npm configuration. Remove that override from shell startup and retry.'.format(key))
    safe_config(npmrc)
    safe_config(STATE / 'expected.json')
    # Validate shell destinations before any installs; unusual symlinks need review.
    shell_configs(shell, [])
    metadata = json.loads(fetch(REGISTRY + '/@openai%2fcodex/latest'))
    requirement = metadata.get('engines', {}).get('node', '')
    minimum = re.fullmatch(r'>=\s*(\d+)(?:\.(\d+))?(?:\.(\d+))?', requirement)
    if not minimum or not re.fullmatch(r'\d+\.\d+\.\d+', metadata.get('version', '')):
        fail('Unexpected Codex package version/Node requirement; review current official metadata before installing.')
    needed = tuple(int(n or 0) for n in minimum.groups())
    node_result = run([str(node), '--version'], check=False) if node else None
    compatible = node_result and node_result.returncode == 0 and version_tuple(node_result.stdout) >= needed
    npm_ok = npm and run([str(npm), '--version'], check=False).returncode == 0
    if not compatible or not npm_ok:
        print('Node/npm is missing or incompatible; preparing an isolated current LTS runtime.', flush=True)
        node, npm = download_node()
        if version_tuple(run([str(node), '--version']).stdout) < needed:
            fail('Current Node LTS does not meet the Codex requirement; no configuration was changed.')
    env['PATH'] = str(node.parent) + ':' + env.get('PATH', '')
    if Path(npm_get(npm, 'userconfig')) != npmrc:
        fail('npm uses a custom userconfig. Restore the standard ~/.npmrc location before applying.')
    current_prefix = Path(npm_get(npm, 'prefix'))
    print('Effective npm prefix: {}'.format(current_prefix), flush=True)
    runtime_prefix = node.parent.parent
    managed = any(part in str(node) for part in ('/.nvm/', '/fnm/', '/codex-node/'))
    for key in ['NVM_DIR', 'FNM_DIR']:
        if env.get(key):
            try:
                node.relative_to(Path(env[key]).resolve())
                managed = True
            except ValueError:
                pass
    if managed:
        prefix_path = runtime_prefix
    elif writable_tree(current_prefix):
        prefix_path = current_prefix
    else:
        prefix_path = HOME_DIR / '.local/share/codex-npm'
    if not writable_tree(prefix_path):
        fail('Selected npm prefix is not writable and user-owned: {}'.format(prefix_path))
    for path in [prefix_path / 'lib/node_modules/@openai', prefix_path / 'lib/node_modules/@openai/codex',
                 prefix_path / 'bin']:
        if not writable_tree(path):
            fail('Selected package path is not writable and user-owned: {}'.format(path))
    content = npmrc.read_text() if npmrc.exists() else ''
    if managed:
        content = re.sub(r'^\s*prefix\s*=.*\n?', '', content, flags=re.M)
    else:
        content = re.sub(r'^\s*prefix\s*=.*\n?', '', content, flags=re.M)
        content = content.rstrip('\n') + '\nprefix=' + str(prefix_path) + '\n'
    cache = Path(npm_get(npm, 'cache'))
    # Root-owned cache entries can fail npm even when the cache directory is writable.
    bad_cache = not writable_tree(cache)
    if not bad_cache and cache.exists():
        bad_cache = any(p.stat().st_uid != os.getuid() for p in cache.rglob('*') if p.exists())
    if bad_cache:
        cache = HOME_DIR / '.cache/codex-npm'
        if not writable_tree(cache):
            fail('No writable npm cache at {}'.format(cache))
        content = re.sub(r'^\s*cache\s*=.*\n?', '', content, flags=re.M)
        content = content.rstrip('\n') + '\ncache=' + str(cache) + '\n'
    # Install before switching shell/config routing. Temporary flags isolate this
    # install; the second SSH session proves the persistent ordinary command.
    prefix_path.mkdir(parents=True, exist_ok=True)
    install_env = {**env, 'npm_config_cache': str(cache)}
    print('Installing Codex {} into {}'.format(metadata['version'], prefix_path), flush=True)
    run([str(npm), 'install', '-g', '@openai/codex@' + metadata['version'],
         '--prefix', str(prefix_path), '--registry', REGISTRY, '--engine-strict'], environment=install_env)
    binary = prefix_path / 'bin/codex'
    result = run([str(binary), '--version'])
    if not re.search(r'^codex-cli ', result.stdout, re.M):
        fail('Installed Codex did not report its version; shell configuration was not changed.')
    paths = list(dict.fromkeys([prefix_path / 'bin', node.parent]))
    changes = shell_configs(shell, paths)
    if content != (npmrc.read_text() if npmrc.exists() else ''):
        changes[npmrc] = content
    write_configs(changes)
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    (STATE / 'expected.json').write_text(json.dumps({'prefix': str(prefix_path)}))
    print('Repair installed. Verifying through a second SSH session...', flush=True)


try:
    main()
except Exception as exc:
    print('ERROR: {}'.format(exc), file=sys.stderr, flush=True)
    if backup_dir:
        print('Configuration backup: {}'.format(backup_dir), file=sys.stderr, flush=True)
    sys.exit(1)
PYTHON
}

remote_run() {
  local action=$1 status
  # Only this constant action is interpolated into the remote command. Host,
  # port and identity remain separate SSH arguments, never shell program text.
  if remote_payload | ssh "${ssh_options[@]}" "$host" "python3 - $action"; then
    return 0
  else
    status=$?
    if [[ $status == 255 ]]; then
      printf 'ERROR: SSH connection failed for %s (exit %s). Check the error above.\n' "$host" "$status" >&2
      printf 'For an unknown host, verify its fingerprint with your VPS provider and connect normally first.\n' >&2
    else
      printf 'ERROR: Remote %s failed for %s (exit %s). Check the error above.\n' "$action" "$host" "$status" >&2
    fi
    return "$status"
  fi
}

printf 'Codex VPS %s: %s\n' "$mode" "$host"
remote_run "$mode"
if [[ $mode == apply ]]; then
  remote_run verify
fi
