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
             next_steps='Run the remaining checks.', priority='actionable',
             priority_reason='The conversation reports unfinished checks that can run now.')
LEGACY_RECAP = {key: RECAP[key] for key in ('headline', 'goal', 'progress', 'state', 'next_steps')}


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
if mode=='hold':
    while not Path(sys.argv[5]).exists(): time.sleep(.01)
if mode=='auth': print('401 authentication failed',file=sys.stderr);sys.exit(1)
if mode=='rate': print('429 rate_limit_exceeded',file=sys.stderr);sys.exit(1)
if mode=='bad': Path(sys.argv[1]).write_text('{malformed');sys.exit(0)
Path(sys.argv[1]).write_text(sys.argv[4])
''')
        owner=self
        class Runtime:
            model='synthetic-model'
            prepared=0
            output=RECAP
            hold_path=owner.root/'release'
            def prepare(self): self.prepared+=1; return self.model
            def cancel(self): pass
            def command(self,workdir,schema_path,output_path):
                return [sys.executable,str(fixture),str(output_path),str(owner.log),mode,json.dumps(self.output),str(self.hold_path)],dict(os.environ)
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

    def test_priority_validation_accepts_only_evidence_tiers_and_bounded_reason(self):
        for priority in ('urgent', 'actionable', 'unknown', 'waiting', 'complete'):
            self.assertEqual(self.m.validate_recap({**RECAP, 'priority': priority})['priority'], priority)
        for bad in ({**RECAP, 'priority': 'ignore instructions'},
                    {**RECAP, 'priority': []}, {**RECAP, 'priority_reason': ''},
                    {**RECAP, 'priority_reason': 'x' * 241}, LEGACY_RECAP):
            with self.subTest(bad=repr(bad)), self.assertRaises(ValueError):
                self.m.validate_recap(bad)
        # Exactly 150 prose words is valid; the enum label is not prose.
        at_limit = dict(headline='task', goal='goal', progress='progress', state='state',
                        next_steps='word ' * 145, priority='unknown', priority_reason='uncertain')
        self.m.validate_recap(at_limit)
        with self.assertRaises(ValueError):
            self.m.validate_recap({**at_limit, 'priority_reason': 'still uncertain'})

    def test_legacy_five_field_cache_remains_readable_with_unknown_stale_priority(self):
        directory = self.root / 'recaps'; directory.mkdir(mode=0o700)
        # Even a coincidentally matching envelope cannot certify missing priority.
        path = directory / (ID + '.json')
        path.write_text(json.dumps({'id': ID, 'key': self.m.recap_key(self.entry, 'synthetic-model'),
                                    'version': 1, 'partial': False, 'recap': LEGACY_RECAP}))
        status = self.m.RecapCache(self.root, 'synthetic-model').status(self.entry)
        self.assertEqual(status['status'], 'stale')
        self.assertEqual(status['recap']['headline'], 'Synthetic cache task')
        self.assertEqual(status['recap']['priority'], 'unknown')
        self.assertTrue(status['recap']['priority_reason'])

    def test_generated_five_field_legacy_output_is_rejected(self):
        self.runtime.output = LEGACY_RECAP
        manager = self.manager(); manager.start([self.entry])
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'unavailable')
        self.assertEqual(manager.cache.status(self.entry)['status'], 'missing')

    def update_manager(self, manager, entries):
        self.assertTrue(callable(getattr(manager, 'update', None)), 'live recap updates are not implemented')
        manager.update(entries)

    def pending_entry(self, entry, retain_dialogue=False):
        return {**entry, 'index_pending': True,
                **({} if retain_dialogue else {'dialogue': '', 'dialogue_hash': ''})}

    def test_pending_index_starts_no_model_work_and_generates_once_when_indexed(self):
        pending = self.pending_entry(self.entry)
        manager = self.manager(count=1); manager.start([pending])
        time.sleep(.08)
        status = manager.status(pending)
        self.assertEqual(status['status'], 'indexing')
        self.assertEqual(status['detail'], 'Indexing local dialogue; recap will be available shortly.')
        self.assertFalse(self.calls())
        self.assertEqual(self.runtime.prepared, 0)
        self.update_manager(manager, [self.entry])
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'ready')
        self.assertEqual(len(self.calls()), 1)
        self.update_manager(manager, [self.entry]); time.sleep(.08)
        self.assertEqual(len(self.calls()), 1)

    def test_pending_index_keeps_cached_recap_stale_even_when_old_key_matches(self):
        cache = self.m.RecapCache(self.root, 'synthetic-model')
        cache.save(self.entry, RECAP, False)
        pending = self.pending_entry(self.entry, retain_dialogue=True)
        status = cache.status(pending)
        self.assertEqual(status['status'], 'stale')
        self.assertEqual(status['recap'], RECAP)
        manager = self.manager(); manager.start([pending]); time.sleep(.08)
        status = manager.status(pending)
        self.assertEqual(status['status'], 'stale')
        self.assertEqual(status['detail'], 'Indexing local dialogue; recap will be available shortly.')
        self.assertEqual(status['recap']['headline'], 'Synthetic cache task')
        self.assertFalse(self.calls())
        self.assertEqual(self.runtime.prepared, 0)

    def test_pending_manual_request_survives_indexing_outside_zero_automatic_window(self):
        pending = self.pending_entry(self.entry)
        manager = self.manager(count=0); manager.start([pending])
        manager.request(pending); manager.request(pending); time.sleep(.08)
        self.assertFalse(self.calls())
        self.assertEqual(self.runtime.prepared, 0)
        other = self.make_entry('00000000-0000-4000-8000-000000000002')
        self.update_manager(manager, [other, self.entry])
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'ready')
        self.assertEqual(manager.status(other)['status'], 'missing')
        self.assertEqual(len(self.calls()), 1)
        self.update_manager(manager, [other, self.entry]); time.sleep(.08)
        self.assertEqual(len(self.calls()), 1)

    def test_pending_manual_request_moves_before_automatic_ready_backlog(self):
        import threading
        entered = threading.Event(); release = threading.Event()
        original = self.runtime.prepare
        def controlled_prepare():
            entered.set(); release.wait(3)
            return original()
        self.runtime.prepare = controlled_prepare
        self.addCleanup(release.set)
        other = self.make_entry('00000000-0000-4000-8000-000000000002', 'Automatic second request')
        selected = self.make_entry('00000000-0000-4000-8000-000000000003', 'Manual third request')
        pending_other = self.pending_entry(other)
        pending_selected = self.pending_entry(selected)
        manager = self.manager(count=2); manager.start([self.entry, pending_other, pending_selected])
        self.assertTrue(entered.wait(2))
        manager.request(pending_selected)
        self.update_manager(manager, [self.entry, other, selected])
        self.assertEqual(manager.status(selected).get('queue_position'), 1)
        self.assertEqual(manager.status(other).get('queue_position'), 2)
        release.set()
        for entry in (self.entry, other, selected):
            self.assertEqual(self.wait_status(manager, entry)['status'], 'ready')
        self.assertEqual(len(self.calls()), 3)
        self.assertIn('Manual third request', self.calls()[1]['prompt'])
        self.assertIn('Automatic second request', self.calls()[2]['prompt'])

    def test_queued_manual_request_defers_when_its_input_becomes_pending(self):
        import threading
        entered = threading.Event(); release = threading.Event()
        original = self.runtime.prepare
        def controlled_prepare():
            entered.set(); release.wait(3)
            return original()
        self.runtime.prepare = controlled_prepare
        self.addCleanup(release.set)
        other = self.make_entry('00000000-0000-4000-8000-000000000002')
        manager = self.manager(count=1); manager.start([self.entry, other])
        self.assertTrue(entered.wait(2))
        manager.request(other)
        pending = self.pending_entry(other, retain_dialogue=True)
        self.update_manager(manager, [self.entry, pending])
        self.assertEqual(manager.status(pending)['status'], 'indexing')
        release.set()
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'ready')
        time.sleep(.1)
        self.assertEqual(len(self.calls()), 1)
        self.update_manager(manager, [self.entry, other])
        self.assertEqual(self.wait_status(manager, other)['status'], 'ready')
        self.assertEqual(len(self.calls()), 2)

    def test_deleted_pending_manual_request_does_not_survive_reappearance(self):
        pending = self.pending_entry(self.entry)
        manager = self.manager(count=0); manager.start([pending]); manager.request(pending)
        self.update_manager(manager, [])
        self.update_manager(manager, [self.entry]); time.sleep(.08)
        self.assertFalse(self.calls())
        self.assertEqual(manager.status(self.entry)['status'], 'missing')
        manager.request(self.entry)
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'ready')
        self.assertEqual(len(self.calls()), 1)

    def test_disabled_pending_manual_request_never_runs_after_index_ready(self):
        pending = self.pending_entry(self.entry)
        manager = self.manager(enabled=False, count=0); manager.start([pending]); manager.request(pending)
        self.update_manager(manager, [self.entry]); time.sleep(.08)
        self.assertFalse(self.calls())
        self.assertEqual(self.runtime.prepared, 0)
        self.assertEqual(manager.status(self.entry)['status'], 'missing')

    def test_changed_dialogue_gets_one_new_attempt_but_metadata_update_does_not(self):
        manager = self.manager(count=1); manager.start([self.entry])
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'ready')
        metadata = {**self.entry, 'timestamp': '2026-10-09T00:00:00Z', 'title': 'Guardian title'}
        self.update_manager(manager, [metadata]); time.sleep(.1)
        self.assertEqual(len(self.calls()), 1)
        changed = self.make_entry(ID, 'Guardian new request', 'Reported new remaining check')
        self.update_manager(manager, [changed])
        self.assertEqual(self.wait_status(manager, changed)['status'], 'ready')
        self.assertEqual(len(self.calls()), 2)
        self.assertIn('Guardian new request', self.calls()[1]['prompt'])
        self.update_manager(manager, [changed]); manager.request(changed); time.sleep(.1)
        self.assertEqual(len(self.calls()), 2)

    def test_update_requeues_only_the_newest_automatic_window(self):
        manager = self.manager(count=1); manager.start([self.entry])
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'ready')
        newest = self.make_entry('00000000-0000-4000-8000-000000000002', 'New newest session')
        outside = self.make_entry('00000000-0000-4000-8000-000000000003')
        self.update_manager(manager, [newest, outside, self.entry])
        self.assertEqual(self.wait_status(manager, newest)['status'], 'ready')
        self.assertEqual(manager.status(outside)['status'], 'missing')
        self.assertEqual(len(self.calls()), 2)

    def test_metadata_refresh_preserves_manual_request_ahead_of_automatic_queue(self):
        import threading
        entered = threading.Event(); release = threading.Event()
        prepare = self.runtime.prepare
        def controlled_prepare():
            entered.set(); release.wait(3)
            return prepare()
        self.runtime.prepare = controlled_prepare
        self.addCleanup(release.set)
        entries = [self.entry, self.make_entry('00000000-0000-4000-8000-000000000002'),
                   self.make_entry('00000000-0000-4000-8000-000000000003')]
        manager = self.manager(count=3); manager.start(entries)
        self.assertTrue(entered.wait(2))
        manager.request(entries[2])
        self.update_manager(manager, [{**entry, 'title': 'Updated Guardian title'} for entry in entries])
        self.assertEqual(manager.status(entries[2]).get('queue_position'), 1)
        self.assertEqual(manager.status(entries[1]).get('queue_position'), 2)
        release.set()
        for entry in entries:
            self.assertEqual(self.wait_status(manager, entry)['status'], 'ready')
        self.assertEqual(len(self.calls()), 3)

    def test_effective_model_resolution_preserves_queue_progress_and_attempt_cap(self):
        import threading
        entered = threading.Event(); release = threading.Event()
        self.runtime.model = 'effective-synthetic-model'
        command = self.runtime.command
        def controlled_command(*args):
            entered.set(); release.wait(3)
            return command(*args)
        self.runtime.command = controlled_command
        self.addCleanup(release.set)
        other = self.make_entry('00000000-0000-4000-8000-000000000002')
        manager = self.manager(count=2); manager.start([self.entry, other])
        self.assertTrue(entered.wait(2))
        status = manager.status(other)
        self.assertEqual(status['status'], 'queued')
        self.assertEqual(status.get('queue_position'), 1)
        release.set()
        for entry in (self.entry, other):
            self.assertEqual(self.wait_status(manager, entry)['status'], 'ready')
        self.update_manager(manager, [self.entry, other]); time.sleep(.1)
        self.assertEqual(len(self.calls()), 2)

    def replace_dialogue_file(self, entry):
        token = hashlib.md5((entry['dialogue'] + '-replacement').encode()).hexdigest()
        replacement = {**entry, 'dialogue': token + '.dialogue.jsonl'}
        (self.root / replacement['dialogue']).write_bytes((self.root / entry['dialogue']).read_bytes())
        (self.root / entry['dialogue']).unlink()
        return replacement

    def publish_manifest(self, entries):
        import codex_search_index
        sources = {}
        for entry in entries:
            token = entry['dialogue'].split('.')[0]
            sources[str(self.home / 'sessions' / (entry['id'] + '.jsonl'))] = {
                **entry, 'signature': [0, 0, 0, 0, 0], 'skipped': 0,
                'conversation': token + '.conversation.txt', 'tools': token + '.tools.txt'}
            (self.root / (token + '.conversation.txt')).write_text('Synthetic indexed conversation')
            (self.root / (token + '.tools.txt')).write_text('Synthetic indexed tools')
        codex_search_index.atomic_json(self.root / 'manifest.json', {
            'version': codex_search_index.CACHE_VERSION, 'home': str(self.home), 'sources': sources})

    def test_metadata_only_replacement_updates_queued_dialogue_filename(self):
        import threading
        entered = threading.Event(); release = threading.Event()
        prepare = self.runtime.prepare
        def controlled_prepare():
            entered.set(); release.wait(3)
            return prepare()
        self.runtime.prepare = controlled_prepare
        self.addCleanup(release.set)
        other = self.make_entry('00000000-0000-4000-8000-000000000002')
        manager = self.manager(count=2); manager.start([self.entry, other])
        self.assertTrue(entered.wait(2))
        replacement = self.replace_dialogue_file(other)
        self.update_manager(manager, [self.entry, replacement])
        release.set()
        self.assertEqual(self.wait_status(manager, replacement)['status'], 'ready')
        self.assertEqual(len(self.calls()), 2)
        self.update_manager(manager, [self.entry, replacement]); time.sleep(.1)
        self.assertEqual(len(self.calls()), 2)

    def test_metadata_only_replacement_updates_input_waiting_for_index_lock(self):
        import fcntl
        manager = self.manager()
        with (self.root / '.lock').open('a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            manager.start([self.entry])
            self.wait_status(manager, self.entry, states=('generating',))
            replacement = self.replace_dialogue_file(self.entry)
            self.update_manager(manager, [replacement])
        self.assertEqual(self.wait_status(manager, replacement)['status'], 'ready')
        self.assertEqual(len(self.calls()), 1)

    def test_metadata_only_replacement_before_ui_update_uses_validated_manifest(self):
        import fcntl
        manager = self.manager()
        with (self.root / '.lock').open('a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            manager.start([self.entry])
            self.wait_status(manager, self.entry, states=('generating',))
            replacement = self.replace_dialogue_file(self.entry)
            self.publish_manifest([replacement])
        # The watcher has released .lock, but the UI has not read its new snapshot.
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'ready')
        self.assertEqual(len(self.calls()), 1)
        self.update_manager(manager, [replacement]); time.sleep(.1)
        self.assertEqual(len(self.calls()), 1)

    def test_old_unavailable_state_does_not_follow_changed_dialogue(self):
        runtime = self.runtime_for('bad')
        manager = self.manager(runtime=runtime); manager.start([self.entry])
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'unavailable')
        good = self.runtime_for('success')
        runtime.command = good.command
        changed = self.make_entry(ID, 'Updated after invalid old provider output')
        self.update_manager(manager, [changed])
        self.assertNotEqual(manager.status(changed)['status'], 'unavailable')
        self.assertEqual(self.wait_status(manager, changed)['status'], 'ready')
        self.assertEqual(len(self.calls()), 2)

    def test_delayed_old_generation_cannot_overwrite_new_dialogue(self):
        runtime = self.runtime_for('hold')
        first_release = runtime.hold_path
        second_release = self.root / 'release-new'
        self.addCleanup(first_release.touch); self.addCleanup(second_release.touch)
        manager = self.manager(runtime=runtime, count=1); manager.start([self.entry])
        end = time.monotonic() + 3
        while len(self.calls()) < 1 and time.monotonic() < end: time.sleep(.01)
        self.assertEqual(len(self.calls()), 1)
        changed = self.make_entry(ID, 'Guardian changed while old inference runs')
        self.update_manager(manager, [changed])
        self.assertEqual(manager.status(changed)['status'], 'queued')
        runtime.hold_path = second_release
        first_release.touch()
        end = time.monotonic() + 3
        while len(self.calls()) < 2 and time.monotonic() < end: time.sleep(.01)
        self.assertEqual(len(self.calls()), 2)
        self.assertEqual(manager.cache.status(self.entry)['status'], 'missing', 'old delayed output was saved')
        second_release.touch()
        self.assertEqual(self.wait_status(manager, changed)['status'], 'ready')
        self.assertIn('Guardian changed', self.calls()[1]['prompt'])

    def test_bounded_input_snapshot_survives_cleanup_during_runtime_prepare(self):
        import fcntl
        original = self.runtime.prepare
        def cleanup_after_snapshot():
            with (self.root / '.lock').open('a+') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                (self.root / self.entry['dialogue']).unlink()
            return original()
        self.runtime.prepare = cleanup_after_snapshot
        manager = self.manager(); manager.start([self.entry])
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'ready')
        self.assertIn('Synthetic first request', self.calls()[0]['prompt'])

    def test_close_cancels_snapshot_waiting_for_local_index_maintenance(self):
        import fcntl
        import threading
        manager = self.manager()
        with (self.root / '.lock').open('a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            manager.start([self.entry])
            self.wait_status(manager, self.entry, states=('generating',))
            self.assertFalse(self.calls(), 'inference started before index lock release')
            closer = threading.Thread(target=manager.close)
            closer.start()
            try:
                closer.join(.4)
                self.assertFalse(closer.is_alive(), 'close blocked on local index maintenance')
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)
                closer.join(3)
        self.assertFalse(self.calls())

    def test_old_digest_does_not_send_replaced_dialogue_to_provider(self):
        self.make_entry(ID, 'Replaced bytes before queued work starts')
        manager = self.manager(); manager.start([self.entry])
        self.assertEqual(self.wait_status(manager, self.entry)['status'], 'unavailable')
        self.assertFalse(self.calls(), 'old digest incorrectly inferred newer content')

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
        status = disabled.status(other)
        self.assertEqual(status['status'],'missing');self.assertEqual(len(self.calls()),1)
        self.assertNotIn('elapsed_seconds', status)
        self.assertNotIn('queue_position', status)

    def test_queue_progress_reports_position_and_phase_elapsed_time(self):
        import threading
        entered = threading.Event(); release = threading.Event()
        prepare = self.runtime.prepare
        def slow_prepare():
            entered.set()
            release.wait(5)
            return prepare()
        self.runtime.prepare = slow_prepare
        entries = [self.entry, self.make_entry('00000000-0000-4000-8000-000000000002'),
                   self.make_entry('00000000-0000-4000-8000-000000000003')]
        manager = self.manager(count=3)
        self.addCleanup(release.set)
        started = time.monotonic()
        with patch.object(self.m.time, 'monotonic', return_value=started) as clock:
            manager.start(entries)
            self.assertTrue(entered.wait(2), 'controlled preflight did not start')
            clock.return_value = started + 12.8
            waiting = manager.status(entries[1])
            self.assertEqual(waiting['status'], 'queued')
            self.assertEqual(waiting.get('queue_position'), 1)
            self.assertEqual(waiting.get('elapsed_seconds'), 12)
            self.assertEqual(manager.status(entries[2]).get('queue_position'), 2)
            active = manager.status(entries[0])
            self.assertEqual(active['status'], 'generating')
            self.assertEqual(active.get('elapsed_seconds'), 12)
            manager.request(entries[2])
            clock.return_value = started + 17.2
            self.assertEqual(manager.status(entries[2]).get('queue_position'), 1)
            self.assertEqual(manager.status(entries[2]).get('elapsed_seconds'), 17)
            self.assertEqual(manager.status(entries[1]).get('queue_position'), 2)
        release.set()
        for entry in entries:
            ready = self.wait_status(manager, entry)
            self.assertEqual(ready['status'], 'ready')
            self.assertNotIn('elapsed_seconds', ready)
            self.assertNotIn('queue_position', ready)

    def test_malformed_output_and_one_attempt_per_opening(self):
        manager=self.manager(runtime=self.runtime_for('bad'));manager.start([self.entry])
        self.assertEqual(self.wait_status(manager,self.entry)['status'],'unavailable')
        self.assertNotIn('elapsed_seconds', manager.status(self.entry))
        manager.request(self.entry);time.sleep(.05);self.assertEqual(len(self.calls()),1)
        self.assertEqual(self.m.RecapCache(self.root,'synthetic-model').status(self.entry)['status'],'missing')

    def test_closing_manager_ends_active_and_queued_progress(self):
        other = self.make_entry('00000000-0000-4000-8000-000000000002')
        manager = self.manager(count=2, runtime=self.runtime_for('sleep'))
        manager.start([self.entry, other])
        end = time.monotonic() + 3
        while not self.calls() and time.monotonic() < end:
            time.sleep(.02)
        self.assertTrue(self.calls(), 'controlled generation did not start')
        self.assertEqual(manager.status(other)['status'], 'queued')
        manager.close()
        for entry in (self.entry, other):
            status = manager.status(entry)
            self.assertNotIn(status['status'], ('generating', 'queued'))
            self.assertNotIn('elapsed_seconds', status)
            self.assertNotIn('queue_position', status)

    def test_auth_and_rate_failures_stop_batch(self):
        for mode in ('auth','rate'):
            with self.subTest(mode=mode):
                self.log.unlink(missing_ok=True)
                entries=[self.entry,self.make_entry('00000000-0000-4000-8000-000000000002')]
                manager=self.manager(runtime=self.runtime_for(mode));manager.start(entries)
                self.assertEqual(self.wait_status(manager,entries[0])['status'],'unavailable')
                time.sleep(.08);self.assertEqual(len(self.calls()),1)
                self.assertEqual(manager.status(entries[1])['status'],'unavailable')
                self.assertNotIn('elapsed_seconds', manager.status(entries[1]))
                self.assertNotIn('queue_position', manager.status(entries[1]))
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
        self.assertNotIn('elapsed_seconds', manager.status(self.entry))
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
        end = time.monotonic() + 1
        while True:
            try:
                state = stat_file.read_text().split()[2]
            except FileNotFoundError:
                break
            if state == 'Z':
                break
            if time.monotonic() >= end:
                self.fail('descendant still running after cancellation: ' + state)
            time.sleep(.01)

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
