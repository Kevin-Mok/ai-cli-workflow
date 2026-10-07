"""Synthetic contracts for recent-session indexing and normalized dialogue."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'scripts/codex_search_index.py'
ID1 = '00000000-0000-4000-8000-000000000001'
ID2 = '00000000-0000-4000-8000-000000000002'


def record(kind, payload, timestamp='2026-10-01T12:00:00Z'):
    return {'timestamp': timestamp, 'type': kind, 'payload': payload}


def message(role, text, timestamp='2026-10-01T12:00:00Z'):
    return record('response_item', {'type': 'message', 'role': role,
                  'content': [{'type': 'input_text' if role == 'user' else 'output_text', 'text': text}]}, timestamp)


def event(role, text, timestamp='2026-10-01T12:00:00Z'):
    return record('event_msg', {'type': 'user_message' if role == 'user' else 'agent_message',
                              'message': text}, timestamp)


class CodexSearchIndexTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.is_file(), 'shared session index implementation is missing')
        spec = importlib.util.spec_from_file_location('codex_search_index_test', MODULE)
        self.index = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.index)
        self.temp = tempfile.TemporaryDirectory(prefix='codex-search-index-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / 'home'
        self.sessions = self.home / 'sessions'
        self.sessions.mkdir(parents=True)
        self.cache = self.base / 'cache'
        self.cache.mkdir(mode=0o700)

    def session(self, name='one.jsonl', sid=ID1, cwd='/project/one',
                created='2026-10-01T00:00:00Z', rows=()):
        path = self.sessions / name
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [record('session_meta', {'id': sid, 'cwd': cwd, 'timestamp': created}, created), *rows]
        path.write_text(''.join(json.dumps(row, ensure_ascii=True) + '\n' for row in payload))
        return path

    def extract(self, path):
        return self.index.extract(path, self.cache, self.index.signature(path))

    def dialogue(self, entry):
        return [json.loads(line) for line in (self.cache / entry['dialogue']).read_text().splitlines()]

    def test_recent_uses_activity_offsets_across_directories_and_deduplicates_uuid(self):
        old = self.session('old/one.jsonl', cwd='/old-copy', rows=[message('user', 'first')])
        active = self.session('elsewhere/newer.jsonl', cwd='/project/active',
                              rows=[message('user', 'still working', '2026-10-05T01:00:00-04:00')])
        other = self.session('other/two.jsonl', sid=ID2, cwd='/project/two',
                             created='2026-10-05T04:30:00Z',
                             rows=[message('user', 'newly created', '2026-10-05T04:30:00Z')])
        os.utime(old, (2000000000, 2000000000))
        entries = self.index.refresh(self.cache, self.home)
        recent = self.index.recent_entries(entries)
        self.assertEqual([entry['id'] for entry, _ in recent], [ID1, ID2])
        self.assertEqual(recent[0][0]['cwd'], '/project/active')
        self.assertEqual(recent[0][0]['timestamp'], '2026-10-05T01:00:00-04:00')
        self.assertEqual([snippets for _, snippets in recent], [[], []])
        self.assertEqual(set(entries), {str(old), str(active), str(other)})
        os.utime(self.cache / recent[1][0]['dialogue'], (2100000000, 2100000000))
        self.assertEqual([entry['id'] for entry, _ in self.index.recent_entries(entries)], [ID1, ID2])

    def test_latest_record_compares_epoch_not_timestamp_text(self):
        path = self.session(rows=[message('user', 'latest', '2026-10-05T01:00:00-04:00'),
                                  message('assistant', 'older clock text', '2026-10-05T04:30:00Z')])
        self.assertEqual(self.extract(path)['timestamp'], '2026-10-05T01:00:00-04:00')

    def test_dialogue_keeps_roles_order_and_event_only_messages_without_mirrors(self):
        path = self.session(rows=[
            event('user', 'First café'), message('user', 'First café'),
            event('assistant', 'Event-only middle'),
            message('user', 'Second question'), event('user', 'Second question'),
            event('assistant', 'Final reply'), message('assistant', 'Final reply'),
        ])
        entry = self.extract(path)
        expected = [
            {'role': 'user', 'text': 'First café'},
            {'role': 'assistant', 'text': 'Event-only middle'},
            {'role': 'user', 'text': 'Second question'},
            {'role': 'assistant', 'text': 'Final reply'},
        ]
        self.assertEqual(self.dialogue(entry), expected)
        canonical = ('{"role":"user","text":"First café"}\n'
                     '{"role":"assistant","text":"Event-only middle"}\n'
                     '{"role":"user","text":"Second question"}\n'
                     '{"role":"assistant","text":"Final reply"}\n').encode('utf-8')
        self.assertEqual((self.cache / entry['dialogue']).read_bytes(), canonical)
        self.assertEqual(entry['dialogue_hash'], hashlib.sha256(canonical).hexdigest())
        self.assertEqual((self.cache / entry['conversation']).read_text(),
                         'First café\nEvent-only middle\nSecond question\nFinal reply\n')

    def test_dialogue_excludes_context_reasoning_tools_and_keeps_ide_request(self):
        path = self.session(rows=[
            message('system', 'system private'), message('developer', 'developer private'),
            message('user', '# AGENTS.md instructions\nprivate rules'),
            event('user', '<environment_context>private setup</environment_context>'),
            message('user', '# AGENTS.md instructions\nprivate\n## My request for Codex:\nFix the parser'),
            record('response_item', {'type': 'reasoning', 'text': 'private reasoning'}),
            record('turn_context', {'text': 'private turn'}),
            record('response_item', {'type': 'function_call_output', 'output': 'Tool result marker'}),
            message('assistant', 'Parser work started'),
        ])
        entry = self.extract(path)
        self.assertEqual(self.dialogue(entry), [{'role': 'user', 'text': 'Fix the parser'},
                                               {'role': 'assistant', 'text': 'Parser work started'}])
        self.assertIn('Tool result marker', (self.cache / entry['tools']).read_text())
        self.assertNotIn('Tool result marker', (self.cache / entry['conversation']).read_text())

    def test_hash_ignores_tool_and_metadata_changes_but_tracks_full_dialogue(self):
        path = self.session(rows=[message('user', 'Initial request'), message('assistant', 'Progress')])
        first = self.extract(path)
        with path.open('a') as out:
            out.write(json.dumps(record('response_item', {'type': 'function_call_output',
                                                         'output': 'changed tool output'}, '2026-10-07T00:00:00Z')) + '\n')
            out.write(json.dumps(record('turn_context', {'cwd': '/different'})) + '\n')
        second = self.extract(path)
        self.assertEqual(second['dialogue_hash'], first['dialogue_hash'])
        self.assertNotEqual(second['timestamp'], first['timestamp'])
        with path.open('a') as out:
            out.write(json.dumps(message('assistant', 'New progress')) + '\n')
        third = self.extract(path)
        self.assertNotEqual(third['dialogue_hash'], second['dialogue_hash'])
        self.assertEqual(self.dialogue(third)[-1], {'role': 'assistant', 'text': 'New progress'})

    def test_malformed_records_keep_valid_neighbors_and_repeated_turns(self):
        path = self.session(rows=[
            message('user', 'Repeat'), message('assistant', 'Acknowledged'), message('user', 'Repeat'),
            record([], {}), record('event_msg', {'type': []}),
            message('user', '\ud800'), message('assistant', 'Final valid reply'),
        ])
        with path.open('a') as out:
            out.write('{malformed tail')
        entry = self.extract(path)
        self.assertEqual(entry['skipped'], 4)
        self.assertEqual(self.dialogue(entry), [
            {'role': 'user', 'text': 'Repeat'}, {'role': 'assistant', 'text': 'Acknowledged'},
            {'role': 'user', 'text': 'Repeat'}, {'role': 'assistant', 'text': 'Final valid reply'}])

    def test_refresh_reuses_private_dialogue_rebuilds_missing_and_preserves_recaps(self):
        source = self.session(rows=[message('user', 'Original')])
        original = source.read_bytes()
        source_stat = self.index.signature(source)
        entry = self.index.refresh(self.cache, self.home)[str(source)]
        dialogue = self.cache / entry['dialogue']
        signature = self.index.signature(dialogue)
        recaps = self.cache / 'recaps'
        recaps.mkdir(mode=0o700)
        retained = recaps / 'generation.lock'
        retained.write_text('retained')
        again = self.index.refresh(self.cache, self.home)[str(source)]
        self.assertEqual(again, entry)
        reused_signature = self.index.signature(dialogue)
        # Permission hardening can update ctime without rewriting the cache.
        self.assertEqual(reused_signature[:2] + reused_signature[3:],
                         signature[:2] + signature[3:])
        self.assertEqual(self.dialogue(again), [{'role': 'user', 'text': 'Original'}])
        self.assertEqual(retained.read_text(), 'retained')
        self.assertEqual(stat.S_IMODE(dialogue.stat().st_mode), 0o600)
        dialogue.unlink()
        rebuilt = self.index.refresh(self.cache, self.home)[str(source)]
        self.assertNotEqual(rebuilt['dialogue'], entry['dialogue'])
        self.assertEqual(rebuilt['dialogue_hash'], entry['dialogue_hash'])
        self.assertFalse((self.cache / entry['conversation']).exists())
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(self.index.signature(source), source_stat)

    def test_manifest_rejects_invalid_dialogue_filename_hash_and_old_format(self):
        source = self.session(rows=[message('user', 'Request')])
        entries = self.index.refresh(self.cache, self.home)
        manifest = self.cache / 'manifest.json'
        valid = json.loads(manifest.read_text())
        for change in ({'dialogue': '../outside.jsonl'}, {'dialogue_hash': 'not-a-hash'},
                       {'dialogue_hash': None}):
            with self.subTest(change=change):
                data = json.loads(json.dumps(valid))
                data['sources'][str(source)].update(change)
                manifest.write_text(json.dumps(data))
                self.assertEqual(self.index.load_manifest(self.cache, self.home), {})
        valid['version'] = 1
        manifest.write_text(json.dumps(valid))
        self.assertEqual(self.index.load_manifest(self.cache, self.home), {})
        self.assertEqual(len(entries), 1)


if __name__ == '__main__':
    unittest.main()
