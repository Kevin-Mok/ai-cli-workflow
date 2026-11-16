"""Exercise real pywal exports through the repo entrypoint, in a disposable HOME."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import pywal

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / 'scripts/executable_apply-pywal-theme'


def luminance(color):
    rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
    return sum(c * w for c, w in zip(linear, (.2126, .7152, .0722)))


def ratio(a, b):
    a, b = sorted((luminance(a), luminance(b)))
    return (b + .05) / (a + .05)


def palette(color):
    return {'wallpaper': '', 'alpha': '100',
            'special': {'background': '#050412', 'foreground': '#8dd6dc', 'cursor': color},
            'colors': {f'color{i}': color for i in range(16)}}


class ReadablePaletteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.cache = self.home / '.cache/wal'
        self.bin = self.home / 'bin'
        self.bin.mkdir()
        for name in ('xrdb', 'kitty', 'i3-msg'):
            p = self.bin / name
            p.write_text('#!/bin/sh\nexit 0\n')
            p.chmod(0o755)
        p = self.bin / 'wal'
        p.write_text('#!/bin/sh\nexec python3 -m pywal "$@"\n')
        p.chmod(0o755)
        self.env = {**os.environ, 'HOME': str(self.home), 'XDG_CACHE_HOME': str(self.home / '.cache'),
                    'XDG_CONFIG_HOME': str(self.home / '.config'), 'PYTHONPATH': str(Path(pywal.__file__).parent.parent),
                    'PATH': str(self.bin) + ':' + os.environ['PATH']}

    def apply(self, *args):
        return subprocess.run(['bash', str(WRAPPER), *args], env=self.env, capture_output=True, text=True)

    def check_palette(self, source):
        actual = json.loads((self.cache / 'colors.json').read_text())
        bg = source['special']['background']
        # White wallpaper, 90% opacity, sRGB source-over compositing.
        bound = '#' + ''.join(f'{round(int(bg[i:i+2], 16) * .9 + 25.5):02x}' for i in (1, 3, 5))
        self.assertEqual(actual['special']['background'], bg)
        for color in [*actual['colors'].values(), actual['special']['foreground'], actual['special']['cursor']]:
            self.assertRegex(color, r'^#[0-9a-fA-F]{6}$')
            for background in (bg, bound, '#000000'):
                self.assertGreaterEqual(ratio(color, background), 4.5, (color, background))
        self.assertEqual(actual['special']['foreground'], source['special']['foreground'])
        for name in ('colors-kitty.conf', 'colors.Xresources', 'colors-wal.vim', 'colors.sh', 'sequences'):
            text = (self.cache / name).read_text()
            for color in actual['colors'].values():
                self.assertIn(color, text, name)
            self.assertIn(bg, text)
        for name in ('colors-wal-dmenu.h', 'colors-wal-dwm.h', 'colors-wal-tabbed.h'):
            self.assertIn(bg, (self.cache / name).read_text(), name)
        for key in ('BG', 'MENU_BG', 'TXT_BG'):
            self.assertIn(f'{key}={bg[1:]}'.upper(), (self.cache / 'colors-oomox').read_text().upper())
        self.assertIn('defaultbg = 256;', (self.cache / 'colors-wal-st.h').read_text())
        return actual

    def test_dark_and_saturated_text_is_readable_in_all_exports_and_restore(self):
        for color in ('#000000', '#010208', '#1626c7', '#560f8e', '#8dd6dc'):
            with self.subTest(color=color):
                source = palette(color)
                path = self.home / 'fixture.json'
                path.write_text(json.dumps(source))
                result = self.apply('--theme', str(path), '-n', '-s', '-q')
                self.assertEqual(result.returncode, 0, result.stderr)
                first = self.check_palette(source)
                if color == '#8dd6dc':
                    self.assertEqual(first['colors'], source['colors'])
                result = self.apply('-R', '-n', '-s', '-q')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.check_palette(source), first)

    def test_upper_supported_background_requires_light_side_text(self):
        source = palette('#000000')
        source['special']['background'] = '#666666'
        path = self.home / 'upper-background.json'
        path.write_text(json.dumps(source))
        result = self.apply('--theme', str(path), '-n', '-s', '-q')
        self.assertEqual(result.returncode, 0, result.stderr)
        actual = json.loads((self.cache / 'colors.json').read_text())
        for color in [*actual['colors'].values(), actual['special']['foreground'], actual['special']['cursor']]:
            for bg in ('#666666', '#757575', '#000000'):
                self.assertGreaterEqual(ratio(color, bg), 4.5, (color, bg))

    def test_actual_screenshot_palette_and_deprecated_restore(self):
        source = palette('#050412')
        values = ['#050412', '#0b5065', '#0b4d65', '#560f8e', '#eaa148', '#0f688f', '#1626c7', '#8dd6dc',
                  '#62959a', '#0b5065', '#0b4d65', '#560f8e', '#eaa148', '#0f688f', '#1626c7', '#8dd6dc']
        source['colors'] = dict(zip(source['colors'], values))
        source['special']['cursor'] = '#8dd6dc'
        self.cache.mkdir(parents=True)
        (self.cache / 'colors.json').write_text(json.dumps(source))
        result = self.apply('-r', '-n', '-s', '-q')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.check_palette(source)

    def test_new_generation_and_unrepaired_image_cache_cannot_bypass(self):
        image = self.home / 'dim.ppm'
        image.write_text('P3 1 1 255 1 2 3')
        # Only extraction is stubbed; use real pywal CLI/get/cache/send/export.
        driver = """
