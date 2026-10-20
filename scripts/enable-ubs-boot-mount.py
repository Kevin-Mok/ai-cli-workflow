#!/usr/bin/env python3
"""Persist the already-mounted wallpaper disk without formatting or unmounting it."""

import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid


TARGET = '/mnt/linux-files-3'


def configure(contents, disk_uuid):
    entry = (f'UUID={disk_uuid} {TARGET} ext4 '
             'defaults,nofail,x-systemd.automount,x-systemd.device-timeout=5s 0 2')
    matches = []
    for line in contents.splitlines():
        fields = line.split('#', 1)[0].split()
        if len(fields) >= 2 and (fields[1] == TARGET or fields[0] == f'UUID={disk_uuid}'):
            matches.append(fields)
    if matches:
        if matches == [entry.split()]:
            return contents
        raise ValueError('Conflicting fstab entry; review it manually before continuing.')
    return contents.rstrip('\n') + '\n' + entry + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='Preview the required boot entry; no writes.')
    mode.add_argument('--apply', action='store_true', help='Back up and update /etc/fstab; requires sudo.')
    parser.add_argument('--plain', action='store_true', help='Use ASCII output.')
    args = parser.parse_args()

    def note(icon, message):
        print(message if args.plain else f'{icon} {message}', flush=True)

    try:
        fields = subprocess.check_output(
            ['findmnt', '-nro', 'UUID,FSTYPE', '--mountpoint', TARGET], text=True).split()
        if len(fields) != 2 or fields[1] != 'ext4':
            raise ValueError(f'{TARGET} must already contain the intended mounted ext4 disk.')
        disk_uuid = str(uuid.UUID(fields[0]))
        fstab = Path('/etc/fstab')
        original = fstab.read_text()
        updated = configure(original, disk_uuid)
        note('💾', f'Wallpaper disk: UUID={disk_uuid} at {TARGET}')
        if updated == original:
            note('✅', 'Boot mount is already configured.')
            return 0
        note('📝', updated.splitlines()[-1])
        if args.check:
            note('⚠️', 'Boot mount is missing. Run this script with sudo and --apply.')
            return 0
        if os.geteuid() != 0:
            raise ValueError('Apply requires sudo; run this script in a terminal with --apply.')
        backup = Path(f'/etc/fstab.ubs-{datetime.now():%Y%m%d-%H%M%S-%f}')
        with backup.open('x') as output:
            output.write(original)
        shutil.copystat(fstab, backup)
        note('📦', f'Backup: {backup}')
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', dir='/etc', prefix='.fstab-ubs-', delete=False) as output:
                temporary = Path(output.name)
                output.write(updated)
                output.flush()
                os.fsync(output.fileno())
            shutil.copystat(fstab, temporary)
            stat = fstab.stat()
            os.chown(temporary, stat.st_uid, stat.st_gid)
            if fstab.read_text() != original:
                raise ValueError('fstab changed during installation; no replacement made.')
            os.replace(temporary, fstab)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        note('🔄', 'Reloading systemd mount configuration…')
        subprocess.run(['systemctl', 'daemon-reload'], check=True, timeout=30)
        note('✅', 'Boot mount configured. Current mount preserved; verify wallpaper after reboot.')
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        note('❌', f'Boot mount setup stopped: {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
