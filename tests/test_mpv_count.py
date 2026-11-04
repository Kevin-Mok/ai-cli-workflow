import os
from pathlib import Path
import subprocess
import sqlite3
import tempfile
import unittest
import wave
import time


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/executable_mpv-count'


class PlayCountTest(unittest.TestCase):
    def test_top_is_ranked_pretty_text_and_handles_empty_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, XDG_STATE_HOME=tmp)
            def run(*args):
                return subprocess.run(['python3', str(SCRIPT), *args], env=env,
                                      text=True, capture_output=True, timeout=5)
            empty = run('--top')
            self.assertEqual(empty.returncode, 0, empty.stderr)
            self.assertIn('No plays recorded yet.', empty.stdout)
            with sqlite3.connect(Path(tmp) / 'mpv-count/plays.sqlite3') as db:
                db.executemany('INSERT INTO plays VALUES (?, ?)', [
                    ('/music/Quiet song.mp3', 2), ('/music/Favorite.mp3', 12),
                    ('/music/Unplayed.mp3', 0), ('/music/Another song.mp3', 2),
                    ('/music/Fourth.mp3', 1)])
            ranked = run('--top')
            self.assertEqual(ranked.returncode, 0, ranked.stderr)
            self.assertIn('🎵 Most played', ranked.stdout)
            self.assertIn('🥇  12 plays  Favorite.mp3', ranked.stdout)
            self.assertLess(ranked.stdout.index('Favorite.mp3'), ranked.stdout.index('Another song.mp3'))
            self.assertLess(ranked.stdout.index('Another song.mp3'), ranked.stdout.index('Quiet song.mp3'))
            self.assertNotIn('Unplayed', ranked.stdout)
            self.assertIn('4.', ranked.stdout)
            plain = run('--plain', '--top')
            self.assertEqual(plain.returncode, 0, plain.stderr)
            self.assertTrue(plain.stdout.isascii(), plain.stdout)
            self.assertIn('1.  12 plays  Favorite.mp3', plain.stdout)
            self.assertNotEqual(run('--count', '--top').returncode, 0)
            self.assertNotEqual(run().returncode, 0)

    def test_record_is_atomic_and_rejects_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / 'song.mp3'
            media.touch()
            env = dict(os.environ, XDG_STATE_HOME=str(Path(tmp) / 'state'))
            command = ['python3', str(SCRIPT), '--plain']
            initialized = subprocess.run([*command, '--count', str(media)], env=env,
                                         text=True, capture_output=True, timeout=5)
            self.assertEqual(initialized.returncode, 0, initialized.stderr)
            workers = [subprocess.Popen([*command, '--record', str(media)], env=env,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                       for _ in range(4)]
            for worker in workers:
                output, errors = worker.communicate(timeout=5)
                self.assertEqual(worker.returncode, 0, errors)
            counted = subprocess.run([*command, '--count', str(media)], env=env,
                                     text=True, capture_output=True, timeout=5)
            self.assertEqual(counted.stdout.strip(), 'Plays: 4')
            missing = subprocess.run([*command, '--record', str(Path(tmp) / 'missing.mp3')],
                                     env=env, text=True, capture_output=True, timeout=5)
            self.assertNotEqual(missing.returncode, 0)

    def test_automatic_native_loops_and_wrapper_do_not_double_count(self):
        hook = SCRIPT.parent.parent / 'dot_config/mpv/scripts/play-count.lua'
        self.assertTrue(hook.is_file(), 'automatic mpv hook must exist')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / 'Automatic song.wav'
            with wave.open(str(media), 'wb') as audio:
                audio.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
                audio.writeframes(b'\0\0' * 6400)
            config = root / 'config'
            (config / 'scripts').mkdir(parents=True)
            (config / 'scripts/play-count.lua').write_bytes(hook.read_bytes())
            env = dict(os.environ, XDG_STATE_HOME=str(root / 'state'))
            options = [f'--config-dir={config}', '--vo=null', '--ao=null',
                       f'--script-opts=play-count-helper={SCRIPT}']
            def total():
                result = subprocess.run(['python3', str(SCRIPT), '--plain', '--count', str(media)],
                                        env=env, text=True, capture_output=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                return int(result.stdout.strip().split()[-1])
            played = subprocess.run(['mpv', *options, '--loop-file=2', str(media)],
                                    env=env, text=True, capture_output=True, timeout=15)
            self.assertEqual(played.returncode, 0, played.stderr)
            self.assertEqual(total(), 3, played.stdout + played.stderr)
            driver = root / 'seek-pause.lua'
            driver.write_text("mp.register_event('file-loaded', function() "
                              "mp.add_timeout(0.2, function() mp.commandv('seek', 0, 'absolute') end); "
                              "mp.add_timeout(0.3, function() mp.set_property_bool('pause', true) end); "
                              "mp.add_timeout(0.45, function() mp.set_property_bool('pause', false) end) end)")
            ordinary = subprocess.run(['mpv', *options, f'--script={driver}', str(media)],
                                       env=env, text=True, capture_output=True, timeout=15)
            self.assertEqual(ordinary.returncode, 0, ordinary.stderr)
            self.assertEqual(total(), 4, ordinary.stdout + ordinary.stderr)
            played = subprocess.run(['python3', str(SCRIPT), str(media), '--', *options,
                                     '--hwdec=no', '--vf=', '--loop-playlist=2'],
                                    env=env, text=True, capture_output=True, timeout=15)
            self.assertEqual(played.returncode, 0, played.stderr)
            self.assertEqual(total(), 6, played.stdout + played.stderr)
            with subprocess.Popen(['mpv', *options, '--loop-file=inf', str(media)], env=env,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as player:
                try:
                    deadline = time.monotonic() + 8
                    while total() < 9 and time.monotonic() < deadline:
                        time.sleep(0.1)
                    self.assertGreaterEqual(total(), 9, 'infinite loops must keep counting')
                finally:
                    player.terminate()
                    player.wait(timeout=5)

    def test_real_loops_persistence_and_paths(self):
        self.assertTrue(SCRIPT.exists(), 'mpv-count wrapper must exist')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / 'clip with spaces.wav'
            with wave.open(str(media), 'wb') as audio:
                audio.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
                audio.writeframes(b'\0\0' * 1600)
            env = dict(os.environ, XDG_STATE_HOME=str(root / 'state'))
            def run(*args):
                return subprocess.run(['python3', str(SCRIPT), '--plain', *map(str, args)],
                                      env=env, text=True, capture_output=True, timeout=15)
            self.assertEqual(run('--count', media).stdout.strip(), 'Plays: 0')
            for expected in (3, 6):
                played = run(media, '--', '--no-config', '--vo=null', '--ao=null',
                             '--loop-playlist=3', '--hwdec=no', '--vf=')
                self.assertEqual(played.returncode, 0, played.stderr)
                self.assertEqual(run('--count', media).stdout.strip(), f'Plays: {expected}')
            alias = root / 'alias.wav'
            alias.symlink_to(media)
            self.assertEqual(run('--count', alias).stdout.strip(), 'Plays: 6')
            other = root / 'other.wav'
            other.write_bytes(media.read_bytes())
            self.assertEqual(run('--count', other).stdout.strip(), 'Plays: 0')
            self.assertNotEqual(run(root / 'missing.wav').returncode, 0)
            self.assertEqual(run('--count', media).stdout.strip(), 'Plays: 6')


if __name__ == '__main__':
    unittest.main()
