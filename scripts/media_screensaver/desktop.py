"""Reconcile all native Chrome windows and gate video on mapped windows only."""
from Xlib import X, display, error


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
