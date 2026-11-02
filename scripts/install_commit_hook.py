#!/usr/bin/env python3
"""Install the tracked commit gate without replacing other Git hooks."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plain', action='store_true', help='ASCII output')
    args = parser.parse_args()
    plain = args.plain or os.environ.get('CLI_PLAIN') == '1'
    try:
        configured = subprocess.run(['git', 'config', '--get', 'core.hooksPath'],
                                    capture_output=True, check=False)
        if configured.returncode != 1:
            raise ValueError('Resolve existing core.hooksPath configuration before installing.')
        root = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
        common = Path(subprocess.check_output(
            ['git', 'rev-parse', '--path-format=absolute', '--git-common-dir'], text=True).strip())
        source = root / 'hooks/pre-commit'
        if not source.is_file() or not os.access(source, os.X_OK):
            raise ValueError('Tracked hooks/pre-commit is missing or not executable.')
        target = common / 'hooks/pre-commit'
        backup = target.with_name('pre-commit.file-size-previous')
        if target.is_symlink() and target.resolve() == source.resolve():
            pass
        else:
            if backup.exists() or backup.is_symlink():
                raise ValueError('Preserved pre-commit already exists; review the installation locally.')
            if target.is_symlink() or (target.exists() and
                    (not target.is_file() or not os.access(target, os.X_OK))):
                raise ValueError('Existing pre-commit needs manual preservation; nothing replaced.')
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                target.rename(backup)
            try:
                target.symlink_to(source)
            except OSError:
                if backup.exists():
                    backup.rename(target)
                raise
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(('Error: ' if plain else '❌ ') + str(exc), file=sys.stderr)
        return 1
    print(('OK: ' if plain else '✅ ') + 'Commit gate installed; other Git hooks preserved.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
