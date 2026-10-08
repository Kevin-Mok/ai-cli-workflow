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

    def test_five_recent_directories_each_have_their_three_latest_sessions(self):
        for directory in range(1, 7):
            for index in range(1, 5):
                number = directory * 10 + index
                path = self.source(number, f'2026-10-07T{directory+10:02d}:{index:02d}:00Z')
                rows = [json.loads(line) for line in path.read_text().splitlines()]
                rows[0]['payload']['cwd'] = f'/directory/{directory}'
                path.write_text(''.join(json.dumps(row)+'\n' for row in rows))
        result = sessions.review()
        self.assertEqual([entry['title'] for entry in result['sessions']],
                         [f'Task {directory*10+index}' for directory in range(6,1,-1) for index in (4,3,2)])
        self.assertEqual(result['model_calls'], 15)
        self.assertEqual(sessions.review()['model_calls'], 0)
        self.assertEqual(len(sessions.review(limit=1, refresh_limit=0)['sessions']), 3)
        self.assertEqual(len(sessions.review(all_sessions=True, refresh_limit=0)['sessions']), 24)

    def test_inference_uses_global_activity_even_though_display_groups_directories(self):
        for number, date in [(1,'2026-10-07T19:00:00Z'), (2,'2026-10-07T12:00:00Z'),
                             (3,'2026-10-07T18:00:00Z')]:
            path=self.source(number,date)
            if number==2:
                rows=[json.loads(line) for line in path.read_text().splitlines()]
                rows[0]['payload']['cwd']='/project/1'
                path.write_text(''.join(json.dumps(row)+'\n' for row in rows))
        result=sessions.review(limit=2,refresh_limit=2)
        self.assertEqual([entry['title'] for entry in result['sessions']], ['Task 1','Task 2','Task 3'])
        self.assertEqual([entry['summary'] is not None for entry in result['sessions']], [True,False,True])

    def test_public_policy_tool_output_and_skill_read_are_not_private_retrieval(self):
        source=self.source(1,'2026-10-07T12:00:00Z')
        rows=[{'type':'response_item','timestamp':'2026-10-08T15:00:00Z',
               'payload':{'type':'function_call','name':'exec_command','call_id':'public',
                          'arguments':json.dumps({'cmd':'cat /home/example/.agents/skills/personal-context/SKILL.md'})}},
              {'type':'response_item','payload':{'type':'function_call_output','call_id':'public',
                         'output':'Policy: use personal-context automatically; private data lives at /home/example/coding/personal-context'}},
              {'type':'response_item','payload':{'type':'function_call_output','call_id':'code',
                         'output':'PRIVATE_TOOL = personal-context; example private store path'}}]
        with source.open('a') as stream:
            stream.write(''.join(json.dumps(row)+'\n' for row in rows))
        result=sessions.review(refresh_limit=0)
        self.assertEqual(len(result['sessions']),1)
        self.assertEqual(result['sessions'][0]['last_activity'],'2026-10-08T15:00:00Z')
        self.assertEqual(len(self.calls),0)

    def test_private_tool_invocation_still_excludes_session(self):
        source=self.source(1,'2026-10-07T12:00:00Z')
        with source.open('a') as stream:
            stream.write(json.dumps({'type':'response_item','payload':{'type':'function_call',
                'name':'exec_command','arguments':json.dumps({'cmd':'cat /home/example/coding/personal-context/brief.md'})}})+'\n')
        self.assertEqual(sessions.review()['sessions'],[])
        self.assertEqual(len(self.calls),0)

    def test_old_screening_fingerprint_is_revalidated_without_losing_disposition(self):
        self.source(1,'2026-10-07T12:00:00Z'); first=sessions.review()
        cid=first['open_checks'][0]['id']
        sessions.resolve({'schema_version':1,'check_id':cid,'disposition':'checked','confirmed':True})
        path=self.base/'state/second-brain/sessions/state.json'; old=self.state()
        for key,stamp in old['screened'].items(): old['screened'][key]=stamp[-5:]
        path.write_text(json.dumps(old))
        with patch('second_brain.session_review.parse', wraps=sessions.parse) as parse:
            result=sessions.review()
        self.assertTrue(parse.called)
        self.assertEqual(result['model_calls'],0)
        self.assertEqual(result['sessions'][0]['checks'][0]['disposition'],'checked')

    def test_native_root_agent_message_is_dialogue_not_tool_output(self):
        source=self.source(1,'2026-10-07T12:00:00Z')
        with source.open('a') as stream:
            stream.write(json.dumps({'type':'response_item','timestamp':'2026-10-08T15:00:00Z',
                'payload':{'type':'agent_message','author':'/root','content':[
                    {'type':'input_text','text':'Implemented newest directory grouping.'},
                    {'type':'encrypted_content','encrypted_content':'opaque'}]}})+'\n')
        sessions.review()
        self.assertIn('Implemented newest directory grouping.', ''.join(self.calls))
        self.assertNotIn('opaque', ''.join(self.calls))

    def test_private_directory_and_wrapped_private_callable_are_excluded(self):
        source=self.source(1,'2026-10-07T12:00:00Z')
        rows=[json.loads(line) for line in source.read_text().splitlines()]
        rows[0]['payload']['cwd']='/home/example/coding/personal-context'
        source.write_text(''.join(json.dumps(row)+'\n' for row in rows))
        self.source(2,'2026-10-07T13:00:00Z')
        with (self.home/'sessions/2.jsonl').open('a') as stream:
            stream.write(json.dumps({'type':'response_item','payload':{'type':'function_call',
                'name':'functions.exec','arguments':'await tools.mcp__personal_context__lookup({topic: "private"})'}})+'\n')
        self.assertEqual(sessions.review()['sessions'],[])
        self.assertEqual(len(self.calls),0)

    def test_nested_mcp_private_invocation_and_private_turn_cwd_are_excluded(self):
        source=self.source(1,'2026-10-07T12:00:00Z')
        with source.open('a') as stream:
            stream.write(json.dumps({'type':'event_msg','payload':{'type':'mcp_tool_call_begin',
                'invocation':{'server':'personal_context','tool':'retrieve','arguments':{'topic':'private'}}}})+'\n')
        source=self.source(2,'2026-10-07T13:00:00Z')
        with source.open('a') as stream:
            stream.write(json.dumps({'type':'turn_context','payload':{'cwd':'/home/example/coding/personal-context'}})+'\n')
        self.assertEqual(sessions.review()['sessions'],[])
        self.assertEqual(len(self.calls),0)

    def test_public_patch_fixture_literal_is_not_private_store_access(self):
        source=self.source(1,'2026-10-07T12:00:00Z')
        with source.open('a') as stream:
            stream.write(json.dumps({'type':'response_item','payload':{'type':'custom_tool_call',
                'name':'apply_patch','input':'*** Begin Patch\n*** Update File: tests/test_privacy.py\n+fixture = "/home/example/coding/personal-context/brief.md"\n*** End Patch'}})+'\n')
        self.assertEqual(len(sessions.review(refresh_limit=0)['sessions']),1)
        with source.open('a') as stream:
            stream.write(json.dumps({'type':'response_item','payload':{'type':'custom_tool_call',
                'name':'apply_patch','input':'*** Begin Patch\n*** Update File: /home/example/coding/personal-context/brief.md\n+private\n*** End Patch'}})+'\n')
        self.assertEqual(sessions.review(refresh_limit=0)['sessions'],[])

    def test_cached_false_private_exclusion_is_rechecked_after_parser_revision(self):
        self.source(1,'2026-10-07T12:00:00Z'); sessions.review(refresh_limit=0)
        path=self.base/'state/second-brain/sessions/state.json'; v=self.state()
        for entry in v['sessions'].values():
            entry.update(status='skipped',reason='private_context',id='',cwd='',title='',source='')
        for key,stamp in v['screened'].items():v['screened'][key]=stamp[-5:]
        path.write_text(json.dumps(v))
        result=sessions.review(refresh_limit=0)
        self.assertEqual([entry['title'] for entry in result['sessions']],['Task 1'])

    def test_top_level_private_name_is_not_hidden_by_nested_arguments(self):
        for number, kind in ((1,'response_item'),(2,'event_msg')):
            source=self.source(number,'2026-10-07T12:00:00Z')
            with source.open('a') as stream:
                stream.write(json.dumps({'type':kind,'payload':{'type':'mcp_tool_call' if kind=='response_item' else 'mcp_tool_call_end',
                    'name':'personal_context_retrieve','invocation':{'arguments':{'topic':'private'}}}})+'\n')
        self.assertEqual(sessions.review()['sessions'],[])
        self.assertEqual(len(self.calls),0)

if __name__=='__main__': unittest.main()
