"""Bounded, best-effort startup contracts using synthetic session archives."""
from contextlib import redirect_stderr
import fcntl
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ID1 = '00000000-0000-4000-8000-000000000001'
ID2 = '00000000-0000-4000-8000-000000000002'
ID3 = '00000000-0000-4000-8000-000000000003'


class IndexStartupTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('index_startup_test', ROOT / 'scripts/codex_search_index.py')
        self.index = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.index)
        self.temp = tempfile.TemporaryDirectory(prefix='codex-startup-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / 'home'
        self.sessions = self.home / 'sessions'
        self.sessions.mkdir(parents=True)
        self.cache = self.base / 'cache'
        self.cache.mkdir(mode=0o700)

    def session(self, name='2026/10/09/one.jsonl', sid=ID1, timestamp='2026-10-09T12:00:00Z', tail=b''):
        path = self.sessions / name
        path.parent.mkdir(parents=True, exist_ok=True)
        row = {'type': 'session_meta', 'timestamp': timestamp,
               'payload': {'id': sid, 'cwd': '/synthetic/project', 'timestamp': timestamp}}
        path.write_bytes(json.dumps(row).encode() + b'\n' + tail)
        return path

    def startup(self, **kwargs):
        self.assertTrue(hasattr(self.index, 'initial_recent'), 'bounded initial_recent API is required')
        return self.index.initial_recent(self.cache, self.home, **kwargs)

    def bounded_refresh(self, **kwargs):
        self.assertIn('max_updates', self.index.refresh.__code__.co_varnames,
                      'refresh must support bounded background passes')
        return self.index.refresh(self.cache, self.home, details=False, **kwargs)

    def test_prepare_cache_does_not_acquire_an_index_lock(self):
        self.assertTrue(hasattr(self.index, 'prepare_cache'), 'prepare_cache API is required')
        with patch.dict(os.environ, {'XDG_CACHE_HOME': str(self.base / 'xdg')}), \
                patch.object(self.index.fcntl, 'flock', side_effect=AssertionError('startup took a lock')):
            root = self.index.prepare_cache(self.home)
        self.assertEqual(stat.S_IMODE(root.stat().st_mode), 0o700)
        self.assertFalse((root / '.lock').exists())
        with patch.dict(os.environ, {'XDG_CACHE_HOME': str(self.base / 'xdg')}):
            with self.index.cache_lock(self.home) as locked:
                self.assertEqual(locked, root)

    def test_cached_startup_returns_without_waiting_or_rewriting_manifest(self):
        source = self.session()
        cached = self.index.refresh(self.cache, self.home)
        original = (self.cache / 'manifest.json').read_bytes()
        with (self.cache / '.lock').open('w') as locked:
            fcntl.flock(locked, fcntl.LOCK_EX)
            with patch.object(self.index.fcntl, 'flock', side_effect=AssertionError('startup took a lock')), \
                    patch.object(self.index, 'extract', side_effect=AssertionError('startup parsed dialogue')):
                result = self.startup()
        self.assertEqual(result[str(source)]['source'], str(source))
        self.assertEqual(result[str(source)]['dialogue_hash'], cached[str(source)]['dialogue_hash'])
        self.assertEqual((self.cache / 'manifest.json').read_bytes(), original)

    def test_cold_startup_reads_only_native_headers_and_creates_no_dialogue(self):
        older = self.session('2026/07/01/old.jsonl', sid=ID2)
        newest = self.session(tail=b'{' + b'x' * (2 * 1024 * 1024))
        before = newest.read_bytes()
        with patch.object(self.index, 'extract', side_effect=AssertionError('startup parsed dialogue')):
            result = self.startup(limit=1)
        self.assertEqual(set(result), {str(newest)})
        entry = result[str(newest)]
        self.assertEqual(entry['id'], ID1)
        self.assertEqual(entry['source'], str(newest))
        self.assertTrue(entry['index_pending'])
        self.assertEqual(entry['dialogue'], '')
        self.assertEqual(entry['dialogue_hash'], '')
        self.assertEqual(list(self.cache.iterdir()), [])
        self.assertEqual(newest.read_bytes(), before)
        self.assertTrue(older.exists())

    def test_cold_startup_skips_broken_headers_and_enforces_read_budget(self):
        valid = self.session('2026/10/07/valid.jsonl', sid=ID2)
        malformed = self.sessions / '2026/10/09/malformed.jsonl'
        malformed.parent.mkdir(parents=True, exist_ok=True)
        malformed.write_bytes(b'\xff\n{bad\n')
        hidden = self.session('2026/10/08/late.jsonl', sid=ID3)
        hidden.write_bytes(b'x' * (70 * 1024) + b'\n' + hidden.read_bytes())
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = self.startup()
        self.assertEqual(set(result), {str(valid)})
        self.assertEqual(stderr.getvalue(), '')

    def test_invalid_manifest_falls_back_quietly_but_symlink_is_fatal(self):
        source = self.session()
        manifest = self.cache / 'manifest.json'
        manifest.write_bytes(b'\xffinvalid')
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(set(self.startup()), {str(source)})
        self.assertEqual(stderr.getvalue(), '')
        manifest.unlink()
        outside = self.base / 'outside.json'
        outside.write_text('{}')
        manifest.symlink_to(outside)
        with self.assertRaises(self.index.SearchError):
            self.startup()

    def test_cached_startup_marks_missing_dialogue_pending_and_rejects_unsafe_cache(self):
        source = self.session()
        entry = self.index.refresh(self.cache, self.home)[str(source)]
        dialogue = self.cache / entry['dialogue']
        dialogue.unlink()
        self.assertTrue(self.startup()[str(source)]['index_pending'])
        outside = self.base / 'outside-dialogue'
        outside.write_text('private')
        dialogue.symlink_to(outside)
        with self.assertRaises(self.index.SearchError):
            self.startup()

    def test_bounded_refresh_prioritizes_newest_and_reports_unindexed_inventory(self):
        sources = [self.session(f'2026/10/0{day}/session.jsonl', sid=sid)
                   for day, sid in ((1, ID1), (2, ID2), (3, ID3))]
        for number, source in enumerate(sources):
            os.utime(source, ns=(1_000_000_000 + number, 1_000_000_000 + number))
        stats = {}
        result = self.bounded_refresh(max_updates=2, stats=stats)
        self.assertEqual(set(result), {str(sources[1]), str(sources[2])})
        self.assertEqual(set(stats['sources']), {str(path) for path in sources})
        self.assertEqual(stats['pending_sources'], [str(sources[0])])
        self.assertEqual((stats['total'], stats['pending'], stats['refreshed']), (3, 1, 2))
        second = self.bounded_refresh(max_updates=2, stats=stats)
        self.assertEqual(set(second), {str(path) for path in sources})
        self.assertEqual((stats['pending'], stats['refreshed']), (0, 1))

    def test_changed_unprocessed_cache_remains_pending_with_original_evidence(self):
        old = self.session('2026/10/01/old.jsonl')
        first = self.index.refresh(self.cache, self.home)[str(old)]
        with old.open('ab') as out:
            out.write(b'{incomplete tail')
        newest = self.session('2026/10/09/new.jsonl', sid=ID2)
        os.utime(old, ns=(1, 1))
        os.utime(newest, ns=(2, 2))
        stats = {}
        pending = self.bounded_refresh(max_updates=1, stats=stats)[str(old)]
        self.assertTrue(pending['index_pending'])
        for key in ('signature', 'dialogue', 'dialogue_hash'):
            self.assertEqual(pending[key], first[key])
        self.assertTrue((self.cache / first['dialogue']).exists())
        self.assertNotIn('source', self.index.load_manifest(self.cache, self.home)[str(old)])
        ready = self.bounded_refresh(max_updates=1, stats=stats)[str(old)]
        self.assertFalse(ready.get('index_pending', False))
        self.assertEqual(ready['signature'], self.index.signature(old))
        self.assertEqual(stats['skipped'], 1)

    def test_preferred_pending_source_is_processed_before_newer_source(self):
        old = self.session('2026/10/01/old.jsonl')
        new = self.session('2026/10/09/new.jsonl', sid=ID2)
        os.utime(old, ns=(1, 1))
        os.utime(new, ns=(2, 2))
        result = self.bounded_refresh(max_updates=1, preferred_sources=[str(old)])
        self.assertEqual(set(result), {str(old)})

    def test_quiet_refresh_and_optional_titles_skip_malformed_neighbors(self):
        source = self.session(tail=b'{malformed\n')
        (self.home / 'session_index.jsonl').write_text(
            '{bad\n' + json.dumps({'id': ID1, 'thread_name': 'Valid title'}) + '\n')
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = self.bounded_refresh(max_updates=20)
            again = self.bounded_refresh(max_updates=20)
            self.assertEqual(self.startup()[str(source)]['skipped'], 1)
            self.assertEqual(self.index.titles(self.home, details=False), {ID1: 'Valid title'})
        self.assertEqual(result[str(source)]['skipped'], 1)
        self.assertEqual(again[str(source)]['skipped'], 1)
        self.assertEqual(stderr.getvalue(), '')

    def test_deleted_source_is_removed_from_inventory_and_pending_cache(self):
        deleted = self.session()
        survivor = self.session('2026/10/08/survivor.jsonl', sid=ID2)
        first = self.index.refresh(self.cache, self.home)
        deleted.unlink()
        stats = {}
        result = self.bounded_refresh(max_updates=0, stats=stats)
        self.assertEqual(set(result), {str(survivor)})
        self.assertEqual(stats['sources'], [str(survivor)])
        self.assertFalse((self.cache / first[str(deleted)]['dialogue']).exists())

    def test_time_budget_stops_between_sources_and_does_not_erase_pending(self):
        newest = self.session(sid=ID1)
        older = self.session('2026/10/08/old.jsonl', sid=ID2)
        os.utime(newest, ns=(2, 2))
        os.utime(older, ns=(1, 1))
        stats = {}
        # The first source is processed at t=0; the next pass check is over budget.
        with patch.object(self.index.time, 'monotonic', side_effect=[0.0, 0.0, 1.1]):
            result = self.bounded_refresh(max_updates=20, stats=stats)
        self.assertEqual(set(result), {str(newest)})
        self.assertEqual(stats['pending_sources'], [str(older)])

    def test_unreadable_source_keeps_cached_metadata_pending_and_inventory(self):
        source = self.session()
        first = self.index.refresh(self.cache, self.home)[str(source)]
        real_signature = self.index.signature

        def unreadable(path):
            if path == source:
                raise PermissionError('synthetic source permission failure')
            return real_signature(path)

        stats = {}
        with patch.object(self.index, 'signature', side_effect=unreadable):
            startup = self.startup()
            result = self.bounded_refresh(max_updates=20, stats=stats)
        self.assertTrue(startup[str(source)]['index_pending'])
        self.assertTrue(result[str(source)]['index_pending'])
        self.assertEqual(result[str(source)]['dialogue_hash'], first['dialogue_hash'])
        self.assertEqual(stats['sources'], [str(source)])
        self.assertEqual(stats['unreadable'], 1)
        self.assertEqual(stats['pending'], 1)

    def test_failed_extraction_preserves_cached_evidence_without_hiding_neighbors(self):
        source = self.session()
        first = self.index.refresh(self.cache, self.home)[str(source)]
        with source.open('ab') as out:
            out.write(b'{partial')
        neighbor = self.session('2026/10/08/neighbor.jsonl', sid=ID2)
        real_extract = self.index.extract

        def unreadable(path, *args, **kwargs):
            if path == source:
                raise PermissionError('synthetic source read failure')
            return real_extract(path, *args, **kwargs)

        stats = {}
        with patch.object(self.index, 'extract', side_effect=unreadable):
            result = self.bounded_refresh(max_updates=20, stats=stats)
        self.assertEqual(set(result), {str(source), str(neighbor)})
        self.assertTrue(result[str(source)]['index_pending'])
        self.assertEqual(result[str(source)]['dialogue_hash'], first['dialogue_hash'])
        self.assertEqual(stats['unreadable'], 1)

    def test_incomplete_discovery_preserves_cached_sources_and_reports_uncertainty(self):
        source = self.session()
        self.index.refresh(self.cache, self.home)
        folder = source.parent

        def incomplete_walk(root, onerror, followlinks):
            error = PermissionError('synthetic directory read failure')
            error.filename = str(folder)
            onerror(error)
            return iter(())

        stats = {}
        with patch.object(self.index.os, 'walk', side_effect=incomplete_walk):
            result = self.bounded_refresh(max_updates=20, stats=stats)
        self.assertTrue(result[str(source)]['index_pending'])
        self.assertIn(str(source), stats['sources'])
        self.assertTrue(stats['discovery_incomplete'])
        self.assertEqual(stats['unreadable_directories'], [str(folder)])

    def test_cold_startup_limits_candidates_even_when_clock_does_not_advance(self):
        # A clock-independent bound also protects archives full of broken headers.
        self.session('2026/01/01/valid.jsonl')
        broken = self.sessions / '2026/10/09'
        broken.mkdir(parents=True, exist_ok=True)
        for number in range(1001):
            (broken / f'{number:04}.jsonl').write_text('{broken')
        with patch.object(self.index.time, 'monotonic', return_value=0.0):
            result = self.startup()
        self.assertEqual(result, {})

    def test_failed_extractions_count_toward_pass_limit(self):
        sources = [self.session(f'2026/10/09/{number}.jsonl') for number in range(6)]
        stats = {}
        with patch.object(self.index, 'extract', side_effect=PermissionError('synthetic read failure')) as extract:
            result = self.bounded_refresh(max_updates=2, stats=stats)
        self.assertEqual(result, {})
        self.assertEqual(extract.call_count, 2)
        self.assertEqual(set(stats['sources']), {str(source) for source in sources})
        self.assertEqual((stats['pending'], stats['unreadable'], stats['refreshed']), (6, 2, 0))

    def test_bounded_zero_pass_still_rejects_unsafe_cached_dialogue(self):
        source = self.session()
        entry = self.index.refresh(self.cache, self.home)[str(source)]
        dialogue = self.cache / entry['dialogue']
        dialogue.unlink()
        dialogue.symlink_to(self.base / 'missing-outside-dialogue')
        with self.assertRaises(self.index.SearchError):
            self.bounded_refresh(max_updates=0)

    def test_bounded_title_lookup_reads_at_most_cap_and_keeps_newest_titles(self):
        self.assertIn('max_bytes', self.index.titles.__code__.co_varnames,
                      'startup title lookup must accept a byte budget')
        path = self.home / 'session_index.jsonl'
        old = json.dumps({'id': ID2, 'thread_name': 'Outside the recent tail'}) + '\n'
        latest = json.dumps({'id': ID1, 'thread_name': 'Newest title'}) + '\n'
        path.write_text(old + ('{malformed padding\n' * 70000) + latest)
        real_open = Path.open
        read_bytes = []

        class CountingFile:
            def __init__(self, source):
                self.source = source

            def __enter__(self):
                self.source.__enter__()
                return self

            def __exit__(self, *args):
                return self.source.__exit__(*args)

            def __getattr__(self, name):
                return getattr(self.source, name)

            def read(self, size=-1):
                self.assert_budget(size)
                result = self.source.read(size)
                read_bytes.append(len(result))
                return result

            @staticmethod
            def assert_budget(size):
                if not 0 <= size <= 1024 * 1024:
                    raise AssertionError('title startup requested an unbounded read')

        def counted_open(candidate, *args, **kwargs):
            source = real_open(candidate, *args, **kwargs)
            return CountingFile(source) if candidate == path else source

        with patch.object(Path, 'open', new=counted_open):
            result = self.index.titles(self.home, details=False, max_bytes=1024 * 1024)
        self.assertEqual(result, {ID1: 'Newest title'})
        self.assertLessEqual(sum(read_bytes), 1024 * 1024)
        self.assertGreater(sum(read_bytes), 0)

    def test_bounded_titles_keep_complete_first_line_and_validate_neighbors(self):
        self.assertIn('max_bytes', self.index.titles.__code__.co_varnames,
                      'startup title lookup must accept a byte budget')
        path = self.home / 'session_index.jsonl'
        path.write_text(json.dumps({'id': ID1, 'thread_name': 'First title'}) + '\n' +
                        '{bad\n' + json.dumps({'id': [], 'thread_name': 'Invalid identity'}) + '\n' +
                        json.dumps({'id': ID2, 'thread_name': 'Second title'}) + '\n')
        result = self.index.titles(self.home, details=False, max_bytes=1024 * 1024)
        self.assertEqual(result, {ID1: 'First title', ID2: 'Second title'})

    def test_bounded_titles_skip_partial_leading_record_without_warning(self):
        self.assertIn('max_bytes', self.index.titles.__code__.co_varnames,
                      'startup title lookup must accept a byte budget')
        path = self.home / 'session_index.jsonl'
        newest = json.dumps({'id': ID1, 'thread_name': 'Latest'}) + '\n'
        path.write_text(json.dumps({'id': ID2, 'thread_name': 'x' * 1000}) + '\n' + newest)
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = self.index.titles(self.home, max_bytes=len(newest) + 10)
        self.assertEqual(result, {ID1: 'Latest'})
        self.assertEqual(stderr.getvalue(), '')

    def test_optional_titles_skip_non_regular_index_without_opening_it(self):
        path = self.home / 'session_index.jsonl'
        os.mkfifo(path)
        with patch.object(Path, 'open', side_effect=AssertionError('opening a FIFO can block startup')):
            self.assertEqual(self.index.titles(self.home, details=False, max_bytes=1024), {})

    def test_optional_title_stat_failure_is_quiet_and_recoverable(self):
        path = self.home / 'session_index.jsonl'
        path.write_text('{}\n')
        real_stat = Path.stat

        def unreadable(candidate, *args, **kwargs):
            if candidate == path:
                raise PermissionError('synthetic title metadata failure')
            return real_stat(candidate, *args, **kwargs)

        stderr = io.StringIO()
        with patch.object(Path, 'stat', new=unreadable), redirect_stderr(stderr):
            self.assertEqual(self.index.titles(self.home, details=False, max_bytes=1024), {})
        self.assertEqual(stderr.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
