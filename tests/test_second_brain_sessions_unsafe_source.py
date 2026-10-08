"""Malformed transcripts must never permit uncertain privacy separation."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from second_brain import sessions
from second_brain.session_digest_input import parse

SUMMARY = {'title': 'Synthetic work', 'goal': 'Verify fixture', 'intentions': [],
           'accomplishments': ['Reported progress'], 'remaining': [], 'blockers': [],
           'verification': [], 'checks': [{'key': 'review-fixture', 'text': 'Review output'}]}


class UnsafeSourceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.home = self.root / 'codex'
        (self.home / 'sessions').mkdir(parents=True)
        self.source = self.home / 'sessions' / 'fixture.jsonl'
        rows = [
            {'type': 'session_meta', 'timestamp': '2026-10-07T16:00:00Z',
             'payload': {'id': '00000000-0000-0000-0000-000000000001', 'cwd': '/fixture'}},
            {'type': 'event_msg', 'payload': {'type': 'agent_message',
             'message': 'Reported work requiring review'}}]
        self.source.write_text(''.join(json.dumps(row) + '\n' for row in rows))
        env = patch.dict(os.environ, {'CODEX_HOME': str(self.home),
            'XDG_STATE_HOME': str(self.root / 'state'),
            'SECOND_BRAIN_NOW': '2026-10-07T16:00:00-04:00'})
        env.start()
        self.addCleanup(env.stop)

    def append_malformed_private_tool(self):
        with self.source.open('a') as stream:
            stream.write('{"type":"response_item","payload":{"type":"function_call",'
                         '"arguments":"read /home/example/coding/personal-context/brief.md"\n')

    def test_malformed_private_invocation_excludes_entire_input(self):
        self.append_malformed_private_tool()
        result = parse(self.source, self.home)
        self.assertEqual(result['status'], 'skipped')
        self.assertEqual(result['reason'], 'unsafe_source')
        self.assertEqual(result['dialogue'], '')
        self.assertEqual(result['id'], '')
        self.assertEqual(result['cwd'], '')
        self.assertEqual(result['source'], '')

    def test_malformed_append_withdraws_previous_summary_and_checks_without_inference(self):
        with patch.object(sessions, 'infer', return_value=SUMMARY):
            first = sessions.refresh()
        self.assertEqual(first['pending_count'], 1)
        self.append_malformed_private_tool()
        with patch.object(sessions, 'infer') as infer:
            second = sessions.refresh()
        infer.assert_not_called()
        self.assertEqual(second['pending_count'], 0)
        self.assertEqual(second['sessions'][0]['status'], 'skipped')
        self.assertEqual(second['sessions'][0]['reason'], 'unsafe_source')
        self.assertIsNone(second['sessions'][0]['summary'])
        self.assertEqual(second['sessions'][0]['checks'], [])


if __name__ == '__main__':
    unittest.main()
