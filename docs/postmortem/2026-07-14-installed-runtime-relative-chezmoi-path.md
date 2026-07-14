# Installed Runtime Used A Relative Chezmoi Target

## Symptom

The source `setup-second-brain-timer --check` passed after activation, while
the byte-identical installed command exited with
`timer setup state path is unsafe`.

## Impact

The timer was enabled and waiting, but the installed `second-brain checkpoint`
entrypoint would have failed to resolve the source repository at 16:20. No
checkpoint had run, and no repository or remote ref moved.

## Evidence

Real `chezmoi source-path second-brain/README.md` exited 1 with `not managed`.
The absolute applied destination at `~/second-brain/README.md` resolved to
`/home/example/linux-config/second-brain/README.md`. The source command avoided
the bug because its module path already lives below the Git checkout.

## Root Cause

The installed fallback passed a relative path to chezmoi. Its test double
printed the expected source for every argument, so it did not enforce the real
CLI contract and masked the invalid request.

## Resolution

Repository fallback now asks chezmoi for the source of the absolute applied
vault front door, then retains the existing absolute-path, symlink, Git-root,
and vault-front-door validation.

## Verification

The strengthened installed-layout test failed before the fix and passed after
it; the final independent command/path/real-chezmoi suite passed 52 tests. After
commit `0bdb8c2` was pushed, source and installed runtime hashes matched, the
installed setup check and status passed from `/tmp`, and checkpoint dry-run
reported only the protected config without mutation. The timer remained
enabled and active for 16:20 with no catch-up journal. Git refs and protected
repo/live checksums remained exact. Full evidence is recorded in the
[Second Brain ExecPlan](../../plans/integrate-second-brain.md).

## Follow-Up

- Make fake external commands reject unexpected arguments.
- Exercise installed entrypoints with real tool mappings before activation.
- Keep source and installed repository resolution on the same validated path.
