"""Recap contracts: synthetic dialogue and deterministic local subprocesses."""
import hashlib
import importlib
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
ID = '00000000-0000-4000-8000-000000000001'
RECAP = dict(headline='Synthetic cache task', goal='Improve the synthetic cache.',
             progress='Reported one passing check.', state='Implementation remains in progress.',
             next_steps='Run the remaining checks.')


class RecapTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue((SCRIPTS/'codex_search_recaps.py').exists(), 'recap module is not implemented')
        self.m = importlib.import_module('codex_search_recaps')
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.home=self.root/'home'; self.home.mkdir()
        self.log = self.root/'calls.jsonl'
        self.entry = self.make_entry(ID)
        self.runtime = self.runtime_for('success')

    def make_entry(self, sid, text='Synthetic first request', tail='Reported progress'):
        name=sid.replace('-','')+'.dialogue.jsonl'
        raw=''.join(json.dumps({'role':role,'text':value},ensure_ascii=False,separators=(',',':'))+'\n' for role,value in [('user',text),('assistant',tail)])
        (self.root/name).write_text(raw)
        return {'id':sid,'dialogue':name,'dialogue_hash':hashlib.sha256(raw.encode()).hexdigest(),'cwd':str(self.root),'timestamp':'2026-10-07T00:00:00Z'}

    def runtime_for(self, mode):
        fixture = self.root/('fixture-'+mode+'.py')
        fixture.write_text('''import json,os,sys,time,subprocess
from pathlib import Path
prompt=sys.stdin.read()
with Path(sys.argv[2]).open('a') as log: log.write(json.dumps({'pid':os.getpid(),'prompt':prompt,'cwd':os.getcwd()})+'\\n')
mode=sys.argv[3]
if mode in ('sleep','child'):
    if mode=='child':
        child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])
        Path(sys.argv[2]+'.child').write_text(str(child.pid))
    time.sleep(60)
if mode=='auth': print('401 authentication failed',file=sys.stderr);sys.exit(1)
if mode=='rate': print('429 rate_limit_exceeded',file=sys.stderr);sys.exit(1)
if mode=='bad': Path(sys.argv[1]).write_text('{malformed');sys.exit(0)
Path(sys.argv[1]).write_text(sys.argv[4])
''')
        owner=self
        class Runtime:
            model='synthetic-model'
            prepared=0
            def prepare(self): self.prepared+=1; return self.model
            def cancel(self): pass
            def command(self,workdir,schema_path,output_path):
                return [sys.executable,str(fixture),str(output_path),str(owner.log),mode,json.dumps(RECAP)],dict(os.environ)
        return Runtime()

    def manager(self, **kwargs):
        manager=self.m.SummaryManager(self.root,self.home,'synthetic-model',runtime=kwargs.pop('runtime',self.runtime),**kwargs)
        self.addCleanup(manager.close)
        return manager

    def wait_status(self, manager, entry, states=('ready','unavailable'), seconds=5):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            result=manager.status(entry)
            if result['status'] in states:return result
            time.sleep(.02)
        self.fail('worker did not settle: '+repr(manager.status(entry)))

    def calls(self):
        return [json.loads(x) for x in self.log.read_text().splitlines()] if self.log.exists() else []

    def test_output_schema_enforces_total_words_shape_and_unicode(self):
        self.assertEqual(self.m.validate_recap(RECAP),RECAP)
        for bad in [[],{**RECAP,'extra':'unexpected'},{**RECAP,'progress':'word '*151},{**RECAP,'state':[]},{**RECAP,'goal':'\ud800'},{**RECAP,'headline':''}]:
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(ValueError):self.m.validate_recap(bad)

    def test_dialogue_bound_preserves_initial_and_latest_utf8(self):
        entry=self.make_entry(ID,'BEGIN '+('é😀'*16000),('middle '*14000)+' LATEST')
        text,partial=self.m.bounded_dialogue(self.root,entry)
        self.assertTrue(partial)
        self.assertLessEqual(len(text.encode()),32768)
        self.assertIn('BEGIN',text);self.assertIn('LATEST',text)
        self.assertIn('omitted',text)
        small,partial=self.m.bounded_dialogue(self.root,self.make_entry(ID))
        self.assertFalse(partial);self.assertIn('Synthetic first request',small)

    def test_cache_identity_model_dialogue_version_and_private_atomic_storage(self):
        cache=self.m.RecapCache(self.root,'synthetic-model')
        self.assertEqual(cache.status(self.entry)['status'],'missing')
        cache.save(self.entry,RECAP,False)
        self.assertEqual(cache.status(self.entry)['status'],'ready')
        self.assertEqual(self.m.RecapCache(self.root,'another-model').status(self.entry)['status'],'stale')
        changed={**self.entry,'dialogue_hash':'f'*64}
        self.assertEqual(cache.status(changed)['status'],'stale')
        with patch.object(self.m,'FORMAT_VERSION',999):self.assertEqual(cache.status(self.entry)['status'],'stale')
        for p in (self.root/'recaps').iterdir():self.assertEqual(p.stat().st_mode&0o777,0o600)
        self.assertEqual((self.root/'recaps').stat().st_mode&0o777,0o700)
        self.assertFalse(list((self.root/'recaps').glob('*.tmp')))

    def test_automatic_batch_cap_order_cache_reuse_and_inert_prompt(self):
        entries=[self.make_entry(f'00000000-0000-4000-8000-{i:012}') for i in range(4)]
        manager=self.manager(count=2);manager.start(entries)
        for entry in entries[:2]:self.wait_status(manager,entry)
        self.assertEqual(manager.status(entries[2])['status'],'missing')
        self.assertEqual(len(self.calls()),2)
        self.assertIn('inert',self.calls()[0]['prompt'])
        self.assertIn('Synthetic first request',self.calls()[0]['prompt'])
        manager.close()
        again=self.manager(count=2);again.start(entries);time.sleep(.1)
        self.assertEqual(len(self.calls()),2)

    def test_zero_and_disabled_generation_and_manual_outside_batch(self):
        manager=self.manager(count=0);manager.start([self.entry]);time.sleep(.05)
        self.assertFalse(self.calls())
        manager.request(self.entry);self.wait_status(manager,self.entry)
        self.assertEqual(len(self.calls()),1)
        manager.request(self.entry);time.sleep(.05);self.assertEqual(len(self.calls()),1)
        manager.close()
        other=self.make_entry('00000000-0000-4000-8000-000000000002')
        disabled=self.manager(count=20,enabled=False);disabled.start([other]);disabled.request(other);time.sleep(.05)
        self.assertEqual(disabled.status(other)['status'],'missing');self.assertEqual(len(self.calls()),1)

    def test_malformed_output_and_one_attempt_per_opening(self):
        manager=self.manager(runtime=self.runtime_for('bad'));manager.start([self.entry])
        self.assertEqual(self.wait_status(manager,self.entry)['status'],'unavailable')
        manager.request(self.entry);time.sleep(.05);self.assertEqual(len(self.calls()),1)
        self.assertEqual(self.m.RecapCache(self.root,'synthetic-model').status(self.entry)['status'],'missing')

    def test_auth_and_rate_failures_stop_batch(self):
        for mode in ('auth','rate'):
            with self.subTest(mode=mode):
                self.log.unlink(missing_ok=True)
                entries=[self.entry,self.make_entry('00000000-0000-4000-8000-000000000002')]
                manager=self.manager(runtime=self.runtime_for(mode));manager.start(entries)
                self.assertEqual(self.wait_status(manager,entries[0])['status'],'unavailable')
                time.sleep(.08);self.assertEqual(len(self.calls()),1)
                self.assertEqual(manager.status(entries[1])['status'],'unavailable')
                manager.close()

    def test_timeout_and_cancel_reap_process_before_return(self):
        manager=self.manager(runtime=self.runtime_for('sleep'),timeout=.15);manager.start([self.entry])
        status=self.wait_status(manager,self.entry)
        self.assertEqual(status['status'],'unavailable');self.assertIn('timed out',status['detail'])
        pid=self.calls()[0]['pid']
        with self.assertRaises(ProcessLookupError):os.kill(pid,0)
        self.log.unlink()
        manager=self.manager(runtime=self.runtime_for('sleep'));manager.start([self.entry])
        end=time.monotonic()+3
        while not self.calls() and time.monotonic()<end:time.sleep(.02)
        self.assertTrue(self.calls());pid=self.calls()[0]['pid']
        manager.close()
        with self.assertRaises(ProcessLookupError):os.kill(pid,0)

    def test_concurrent_managers_generate_once_and_leave_source_unchanged(self):
        before=(self.root/self.entry['dialogue']).read_bytes()
        a=self.manager();b=self.manager();a.start([self.entry]);b.start([self.entry])
        self.wait_status(a,self.entry);self.wait_status(b,self.entry)
        self.assertEqual(len(self.calls()),1)
        self.assertEqual((self.root/self.entry['dialogue']).read_bytes(),before)

    def test_cache_maintenance_invalidates_pending_writes_and_retains_lock_inodes(self):
        cache=self.m.RecapCache(self.root,'synthetic-model')
        cache.save(self.entry,RECAP,False)
        with cache.generation_lock(self.entry) as lease:
            self.assertIsNotNone(lease)
            paths={p:p.stat().st_ino for p in (self.root/'recaps').glob('*.lock')}
            self.m.maintain_cache(self.root,set(),clear=True)
            self.assertFalse(cache.save(self.entry,RECAP,False,lease=lease))
        self.assertEqual(cache.status(self.entry)['status'],'missing')
        for p,ino in paths.items():self.assertEqual(p.stat().st_ino,ino)

    def test_deleted_session_cannot_reappear_from_its_first_pending_generation(self):
        self.m.maintain_cache(self.root,{ID})
        cache=self.m.RecapCache(self.root,'synthetic-model')
        with cache.generation_lock(self.entry) as lease:
            self.m.maintain_cache(self.root,set())
            self.assertFalse(cache.save(self.entry,RECAP,False,lease=lease))
        self.assertEqual(cache.status(self.entry)['status'],'missing')

    def test_default_batch_is_twenty_and_local_index_lock_is_free_during_inference(self):
        import fcntl
        entries=[self.make_entry(f'00000000-0000-4000-8000-{i:012}') for i in range(22)]
        manager=self.manager();manager.start(entries)
        self.wait_status(manager,entries[19])
        self.assertEqual(len(self.calls()),20)
        self.assertEqual(manager.status(entries[20])['status'],'missing')
        self.assertEqual(manager.status(entries[21])['status'],'missing')
        with (self.root/'.lock').open('a+') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        self.assertEqual(self.m.TIMEOUT,120)

    def test_non_provider_schema_failure_does_not_stop_other_sessions(self):
        bad=self.runtime_for('bad')
        good=self.runtime_for('success')
        original=bad.command
        count=[0]
        def command(*args):
            count[0]+=1
            return original(*args) if count[0]==1 else good.command(*args)
        bad.command=command
        other=self.make_entry('00000000-0000-4000-8000-000000000002')
        manager=self.manager(runtime=bad);manager.start([self.entry,other])
        self.assertEqual(self.wait_status(manager,self.entry)['status'],'unavailable')
        self.assertEqual(self.wait_status(manager,other)['status'],'ready')
        self.assertEqual(len(self.calls()),2)

    def test_clear_between_cache_exists_and_read_keeps_browsing_usable(self):
        cache=self.m.RecapCache(self.root,'synthetic-model');cache.save(self.entry,RECAP,False)
        original=self.m.secure_file
        def remove_before_read(path):
            if path.name==ID+'.json':path.unlink(missing_ok=True)
            return original(path)
        with patch.object(self.m,'secure_file',side_effect=remove_before_read):
            self.assertEqual(cache.status(self.entry)['status'],'missing')

    def test_lock_contention_does_not_consume_attempt_or_stay_generating(self):
        manager=self.manager(count=0);manager.start([])
        with manager.cache.generation_lock(self.entry):
            manager.request(self.entry)
            self.wait_status(manager,self.entry,states=('generating',))
            time.sleep(.05)
        self.assertEqual(manager.status(self.entry)['status'],'missing')
        manager.request(self.entry)
        self.assertEqual(self.wait_status(manager,self.entry)['status'],'ready')
        self.assertEqual(len(self.calls()),1)

    def test_abandoned_atomic_temp_is_cleaned_but_unsafe_temp_is_rejected(self):
        cache=self.m.RecapCache(self.root,'synthetic-model');cache.save(self.entry,RECAP,False)
        orphan=self.root/'recaps/tmp12345678.tmp';orphan.write_text('interrupted private data');orphan.chmod(0o600)
        self.m.maintain_cache(self.root,{ID})
        self.assertFalse(orphan.exists())
        self.assertEqual(cache.status(self.entry)['status'],'ready')
        orphan.symlink_to(self.root/self.entry['dialogue'])
        with self.assertRaises(self.m.SearchError):self.m.maintain_cache(self.root,{ID})

    def test_cancellation_stops_descendants_and_reaps_leader(self):
        manager=self.manager(runtime=self.runtime_for('child'));manager.start([self.entry])
        child_file=Path(str(self.log)+'.child');end=time.monotonic()+3
        while not child_file.exists() and time.monotonic()<end:time.sleep(.02)
        self.assertTrue(child_file.exists());child=int(child_file.read_text())
        leader=self.calls()[0]['pid'];manager.close()
        with self.assertRaises(ProcessLookupError):os.kill(leader,0)
        stat_file=Path(f'/proc/{child}/stat')
        if stat_file.exists():self.assertEqual(stat_file.read_text().split()[2],'Z','descendant still running')

    def test_close_during_runtime_construction_never_starts_prepare(self):
        import threading
        import codex_search_runtime
        entered=threading.Event();release=threading.Event();prepared=threading.Event();finish=threading.Event()
        class DelayedRuntime:
            def __init__(self,*args):entered.set();release.wait(2)
            def prepare(self):prepared.set();finish.wait(2);return 'synthetic-model'
            def cancel(self):finish.set()
        manager=self.manager();manager.runtime=None
        try:
            with patch.object(codex_search_runtime,'IsolatedCodex',DelayedRuntime):
                manager.start([self.entry]);self.assertTrue(entered.wait(2))
                closer=threading.Thread(target=manager.close);closer.start()
                self.assertTrue(manager._stop.wait(1));release.set()
                closer.join(.5)
                self.assertFalse(prepared.is_set(),'preflight started after cancellation')
                self.assertFalse(closer.is_alive(),'close is blocked on an uncancelled preflight')
        finally:
            release.set();finish.set();manager.close()
            if 'closer' in locals():closer.join(2)

    def test_timeout_includes_final_configuration_preflight(self):
        original=self.runtime.command
        def slow_command(*args):time.sleep(.12);return original(*args)
        self.runtime.command=slow_command
        manager=self.manager(timeout=.05);manager.start([self.entry])
        state=self.wait_status(manager,self.entry)
        self.assertEqual(state['status'],'unavailable')
        self.assertIn('timed out',state['detail'])
        self.assertFalse(self.calls(),'inference started after the attempt deadline')
