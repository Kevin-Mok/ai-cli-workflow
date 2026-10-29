#!/usr/bin/env python3
"""Verify colorful i3 workspace labels and existing select/move shortcuts."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('config', nargs='?', default='dot_config/i3/config.tmpl')
parser.add_argument('--live', action='store_true', help='Read running i3 config and workspace identities')
parser.add_argument('--plain', action='store_true', help='Use ASCII output')
args = parser.parse_args()
text = (json.loads(subprocess.check_output(['i3-msg', '-r', '-t', 'get_config'], text=True))['config']
        if args.live else Path(args.config).expanduser().read_text())
labels = dict(re.findall(r'^set \$ws(\d+) "([^"]+)"$', text, re.M))
icons = ('💻', '💻', '🌐', '🧰', '🎥', '💬', '📤', '📚', '📝', '🎵', '🖥️', '🎮', '💻')
errors = []
for number, icon in enumerate(icons, 1):
    if labels.get(str(number)) != f'{number}{icon}':
        errors.append(f'workspace {number} must use compact label {number}{icon}')
for number in (14, 15):
    if labels.get(str(number)) != str(number):
        errors.append(f'workspace {number} changed')
expected = ['bindsym Mod4+1 workspace $ws11', 'bindsym Mod4+F11 workspace $ws11']
for key, number in zip('1234567890', range(1, 11)):
    expected += [f'bindsym $mod+{key} workspace $ws{number}',
                 f'bindsym $mod+Control+{key} move container to workspace $ws{number}; workspace $ws{number}']
for key, number in zip('12345', range(11, 16)):
    expected.append(f'bindsym $mod+Shift+{key} move container to workspace $ws{number}; workspace $ws{number}')
for binding in expected:
    if text.splitlines().count(binding) != 1:
        errors.append(f'missing or duplicate shortcut: {binding}')
if args.live:
    for workspace in json.loads(subprocess.check_output(['i3-msg', '-r', '-t', 'get_workspaces'], text=True)):
        number = str(workspace['num'])
        if number in labels and workspace['name'] != labels[number]:
            errors.append(f'workspace {number} still has a stale name')
plain = args.plain or os.environ.get('CLI_PLAIN') == '1'
if errors:
    raise SystemExit(('' if plain else '❌ ') + '\n'.join(errors))
print(('' if plain else '✅ ') + 'PASS: colorful workspace labels; Alt digits, Super+1/F11 and all number move shortcuts preserved' + ('; live names match' if args.live else ''))
