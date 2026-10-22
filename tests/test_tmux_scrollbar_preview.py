#!/usr/bin/env python3
"""Check that scrollbar previews cannot connect to the production server."""
import contextlib
import io
from pathlib import Path
import runpy
import sys
import unittest
from unittest.mock import patch

HELPER = Path(__file__).resolve().parents[1] / 'scripts/executable_tmux-scrollback-smoke'


class ScrollbarPreview(unittest.TestCase):
    def test_preview_uses_versioned_binary_and_disposable_socket(self):
        main = runpy.run_path(str(HELPER))['main']
        with patch.object(sys, 'argv', [str(HELPER), '--scrollbar']), \
             patch('shutil.which', return_value='/usr/bin/kitty'), \
             patch.object(Path, 'is_file', return_value=True), \
             patch('subprocess.run') as run, patch('subprocess.call', return_value=0) as call:
            self.assertEqual(main(), 0)
        binary = str(Path.home() / '.local/opt/tmux-3.8/bin/tmux')
        commands = [c.args[0] for c in run.call_args_list]
        self.assertTrue(all(c[0] == binary and c[1] == '-S' for c in commands))
        self.assertTrue(all(c[2] != '/tmp/tmux-1000/default' for c in commands))
        self.assertTrue(any(c[3:] == ['set-option', '-gw', 'pane-scrollbars', 'on'] for c in commands))
        self.assertIn(binary, call.call_args.args[0])
        self.assertEqual(call.call_args.args[0][0], str(Path.home() / '.local/bin/kitty'))
        self.assertEqual(call.call_args.kwargs['env']['PATH'].split(':')[0], str(Path(binary).parent))
        self.assertTrue(any('--scrollbar' in c[-1] for c in commands if 'new-window' in c))

    def test_preview_instructions_describe_scrollbar(self):
        main = runpy.run_path(str(HELPER))['main']
        output = io.StringIO()
        with patch.object(sys, 'argv', [str(HELPER), '--scrollbar', '--emit', '--lines', '2']), \
             patch('builtins.input', side_effect=EOFError), contextlib.redirect_stdout(output):
            self.assertEqual(main(), 0)
        self.assertIn('Drag the right-edge scrollbar', output.getvalue())
        self.assertNotIn('has no draggable', output.getvalue())


if __name__ == '__main__':
    unittest.main()
