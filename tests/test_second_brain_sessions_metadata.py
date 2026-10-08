"""Metadata-first queue migration, invalidation and privacy acceptance cases."""
import json
import os
import unittest
from unittest.mock import patch

import test_second_brain_sessions as fixtures

sessions = fixtures.sessions


class MetadataFirstDigestTests(unittest.TestCase):
    setUp = fixtures.DigestTests.setUp
    tearDown = fixtures.DigestTests.tearDown
    fake = fixtures.DigestTests.fake
    source = fixtures.DigestTests.source

    def test_version_one_migrates_without_losing_dispositions_or_summaries(self):
        self.source()
        report = sessions.refresh()
        check = report['open_checks'][0]['id']
        sessions.resolve({'schema_version': 1, 'check_id': check,
                          'disposition': 'dismissed', 'confirmed': True})
        state_path = self.base / 'state' / 'second-brain' / 'sessions' / 'state.json'
        old = json.loads(state_path.read_text())
        old['schema_version'] = 1
        old.pop('fingerprints')
        old.pop('screened')
        old.pop('summary_hashes')
        old.pop('background_refreshed_at')
        state_path.write_text(json.dumps(old))
        before = next(iter(old['sessions'].values()))
        self.assertEqual(sessions.metadata()['pending_count'], 0)
        report = sessions.refresh(limit=1)
        after = report['sessions'][0]
        self.assertEqual(after['summary'], before['summary'])
        self.assertEqual(after['checks'], before['checks'])
        self.assertEqual(report['model_calls'], 0)
        self.assertEqual(json.loads(state_path.read_text())['schema_version'], 3)

    def test_old_source_changes_with_restored_mtime_are_processed(self):
        source = self.source(date='2026-09-01T12:00:00Z')
        os.utime(source, (1, 1))
        self.assertEqual(sessions.refresh()['model_calls'], 0)
        before = source.stat()
        source.write_bytes(source.read_bytes().replace(b'Build feature', b'Check feature'))
        os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))
        self.assertEqual(source.stat().st_size, before.st_size)
        self.assertEqual(source.stat().st_mtime_ns, before.st_mtime_ns)
        self.assertEqual(sessions.refresh(limit=1)['model_calls'], 1)

    def test_changed_private_source_withdraws_prior_summary_once_screened(self):
        private = self.source('z-private')
        initial = sessions.refresh(limit=1)
        old_key = initial['sessions'][0]['key']
        old_check = initial['open_checks'][0]['id']
        self.source('a-before')
        with private.open('a') as stream:
            stream.write(json.dumps({'type': 'event_msg', 'payload': {
                'type': 'user_message', 'message': '$personal-context discuss private matters'}}) + '\n')
        report = sessions.refresh(limit=1)
        pending = next(entry for entry in report['sessions'] if entry['key'] == old_key)
        self.assertEqual(pending['status'], 'stale')
        self.assertEqual(pending['reason'], 'changed_source')
        self.assertIsNotNone(pending['summary'])
        self.assertEqual(pending['checks'][0]['id'], old_check)
        state_path = self.base / 'state' / 'second-brain' / 'sessions' / 'state.json'
        persisted = state_path.read_text()
        self.assertNotIn('private matters', persisted)
        self.assertNotIn('$personal-context', persisted)
        retained = json.loads(persisted)['sessions'][old_key]
        self.assertEqual(retained['checks'][0]['id'], old_check)
        report = sessions.refresh(limit=1)
        self.assertEqual(report['model_calls'], 0)
        excluded = next(entry for entry in report['sessions'] if entry['key'] == old_key)
        self.assertEqual(excluded['status'], 'skipped')
        self.assertEqual(excluded['reason'], 'private_context')
        self.assertIsNone(excluded['summary'])
        self.assertEqual(excluded['checks'], [])

    def test_changed_unscreened_source_keeps_previously_screened_native_title(self):
        source = self.source('z-private')
        index = self.home / 'session_index.jsonl'
        sid = '00000000-0000-0000-0000-000000000001'
        index.write_text(json.dumps({'id': sid, 'thread_name': 'Safe work title'}) + '\n')
        initial = sessions.refresh(limit=1)
        old_key = initial['sessions'][0]['key']
        preceding = self.source('a-before')
        preceding.write_text(preceding.read_text().replace(sid, sid[:-1] + '2'))
        index.write_text(json.dumps({'id': sid, 'thread_name': 'PRIVATE_CONTEXT_TITLE'}) + '\n')
        with source.open('a') as stream:
            stream.write(json.dumps({'type': 'event_msg', 'payload': {
                'type': 'user_message', 'message': '$personal-context discuss private matters'}}) + '\n')
        report = sessions.refresh(limit=1)
        pending = next(entry for entry in report['sessions'] if entry['key'] == old_key)
        self.assertEqual(pending['title'], 'Safe work title')
        state_path = self.base / 'state' / 'second-brain' / 'sessions' / 'state.json'
        self.assertNotIn('PRIVATE_CONTEXT_TITLE', state_path.read_text())
        report = sessions.refresh(limit=1)
        excluded = next(entry for entry in report['sessions'] if entry['key'] == old_key)
        self.assertEqual(excluded['title'], '')
        self.assertEqual(excluded['reason'], 'private_context')

    def test_initial_window_uses_native_activity_despite_recent_filesystem_mtime(self):
        source = self.source(date='2026-09-01T12:00:00Z')
        report = sessions.refresh(limit=1)
        self.assertEqual(report['model_calls'], 0)
        self.assertFalse(any(entry['summary'] for entry in report['sessions']))
        # A later actual content change is eligible after the initial scan.
        with source.open('a') as stream:
            stream.write(json.dumps({'type': 'event_msg', 'payload': {
                'type': 'user_message', 'message': 'New work reported after initial scan'}}) + '\n')
        self.assertEqual(sessions.refresh(limit=1)['model_calls'], 1)

    def test_initial_queued_activity_window_keeps_its_original_cutoff(self):
        self.source('a-first', date='2026-10-07T12:00:00Z')
        self.source('b-later', date='2026-10-03T12:00:00Z')
        first = sessions.refresh(limit=1)
        self.assertEqual(first['model_calls'], 1)
        self.assertEqual(first['backlog_count'], 1)
        with patch.dict(os.environ, {'SECOND_BRAIN_NOW': '2026-11-07T16:00:00-05:00'}):
            second = sessions.refresh(limit=1)
        self.assertEqual(second['model_calls'], 1)
        self.assertEqual(second['backlog_count'], 0)

    def test_failed_source_retries_after_untouched_queue_work(self):
        self.source('a-first')
        self.source('b-second')
        with patch.object(sessions, 'infer', side_effect=sessions.InferenceError('authentication')):
            first = sessions.refresh(limit=1)
        self.assertEqual(first['model_calls'], 1)
        failed_key = next(entry['key'] for entry in first['sessions'] if entry['status'] == 'failed')
        second = sessions.refresh(limit=1)
        remaining_failed = next(entry for entry in second['sessions'] if entry['key'] == failed_key)
        self.assertEqual(remaining_failed['status'], 'failed')
        self.assertEqual(second['backlog_count'], 1)
        self.assertEqual(len([entry for entry in second['sessions'] if entry['status'] == 'ready']), 1)


if __name__ == '__main__':
    unittest.main()
