#!/usr/bin/env python3
"""Mount the existing 8 TB disk on power-on and on access; never format or unmount it."""

import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


UUID = 'e2f4a51f-954a-4168-a1af-2c9645d3f00a'
TARGET = '/mnt/usb-8tb'
UNIT = r'mnt-usb\x2d8tb'
OPTIONS = 'defaults,nofail,x-systemd.automount,x-systemd.device-timeout=5s,x-systemd.device-bound=yes'
ENTRY = f'UUID={UUID} {TARGET} ext4 {OPTIONS} 0 2'
UDEV_UNIT = UNIT.replace('\\', '\\\\')
RULE = (f'ACTION=="add", SUBSYSTEM=="block", ENV{{ID_FS_UUID}}=="{UUID}", '
        f'TAG+="systemd", ENV{{SYSTEMD_WANTS}}+="{UDEV_UNIT}.mount"\n')
RULE_PATH = Path('/etc/udev/rules.d/99-usb-8tb-automount.rules')


def configure(contents):
    lines = contents.splitlines(keepends=True)
    matches = []
    for index, line in enumerate(lines):
        fields = line.split('#', 1)[0].split()
        if len(fields) >= 2 and (fields[1] == TARGET or fields[0] in
                                (f'UUID={UUID}', f'/dev/disk/by-uuid/{UUID}')):
            matches.append((index, fields))
    if len(matches) != 1:
        raise ValueError('Expected exactly one existing UUID entry for the 8 TB disk in fstab.')
    index, fields = matches[0]
    old = f'UUID={UUID} {TARGET} ext4 defaults,nofail 0 2'.split()
    if fields not in (old, ENTRY.split()):
        raise ValueError('Conflicting fstab options, disk, or mountpoint; review manually.')
    if fields == ENTRY.split():
        return contents
    comment = ' #' + lines[index].split('#', 1)[1].rstrip('\n') if '#' in lines[index] else ''
    lines[index] = ENTRY + comment + '\n'
    return ''.join(lines)


def replace_file(path, contents):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, prefix='.usb-8tb-', delete=False) as output:
            temporary = Path(output.name)
            output.write(contents)
            output.flush()
            os.fsync(output.fileno())
        if path.exists():
            shutil.copystat(path, temporary)
            stat = path.stat()
            os.chown(temporary, stat.st_uid, stat.st_gid)
        else:
            temporary.chmod(0o644)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def activate(note):
    try:
        mounted = subprocess.check_output(
            ['findmnt', '-nro', 'FSTYPE,UUID', '--mountpoint', TARGET], text=True).split()
    except subprocess.CalledProcessError as error:
        if error.returncode != 1:
            raise
        mounted = []
    if mounted and mounted[0] != 'autofs':
        if mounted != ['ext4', UUID]:
            raise ValueError('Unexpected filesystem at the mountpoint; current mount preserved.')
        note('💾', 'Current mount preserved; on-access fallback activates on next boot.')
    else:
        note('⏳', 'Starting the on-access mount (up to 30 seconds)…')
        subprocess.run(['systemctl', 'start', f'{UNIT}.automount'], check=True, timeout=30)
    if Path(f'/dev/disk/by-uuid/{UUID}').exists():
        note('⏳', 'Mounting the connected disk (up to 30 seconds)…')
        subprocess.run(['systemctl', 'start', f'{UNIT}.mount'], check=True, timeout=30)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='Preview configuration without writing.')
    mode.add_argument('--apply', action='store_true', help='Install and activate; requires sudo.')
    parser.add_argument('--plain', action='store_true', help='Use ASCII output.')
    args = parser.parse_args()

    def note(icon, message):
        print(message if args.plain else f'{icon} {message}', flush=True)

    try:
        fstab = Path('/etc/fstab')
        if fstab.is_symlink() or RULE_PATH.is_symlink():
            raise ValueError('Refusing symlinked system configuration; review manually.')
        original = fstab.read_text()
        updated = configure(original)
        rule_before = RULE_PATH.read_text() if RULE_PATH.exists() else None
        if rule_before not in (None, RULE):
            raise ValueError(f'Conflicting rule at {RULE_PATH}; review manually.')
        note('💾', ENTRY)
        note('🔌', RULE.rstrip())
        ready = updated == original and rule_before == RULE
        if args.check:
            note('✅' if ready else '⚠️', 'Configuration installed; runtime not checked.' if ready else
                 'Installation pending. Run with sudo and --apply.')
            return 0
        if os.geteuid() != 0:
            raise ValueError('Administrator authentication required: run with sudo and --apply.')
        if updated != original:
            backup = Path(f'/etc/fstab.usb-8tb-{datetime.now():%Y%m%d-%H%M%S-%f}')
            with backup.open('x') as output:
                output.write(original)
            shutil.copystat(fstab, backup)
            note('📦', f'fstab backup: {backup}')
            if fstab.read_text() != original:
                raise ValueError('fstab changed during installation; rerun after review.')
            replace_file(fstab, updated)
        if rule_before is None:
            replace_file(RULE_PATH, RULE)
        note('🔄', 'Reloading systemd and udev configuration…')
        subprocess.run(['systemctl', 'daemon-reload'], check=True, timeout=30)
        subprocess.run(['udevadm', 'control', '--reload-rules'], check=True, timeout=30)
        activate(note)
        note('✅', 'Automatic mounting installed. Safely unmount before switching the disk off.')
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        note('❌', f'Setup stopped: {error}. Configuration may be partially installed; review and rerun.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
