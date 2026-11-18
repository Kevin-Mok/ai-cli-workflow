"""Local screen inactivity ignores the i3 bar and never persists screenshots."""
from pathlib import Path
import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from media_screensaver.motion import ScreenMotion

MONITOR = dict(x=0, y=0, width=320, height=180)


class MotionTests(unittest.TestCase):
    def test_bar_changes_are_ignored_but_content_restarts_five_minutes(self):
        frame = Image.new('RGB', (320, 180), 'black')
        bar = (0, 160, 320, 180)
        detector = ScreenMotion()
        with patch.object(detector, '_capture', side_effect=lambda middle: (frame.copy(), [bar])), patch('media_screensaver.motion.time.monotonic') as now:
            now.return_value = 0
            self.assertFalse(detector.sample(MONITOR)[0])
            ImageDraw.Draw(frame).rectangle((0, 160, 319, 179), fill='white')
            now.return_value = 299
            self.assertFalse(detector.sample(MONITOR)[0])
            now.return_value = 300
            self.assertTrue(detector.sample(MONITOR)[0])
            ImageDraw.Draw(frame).rectangle((50, 50, 100, 100), fill='white')
            now.return_value = 301
            self.assertFalse(detector.sample(MONITOR)[0])
            now.return_value = 600
            self.assertFalse(detector.sample(MONITOR)[0])
            now.return_value = 601
            self.assertTrue(detector.sample(MONITOR)[0])
        detector.close()

    def test_single_pixel_color_change_on_4k_restarts_quiet_period(self):
        monitor = dict(x=0, y=0, width=3840, height=2160)
        frame = Image.new('RGB', (3840, 2160), (255, 0, 0))
        detector = ScreenMotion()
        with patch.object(detector, '_capture', side_effect=lambda middle: (frame.copy(), [])), patch('media_screensaver.motion.time.monotonic') as now:
            now.return_value = 0
            self.assertFalse(detector.sample(monitor)[0])
            frame.putpixel((1920, 1080), (0, 130, 0))
            now.return_value = 300
            self.assertFalse(detector.sample(monitor)[0])
            self.assertEqual(detector.quiet_seconds, 0)

    def test_slow_cumulative_changes_restart_quiet_period(self):
        detector = ScreenMotion()
        frame = Image.new('RGB', (320, 180), (0, 0, 0))
        with patch.object(detector, '_capture', side_effect=lambda middle: (frame.copy(), [])), patch('media_screensaver.motion.time.monotonic') as now:
            for instant, level in ((0, 0), (100, 3), (200, 6), (300, 9)):
                frame.paste((level, level, level), (0, 0, 320, 180))
                now.return_value = instant
                self.assertFalse(detector.sample(MONITOR)[0])
            self.assertEqual(detector.quiet_seconds, 0)
        detector.close()

    def test_geometry_changes_and_explicit_reset_restart_quiet_period(self):
        detector = ScreenMotion()
        with patch.object(detector, '_capture', return_value=(Image.new('RGB', (320, 180)), [])), patch('media_screensaver.motion.time.monotonic') as now:
            now.return_value = 0
            detector.sample(MONITOR)
            now.return_value = 300
            self.assertTrue(detector.sample(MONITOR)[0])
            self.assertFalse(detector.sample(dict(MONITOR, x=320))[0])
            now.return_value = 600
            self.assertTrue(detector.sample(dict(MONITOR, x=320))[0])
            detector.reset()
            self.assertFalse(detector.sample(dict(MONITOR, x=320))[0])
        detector.close()

    def test_native_capture_failure_never_falls_back_to_disk_screenshot(self):
        detector = ScreenMotion()
        detector.connection = MagicMock()
        detector.connection.get_display_name.return_value = ':99'
        detector.connection.screen.return_value.root.query_tree.return_value.children = []
        with patch('PIL.ImageGrab.Image.core.grabscreen_x11', side_effect=OSError('native capture unavailable')), patch('PIL.ImageGrab.shutil.which', return_value='/synthetic/gnome-screenshot'), patch('PIL.ImageGrab.tempfile.mkstemp', side_effect=AssertionError('screen image must never be saved')):
            with self.assertRaises(OSError):
                detector._capture(MONITOR)
        detector.close()

    def test_capture_failure_is_closed_and_recovery_needs_full_quiet_period(self):
        detector = ScreenMotion()
        frame = Image.new('RGB', (320, 180))
        with patch.object(detector, '_capture', return_value=(frame, [])) as capture, patch('media_screensaver.motion.time.monotonic') as now:
            now.return_value = 0
            detector.sample(MONITOR)
            now.return_value = 300
            self.assertTrue(detector.sample(MONITOR)[0])
            capture.side_effect = RuntimeError('capture unavailable')
            allowed, reason = detector.sample(MONITOR)
            self.assertFalse(allowed)
            self.assertIn('unavailable', reason)
            capture.side_effect = None
            self.assertFalse(detector.sample(MONITOR)[0])
        detector.close()

    @unittest.skipUnless(os.environ.get('SCREENSAVER_MOTION_4K_TEST') == '1', 'requires disposable 4K Xvfb display')
    def test_real_4k_capture_completes_without_large_python_reply_decode(self):
        script = "from media_screensaver.motion import ScreenMotion; m=ScreenMotion(); image,bars=m._capture(dict(x=0,y=0,width=3840,height=2160)); assert image.size==(3840,2160); m.close()"
        environment = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1] / 'scripts'))
        result = subprocess.run([sys.executable, '-B', '-c', script], env=environment, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.environ.get('SCREENSAVER_MOTION_X11_TEST') == '1', 'requires disposable Xvfb display')
    def test_real_x11_capture_masks_i3bar_and_detects_content(self):
        from Xlib import X, display
        connection = display.Display()
        root = connection.screen().root
        content = root.create_window(0, 0, 320, 180, 0, X.CopyFromParent, X.InputOutput, X.CopyFromParent, background_pixel=0)
        frame = root.create_window(0, 160, 320, 20, 0, X.CopyFromParent, X.InputOutput, X.CopyFromParent, background_pixel=0)
        frame.set_wm_class('i3-frame', 'i3-frame')
        bar = frame.create_window(0, 0, 320, 20, 0, X.CopyFromParent, X.InputOutput, X.CopyFromParent, background_pixel=0)
        bar.set_wm_class('bar-0', 'i3bar')
        content.map()
        frame.map()
        bar.map()
        connection.sync()
        detector = ScreenMotion()
        try:
            with patch('media_screensaver.motion.time.monotonic') as now:
                now.return_value = 0
                self.assertFalse(detector.sample(MONITOR)[0])
                bar.change_attributes(background_pixel=0xffffff)
                bar.clear_area()
                connection.sync()
                now.return_value = 300
                self.assertTrue(detector.sample(MONITOR)[0])
                content.change_attributes(background_pixel=0xffffff)
                content.clear_area()
                connection.sync()
                now.return_value = 301
                self.assertFalse(detector.sample(MONITOR)[0])
        finally:
            detector.close()
            bar.destroy()
            frame.destroy()
            content.destroy()
            connection.close()


if __name__ == '__main__':
    unittest.main()
