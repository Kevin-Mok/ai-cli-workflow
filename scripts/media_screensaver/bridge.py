"""Private Chrome native-messaging state and the screensaver's fail-closed gate."""
from __future__ import annotations

import base64
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import stat
import struct
import sys
import tempfile
import time


MAX_MESSAGE = 131072
TTL = 4.0
HOST_NAME = "org.kevin.media_screensaver"
# The manifest's public key pins an unpacked extension's ID across installs.
PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuxCNancoTfvgQkwGDsu7e6ENIF70dVoRUqw/HgI0p1ylvRU92jLnrbufXa9L8h/RZ6bpnATrcR2Ht6N7QxqdfKkRF6FkgoYe4N3cFKQ4Crxj4uqkaHY5eCTmaPANshLhyNZMLFu4t2O16vdUzcpN2kbW8erRW4AS40eMQLvxTBKPfm7M9KtiBthBv+Hfj4fd1I8k3yq6iDSCcJ4/H9lR00q9LtnGc2C5Nwby1FLAM3wxPErNy0P79TLE2Q8VX2vBskBrHH3KHOsPyC/2jICu5B5pQaWH1gvOm5AFZkvRS8YnUgpjCJVKzqCPmoTTBVseFqSZ/UPEvGvtSR+Bss323QIDAQAB"
EXTENSION_ID = "".join(chr(ord("a") + int(n, 16)) for n in
                       hashlib.sha256(base64.b64decode(PUBLIC_KEY)).hexdigest()[:32])


def _private_directory(path: Path) -> Path:
    info = path.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) != 0o700):
        raise RuntimeError("browser bridge directory must be owned by this user with mode 0700")
    return path


def runtime_dir() -> Path:
    """Create an owned private runtime directory without following symlinks."""
    base = os.environ.get("XDG_RUNTIME_DIR")
    if base:
        parent = Path(base)
        if not parent.is_absolute():
            raise RuntimeError("XDG_RUNTIME_DIR must be an absolute private directory")
        _private_directory(parent)
        directory = parent / "media-screensaver"
    else:
        directory = Path("/tmp") / f"media-screensaver-{os.getuid()}"
    try:
        directory.mkdir(mode=0o700)
    except FileExistsError:
        pass
    return _private_directory(directory)


def _keys(value: object, expected: set[str]) -> dict:
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError("unexpected browser state fields")
    return value


def _number(value: object, limit: float = 1000000) -> float:
    if type(value) not in (int, float) or not math.isfinite(value) or abs(value) > limit:
        raise ValueError("invalid browser geometry")
    return value


def _rect(value: object) -> dict:
    rect = _keys(value, {"x", "y", "width", "height"})
    for key, number in rect.items():
        _number(number)
        if key in ("width", "height") and not 0 <= number <= 100000:
            raise ValueError("invalid browser dimensions")
    return rect


def _state(value: object) -> dict:
    data = _keys(value, {"version", "healthy", "windows"})
    if type(data["version"]) is not int or data["version"] != 1 or type(data["healthy"]) is not bool:
        raise ValueError("unsupported browser state")
    if not isinstance(data["windows"], list) or len(data["windows"]) > 64:
        raise ValueError("too many browser windows")
    seen = set()
    for window in data["windows"]:
        _keys(window, {"id", "state", "bounds", "videos"})
        identifier = window["id"]
        if type(identifier) is not int or not 0 <= identifier <= 2147483647 or identifier in seen:
            raise ValueError("invalid browser window identifier")
        seen.add(identifier)
        if window["state"] not in ("normal", "maximized", "fullscreen", "minimized"):
            raise ValueError("invalid browser window state")
        _rect(window["bounds"])
        if not isinstance(window["videos"], list) or len(window["videos"]) > 256:
            raise ValueError("too many browser videos")
        for video in window["videos"]:
            _keys(video, {"playing", "rect"})
            if type(video["playing"]) is not bool:
                raise ValueError("invalid playback state")
            _rect(video["rect"])
    return data


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate browser state field")
        value[key] = item
    return value


def _decode(raw: bytes) -> object:
    try:
        return json.loads(raw, object_pairs_hook=_unique_object)
    except RecursionError as error:
        raise ValueError("browser state nesting too deep") from error


def _intersects(a: dict, b: dict) -> bool:
    return (a["width"] > 0 and a["height"] > 0
            and a["x"] < b["x"] + b["width"] and b["x"] < a["x"] + a["width"]
            and a["y"] < b["y"] + b["height"] and b["y"] < a["y"] + a["height"])


