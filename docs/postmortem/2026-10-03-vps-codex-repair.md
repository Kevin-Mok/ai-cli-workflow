# VPS Codex Update Permission Failure

## Symptom And Impact

The supplied October 3 screenshot shows `npm install -g @openai/codex`
failing with EACCES while renaming `/usr/lib/node_modules/@openai/codex`.
Codex cannot update as the normal VPS user. Runtime age is unverified.

## Evidence And Current Status

The failing path is a system npm prefix. Ownership and effective npm
configuration on the VPS have not been inspected in this session. A local
repair script is being built; the user will run it against the VPS.

During preparation, shell inspection also failed before startup with
`bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. No command
body ran. Approved execution outside that sandbox restored local inspection.
This environment limitation is separate from the VPS permissions failure.

## Root Cause And Resolution

The screenshot establishes insufficient permission to modify the active
global Codex installation. The helper will confirm ownership and effective
prefix, install into a writable user location, and persist shell routing.
Node/npm replacement is conditional on actual runtime compatibility.

## Verification And Follow-up

The first implementation run reached the safety check but rejected the user's
home directory as a writable configuration parent. The containment helper
allowed descendants only, even when checking a parent. Eight of thirteen
isolated tests failed with that same error. Permit the home directory for
parent writability checks while retaining containment for writable targets.

The next run passed eleven tests and exposed an off-by-one path in the test
npm substitute: its default prefix was `installation/lib` instead of
`installation`. Corrected the fixture to match npm's actual prefix semantics;
the managed-runtime assertions were retained.

Both initial issues are resolved. The expanded local suite now passes 22
tests, including permissions, bash/fish PATH persistence, repeated runs,
rollback, SSH errors, dry-run immutability, runtime checksum failure,
interrupted install recovery, shell-function shadowing, and malicious archive
symlink/duplicate-member rejection. Bash syntax
checking also passes. These checks use disposable homes and external-service
substitutes, not the VPS.

The user's live dry-run/apply results remain pending. The helper reports
success only after a second SSH session proves ordinary updates work.
Record local evidence here when available. No live VPS repair is claimed.
