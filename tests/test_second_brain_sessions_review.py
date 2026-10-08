"""Recent review acceptance: real sources/state; inference alone is simulated."""
import copy
import json
import os
import unittest
from unittest.mock import patch
import test_second_brain_sessions as fixtures

sessions = fixtures.sessions


class RecentReviewTests(unittest.TestCase):
    setUp = fixtures.DigestTests.setUp
    tearDown = fixtures.DigestTests.tearDown
    fake = fixtures.DigestTests.fake

    def source(self, number, date, *, name=None, origin=None, text=None):
        path = fixtures.DigestTests.source(self, name or str(number), text or f'Work {number}',
                                           cwd=f'/project/{number}', date=date)
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        sid = f'00000000-0000-0000-0000-{number:012d}'
        rows[0]['payload']['id'] = sid
        if origin:
            rows[0]['payload'].update(origin)
        path.write_text(''.join(json.dumps(row)+'\n' for row in rows))
        with (self.home/'session_index.jsonl').open('a') as stream:
            stream.write(json.dumps({'id':sid,'thread_name':f'Task {number}'})+'\n')
        return path

    def state(self):
        return json.loads((self.base/'state/second-brain/sessions/state.json').read_text())

    def test_latest_five_without_checks_outrank_old_actionable_backlog(self):
        self.source(1, '2026-10-01T12:00:00Z')
        sessions.refresh(limit=1)
        for number in range(2, 45):
            self.source(number, '2026-10-02T12:00:00Z')
        sessions.refresh(limit=1)  # A real queued backlog already exists.
        for number in range(45, 52):
            self.source(number, f'2026-10-07T{number-30:02d}:00:00Z')
        complete = {**copy.deepcopy(fixtures.SUMMARY), 'remaining':[], 'checks':[]}
        with patch.object(sessions,'infer',return_value=complete):
            result=sessions.review()
        self.assertEqual([entry['title'] for entry in result['sessions']],
                         ['Task 51','Task 50','Task 49','Task 48','Task 47'])
        self.assertEqual(result['pending_count'],0)
        self.assertEqual(result['model_calls'],5)
        self.assertGreater(result['backlog_count'],20)

    def test_native_helpers_and_legacy_guardian_never_occupy_slots(self):
        self.source(1,'2026-10-07T12:00:00Z')
        for number, origin in enumerate([
            {'source':{'subagent':{'thread_spawn':{'parent_thread_id':'parent'}}}},
            {'source':{'subagent':{'other':'guardian'}}},
            {'thread_source':{'kind':'guardian'}},
            {'parent_thread_id':'parent','source':'cli'},
        ],2):
            self.source(number,'2026-10-08T12:00:00Z',origin=origin)
        self.source(6,'2026-10-08T13:00:00Z')
        with (self.home/'session_index.jsonl').open('a') as stream:
            stream.write(json.dumps({'id':'00000000-0000-0000-0000-000000000006',
                                     'thread_name':' Guardian Review '})+'\n')
        result=sessions.review()
        self.assertEqual([entry['title'] for entry in result['sessions']],['Task 1'])
        self.assertEqual(result['model_calls'],1)

    def test_duplicate_ids_and_timezone_order_use_latest_native_activity(self):
        self.source(1,'2026-10-07T12:30:00Z')
        duplicate=self.source(1,'2026-10-07T09:00:00-04:00',name='copy')
        archived=self.home/'archived_sessions'; archived.mkdir()
        duplicate.rename(archived/'copy.jsonl')
        self.source(2,'2026-10-07T12:59:59Z')
        self.source(3,'2026-10-07T14:00:00+02:00')
        result=sessions.review()
        self.assertEqual([entry['title'] for entry in result['sessions']],['Task 1','Task 2','Task 3'])
        self.assertEqual(result['model_calls'],3)

    def test_display_and_inference_budgets_are_independent_and_newest_first(self):
        for number in range(1,8): self.source(number,f'2026-10-07T{number+10}:00:00Z')
        result=sessions.review(limit=3,refresh_limit=1)
        self.assertEqual([entry['title'] for entry in result['sessions']],['Task 7','Task 6','Task 5'])
        self.assertEqual(result['model_calls'],1)
        self.assertIsNotNone(result['sessions'][0]['summary'])
        self.assertIsNone(result['sessions'][1]['summary'])
        result=sessions.review(limit=1,refresh_limit=0)
        self.assertEqual(len(result['sessions']),1)
        self.assertEqual(result['model_calls'],0)
        result=sessions.review(all_sessions=True,refresh_limit=0)
        self.assertEqual(len(result['sessions']),7)

    def test_discovery_cannot_mark_a_stale_recap_fresh_or_lose_resolution(self):
        source=self.source(1,'2026-10-07T12:00:00Z')
        first=sessions.review(); cid=first['open_checks'][0]['id']
        sessions.resolve({'schema_version':1,'check_id':cid,'disposition':'dismissed','confirmed':True})
        with source.open('a') as stream:
            stream.write(json.dumps({'type':'event_msg','timestamp':'2026-10-07T15:00:00Z',
                'payload':{'type':'user_message','message':'New work'}})+'\n')
        zero=sessions.review(refresh_limit=0)
        self.assertEqual(zero['sessions'][0]['status'],'stale')
        self.assertEqual(zero['model_calls'],0)
        refreshed=sessions.review()
        self.assertEqual(refreshed['model_calls'],1)
        self.assertEqual(refreshed['sessions'][0]['checks'][0]['disposition'],'dismissed')
        self.assertEqual(sessions.review()['model_calls'],0)

    def test_unchanged_summaries_and_lifecycle_updates_need_no_inference(self):
        source=self.source(1,'2026-10-07T12:00:00Z')
        sessions.review()
        with patch.object(sessions,'infer',side_effect=AssertionError('unexpected inference')):
            result=sessions.review(); self.assertEqual(result['model_calls'],0)
            with source.open('a') as stream:
                stream.write(json.dumps({'type':'event_msg','timestamp':'2026-10-07T15:00:00Z',
                    'payload':{'type':'task_complete'}})+'\n')
            result=sessions.review()
        self.assertEqual(result['sessions'][0]['last_activity'],'2026-10-07T15:00:00Z')
        self.assertEqual(result['model_calls'],0)

    def test_failure_keeps_stale_recap_and_is_retried(self):
        source=self.source(1,'2026-10-07T12:00:00Z'); before=sessions.review()['sessions'][0]['summary']
        with source.open('a') as stream:
            stream.write(json.dumps({'type':'event_msg','payload':{'type':'user_message','message':'Changed'}})+'\n')
        with patch.object(sessions,'infer',side_effect=sessions.InferenceError('authentication')):
            failed=sessions.review()
        self.assertEqual(failed['sessions'][0]['summary'],before)
        self.assertEqual(failed['sessions'][0]['status'],'failed')
        self.assertEqual(sessions.review()['model_calls'],1)

    def test_private_and_malformed_changes_withdraw_cached_content_even_with_zero_budget(self):
        for number in range(1,4): self.source(number,'2026-10-07T12:00:00Z')
        sessions.review()
        with (self.home/'sessions/1.jsonl').open('a') as stream:
            stream.write(json.dumps({'type':'event_msg','payload':{'type':'user_message',
                'message':'$personal-context private sentinel'}})+'\n')
        with (self.home/'sessions/2.jsonl').open('a') as stream: stream.write('{broken private tool\n')
        result=sessions.review(refresh_limit=0)
        self.assertEqual([entry['title'] for entry in result['sessions']],['Task 3'])
        self.assertNotIn('private sentinel',json.dumps(self.state()))
        excluded=[entry for entry in self.state()['sessions'].values() if entry['status']=='skipped']
        self.assertEqual(len(excluded),2)
        self.assertTrue(all(not entry['summary'] and not entry['checks'] and not entry['title'] for entry in excluded))

    def test_history_is_discovered_without_seven_day_cutoff(self):
        old=self.source(1,'2026-01-01T12:00:00Z'); os.utime(old,(1,1))
        result=sessions.review()
        self.assertEqual(len(result['sessions']),1)
        self.assertEqual(result['model_calls'],1)

    def test_version_two_migration_reuses_summary_and_preserves_disposition(self):
        self.source(1,'2026-10-07T12:00:00Z'); initial=sessions.refresh()
        cid=initial['open_checks'][0]['id']
        sessions.resolve({'schema_version':1,'check_id':cid,'disposition':'checked','confirmed':True})
        path=self.base/'state/second-brain/sessions/state.json'; old=json.loads(path.read_text())
        old={key:old[key] for key in ('schema_version','refreshed_at','seen','fingerprints','sessions','queue','coverage','error')}
        old['schema_version']=2; path.write_text(json.dumps(old))
        result=sessions.review()
        self.assertEqual(result['model_calls'],0)
        self.assertEqual(result['sessions'][0]['checks'][0]['disposition'],'checked')

    def test_private_append_during_another_recap_is_screened_before_display(self):
        cached=self.source(1,'2026-10-07T12:00:00Z'); sessions.review()
        self.source(2,'2026-10-07T15:00:00Z')
        def generate(dialogue, previous):
            with cached.open('a') as stream:
                stream.write(json.dumps({'type':'event_msg','payload':{'type':'user_message',
                    'message':'$personal-context now private'}})+'\n')
            return copy.deepcopy(fixtures.SUMMARY)
        with patch.object(sessions,'infer',side_effect=generate): result=sessions.review()
        self.assertEqual([entry['title'] for entry in result['sessions']],['Task 2'])
        self.assertNotIn('Task 1',json.dumps(self.state()))

    def test_review_discovery_does_not_enroll_old_history_in_background_queue(self):
        old=self.source(1,'2026-01-01T12:00:00Z'); os.utime(old,(1,1))
        sessions.refresh()
        sessions.review(refresh_limit=0)
        self.assertEqual(sessions.refresh()['model_calls'],0)

    def test_cold_review_does_not_change_background_initial_window(self):
        self.source(1,'2026-01-01T12:00:00Z')
        sessions.review(refresh_limit=0)
        self.assertEqual(sessions.refresh()['model_calls'],0)

    def test_archive_move_keeps_recap_check_id_and_dismissal(self):
        source=self.source(1,'2026-10-07T12:00:00Z'); result=sessions.review()
        cid=result['open_checks'][0]['id']
        sessions.resolve({'schema_version':1,'check_id':cid,'disposition':'dismissed','confirmed':True})
        archived=self.home/'archived_sessions'; archived.mkdir(); source.rename(archived/source.name)
        moved=sessions.review()
        self.assertEqual(moved['model_calls'],0)
        self.assertEqual(moved['sessions'][0]['checks'][0]['id'],cid)
        self.assertEqual(moved['sessions'][0]['checks'][0]['disposition'],'dismissed')
        self.assertEqual(sessions.review()['model_calls'],0)
        self.assertEqual(sessions.refresh()['pending_count'],0)

    def test_ambiguous_v2_stale_summary_is_not_certified_fresh(self):
        source=self.source(1,'2026-10-07T12:00:00Z'); sessions.review()
        with source.open('a') as stream:
            stream.write(json.dumps({'type':'event_msg','payload':{'type':'user_message','message':'Changed'}})+'\n')
        sessions.review(refresh_limit=0)
        path=self.base/'state/second-brain/sessions/state.json'; v=json.loads(path.read_text())
        old={key:v[key] for key in ('schema_version','refreshed_at','seen','fingerprints','sessions','queue','coverage','error')}
        old['schema_version']=2
        key=next(iter(old['sessions'])); old['seen'][key]=old['sessions'][key]['hash']
        path.write_text(json.dumps(old))
        result=sessions.review()
        self.assertEqual(result['model_calls'],1)

if __name__=='__main__': unittest.main()
