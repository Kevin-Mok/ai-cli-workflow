"""Pixel regressions for metadata and additional displayed-picture rotation."""
import hashlib
import importlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from media_screensaver import renderer
from media_screensaver.core import Entry
from gi.repository import Gdk, Gtk, Gst


def pump(seconds=.25):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        time.sleep(.01)


class OrientationFixtures:
    @classmethod
    def setUpClass(cls):
        assert Gtk.init_check()[0], "X11 display required"
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.paths = {}
        colors = [bytes((255, 0, 0)), bytes((0, 255, 0)), bytes((0, 0, 255)), bytes((255, 255, 0))]
        for shape, w, h in [('landscape', 120, 80), ('portrait', 80, 120)]:
            ppm = cls.root / (shape + '.ppm')
            ppm.write_bytes(f'P6\n{w} {h}\n255\n'.encode() + b''.join(
                colors[(y >= h//2)*2 + (x >= w//2)] for y in range(h) for x in range(w)))
            base = cls.root / (shape + ' no metadata.mp4')
            subprocess.run(['ffmpeg', '-v', 'error', '-loop', '1', '-i', str(ppm), '-t', '1',
                            '-r', '20', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(base)], check=True)
            cls.paths[shape, 0] = base
            for degrees in (90, 180, 270):
                dest = cls.root / f'{shape} rotate {degrees}.mov'
                subprocess.run(['ffmpeg', '-v', 'error', '-noautorotate', '-display_rotation', str(degrees),
                                '-i', str(base), '-c', 'copy', str(dest)], check=True)
                import json
                metadata = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream_side_data=rotation', '-of', 'json', str(dest)]))
                assert metadata['streams'][0]['side_data_list'][0]['rotation'] % 360 == degrees
                cls.paths[shape, degrees] = dest

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def capture(self, card, window):
        pump(.35)
        width, height = card.widget.get_allocated_width(), card.widget.get_allocated_height()
        x, y = card.widget.translate_coordinates(window, 0, 0)
        pix = Gdk.pixbuf_get_from_window(window.get_window(), x, y, width, height)
        data = pix.get_pixels()
        def color(x, y):
            i = int(y)*pix.get_rowstride() + int(x)*pix.get_n_channels()
            rgb = tuple(data[i:i+3])
            return tuple(round(c/255) for c in rgb)
        # Square window; quadrants sit inside either portrait or landscape bars.
        return [color(width*x, height*y) for x, y in ((.35,.35),(.65,.35),(.35,.65),(.65,.65))]

class OrientationPixels(OrientationFixtures, unittest.TestCase):
    def test_metadata_rotates_displayed_pixels_for_all_directions_and_shapes(self):
        expected = {
            0: [(1,0,0),(0,1,0),(0,0,1),(1,1,0)],
            90: [(0,1,0),(1,1,0),(1,0,0),(0,0,1)],
            180: [(1,1,0),(0,0,1),(0,1,0),(1,0,0)],
            270: [(0,0,1),(1,0,0),(1,1,0),(0,1,0)],
        }
        with patch.dict(os.environ, {'XDG_CONFIG_HOME': str(self.root / 'config')}):
            for (shape, degrees), path in self.paths.items():
                with self.subTest(shape=shape, metadata=degrees):
                    before = hashlib.sha256(path.read_bytes()).digest()
                    errors = []
                    card = renderer.Card(Entry(1, path), lambda *args: errors.append(args))
                    window = Gtk.Window()
                    window.set_default_size(240,240)
                    window.add(card.widget)
                    window.show_all()
                    try:
                        self.assertEqual(self.capture(card, window), expected[degrees])
                        # Both orientations must fit inside the square without cropping.
                        pix = Gdk.pixbuf_get_from_window(window.get_window(),0,0,*window.get_size())
                        raw = pix.get_pixels()
                        index = pix.get_rowstride() + pix.get_n_channels()
                        self.assertEqual(tuple(raw[index:index+3]),(0,0,0))
                        self.assertFalse(errors)
                    finally:
                        card.close()
                        window.destroy()
                    self.assertEqual(card.pipeline.get_state(Gst.SECOND)[1], Gst.State.NULL)
                    self.assertEqual(hashlib.sha256(path.read_bytes()).digest(), before)

    def test_saved_corrections_rotate_after_metadata_and_survive_loop_and_movement(self):
        from media_screensaver.orientation import OrientationStore
        expected = {
            0: [(0,1,0),(1,1,0),(1,0,0),(0,0,1)],
            90: [(1,0,0),(0,1,0),(0,0,1),(1,1,0)],
            180: [(0,0,1),(1,0,0),(1,1,0),(0,1,0)],
            270: [(1,1,0),(0,0,1),(0,1,0),(1,0,0)],
        }
        with tempfile.TemporaryDirectory() as config, patch.dict(os.environ, {'XDG_CONFIG_HOME':config}):
            path = self.paths['landscape',90]
            for degrees in (0,90,180,270):
                with self.subTest(additional=degrees):
                    OrientationStore().save(path, degrees)
                    errors = []
                    card = renderer.Card(Entry(1,path), lambda *args: errors.append(args))
                    window = Gtk.Window()
                    window.set_default_size(240,240)
                    layout = Gtk.Layout()
                    window.add(layout)
                    layout.put(card.widget,0,0)
                    card.widget.set_size_request(240,240)
                    window.show_all()
                    pipeline = card.pipeline
                    try:
                        self.assertEqual(self.capture(card,window), expected[degrees])
                        positions = []
                        for slot in range(3):
                            layout.move(card.widget,slot*3,0)
                            pump(.45)
                            positions.append(card.position())
                            self.assertEqual(self.capture(card,window), expected[degrees])
                        self.assertIs(card.pipeline,pipeline)
                        self.assertTrue(any(b<a for a,b in zip(positions,positions[1:])),positions)
                        self.assertFalse(errors)
                    finally:
                        card.close()
                        window.destroy()
                    self.assertEqual(pipeline.get_state(Gst.SECOND)[1],Gst.State.NULL)


class OrientationRecords(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = patch.dict(os.environ, {'XDG_CONFIG_HOME': str(self.root / 'private')})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.assertIsNotNone(importlib.util.find_spec('media_screensaver.orientation'), 'orientation store missing')
        self.store = importlib.import_module('media_screensaver.orientation').OrientationStore()
        self.video = self.root / 'video with spaces.mov'
        self.video.write_bytes(b'fixture')

    def test_save_reopen_reset_preserves_other_entries_and_private_modes(self):
        other = self.root / 'other.mp4'
        other.write_bytes(b'other')
        self.assertEqual(self.store.load(self.video), 0)
        self.store.save(other, 90)
        for degrees in (0,90,180,270):
            self.store.save(self.video, degrees)
            self.assertEqual(type(self.store)().load(self.video), degrees)
        self.store.save(self.video, 0)
        self.assertEqual(self.store.load(self.video), 0)
        self.assertEqual(self.store.load(other), 90)
        self.assertEqual(self.store.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.store.path.parent.stat().st_mode & 0o777, 0o700)

    def test_changed_file_ignores_saved_correction_and_refuses_stale_review(self):
        self.store.save(self.video, 270)
        stat = self.video.stat()
        self.video.write_bytes(b'changed size')
        self.assertEqual(self.store.load(self.video), 0)
        original = self.store.path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.store.save(self.video, 90, expected=(stat.st_size, stat.st_mtime_ns))
        self.assertEqual(self.store.path.read_bytes(), original)

    def test_malformed_records_refuse_read_and_save_without_overwriting(self):
        import json
        self.store.path.parent.mkdir(parents=True)
        for data in ('{', '[]', '{"version":true,"files":{}}',
                     json.dumps({'version':1,'files':{str(self.video):{'size':1,'mtime_ns':1,'clockwise':45}}}),
                     json.dumps({'version':1,'files':{'relative.mov':{'size':1,'mtime_ns':1,'clockwise':90}}}),
                     json.dumps({'version':1,'files':{str(self.video):{'size':True,'mtime_ns':1,'clockwise':90}}})):
            with self.subTest(data=data):
                self.store.path.write_text(data)
                with self.assertRaises(ValueError): self.store.load(self.video)
                with self.assertRaises(ValueError): self.store.save(self.video, 90)
                self.assertEqual(self.store.path.read_text(), data)

    def test_competing_saves_preserve_each_files_record(self):
        paths = [self.root/f'concurrent {i}.mov' for i in range(8)]
        for path in paths: path.write_bytes(b'fixture')
        script = 'import sys; from pathlib import Path; from media_screensaver.orientation import OrientationStore; OrientationStore().save(Path(sys.argv[1]),90)'
        env = dict(os.environ,PYTHONPATH=str(Path(__file__).resolve().parents[1]/'scripts'))
        children = [subprocess.Popen([sys.executable,'-c',script,str(path)],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE) for path in paths]
        try:
            for child in children:
                out,error = child.communicate(timeout=10)
                self.assertEqual(child.returncode,0,error.decode())
            for path in paths: self.assertEqual(self.store.load(path),90)
        finally:
            for child in children:
                if child.poll() is None: child.kill(); child.wait()

    def test_failed_atomic_replace_preserves_previous_records_and_removes_temporary(self):
        self.store.save(self.video,90)
        previous = self.store.path.read_bytes()
        with patch.object(Path,'replace',side_effect=OSError('simulated full disk')):
            with self.assertRaises(OSError): self.store.save(self.video,180)
        self.assertEqual(self.store.path.read_bytes(),previous)
        self.assertEqual(list(self.store.path.parent.glob('.orientation-*')),[])

    def test_same_size_new_mtime_ignores_correction(self):
        self.store.save(self.video,90)
        stat = self.video.stat()
        os.utime(self.video,ns=(stat.st_atime_ns,stat.st_mtime_ns+1000000000))
        self.assertEqual(self.store.load(self.video),0)

    def test_symlink_store_does_not_overwrite_target(self):
        self.store.path.parent.mkdir(parents=True)
        target = self.root / 'unrelated'
        target.write_text('protected')
        self.store.path.symlink_to(target)
        with self.assertRaises((OSError, ValueError)): self.store.save(self.video, 90)
        self.assertEqual(target.read_text(), 'protected')

class ReviewTests(OrientationFixtures, unittest.TestCase):
    def test_buttons_rotate_display_pixels_save_reopen_reset_cancel_and_cleanup(self):
        self.assertIsNotNone(importlib.util.find_spec('media_screensaver.review'), 'orientation review missing')
        review = importlib.import_module('media_screensaver.review')
        from media_screensaver.orientation import OrientationStore
        path = self.paths['landscape', 90]  # Deliberately wrong metadata for this picture.
        before = hashlib.sha256(path.read_bytes()).digest()
        with tempfile.TemporaryDirectory() as config, patch.dict(os.environ, {'XDG_CONFIG_HOME':config}):
            window = review.OrientationReview(path, lambda *args: None)
            window.show_all()
            pipeline = window.card.pipeline
            try:
                window.buttons['Rotate right 90°'].clicked()
                self.assertEqual(self.capture(window.card, window), [(1,0,0),(0,1,0),(0,0,1),(1,1,0)])
                window.buttons['Rotate right 90°'].clicked()
                self.assertEqual(window.rotation, 180)
                window.buttons['Rotate left 90°'].clicked()
                self.assertEqual(window.rotation, 90)
                window.buttons['Save'].clicked()
                self.assertEqual(OrientationStore().load(path), 90)
                self.assertEqual(pipeline.get_state(Gst.SECOND)[1], Gst.State.NULL)
                reopened = review.OrientationReview(path, lambda *args: None)
                reopened.show_all()
                try:
                    self.assertEqual(reopened.rotation, 90)
                    reopened.buttons['Use metadata'].clicked()
                    self.assertEqual(reopened.rotation, 0)
                    reopened.buttons['Cancel'].clicked()
                    self.assertEqual(OrientationStore().load(path), 90)
                finally:
                    reopened.destroy()
                reset = review.OrientationReview(path, lambda *args: None)
                reset.buttons['Use metadata'].clicked()
                reset.buttons['Save'].clicked()
                self.assertEqual(OrientationStore().load(path), 0)
            finally:
                window.destroy()
            self.assertEqual(hashlib.sha256(path.read_bytes()).digest(), before)

    def test_cli_file_dispatch_closes_review_and_chooser_cancel_returns(self):
        from media_screensaver import main
        from media_screensaver.review import OrientationReview
        from gi.repository import GLib
        seen = []
        def cancel():
            for window in Gtk.Window.list_toplevels():
                if isinstance(window,OrientationReview):
                    seen.append('review')
                    window.buttons['Cancel'].clicked()
                    return False
                if isinstance(window,Gtk.FileChooserDialog):
                    seen.append('chooser')
                    window.response(Gtk.ResponseType.CANCEL)
                    return False
            return True
        with tempfile.TemporaryDirectory() as config, patch.dict(os.environ, {'XDG_CONFIG_HOME':config}):
            GLib.timeout_add(100,cancel)
            self.assertEqual(main.main(['orient','--file',str(self.paths['landscape',90]),'--plain']),0)
            GLib.timeout_add(100,cancel)
            self.assertEqual(main.main(['orient','--media',str(self.root),'--plain']),0)
            self.assertEqual(seen,['review','chooser'])
            self.assertFalse((Path(config)/'media-screensaver/orientation.json').exists())
            self.assertEqual(main.main(['orient','--file',str(self.root/'missing.mov'),'--plain']),1)

    def test_plain_cli_save_and_periodic_progress_are_ascii(self):
        import contextlib
        import io
        from media_screensaver import main
        from media_screensaver.review import OrientationReview
        from gi.repository import GLib
        def save():
            for window in Gtk.Window.list_toplevels():
                if isinstance(window,OrientationReview):
                    window.buttons['Rotate right 90°'].clicked()
                    window.buttons['Save'].clicked()
                    return False
            return True
        with tempfile.TemporaryDirectory() as config, patch.dict(os.environ, {'XDG_CONFIG_HOME':config}):
            captured = io.StringIO()
            GLib.timeout_add(150,save)
            with patch.object(GLib,'timeout_add_seconds',side_effect=lambda seconds,callback: GLib.timeout_add(20,callback)), contextlib.redirect_stderr(captured):
                self.assertEqual(main.main(['orient','--file',str(self.paths['landscape',0]),'--plain']),0)
            self.assertIn('awaiting Save or Cancel',captured.getvalue())
            self.assertIn('Saved additional correction',captured.getvalue())
            self.assertTrue(captured.getvalue().isascii())

    def test_decoder_failure_disables_save_and_close_releases_pipeline(self):
        from media_screensaver.review import OrientationReview
        path = self.root/'broken.mp4'
        path.write_bytes(b'not a video')
        with tempfile.TemporaryDirectory() as config, patch.dict(os.environ, {'XDG_CONFIG_HOME':config}):
            events = []
            window = OrientationReview(path,lambda *args: events.append(args))
            window.show_all()
            pipeline = window.card.pipeline
            try:
                pump(.5)
                self.assertFalse(window.buttons['Save'].get_sensitive())
                window.buttons['Save'].clicked()
                self.assertTrue(window.get_visible())
                self.assertTrue(events)
                self.assertFalse((Path(config)/'media-screensaver/orientation.json').exists())
            finally:
                window.destroy()
            self.assertEqual(pipeline.get_state(Gst.SECOND)[1],Gst.State.NULL)

    def test_chooser_starts_in_library_and_cancel_writes_nothing(self):
        from media_screensaver.review import choose_file
        from gi.repository import GLib
        seen = []
        def cancel():
            for window in Gtk.Window.list_toplevels():
                if isinstance(window,Gtk.FileChooserDialog):
                    folder = window.get_current_folder()
                    if folder is None: return True
                    seen.append(folder)
                    window.response(Gtk.ResponseType.CANCEL)
                    return False
            return True
        GLib.timeout_add(100,cancel)
        self.assertIsNone(choose_file(self.root))
        self.assertEqual(seen,[str(self.root)])

    def test_keyboard_mouse_do_not_dismiss_review(self):
        import ctypes as C
        from media_screensaver.review import OrientationReview
        with tempfile.TemporaryDirectory() as config, patch.dict(os.environ, {'XDG_CONFIG_HOME':config}):
            window = OrientationReview(self.paths['landscape',0],lambda *args: None)
            window.show_all()
            clock = renderer.IdleClock()
            try:
                pump(.3)
                clock.x.XSync.argtypes = [C.c_void_p,C.c_int]
                xtest = C.CDLL('libXtst.so.6')
                xtest.XTestFakeKeyEvent.argtypes = [C.c_void_p,C.c_uint,C.c_int,C.c_ulong]
                xtest.XTestFakeMotionEvent.argtypes = [C.c_void_p,C.c_int,C.c_int,C.c_int,C.c_ulong]
                xtest.XTestFakeMotionEvent(clock.display,-1,100,100,0)
                xtest.XTestFakeKeyEvent(clock.display,38,1,0)
                xtest.XTestFakeKeyEvent(clock.display,38,0,0)
                clock.x.XSync(clock.display,0)
                pump(.3)
                self.assertTrue(window.get_visible())
                self.assertGreater(clock.seconds(),0)
                self.assertGreater(clock.generation,0)
            finally:
                clock.close()
                window.destroy()

    def test_invalid_store_warns_but_plays_and_save_stays_open(self):
        self.assertIsNotNone(importlib.util.find_spec('media_screensaver.review'), 'orientation review missing')
        from media_screensaver.review import OrientationReview
        with tempfile.TemporaryDirectory() as config, patch.dict(os.environ, {'XDG_CONFIG_HOME':config}):
            dest = Path(config) / 'media-screensaver/orientation.json'
            dest.parent.mkdir()
            dest.write_text('{broken')
            events = []
            window = OrientationReview(self.paths['portrait',0], lambda *args: events.append(args))
            window.show_all()
            try:
                pump(.3)
                self.assertTrue(events)
                window.buttons['Save'].clicked()
                self.assertTrue(window.get_visible())
                self.assertEqual(dest.read_text(), '{broken')
                self.assertIn('not saved', window.status.get_text().lower())
            finally:
                window.destroy()


if __name__ == '__main__':
    unittest.main()
