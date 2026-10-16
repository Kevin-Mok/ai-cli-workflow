"""Socket discovery and execution-once checks for the runner's terminal opener."""
import importlib.util
import subprocess
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / 'dot_agents/skills/metaprompt-run/scripts/open_thread.py'
spec = importlib.util.spec_from_file_location('metaprompt_open_thread', SOURCE)
opener = importlib.util.module_from_spec(spec)
spec.loader.exec_module(opener)

THREAD = '00000000-0000-4000-8000-000000000001'
TITLE = 'Fix metaprompt terminal navigation'


def tree(title=TITLE, command=None):
    return [{'id': 9, 'tabs': [{'id': 4, 'is_active': True, 'windows': [
        {'id': 7, 'title': title, 'foreground_processes': [{'cmdline': command or []}]}]}]}]


class OpenThreadTests(unittest.TestCase):
    def test_remote_inherited_endpoint_is_never_probed(self):
        with patch.dict(opener.os.environ, {'KITTY_LISTEN_ON': 'tcp:remote.example:1234'}), patch.object(opener.Path, 'glob', return_value=[]):
            self.assertEqual(opener.socket_addresses(), [])

    def test_socket_discovery_keeps_only_owned_local_sockets(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'kitty-test'
            regular = Path(folder) / 'kitty-regular'
            regular.write_text('not a socket')
            with socket.socket(socket.AF_UNIX) as server:
                server.bind(str(path))
                with patch.dict(opener.os.environ, {'KITTY_LISTEN_ON': 'unix:' + str(path)}), patch.object(opener.Path, 'glob', return_value=[path, regular]):
                    self.assertEqual(opener.socket_addresses(), ['unix:' + str(path)])
                with patch.object(opener.os, 'getuid', return_value=-1), patch.object(opener.Path, 'glob', return_value=[path]):
                    self.assertEqual(opener.socket_addresses(), [])

    def test_stale_inherited_socket_finds_unique_live_source(self):
        with patch.object(opener, 'socket_addresses', return_value=['unix:/tmp/dead', 'unix:/tmp/live']), patch.object(opener, 'kitty_tree', side_effect=lambda _, address: None if address.endswith('dead') else tree('⠦ ' + TITLE)):
            self.assertEqual(opener.find_source('kitten', TITLE), ('unix:/tmp/live', 4, 7))

    def test_ambiguous_titles_do_not_choose_any_terminal(self):
        with patch.object(opener, 'socket_addresses', return_value=['a', 'b']), patch.object(opener, 'kitty_tree', return_value=tree()):
            with self.assertRaisesRegex(opener.NavigationError, '2 source windows'):
                opener.find_source('kitten', TITLE)

    def test_reachable_unrelated_terminal_is_not_a_fallback(self):
        with patch.object(opener, 'socket_addresses', return_value=['a']), patch.object(opener, 'kitty_tree', return_value=tree('Unrelated task')):
            with self.assertRaisesRegex(opener.NavigationError, '0 source windows'):
                opener.find_source('kitten', TITLE)

    def test_resume_uses_existing_id_exact_cwd_and_source_tab(self):
        cwd = '/tmp/workspace with ü and spaces'
        launched = tree(command=['/bin/codex', 'resume', THREAD])
        with patch.object(opener.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '7\n', '')) as run, patch.object(opener, 'kitty_tree', side_effect=[None, launched]):
            self.assertEqual(opener.launch('kitten', '/bin/codex', 'unix:/tmp/live', 4, 2, cwd, THREAD), 7)
        args = run.call_args_list[0].args[0]
        self.assertEqual(args[-3:], ['/bin/codex', 'resume', THREAD])
        self.assertEqual(args[args.index('--cwd') + 1], cwd)
        self.assertIn('id:4', args)
        self.assertIn('id:2', args)

    def test_created_window_without_resume_command_is_not_verified(self):
        with patch.object(opener.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '7\n', '')), patch.object(opener, 'kitty_tree', return_value=tree(command=['/bin/false'])), patch.object(opener.time, 'sleep'):
            with self.assertRaisesRegex(opener.NavigationError, 'not verified'):
                opener.launch('kitten', '/bin/codex', 'unix:/tmp/live', 4, 2, '/tmp', THREAD)

    def test_existing_executor_tab_is_focused_without_another_launch(self):
        attached = tree(command=['/bin/codex', 'resume', THREAD])
        with patch.object(opener.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run, patch.object(opener, 'kitty_tree', return_value=attached):
            self.assertEqual(opener.launch('kitten', '/bin/codex', 'live', 4, 2, '/tmp', THREAD), 7)
        self.assertEqual(run.call_count, 1)
        self.assertIn('focus-window', run.call_args.args[0])

    def test_launch_failure_does_not_retry_or_resend_prompt(self):
        with patch.object(opener.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', 'launch denied')) as run, patch.object(opener, 'kitty_tree', return_value=None):
            with self.assertRaisesRegex(opener.NavigationError, 'launch denied'):
                opener.launch('kitten', '/bin/codex', 'unix:/tmp/live', 4, 2, '/tmp', THREAD)
        self.assertEqual(run.call_count, 1)


if __name__ == '__main__':
    unittest.main()
