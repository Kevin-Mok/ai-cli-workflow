# UBS wallpaper missing at i3 login

Trace the startup-only failure, reproduce it without an interactive terminal, and fix the earliest failing boundary while preserving manual startup.

- Symptom: wallpaper absent at login; manually running `ubs` restores it.
- Impact: existing autostart hook does not establish successful desktop initialization. Prior response incorrectly inferred success from the hook and running processes.
- Evidence: user report; startup script performs `sudo mount` before wallpaper, then invokes a wallpaper helper that needs `wal` on PATH.
- Lookup: `ubuntu-start wallpaper sudo mount` returned related interactive-sudo guidance, but no direct established remedy for this script.
- Cause: the wallpaper symlink resolves to `/mnt/linux-files-3/Pictures/Backgrounds/4k/sukana.jpg`; the ext4 disk is mounted from `/dev/sdc1` but has no fstab entry. The startup mount requires sudo authentication with no terminal. i3 PATH includes `wal`, ruling out the proposed missing-PATH explanation on this host. Confidence is supported; no fresh boot was traced.
- Resolution prepared: `scripts/enable-ubs-boot-mount.py` discovers the mounted ext4 UUID, previews or installs an idempotent systemd automount entry, refuses conflicts, backs up fstab and replaces it atomically. It does not format or unmount disks or modify sudoers.
- Verification: defining tests first failed twice because the installer was absent, then both passed. Existing ubuntu-start and pywal regression scripts exit 0. Actual-host `--check` exit 0 prints the missing entry. `sudo -n -l` exits 1 with password required; no privileged apply attempted. A missing optional sync-shortcuts function file was an inspection-only miss; the real external helper exists. Slow journal inspection completed without establishing a fresh-login sudo trace.
- Status: activation_pending. Agent cannot supply the sudo password; root installation and reboot visual acceptance remain outstanding. No claim of live boot success.
- Next: run `sudo python3 scripts/enable-ubs-boot-mount.py --apply` from the repository root, repeat `--check`, then verify wallpaper appears after reboot before opening a terminal.
- Learning: recorded a local lesson about verifying startup outcomes; reviewed ledger and guidance keep privileged activation separate from passing code checks.