import runpy, sys
import pywal.backends.wal
pywal.backends.wal.get = lambda img, light: ['#050412'] + ['#1626c7'] * 14 + ['#8dd6dc']
sys.argv = [sys.argv[1], '--saturate', '0.8', '-e', '-i', sys.argv[2], '-n', '-s', '-q']
runpy.run_path(sys.argv[0], run_name='__main__')
"""
        helper = ROOT / 'scripts/executable_pywal-readable'
        result = subprocess.run(['python3', '-c', driver, str(helper), str(image)],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        source = palette('#1626c7')
        first = self.check_palette(source)
        # The upstream extraction cache deliberately retains unsafe source colors.
        cached = list((self.cache / 'schemes').glob('*.json'))
        self.assertEqual(len(cached), 1)
        self.assertLess(ratio(json.loads(cached[0].read_text())['colors']['color6'], '#050412'), 4.5)
        result = self.apply('-i', str(image), '-n', '-s', '-q')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.check_palette(source), first)

    def test_vim_uses_explicit_background_when_ansi_black_is_brightened(self):
        source = palette('#050412')
        path = self.home / 'fixture.json'
        path.write_text(json.dumps(source))
        result = self.apply('--theme', str(path), '-n', '-s', '-q')
        self.assertEqual(result.returncode, 0, result.stderr)
        config = (ROOT / 'dot_vimrc.tmpl').read_text()
        function = 'function! LoadWalPalette() abort' + config.split('function! LoadWalPalette() abort', 1)[1].split('endfunction', 1)[0] + 'endfunction'
        probe = self.home / 'probe.vim'
        output = self.home / 'vim-bg.txt'
        probe.write_text(function + "\ncall writefile([LoadWalPalette().bg], '" + str(output) + "')\nqall!\n")
        result = subprocess.run(['nvim', '--headless', '-u', 'NONE', '-i', 'NONE', '-S', str(probe)],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output.read_text().strip(), source['special']['background'])

    def test_invalid_palette_fails_before_export_or_send(self):
        for color in ('#broken', '#ffffff'):
            source = palette('#1626c7')
            source['special']['background'] = color
            path = self.home / 'invalid.json'
            path.write_text(json.dumps(source))
            result = self.apply('--theme', str(path), '-n', '-s')
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((self.cache / 'sequences').exists())
            self.assertFalse((self.cache / 'colors.json').exists())


if __name__ == '__main__':
    unittest.main()
