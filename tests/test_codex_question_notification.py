"""Queued questions announce their prompt through the real notification bridge."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_bridge():
    loader = importlib.machinery.SourceFileLoader('question_bridge', str(ROOT / 'scripts/executable_codex-notification-event'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class QuestionNotificationTests(unittest.TestCase):
    A = '11111111-1111-4111-8111-111111111111'
    B = '22222222-2222-4222-8222-222222222222'

    def setUp(self):
        self.bridge = load_bridge()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / 'codex'
        self.path = self.home / 'sessions/rollout-fixture.jsonl'
        self.path.parent.mkdir(parents=True)
        self.meta = {'id': self.A, 'source': 'vscode'}
        self.write_meta()
        (self.home / 'session_index.jsonl').write_text(json.dumps({'id': self.A, 'thread_name': 'Unrelated saved task title'})+'\n')
        env = patch.dict(os.environ, {'CODEX_HOME': str(self.home)})
        env.start()
        self.addCleanup(env.stop)

    def write_meta(self):
        self.path.write_text(json.dumps({'type': 'session_meta', 'payload': self.meta})+'\n')

    def event(self, name='request_user_input_async', questions=None):
        return {'hook_event_name': 'PreToolUse' if name == 'request_user_input' else 'PostToolUse', 'tool_response': json.dumps({'accepted': True}), 'session_id': self.A,
                'transcript_path': str(self.path), 'tool_use_id': 'call-question',
                'tool_name': name, 'tool_input': {'questions': questions if questions is not None else [
                    {'title': 'Should I deploy the change now?', 'options': ['Deploy', 'Keep local']} ]}}

    def dispatch(self, event, enabled=True):
        with patch.object(self.bridge, 'speech_enabled', return_value=enabled), patch.object(self.bridge.subprocess, 'Popen') as spawn:
            self.assertEqual(self.bridge.main([json.dumps(event)]), 0)
            return spawn

    def test_async_question_speaks_prompt_not_task_title_or_options(self):
        spawn = self.dispatch(self.event())
        spawn.assert_called_once()
        self.assertEqual(json.loads(spawn.return_value.stdin.write.call_args.args[0]), 'Codex asks: Should I deploy the change now?')
        self.assertEqual(spawn.call_args.args[0][-1], 'event-play')
        self.assertTrue(spawn.call_args.kwargs['start_new_session'])

    def test_blocking_question_uses_question_field_and_summarizes_context(self):
        spawn = self.dispatch(self.event('request_user_input', [{'id': 'deploy', 'header': 'Deploy', 'question': 'The checks passed. Should I deploy now?', 'options': [{'label': 'Yes', 'description': 'Deploy everything'}]}]))
        spawn.assert_called_once()
        self.assertEqual(json.loads(spawn.return_value.stdin.write.call_args.args[0]), 'Codex asks: Should I deploy now?')

    def test_multiple_questions_form_one_sentence(self):
        spawn = self.dispatch(self.event(questions=[{'title': 'Which voice should I use?'}, {'title': 'Should it play faster?'}]))
        spawn.assert_called_once()
        self.assertEqual(json.loads(spawn.return_value.stdin.write.call_args.args[0]), 'Codex asks: Which voice should I use; Should it play faster?')

    def test_accepted_async_batch_over_three_still_cues_with_bounded_summary(self):
        spawn = self.dispatch(self.event(questions=[{'title': f'Prompt {i}?'} for i in range(1, 5)]))
        spawn.assert_called_once()
        self.assertEqual(json.loads(spawn.return_value.stdin.write.call_args.args[0]),
                         'Codex asks: Prompt 1; Prompt 2; Prompt 3; and 1 more question?')

    def test_json_encoded_input_and_literal_shell_text_remain_safe(self):
        event = self.event(questions=[{'title': 'Use café $(touch /tmp/no-question-shell); `echo yes`?'}])
        event['tool_input'] = json.dumps(event['tool_input'])
        spawn = self.dispatch(event)
        spawn.assert_called_once()
        spoken = json.loads(spawn.return_value.stdin.write.call_args.args[0])
        self.assertEqual(spoken, 'Codex asks: Use café $(touch /tmp/no-question-shell); `echo yes`?')
        self.assertNotIn(spoken, spawn.call_args.args[0])

    def test_summary_has_bound_and_no_controls(self):
        spawn = self.dispatch(self.event(questions=[{'title': 'Which\n\t' + 'configuration option ' * 100 + 'should I choose?'}]))
        spawn.assert_called_once()
        text = json.loads(spawn.return_value.stdin.write.call_args.args[0])
        self.assertLessEqual(len(text), 280)
        self.assertTrue(text.endswith('?'))
        self.assertFalse(any(ord(c) < 32 for c in text))

    def test_blank_malformed_secret_and_unrelated_tools_are_silent(self):
        events = [self.event(questions=[]), self.event(questions=[{'title': ' \n\t '}]),
                  self.event(questions=[{'title': 'What is your password?', 'isSecret': True}]),
                  self.event('exec_command'), self.event('request_user_input', [{'header': 'Only header'}])]
        for data in (None, [], 'not JSON', {'questions': 'bad'}, {'questions': [123]}):
            event = self.event(); event['tool_input'] = data; events.append(event)
        for event in events:
            with self.subTest(event=event): self.dispatch(event).assert_not_called()
        self.dispatch(self.event(), enabled=False).assert_not_called()

    def test_helper_unknown_parent_and_mismatched_identities_are_silent(self):
        for source in ('guardian', 'unknown', {'subagent': {'thread_spawn': {'agent_role': 'worker'}}}):
            self.meta['source'] = source; self.write_meta()
            self.dispatch(self.event()).assert_not_called()
        self.meta['source'] = 'cli'; self.meta['parent_thread_id'] = self.B; self.write_meta()
        self.dispatch(self.event()).assert_not_called()
        del self.meta['parent_thread_id']; self.write_meta()
        for key in ('session_id', 'agent_id'):
            event = self.event(); event[key] = self.B
            self.dispatch(event).assert_not_called()
        event = self.event(); event['transcript_path'] = str(self.home.parent / 'outside.jsonl')
        Path(event['transcript_path']).write_text(self.path.read_text())
        self.dispatch(event).assert_not_called()

    def test_blocking_malformed_schema_is_silent_before_native_rejection(self):
        for question in ({'question': 'Proceed?'}, {'id': 'x', 'header': '', 'question': 'Proceed?'},
                         {'id': 'x', 'header': 'Next', 'question': 'Proceed?', 'options': ['Yes']},
                         {'id': 'x', 'header': 'Next', 'question': 'Proceed?', 'options': [{'label': 'Yes'}]}):
            with self.subTest(question=question):
                self.dispatch(self.event('request_user_input', [question])).assert_not_called()

    def test_async_requires_accepted_post_hook_and_never_announces_twice(self):
        event = self.event()
        event['hook_event_name'] = 'PreToolUse'
        self.dispatch(event).assert_not_called()
        event['hook_event_name'] = 'PostToolUse'
        for response in (None, {}, {'accepted': False}, {'accepted': 1}, 'not JSON', '{"error":"rejected"}'):
            event['tool_response'] = response
            with self.subTest(response=response): self.dispatch(event).assert_not_called()
        event['tool_response'] = {'accepted': True}
        self.dispatch(event).assert_called_once()
        event = self.event('request_user_input', [{'question': 'Proceed?'}])
        event['hook_event_name'] = 'PostToolUse'
        self.dispatch(event).assert_not_called()

    def test_hook_config_matches_both_question_tools_and_preserves_permission_silence(self):
        hooks = json.loads((ROOT / 'dot_codex/hooks.json').read_text())['hooks']
        self.assertEqual(hooks['PreToolUse'][0]['matcher'], '^request_user_input$')
        self.assertEqual(hooks['PostToolUse'][0]['matcher'], '^request_user_input_async$')
        for key in ('PreToolUse', 'PostToolUse'):
            self.assertIn('codex-notification-event', hooks[key][0]['hooks'][0]['command'])
        self.assertNotIn('PermissionRequest', hooks)


class QuestionProbeTests(unittest.TestCase):
    def test_real_cli_question_probe_checks_clip_then_summary_and_silence(self):
        import subprocess
        import sys
        for kind, expected in (('question', 'Should I deploy now'), ('multi-question', 'Which voice should I use; Should it play faster'), ('question-blocking', 'Should I deploy now')):
            with self.subTest(kind=kind):
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/smoke_codex_question_events.py'), '--case', kind, '--plain'], capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(f'PASS {kind}: 2 playback(s)', result.stdout)
                self.assertIn('Spoken: Codex asks: ' + expected + '?', result.stdout)
        for kind in ('question-worker', 'question-empty', 'question-secret'):
            with self.subTest(kind=kind):
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/smoke_codex_question_events.py'), '--case', kind, '--plain'], capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(f'PASS {kind}: 0 playback(s)', result.stdout)


if __name__ == '__main__':
    unittest.main()
