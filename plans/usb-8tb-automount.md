# Automatically mount the external 8 TB disk

Make the existing ext4 disk available at /mnt/usb-8tb when powered on, without blocking startup while it is off. Preserve all disk contents and unrelated configuration.

## Context and decisions

The existing fstab row identifies UUID=e2f4a51f-954a-4168-a1af-2c9645d3f00a with defaults,nofail. The drive is currently mounted. Use native systemd automount plus a UUID-specific udev activation rule for eager hotplug mounting. Reuse the existing boot-mount installer style, without altering its wallpaper-drive contract. Only the exact existing 8 TB row may change; conflicting entries must stop installation. No formatting, unmounting, or privilege-policy changes.

## Checklist

- [x] Capture initial git status and inspect host disk/fstab; preserve all pre-existing dirty files.
- [x] Identify administrator boundary: sudo requires a password; host reads require approved execution outside sandbox.
- [x] Observe defining RED tests, implement installer, verify focused regressions and preview.
- [x] Update README and grouped smoke checks; record evidence.
- [ ] Apply with administrator authentication and verify active units.
- [ ] Verify safe power cycle and off-at-boot behavior manually.

## Scope and risk

Files: scripts/enable-usb-8tb-automount.py, tests/test_usb_8tb_automount.py, this plan, README.md, and additive docs/smoke-tests.md entries. Preserve pre-existing changes in smoke tests and all other files. An interrupted install is safely rerunnable. Back up fstab before replacing it. Refuse a pre-existing different udev rule. Rollback: remove only the installed rule, restore the printed fstab backup, reload udev and systemd. Do not power off without unmounting first. Actual device appearance and reboot cannot be simulated safely on a disk in use.

## Verification

Defining tests cover upgrading the exact existing fstab row, idempotence, preserving unrelated rows, rejecting a mismatched UUID/mountpoint/filesystem, and the hotplug rule. Use --check for read-only preview, --apply with sudo, systemctl status for the automount, and findmnt after safe replug. Run the focused new test plus existing boot-mount regression. Installer preview must not claim activation. Review final diff and documentation for consistency.

## Progress and evidence

Initial inspection: fstab lacks automount/hotplug configuration; host systemctl shows the existing mount active. No privileged writes made. See docs/postmortem/2026-10-22-usb-8tb-admin-boundary.md for inspection access limits. The user subsequently requested commit-session; only directly observed USB task edits are eligible.

## Final verification and handoff

- Initial RED: four tests failed because the installer was absent. Second RED: doubled unit-name escaping and both activation cases failed before implementation.
- Final GREEN: `python3 -B tests/test_usb_8tb_automount.py` passed 6 tests, exit 0; `python3 -B tests/test_ubs_boot_mount.py` passed 2 tests, exit 0.
- `python3 scripts/enable-usb-8tb-automount.py --check` and `--check --plain` show the intended configuration and correctly report installation pending.
- `udevadm verify /tmp/99-usb-8tb-automount.rules`: one success, zero failures, exit 0 (final doubled-backslash rule).
- Host `findmnt --verify --verbose --tab-file /tmp/usb-8tb-candidate.fstab`: zero parse errors, zero errors, exit 0; six filesystem-probe warnings because an unprivileged user cannot read raw devices. The sandbox validation could not resolve device links; host validation confirmed the correct /dev/sdd1 UUID.
- Reviewed systemd 255 compatibility: an active real mount prevents starting the automount; preserve it and defer on-access activation. Udev SYSTEMD_WANTS requires doubled backslashes for the escaped hyphen. The rule requests the mount unit directly on device arrival. Sources: https://www.freedesktop.org/software/systemd/man/257/systemd.mount.html and https://github.com/systemd/systemd/issues/16760.
- Updated README command table and docs/smoke-tests.md with installation, power-cycle, absent-at-boot, and rollback checks. No live tracked dotfile configuration changed; refresh-config is not needed for an unapplied standalone administrator installer.
- Installation, reboot, and actual power-cycle acceptance remain pending administrator authentication. Do not claim these passed. Live installation is separate from committing the prepared installer. Protected dirty state remains outside this change.

Atomic follow-through: run the installer with sudo; inspect installed preview and mount; close drive users and safely unmount before a power-cycle test; verify a later reboot with the disk off. Run the exact automated checks above after any edits. See the smoke-test section for exact manual acceptance and rollback.

Cursor continuation prompt: "Read plans/usb-8tb-automount.md and the USB installer. Preserve all unrelated dirty work. Have the user run sudo python3 scripts/enable-usb-8tb-automount.py --apply in an authenticated terminal. Verify configuration and the active ext4 mount; only test power cycling after a successful clean unmount. Record actual results without claiming pending hardware checks passed."

Suggested commit: `fix(storage): mount external 8TB disk on connection`. Include this plan and related docs with implementation if a commit is later requested.

## Commit milestone: fix(storage): mount external 8TB disk on connection

Prepared implementation and documentation are verified; live installation remains pending sudo, with reboot and power-cycle acceptance unperformed. Commit and push this milestone to origin/main; no other implementation work is required before installation. Rollback and subsequent validation remain documented above.

Session scope: 01a164fe-0b7b-78b3-9e3b-719b3f2a7477. session_scope.py returned unsafe because it detected no wrapper-mediated writes or baseline; direct conversation evidence establishes the four newly authored files (installer, tests, plan, postmortem), the README command row, the external-8-TB smoke section, and the single postmortem ledger record. For the shared ledger, form the candidate from HEAD plus only this report; retain unrelated working changes. Other dirty files and unrelated ledger edits remain excluded. An isolated candidate index preserves unrelated staging.

Fresh commit checks: USB tests 6/6 and existing wallpaper boot-mount tests 2/2 passed, both exit 0; README gate returned pass_no_change. The staged privacy gate must pass immediately before committing. Commit hash and actual push result will be reported in the handoff; neither hardware activation nor hotplug acceptance is implied by shipment.

Privacy review: the initial exact-candidate gate blocked the local home-path ledger alias. The committed entry uses the existing /home/example convention; local working lookup retains the actual alias. The candidate includes only the newly reviewed report, and leaves all unrelated ledger changes uncommitted. Repeat the privacy gate after this repair.
