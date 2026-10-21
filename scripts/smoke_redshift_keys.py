#!/usr/bin/env python3
"""Check Redshift shortcuts in a tracked, installed, or running i3 config."""
import argparse
import json
from pathlib import Path
import re
import subprocess


def _cli_message(text, icon):
    """Decorate human output; CLI_PLAIN=1 keeps legacy scripts undecorated."""
    import os
    import sys
    plain = os.environ.get('CLI_PLAIN') == '1' or '--plain' in sys.argv
    return ('' if plain else icon + ' ') + text

parser = argparse.ArgumentParser(description=_cli_message(__doc__, '🧰'))
parser.add_argument('config', nargs='?', default='dot_config/i3/config.tmpl')
parser.add_argument('--live', action='store_true', help='Check running i3 via IPC')
args = parser.parse_args()
if args.live:
    result = subprocess.run(['i3-msg', '-r', '-t', 'get_config'], check=True,
                            capture_output=True, text=True)
    text = json.loads(result.stdout)['config']
    label = 'running i3'
else:
    text = Path(args.config).expanduser().read_text()
    label = args.config
temperatures = (1800, 2300, 2850, 3350, 3900, 4400, 4950, 5450, 6000, 6500)
expected = [(key, str(value)) for key, value in zip('234567890', temperatures[1:])]
actual = re.findall(r'^bindsym Mod4\+([0-9]) exec --no-startup-id ~/scripts/redshift-control set (\d+)$', text, re.M)
if actual != expected:
    raise SystemExit(_cli_message(f'FAIL: {label}: expected {expected}; found {actual}', '❌'))
for key in ('grave',):
    if not re.search(rf'^bindsym Mod4\+{key} exec --no-startup-id ~/scripts/redshift-control reset$', text, re.M):
        raise SystemExit(_cli_message(f'FAIL: {label}: {key} must reset the filter', '❌'))
for key, step in (('Up', 250), ('Down', -250)):
    binding = f'bindsym Control+$mod+{key} exec --no-startup-id ~/scripts/redshift-control adjust {step}'
    if text.splitlines().count(binding) != 1:
        raise SystemExit(_cli_message(f'FAIL: {label}: missing or duplicate {key} adjustment', '❌'))
for key in '1234567890':
    bindings = re.findall(rf'^bindsym Mod4\+{key} (.+)$', text, re.M)
    expected_action = ('workspace $ws11' if key == '1' else
                       f'exec --no-startup-id ~/scripts/redshift-control set {temperatures[int(key) - 1]}')
    if bindings != [expected_action]:
        raise SystemExit(_cli_message(f'FAIL: {label}: Super+{key} has an incorrect or duplicate action', '❌'))
    workspace = 10 if key == '0' else int(key)
    binding = f'bindsym $mod+{key} workspace $ws{workspace}'
    if text.splitlines().count(binding) != 1:
        raise SystemExit(_cli_message(f'FAIL: {label}: Alt+{key} workspace shortcut changed', '❌'))
if text.splitlines().count('bindsym Mod4+F11 workspace $ws11') != 1:
    raise SystemExit(_cli_message(f'FAIL: {label}: Super+F11 must select workspace 11', '❌'))
for key, command in [(key, f'set {value}') for key, value in zip('1234567890', temperatures)] + [('grave', 'reset')]:
    binding = f'bindsym $mod+Mod4+{key} exec --no-startup-id ~/scripts/redshift-control {command}'
    if text.splitlines().count(binding) != 1:
        raise SystemExit(_cli_message(f'FAIL: {label}: missing or duplicate Alt+Super+{key} preset/reset', '❌'))
print(_cli_message(f'PASS: {label}: Super+1 = workspace 11; Super+2–0 presets preserved; Alt+Super+1–0 = 1800, 2300, 2850, 3350, 3900, 4400, 4950, 5450, 6000, 6500 K; 0 = 6500 K; grave resets both modifiers; Ctrl+Alt+Up/Down = +/-250 K; Alt+digits preserved; Super+F11 = workspace 11', '✅'))
