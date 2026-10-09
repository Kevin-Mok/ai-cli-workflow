"""Recent picker contracts using synthetic sessions and deterministic recaps."""
import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'codex_search_recent.py'
ID1 = '00000000-0000-4000-8000-000000000001'
ID2 = '00000000-0000-4000-8000-000000000002'


class FakeManager:
    """Inference boundary only; fzf, files, callbacks and rendering stay real."""
    model = 'synthetic-model'

    def __init__(self, status=None):
        self.value = status or {'status': 'missing', 'recap': None, 'partial': False, 'detail': ''}
        self.started = False
        self.closed = False
        self.requests = []

    def start(self, entries):
        self.started = True

    def request(self, entry):
        self.requests.append(entry['id'])

    def status(self, entry):
        return self.value

    def close(self):
        self.closed = True


class RecentPickerTest(unittest.TestCase):
    def test_activity_displays_toronto_time_in_row_and_preview(self):
        for stamp, short, expected in (
            ('2026-10-08T16:17:14.030Z', 'Oct 8 12:17', '2026-10-08 12:17:14.030-04:00 (EDT)'),
            ('2026-01-08T16:17:14.030Z', 'Jan 8 11:17', '2026-01-08 11:17:14.030-05:00 (EST)'),
            ('2026-10-08T02:17:14Z', 'Oct 7 22:17', '2026-10-07 22:17:14-04:00 (EDT)'),
        ):
            with self.subTest(stamp=stamp):
                entry = dict(self.entry, timestamp=stamp)
                row, preview = self.module.render_session(entry, 'Synthetic task', FakeManager().value)
                self.assertEqual(row.split('\t')[1], short)
                self.assertIn('Activity: ' + expected, preview)
                self.assertEqual(entry['timestamp'], stamp)

    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'recent picker module is missing')
        sys.path.insert(0, str(ROOT / 'scripts'))
        self.addCleanup(lambda: sys.path.remove(str(ROOT / 'scripts')))
        self.module = importlib.import_module('codex_search_recent')
        temporary = tempfile.TemporaryDirectory(prefix='recent-picker-test-')
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.cache = self.base / 'cache'
        self.cache.mkdir(mode=0o700)
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.entry = {'id': ID1, 'cwd': str(self.base), 'timestamp': '2026-10-07T15:00:00Z',
                      'conversation': '1' * 32 + '.conversation.txt',
                      'dialogue': '1' * 32 + '.dialogue.jsonl'}
        (self.cache / self.entry['conversation']).write_text('Initial synthetic request\nLatest synthetic reply\n')
        (self.cache / self.entry['dialogue']).write_text(json.dumps({'role': 'user', 'text': 'Initial synthetic request'}) + '\n' +
                                                       json.dumps({'role': 'assistant', 'text': 'Latest synthetic reply'}) + '\n')

    def fzf(self, code):
        script = self.bin / 'fzf'
        script.write_text('#!' + sys.executable + '\nimport sys,os,json,time\nfrom pathlib import Path\n' + code)
        script.chmod(0o755)

    def pick(self, manager):
        with patch.dict(os.environ, {'PATH': str(self.bin) + os.pathsep + os.environ['PATH'],
                                     'FZF_DEFAULT_OPTS': '--bind=enter:execute(echo forged)',
                                     'FZF_DEFAULT_OPTS_FILE': '/missing'}):
            return self.module.pick_recent([(self.entry, [])], {ID1: 'Synthetic title'}, self.cache, manager)

    def test_guardian_review_uses_cached_ai_headline_in_row_and_preview(self):
        for state in ('ready', 'stale'):
            with self.subTest(state=state):
                status = {'status': state, 'recap': {'headline': 'Review parser edge cases'}, 'partial': False}
                row, preview = self.module.render_session(self.entry, 'Guardian review', status)
                self.assertEqual(row.split('\t')[3], 'Review parser edge cases')
                self.assertTrue(preview.startswith('Review parser edge cases\n'))
                self.assertIn('Original title: Guardian review', preview)
                self.assertIn('AI recap: ' + state, preview)

    def test_guardian_title_fallback_and_meaningful_titles_are_preserved(self):
        for title, headline, expected in (
            ('Guardian review', '', 'Guardian review'),
            ('Guardian review', None, 'Guardian review'),
            ('Guardian review', ['Bad headline'], 'Guardian review'),
            ('Guardian review', '   ', 'Guardian review'),
            (' Guardian review ', 'Audit shell quoting', 'Audit shell quoting'),
            ('guardian REVIEW', 'Audit shell quoting', 'Audit shell quoting'),
            ('Implement fast directory sizes', 'Review parser', 'Implement fast directory sizes'),
        ):
            with self.subTest(title=title, headline=headline):
                status = {'status': 'ready', 'recap': {'headline': headline}}
                row, preview = self.module.render_session(self.entry, title, status)
                self.assertEqual(row.split('\t')[3], expected)
                self.assertTrue(preview.startswith(expected + '\n'))

    def test_untitled_rows_adopt_ai_headlines(self):
        for title in ('', '   ', '(untitled)', ' (UNTITLED) '):
            with self.subTest(title=title):
                row, preview = self.module.render_session(self.entry, title,
                    {'status': 'ready', 'recap': {'headline': 'Inspect pending title progress'}})
                self.assertEqual(row.split('\t')[3], 'Inspect pending title progress')
                self.assertIn('Original title:', preview)

    def test_generic_rows_show_queue_position_and_elapsed_generation(self):
        for title in ('Guardian review', '', '(untitled)'):
            for state, elapsed, suffix in (
                ('queued', 12, 'queued #2 12s'),
                ('generating', 65, 'generating 1m05s'),
            ):
                with self.subTest(title=title, state=state):
                    status = {'status': state, 'recap': None, 'elapsed_seconds': elapsed,
                              'queue_position': 2}
                    row, preview = self.module.render_session(self.entry, title, status)
                    self.assertEqual(row.split('\t')[3], (title or '(untitled)') + ' [' + suffix + ']')
                    self.assertIn('Recap progress: ' + suffix, preview)
                    self.assertIn('AI recap: ' + state, preview)
        row, preview = self.module.render_session(self.entry, 'Meaningful task title',
            {'status': 'generating', 'elapsed_seconds': 12})
        self.assertEqual(row.split('\t')[3], 'Meaningful task title')
        self.assertIn('Recap progress: generating 12s', preview)

    def test_generic_rows_explain_missing_disabled_and_failed_titles(self):
        for title in ('Guardian review', ''):
            for state, enabled, suffix in (
                ('missing', True, 'Ctrl-G'),
                ('missing', False, 'recaps off'),
                ('unavailable', True, 'unavailable'),
            ):
                with self.subTest(title=title, state=state, enabled=enabled):
                    row, _ = self.module.render_session(self.entry, title,
                        {'status': state, 'generation_enabled': enabled, 'recap': None})
                    self.assertEqual(row.split('\t')[3], (title or '(untitled)') + ' [' + suffix + ']')

    def test_directory_abbreviation_keeps_basename_and_full_preview(self):
        for directory, short in (
            ('/mnt/usb-8tb/', '/m/usb-8tb>'),
            ('/home/example/linux-config', '/h/k/linux-config>'),
            ('/', '/>'),
        ):
            with self.subTest(directory=directory):
                entry = dict(self.entry, cwd=directory)
                title = 'Implement fast directory sizes'
                row, preview = self.module.render_session(entry, title, FakeManager().value)
                self.assertEqual(row.split('\t')[2], short)
                self.assertEqual(row.split('\t')[3], title)
                self.assertIn('Directory: ' + directory, preview)
                self.assertTrue(preview.startswith(title + '\n'))
                self.assertEqual(entry['cwd'], directory)

    def test_selected_row_returns_trusted_entry_and_closes_before_return(self):
        self.fzf("assert 'FZF_DEFAULT_OPTS' not in os.environ\nassert 'FZF_DEFAULT_OPTS_FILE' not in os.environ\nrows=sys.stdin.read().splitlines()\nprint(rows[0])\n")
        manager = FakeManager()
        selected = self.pick(manager)
        self.assertEqual(selected, self.entry)
        self.assertTrue(manager.started)
        self.assertTrue(manager.closed)

    def test_cancellation_closes_manager_and_stderr_remains_visible(self):
        self.fzf("sys.stdin.read()\nprint('SYNTHETIC PICKER UI',file=sys.stderr)\nsys.exit(130)\n")
        manager = FakeManager()
        self.assertIsNone(self.pick(manager))
        self.assertTrue(manager.closed)

    def test_forged_complete_row_is_rejected_even_with_valid_uuid(self):
        self.fzf("sys.stdin.read()\nprint('" + ID1 + "\\tforged directory\\tforged recap')\n")
        manager = FakeManager()
        with self.assertRaisesRegex(self.module.SearchError, 'invalid selection'):
            self.pick(manager)
        self.assertTrue(manager.closed)

    def test_rows_and_preview_escape_controls_and_explain_partial_stale_recap(self):
        value = {'status': 'stale', 'partial': True, 'detail': 'Input changed', 'recap': {
            'headline': 'A headline\x1b[31m', 'goal': 'Goal text', 'progress': ['Reported step'],
            'state': 'Uncertain state', 'next_steps': ['Next step']}}
        row, preview = self.module.render_session(self.entry, 'Title\twith control', value, 'Local text')
        self.assertEqual(row.split('\t')[0], ID1)
        self.assertEqual(len(row.split('\t')), 5)
        self.assertNotIn('\x1b', row + preview)
        for label in ('stale', 'partial', 'Goal:', 'Reported progress:', 'Current state:', 'Remaining work:'):
            self.assertIn(label, preview)
        self.assertIn('A headline\\x1b[31m', row)

    def test_missing_preview_keeps_local_dialogue(self):
        _, preview = self.module.render_session(self.entry, 'Synthetic', FakeManager().value,
                                                'User: Initial request\nAssistant: Latest answer')
        self.assertIn('missing', preview)
        self.assertIn('Initial request', preview)
        self.assertIn('Latest answer', preview)

    def test_callbacks_reject_unknown_uuid_and_outside_private_runtime(self):
        public = self.base / 'public'
        public.mkdir(mode=0o755)
        result = subprocess.run([sys.executable, str(SCRIPT), '--helper', 'request', str(public), ID1],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((public / ('request-' + ID1)).exists())
        private = self.base / 'codex-search-picker-synthetic'
        private.mkdir(mode=0o700)
        self.module.atomic_json(private / 'manifest.json', {'ids': [ID1], 'root': str(self.cache)})
        result = subprocess.run([sys.executable, str(SCRIPT), '--helper', 'request', str(private), ID2],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((private / ('request-' + ID2)).exists())


@unittest.skipUnless(shutil.which('fzf'), 'real fzf is optional')
class RecentPickerTerminalTest(unittest.TestCase):
    def test_async_recap_preserves_query_and_uuid_and_ctrl_g_requests_selected(self):
        fixture = ROOT / 'tests' / 'scripts' / 'codex_recent_live_check.py'
        self.assertTrue(fixture.exists(), 'real recent picker fixture is missing')
        result = subprocess.run([sys.executable, str(fixture)], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn('query, selection, Ctrl-G, cancellation and worker cleanup passed', result.stdout)


if __name__ == '__main__':
    unittest.main()
