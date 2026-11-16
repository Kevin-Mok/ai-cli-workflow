"""Exercise real pywal exports through the repo entrypoint, in a disposable HOME."""
import json
import colorsys
from itertools import combinations
import os
from pathlib import Path
import re
import runpy
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


def white_composite(background):
    return '#' + ''.join(f'{round(int(background[i:i+2], 16) * .9 + 25.5):02x}'
                         for i in (1, 3, 5))


def saturation(color):
    red, green, blue = (int(color[index:index + 2], 16) / 255 for index in (1, 3, 5))
    return colorsys.rgb_to_hls(red, green, blue)[2]


def oklab(color):
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    red, green, blue = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
                        for value in channels]
    l = (0.4122214708 * red + 0.5363325363 * green + 0.0514459929 * blue) ** (1 / 3)
    m = (0.2119034982 * red + 0.6806995451 * green + 0.1073969566 * blue) ** (1 / 3)
    s = (0.0883024619 * red + 0.2817188376 * green + 0.6299787005 * blue) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklab_distance(first, second):
    return sum((a - b) ** 2 for a, b in zip(oklab(first), oklab(second))) ** 0.5


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

    def assert_text_contrast(self, colors, special, backgrounds):
        for index in range(16):
            key = f'color{index}'
            required = 7 if key == 'color7' else 4.5
            for background in backgrounds:
                self.assertGreaterEqual(ratio(colors[key], background), required, (key, colors[key], background))
        for key in ('foreground', 'cursor'):
            for background in backgrounds:
                self.assertGreaterEqual(ratio(special[key], background), 7, (key, special[key], background))

    def check_palette(self, source):
        actual = json.loads((self.cache / 'colors.json').read_text())
        bg = source['special']['background']
        # White wallpaper, 90% opacity, sRGB source-over compositing.
        bound = '#' + ''.join(f'{round(int(bg[i:i+2], 16) * .9 + 25.5):02x}' for i in (1, 3, 5))
        self.assertEqual(actual['special']['background'], bg)
        for color in [*actual['colors'].values(), actual['special']['foreground'], actual['special']['cursor']]:
            self.assertRegex(color, r'^#[0-9a-fA-F]{6}$')
        self.assert_text_contrast(actual['colors'], actual['special'], (bg, bound, '#000000'))
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

    def assert_vivid_chromatic_slots(self, colors, minimum_distance=0.04):
        slots = [f'color{index}' for index in (*range(1, 7), *range(9, 15))]
        values = [colors[slot] for slot in slots]
        self.assertEqual(len(set(values)), 12)
        self.assertTrue(all(saturation(color) >= .98 for color in values), values)
        distances = [(oklab_distance(first, second), first_slot, second_slot)
                     for (first_slot, first), (second_slot, second) in combinations(zip(slots, values), 2)]
        closest = min(distances)
        self.assertGreaterEqual(closest[0], minimum_distance, closest)
        return closest

    def test_sparse_quantizer_fallback_uses_real_palette_when_pywal_generator_fails(self):
        helper = runpy.run_path(str(ROOT / 'scripts/executable_pywal-readable'))

        class Backend:
            def has_im(self):
                return 'magick'

            def imagemagick(self, count, image, command):
                palette_size = 9 if count == 16 else 46
                return [b'header'] + [f'#{index:02X}{(index + 1):02X}{(index + 2):02X}'.encode()
                                      for index in range(palette_size)]

        backend = Backend()

        def broken_generator(image):
            raise SystemExit(1)

        extracted = helper['sparse_colors']('fixture.jpeg', broken_generator, backend)
        real_colors = [row.decode() for row in backend.imagemagick(256, 'fixture.jpeg', 'magick')[1:]]
        self.assertEqual(len(extracted), 16)
        self.assertEqual(len(set(extracted)), 16)
        self.assertTrue(set(extracted).issubset(real_colors))
        self.assertEqual(extracted[0], real_colors[0])
        self.assertEqual(extracted[-1], real_colors[-1])

        expected = ['#123456'] * 16
        self.assertEqual(helper['sparse_colors']('fixture.jpeg', lambda image: expected, backend), expected)

    def test_vivid_palette_separates_twelve_chromatic_slots_across_all_72_anchors(self):
        helper = runpy.run_path(str(ROOT / 'scripts/executable_pywal-readable'))
        for hue in range(0, 360, 5):
            with self.subTest(anchor_hue=hue):
                red, green, blue = colorsys.hls_to_rgb(hue / 360, .5, .8)
                anchor = '#' + ''.join(f'{round(channel * 255):02X}' for channel in (red, green, blue))
                source = {
                    'special': {'background': '#050412', 'foreground': '#dddddd', 'cursor': '#dddddd'},
                    'colors': {'color0': '#050412', **{f'color{index}': '#222222' for index in range(1, 16)}},
                }
                source['colors']['color1'] = anchor
                helper['repair_palette'](source)
                self.assert_vivid_chromatic_slots(source['colors'], .08)
                actual_hue = colorsys.rgb_to_hls(*(int(source['colors']['color1'][i:i + 2], 16) / 255
                                                   for i in (1, 3, 5)))[0]
                self.assertLessEqual(abs((actual_hue * 360 - hue + 180) % 360 - 180), 3)
                first = json.dumps(source, sort_keys=True)
                helper['repair_palette'](source)
                self.assertEqual(json.dumps(source, sort_keys=True), first)

    def test_dark_and_saturated_text_is_readable_in_all_exports_and_restore(self):
        for color in ('#000000', '#010208', '#1626c7', '#560f8e', '#8dd6dc'):
            with self.subTest(color=color):
                source = palette(color)
                path = self.home / 'fixture.json'
                path.write_text(json.dumps(source))
                result = self.apply('--theme', str(path), '-n', '-s', '-q')
                self.assertEqual(result.returncode, 0, result.stderr)
                first = self.check_palette(source)
                self.assert_vivid_chromatic_slots(first['colors'], .08)
                result = self.apply('-R', '-n', '-s', '-q')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.check_palette(source), first)

    def test_upper_background_normalizes_for_vivid_text_headroom(self):
        source = palette('#000000')
        source['special']['background'] = '#666666'
        path = self.home / 'upper-background.json'
        path.write_text(json.dumps(source))
        result = self.apply('--theme', str(path), '-n', '-s', '-q')
        self.assertEqual(result.returncode, 0, result.stderr)
        actual = json.loads((self.cache / 'colors.json').read_text())
        self.assertNotEqual(actual['special']['background'], '#666666')
        self.assertGreaterEqual(ratio('#ffffff', white_composite(actual['special']['background'])), 7)
        self.assert_text_contrast(actual['colors'], actual['special'],
                                  (actual['special']['background'], white_composite(actual['special']['background']), '#000000'))

    def test_unsupported_bright_backgrounds_are_darkened_with_readable_idempotent_exports(self):
        for background in ('#11820f', '#078504', '#079F08', '#ffffff'):
            with self.subTest(background=background):
                source = palette('#ffffff')
                source['special']['background'] = background
                path = self.home / 'unsupported-background.json'
                path.write_text(json.dumps(source))
                self.assertLess(ratio('#ffffff', white_composite(background)), 4.5)

                result = self.apply('--theme', str(path), '-n', '-s', '-q')
                self.assertEqual(result.returncode, 0, result.stderr)
                first = json.loads((self.cache / 'colors.json').read_text())
                adjusted = first['special']['background']
                self.assertNotEqual(adjusted.lower(), background.lower())
                self.assertGreaterEqual(ratio('#ffffff', white_composite(adjusted)), 7.0)
                self.assertTrue(all(new <= old for old, new in zip(
                    (int(background[i:i+2], 16) for i in (1, 3, 5)),
                    (int(adjusted[i:i+2], 16) for i in (1, 3, 5)))))
                self.assert_text_contrast(first['colors'], first['special'], (adjusted, white_composite(adjusted), '#' + ''.join(
                    f'{round(int(adjusted[i:i+2], 16) * .9):02x}' for i in (1, 3, 5))))
                for name in ('colors-kitty.conf', 'colors.Xresources', 'colors-wal.vim', 'colors.sh', 'sequences'):
                    self.assertIn(adjusted, (self.cache / name).read_text(), name)
                self.assert_vivid_chromatic_slots(first['colors'], .04)
                result = self.apply('-R', '-n', '-s', '-q')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads((self.cache / 'colors.json').read_text()), first)

    def test_one_and_two_color_wallpapers_generate_readable_palettes_without_changing_raw_hues(self):
        fixtures = {
            'one-color': ['#222222'],
            'two-color': ['#222222', '#777777'],
        }
        for name, colors in fixtures.items():
            with self.subTest(name=name):
                image = self.home / f'{name}.ppm'
                pixels = [colors[index % len(colors)] for index in range(64 * 64)]
                rgb = [channel for color in pixels for channel in
                       (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))]
                image.write_text('P3\n64 64\n255\n' + ' '.join(map(str, rgb)) + '\n')
                result = self.apply('-i', str(image), '-n', '-s', '-q')
                self.assertEqual(result.returncode, 0, result.stderr)
                actual = json.loads((self.cache / 'colors.json').read_text())
                for color in [*actual['colors'].values(), actual['special']['foreground'], actual['special']['cursor']]:
                    self.assertRegex(color, r'^#[0-9a-fA-F]{6}$')
                self.assert_text_contrast(actual['colors'], actual['special'],
                                          (actual['special']['background'], white_composite(actual['special']['background']), '#000000'))
                self.assert_vivid_chromatic_slots(actual['colors'], .04)
                from pywal.backends import wal as backend
                helper = runpy.run_path(str(ROOT / 'scripts/executable_pywal-readable'))
                extracted = helper['sparse_colors'](str(image), backend.gen_colors, backend)
                self.assertEqual(len(extracted), 16)
                for color in extracted:
                    self.assertEqual(color[1:3], color[3:5], color)
                    self.assertEqual(color[3:5], color[5:7], color)

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
        actual = self.check_palette(source)
        self.assert_vivid_chromatic_slots(actual['colors'], .08)

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

    def test_vim_keeps_readable_vivid_accent_lanes_instead_of_collapsing_them(self):
        source = palette('#8dd6dc')
        path = self.home / 'fixture.json'
        path.write_text(json.dumps(source))
        result = self.apply('--theme', str(path), '-n', '-s', '-q')
        self.assertEqual(result.returncode, 0, result.stderr)
        generated = json.loads((self.cache / 'colors.json').read_text())
        accent_colors = [generated['colors'][f'color{index}'] for index in range(1, 7)]
        self.assertEqual(len(set(color.upper() for color in accent_colors)), 6)
        background = generated['special']['background']
        effective_background = white_composite(background)
        for color in accent_colors:
            self.assertGreaterEqual(ratio(color, effective_background), 4.5, color)

        config = (ROOT / 'dot_vimrc.tmpl').read_text()
        names = ('KmWalHexToRgb', 'KmWalBlend', 'KmWalRelativeLuminance', 'KmWalContrastRatio',
                 'KmWalEffectiveBackground', 'KmWalCompareAccentCandidates', 'KmWalReadableAccentLanes',
                 'LoadWalPalette')
        functions = []
        for name in names:
            match = re.search(rf'(?ms)^function! {re.escape(name)}\b.*?^endfunction$', config)
            self.assertIsNotNone(match, f'missing Vim function {name}')
            functions.append(match.group(0))

        weak = {'bg': '#050412', 'fg': '#DDDDDD', 'const': '#1E1E1E', 'string': '#252525',
                'type': '#2C2C2C', 'func': '#333333', 'keyword': '#3A3A3A', 'special': '#414141'}
        weak_literal = '{' + ', '.join(f"'{key}': '{value}'" for key, value in weak.items()) + '}'
        output = self.home / 'vim-accent-lanes.json'
        probe = self.home / 'probe.vim'
        probe.write_text('\n'.join([
            'let s:km_wal_terminal_opacity = 0.9',
            *functions,
            f"let result = {{'strong': KmWalReadableAccentLanes(LoadWalPalette()), 'weak': KmWalReadableAccentLanes({weak_literal})}}",
            f"call writefile([json_encode(result)], '{output}')",
            'qall!',
            '',
        ]))
        result = subprocess.run(['nvim', '--headless', '-u', 'NONE', '-i', 'NONE', '-S', str(probe)],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        lanes = json.loads(output.read_text())
        self.assertEqual([value.upper() for value in lanes['strong']],
                         [generated['colors'][f'color{index}'].upper() for index in (4, 5, 6)])
        self.assertEqual([value.upper() for value in lanes['weak']], ['#414141', '#3A3A3A', '#333333'])

    def test_invalid_palette_fails_before_export_or_send(self):
        for color in ('#broken',):
            source = palette('#1626c7')
            source['special']['background'] = color
            path = self.home / 'invalid.json'
            path.write_text(json.dumps(source))
            result = self.apply('--theme', str(path), '-n', '-s')
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((self.cache / 'sequences').exists())
            self.assertFalse((self.cache / 'colors.json').exists())

        source = palette('#1626c7')
        del source['special']['cursor']
        path = self.home / 'missing-key.json'
        path.write_text(json.dumps(source))
        result = self.apply('--theme', str(path), '-n', '-s')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.cache / 'sequences').exists())
        self.assertFalse((self.cache / 'colors.json').exists())


if __name__ == '__main__':
    unittest.main()
