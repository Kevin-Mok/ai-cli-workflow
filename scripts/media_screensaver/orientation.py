"""Private, validated additional rotations; media files are never written."""
import fcntl
import json
import os
from pathlib import Path
import tempfile


class OrientationStore:
    def __init__(self):
        self.path = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')) / 'media-screensaver/orientation.json'

    def read(self):
        try:
            fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW)
        except FileNotFoundError:
            return dict(version=1, files={})
        try:
            with os.fdopen(fd) as handle:
                data = json.load(handle)
            if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 1 or not isinstance(data.get('files'), dict):
                raise ValueError('Invalid orientation records')
            for path, record in data['files'].items():
                if not Path(path).is_absolute() or '\0' in path or not isinstance(record, dict):
                    raise ValueError('Invalid orientation record path')
                if (any(type(record.get(key)) is not int or record[key] < 0 for key in ('size', 'mtime_ns'))
                        or type(record.get('clockwise')) is not int or record['clockwise'] not in (0, 90, 180, 270)):
                    raise ValueError('Invalid orientation record values')
            return data
        except (ValueError, UnicodeError, RecursionError) as error:
            raise ValueError('Saved orientation data is invalid; repair or move orientation.json before saving. It has been left unchanged.') from error

    def load(self, path):
        record = self.read()['files'].get(str(path.absolute()))
        stat = path.stat()
        if record and (record['size'], record['mtime_ns']) == (stat.st_size, stat.st_mtime_ns):
            return record['clockwise']
        return 0

    def save(self, path, clockwise, expected=None):
        if type(clockwise) is not int or clockwise not in (0, 90, 180, 270):
            raise ValueError('Additional rotation must be 0, 90, 180 or 270 clockwise degrees.')
        directory = self.path.parent
        directory.mkdir(parents=True, mode=0o700, exist_ok=True)
        if directory.is_symlink() or directory.stat().st_uid != os.getuid():
            raise ValueError('Orientation directory must be a private directory owned by you.')
        directory.chmod(0o700)
        fd = os.open(directory / 'orientation.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            data = self.read()
            stat = path.stat()
            if expected is not None and expected != (stat.st_size, stat.st_mtime_ns):
                raise ValueError('Video changed during review; reopen it before saving.')
            key = str(path.absolute())
            if clockwise:
                data['files'][key] = dict(size=stat.st_size, mtime_ns=stat.st_mtime_ns, clockwise=clockwise)
            else:
                data['files'].pop(key, None)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(mode='w', dir=directory, prefix='.orientation-', delete=False) as handle:
                    temporary = Path(handle.name)
                    json.dump(data, handle, indent=2)
                    handle.write('\n')
                    handle.flush()
                    os.fsync(handle.fileno())
                temporary.replace(self.path)
            finally:
                if temporary:
                    temporary.unlink(missing_ok=True)
