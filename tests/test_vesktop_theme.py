"""Guard the managed Vesktop theme selection and readable wallpaper overlay."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'dot_config/vesktop'


class VesktopThemeTests(unittest.TestCase):
    def test_one_full_theme(self):
        settings = json.loads((ROOT / 'settings/settings.json').read_text())
        self.assertTrue(settings['useQuickCss'])
        self.assertEqual(settings['enabledThemes'], ['ClearVision-v7-BetterDiscord.theme.css'])

    def test_dark_overlay(self):
        css = (ROOT / 'settings/quickCss.css').read_text()
        self.assertNotIn('--background-shading: transparent !important', css)
        self.assertIn('--background-shading: rgba(0, 0, 0, 0.60) !important;', css)
        self.assertIn('--background-shading-percent: 100% !important;', css)


if __name__ == '__main__':
    unittest.main()
