# VPS Repair Fails While Reading Fish Environment

## Symptom And Impact

The user ran the delivered VPS repair helper on October 3. SSH reached the
VPS, printed missing desktop fish-function and pywal-file warnings, and the
helper exited with `Could not read the login shell environment`. No Codex
installation or managed configuration repair had started at that point.

## Evidence And Current Status

The screenshot shows a successful connection followed by a local payload
handshake failure. `shell_environment` requires exactly one output line
starting with `VPS_CODEX_ENV=`. Its initial tests used quiet fish startup.
A read-only SSH probe reproduced it: fish exited 0 and emitted exactly one
marker, but zero lines began with that marker. The bytes before the marker
were `ESC[6 q`, a cursor-control sequence with no terminating newline.
The missing desktop paths are separate startup warnings.

## Root Cause

The helper assumed line-oriented startup output. Fish's cursor initialization
violates that assumption, joining a terminal-control sequence to the marker.
The same assumption also affects shell-type and final-version checks. Initial
tests covered real fish PATH changes but used quiet startup, so they missed
this behavior.

## Resolution And Verification

Added regressions for real fish emitting the exact cursor sequence, bash
printing a banner without a newline, and misleading host-key advice after an
ordinary remote command failure. All three failed for the expected reasons
before implementation (exit 1).

All interactive shell commands now pass through `login_run`, which prints a
newline after startup and before the command output. Exact marker validation
is preserved. Host-key advice now appears only for SSH exit 255.

`python3 tests/test_fix_vps_codex.py` passed all 24 tests, and
`bash -n scripts/executable_fix-vps-codex.sh` passed (both exit 0).
A read-only SSH probe extracted the exact corrected functions from the helper
and exercised environment capture, both command-type checks, and
`codex --version` on the VPS. All passed (SSH exit 0); the installed CLI
reported `codex-cli 0.114.0`. No npm install or managed configuration change
was performed by that probe. The desktop-path warnings remain independent.

The user can rerun the same local repair command. Live update acceptance is
still pending; no remote upgrade is claimed. Rollback for this code fix is
reverting the local helper/test/doc edits, though that restores the known bug.
