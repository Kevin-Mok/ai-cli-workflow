"""Exercise Codex-shaped OSC 9 through a real isolated tmux client."""
import fcntl
import os
from pathlib import Path
import pty
import runpy
from unittest.mock import MagicMock, patch
import select
import shlex
import struct
import subprocess
import tempfile
import termios
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TmuxNotifications(unittest.TestCase):
    def test_visible_and_hidden_panes_forward_wrapped_osc9(self):
        with tempfile.TemporaryDirectory(prefix='codex-tmux-') as directory:
            folder = Path(directory)
            socket = str(folder / 'socket')
            env = dict(os.environ, TERM='xterm-256color')
            env.pop('TMUX', None)
            def tmux(*args):
                return subprocess.check_output(['tmux', '-S', socket, *args],
                                               env=env, text=True, stderr=subprocess.STDOUT).strip()
            fifo = folder / 'events'
            os.mkfifo(fifo)
            inputs = folder / 'input'
            fixture = folder / 'fixture.py'
            fixture.write_text("""import os, sys, threading, tty
from pathlib import Path
def emit():
    with open(sys.argv[1], 'rb', buffering=0) as events:
        while data := events.read(4096):
            os.write(1, data)
threading.Thread(target=emit, daemon=True).start()
tty.setraw(0)
os.write(1, b'\\x1b[?1004h')
with open(sys.argv[2], 'wb', buffering=0) as inputs:
    while True:
        inputs.write(os.read(0, 1024))
""")
            master, slave = pty.openpty()
            fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 24, 80, 0, 0))
            client = None
            try:
                tmux('-f', '/dev/null', 'new-session', '-d', '-s', 'probe',
                            '-P', '-F', '#{pane_id}', shlex.join(['python3', str(fixture), str(fifo), str(inputs)]))
                tmux('source-file', str(ROOT / 'dot_tmux.conf'))
                client = subprocess.Popen(['tmux', '-S', socket, 'attach', '-t', 'probe'],
                                          stdin=slave, stdout=slave, stderr=slave,
                                          env=env, start_new_session=True)
                os.close(slave)
                slave = -1
                deadline = time.monotonic() + 3
                while not tmux('list-clients') and time.monotonic() < deadline:
                    time.sleep(.03)
                self.assertTrue(tmux('list-clients'), 'Probe client must attach')
                with fifo.open('wb', buffering=0) as events:
                    deadline = time.monotonic() + 3
                    while not inputs.exists() and time.monotonic() < deadline:
                        time.sleep(.03)
                    self.assertTrue(inputs.exists(), 'Input reader must be ready')
                    for hidden in (False, True):
                        with self.subTest(hidden=hidden):
                            if hidden:
                                tmux('new-window', '-n', 'foreground', 'sleep 30')
                                deadline = time.monotonic() + 2
                                while b'\x1b[O' not in inputs.read_bytes() and time.monotonic() < deadline:
                                    time.sleep(.03)
                                self.assertIn(b'\x1b[O', inputs.read_bytes(),
                                              'Hidden Codex must receive focus loss')
                            title = b'CODEX_HIDDEN_PROBE' if hidden else b'CODEX_VISIBLE_PROBE'
                            # Installed Codex OSC9 uses this DCS envelope in tmux.
                            events.write(b'\x1bPtmux;\x1b\x1b]9;' + title + b'\x07\x1b\\')
                            output = bytearray()
                            deadline = time.monotonic() + 2
                            while time.monotonic() < deadline:
                                if select.select([master], [], [], .05)[0]:
                                    output.extend(os.read(master, 65536))
                                if b'\x1b]9;' + title + b'\x07' in output:
                                    break
                            self.assertIn(b'\x1b]9;' + title + b'\x07', output,
                                          'Notification must reach the outer terminal')
            finally:
                subprocess.run(['tmux', '-S', socket, 'kill-server'], env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if client:
                    client.wait(timeout=3)
                os.close(master)
                if slave != -1:
                    os.close(slave)


class VisualProbe(unittest.TestCase):
    def test_probe_routes_and_non_terminal_guard(self):
        main = runpy.run_path(str(ROOT / 'scripts/smoke_codex_tmux_notifications.py'))['main']
        for route in ('desktop', 'direct', 'tmux', 'pipe'):
            with self.subTest(route=route), patch.dict(os.environ, {}, clear=True), \
                    patch('sys.argv', ['probe', '--plain', '--case',
                                       'desktop' if route == 'desktop' else 'terminal']), \
                    patch('sys.stdout', MagicMock()) as output, \
                    patch('time.sleep'), patch('subprocess.run') as send:
                output.isatty.return_value = route != 'pipe'
                if route == 'tmux':
                    os.environ['TMUX'] = '/tmp/test,1,0'
                self.assertEqual(main(), 1 if route == 'pipe' else 0)
                if route == 'desktop':
                    self.assertEqual(send.call_args.args[0][0], 'notify-send')
                elif route == 'pipe':
                    output.buffer.write.assert_not_called()
                    send.assert_not_called()
                else:
                    title = ('tmux' if route == 'tmux' else 'Kitty').encode()
                    expected = b'\x1b]9;Codex visual probe: ' + title + b'\x07'
                    if route == 'tmux':
                        expected = b'\x1bPtmux;' + expected.replace(b'\x1b', b'\x1b\x1b') + b'\x1b\\'
                    output.buffer.write.assert_called_once_with(expected)


if __name__ == '__main__':
    unittest.main()
