#!/usr/bin/env python3
"""Demonstrate staged size policy in an isolated temporary Git repository."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

GUARD = Path(__file__).resolve().with_name('file_size_guard.py')


def main():
    plain = '--plain' in sys.argv or os.environ.get('CLI_PLAIN') == '1'
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
    with tempfile.TemporaryDirectory(prefix='file-size-guard-') as folder:
        repo = Path(folder)

        def git(*args):
            subprocess.run(['git', *args], cwd=repo, env=env, check=True, capture_output=True)

        def stage(size):
            (repo / 'code.py').write_bytes(b'x' * size)
            git('add', 'code.py')

        def check(label, expected):
            result = subprocess.run([sys.executable, str(GUARD), '--plain'],
                                    cwd=repo, env=env, capture_output=True, text=True)
            if result.returncode != expected:
                raise RuntimeError(f'{label}: expected exit {expected}, got {result.returncode}: {result.stderr}')
            print(('OK: ' if plain else '✅ ') + label)

        git('init', '-q')
        git('config', 'user.name', 'Guard Smoke')
        git('config', 'user.email', 'smoke@example.invalid')
        for name in ('hooks/pre-commit', 'scripts/install_commit_hook.py',
                     'scripts/file_size_guard.py', 'config/file-size-guard.json'):
            dest = repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(GUARD.parents[1] / name, dest)
        stage(24000)
        check('New oversized staged file blocked', 1)
        (repo / 'code.py').write_bytes(b'small unstaged copy')
        check('Unstaged shrink cannot hide staged growth', 1)
        # Establish the legacy baseline before installing any hook.
        git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture: legacy oversized file')
        privacy = GUARD.with_name('executable_privacy-gate')
        subprocess.run([sys.executable, str(privacy), '--repo', str(repo), 'install', '--plain'],
                       cwd=repo, env=env, check=True, capture_output=True)
        subprocess.run([sys.executable, 'scripts/install_commit_hook.py', '--plain'],
                       cwd=repo, env=env, check=True, capture_output=True)
        stage(22000)
        check('Existing oversized file shrinking allowed', 0)
        stage(24004)
        check('Existing oversized file growing blocked', 1)
        blocked = subprocess.run(['git', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'blocked'],
                                 cwd=repo, env=env, capture_output=True, text=True)
        if blocked.returncode != 1 or 'Staged file-size guard' not in blocked.stderr:
            raise RuntimeError('Installed hook did not reject oversized commit')
        print(('OK: ' if plain else '✅ ') + 'Installed hook rejects a real oversized commit')
        stage(20000)
        (repo / 'data').mkdir()
        (repo / 'data/output.txt').write_bytes(b'x' * 40000)
        git('add', 'data/output.txt')
        check('Exact limit and skipped data allowed', 0)
        git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'allowed')
        print(('OK: ' if plain else '✅ ') + 'Installed hook allows an eligible commit')
        (repo / 'unsafe.txt').write_text('ghp_' + 'a' * 36)
        git('add', 'unsafe.txt')
        blocked = subprocess.run(['git', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'blocked'],
                                 cwd=repo, env=env, capture_output=True)
        if blocked.returncode != 1 or b'Privacy gate BLOCKED' not in blocked.stderr:
            raise RuntimeError('Preserved privacy hook did not reject a secret fixture')
        print(('OK: ' if plain else '✅ ') + 'Preserved privacy hook rejects a synthetic secret')
    return 0


if __name__ == '__main__':
    sys.exit(main())
