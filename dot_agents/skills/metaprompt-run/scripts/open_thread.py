#!/usr/bin/env python3
"""Open an already-created Codex thread in its compiler's live Kitty instance."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time
import uuid


class NavigationError(Exception):
    pass


def socket_addresses():
    paths = list(Path('/tmp').glob('kitty-*'))
    inherited = os.environ.get('KITTY_LISTEN_ON', '')
    if inherited.startswith('unix:'):
        paths.insert(0, Path(inherited[5:]))
    addresses = []
    for path in paths:
        try:
            info = path.lstat()
        except OSError:
            continue
        if stat.S_ISSOCK(info.st_mode) and info.st_uid == os.getuid():
            addresses.append('unix:' + str(path))
    return list(dict.fromkeys(addresses))


def kitty_tree(kitten, address):
    try:
        result = subprocess.run([kitten, '@', '--to', address, 'ls'], capture_output=True, text=True, timeout=2)
        data = json.loads(result.stdout) if result.returncode == 0 else None
        return data if isinstance(data, list) else None
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None


def windows(tree):
    for os_window in tree or []:
        for tab in os_window.get('tabs', []):
            for window in tab.get('windows', []):
                yield tab, window


def plain_title(title):
    prefix, space, rest = title.strip().partition(' ')
    if space and len(prefix) == 1 and (0x2800 <= ord(prefix) <= 0x28ff or prefix in '✓✔●✗•'):
        return rest
    return title.strip()


def find_source(kitten, source_title, progress=None):
    matches = []
    addresses = socket_addresses()
    started = last_update = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = pool.map(lambda address: kitty_tree(kitten, address), addresses)
        for index, (address, tree) in enumerate(zip(addresses, results), 1):
            for tab, window in windows(tree):
                if plain_title(window.get('title', '')) == source_title:
                    matches.append((address, tab['id'], window['id']))
            if progress and time.monotonic() - last_update >= 2:
                progress(f'Checked {index}/{len(addresses)} terminal sockets; elapsed {int(time.monotonic() - started)}s')
                last_update = time.monotonic()
    if len(matches) != 1:
        raise NavigationError(f'Found {len(matches)} source windows for {source_title!r}; need exactly one. Keep the compiler conversation open with a unique title; socket access may require the normal sandbox approval.')
    return matches[0]


def has_thread(window, thread_id):
    for process in window.get('foreground_processes', []):
        args = process.get('cmdline', [])
        if any(args[index:index + 2] == ['resume', thread_id] for index in range(len(args) - 1)):
            return True
    return False


def remote(kitten, address, *args):
    try:
        result = subprocess.run([kitten, '@', '--to', address, *args], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise NavigationError(f'Terminal request failed or timed out; inspect existing tabs before retrying: {error}') from error
    if result.returncode:
        raise NavigationError(result.stderr.strip() or 'Kitty rejected the terminal request.')
    return result.stdout.strip()


def launch(kitten, codex, address, tab_id, source_window, cwd, thread_id, progress=None):
    existing = [window['id'] for _, window in windows(kitty_tree(kitten, address)) if has_thread(window, thread_id)]
    if len(existing) > 1:
        raise NavigationError('Multiple tabs already show this thread; no new tab opened.')
    if existing:
        window_id = existing[0]
    else:
        response = remote(kitten, address, 'launch', '--type=tab', '--match', f'id:{tab_id}', '--source-window', f'id:{source_window}', '--cwd', cwd, '--env', 'PATH=' + os.environ.get('PATH', ''), codex, 'resume', thread_id)
        try:
            window_id = int(response)
        except ValueError as error:
            raise NavigationError('Kitty launch returned no window ID; inspect tabs before retrying.') from error
    remote(kitten, address, 'focus-window', '--match', f'id:{window_id}')
    for attempt in range(20):
        for tab, window in windows(kitty_tree(kitten, address)):
            if window['id'] == window_id and tab.get('is_active') and has_thread(window, thread_id):
                return window_id
        if progress and attempt in (4, 9, 14):
            progress(f'Waiting for Codex to attach to window {window_id}; elapsed {(attempt + 1) // 2}s')
        time.sleep(0.5)
    raise NavigationError(f'Window {window_id} opened but its active Codex thread was not verified; do not recreate the task.')


def main():
    parser = argparse.ArgumentParser(description='Open an existing Codex thread in a uniquely identified Kitty source terminal.')
    parser.add_argument('thread_id', type=uuid.UUID)
    parser.add_argument('--source-title', required=True, help='Exact current compiler conversation title, without its activity indicator')
    parser.add_argument('--cwd', required=True, type=Path)
    parser.add_argument('--plain', action='store_true', help='Use ASCII output')
    parser.add_argument('--details', action='store_true', help='Show underlying diagnostics on failure')
    args = parser.parse_args()
    def say(symbol, message):
        print((symbol + ' ' if not args.plain else '') + message, file=sys.stderr, flush=True)
    try:
        kitten, codex = shutil.which('kitten'), shutil.which('codex')
        if not kitten or not codex or not args.cwd.is_dir():
            raise NavigationError('Need installed kitten/codex executables and an existing workspace directory.')
        say('🔎', 'Finding the live source terminal by conversation title…')
        address, tab, window = find_source(kitten, args.source_title, lambda text: say('🔎', text))
        say('↗️', 'Opening the existing execution thread…')
        target = launch(kitten, codex, address, tab, window, str(args.cwd.resolve()), str(args.thread_id), lambda text: say('⏳', text))
        say('✅', f'Opened and verified thread {args.thread_id} in Kitty window {target} via {address}')
        return 0
    except NavigationError as error:
        say('⚠️', 'Tab navigation could not be verified; the existing execution task is preserved. Use --details for the reason.')
        if args.details:
            say('🔎', str(error))
        return 1


if __name__ == '__main__':
    sys.exit(main())
