"""Offline CLI contract tests; no network or installed yt-dlp needed."""
import os
import contextlib
import io
import runpy
from unittest import mock
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
import json, os, pathlib, sys
a = sys.argv[1:]
if '--dump-single-json' in a:
    assert '--skip-download' in a and '--ignore-config' in a, a
    if os.environ.get('METADATA_WARNING'):
        print('WARNING: Some formats may be missing', file=sys.stderr)
    print(json.dumps({'id': 'oLOzkH0zVZo', 'formats': [
        {'vcodec': 'av01', 'acodec': 'none', 'width': 1920 if os.environ.get('ONLY_1080') else 3840, 'height': 1080 if os.environ.get('ONLY_1080') else 2160, 'fps': 60, 'url': 'https://example.invalid/video'},
        {'vcodec': 'avc1', 'acodec': 'none', 'width': 1920, 'height': 1080, 'fps': 60, 'url': 'https://example.invalid/low'}]}))
    sys.exit(0)
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
        probe = self.bin / 'ffprobe'
        probe.write_text(f'#!{sys.executable}\n' + '''
import json, os, pathlib, sys
assert pathlib.Path(sys.argv[-1]).is_file(), sys.argv
low = os.environ.get('LOW_QUALITY') or os.environ.get('ONLY_1080')
print(json.dumps({'streams': [
    {'codec_type': 'video', 'width': 1920 if low else 3840,
     'height': 1080 if low else 2160, 'avg_frame_rate': '30/1' if os.environ.get('LOW_FPS') else os.environ.get('PROBE_FPS', '60/1')},
    {'codec_type': 'subtitle' if os.environ.get('NO_AUDIO') else 'audio'}]}))
''')
        probe.chmod(0o755)
        (self.bin / 'node').symlink_to('/bin/true')

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
        main = runpy.run_path(str(SCRIPT))['main']
        with mock.patch.object(sys, 'argv', [str(SCRIPT), URL]), \
                mock.patch('shutil.which', return_value='/fixture/tool'), \
                mock.patch.object(Path, 'mkdir', autospec=True,
                                  side_effect=OSError('stop before filesystem writes')) as mkdir, \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(), 1)
        mkdir.assert_called_once_with(Path('/mnt/linux-files-3/yt-vids'),
                                      parents=True, exist_ok=True)

    def test_immediate_4k_verification(self):
        result = self.invoke(URL, '-o', str(self.output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('4K', result.stderr)
        self.assertIn('VERIFIED', result.stderr)
        self.assertEqual(len(result.stdout.strip().splitlines()), 1)

    def test_existing_lower_resolution_is_not_success(self):
        self.output.mkdir()
        target = self.output / 'oLOzkH0zVZo.mp4'
        target.write_bytes(b'old 1080p file')
        (self.output / 'oLOzkH0zVZo.info.json').write_text('{"height": 1080}')
        self.env['LOW_QUALITY'] = '1'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('2160', result.stderr)
        self.assertEqual(target.read_bytes(), b'old 1080p file')
        self.assertEqual(result.stdout, '')
        self.assertTrue((self.output / 'oLOzkH0zVZo.mp4').is_file())

    def test_lower_fps_is_not_highest_quality(self):
        self.env['LOW_FPS'] = '1'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('fps', result.stderr)

    def test_incomplete_format_list_cannot_claim_verified(self):
        self.env['METADATA_WARNING'] = '1'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('VERIFIED', result.stderr)

    def test_highest_available_1080_reports_no_4k(self):
        self.env['ONLY_1080'] = '1'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('4K not reported', result.stderr)

    def test_fractional_fps_and_invalid_fps(self):
        self.env['PROBE_FPS'] = '60000/1001'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.env['PROBE_FPS'] = '0/0'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('VERIFIED', result.stderr)

    def test_missing_audio_fails_quality_check(self):
        self.env['NO_AUDIO'] = '1'
        result = self.invoke(URL, '-o', str(self.output))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('lacks video or audio', result.stderr)

    def test_existing_media_preserved(self):
        self.output.mkdir()
        target = self.output / 'oLOzkH0zVZo.mp4'
        target.write_bytes(b'original media')
        result = self.invoke(URL, '-o', str(self.output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(target.read_bytes(), b'original media')

    def test_missing_dependencies(self):
        for dependency in ['yt-dlp', 'ffmpeg', 'ffprobe']:
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
