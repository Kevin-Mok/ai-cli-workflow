"""Exercise the wrapper's format choice with real yt-dlp, without networking."""
import contextlib
import importlib.util
import io
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'executable_yt-dl'


@unittest.skipUnless(importlib.util.find_spec('yt_dlp'), 'requires yt-dlp Python package')
class QualitySelectionTest(unittest.TestCase):
    def select(self, formats):
        from yt_dlp import YoutubeDL

        namespace = runpy.run_path(str(SCRIPT))
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / 'oLOzkH0zVZo.mkv'
            artifact.write_bytes(b'fixture')
            namespace['main'].__globals__['verify_quality'] = lambda *args: None
            def download(argv, **kwargs):
                if '--dump-single-json' in argv:
                    return subprocess.CompletedProcess(argv, 0,
                        '{"id": "oLOzkH0zVZo", "title": "Quality Fixture"}', '')
                Path(argv[argv.index('--print-to-file') + 2]).write_text(str(artifact) + '\n')
                return subprocess.CompletedProcess(argv, 0)
            with patch.object(sys, 'argv', [str(SCRIPT),
                              'https://youtu.be/oLOzkH0zVZo', '-o', directory]), \
                    patch('shutil.which', return_value='/fixture/tool'), \
                    patch('subprocess.run', side_effect=download) as runner, \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(namespace['main'](), 0)
            argv = runner.call_args.args[0]
        selector = argv[argv.index('--format') + 1]
        options = {'format': selector, 'quiet': True}
        if '--format-sort' in argv:
            options['format_sort'] = argv[argv.index('--format-sort') + 1].split(',')
        options['format_sort_force'] = '--format-sort-force' in argv
        with YoutubeDL(options) as downloader:
            result = downloader.process_ie_result({
                'id': 'oLOzkH0zVZo', 'title': 'Quality fixture', 'formats': formats,
            }, download=False)
        return result

    def test_higher_resolution_and_audio_win_over_mp4_preference(self):
        result = self.select([
            {'format_id': 'mp4-1080', 'url': 'https://example.invalid/low.mp4',
             'ext': 'mp4', 'vcodec': 'avc1', 'acodec': 'none', 'height': 1080, 'width': 1920},
            {'format_id': 'webm-2160', 'url': 'https://example.invalid/high.webm',
             'ext': 'webm', 'vcodec': 'vp9', 'acodec': 'none', 'height': 2160, 'width': 3840},
            {'format_id': 'm4a-128', 'url': 'https://example.invalid/low.m4a',
             'ext': 'm4a', 'vcodec': 'none', 'acodec': 'mp4a', 'abr': 128},
            {'format_id': 'opus-160', 'url': 'https://example.invalid/high.webm',
             'ext': 'webm', 'vcodec': 'none', 'acodec': 'opus', 'abr': 160},
        ])
        self.assertEqual([f['format_id'] for f in result['requested_formats']],
                         ['webm-2160', 'opus-160'])

    def test_resolution_and_fps_override_source_preference(self):
        result = self.select([
            {'format_id': 'preferred-1080', 'url': 'https://example.invalid/low.mp4',
             'ext': 'mp4', 'vcodec': 'avc1', 'acodec': 'mp4a',
             'height': 1080, 'width': 1920, 'fps': 60, 'preference': 10},
            {'format_id': '2160-30', 'url': 'https://example.invalid/4k30.mp4',
             'ext': 'mp4', 'vcodec': 'avc1', 'acodec': 'mp4a',
             'height': 2160, 'width': 3840, 'fps': 30, 'preference': 5},
            {'format_id': '2160-60', 'url': 'https://example.invalid/4k60.mp4',
             'ext': 'mp4', 'vcodec': 'avc1', 'acodec': 'mp4a',
             'height': 2160, 'width': 3840, 'fps': 60, 'preference': 0},
        ])
        self.assertEqual(result['format_id'], '2160-60')

    def test_combined_format_fallback(self):
        result = self.select([
            {'format_id': 'combined-720', 'url': 'https://example.invalid/video.mp4',
             'ext': 'mp4', 'vcodec': 'avc1', 'acodec': 'mp4a', 'height': 720},
        ])
        self.assertEqual(result['format_id'], 'combined-720')


if __name__ == '__main__':
    unittest.main()
