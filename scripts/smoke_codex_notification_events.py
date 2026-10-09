#!/usr/bin/env python3
"""Probe automatic audio eligibility using isolated events and a silent player."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def _cli_message(text, icon):
    """Decorate human output; CLI_PLAIN=1 keeps legacy scripts undecorated."""
    import os
    import sys
    plain = os.environ.get('CLI_PLAIN') == '1' or '--plain' in sys.argv
    return ('' if plain else icon + ' ') + text

QUESTION_CASES = ('question', 'multi-question', 'question-blocking', 'question-worker', 'question-empty', 'question-secret')
CASES = ('completion', 'worker', 'empty', 'missing', 'unknown', 'ambiguous', 'parent', 'permission', *QUESTION_CASES)
SPOKEN = {'question': 'Codex asks: Should I deploy now?', 'multi-question': 'Codex asks: Which voice should I use; Should it play faster?', 'question-blocking': 'Codex asks: Should I deploy now?'}
IDENTITY = '11111111-1111-4111-8111-111111111111'


def probe(kind: str, source: Path) -> tuple[int, str | None]:
    with tempfile.TemporaryDirectory(prefix='codex-event-smoke-') as directory:
        root = Path(directory)
        codex = root / 'codex'
        sessions = codex / 'sessions'
        sessions.mkdir(parents=True)
        helpers = root / 'helpers'
        helpers.mkdir()
        for name in ('codex-notification-event', 'codex-notification-sound'):
            path = source / name
            if not path.exists():
                path = source / ('executable_' + name)
            shutil.copy2(path, helpers / name)
        config = root / 'config/codex-notification-sound'
        config.mkdir(parents=True)
        clip = root / 'clip.mp3'
        clip.write_bytes(b'fixture; player never decodes audio')
        (config / 'sound.json').write_text(json.dumps({'path': str(clip)}))
        (config / 'speech.json').write_text(json.dumps({'enabled': True}))
        log = root / 'playbacks'
        player = helpers / 'mpv'
        player.write_text('#!' + sys.executable + '\nimport json,os,sys\nfrom pathlib import Path\np=Path(sys.argv[-1])\nrow={"kind":"clip" if p.suffix==".mp3" else "speech", "text":None if p.suffix==".mp3" else p.read_text().strip()}\nwith Path(os.environ["EVENT_SMOKE_LOG"]).open("a") as stream:\n stream.write(json.dumps(row)+"\\n")\n')
        if kind in QUESTION_CASES:
            # Fixture synthesis lets the real player expose spoken content and
            # clip/speech ordering without using a voice model or audio device.
            data = root / 'data/codex-notification-speech'
            python = data / 'venv/bin/python'
            python.parent.mkdir(parents=True)
            python.write_text('#!' + sys.executable + '\nimport sys\nfrom pathlib import Path\nPath(sys.argv[sys.argv.index("--output_file")+1]).write_text(sys.stdin.read())\n')
            python.chmod(0o700)
            model = data / 'voices/en_US-Voice Contributor-high.onnx'
            model.parent.mkdir()
            model.write_bytes(b'fixture')
            model.with_suffix('.onnx.json').write_text('{}')
        player.chmod(0o700)
        meta: dict[str, object] = {'id': IDENTITY, 'source': 'vscode'}
        if kind in ('worker', 'question-worker'):
            meta['source'] = {'subagent': {'thread_spawn': {'parent_thread_id': IDENTITY, 'agent_role': 'worker'}}}
        if kind == 'parent':
            meta['parent_thread_id'] = IDENTITY
        transcript = sessions / 'rollout-fixture.jsonl'
        if kind != 'unknown':
            transcript.write_text(json.dumps({'type': 'session_meta', 'payload': meta}) + '\n')
        if kind == 'ambiguous':
            (sessions / 'duplicate.jsonl').write_text(json.dumps({'type': 'session_meta', 'payload': {'id': IDENTITY, 'source': 'cli'}}) + '\n')
        (codex / 'session_index.jsonl').write_text(json.dumps({'id': IDENTITY, 'thread_name': 'Synthetic user answer'}) + '\n')
        event: dict[str, object] = {'type': 'agent-turn-complete', 'thread-id': IDENTITY, 'last-assistant-message': 'Ready to read.'}
        if kind == 'empty':
            event['last-assistant-message'] = ' \t\n\u00a0\u2003 '
        if kind == 'missing':
            del event['last-assistant-message']
        if kind == 'permission':
            event = {'hook_event_name': 'PermissionRequest', 'transcript_path': str(transcript), 'agent_id': IDENTITY}
        if kind in QUESTION_CASES:
            name = 'request_user_input' if kind == 'question-blocking' else 'request_user_input_async'
            field = 'question' if kind == 'question-blocking' else 'title'
            questions: list[dict[str, object]] = [{field: 'The checks passed. Should I deploy now?', 'options': ['Deploy', 'Keep local']}]
            if kind == 'question-blocking':
                questions = [{'id': 'deploy', 'header': 'Deploy', 'question': 'The checks passed. Should I deploy now?',
                              'options': [{'label': 'Deploy', 'description': 'Apply the change'},
                                          {'label': 'Keep local', 'description': 'Do not deploy'}]}]
            if kind == 'multi-question':
                questions = [{'title': 'Which voice should I use?'}, {'title': 'Should it play faster?'}]
            if kind == 'question-empty':
                questions = [{'title': ' \t\n '}]
            if kind == 'question-secret':
                questions = [{'title': 'What is your password?', 'isSecret': True}]
            event = {'hook_event_name': 'PreToolUse' if name == 'request_user_input' else 'PostToolUse',
                     'tool_response': json.dumps({'accepted': True}), 'session_id': IDENTITY, 'transcript_path': str(transcript),
                     'tool_name': name, 'tool_input': {'questions': questions}, 'tool_use_id': 'synthetic-question'}
        env = {**os.environ, 'CODEX_HOME': str(codex), 'XDG_CONFIG_HOME': str(root / 'config'),
               'XDG_STATE_HOME': str(root / 'state'), 'XDG_DATA_HOME': str(root / 'data'),
               'EVENT_SMOKE_LOG': str(log), 'PATH': str(helpers) + os.pathsep + os.environ.get('PATH', '')}
        result = subprocess.run([sys.executable, str(helpers / 'codex-notification-event')],
                                input=json.dumps(event), env=env, text=True, capture_output=True, timeout=5)
        if result.returncode or result.stdout or result.stderr:
            raise RuntimeError(f'{kind}: bridge exited {result.returncode} or produced unexpected output')
        # Playback detaches. Observe the isolated marker long enough for child
        # startup; positive delivery waits up to five seconds, silence one.
        expected = 2 if kind in SPOKEN else 1 if kind == 'completion' else 0
        deadline = time.monotonic() + (5 if expected else 1)
        rows: list[dict[str, object]] = []
        while time.monotonic() < deadline:
            if log.exists():
                rows = [json.loads(line) for line in log.read_text().splitlines()]
                if expected and len(rows) >= expected:
                    break
            time.sleep(.02)
        spoken = rows[-1].get('text') if rows else None
        if kind in SPOKEN and (len(rows) != 2 or rows[0].get('kind') != 'clip'
                or rows[1].get('kind') != 'speech' or spoken != SPOKEN[kind]):
            raise RuntimeError(f'{kind}: expected clip then exact question sentence, got {rows}')
        return len(rows), spoken if isinstance(spoken, str) else None


def main() -> int:
    parser = argparse.ArgumentParser(description=_cli_message(__doc__, '🎙️'))
    parser.add_argument('--case', choices=('all', *CASES), default='all', help='event scenario (default: all)')
    parser.add_argument('--installed', action='store_true', help='probe copies of ~/scripts handlers instead of checkout sources')
    parser.add_argument('--plain', action='store_true', help='use ASCII output')
    args = parser.parse_args()
    args.plain = args.plain or os.environ.get("CLI_PLAIN") == "1"
    source = Path.home() / 'scripts' if args.installed else Path(__file__).resolve().parent
    cases = CASES if args.case == 'all' else (args.case,)
    try:
        for kind in cases:
            print(f'{"" if args.plain else "🔎 "}Checking {kind} (silent isolated player)...', flush=True)
            count, spoken = probe(kind, source)
            expected = 2 if kind in SPOKEN else 1 if kind == 'completion' else 0
            if count != expected:
                print(('' if args.plain else '❌ ') + f'FAIL {kind}: {count} playback(s); expected {expected}', file=sys.stderr)
                return 1
            print(f'{"" if args.plain else "✅ "}PASS {kind}: {count} playback(s)', flush=True)
            if spoken:
                print(('' if args.plain else '🗣️ ') + f'Spoken: {spoken}', flush=True)
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(('' if args.plain else '❌ ') + f'Event probe failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
