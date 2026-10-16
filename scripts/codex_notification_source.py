"""Optional, verified source outlines for the duration of notification playback."""
from contextlib import contextmanager
import importlib
import os
from pathlib import Path
import re
import select
import subprocess
import threading
from typing import Iterator, Protocol


class _Outline(Protocol):
    def close(self) -> None: ...


def _process(pid: int) -> tuple[int, int] | None:
    if pid <= 0:
        return None
    try:
        fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
        return int(fields[1]), int(fields[19])
    except (OSError, ValueError, IndexError):
        return None


def _ancestry() -> list[dict[str, int]]:
    chain: list[dict[str, int]] = []
    observed: list[tuple[int, tuple[int, int]]] = []
    pid = os.getpid()
    while pid > 1 and len(chain) < 128:
        process = _process(pid)
        if process is None or any(item['pid'] == pid for item in chain):
            break
        parent, start = process
        chain.append({'pid': pid, 'start': start})
        observed.append((pid, process))
        pid = parent
    return chain if all(_process(pid) == process for pid, process in observed) else []


def _identity(value: object) -> dict[str, int] | None:
    if not isinstance(value, dict):
        return None
    pid, start = value.get('pid'), value.get('start')
    if type(pid) is not int or type(start) is not int or pid <= 0 or start <= 0:
        return None
    process = _process(pid)
    return {'pid': pid, 'start': start} if process is not None and process[1] == start else None


def _tmux(socket: str, *args: str) -> str:
    return subprocess.run(['tmux', '-S', socket, *args], check=True, capture_output=True,
                          text=True, timeout=1).stdout.removesuffix('\n')


def _tmux_location(socket: str, pane: str) -> tuple[int, int, str, str]:
    result = _tmux(socket, 'display-message', '-p', '-t', pane,
                   '#{pid}\t#{pane_pid}\t#{pane_id}\t#{window_id}').split('\t')
    if len(result) != 4 or result[2] != pane or not re.fullmatch(r'@\d+', result[3]):
        raise ValueError('unverified tmux pane')
    return int(result[0]), int(result[1]), result[2], result[3]


def _capture_tmux(chain: list[dict[str, int]]) -> dict[str, object] | None:
    socket, server_text, _ = os.environ['TMUX'].rsplit(',', 2)
    pane = os.environ.get('TMUX_PANE', '')
    if not os.path.isabs(socket) or not re.fullmatch(r'%\d+', pane):
        return None
    server_pid, pane_pid, _, window = _tmux_location(socket, pane)
    if server_pid != int(server_text):
        return None
    owner = next((item for item in chain if item['pid'] == pane_pid), None)
    server = _process(server_pid)
    if owner is None or _identity(owner) is None or server is None:
        return None
    return {'kind': 'tmux', 'socket': socket, 'pane': pane, 'window': window,
            'owner': owner, 'server': {'pid': server_pid, 'start': server[1]}}


def _x11_display(name: str):
    # System python3-xlib is optional; importing this module must not require it.
    display = importlib.import_module('Xlib.display').Display(name)
    display.set_error_handler(lambda *args: None)
    return display


def _owned_windows(display, chain: list[dict[str, int]]) -> list[tuple[int, dict[str, int]]]:
    root = display.screen().root
    clients = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), 33)
    if clients is None:
        return []
    owners = {item['pid']: item for item in chain}
    matches = []
    for window_id in clients.value:
        window = display.create_resource_object('window', int(window_id))
        try:
            classes = window.get_wm_class() or ()
            if not any(str(value).lower() == 'kitty' for value in classes):
                continue
            property_ = window.get_full_property(display.intern_atom('_NET_WM_PID'), 6)
            if property_ is not None and len(property_.value) == 1:
                owner = owners.get(int(property_.value[0]))
                if owner is not None:
                    matches.append((int(window_id), owner))
        except Exception:
            continue  # One closing client must not hide a different verified source.
    return matches


def _capture_x11(chain: list[dict[str, int]]) -> dict[str, object] | None:
    name = os.environ.get('DISPLAY', '')
    if not name:
        return None
    display = _x11_display(name)
    try:
        matches = _owned_windows(display, chain)
        if len(matches) == 1:
            window, owner = matches[0]
            return {'kind': 'x11', 'display': name, 'window': window, 'owner': owner}
        return None
    finally:
        display.close()


def capture_source() -> dict[str, object] | None:
    """Capture before detachment; environment hints alone never identify a source."""
    try:
        chain = _ancestry()
        if os.environ.get('TMUX'):
            return _capture_tmux(chain)
        return _capture_x11(chain)
    except Exception:
        return None


def _ring_rectangles(width: int, height: int) -> list[tuple[int, int, int, int]]:
    thickness = min(2, width, height)
    if width <= 4 or height <= 4:
        return [(0, 0, max(1, width), max(1, height))]
    return [(0, 0, width, thickness), (0, height - thickness, width, thickness),
            (0, thickness, thickness, height - 2 * thickness),
            (width - thickness, thickness, thickness, height - 2 * thickness)]


