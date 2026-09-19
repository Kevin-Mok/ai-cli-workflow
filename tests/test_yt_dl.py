"""Offline CLI contract tests; no network or installed yt-dlp needed."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'yt-dl'
URL = 'https://www.youtube.com/watch?v=oLOzkH0zVZo'


class DownloaderTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.output = self.root / 'output with spaces'
        self.env = dict(os.environ, PATH=str(self.bin), HOME=str(self.root))
        fake = self.bin / 'yt-dlp'
        fake.write_text(f'#!{sys.executable}\n' + '''
import os, pathlib, sys
a = sys.argv[1:]
required = ['--ignore-config', '--no-playlist', '--no-overwrites', '--no-simulate', '--write-info-json']
assert all(x in a for x in required), a
assert a[-2] == '--' and a[-1] == 'https://www.youtube.com/watch?v=oLOzkH0zVZo', a
assert a[a.index('--print') + 1] == 'after_move:filepath', a
assert a[a.index('--output') + 1] == '%(id)s.%(ext)s', a
assert a[a.index('--format') + 1] == 'bv*+ba/b', a
assert a[a.index('--merge-output-format') + 1] == 'mkv', a
if os.environ.get('FAIL_DOWNLOAD'):
    print('fixture network failure', file=sys.stderr)
    sys.exit(7)
out = pathlib.Path(a[a.index('--paths') + 1]) / 'oLOzkH0zVZo.mp4'
if not os.environ.get('MISSING_OUTPUT'):
    if not out.exists():
        out.write_bytes(b'' if os.environ.get('EMPTY_OUTPUT') else b'fixture media')
if not os.environ.get('NO_REPORT'):
    print(out)
if os.environ.get('MULTIPLE_REPORTS'):
    print(out)
''')
        fake.chmod(0o755)
        (self.bin / 'ffmpeg').symlink_to('/bin/true')

    def invoke(self, *args):
        self.assertTrue(SCRIPT.exists(), 'scripts/yt-dl is not implemented')
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              env=self.env, capture_output=True, text=True)

    def test_help_without_dependencies(self):
        self.env['PATH'] = ''
        result = self.invoke('--help')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('output-dir', result.stdout)

    def test_rejects_missing_and_non_video_urls(self):
        for args in [(), ('--bad',), ('https://example.com/watch?v=oLOzkH0zVZo',),
                     ('https://youtube.com/playlist?list=abc',),
                     ('https://youtube.com.evil.test/watch?v=oLOzkH0zVZo',),
                     ('file:///tmp/video',)]:
            with self.subTest(args=args):
                self.assertEqual(self.invoke(*args).returncode, 2)

    def test_download_with_spaces_and_playlist_removed(self):
        result = self.invoke(URL + '&list=ignored', '--output-dir', str(self.output))
        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.output / 'oLOzkH0zVZo.mp4'
        self.assertEqual(result.stdout.strip(), str(target))
        self.assertTrue(target.is_file())

    def test_short_url_normalized(self):
        result = self.invoke('https://youtu.be/oLOzkH0zVZo?t=1', '-o', str(self.output))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_default_output(self):
        result = self.invoke(URL)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'Downloads/yt-dl/oLOzkH0zVZo.mp4').is_file())

    def test_existing_media_preserved(self):
        self.output.mkdir()
        target = self.output / 'oLOzkH0zVZo.mp4'
        target.write_bytes(b'original media')
        result = self.invoke(URL, '-o', str(self.output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(target.read_bytes(), b'original media')

    def test_missing_dependencies(self):
        for dependency in ['yt-dlp', 'ffmpeg']:
            with self.subTest(dependency=dependency):
                path = self.bin / dependency
                renamed = self.bin / (dependency + '.disabled')
                path.rename(renamed)
                result = self.invoke(URL)
                renamed.rename(path)
                self.assertEqual(result.returncode, 1)
                self.assertIn(dependency, result.stderr)

    def test_downloader_failure_propagates(self):
        self.env['FAIL_DOWNLOAD'] = '1'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertEqual(result.returncode, 7)
        self.assertIn('fixture network failure', result.stderr)
        self.assertEqual(result.stdout, '')

    def test_missing_artifact_is_failure(self):
        self.env['MISSING_OUTPUT'] = '1'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')

    def test_empty_artifact_is_failure(self):
        self.env['EMPTY_OUTPUT'] = '1'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')

    def test_ambiguous_or_missing_report_is_failure(self):
        for mode in ('NO_REPORT', 'MULTIPLE_REPORTS'):
            with self.subTest(mode=mode):
                self.env[mode] = '1'
                result = self.invoke(URL, '-o', str(self.output))
                del self.env[mode]
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, '')

    def test_output_metacharacters_are_literal(self):
        target = self.root / '100% $(touch injected); destination'
        result = self.invoke(URL, '-o', str(target))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(result.stdout.strip()).parent, target)

    def test_output_is_file(self):
        self.output.write_text('keep')
        result = self.invoke(URL, '-o', str(self.output))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.output.read_text(), 'keep')


if __name__ == '__main__':
    unittest.main()
