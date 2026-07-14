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
it. The complete command, path, and timer suites pass. Final installed command,
checkpoint dry-run, timer, Git-ref, and protected-state evidence is recorded in
the [Second Brain ExecPlan](../../plans/integrate-second-brain.md).

## Follow-Up

- Make fake external commands reject unexpected arguments.
- Exercise installed entrypoints with real tool mappings before activation.
- Keep source and installed repository resolution on the same validated path.
