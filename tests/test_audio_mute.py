"""Exercise mute helper with controlled external desktop commands."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/executable_audio-mute'


class AudioMuteTest(unittest.TestCase):
    def invoke(self, switch='off', failure=''):
        self.assertTrue(SCRIPT.exists(), 'shared mute notification helper is missing')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for command in ('amixer', 'notify-send', 'pkill'):
                stub = root / command
                stub.write_text('''#!/usr/bin/env python3
import json, os, pathlib, sys
name = pathlib.Path(sys.argv[0]).name
with open(os.environ['CALLS'], 'a') as log:
    log.write(json.dumps([name, *sys.argv[1:]]) + '\\n')
if name == os.environ['FAIL']:
    sys.exit(1)
if name == 'amixer':
    print("Simple mixer control 'Master',0\\n  Front Left: Playback 50 [50%] [" + os.environ['SWITCH'] + "]")
''')
                stub.chmod(0o755)
            result = subprocess.run(['python3', str(SCRIPT)], text=True, capture_output=True,
                env={**os.environ, 'PATH': directory + ':' + os.environ['PATH'],
                     'XDG_RUNTIME_DIR': directory, 'CALLS': str(root / 'calls'), 'SWITCH': switch, 'FAIL': failure})
            calls = [json.loads(line) for line in (root / 'calls').read_text().splitlines()]
            return result, calls

    def test_applied_state_notifies_with_same_replacement_tag(self):
        for switch, status in (('off', 'Muted'), ('on', 'Unmuted')):
            with self.subTest(switch=switch):
                result, calls = self.invoke(switch)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(calls[0], ['amixer', '-D', 'pulse', 'sset', 'Master', 'toggle'])
                self.assertIn(['pkill', '-RTMIN+1', 'i3blocks'], calls)
                notify = next(call for call in calls if call[0] == 'notify-send')
                self.assertIn('string:x-dunst-stack-tag:audio-mute', notify)
                self.assertEqual(notify[-1], status)

    def test_failed_mixer_does_not_notify(self):
        result, calls = self.invoke(failure='amixer')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([call[0] for call in calls], ['amixer'])

    def test_notification_and_missing_bar_do_not_fail_toggle(self):
        for failure in ('notify-send', 'pkill'):
            with self.subTest(failure=failure):
                result, calls = self.invoke(failure=failure)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('notify-send', [call[0] for call in calls])

    def test_unknown_mixer_state_does_not_claim_success(self):
        result, calls = self.invoke(switch='unknown')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('notify-send', [call[0] for call in calls])


if __name__ == '__main__':
    unittest.main()
