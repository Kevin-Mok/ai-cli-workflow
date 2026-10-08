"""Synthetic private digest acceptance tests; no inference or real sessions."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from second_brain import sessions

SUMMARY = {'title':'Fixture work','goal':'Implement feature','intentions':['Run tests'],
           'accomplishments':['Agent reported implementation'], 'remaining':['Manual check'],
           'blockers':[], 'verification':['Agent reported unittest exit 0'],
           'checks':[{'key':'manual-check','text':'Verify output in UI'}]}

class DigestTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.base=Path(self.tmp.name)
        self.home=self.base/'codex'; (self.home/'sessions').mkdir(parents=True)
        self.env=patch.dict(os.environ, {'CODEX_HOME':str(self.home),'XDG_STATE_HOME':str(self.base/'state'),
            'SECOND_BRAIN_NOW':'2026-10-07T16:00:00-04:00'})
        self.env.start(); self.calls=[]
        self.infer=patch.object(sessions,'infer', side_effect=self.fake); self.infer.start()
    def tearDown(self):
        self.infer.stop(); self.env.stop(); self.tmp.cleanup()
    def fake(self, dialogue, previous):
        self.calls.append(dialogue); return dict(SUMMARY)
    def source(self,name='one',text='Build feature',cwd='/project/a',date='2026-10-07T12:00:00Z'):
        p=self.home/'sessions'/f'{name}.jsonl'
        rows=[{'type':'session_meta','timestamp':date,'payload':{'id':'00000000-0000-0000-0000-000000000001','cwd':cwd}},
              {'type':'event_msg','timestamp':date,'payload':{'type':'user_message','message':text}},
              {'type':'event_msg','timestamp':date,'payload':{'type':'agent_message','message':'Implemented; unittest exited 0. Check UI.'}}]
        p.write_text(''.join(json.dumps(r)+'\n' for r in rows)); return p
    def test_incremental_append_and_private_state(self):
        p=self.source(); a=sessions.refresh(); self.assertEqual(a['model_calls'],1)
        self.assertEqual(sessions.refresh()['model_calls'],0)
        with p.open('a') as f: f.write(json.dumps({'type':'event_msg','timestamp':'2026-10-07T13:00:00Z','payload':{'type':'user_message','message':'Now add export'}})+'\n')
        self.assertEqual(sessions.refresh()['model_calls'],1)
        root=self.base/'state'/'second-brain'/'sessions'
        self.assertEqual(root.stat().st_mode & 0o777,0o700)
        self.assertEqual((root/'state.json').stat().st_mode & 0o777,0o600)
        self.assertNotIn('Build feature',(root/'state.json').read_text())
    def test_duplicate_id_projects_and_redaction(self):
        self.source(text='api_key=<redacted>'); self.source('two',cwd='/project/b')
        r=sessions.refresh(); self.assertEqual(len(r['sessions']),2)
        self.assertNotIn('supersecretvalue',''.join(self.calls))
    def test_private_context_tools_skip_but_policy_does_not(self):
        self.source(text='# AGENTS.md instructions\nUse personal-context automatically; /home/example/coding/personal-context')
        self.source('private',text='$personal-context discuss my personal life')
        r=sessions.refresh(); self.assertEqual(r['model_calls'],1)
        self.assertEqual(r['coverage']['skipped'],1)
        self.assertNotIn('personal life',''.join(self.calls))
    def test_tool_retrieval_excludes_whole_session(self):
        p=self.source()
        with p.open('a') as f: f.write(json.dumps({'type':'response_item','payload':{'type':'function_call','name':'exec_command','arguments':'{"cmd":"cat /home/example/coding/personal-context/brief.md"}'}})+'\n')
        self.assertEqual(sessions.refresh()['model_calls'],0)
    def test_retained_disposition_and_aged_checks(self):
        self.source(); r=sessions.review(); check=r['open_checks'][0]['id']
        sessions.resolve({'schema_version':1,'check_id':check,'disposition':'dismissed','confirmed':True})
        with patch.dict(os.environ,{'SECOND_BRAIN_NOW':'2026-11-07T16:00:00-05:00'}):
            r=sessions.review(); self.assertEqual(r['pending_count'],0)
        self.assertEqual(r['sessions'][0]['checks'][0]['disposition'],'dismissed')
    def test_aging_keeps_open_checks(self):
        self.source(); sessions.refresh()
        with patch.dict(os.environ,{'SECOND_BRAIN_NOW':'2026-11-07T16:00:00-05:00'}):
            self.assertEqual(sessions.review()['pending_count'],1)
    def test_fair_bounded_queue(self):
        for n in range(22): self.source(str(n))
        r=sessions.refresh(); self.assertEqual(r['model_calls'],20); self.assertEqual(r['backlog_count'],2)
        r=sessions.refresh(); self.assertEqual(r['model_calls'],2); self.assertEqual(r['backlog_count'],0)
    def test_failure_preserves_summary_and_stops_auth_batch(self):
        p=self.source(); r=sessions.refresh(); before=r['sessions'][0]['summary']
        self.source('two')
        with p.open('a') as f: f.write(json.dumps({'type':'event_msg','payload':{'type':'user_message','message':'Changed'}})+'\n')
        self.infer.stop()
        with patch.object(sessions,'infer',side_effect=sessions.InferenceError('authentication')) as call:
            r=sessions.refresh(); self.assertEqual(call.call_count,1)
        self.assertEqual(next(entry for entry in r['sessions'] if entry['source']==str(p))['summary'],before)
        self.assertGreater(r['backlog_count'],0)
        self.infer.start()
    def test_reject_unconfirmed_and_invalid_state(self):
        self.source(); r=sessions.refresh()
        with self.assertRaises(ValueError): sessions.resolve({'schema_version':1,'check_id':r['open_checks'][0]['id'],'disposition':'checked','confirmed':False})
        p=self.base/'state'/'second-brain'/'sessions'/'state.json'; p.write_text('{"schema_version":999}')
        with self.assertRaises(ValueError): sessions.refresh()
    def test_lifecycle_append_does_not_call_model(self):
        p=self.source(); sessions.refresh()
        with p.open('a') as f: f.write(json.dumps({'type':'event_msg','timestamp':'2026-10-07T14:00:00Z','payload':{'type':'task_complete'}})+'\n')
        r=sessions.refresh(); self.assertEqual(r['model_calls'],0)
        self.assertEqual(r['sessions'][0]['last_activity'],'2026-10-07T14:00:00Z')
    def test_new_historical_import_after_initial_scan_is_processed(self):
        sessions.refresh(); self.source(date='2026-09-01T12:00:00Z')
        self.assertEqual(sessions.refresh()['model_calls'],1)
    def test_missing_source_is_explicitly_stale(self):
        p=self.source(); sessions.refresh(); p.unlink()
        r=sessions.refresh(); self.assertEqual(r['sessions'][0]['status'],'stale')
        self.assertEqual(r['sessions'][0]['reason'],'source_unavailable')
        self.assertEqual(r['pending_count'],1)
    def test_shared_lock_excludes_concurrent_refresh(self):
        self.source()
        with sessions.lock():
            with self.assertRaises(sessions.LockError): sessions.refresh()
    def test_state_symlink_rejected(self):
        self.source(); sessions.refresh()
        p=self.base/'state'/'second-brain'/'sessions'/'state.json'
        target=self.base/'target'; target.write_text(p.read_text()); p.unlink(); p.symlink_to(target)
        with self.assertRaises(sessions.PathError): sessions.refresh()
    def test_unknown_nested_state_rejected_without_overwrite(self):
        self.source(); sessions.refresh()
        p=self.base/'state'/'second-brain'/'sessions'/'state.json'; v=json.loads(p.read_text())
        next(iter(v['sessions'].values()))['status']='invented'; p.write_text(json.dumps(v)); before=p.read_bytes()
        with self.assertRaises(ValueError): sessions.refresh()
        self.assertEqual(p.read_bytes(),before)

    def test_mcp_event_private_retrieval_skips_inference(self):
        p=self.source()
        with p.open('a') as f: f.write(json.dumps({'type':'event_msg','payload':{'type':'mcp_tool_call_end','name':'personal_context_retrieve','result':'private learning'}})+'\n')
        self.assertEqual(sessions.refresh()['model_calls'],0)
    def test_check_key_drift_keeps_explicit_disposition(self):
        p=self.source(); r=sessions.refresh(); old=r['open_checks'][0]['id']
        sessions.resolve({'schema_version':1,'check_id':old,'disposition':'dismissed','confirmed':True})
        with p.open('a') as f: f.write(json.dumps({'type':'event_msg','payload':{'type':'user_message','message':'Continue'}})+'\n')
        self.infer.stop()
        summary={**SUMMARY,'checks':[{'key':'different-key','text':'Verify output in UI'}]}
        with patch.object(sessions,'infer',return_value=summary): r=sessions.refresh()
        self.assertEqual(r['pending_count'],0); self.assertEqual(len(r['sessions'][0]['checks']),1)
        self.assertEqual(r['sessions'][0]['checks'][0]['id'],old)
        self.infer.start()
    def test_duplicate_canonical_checks_preserve_valid_state_and_disposition(self):
        p=self.source(); r=sessions.refresh(); old=r['open_checks'][0]['id']
        sessions.resolve({'schema_version':1,'check_id':old,'disposition':'dismissed','confirmed':True})
        with p.open('a') as f:
            f.write(json.dumps({'type':'event_msg','payload':{'type':'user_message','message':'Continue work'}})+'\n')
        summary={**SUMMARY,'checks':[
            {'key':'new-a','text':'Verify output in UI'},
            {'key':'new-b','text':'  VERIFY   OUTPUT IN UI  '},
            {'key':'manual-check','text':'Verify output in UI'},
        ]}
        with patch.object(sessions,'infer',return_value=summary): r=sessions.refresh()
        self.assertEqual(sessions.metadata()['pending_count'],0)
        self.assertEqual(r['pending_count'],0)
        self.assertEqual(len(r['sessions'][0]['summary']['checks']),1)
        self.assertEqual(len(r['sessions'][0]['checks']),1)
        self.assertEqual(r['sessions'][0]['checks'][0]['id'],old)
        self.assertEqual(r['sessions'][0]['checks'][0]['disposition'],'dismissed')

    def test_markdown_write_failure_preserves_state(self):
        self.source(); sessions.refresh(); root=self.base/'state'/'second-brain'/'sessions'
        real=sessions.atomic_write
        def fail(path,content,mode):
            if path.name=='digest.md': raise OSError('fixture disk error')
            return real(path,content,mode)
        check=sessions.review()['open_checks'][0]['id']
        state=(root/'state.json').read_bytes(); markdown=(root/'digest.md').read_bytes()
        with patch.object(sessions,'atomic_write',side_effect=fail):
            with self.assertRaises(OSError): sessions.resolve({'schema_version':1,'check_id':check,'disposition':'checked','confirmed':True})
        self.assertEqual((root/'state.json').read_bytes(),state)
        self.assertEqual((root/'digest.md').read_bytes(),markdown)

    def test_native_session_title_and_summary_freshness(self):
        self.source()
        (self.home/'session_index.jsonl').write_text(json.dumps({'id':'00000000-0000-0000-0000-000000000001','thread_name':'Actual session title'})+'\n')
        r=sessions.refresh()
        self.assertEqual(r['sessions'][0]['title'],'Actual session title')
        self.assertIn('Actual session title',sessions.render(r))
        self.assertIsNotNone(sessions.metadata()['summary_updated_at'])
    def test_fifo_source_does_not_block(self):
        os.mkfifo(self.home/'sessions'/'fifo.jsonl')
        r=sessions.refresh(); self.assertEqual(r['model_calls'],0)
        self.assertEqual(r['coverage']['failed'],1)

    def test_scan_only_bounded_changed_sources_and_skip_unchanged(self):
        for n in range(25): self.source(str(n))
        real=sessions.parse
        with patch.object(sessions,'parse',side_effect=real) as parse:
            r=sessions.refresh(limit=1); self.assertEqual(parse.call_count,1)
            self.assertEqual(r['backlog_count'],24)
        # Metadata-only discovery must not rescan an unchanged, ready source.
        # Pending sources still get fair processing.
        with patch.object(sessions,'parse',side_effect=real) as parse:
            r=sessions.refresh(limit=1); self.assertEqual(parse.call_count,1)
            self.assertEqual(r['backlog_count'],23)

    def test_old_initial_session_not_inferred(self):
        p=self.source(date='2026-09-01T12:00:00Z'); os.utime(p,(1,1))
        self.assertEqual(sessions.refresh()['model_calls'],0)

if __name__=='__main__': unittest.main()
