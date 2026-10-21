#!/usr/bin/env python3
"""Real Xvfb/GStreamer integration: movement preserves playback, shutdown releases it."""
import importlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
try:
    runtime = importlib.import_module('media_screensaver.renderer')
except ModuleNotFoundError:
    runtime = None

class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(runtime, 'persistent GTK renderer has not been implemented')

    def test_video_moves_without_restart_and_shutdown_releases_pipeline(self):
        from gi.repository import Gtk, Gst
        from media_screensaver.core import Entry
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'long.mp4'
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=160x90:rate=20', '-t', '6', '-c:v', 'libx264', '-preset', 'ultrafast', '-y', str(path)], check=True)
            window = Gtk.Window()
            layout = Gtk.Layout()
            window.add(layout)
            card = runtime.Card(Entry(1, path), lambda *args: self.fail(str(args)))
            layout.put(card.widget, 0, 0)
            window.show_all()
            def pump(seconds):
                end = time.monotonic() + seconds
                while time.monotonic() < end:
                    while Gtk.events_pending(): Gtk.main_iteration_do(False)
                    time.sleep(.01)
            try:
                card.widget.set_size_request(320, 180)
                pump(1.2)
                before = card.position()
                self.assertGreater(before, .5)
                pipeline = card.pipeline
                layout.move(card.widget, 320, 30)
                card.widget.set_size_request(480, 270)
                pump(1.0)
                self.assertIs(card.pipeline, pipeline)
                self.assertGreater(card.position(), before + .5)
            finally:
                pipeline = card.pipeline
                card.close()
                window.destroy()
            self.assertEqual(pipeline.get_state(Gst.SECOND)[1], Gst.State.NULL)

    def test_short_video_loops_in_same_pipeline(self):
        from gi.repository import Gtk, Gst
        from media_screensaver.core import Entry
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'short.mp4'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=size=160x90:rate=20','-t','0.5','-c:v','libx264','-preset','ultrafast','-y',str(path)], check=True)
            errors = []
            window = Gtk.Window()
            card = runtime.Card(Entry(1,path), lambda *args: errors.append(args))
            window.add(card.widget)
            window.show_all()
            positions = []
            try:
                end = time.monotonic()+2
                while time.monotonic()<end:
                    while Gtk.events_pending(): Gtk.main_iteration_do(False)
                    pos = card.position()
                    if pos is not None: positions.append(pos)
                    time.sleep(.01)
                self.assertFalse(errors)
                self.assertTrue(any(b<a-.1 for a,b in zip(positions,positions[1:])), positions)
                self.assertEqual(card.pipeline.get_state(0)[1], Gst.State.PLAYING)
            finally:
                card.close()
                window.destroy()

    def test_video_remains_visible_beside_photo_windows(self):
        from gi.repository import Gtk, Gdk, GdkPixbuf
        from media_screensaver.core import Entry
        with tempfile.TemporaryDirectory() as directory:
            photo = Path(directory) / 'green.png'
            video = Path(directory) / 'red.mp4'
            pixels = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, False, 8, 160, 90)
            pixels.fill(0x00ff00ff)
            pixels.savev(str(photo), 'png', [], [])
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                            'color=c=red:size=160x90:rate=20', '-t', '2', '-c:v',
                            'libx264', '-pix_fmt', 'yuv420p', str(video)], check=True)
            errors = []
            window = Gtk.Window(type=Gtk.WindowType.POPUP)
            window.move(0, 0)
            window.set_default_size(600, 200)
            layout = Gtk.Layout()
            window.add(layout)
            cards = []
            for identity, (path, x) in enumerate(((photo, 0), (video, 230), (photo, 400)), 1):
                card = runtime.Card(Entry(identity, path), lambda *args: errors.append(args))
                card.widget.set_size_request(160, 90)
                layout.put(card.widget, x, 50)
                cards.append(card)
            window.show_all()
            try:
                end = time.monotonic() + 1
                while time.monotonic() < end:
                    while Gtk.events_pending(): Gtk.main_iteration_do(False)
                    time.sleep(.01)
                self.assertFalse(errors)
                self.assertGreater(cards[1].position(), .3)
                # Flush GTK, then read the actual X11 screen including native child windows.
                from Xlib import X, display
                Gdk.Display.get_default().sync()
                _, origin_x, origin_y = window.get_window().get_origin()
                connection = display.Display()
                try:
                    def bgr(x, y):
                        pixel = connection.screen().root.get_image(
                            origin_x + x, origin_y + y, 1, 1, X.ZPixmap, 0xffffffff)
                        data = pixel.data.encode('latin1') if isinstance(pixel.data, str) else pixel.data
                        return tuple(data[:3])
                    self.assertEqual(bgr(30, 65), (0, 255, 0))
                    self.assertEqual(bgr(430, 65), (0, 255, 0))
                    self.assertGreater(bgr(260, 65)[2], 240, 'video is black behind photo sibling windows')
                    self.assertGreater(bgr(310, 95)[2], 240)
                    before = cards[1].position()
                    cards[1].widget.set_size_request(200, 112)
                    layout.move(cards[1].widget, 180, 30)
                    end = time.monotonic() + .35
                    while time.monotonic() < end:
                        while Gtk.events_pending(): Gtk.main_iteration_do(False)
                        time.sleep(.01)
                    Gdk.Display.get_default().sync()
                    self.assertGreater(cards[1].position(), before + .1)
                    self.assertEqual(bgr(30, 65), (0, 255, 0))
                    self.assertEqual(bgr(430, 65), (0, 255, 0))
                    self.assertGreater(bgr(210, 45)[2], 240)
                    self.assertGreater(bgr(280, 85)[2], 240)
                finally:
                    connection.close()
            finally:
                for card in cards: card.close()
                window.destroy()

    def test_portrait_photo_is_letterboxed_instead_of_cropped(self):
        from gi.repository import Gtk, GdkPixbuf
        from media_screensaver.core import Entry
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'portrait.png'
            photo = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB,False,8,20,40)
            photo.fill(0xff0000ff)
            photo.savev(str(path),'png',[],[])
            window = Gtk.OffscreenWindow()
            card = runtime.Card(Entry(1,path), lambda *args: self.fail(str(args)))
            card.widget.set_size_request(200,200)
            window.add(card.widget)
            window.show_all()
            try:
                end = time.monotonic()+.3
                while time.monotonic()<end:
                    while Gtk.events_pending(): Gtk.main_iteration_do(False)
                    time.sleep(.01)
                pixels = window.get_pixbuf()
                data = pixels.get_pixels()
                def rgb(x,y):
                    i = y*pixels.get_rowstride()+x*pixels.get_n_channels()
                    return tuple(data[i:i+3])
                self.assertEqual(rgb(1,100),(0,0,0))
                self.assertEqual(rgb(100,100),(255,0,0))
                self.assertEqual(rgb(199,100),(0,0,0))
            finally:
                card.close()
                window.destroy()

    def test_software_screensaver_reset_is_ignored_but_raw_keypress_resets_idle(self):
        import ctypes as C
        idle = runtime.IdleClock()
        try:
            time.sleep(.2)
            before = idle.seconds()
            idle.x.XResetScreenSaver.argtypes = [C.c_void_p]
            idle.x.XSync.argtypes = [C.c_void_p, C.c_int]
            idle.x.XResetScreenSaver(idle.display)
            idle.x.XSync(idle.display, 0)
            self.assertGreaterEqual(idle.seconds(), before)
            xtest = C.CDLL('libXtst.so.6')
            xtest.XTestFakeKeyEvent.argtypes = [C.c_void_p, C.c_uint, C.c_int, C.c_ulong]
            xtest.XTestFakeKeyEvent(idle.display, 38, 1, 0)
            xtest.XTestFakeKeyEvent(idle.display, 38, 0, 0)
            idle.x.XSync(idle.display, 0)
            self.assertLess(idle.seconds(), .1)
            self.assertGreater(idle.generation, 0)
        finally:
            idle.close()

    def test_raw_input_is_seen_while_another_client_holds_keyboard_grab(self):
        import ctypes as C
        idle = runtime.IdleClock()
        other = idle.x.XOpenDisplay(None)
        try:
            root = idle.x.XDefaultRootWindow(other)
            idle.x.XGrabKeyboard.argtypes = [C.c_void_p,C.c_ulong,C.c_int,C.c_int,C.c_int,C.c_ulong]
            idle.x.XUngrabKeyboard.argtypes = [C.c_void_p,C.c_ulong]
            idle.x.XSync.argtypes = [C.c_void_p,C.c_int]
            self.assertEqual(idle.x.XGrabKeyboard(other,root,0,1,1,0), 0)
            idle.x.XSync(other,0)
            xtest = C.CDLL('libXtst.so.6')
            xtest.XTestFakeKeyEvent.argtypes = [C.c_void_p,C.c_uint,C.c_int,C.c_ulong]
            xtest.XTestFakeKeyEvent(other,38,1,0)
            xtest.XTestFakeKeyEvent(other,38,0,0)
            idle.x.XSync(other,0)
            idle.seconds()
            self.assertGreater(idle.generation, 0)
        finally:
            idle.x.XUngrabKeyboard(other,0)
            idle.x.XCloseDisplay(other)
            idle.close()

    def test_manual_preview_still_runs_when_bridge_runtime_is_unavailable(self):
        from gi.repository import GdkPixbuf
        from types import SimpleNamespace
        from unittest.mock import patch
        from media_screensaver import main
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'photo.png'
            photo = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB,False,8,20,40)
            photo.fill(0xff0000ff)
            photo.savev(str(path),'png',[],[])
            args = SimpleNamespace(media=Path(directory),seconds=.2,report=None,plain=True,details=False)
            geometry = [dict(name=str(i),x=i*100,y=0,width=100,height=100) for i in range(3)]
            with patch.object(main,'monitors',return_value=geometry), patch.object(main.bridge,'runtime_dir',side_effect=RuntimeError('fixture bridge unavailable')):
                self.assertIsNone(main.preview(args))
            self.assertTrue(path.is_file())

    def test_starting_middle_video_dismisses_and_releases_manual_preview(self):
        from gi.repository import GdkPixbuf
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'photo.png'
            photo = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB,False,8,20,40)
            photo.fill(0xff0000ff)
            photo.savev(str(path),'png',[],[])
            started = time.monotonic()
            def gate():
                return (True,'browser bridge ready') if time.monotonic()-started<.2 else (False,'playing video on the middle display')
            events = []
            runtime.run([path],[dict(name=str(i),x=i*100,y=0,width=100,height=100) for i in range(3)],
                        seconds=2,gate=gate,automatic=False,emit=lambda *args: None,report=events.append)
            self.assertEqual([e['reason'] for e in events if e['event']=='dismiss'],['playing video on the middle display'])
            self.assertEqual(events[-1]['event'],'cleanup')
            self.assertEqual(events[-1]['players'],0)

    def test_idle_query_is_read_only_and_returns_seconds(self):
        idle = runtime.IdleClock()
        try:
            self.assertGreaterEqual(idle.seconds(), 0)
        finally:
            idle.close()

if __name__ == '__main__': unittest.main()
