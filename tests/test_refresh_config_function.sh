#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 - "$repo_root" <<'PY'
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

repo = Path(sys.argv[1])
fish = shutil.which('fish')
assert fish, 'fish is required'
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    home = root / 'home'
    bin_dir = root / 'bin'
    bin_dir.mkdir()
    (home / '.codex').mkdir(parents=True)
    (home / '.config/fish').mkdir(parents=True)
    source = root / 'source'
    source.mkdir()
    codex = source / 'config.toml'
    gitconfig = source / 'dot_gitconfig.tmpl'
    codex.write_text('model = "reviewed"\n')
    gitconfig.write_text('[user]\n name = {{ .gitName }}\n')
    (home / '.codex/config.toml').write_text('model = "PRIVATE-LIVE-VALUE"\n')
    (home / '.gitconfig').write_text('[user]\n name = PRIVATE-LIVE-VALUE\n')
    log = root / 'calls'
    (home / '.config/fish/key_abbr.fish').write_text('echo sourced-shortcuts >>$TEST_LOG\n')
    programs = {
        'chezmoi': '''#!/bin/sh
printf 'chezmoi:%s\\n' "$*" >> "$TEST_LOG"
if [ "$1" = source-path ]; then printf '%s\\n' "$TEST_SOURCE"; fi
if [ "${TEST_SLOW_APPLY:-0}" = 1 ]; then sleep 11; fi
if [ "${TEST_APPLY_FAIL:-0}" = 1 ]; then
 printf '%s\\n' 'private.txt has changed since chezmoi last wrote it' >&2
 exit 9
fi
''',
        'snapshot-codex-config': '#!/bin/sh\necho snapshot >>"$TEST_LOG"\nexit 8\n',
        'sync-shortcuts': '#!/bin/sh\necho sync-shortcuts >>"$TEST_LOG"\n',
    }
    for name, content in programs.items():
        program = bin_dir / name
        program.write_text(content)
        program.chmod(0o755)
    env = dict(os.environ, HOME=str(home), PATH=f'{bin_dir}:{os.environ["PATH"]}',
               TEST_LOG=str(log), TEST_SOURCE=str(codex))
    def run(entrypoint, **extra):
        log.write_text('')
        return subprocess.run([fish, '--no-config', '-c',
            f"set -p fish_function_path '{repo}/dot_config/fish/functions'; {entrypoint}"],
            env=dict(env, **extra), capture_output=True, text=True)
    for entrypoint in ('refresh-config', 'refresh-config-task'):
        result = run(entrypoint)
        assert result.returncode == 0, result.stderr
        assert 'REFRESH COMPLETE' in result.stdout, result.stdout
        assert codex.read_text() == 'model = "reviewed"\n'
        assert gitconfig.read_text() == '[user]\n name = {{ .gitName }}\n'
        calls = log.read_text()
        assert 'snapshot' not in calls, calls
        assert 'source-path' not in calls, calls
        assert 'chezmoi:add' not in calls, calls
        assert '--force' not in calls, calls
        assert 'chezmoi:apply --exclude scripts,externals,remove --no-tty' in calls, calls
        assert 'sync-shortcuts' in calls and 'sourced-shortcuts' in calls, calls
        failed = run(entrypoint, TEST_APPLY_FAIL='1')
        assert failed.returncode == 9, failed
        calls = log.read_text()
        assert calls.count('chezmoi:apply') == 1, calls
        assert 'chezmoi:add' not in calls and 'sync-shortcuts' not in calls, calls
        assert 'private.txt' not in failed.stderr, failed.stderr
        plain = run(entrypoint, CLI_PLAIN='1')
        assert plain.returncode == 0 and plain.stdout.isascii() and plain.stderr.isascii(), plain
    slow = run('refresh-config', TEST_SLOW_APPLY='1')
    assert slow.returncode == 0, slow.stderr
    assert 'elapsed 10s' in slow.stderr, slow.stderr
    assert 'PRIVATE-LIVE-VALUE' not in slow.stderr
    chezmoi = shutil.which('chezmoi')
    assert chezmoi, 'chezmoi is required'
    real_source = root / 'real-source'
    real_source.mkdir()
    (real_source / 'dot_reviewed').write_text('reviewed configuration\n')
    (real_source / 'run_install.sh').write_text('#!/bin/sh\ntouch "' + str(root / 'installer-ran') + '"\n')
    (real_source / '.chezmoiexternal.toml').write_text(
        '["external-must-not-download"]\n type = "file"\n url = "http://127.0.0.1:1/never"\n')
    live = root / 'real-home'
    live.mkdir()
    (live / 'keep-this').write_text('keep me\n')
    (real_source / '.chezmoiremove').write_text('keep-this\n')
    actual = subprocess.run([chezmoi, '--config', str(root / 'isolated.toml'),
        '--source', str(real_source), '--destination', str(live),
        '--cache', str(root / 'cache'), '--persistent-state', str(root / 'state.db'),
        'apply', '--exclude', 'scripts,externals,remove', '--no-tty'],
        env=dict(os.environ, HOME=str(live)), capture_output=True, text=True)
    assert actual.returncode == 0, actual.stderr
    assert (live / '.reviewed').read_text() == 'reviewed configuration\n'
    assert (live / 'keep-this').read_text() == 'keep me\n'
    assert not (root / 'installer-ran').exists()
    assert not (live / 'external-must-not-download').exists()
print('✅ Refresh isolation, conflict refusal, and installed chezmoi exclusions verified.')
PY
