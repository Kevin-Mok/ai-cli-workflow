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
        result = subprocess.run([sys.executable, str(fixture)], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn('query, selection, Ctrl-G, cancellation and worker cleanup passed', result.stdout)


if __name__ == '__main__':
    unittest.main()
