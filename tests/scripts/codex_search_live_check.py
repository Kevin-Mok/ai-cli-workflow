#!/usr/bin/env python3
"""Interactive synthetic smoke fixture; no private conversation data is copied."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

cli = argparse.ArgumentParser(description='Check printed search/picker against disposable synthetic sessions; no sudo.')
cli.add_argument('--fzf', help='fzf binary path, e.g. one extracted under /tmp')
cli.add_argument('--real-resume', action='store_true', help='open synthetic history in the real Codex CLI; do not send a prompt')
args = cli.parse_args()
root = Path(__file__).resolve().parents[2]
sid = '00000000-0000-4000-8000-000000000001'
with tempfile.TemporaryDirectory(prefix='codex-search-live-') as temporary:
    base = Path(temporary)
    home = base / 'codex'
    sessions = home / 'sessions/2026/10/01'
    sessions.mkdir(parents=True)
    project = base / 'project with spaces'
    project.mkdir()
    rows = [
        {'timestamp': '2026-10-01T12:00:00Z', 'type': 'session_meta', 'payload': {
            'id': sid, 'session_id': sid, 'timestamp': '2026-10-01T12:00:00Z', 'cwd': str(project),
            'originator': 'codex_cli_rs', 'cli_version': '0.160.1', 'source': 'cli',
            'model_provider': 'smoke', 'base_instructions': {'text': 'Synthetic smoke session.'}}},
        {'timestamp': '2026-10-01T12:00:01Z', 'type': 'response_item', 'payload': {
            'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'SYNTHETIC search smoke history'}]}},
        {'timestamp': '2026-10-01T12:00:02Z', 'type': 'response_item', 'payload': {
            'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'SYNTHETIC saved reply: cache and directory verified.'}]}},
    ]
    # Codex's interactive history projection also consumes mirrored legacy events.
    rows.insert(1, {'timestamp': '2026-10-01T12:00:01Z', 'type': 'event_msg', 'payload': {
        'type': 'user_message', 'message': 'SYNTHETIC search smoke history', 'images': [], 'local_images': []}})
    rows.append({'timestamp': '2026-10-01T12:00:02Z', 'type': 'event_msg', 'payload': {
        'type': 'agent_message', 'message': 'SYNTHETIC saved reply: cache and directory verified.'}})
    source = sessions / ('rollout-2026-10-01T12-00-00-' + sid + '.jsonl')
    source.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    (home / 'session_index.jsonl').write_text(json.dumps({'id': sid, 'thread_name': 'Synthetic search smoke', 'updated_at': '2026-10-01T12:00:02Z'}) + '\n')
    # A non-authenticated local provider prevents sending anything to a remote model.
    (home / 'config.toml').write_text('''model = "synthetic-smoke"
model_provider = "smoke"
[model_providers.smoke]
name = "Synthetic smoke (no inference)"
base_url = "http://127.0.0.1:9/v1"
wire_api = "responses"
requires_openai_auth = false
[tui]
alternate_screen = "never"
''')
    binaries = base / 'bin'
    binaries.mkdir()
    if args.fzf:
        (binaries / 'fzf').symlink_to(Path(args.fzf).resolve())
    if not args.real_resume:
        stub = binaries / 'codex'
        stub.write_text('#!' + sys.executable + '\nimport json,sys\nprint("RESUME ARGS: " + json.dumps(sys.argv[1:]))\n')
        stub.chmod(0o755)
    env = {**os.environ, 'CODEX_HOME': str(home), 'XDG_CACHE_HOME': str(base / 'cache'),
           'PATH': str(binaries) + os.pathsep + os.environ['PATH']}
    env.pop('CODEX_THREAD_ID', None)
    env.pop('CODEX_INTERNAL_ORIGINATOR_OVERRIDE', None)
    before = source.read_bytes()
    command = [sys.executable, str(root / 'scripts/executable_codex-search'), '-F', 'SYNTHETIC']
    subprocess.run(command, env=env, check=True)
    assert source.read_bytes() == before, 'search modified the synthetic source'
    print('Picker: press Esc to cancel; run again to select. Real resume: inspect /status, then Ctrl-C without sending a prompt.', flush=True)
    code = subprocess.run([command[0], command[1], '--pick', *command[2:]], env=env).returncode
    if not args.real_resume:
        assert source.read_bytes() == before, 'stub picker modified the synthetic source'
    print('Picker/resume exit:', code, '; search left source bytes unchanged')
    sys.exit(code)