class _X11Outline:
    def __init__(self, source: dict[str, object], owner: dict[str, int]):
        self.display = _x11_display(str(source['display']))
        self.child = None
        self.reader = self.writer = -1
        try:
            matches = _owned_windows(self.display, [owner])
            if matches != [(source['window'], owner)] or _identity(owner) is None:
                raise ValueError('source window changed')
            self.constants = importlib.import_module('Xlib.X')
            self.shape = importlib.import_module('Xlib.ext.shape')
            if not self.display.has_extension('SHAPE'):
                raise ValueError('SHAPE unavailable')
            version = self.display.shape_query_version()
            if (version.major_version, version.minor_version) < (1, 1):
                raise ValueError('input shaping unavailable')
            parent = self.display.create_resource_object('window', source['window'])
            geometry = parent.get_geometry()
            color = self.display.screen().default_colormap.alloc_color(0x8F8F, 0xBCBC, 0x8F8F).pixel
            parent.change_attributes(event_mask=self.constants.StructureNotifyMask)
            self.child = parent.create_window(0, 0, geometry.width, geometry.height, 0,
                                              self.constants.CopyFromParent,
                                              background_pixel=color, override_redirect=1)
            self._input_shape()
            self._resize(geometry.width, geometry.height)
            self.child.map()
            self.display.sync()
            self.reader, self.writer = os.pipe()
            self.thread = threading.Thread(target=self._events, daemon=True)
            self.thread.start()
        except BaseException:
            self._destroy()
            raise

    def _input_shape(self) -> None:
        if self.child is None:
            return
        if hasattr(self.shape, 'SO'):
            self.child.shape_rectangles(0, 2, self.constants.Unsorted, 0, 0, [])
            return
        # Legacy Xlib rejects Input (2); SHAPE 1.1 accepts this empty region.
        rq = importlib.import_module('Xlib.protocol.rq')
        class InputShape(rq.Request):
            _request = rq.Struct(
                rq.Card8('opcode'), rq.Opcode(1), rq.RequestLength(),
                rq.Card8('operation'), rq.Card8('kind'), rq.Card8('ordering'),
                rq.Pad(1), rq.Window('window'), rq.Int16('x'), rq.Int16('y'))
        InputShape(display=self.child.display,
                   opcode=self.child.display.get_extension_major('SHAPE'),
                   operation=0, kind=2, ordering=0, window=self.child.id, x=0, y=0)

    def _resize(self, width: int, height: int) -> None:
        if self.child is None:
            return
        self.child.configure(x=0, y=0, width=width, height=height,
                             stack_mode=self.constants.Above)
        self.child.shape_rectangles(0, 0, self.constants.Unsorted, 0, 0,
                                    _ring_rectangles(width, height))
        self.display.flush()

    def _events(self) -> None:
        try:
            while True:
                while self.display.pending_events():
                    event = self.display.next_event()
                    if event.type == self.constants.DestroyNotify:
                        return
                    if event.type == self.constants.ConfigureNotify:
                        self._resize(event.width, event.height)
                readable, _, _ = select.select([self.display.fileno(), self.reader], [], [])
                if self.reader in readable:
                    break
        except Exception:
            pass
        finally:
            self._destroy()

    def _destroy(self) -> None:
        try:
            if self.child is not None:
                self.child.destroy()
                self.display.sync()
        except Exception:
            pass
        finally:
            try:
                self.display.close()
            except Exception:
                pass
            for descriptor in (self.reader, self.writer):
                if descriptor >= 0:
                    try:
                        os.close(descriptor)
                    except OSError:
                        pass
            self.reader = self.writer = -1

    def close(self) -> None:
        try:
            if self.writer >= 0:
                os.write(self.writer, b'x')
        except OSError:
            pass
        self.thread.join(timeout=2)


class _TmuxOutline:
    def __init__(self, source: dict[str, object], owner: dict[str, int]):
        socket, pane, window = source['socket'], source['pane'], source['window']
        server = _identity(source.get('server'))
        if not all(isinstance(item, str) for item in (socket, pane, window)) or server is None:
            raise ValueError('invalid tmux identity')
        self.socket, self.window = str(socket), str(window)
        self.server = server
        server_pid, pane_pid, _, current_window = _tmux_location(self.socket, str(pane))
        if server_pid != server['pid'] or pane_pid != owner['pid'] or current_window != window:
            raise ValueError('tmux identity changed')
        if _identity(owner) is None:
            raise ValueError('pane process changed')
        self.styles: list[tuple[str, str | None, str]] = []
        try:
            for name in ('pane-border-style', 'pane-active-border-style'):
                original = self._local(name)
                effective = _tmux(self.socket, 'show-options', '-w', '-A', '-v', '-t', self.window, name)
                temporary = effective + f',#{{?#{{==:#{{pane_id}},{pane}}},fg=#8FBC8F,}}'
                self.styles.append((name, original, temporary))
                _tmux(self.socket, 'set-option', '-w', '-t', self.window, name, temporary)
        except BaseException:
            self.close()
            raise

    def _local(self, name: str) -> str | None:
        listed = _tmux(self.socket, 'show-options', '-w', '-t', self.window, name)
        if not listed:
            return None
        return _tmux(self.socket, 'show-options', '-w', '-v', '-t', self.window, name)

    def close(self) -> None:
        for name, original, temporary in reversed(self.styles):
            try:
                if _identity(self.server) is None or self._local(name) != temporary:
                    continue  # Preserve a concurrent user's style edit.
                if original is None:
                    _tmux(self.socket, 'set-option', '-w', '-u', '-t', self.window, name)
                else:
                    _tmux(self.socket, 'set-option', '-w', '-t', self.window, name, original)
            except Exception:
                pass


def _open_outline(source: object) -> _Outline | None:
    if not isinstance(source, dict):
        return None
    owner = _identity(source.get('owner'))
    if owner is None:
        return None
    if source.get('kind') == 'x11' and isinstance(source.get('display'), str) and type(source.get('window')) is int and source['window'] > 0:
        return _X11Outline(source, owner)
    if source.get('kind') == 'tmux':
        return _TmuxOutline(source, owner)
    return None


@contextmanager
def outline(source: object) -> Iterator[None]:
    """Yield even when visual support fails; always preserve the player's error."""
    active = None
    try:
        active = _open_outline(source)
    except Exception:
        pass
    try:
        yield
    finally:
        if active is not None:
            try:
                active.close()
            except Exception:
                pass
