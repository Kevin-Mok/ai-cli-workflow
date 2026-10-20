"""Persistent GTK/GStreamer cards; X11 screensaver idle is queried, never reset."""
import ctypes as C
from pathlib import Path
import signal
import subprocess
import tempfile
import time

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gdk, GdkPixbuf, GLib, Gst, Gtk

from .core import Conveyor, VIDEOS, placement

Gst.init(None)
# gtksink uses system memory; prefer libav over CUDA-only decoders on this CPU sink.
for factory in Gst.Registry.get().get_feature_list(Gst.ElementFactory):
    if factory.get_name().startswith('avdec_'):
        factory.set_rank(Gst.Rank.PRIMARY + 100)


class XIEventMask(C.Structure):
    _fields_ = [('deviceid', C.c_int), ('mask_len', C.c_int), ('mask', C.POINTER(C.c_ubyte))]


class EventCookie(C.Structure):
    _fields_ = [('type', C.c_int), ('serial', C.c_ulong), ('send_event', C.c_int),
                ('display', C.c_void_p), ('extension', C.c_int), ('evtype', C.c_int),
                ('cookie', C.c_uint), ('data', C.c_void_p)]


class IdleClock:
    """Track real XI2 keyboard/mouse activity, unaffected by player idle resets."""
    def __init__(self):
        self.x = C.CDLL('libX11.so.6')
        self.xi = C.CDLL('libXi.so.6')
        self.x.XOpenDisplay.argtypes = [C.c_char_p]
        self.x.XOpenDisplay.restype = C.c_void_p
        self.x.XDefaultRootWindow.argtypes = [C.c_void_p]
        self.x.XDefaultRootWindow.restype = C.c_ulong
        self.x.XCloseDisplay.argtypes = [C.c_void_p]
        self.x.XPending.argtypes = [C.c_void_p]
        self.x.XNextEvent.argtypes = [C.c_void_p, C.c_void_p]
        self.x.XFlush.argtypes = [C.c_void_p]
        self.x.XQueryExtension.argtypes = [C.c_void_p, C.c_char_p, C.POINTER(C.c_int), C.POINTER(C.c_int), C.POINTER(C.c_int)]
        self.xi.XIQueryVersion.argtypes = [C.c_void_p, C.POINTER(C.c_int), C.POINTER(C.c_int)]
        self.xi.XISelectEvents.argtypes = [C.c_void_p, C.c_ulong, C.POINTER(XIEventMask), C.c_int]
        self.display = self.x.XOpenDisplay(None)
        if not self.display:
            raise ValueError('Cannot open X11 display; run inside the desktop session.')
        self.last_activity = time.monotonic()
        self.generation = 0
        self.opcode = C.c_int()
        event, error = C.c_int(), C.c_int()
        major, minor = C.c_int(2), C.c_int(1)
        if (not self.x.XQueryExtension(self.display, b'XInputExtension', C.byref(self.opcode), C.byref(event), C.byref(error))
                or self.xi.XIQueryVersion(self.display, C.byref(major), C.byref(minor)) != 0):
            self.close()
            raise ValueError('XInput2.1 unavailable; raw keyboard/mouse idle activation disabled.')
        # XIAllMasterDevices=1; RawKeyPress=13, RawButtonPress=15, RawMotion=17.
        bits = (1 << 13) | (1 << 15) | (1 << 17)
        mask = (C.c_ubyte * 3)(*(bits.to_bytes(3, 'little')))
        selection = XIEventMask(1, 3, mask)
        if self.xi.XISelectEvents(self.display, self.x.XDefaultRootWindow(self.display), C.byref(selection), 1) != 0:
            self.close()
            raise ValueError('Cannot subscribe to XInput2; automatic activation disabled.')
        self.x.XFlush(self.display)

    def seconds(self):
        event = (C.c_long * 24)()
        while self.x.XPending(self.display):
            self.x.XNextEvent(self.display, event)
            cookie = C.cast(event, C.POINTER(EventCookie)).contents
            if cookie.type == 35 and cookie.extension == self.opcode.value and cookie.evtype in (13, 15, 17):
                self.last_activity = time.monotonic()
                self.generation += 1
        return time.monotonic() - self.last_activity

    def close(self):
        if self.display:
            self.x.XCloseDisplay(self.display)
            self.display = None


def load_photo(path):
    return GdkPixbuf.Pixbuf.new_from_file(str(path)).apply_embedded_orientation()


