"""Separate, interactive orientation review using the screensaver's video Card."""
from pathlib import Path
import signal
import time

from .core import Entry, VIDEOS
from .orientation import OrientationStore
from .renderer import Card, GLib, Gtk


class OrientationReview(Gtk.Window):
    def __init__(self, path, emit):
        super().__init__(title='Review video orientation')
        self.set_default_size(800, 650)
        self.path = path.absolute()
        self.emit = emit
        stat = self.path.stat()
        self.fingerprint = stat.st_size, stat.st_mtime_ns
        self.status = Gtk.Label()
        self.status.set_line_wrap(True)
        self.card = Card(Entry(0, self.path), self.failed, warning=self.warning)
        self.rotation = self.card.rotation
        self.buttons = {}
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_border_width(12)
        self.add(content)
        title = Gtk.Label(label=self.path.name)
        title.set_line_wrap(True)
        content.pack_start(title, False, False, 0)
        content.pack_start(self.card.widget, True, True, 0)
        self.card.widget.set_size_request(240, 240)
        self.adjustment = Gtk.Label()
        content.pack_start(self.adjustment, False, False, 0)
        controls = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        controls.set_layout(Gtk.ButtonBoxStyle.EXPAND)
        content.pack_start(controls, False, False, 0)
        for label, action in (
            ('Rotate left 90°', lambda: self.rotate(-90)),
            ('Rotate right 90°', lambda: self.rotate(90)),
            ('Use metadata', lambda: self.rotate(-self.rotation)),
            ('Save', self.save), ('Cancel', self.destroy),
        ):
            button = Gtk.Button(label=label)
            button.connect('clicked', lambda _, callback=action: callback())
            controls.add(button)
            self.buttons[label] = button
        content.pack_start(self.status, False, False, 0)
        self.connect('destroy', lambda *_: self.card.close())
        self.rotate(0)

    def warning(self, message):
        self.status.set_text('⚠️ ' + message)
        self.emit('warning', message)

    def failed(self, entry, reason):
        self.buttons['Save'].set_sensitive(False)
        self.warning(reason)

    def rotate(self, degrees):
        self.rotation = (self.rotation + degrees) % 360
        self.card.rotate(self.rotation)
        self.adjustment.set_text(f'Additional correction: {self.rotation}° clockwise')

    def save(self):
        if not self.buttons['Save'].get_sensitive():
            return
        try:
            OrientationStore().save(self.path, self.rotation, expected=self.fingerprint)
        except (OSError, ValueError) as error:
            self.warning('Correction not saved: ' + str(error))
            return
        self.emit('success', f'Saved additional correction: {self.rotation} degrees clockwise; original unchanged.')
        self.destroy()


def choose_file(directory):
    chooser = Gtk.FileChooserDialog(title='Choose a video to orient', action=Gtk.FileChooserAction.OPEN)
    chooser.add_buttons('Cancel', Gtk.ResponseType.CANCEL, 'Open', Gtk.ResponseType.OK)
    chooser.set_current_folder(str(directory.absolute()))
    videos = Gtk.FileFilter()
    videos.set_name('Videos (MP4, MOV, MKV)')
    # MIME filters include uppercase filename extensions.
    videos.add_mime_type('video/*')
    for extension in VIDEOS:
        videos.add_pattern('*' + extension)
        videos.add_pattern('*' + extension.upper())
    chooser.add_filter(videos)
    try:
        if chooser.run() == Gtk.ResponseType.OK:
            return Path(chooser.get_filename())
        return None
    finally:
        chooser.destroy()


def run(args, emit):
    if not Gtk.init_check()[0]:
        raise ValueError('GTK cannot open X11 display; launch from the desktop session.')
    path = args.file if args.file is not None else choose_file(args.media)
    if path is None:
        emit('info', 'Orientation review cancelled; nothing saved.')
        return 0
    if not path.is_file() or path.is_symlink() or path.suffix.lower() not in VIDEOS:
        raise ValueError('Choose an existing MP4, MOV or MKV video with --file FILE.')
    window = OrientationReview(path, emit)
    window.connect('destroy', lambda *_: Gtk.main_quit())
    window.show_all()
    emit('info', 'Orientation review open; rotate the displayed picture, then Save or Cancel.')
    start = time.monotonic()
    def progress():
        emit('progress', f'Orientation review open | {int(time.monotonic() - start)}s | awaiting Save or Cancel')
        return True
    sources = [GLib.timeout_add_seconds(30, progress)]
    sources += [GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, sig, lambda: (window.destroy(), False)[1])
                for sig in (signal.SIGINT, signal.SIGTERM)]
    try:
        Gtk.main()
    finally:
        for source in sources:
            if GLib.MainContext.default().find_source_by_id(source):
                GLib.source_remove(source)
        window.destroy()
    return 0
