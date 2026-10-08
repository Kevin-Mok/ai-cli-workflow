# Live backup preflight rejected the mounted system's swap alias

The read-only live backup preflight reached the current installation but rejected a valid swap device expressed as /dev/disk/by-uuid. Resolve conventional swap aliases before comparing them with block-device records, then rerun the same preflight and regression tests.

- Symptom/evidence: source_preflight('/', '/mnt/usb-8tb/sys-backup', live=True) reported Unsupported or missing source swap for a /dev/disk/by-uuid path. No backup files or disk writes were made.
- Impact/status: resolved; verified code fix and actual-machine read-only preflight, no full-machine backup performed.
- Lookup: searched tracked postmortem memory for backup swap by-uuid symlink. No directly applicable swap-alias finding identified; general source-path/alias practices apply. Evidence is fstab device alias versus lsblk canonical name.
- Root cause: swap lookup compares the raw fstab string only with canonical names and UUID= expressions, missing /dev/disk symlinks.
- Resolution: resolve absolute swap aliases (and supported LABEL/PARTUUID aliases) to canonical block names before conventional partition/source-disk checks. No layout guard removed.
- Verification: alias regression failed before fix, then passed; source_preflight with / and /mnt/usb-8tb/sys-backup succeeded on this machine, recording its source swap capacity. Final 37 backup tests, bash syntax and whitespace checks passed. No backup/disk/mount writes in the actual preflight.
- Follow-up: use the new --live command with checksum-protected live-nonatomic consistency warnings; validate actual recovery/boot separately in disposable VMs.
- Learning: registered local-backup-swap-alias in tracked paths/ownership guidance and source ledger; verified fix scope covers alias preflight plus code regressions, not live full-backup/recovery success. Installed knowledge remains read-only.
