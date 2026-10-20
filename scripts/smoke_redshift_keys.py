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
temperatures = (1200, 1800, 2100, 2400, 2700, 3000, 4800, 5400, 6000)
expected = [(str(n), str(value)) for n, value in enumerate(temperatures, 1)]
actual = re.findall(r'^bindsym \$mod\+Mod4\+([0-9]) exec --no-startup-id ~/scripts/redshift-control set (\d+)$', text, re.M)
if actual != expected:
    raise SystemExit(_cli_message(f'FAIL: {label}: expected {expected}; found {actual}', '❌'))
for key in ('0', 'grave'):
    if not re.search(rf'^bindsym \$mod\+Mod4\+{key} exec --no-startup-id ~/scripts/redshift-control reset$', text, re.M):
        raise SystemExit(_cli_message(f'FAIL: {label}: {key} must reset the filter', '❌'))
for key, step in (('Up', 250), ('Down', -250)):
    binding = f'bindsym Control+$mod+{key} exec --no-startup-id ~/scripts/redshift-control adjust {step}'
    if text.splitlines().count(binding) != 1:
        raise SystemExit(_cli_message(f'FAIL: {label}: missing or duplicate {key} adjustment', '❌'))
print(_cli_message(f'PASS: {label}: 2–6 = 1800, 2100, 2400, 2700, 3000 K; 1/7–9 unchanged; 0/grave reset; Ctrl+Alt+Up/Down = +/-250 K', '✅'))
