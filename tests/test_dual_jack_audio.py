import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/executable_set-dual-jack-audio'


class DualJackAudioTest(unittest.TestCase):
    def run_script(self, listing, fail=False, *args):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'aplay').write_text('#!/bin/sh\nprintf "%s\\n" "$CARD_LIST"\n')
            (root / 'amixer').write_text(
                '#!/bin/sh\nprintf "%s\\n" "$*" >> "$CALL_LOG"\n'
                'test "$MIXER_FAIL" != 1\n'
            )
            for name in ('aplay', 'amixer'):
                (root / name).chmod(0o755)
            env = dict(os.environ, PATH=f'{tmp}:{os.environ["PATH"]}',
                       CARD_LIST=listing, CALL_LOG=str(root / 'calls'),
                       MIXER_FAIL=str(int(fail)))
            result = subprocess.run(['bash', str(SCRIPT), *args], env=env,
                                    text=True, capture_output=True)
            calls = (root / 'calls').read_text() if (root / 'calls').exists() else ''
            return result, calls

    def test_unmutes_both_jacks_without_changing_volume(self):
        result, calls = self.run_script('card 7: Generic [HD-Audio], device 0: ALC897 Analog [ALC897 Analog]')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls.splitlines(), [f'-q -c 7 sset {name} unmute' for name in ('Master', 'Front', 'Surround')])
        self.assertIn('🔊', result.stdout)

    def test_other_hardware_is_untouched(self):
        result, calls = self.run_script('card 0: HDMI [HDMI], device 0: HDMI')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, '')
        self.assertIn('Skipping', result.stdout)

    def test_mixer_failure_is_reported(self):
        result, _ = self.run_script('card 3: Generic [HD-Audio], device 0: ALC897 Analog', True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Could not unmute', result.stderr)

    def test_plain_output(self):
        result, _ = self.run_script('', False, '--plain')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.isascii())


if __name__ == '__main__':
    unittest.main()
