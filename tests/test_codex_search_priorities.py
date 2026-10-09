"""Priority ordering and source refresh using synthetic local sessions."""
import importlib
import json
import os
from pathlib import Path
import sys
import shutil
import subprocess
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
ID1='00000000-0000-4000-8000-000000000001'
ID2='00000000-0000-4000-8000-000000000002'

class PriorityTest(unittest.TestCase):
    def setUp(self):
        self.m=importlib.import_module('codex_search_recent')

    def test_priority_order_uses_evidence_then_activity_and_unknown_fallback(self):
        self.assertTrue(hasattr(self.m,'order_sessions'),'AI ordering is missing')
        entries=[];statuses={}
        for n,priority in enumerate(('complete','waiting','unknown','actionable','urgent','urgent'),1):
            sid=f'00000000-0000-4000-8000-{n:012d}'
            entry={'id':sid,'cwd':'/synthetic','timestamp':f'2026-10-09T00:00:0{n}Z'}
            entries.append(entry)
            statuses[sid]={'status':'ready','recap':{'priority':priority,'priority_reason':'Synthetic evidence'}}
        ordered=self.m.order_sessions(entries,statuses)
        self.assertEqual([e['id'][-1] for e in ordered],['6','5','4','3','2','1'])
        self.assertEqual([e['id'][-1] for e in self.m.order_sessions(entries,statuses,'recent')],['6','5','4','3','2','1'])
        statuses[entries[-1]['id']]={'status':'missing','recap':None}
        self.assertEqual([e['id'][-1] for e in self.m.order_sessions(entries,statuses)],['5','4','6','3','2','1'])

    def test_priority_reason_and_staleness_are_visible_without_inventing_priority(self):
        entry={'id':ID1,'cwd':'/synthetic','timestamp':'2026-10-09T00:00:00Z'}
        status={'status':'stale','recap':{'headline':'Repair failure','priority':'urgent',
                'priority_reason':'Reported release blocker','goal':'Repair','progress':'Unknown',
                'state':'Unresolved','next_steps':'Reproduce'}}
        row,preview=self.m.render_session(entry,'Synthetic task',status)
        self.assertIn('Priority: urgent (stale)',preview)
        self.assertIn('Reported release blocker',preview)
        self.assertIn('[urgent; stale]',row)
        _,unknown=self.m.render_session(entry,'Synthetic task',{'status':'missing','recap':None})
        self.assertIn('Priority: unknown',unknown)

    def test_enter_resumes_visible_uuid_even_with_a_previous_restoration_focus(self):
        with tempfile.TemporaryDirectory(prefix='codex-search-picker-') as temp:
            path=Path(temp);path.chmod(0o700)
            self.m.atomic_json(path/'manifest.json',{'ids':[ID1,ID2],'root':str(path)})
            self.m.atomic_json(path/'focus.json',ID1)
            self.m.helper('accept',path,ID2)
            self.assertEqual(self.m.read_json(path/'accepted.json'),ID2)

class WatcherTest(unittest.TestCase):
    def test_live_source_title_content_addition_and_deletion_are_refreshed(self):
        self.assertTrue((ROOT/'scripts/codex_search_watch.py').exists(),'Live source watcher is missing')
        module=importlib.import_module('codex_search_watch')
        from codex_search_index import refresh,titles
        with tempfile.TemporaryDirectory(prefix='priority-watch-') as temp:
            base=Path(temp);home=base/'home';sources=home/'sessions';sources.mkdir(parents=True)
            root=base/'cache';root.mkdir(mode=0o700)
            runtime=base/'codex-search-picker-test';runtime.mkdir(mode=0o700)
            def write(sid,text,stamp):
                path=sources/(sid+'.jsonl')
                path.write_text(json.dumps({'type':'session_meta','timestamp':stamp,'payload':{'id':sid,'cwd':str(base)}})+'\n'+json.dumps({'type':'response_item','timestamp':stamp,'payload':{'type':'message','role':'assistant','content':[{'type':'output_text','text':text}]}})+'\n')
                return path
            first=write(ID1,'Initial reported progress','2026-10-09T00:00:00Z')
            original=refresh(root,home)
            oldhash=next(iter(original.values()))['dialogue_hash']
            watcher=module.SessionWatcher(root,home,runtime,interval=.05)
            self.addCleanup(watcher.close);watcher.start()
            def wait_for(check):
                end=time.monotonic()+5
                while time.monotonic()<end:
                    value=watcher.read()
                    if value and check(value):return value
                    time.sleep(.02)
                self.fail('Live source update did not arrive')
            wait_for(lambda v:len(v['entries'])==1)
            (home/'session_index.jsonl').write_text(json.dumps({'id':ID1,'thread_name':'Guardian repaired blocker'})+'\n')
            write(ID1,'Guardian reports fix verified','2026-10-09T00:00:03Z')
            write(ID2,'New task','2026-10-09T00:00:04Z')
            current=wait_for(lambda v:len(v['entries'])==2 and v['names'].get(ID1)=='Guardian repaired blocker')
            entry=next(e for e in current['entries'] if e['id']==ID1)
            self.assertNotEqual(entry['dialogue_hash'],oldhash)
            self.assertEqual(entry['timestamp'],'2026-10-09T00:00:03Z')
            first.unlink()
            wait_for(lambda v:[e['id'] for e in v['entries']]==[ID2])
            watcher.close();self.assertIsNotNone(watcher.process.poll())

@unittest.skipUnless(shutil.which('fzf'), 'real fzf is optional')
class GuardianCLITest(unittest.TestCase):
    def test_actual_cli_guardian_update_preserves_query_uuid_and_cached_generation_cap(self):
        fixture=ROOT/'tests/scripts/codex_priority_live_check.py'
        self.assertTrue(fixture.exists(),'actual CLI Guardian fixture is missing')
        result=subprocess.run([sys.executable,str(fixture),'--scenario','all'],capture_output=True,text=True,timeout=45)
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        self.assertIn('Guardian',result.stdout)
        self.assertIn('cached',result.stdout.lower())

if __name__=='__main__':unittest.main()
