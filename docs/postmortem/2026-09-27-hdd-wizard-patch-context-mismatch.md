# HDD wizard patch context mismatch

## Symptom and impact

An `apply_patch` attempt to add explicit ext4 `64bit` options failed because
its expected printf line did not match the current script. The tool reported
`Failed to find expected lines`. The patch made no file changes.

## Evidence and root cause

The failure occurred at patch verification, before mutation. The already
verified wizard and docs remained in place. `rg -n 'mkfs.ext4|new-partition'
scripts/hdd-init-wizard.sh` showed the preview was one `printf` source line
containing several literal `\n` escapes. The patch had matched only a
fragment of that line.

## Resolution and verification

Matched the complete `printf` line and updated all three ext4 command sites.
The interactive dry run then exited 0 and showed
`sudo mkfs.ext4 -F -O 64bit -L Storage /dev/sdd1`, followed by
`Dry run complete. No writes were made.` Syntax, help, and non-interactive
dry-run checks were rerun after the final script change.

## Follow-up and rollback

Match complete source lines when a shell `printf` uses embedded `\n` escapes.
No device action was attempted by the failed patch or its replacement.
