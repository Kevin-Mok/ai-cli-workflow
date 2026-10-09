#!/usr/bin/env python3
"""Check Redshift shortcuts in a tracked, installed, or running i3 config."""
import argparse
import json
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
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
expected = [(str(n), str(1200 + (n - 1) * 600)) for n in range(1, 10)]
actual = re.findall(r'^bindsym \$mod\+Mod4\+([0-9]) exec redshift -x && redshift -O (\d+)$', text, re.M)
if actual != expected:
    raise SystemExit(f'FAIL: {label}: expected {expected}; found {actual}')
for key in ('0', 'grave'):
    if not re.search(rf'^bindsym \$mod\+Mod4\+{key} exec redshift -x$', text, re.M):
        raise SystemExit(f'FAIL: {label}: {key} must reset the filter')
print(f'PASS: {label}: 1–9 = 1200–6000 K; 0/grave reset')