class Card:
    def __init__(self, entry, failed):
        self.entry = entry
        self.failed = failed
        self.pipeline = None
        self.bus = None
        self.conversion = None
        self.temporary = None
        self.timer = None
        self.closed = False
        self.pixbuf = None
        if entry.path.suffix.lower() in VIDEOS:
            self.pipeline = Gst.ElementFactory.make('playbin')
            sink = Gst.ElementFactory.make('gtksink')
            if self.pipeline is None or sink is None:
                raise ValueError('GStreamer playbin/gtksink missing; install the documented packages.')
            self.widget = sink.get_property('widget')
            sink.set_property('force-aspect-ratio', True)
            self.pipeline.set_property('video-sink', sink)
            self.pipeline.set_property('audio-sink', Gst.ElementFactory.make('fakesink'))
            self.pipeline.set_property('flags', 1)  # Video only: never open an audio device.
            self.pipeline.set_property('mute', True)
            self.pipeline.set_property('uri', entry.path.absolute().as_uri())
            self.bus = self.pipeline.get_bus()
            self.bus.add_signal_watch()
            self.handler = self.bus.connect('message', self.message)
            self.widget.connect('realize', lambda *_: self.pipeline.set_state(Gst.State.PLAYING))
        else:
            self.widget = Gtk.DrawingArea()
            self.widget.connect('draw', self.draw)
            if entry.path.suffix.lower() == '.heic':
                self.temporary = tempfile.TemporaryDirectory(prefix='media-screensaver-heic-')
                dest = Path(self.temporary.name) / 'frame.png'
                self.conversion = subprocess.Popen(
                    ['convert', '-limit', 'memory', '256MiB', '-limit', 'map', '512MiB',
                     str(entry.path.absolute()) + '[0]', '-auto-orient', '-resize', '3840x2160>', str(dest)],
                    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.decode_started = time.monotonic()
                self.timer = GLib.timeout_add(50, self.converted, dest)
            else:
                try:
                    self.pixbuf = load_photo(entry.path)
                except GLib.Error:
                    GLib.idle_add(self.reject, 'Image decoding failed')

    def reject(self, reason):
        if not self.closed:
            self.failed(self.entry, reason)
        return False

    def converted(self, dest):
        if self.conversion.poll() is None and time.monotonic() - self.decode_started < 10:
            return True
        self.timer = None
        if self.conversion.poll() == 0:
            try:
                self.pixbuf = load_photo(dest)
                self.widget.queue_draw()
            except GLib.Error:
                return self.reject('HEIC decoded image could not be loaded')
            self.temporary.cleanup()
            self.temporary = None
        else:
            return self.reject('HEIC decoder failed or timed out; check ImageMagick HEIC support')
        return False

    def draw(self, widget, cr):
        cr.set_source_rgb(0, 0, 0)
        cr.paint()
        if self.pixbuf:
            w, h = widget.get_allocated_width(), widget.get_allocated_height()
            pw, ph = self.pixbuf.get_width(), self.pixbuf.get_height()
            scale = min(w / pw, h / ph)
            cr.translate((w - pw * scale) / 2, (h - ph * scale) / 2)
            cr.scale(scale, scale)
            Gdk.cairo_set_source_pixbuf(cr, self.pixbuf, 0, 0)
            cr.paint()
        return False

    def message(self, bus, message):
        if self.closed:
            return
        if message.type == Gst.MessageType.ERROR:
            error, _ = message.parse_error()
            self.reject('Video decoding failed: ' + error.message)
        elif message.type == Gst.MessageType.EOS:
            if not self.pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0):
                self.reject('Video could not loop')

    def position(self):
        if self.pipeline:
            ok, nanoseconds = self.pipeline.query_position(Gst.Format.TIME)
            return round(nanoseconds / Gst.SECOND, 3) if ok else None
        return None

    def close(self):
        if self.closed:
            return
        self.closed = True
        if self.timer:
            GLib.source_remove(self.timer)
            self.timer = None
        if self.bus:
            self.bus.disconnect(self.handler)
            self.bus.remove_signal_watch()
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
            self.pipeline.get_state(2 * Gst.SECOND)
        if self.conversion and self.conversion.poll() is None:
            self.conversion.terminate()
            try:
                self.conversion.wait(timeout=.5)
            except subprocess.TimeoutExpired:
                self.conversion.kill()
                self.conversion.wait()
        if self.temporary:
            self.temporary.cleanup()
            self.temporary = None
        self.widget.destroy()