def _read_clients(directory: Path, now: float | None) -> tuple[list[dict], str | None]:
    unavailable = "browser bridge unavailable; install/enable the extension and reconnect Chrome"
    try:
        _private_directory(Path(directory))
        current = time.time() if now is None else _number(now, 1e12)
        paths = sorted(path for path in Path(directory).iterdir()
                       if re.fullmatch(r"bridge-[0-9]+\.json", path.name))
        if not paths:
            return [], unavailable
        if len(paths) > 64:
            return [], "browser bridge has too many clients; reconnect Chrome"
    except (OSError, ValueError, RuntimeError):
        return [], unavailable
    windows = []
    problem = None
    for path in paths:
        try:
            descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC)
            with os.fdopen(descriptor, "rb") as stream:
                info = os.fstat(stream.fileno())
                if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                        or info.st_mode & 0o077 or info.st_size > MAX_MESSAGE):
                    raise ValueError("unsafe browser state file")
                raw = stream.read(MAX_MESSAGE + 1)
            if len(raw) > MAX_MESSAGE:
                raise ValueError("browser state too large")
            stored = _keys(_decode(raw), {"updated", "state"})
            stamp = _number(stored["updated"], 1e12)
            if not 0 <= current - stamp <= TTL:
                problem = "browser bridge state stale; reconnect Chrome (remove abandoned bridge state if necessary)"
                continue
            data = _state(stored["state"])
            if not data["healthy"]:
                problem = "browser bridge cannot inspect the active tab; reconnect or close unsupported browser tabs"
                continue
            windows.extend(data["windows"])
        except (OSError, ValueError, TypeError, OverflowError):
            problem = "browser bridge state invalid; reconnect Chrome"
    return windows, problem


def read_windows(directory: Path, now: float | None = None) -> list[dict]:
    """Return aggregate geometry, raising ValueError if any client is unavailable."""
    windows, problem = _read_clients(directory, now)
    if problem:
        raise ValueError(problem)
    return windows


def read_gate(directory: Path, middle: dict, now: float | None = None) -> tuple[bool, str]:
    """Allow idle start only with fresh, valid state from every connected host."""
    try:
        _rect(middle)
    except (ValueError, TypeError, OverflowError):
        return False, "display geometry unavailable; check the middle monitor"
    windows, problem = _read_clients(directory, now)
    if video_blocks(windows, middle):
        return False, "playing video on the middle display"
    return (False, problem) if problem else (True, "browser bridge ready; no playing video on the middle display")


def video_blocks(windows: list[dict], middle: dict) -> bool:
    return any(window["state"] != "minimized" and any(
        video["playing"] and _intersects(video["rect"], middle)
        for video in window["videos"]) for window in windows)


def _publish(directory: Path, path: Path, data: dict) -> None:
    encoded = json.dumps({"updated": time.time(), "state": data}, allow_nan=False,
                         separators=(",", ":")).encode()
    descriptor, name = tempfile.mkstemp(prefix=".bridge-", dir=directory)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def _read_exact(stream, count: int, clean_eof: bool = False) -> bytes | None:
    result = bytearray()
    while len(result) < count:
        chunk = stream.read(count - len(result))
        if not chunk:
            if clean_eof and not result:
                return None
            raise ValueError("truncated native message")
        result.extend(chunk)
    return bytes(result)


def native_main() -> int:
    """Speak Chrome's length-prefixed protocol; retain no state after disconnect."""
    path = None
    unhealthy = {"version": 1, "healthy": False, "windows": []}
    previous = signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        directory = runtime_dir()
        path = directory / f"bridge-{os.getpid()}.json"
        _publish(directory, path, unhealthy)
        while True:
            header = _read_exact(sys.stdin.buffer, 4, clean_eof=True)
            if header is None:
                return 0
            size = struct.unpack("=I", header)[0]
            if not 0 < size <= MAX_MESSAGE:
                raise ValueError("invalid native message size")
            raw = _read_exact(sys.stdin.buffer, size)
            try:
                data = _state(_decode(raw))
                ok = True
            except (ValueError, TypeError, OverflowError):
                data, ok = unhealthy, False
            _publish(directory, path, data)
            response = json.dumps({"ok": ok}, separators=(",", ":")).encode()
            sys.stdout.buffer.write(struct.pack("=I", len(response)) + response)
            sys.stdout.buffer.flush()
    except (OSError, ValueError, RuntimeError):
        print("⚠️ Browser bridge stopped; reconnect the extension.", file=sys.stderr)
        return 1
    finally:
        signal.signal(signal.SIGTERM, previous)
        if path is not None:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(native_main())
