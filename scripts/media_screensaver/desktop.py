"""X11 browser geometry and scoped display-awake control."""
from Xlib import X, display, error
from contextlib import contextmanager
import ctypes as C


@contextmanager
def keep_awake():
    """Suspend automatic X11 blanking/DPMS for this connection's lifetime."""
    x = C.CDLL('libX11.so.6')
    saver = C.CDLL('libXss.so.1')
    x.XOpenDisplay.argtypes = [C.c_char_p]
    x.XOpenDisplay.restype = C.c_void_p
    x.XCloseDisplay.argtypes = [C.c_void_p]
    x.XSync.argtypes = [C.c_void_p, C.c_int]
    x.XForceScreenSaver.argtypes = [C.c_void_p, C.c_int]
    saver.XScreenSaverQueryExtension.argtypes = [C.c_void_p, C.POINTER(C.c_int), C.POINTER(C.c_int)]
    saver.XScreenSaverQueryVersion.argtypes = [C.c_void_p, C.POINTER(C.c_int), C.POINTER(C.c_int)]
    saver.XScreenSaverSuspend.argtypes = [C.c_void_p, C.c_int]
    saver.XScreenSaverSuspend.restype = None
    connection = x.XOpenDisplay(None)
    if not connection:
        raise ValueError('Cannot keep displays awake; run from the X11 desktop session.')
    try:
        event, error, major, minor = (C.c_int() for _ in range(4))
        if (not saver.XScreenSaverQueryExtension(connection, C.byref(event), C.byref(error))
                or not saver.XScreenSaverQueryVersion(connection, C.byref(major), C.byref(minor))
                or (major.value, minor.value) < (1, 1)):
            raise ValueError('XScreenSaver 1.1 is required to keep scheduled playback visible.')
        saver.XScreenSaverSuspend(connection, True)
        # Suspension prevents future blanking but does not clear an existing blank.
        x.XForceScreenSaver(connection, 0)
        x.XSync(connection, False)
        try:
            yield
        finally:
            saver.XScreenSaverSuspend(connection, False)
            x.XSync(connection, False)
    finally:
        x.XCloseDisplay(connection)


def match_windows(native, reported):
    """Match the complete inventory; return only cards on mapped native windows."""
    if len(native) != len(reported):
        return None
    candidates = list(reported)
    displayed = []
    for actual in sorted(native, key=lambda w: not w.get('visible', True)):
        for index, window in enumerate(candidates):
            bounds = window['bounds']
            if window['state'] == 'minimized':
                matches = not actual.get('visible', True)
            else:
                # i3 decorations and Chrome disagree slightly about outer-frame bounds.
                matches = all(abs(actual[key] - bounds[key]) <= limit for key, limit in
                              (('x', 16), ('y', 48), ('width', 32), ('height', 64)))
            if matches:
                candidates.pop(index)
                if actual.get('visible', True) and window['state'] != 'minimized':
                    displayed.append(window)
                break
        else:
            return None
    return displayed


def browser_windows():
    connection = display.Display()
    try:
        root = connection.screen().root
        clients = root.get_full_property(connection.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType)
        if clients is None:
            raise ValueError('Native browser-window inventory unavailable; run under an EWMH X11 window manager.')
        result = []
        for identifier in clients.value:
            window = connection.create_resource_object('window', int(identifier))
            try:
                classes = [value.lower() for value in (window.get_wm_class() or ())]
                if not any(value in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser') for value in classes):
                    continue
                geometry = window.get_geometry()
                origin = root.translate_coords(window, 0, 0)
                result.append(dict(x=origin.x, y=origin.y, width=geometry.width, height=geometry.height,
                                   visible=window.get_attributes().map_state == X.IsViewable))
            except error.BadWindow:
                # A closing window needs no bridge; new windows are checked at the next poll.
                continue
        return result
    finally:
        connection.close()
