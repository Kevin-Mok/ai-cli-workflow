#!/usr/bin/env python3
"""Keep staged authored files under 5,000 estimated tokens, or non-growing."""
import argparse
import fnmatch
import json
import os
import re
from pathlib import Path, PurePosixPath
import subprocess
import sys

LIMIT = 20000
CONFIG = Path(__file__).resolve().parents[1] / 'config/file-size-guard.json'


def git(*args, input=None):
    return subprocess.run(['git', *args], input=input, capture_output=True,
                          check=True).stdout


def tree(revision=None):
    if revision:
        records = git('ls-tree', '-rz', revision).split(b'\0')
    else:
        records = git('ls-files', '--stage', '-z').split(b'\0')
    entries = {}
    for record in filter(None, records):
        meta, path = record.split(b'\t', 1)
        mode, kind_or_oid, oid_or_stage = meta.split()
        if not revision and oid_or_stage != b'0':
            raise ValueError('Resolve unmerged index entries before committing.')
        entries[os.fsdecode(path)] = (mode, oid_or_stage if revision else kind_or_oid)
    return entries


def exemptions(entries, config):
    parents = set()
    for path, (mode, _) in entries.items():
        parent = str(PurePosixPath(path).parent)
        if (mode in (b'100644', b'100755') and parent != '.'
                and PurePosixPath(path).name in config['upstream_markers']
                and (PurePosixPath(path).name == 'SOURCE.md'
                     or any(fnmatch.fnmatchcase(parent, pattern) for pattern in config['upstream_globs']))):
            parents.add(parent + '/')
    return parents


def skipped(path, content, config, upstream, attributed):
    parts = PurePosixPath(path).parts
    # Match globs both at the repo root and within nested dependency/data trees.
    suffixes = ['/'.join(parts[i:]) for i in range(len(parts))]
    return (path in attributed or content.startswith(b'version https://git-lfs.github.com/spec/v1\n')
            or b'\0' in content[:8000]
            or any(path.startswith(parent) for parent in upstream)
            or any(fnmatch.fnmatchcase(suffix, pattern)
                   for suffix in suffixes for pattern in config['skip_globs'])
            or any(marker.encode() in line
                   for line in content[:2000].splitlines()
                   if re.match(rb'^\s*(#|//|/\*|\*|<!--|--|;)', line)
                   for marker in config['generated_markers']))


def attributed_paths(entries, report=False):
    if not entries:
        return set()
    attrs = git('check-attr', '--source=HEAD' if report else '--cached', '-z', '--stdin', 'filter', 'diff',
                input=b'\0'.join(os.fsencode(path) for path in entries) + b'\0').split(b'\0')
    return {os.fsdecode(attrs[i]) for i in range(0, len(attrs) - 1, 3)
            if (attrs[i + 1:i + 3] == [b'filter', b'lfs']
                or attrs[i + 1:i + 3] == [b'diff', b'unset'])}


def tokens(size):
    return f'{size / 4:,.2f}'.rstrip('0').rstrip('.')


def inspect(report=False):
    config = json.loads(CONFIG.read_text())
    if not isinstance(config, dict) or any(
            not isinstance(config.get(key), list) or
            any(not isinstance(item, str) for item in config[key])
            for key in ('skip_globs', 'upstream_globs', 'upstream_markers', 'generated_markers')):
        raise ValueError('Guard patterns and markers must be lists of strings.')
    ceilings = config.get('grandfathered_max_bytes', {})
    if not isinstance(ceilings, dict) or any(
            type(value) is not int or value < LIMIT for value in ceilings.values()):
        raise ValueError('Grandfathered ceilings must be integer byte limits of at least 20,000.')
    head_exists = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'],
                                 capture_output=True).returncode == 0
    head = tree('HEAD') if head_exists else {}
    entries = head if report else tree()
    upstream = exemptions(entries, config)
    attributed = attributed_paths(entries, report)
    old_paths = {}
    if head_exists and not report:
        changes = git('diff', '--cached', '--name-status', '-z', '--find-renames',
                      '--diff-filter=ACMRT', 'HEAD', '--').split(b'\0')
        i = 0
        while i < len(changes) - 1:
            status, path = changes[i:i + 2]
            i += 2
            if status.startswith((b'R', b'C')):
                new_path = changes[i]
                i += 1
                old_paths[os.fsdecode(new_path)] = os.fsdecode(path)
            else:
                old_paths[os.fsdecode(path)] = os.fsdecode(path)
    elif not report:
        old_paths = {path: path for path in entries}
    rows = []
    for path, (mode, oid) in entries.items():
        if mode not in (b'100644', b'100755') or (not report and path not in old_paths):
            continue
        size = int(git('cat-file', '-s', oid))
        if size <= LIMIT:
            continue
        content = git('cat-file', 'blob', oid)
        if skipped(path, content, config, upstream, attributed):
            continue
        old = head.get(old_paths.get(path, path))
        before = int(git('cat-file', '-s', old[1])) if old and old[0] in (b'100644', b'100755') else 0
        limit = ceilings.get(path, LIMIT) if before else LIMIT
        if report or (size > before and size > limit):
            rows.append((size, path, size - before, limit))
    return sorted(rows, key=lambda row: (-row[0], row[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plain', action='store_true', help='ASCII output')
    parser.add_argument('--report', action='store_true', help='Count eligible HEAD files and show the ten largest')
    args = parser.parse_args()
    plain = args.plain or os.environ.get('CLI_PLAIN') == '1'
    try:
        rows = inspect(args.report)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(('Error: ' if plain else '❌ ') + 'File-size guard could not inspect Git blobs. '
              'Check Git/index state and config/file-size-guard.json. ' + type(exc).__name__, file=sys.stderr)
        return 2
    if args.report:
        print(('Report: ' if plain else '📏 ') + f'{len(rows)} eligible tracked files exceed 5,000 tokens (HEAD).')
        for size, path, _, _ in rows[:10]:
            print(f'{size:>9,} bytes  {tokens(size):>12} tokens  {json.dumps(path, ensure_ascii=False)}')
        return 0
    if not rows:
        return 0
    print(('Blocked: ' if plain else '🛑 ') + 'Staged file-size guard (bytes / 4; limit 5,000 tokens):', file=sys.stderr)
    for size, path, growth, limit in rows:
        print(f'  {json.dumps(path, ensure_ascii=False)}: {tokens(size)} tokens; '
              f'limit {tokens(limit)} tokens; '
              f'growth +{tokens(growth)} tokens (+{growth:,} bytes); '
              f'split into at least {(size + LIMIT - 1) // LIMIT} files', file=sys.stderr)
    print('Steps: group by responsibility; keep each new module under 5,000 tokens; '
          'move code verbatim; leave the original as a thin re-exporting entry point; run tests.', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
