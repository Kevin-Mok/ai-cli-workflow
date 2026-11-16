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
    (source / 'dot_reviewed').write_text('repo version before local import\n')
    log = root / 'calls'
    (home / '.config/fish/key_abbr.fish').write_text('echo sourced-shortcuts >>$TEST_LOG\n')
    programs = {
        'chezmoi': '''#!/bin/sh
printf 'chezmoi:%s\\n' "$*" >> "$TEST_LOG"
if [ "$1" = status ] && [ -e "$TEST_SOURCE/dot_config/mimeapps.list" ] && [ -e "$TEST_SOURCE/dot_config/private_mimeapps.list" ]; then
 printf '%s\\n' 'inconsistent MIME source state' >&2
 exit 6
fi
if [ "$1" = status ]; then printf 'M  .reviewed\\n'; fi
if [ "$1" = source-path ]; then
 if [ "$#" -gt 1 ]; then printf '%s\\n' "$TEST_SOURCE/dot_reviewed";
 else printf '%s\\n' "${TEST_SOURCE_OUTPUT-$TEST_SOURCE}"; fi
fi
if [ "${TEST_SLOW_APPLY:-0}" = 1 ]; then sleep 11; fi
if [ "$1" = apply ] && [ "${TEST_APPLY_FAIL:-0}" = 1 ]; then
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
               TEST_LOG=str(log), TEST_SOURCE=str(source), XDG_STATE_HOME=str(home / ".local/state"))
    def run(entrypoint, **extra):
        log.write_text('')
        return subprocess.run([fish, '--no-config', '-c',
            f"set -p fish_function_path '{repo}/dot_config/fish/functions'; {entrypoint}"],
            env=dict(env, **extra), capture_output=True, text=True)
    for invalid_source in ('', '.', str(root / 'missing-source'), str(source) + '\n' + str(source)):
        bad_source = run('refresh-config', TEST_SOURCE_OUTPUT=invalid_source)
        assert bad_source.returncode != 0, 'invalid successful source-path output must stop refresh'
        assert 'source directory' in bad_source.stderr.lower(), bad_source.stderr
        assert 'chezmoi:status' not in log.read_text()
    mime_dir = source / 'dot_config'
    mime_dir.mkdir()
    ordinary = mime_dir / 'mimeapps.list'
    private = mime_dir / 'private_mimeapps.list'
    private.write_text('[Default Applications]\ntext/plain=editor.desktop;\n')
    ordinary.write_bytes(private.read_bytes())
    unsafe_backup = run('refresh-config', XDG_STATE_HOME=str(source / 'state'))
    assert unsafe_backup.returncode != 0, 'backup must not become managed source content'
    assert ordinary.exists() and private.exists()
    assert not list(source.rglob('mimeapps.*/mimeapps.list'))
    state_alias = root / 'state-alias'
    state_alias.symlink_to(source, target_is_directory=True)
    alias_backup = run('refresh-config', XDG_STATE_HOME=str(state_alias))
    assert alias_backup.returncode != 0 and ordinary.exists() and private.exists()
    recovered = run('refresh-config')
    assert recovered.returncode == 0, recovered.stderr
    assert not ordinary.exists(), 'identical ordinary duplicate must leave the source tree'
    assert private.read_text().endswith('text/plain=editor.desktop;\n')
    backups = list((home / '.local/state/refresh-config/backups').glob('mimeapps.*/mimeapps.list'))
    assert len(backups) == 1 and backups[0].read_bytes() == private.read_bytes(), backups
    assert backups[0].parent.stat().st_mode & 0o777 == 0o700
    assert 'duplicate MIME source' in recovered.stderr and str(backups[0]) in recovered.stderr
    ordinary.write_text('different local association\n')
    conflict = run('refresh-config')
    assert conflict.returncode != 0
    assert ordinary.read_text() == 'different local association\n'
    assert private.read_bytes() == backups[0].read_bytes()
    assert 'chezmoi:apply' not in log.read_text()
    assert 'differ' in conflict.stderr.lower(), conflict.stderr
    ordinary.unlink()
    ordinary.symlink_to(private)
    unsafe = run('refresh-config')
    assert unsafe.returncode != 0 and ordinary.is_symlink()
    assert 'chezmoi:apply' not in log.read_text()
    ordinary.unlink()
    private.unlink()
    for entrypoint in ('refresh-config', 'refresh-config-task'):
        result = run(entrypoint)
        assert result.returncode == 0, result.stderr
        assert 'REFRESH COMPLETE' in result.stdout, result.stdout
        assert codex.read_text() == 'model = "reviewed"\n'
        assert gitconfig.read_text() == '[user]\n name = {{ .gitName }}\n'
        calls = log.read_text()
        assert 'snapshot' not in calls, calls
        assert 'chezmoi:re-add --no-tty -- ' in calls, calls
        assert 'chezmoi:add' not in calls, calls
        assert '--force' not in calls, calls
        assert 'chezmoi:apply --exclude scripts,externals,remove --no-tty' in calls, calls
        assert 'sync-shortcuts' in calls and 'sourced-shortcuts' in calls, calls
        failed = run(entrypoint, TEST_APPLY_FAIL='1')
        assert failed.returncode == 9, failed
        calls = log.read_text()
        assert calls.count('chezmoi:apply') == 2, calls
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
    # Real managed-file updates must reach source before the next apply.
    local_update = 'updated directly in the home directory\n'
    (live / '.reviewed').write_text(local_update)
    (live / '.config/fish').mkdir(parents=True)
    (live / '.config/fish/key_abbr.fish').write_text('true\n')
    real_bin = root / 'real-bin'
    real_bin.mkdir()
    import shlex
    globals_ = [chezmoi, '--config', str(root / 'isolated.toml'),
                '--source', str(real_source), '--destination', str(live),
                '--cache', str(root / 'cache'), '--persistent-state', str(root / 'state.db')]
    launcher = real_bin / 'chezmoi'
    launcher.write_text('#!/bin/sh\n'
        'if [ "$1" = apply ]; then\n'
        ' cmp -s "$TEST_REAL_SOURCE/dot_reviewed" "$HOME/.reviewed" || exit 88\n'
        'fi\nexec ' + shlex.join(globals_) + ' "$@"\n')
    launcher.chmod(0o755)
    shutil.copy(bin_dir / 'sync-shortcuts', real_bin / 'sync-shortcuts')
    real_refresh = subprocess.run([fish, '--no-config', '-c',
        f"set -p fish_function_path '{repo}/dot_config/fish/functions'; refresh-config"],
        env=dict(os.environ, HOME=str(live), PATH=f'{real_bin}:{os.environ["PATH"]}',
                 TEST_LOG=str(root / 'real-calls'), TEST_REAL_SOURCE=str(real_source),
                 XDG_STATE_HOME=str(root / 'real-state')),
        capture_output=True, text=True)
    assert real_refresh.returncode == 0, real_refresh.stderr
    assert 'REFRESH COMPLETE' in real_refresh.stdout
    assert (real_source / 'dot_reviewed').read_text() == local_update
    assert (live / '.reviewed').read_text() == local_update
    imported_backups = list((root / 'real-state/refresh-config/backups').glob('local.*/source'))
    assert any(p.read_text() == 'reviewed configuration\n' for p in imported_backups), 'repo content must be backed up before local import'
    # Local changes win while the simultaneously edited repo version remains recoverable.
    (real_source / 'dot_reviewed').write_text('simultaneous repo edit\n')
    (live / '.reviewed').write_text('second local edit\n')
    both_refresh = subprocess.run(real_refresh.args, env=dict(os.environ, HOME=str(live),
        PATH=f'{real_bin}:{os.environ["PATH"]}', TEST_LOG=str(root / 'real-calls'),
        TEST_REAL_SOURCE=str(real_source), XDG_STATE_HOME=str(root / 'real-state')),
        capture_output=True, text=True)
    assert both_refresh.returncode == 0, both_refresh.stderr
    assert (real_source / 'dot_reviewed').read_text() == 'second local edit\n'
    imported_backups = list((root / 'real-state/refresh-config/backups').glob('local.*/source'))
    assert any(p.read_text() == 'simultaneous repo edit\n' for p in imported_backups)
    # Rendered template changes cannot safely replace their portable source.
    template = real_source / 'dot_template.tmpl'
    template.write_text('os={{ .chezmoi.os }}\n')
    subprocess.run(globals_ + ['apply', '--exclude', 'scripts,externals,remove', '--no-tty'],
                   env=dict(os.environ, HOME=str(live)), check=True, capture_output=True)
    (live / '.template').write_text('local template edit\n')
    template_refresh = subprocess.run(real_refresh.args, env=dict(os.environ, HOME=str(live),
        PATH=f'{real_bin}:{os.environ["PATH"]}', TEST_LOG=str(root / 'real-calls'),
        TEST_REAL_SOURCE=str(real_source), XDG_STATE_HOME=str(root / 'real-state')),
        capture_output=True, text=True)
    assert template_refresh.returncode != 0, 'template edits must stop before apply, not silently skip import'
    assert 'template' in template_refresh.stderr.lower()
    assert template.read_text() == 'os={{ .chezmoi.os }}\n'
    assert (live / '.template').read_text() == 'local template edit\n'

print('✅ Refresh isolation, conflict refusal, and installed chezmoi exclusions verified.')
PY
