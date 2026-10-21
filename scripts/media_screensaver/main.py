"""CLI, installation and idle supervision for the media conveyor."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

from . import bridge
from .core import discover, parse_monitors, VIDEOS

MEDIA = Path('/mnt/linux-files-3/hevin')
IDLE_SECONDS = 300
GLYPHS = dict(progress='🔄', success='✅', warning='⚠️', error='❌', info='🖥️')


def output(args, kind, message, details=None):
    prefix = GLYPHS[kind] + ' ' if not args.plain else ''
    print(prefix + message, file=sys.stderr, flush=True)
    if args.details and details:
        print(details, file=sys.stderr, flush=True)


def monitors():
    p = subprocess.run(['xrandr', '--listmonitors'], capture_output=True, text=True, timeout=5)
    if p.returncode:
        raise ValueError('Cannot read X11 monitors; launch from the desktop session.')
    return parse_monitors(p.stdout)


def scan(args):
    count = [0]
    done = threading.Event()
    def progress():
        start = time.monotonic()
        while not done.wait(2):
            output(args, 'progress', f'Discovering media · {count[0]} candidates · {int(time.monotonic()-start)}s')
    thread = threading.Thread(target=progress, daemon=True)
    output(args, 'progress', 'Discovering supported media…' if not args.plain else 'Discovering supported media...')
    thread.start()
    try:
        result = discover(args.media, lambda total: count.__setitem__(0, total))
    finally:
        done.set()
        thread.join()
    output(args, 'success', f'Found {len(result)} media items; originals remain read-only.')
    return result


def gate(directory, middle):
    rectangle = {key: middle[key] for key in ('x', 'y', 'width', 'height')}
    try:
        windows = bridge.read_windows(directory)
    except ValueError:
        return bridge.read_gate(directory, rectangle)
    from .desktop import browser_windows, match_windows
    try:
        displayed = match_windows(browser_windows(), windows)
    except Exception:
        displayed = None
    if displayed is None:
        return False, 'Browser bridge unavailable for a Chrome window; enable the extension in every profile.'
    if bridge.video_blocks(displayed, rectangle):
        return False, 'playing video on the middle display'
    return True, 'browser bridge ready; no playing video on the middle display'


def preview(args, automatic=False):
    try:
        directory = bridge.runtime_dir()
    except (OSError, RuntimeError):
        if automatic:
            raise ValueError('Browser bridge unavailable; automatic preview suppressed.')
        return _preview(args, automatic=False)
    with (directory / 'preview.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            output(args, 'info', 'Screensaver playback is already running; duplicate launch skipped.')
            return 0
        return _preview(args, automatic=automatic)


def _preview(args, automatic=False):
    paths = scan(args)
    geometry = monitors()
    from .renderer import run
    try:
        directory = bridge.runtime_dir()
        playback_gate = lambda: gate(directory, geometry[1])
    except (OSError, RuntimeError) as error:
        if automatic:
            raise ValueError('Browser bridge unavailable; automatic preview suppressed.') from error
        output(args, 'warning', 'Browser bridge unavailable; manual preview remains available.', str(error))
        playback_gate = lambda: (False, 'browser bridge unavailable')
    reporter = None
    handle = None
    if args.report:
        fd = os.open(args.report, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        handle = os.fdopen(fd, 'w')
        def reporter(value):
            handle.write(json.dumps(value) + '\n')
            handle.flush()
    try:
        return run(paths, geometry, seconds=args.seconds,
                   gate=playback_gate, automatic=automatic,
                   emit=lambda kind, msg, details=None: output(args, kind, msg, details), report=reporter)
    finally:
        if handle:
            handle.close()


def locked():
    # Do not take grabs, inhibit DPMS or reset idle; existing lockers retain ownership.
    session = os.environ.get('XDG_SESSION_ID')
    if session and shutil.which('loginctl'):
        result = subprocess.run(['loginctl', 'show-session', session, '-p', 'LockedHint', '--value'],
                                capture_output=True, text=True, timeout=3)
        if result.returncode != 0:
            return True
        if result.stdout.strip() == 'yes':
            return True
    for proc in Path('/proc').iterdir():
        if proc.name.isdigit():
            try:
                if proc.stat().st_uid == os.getuid() and (proc / 'comm').read_text().strip() in ('i3lock', 'xsecurelock', 'slock', 'xscreensaver'):
                    return True
            except (FileNotFoundError, PermissionError, ProcessLookupError):
                pass
    return False


def daemon(args):
    from .renderer import IdleClock
    directory = bridge.runtime_dir()
    with (directory / 'daemon.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            output(args, 'info', 'Idle monitor is already running.')
            return 0
        lock.seek(0)
        lock.truncate()
        lock.write(str(os.getpid()))
        lock.flush()
        clock = IdleClock()
        stop = threading.Event()
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda *_: stop.set())
        child = None
        last_message = ''
        last_progress = 0
        retry_after = 0
        output(args, 'info', 'Idle monitor running; activation after 5 minutes of keyboard/mouse inactivity.')
        try:
            while not stop.is_set():
                now = time.monotonic()
                geometry = monitors()
                middle = geometry[1]
                if middle['width'] < 3840 or middle['height'] < 2160:
                    allowed, reason = False, 'Automatic activation needs the middle 4K output; inspect the display layout.'
                else:
                    allowed, reason = gate(directory, middle)
                is_locked = locked()
                if is_locked:
                    allowed, reason = False, 'Session is locked or lock state is unavailable.'
                if child and child.poll() is not None:
                    if child.returncode:
                        retry_after = now + 60
                        output(args, 'warning', 'Preview stopped with an error; retrying after 60s. Run preview or probe for details.')
                    child = None
                if child and not allowed:
                    child.terminate()
                idle = clock.seconds()
                if not child and allowed and idle >= IDLE_SECONDS and now >= retry_after:
                    command = [sys.executable, str(Path(__file__).resolve().parents[1] / ('media-screensaver' if (Path(__file__).resolve().parents[1] / 'media-screensaver').exists() else 'executable_media-screensaver')), '_auto', '--media', str(args.media)]
                    if args.plain: command.append('--plain')
                    if args.details: command.append('--details')
                    child = subprocess.Popen(command, stdin=subprocess.DEVNULL, start_new_session=True)
                message = 'Automatic activation ready' if allowed else 'Automatic activation suppressed: ' + reason
                if message != last_message or now - last_progress >= 30:
                    output(args, 'info', message + f' · idle {int(idle)}s')
                    last_message, last_progress = message, now
                status = dict(pid=os.getpid(), updated=time.time(), automatic_allowed=allowed, reason=reason,
                              idle_seconds=int(idle), preview_pid=child.pid if child else None)
                temporary = directory / 'status.tmp'
                temporary.write_text(json.dumps(status))
                temporary.chmod(0o600)
                temporary.replace(directory / 'status.json')
                stop.wait(.5)
        finally:
            if child and child.poll() is None:
                child.terminate()
                try: child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
            clock.close()
            (directory / 'status.json').unlink(missing_ok=True)
            output(args, 'success', 'Idle monitor stopped; owned preview released.')
    return 0


def service(args):
    if not os.environ.get('DISPLAY'):
        raise ValueError('Start the service from the X11 desktop session (DISPLAY is missing).')
    output(args, 'progress', 'Starting supervised five-minute idle monitor...')
    for command in (
        ['daemon-reload'],
        ['import-environment'] + [key for key in ('DISPLAY', 'XAUTHORITY', 'XDG_SESSION_ID') if key in os.environ],
        ['start', 'media-screensaver.service'],
    ):
        result = subprocess.run(['systemctl', '--user'] + command, capture_output=True, text=True, timeout=30)
        if result.returncode:
            output(args, 'error', 'User service could not start; run install first and inspect systemctl --user status media-screensaver.service.', result.stderr)
            return 1
    output(args, 'success', 'Idle service started; automatic activation after five idle minutes when browser and lock checks allow.')
    return 0


def install(args):
    home = Path.home()
    target = home / 'scripts'
    target.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent
    package = target / 'media_screensaver'
    package.mkdir(exist_ok=True)
    for path in source.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts or path.suffix == '.pyc': continue
        dest = package / path.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if path.resolve() != dest.resolve(): shutil.copy2(path, dest)
    launcher = source.parent / 'executable_media-screensaver'
    if not launcher.exists(): launcher = source.parent / 'media-screensaver'
    installed = target / 'media-screensaver'
    if launcher.resolve() != installed.resolve(): shutil.copy2(launcher, installed)
    installed.chmod(0o755)
    native = target / 'media-screensaver-native'
    native.write_text('#!/usr/bin/env python3\nimport sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent))\nfrom media_screensaver.bridge import native_main\nraise SystemExit(native_main())\n')
    native.chmod(0o755)
    config = Path(os.environ.get('XDG_CONFIG_HOME', home / '.config'))
    for browser in ('google-chrome', 'chromium'):
        manifest = config / browser / 'NativeMessagingHosts' / (bridge.HOST_NAME + '.json')
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(dict(name=bridge.HOST_NAME, description='Local playback geometry for the media screensaver',
                                           path=str(native), type='stdio', allowed_origins=['chrome-extension://' + bridge.EXTENSION_ID + '/']), indent=2) + '\n')
    unit = config / 'systemd/user/media-screensaver.service'
    unit.parent.mkdir(parents=True, exist_ok=True)
    unit.write_text((source / 'media-screensaver.service').read_text())
    i3 = config / 'i3/config'
    if i3.is_file():
        startup = f'exec --no-startup-id {installed} service'
        legacy = f'exec --no-startup-id {installed} daemon'
        current = ''.join(line for line in i3.read_text().splitlines(keepends=True) if line.strip() != legacy)
        if startup not in current.splitlines():
            current += ('' if current.endswith('\n') else '\n') + startup + '\n'
        i3.write_text(current)
        output(args, 'info', 'Registered idle service for the next i3 session; existing settings preserved.')
    output(args, 'success', f'Installed launcher: {installed}')
    output(args, 'info', f'Start now from the desktop: {installed} service')
    output(args, 'info', f'Load unpacked browser extension: {package / "browser"}')
    output(args, 'info', f'Expected extension ID: {bridge.EXTENSION_ID}')
    output(args, 'info', 'Enable the extension in every Chrome/Chromium profile; allow incognito if used. See docs/media-screensaver.md.')
    return 0


def probe(args):
    from .renderer import Gst, load_photo
    paths = scan(args)
    passed = 0
    formats = {}
    for index, path in enumerate(paths):
        suffix = path.suffix.lower()
        ok = False
        detail = None
        if suffix in VIDEOS:
            pipeline = Gst.ElementFactory.make('playbin')
            try:
                pipeline.set_property('uri', path.as_uri())
                pipeline.set_property('flags', 1)
                pipeline.set_property('video-sink', Gst.ElementFactory.make('fakesink'))
                pipeline.set_property('audio-sink', Gst.ElementFactory.make('fakesink'))
                pipeline.set_state(Gst.State.PAUSED)
                state, current, _ = pipeline.get_state(10 * Gst.SECOND)
                ok = state == Gst.StateChangeReturn.SUCCESS and current == Gst.State.PAUSED
            finally:
                pipeline.set_state(Gst.State.NULL)
                pipeline.get_state(Gst.SECOND)
        else:
            try:
                if suffix == '.heic':
                    with tempfile.TemporaryDirectory(prefix='media-screensaver-probe-') as d:
                        dest = Path(d) / 'frame.png'
                        p = subprocess.run(['convert', str(path) + '[0]', '-auto-orient', '-resize', '3840x2160>', str(dest)],
                                           stdin=subprocess.DEVNULL, capture_output=True, timeout=15)
                        if p.returncode: raise ValueError('HEIC conversion failed')
                        load_photo(dest)
                else:
                    load_photo(path)
                ok = True
            except Exception as error:
                detail = str(error)
        passed += int(ok)
        formats.setdefault(suffix, [0, 0])[0 if ok else 1] += 1
        output(args, 'progress' if ok else 'warning', f'Decode {index+1}/{len(paths)} · {suffix} · ' + ('passed' if ok else 'skipped'), detail)
    for suffix, (good, bad) in sorted(formats.items()):
        output(args, 'info', f'{suffix}: {good} decoded, {bad} skipped')
    output(args, 'success' if passed else 'error', f'Decoding complete: {passed} decoded, {len(paths)-passed} skipped; originals unchanged.')
    return 0 if passed else 1


def main(argv=None):
    plain_help = '--plain' in (sys.argv[1:] if argv is None else argv) or os.environ.get('CLI_PLAIN') == '1'
    parser = argparse.ArgumentParser(description=('' if plain_help else '🖥️ ') + 'X11 three-monitor media conveyor; see docs/media-screensaver.md.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', nargs='?', choices=['preview', 'daemon', 'service', 'status', 'install', 'probe', 'demo', 'orient', 'scheduled', '_auto'], default='preview', metavar='{preview,daemon,service,status,install,probe,demo,orient,scheduled}')
    parser.add_argument('--media', type=Path, default=MEDIA, help='recursive media library (default: %(default)s)')
    parser.add_argument('--file', type=Path, help='video for orient (otherwise opens a chooser in --media)')
    parser.add_argument('--seconds', type=float, default=0, help='close preview after this many seconds (0: until activity)')
    parser.add_argument('--report', type=Path, help='new private JSONL timing report; item IDs only')
    parser.add_argument('--plain', action='store_true', default=os.environ.get('CLI_PLAIN') == '1', help='ASCII output')
    parser.add_argument('--details', action='store_true', help='show raw decoder diagnostics')
    args = parser.parse_args(argv)
    if args.seconds < 0 or not __import__('math').isfinite(args.seconds): parser.error('--seconds must be finite and nonnegative')
    try:
        if args.command == 'orient':
            from .review import run
            return run(args, lambda kind, message: output(args, kind, message))
        if args.command == 'scheduled':
            if locked():
                output(args, 'info', 'Daily screensaver skipped: session is locked or lock state is unavailable.')
                return 0
            return preview(args, automatic=True) or 0
        if args.command == 'install': return install(args)
        if args.command == 'probe': return probe(args)
        if args.command == 'daemon': return daemon(args)
        if args.command == 'service': return service(args)
        if args.command == 'demo':
            from .fixtures import demo
            return demo(args)
        if args.command == 'status':
            directory = bridge.runtime_dir()
            geometry = monitors()
            allowed, reason = gate(directory, geometry[1])
            output(args, 'info', 'Monitors: ' + ' → '.join(m['name'] for m in geometry) if not args.plain else 'Monitors: ' + ' -> '.join(m['name'] for m in geometry))
            output(args, 'info', ('Automatic activation ready: ' if allowed else 'Automatic activation suppressed: ') + reason)
            status = directory / 'status.json'
            running = status.exists() and time.time() - status.stat().st_mtime < 3
            output(args, 'info', 'Idle monitor: ' + ('running' if running else 'stopped; launch media-screensaver service'))
            return 0
        return preview(args, automatic=args.command == '_auto') or 0
    except KeyboardInterrupt:
        output(args, 'info', 'Stopped.')
        return 130
    except Exception as error:
        output(args, 'error', str(error))
        if args.details:
            import traceback
            traceback.print_exc()
        return 1
