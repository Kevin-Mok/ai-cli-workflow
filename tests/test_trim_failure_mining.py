import importlib.util
import json
import tempfile
import unittest
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / 'benchmarks/trim/mine-failures.py'
NOW = datetime(2026, 10, 23, tzinfo=timezone.utc)


def row(kind, payload, timestamp='2026-10-20T12:00:00Z'):
    return {'timestamp': timestamp, 'type': kind, 'payload': payload}


def user(text, response=False, timestamp='2026-10-20T12:00:00Z'):
    payload = ({'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': text}]}
               if response else {'type': 'user_message', 'message': text})
    return row('response_item' if response else 'event_msg', payload, timestamp)


class FailureMiningTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCANNER.exists(), 'aggregate failure scanner is not implemented')
        spec = importlib.util.spec_from_file_location('trim_failure_mining', SCANNER)
        self.miner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.miner)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        (self.home / 'sessions').mkdir()

    def session(self, number, rows, **metadata):
        path = self.home / 'sessions' / f'{number}.jsonl'
        meta = row('session_meta', {'id': f'00000000-0000-4000-8000-{number:012d}', **metadata})
        path.write_text(''.join(json.dumps(item) + '\n' for item in [meta, *rows]))
        return path

    def scan(self):
        return self.miner.scan(self.home, now=NOW, days=60, progress=lambda: None)

    def test_mirrors_do_not_double_count_but_real_repeats_remain(self):
        complaint = 'Stop asking me for permission again.'
        self.session(1, [user(complaint), user(complaint, True), user(complaint), user(complaint, True)])
        report = self.scan()
        result = report['complaints']['repeated_approval']
        self.assertEqual((result['messages'], result['sessions'], result['dates']), (2, 1, 1))
        self.assertEqual(report['coverage']['eligible_user_messages'], 2)
        self.assertFalse(result['frequent'])

    def test_late_private_and_helper_markers_exclude_all_earlier_counts(self):
        complaint = user('Stop asking me for permission.')
        self.session(1, [complaint, user('Use $personal-context now.')])
        self.session(2, [complaint], source={'subagent': 'worker'})
        self.session(3, [complaint, row('response_item', {
            'type': 'function_call', 'name': 'exec_command',
            'arguments': json.dumps({'cmd': 'cat /home/example/coding/personal-context/private.json'})})])
        self.session(4, [complaint, row('response_item', {
            'type': 'agent_message', 'author': '/root',
            'content': [{'type': 'output_text', 'text': 'Using $personal-context now.'}]})])
        report = self.scan()
        self.assertEqual(report['coverage']['eligible_sessions'], 0)
        self.assertEqual(report['exclusions'], {'helper_session': 1, 'private_context': 3})
        self.assertEqual(report['complaints']['repeated_approval']['messages'], 0)

    def test_instruction_context_quotes_and_old_records_are_not_complaints(self):
        complaint = 'Stop asking me for permission.'
        self.session(1, [user('# AGENTS.md instructions\n' + complaint),
                         user('<codex_internal_context source="goal">' + complaint + '</codex_internal_context>'),
                         user('```text\n' + complaint + '\n```'),
                         user('> ' + complaint), user('"' + complaint + '"'),
                         user('Add this instruction: ' + complaint),
                         user(complaint, timestamp='2026-01-01T12:00:00Z'),
                         user('Why do you keep asking me for approval?')])
        report = self.scan()
        self.assertEqual(report['complaints']['repeated_approval']['messages'], 1)
        self.assertEqual(report['coverage']['filtered_user_messages'], 6)
        self.assertEqual(report['coverage']['outside_window_user_messages'], 1)

    def test_unclosed_fences_and_indented_or_single_quoted_lines_are_excluded(self):
        complaint = 'Stop asking me for permission.'
        self.session(1, [user('```text\n' + complaint), user(' > ' + complaint),
                         user("'" + complaint + "'"), user('    ' + complaint)])
        report = self.scan()
        self.assertEqual(report['complaints']['repeated_approval']['messages'], 0)
        self.assertEqual(report['coverage']['filtered_user_messages'], 4)

    def test_incomplete_and_replaced_input_contribute_no_counts(self):
        path = self.session(1, [user('Stop asking me for permission.')])
        with path.open('a') as stream:
            stream.write('{"type":')
        report = self.scan()
        self.assertEqual(report['exclusions'], {'incomplete_source': 1})
        self.assertEqual(report['complaints']['repeated_approval']['messages'], 0)

        path = self.session(1, [user('Stop asking me for permission.')])
        original_reader = self.miner.source_reader

        @contextmanager
        def replacing_reader(source, home):
            with original_reader(source, home) as opened:
                source.unlink()
                source.write_text('replacement\n')
                yield opened

        with patch.object(self.miner, 'source_reader', replacing_reader):
            report = self.scan()
        self.assertEqual(report['exclusions'], {'changed_during_read': 1})
        self.assertEqual(report['complaints']['repeated_approval']['messages'], 0)

    def test_frequent_requires_three_sessions_across_two_dates(self):
        for number, timestamp in enumerate(('2026-10-19T12:00:00Z', '2026-10-20T12:00:00Z', '2026-10-20T13:00:00Z'), 1):
            self.session(number, [user('You overwrote my changes.', timestamp=timestamp)])
        result = self.scan()['complaints']['overwritten_work']
        self.assertEqual((result['messages'], result['sessions'], result['dates'], result['frequent']), (3, 3, 2, True))

    def test_tool_failures_are_separate_candidates_and_never_payload_exports(self):
        secret = 'synthetic-private-token-not-for-export'
        self.session(1, [row('event_msg', {'type': 'exec_command_end', 'exit_code': 1,
                                         'aggregated_output': 'AssertionError ' + secret}),
                         row('response_item', {'type': 'function_call_output',
                                               'output': 'Process exited with code 2\nPermission denied ' + secret}),
                         row('response_item', {'type': 'function_call_output',
                                               'output': json.dumps({'exit_code': 3, 'output': 'No such file ' + secret})})])
        report = self.scan()
        self.assertEqual(report['tool_failures']['candidates'], 3)
        self.assertEqual(report['tool_failures']['taxonomy']['validation_or_assertion'],
                         {'candidates': 1, 'sessions': 1, 'dates': 1})
        self.assertEqual(report['tool_failures']['taxonomy']['permission_or_read_only'],
                         {'candidates': 1, 'sessions': 1, 'dates': 1})
        self.assertEqual(report['tool_failures']['taxonomy']['missing_resource'],
                         {'candidates': 1, 'sessions': 1, 'dates': 1})
        self.assertEqual(report['complaints']['unsupported_completion']['messages'], 0)
        serialized = json.dumps(report)
        self.assertNotIn(secret, serialized)
        self.assertNotIn(str(self.home), serialized)
        self.assertNotIn('00000000-', serialized)

    def test_oversize_symlink_and_long_instructions_fail_closed(self):
        path = self.session(1, [user('Stop asking me for permission.' + ' x' * 4000)])
        (self.home / 'sessions' / 'linked.jsonl').symlink_to(path)
        report = self.scan()
        self.assertEqual(report['exclusions'], {'unsafe_source': 1})
        self.assertEqual(report['coverage']['filtered_user_messages'], 1)
        self.assertEqual(report['complaints']['repeated_approval']['messages'], 0)
        with patch.object(self.miner, 'MAX_SOURCE_BYTES', 32):
            report = self.scan()
        self.assertEqual(report['exclusions'], {'oversized_source': 1, 'unsafe_source': 1})


if __name__ == '__main__':
    unittest.main()