def run(paths, monitors, *, seconds, gate, automatic, emit, report=None):
    if not Gtk.init_check()[0]:
        raise ValueError('GTK cannot open X11 display; launch from the desktop session.')
    clock = IdleClock()
    window = Gtk.Window(type=Gtk.WindowType.POPUP)
    window.set_title('Media conveyor screensaver')
    window.set_accept_focus(False)
    left = min(m['x'] for m in monitors)
    top = min(m['y'] for m in monitors)
    width = max(m['x'] + m['width'] for m in monitors) - left
    height = max(m['y'] + m['height'] for m in monitors) - top
    window.move(left, top)
    window.set_default_size(width, height)
    layout = Gtk.Layout()
    window.add(layout)
    css = Gtk.CssProvider()
    css.load_from_data(b'* { background-color: black; }')
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    window.connect('delete-event', lambda *_: Gtk.main_quit())
    start = time.monotonic()
    conveyor = Conveyor(paths, start)
    cards = {}
    last_gate = 0
    last_video = gate()[1].startswith('playing video')
    last_step = 0
    done_step = -1
    error_count = 0
    exit_error = None
    blank = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), 'none')

    def event(kind, **values):
        if report:
            report(dict(event=kind, elapsed=round(time.monotonic() - start, 3), **values))

    def failed(entry, reason):
        nonlocal error_count
        error_count += 1
        event('decode-error', item=entry.identity, format=entry.path.suffix.lower())
        emit('warning', f'Skipped item #{entry.identity} ({entry.path.suffix.lower()}); decoder failed.', reason)
        conveyor.reject(entry.path)

    def positions(kind):
        event(kind, items=[dict(item=e.identity, slot=e.slot, position=cards[e.identity].position(),
                               format=e.path.suffix.lower()) for e in conveyor.entries if e.identity in cards])

    def frame(*_):
        nonlocal last_gate, last_video, last_step, done_step, exit_error
        now = time.monotonic()
        try:
            idle = clock.seconds()
            if clock.generation:
                event('dismiss', reason='input')
                Gtk.main_quit()
                return False
            if now - last_gate >= .25:
                last_gate = now
                allowed, reason = gate()
                video = reason.startswith('playing video')
                if (video and not last_video) or (automatic and not allowed):
                    event('dismiss', reason=reason)
                    Gtk.main_quit()
                    return False
                last_video = video
            if seconds and now - start >= seconds:
                event('dismiss', reason='duration')
                Gtk.main_quit()
                return False
            conveyor.tick(now)
            live = {entry.identity for entry in conveyor.entries}
            for identity in list(cards):
                if identity not in live:
                    event('release', item=identity, position=cards[identity].position())
                    cards.pop(identity).close()
            for entry in list(conveyor.entries):
                if entry.identity not in cards:
                    card = Card(entry, failed)
                    cards[entry.identity] = card
                    layout.put(card.widget, 0, 0)
                    card.widget.show_all()
                    event('enter', item=entry.identity, format=entry.path.suffix.lower())
                rect = placement(monitors, entry.slot, conveyor.progress(now))
                card = cards[entry.identity]
                card.widget.set_size_request(rect['width'], rect['height'])
                layout.move(card.widget, rect['x'] - left, rect['y'] - top)
            step = conveyor.sequence
            if step != last_step:
                last_step = step
                positions('advance')
                emit('progress', f'Conveyor active · {int(now - start)}s · {len(cards)} items · {error_count} skipped')
            if conveyor.progress(now) == 1 and done_step != step:
                done_step = step
                positions('settled')
            if not conveyor.paths:
                raise ValueError('No decodable media remains; run media-screensaver probe --media DIR.')
            return True
        except Exception as error:
            exit_error = error
            Gtk.main_quit()
            return False

    signal_sources = [GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, sig, lambda: (Gtk.main_quit(), False)[1])
                      for sig in (signal.SIGTERM, signal.SIGINT)]
    window.show_all()
    window.get_window().set_cursor(blank)
    # Frame-clock callbacks track actual display refresh instead of accumulating timer drift.
    callback = window.add_tick_callback(frame)
    try:
        Gtk.main()
    finally:
        window.remove_tick_callback(callback)
        for source in signal_sources:
            if GLib.MainContext.default().find_source_by_id(source):
                GLib.source_remove(source)
        for identity, card in list(cards.items()):
            event('release', item=identity, position=card.position())
            card.close()
        cards.clear()
        window.destroy()
        clock.close()
        event('cleanup', players=0)
        emit('success', 'Preview closed; all playback pipelines released.')
    if exit_error:
        raise exit_error
