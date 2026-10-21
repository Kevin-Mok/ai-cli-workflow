"""Real Dunst check; run under xvfb-run and a private dbus-run-session."""
import json
import os
import re
import signal
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]


class DaemonTests(unittest.TestCase):
    def test_rule_display_queue_duplicates_history_and_suppression(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            setting = base / 'config/codex-notification-sound/sound.json'
            setting.parent.mkdir(parents=True)
            clip = base / 'clip with spaces; $(bad).mp3'
            clip.write_bytes(b'fixture; fake player only')
            setting.write_text(json.dumps({'path': str(clip)}))
            helper = base / 'codex-notification-sound'
            shutil.copy2(ROOT / 'scripts/executable_codex-notification-sound', helper)
            helper.chmod(0o755)
            binary = base / 'bin'
            binary.mkdir()
            events = base / 'events.jsonl'
            player = binary / 'mpv'
            player.write_text('#!/usr/bin/python3\nimport json, os, sys\nfrom pathlib import Path\npath = Path(sys.argv[-1])\nif path.suffix == ".wav": Path(os.environ["SOUND_TEST_SPEECH"]).write_text(path.read_text())\nwith open(os.environ["SOUND_TEST_EVENTS"], "a") as f: f.write(json.dumps(sys.argv[1:])+"\\n")\n')
            player.chmod(0o755)
            spoken = base / 'spoken.txt'
            env = {**os.environ, 'PATH': f'{binary}:{os.environ["PATH"]}', 'XDG_CONFIG_HOME': str(base / 'config'), 'XDG_STATE_HOME': str(base / 'state'), 'XDG_DATA_HOME': str(base / 'data'), 'SOUND_TEST_EVENTS': str(events), 'SOUND_TEST_SPEECH': str(spoken)}
            config = base / 'config/dunst/dunstrc'
            config.parent.mkdir(parents=True)
            content = (ROOT / 'dot_config/dunst/dunstrc').read_text().replace('~/scripts/codex-notification-sound', str(helper))
            config.write_text(content + '\n[sound_test_suppression]\nappname = codex-kitty\nsummary = suppressed\nformat = ""\n\n[discord_test_suppression]\nappname = FormatSuppressed\nformat = ""\n')
            log = base / 'dunst.log'
            with log.open('w') as output:
                daemon = subprocess.Popen(['dunst', '-config', str(config)], env=env, stdout=output, stderr=output)
                restarted_pid = None
                try:
                    deadline = time.monotonic() + 5
                    while time.monotonic() < deadline:
                        ready = subprocess.run(['dbus-send', '--session', '--print-reply', '--dest=org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus.NameHasOwner', 'string:org.freedesktop.Notifications'], env=env, capture_output=True, text=True)
                        if ready.returncode == 0 and 'boolean true' in ready.stdout:
                            break
                        time.sleep(0.05)
                    self.assertEqual(ready.returncode, 0, log.read_text())
                    self.assertIn('boolean true', ready.stdout, log.read_text())
                    self.assertIsNone(daemon.poll(), 'The explicitly configured daemon must own the private bus')

                    def call(*argv):
                        result = subprocess.run(list(argv), env=env, capture_output=True, text=True, timeout=5)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        return result.stdout.strip()

                    def count():
                        return len(events.read_text().splitlines()) if events.exists() else 0

                    def expect_count(expected):
                        deadline = time.monotonic() + 3
                        while count() < expected and time.monotonic() < deadline:
                            time.sleep(0.05)
                        time.sleep(0.15)
                        self.assertEqual(count(), expected, log.read_text())

                    def notify(app, title, body=''):
                        return call('notify-send', '--app-name', app, '--expire-time', '15000', '--print-id', title, body)

                    notify('kitty', 'Codex approval requested')
                    notify('codex-kitty-other', 'Codex turn complete')
                    expect_count(0)
                    notify('codex-kitty', 'completion fixture')
                    expect_count(1)
                    notify('codex-kitty', 'approval fixture')
                    expect_count(2)
                    call('dunstctl', 'close-all')
                    call('dunstctl', 'history-pop')
                    expect_count(2)  # an already-sounded notification is silent
                    notify('codex-kitty', 'approval fixture')  # coalesced duplicate
                    expect_count(2)
                    call('dunstctl', 'close-all')
                    call('dunstctl', 'history-pop')
                    expect_count(3)  # Dunst's unsounded stacked object first displays
                    call('dunstctl', 'close-all')
                    call('dunstctl', 'set-paused', 'true')
                    notify('codex-kitty', 'queued fixture')
                    expect_count(3)
                    call('dunstctl', 'set-paused', 'false')
                    expect_count(4)
                    call('dunstctl', 'set-paused', 'true')
                    call('dunstctl', 'set-paused', 'false')
                    expect_count(4)
                    notify('codex-kitty', 'suppressed')
                    expect_count(4)
                    speech = setting.with_name('speech.json')
                    speech.write_text(json.dumps({'enabled': True}))
                    notify('codex-kitty', 'speech-enabled silent popup')
                    expect_count(4)
                    speech.write_text(json.dumps({'enabled': False}))
                    notify('codex-kitty', 'speech-disabled restored popup')
                    expect_count(5)
                    for line in events.read_text().splitlines():
                        argv = json.loads(line)
                        self.assertEqual(argv[-2:], ['--', str(clip)])
                    activation_source = ROOT / 'scripts/executable_codex-notification-activate'
                    self.assertTrue(activation_source.is_file(), 'Reusable activation helper not implemented')
                    activation = base / 'codex-notification-activate'
                    shutil.copy2(activation_source, activation)
                    activation.chmod(0o755)
                    callback = base / 'config/kitty/notifications.py'
                    callback.parent.mkdir(parents=True)
                    shutil.copy2(ROOT / 'dot_config/kitty/notifications.py', callback)
                    call(str(activation))
                    pid_reply = call('dbus-send', '--session', '--print-reply', '--dest=org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus.GetConnectionUnixProcessID', 'string:org.freedesktop.Notifications')
                    restarted_pid = int(re.search(r'uint32 (\d+)', pid_reply).group(1))
                    self.assertNotEqual(restarted_pid, daemon.pid)
                    self.assertEqual(call('dunstctl', 'count', 'history'), '0')
                    notify('codex-kitty', 'after activation fixture')
                    expect_count(6)
                    python = base / 'data/codex-notification-speech/venv/bin/python'
                    python.parent.mkdir(parents=True)
                    python.write_text('#!/usr/bin/python3\nimport sys\nfrom pathlib import Path\nPath(sys.argv[sys.argv.index("--output_file")+1]).write_text(sys.stdin.read())\n')
                    python.chmod(0o755)
                    model = base / 'data/codex-notification-speech/voices/en_US-ryan-high.onnx'
                    model.parent.mkdir()
                    model.write_bytes(b'fixture')
                    model.with_suffix('.onnx.json').write_text('{}')
                    speech.write_text(json.dumps({'enabled': True}))
                    notify('Grok Bot other', 'Unrelated Grok lookalike')
                    expect_count(6)
                    call('notify-send', '--app-name', 'Grok Bot', '--expire-time', '15000',
                         'Do not read this title', 'Read this Grok message; $(not a shell command)')
                    expect_count(8)
                    grok_calls = [json.loads(line) for line in events.read_text().splitlines()][6:]
                    self.assertEqual(grok_calls[0][-2:], ['--', str(clip)])
                    self.assertEqual(Path(grok_calls[1][-1]).suffix, '.wav')
                    self.assertEqual(spoken.read_text(), 'Read this Grok message; $(not a shell command)\n')
                    notify('Grok Bot', 'Grok title-only message')
                    expect_count(10)
                    self.assertEqual(spoken.read_text(), 'Grok title-only message\n')
                    call('dunstctl', 'close-all')
                    call('dunstctl', 'history-pop')
                    expect_count(10)
                    discord = setting.with_name('discord-speech.json')
                    notify('FormatProbe', 'Alex (#normie, Active)', 'disabled by default')
                    expect_count(10)
                    discord.write_text(json.dumps({'enabled': True}))
                    notify('FormatProbe', '(A) Alex (#😊normie, Active)', 'hai')
                    expect_count(11)
                    self.assertEqual(spoken.read_text(), '(A) Alex says hai\n')
                    discord_call = json.loads(events.read_text().splitlines()[-1])
                    self.assertEqual(Path(discord_call[-1]).suffix, '.wav')
                    notify('FormatProbe', 'Alex (#😊normie, Another Server)', 'hello')
                    expect_count(12)
                    self.assertEqual(spoken.read_text(), 'Alex says hello\n')
                    notify('FormatProbe', 'Voice: listening', 'nerd-dictation is ready')
                    notify('FormatProbe', 'Alex (#, Active)', 'invalid channel')
                    notify('FormatProbe', 'Alex (#normie, Active)', '   ')
                    expect_count(12)
                    call('dunstctl', 'close-all')
                    call('dunstctl', 'history-pop')
                    expect_count(12)
                    call('dunstctl', 'close-all')
                    call('dunstctl', 'set-paused', 'true')
                    notify('FormatProbe', 'Queued (#normie, Active)', 'waiting')
                    expect_count(12)
                    call('dunstctl', 'set-paused', 'false')
                    expect_count(13)
                    self.assertEqual(spoken.read_text(), 'Queued says waiting\n')
                    call('dunstctl', 'set-paused', 'true')
                    call('dunstctl', 'set-paused', 'false')
                    expect_count(13)
                    notify('FormatSuppressed', 'Silent (#normie, Active)', 'suppressed')
                    expect_count(13)
                    call(str(helper), 'discord-speech', 'disable', '--plain')
                    self.assertFalse(json.loads(discord.read_text())['enabled'])
                    self.assertTrue(json.loads(speech.read_text())['enabled'])
                    notify('FormatProbe', 'Alex (#normie, Active)', 'disabled explicitly')
                    expect_count(13)
                    notify('Grok Bot', 'Still independent', 'Grok remains audible')
                    expect_count(15)
                    self.assertEqual(spoken.read_text(), 'Grok remains audible\n')
                    call(str(helper), 'speech', 'disable', '--plain')
                    notify('codex-kitty', 'Codex remains audible')
                    expect_count(16)
                    self.assertEqual(json.loads(events.read_text().splitlines()[-1])[-2:], ['--', str(clip)])
                    call(str(helper), 'discord-speech', 'enable', '--plain')
                    self.assertFalse(json.loads(speech.read_text())['enabled'])
                    notify('FormatProbe', 'Again (#normie, Active)', 'enabled independently')
                    expect_count(17)
                    self.assertEqual(spoken.read_text(), 'Again says enabled independently\n')
                    call('dunstctl', 'close-all')
                    notify('FormatProbe', 'Stacked (#normie, Active)', 'duplicate')
                    expect_count(18)
                    notify('FormatProbe', 'Stacked (#normie, Active)', 'duplicate')
                    expect_count(18)
                    call('dunstctl', 'close-all')
                    call('dunstctl', 'history-pop')
                    expect_count(19)  # Dunst first displays the unsounded duplicate object.
                    self.assertEqual(spoken.read_text(), 'Stacked says duplicate\n')
                    call('dunstctl', 'close-all')
                    call('dunstctl', 'history-pop')
                    expect_count(19)
                    notify('vesktop-other', 'Alex', 'unrelated DM lookalike')
                    notify('FormatProbe', 'Alex', 'unidentified DM')
                    expect_count(19)
                    notify('vesktop', '(A) Alex', 'hello from a direct message')
                    expect_count(20)
                    self.assertEqual(spoken.read_text(), '(A) Alex says hello from a direct message\n')
                    self.assertEqual(Path(json.loads(events.read_text().splitlines()[-1])[-1]).suffix, '.wav')
                    call(str(helper), 'discord-speech', 'disable', '--plain')
                    notify('vesktop', 'Alex', 'disabled direct message')
                    expect_count(20)
                    print('Private Dunst: Vesktop DM=speech-only; lookalike/unknown-app/disabled=silent')
                    print('Private Dunst: completion/approval=one each; unrelated/duplicates/normal history/suppressed=silent; queued=plays on display; recalled duplicate stack=one sound; speech-enable=silent; disable=MP3 restored')
                    print('Private Dunst: Grok Bot=clip then message; title fallback=spoken; lookalikes/history=silent; Codex speech switch=independent')
                    print('Private Dunst: Discord format from unknown app=speech only; parentheses/Unicode=preserved; Voice/malformed/blank/disabled/suppressed/normal history=silent; queued=spoken on display; recalled duplicate stack=one speech; Codex/Grok switches=independent')
                finally:
                    if restarted_pid is not None:
                        os.kill(restarted_pid, signal.SIGTERM)
                    daemon.terminate()
                    daemon.wait(timeout=5)


if __name__ == '__main__':
    unittest.main()
