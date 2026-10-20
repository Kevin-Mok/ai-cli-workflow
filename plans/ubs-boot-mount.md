# UBS boot mount

Mount the wallpaper disk before desktop startup so the existing i3 `ubuntu-start` hook can apply the wallpaper without a sudo terminal.

## Context and decisions

The live wallpaper resolves into `/mnt/linux-files-3`; its ext4 disk is `/dev/sdc1` with a stable UUID (discovered locally; not stored here). `/etc/fstab` has no entry for this target. i3 PATH already includes `wal`. `sudo -n -l` reports that a password is required. Preserve all pre-existing dirty postmortem knowledge and prompts; do not commit or refresh unrelated changes. The boot-mount installer must discover the UUID from the mounted disk, validate ext4, refuse conflicting fstab entries, and create a backup before changing fstab. Use systemd automount with nofail and a bounded device timeout so an unplugged disk does not prevent login. No sudoers changes.

## Implementation

- [x] Inspect live startup environment, wallpaper symlink, mount and fstab.
- [x] Reproduce missing boot entry with a defining test.
- [x] Add the smallest reusable installer with check/apply modes, protected backup and stable UUID entry.
- [x] Update README and smoke checks; run focused automated checks.
- [x] Document privileged activation boundary. No tracked live configuration was edited; helper is invoked directly from the repo, so no chezmoi refresh is needed.
- [x] Reconcile incident learning and final verification.

## Verification and risks

Test fstab transformation against empty, already-correct and conflicting entries. Run installer check on the actual host. Apply requires sudo authentication unavailable to this agent; provide the exact reusable invocation if not activatable. Do not unmount the live disk, reboot, restart i3, or change sudoers. Rollback is restoring the printed fstab backup then running systemctl daemon-reload; keep the current mount intact. Boot/login visual acceptance remains unverified until a fresh login.

## Progress and review

Investigation confirms missing persistent mount and sudo authentication boundary. Existing startup hook and running compositor did not prove wallpaper success; prior completion claim was too strong.

Verification: `python3 -B tests/test_ubs_boot_mount.py` observed two missing-installer RED failures, then two GREEN tests. `bash tests/test_ubuntu_start.sh` and `bash tests/test_apply_pywal_theme.sh` exited 0. Live helper `--check` exited 0 and printed the proposed missing entry. Activation requires a user-authenticated sudo invocation; no system fstab edit, reboot, or login visual verification performed. README, smoke tests, historical plan follow-up, local lesson and incident knowledge updated together. Commit-session delivery now authorized.

Atomic next step: apply the already-reviewed helper as root, repeat check, reboot and observe wallpaper before opening a terminal. Suggested commit: `fix(i3): prepare persistent wallpaper disk mount`. Cursor continuation prompt: “Read plans/ubs-boot-mount.md. Verify sudo installation of the existing helper and fresh-boot wallpaper; preserve unrelated dirty work and do not claim boot success from process presence.”

## Delivery milestone: fix(i3): prepare persistent wallpaper disk mount

Completed: installer, defining tests, README usage, smoke checks, superseded-plan note, local lesson, and reviewed incident knowledge. Fresh validation: two unit tests pass; ubuntu-start and pywal regression scripts exit 0; README gate `pass_no_change`. Privileged activation and reboot acceptance remain pending, rather than code checks proving boot success. Next step: run the helper once with authenticated sudo, then verify a fresh boot.

Commit scope uses direct-write evidence for session `01a15a8f-bb93-7a62-85cf-86c44d315a88`: scope helper returned unsafe because nested tool writes were not detected. Isolate this session's README/smoke hunks and two report records plus one finding from the mixed postmortem ledger. Exclude screensaver changes, aliases, prompts, pre-existing incident guidance and all other unattributed changes. Keep matching plans in the same commit. Privacy gate must pass against the exact isolated candidate before commit; push the resulting commit once to origin/main. No history rewriting.

Privacy preparation: the first candidate scan blocked machine-local ledger aliases. Sanitize those aliases to the established public example root only in the isolated candidate; retain local lookup aliases and unrelated edits privately. The exact repaired candidate must pass before commit.

Delivery checks: repaired isolated-candidate privacy scan PASS; no rules or hooks bypassed. Only public example aliases are staged; live lookup aliases remain local. README gate `pass_no_change`; fresh two-test unit suite and both existing shell regressions pass.

Local targeted postmortem checks passed for all three UBS reports, and staged report hashes match staged ledger records. A separate screensaver session began staging unrelated changes during delivery; keep the isolated candidate and preserve those real-index entries, including shared-file hunks, during reconciliation.
