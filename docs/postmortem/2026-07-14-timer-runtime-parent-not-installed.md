# Timer Runtime Parent Was Not Installed

## Symptom

The first real `setup-second-brain-timer --enable` run exited with
`chezmoi unit apply failed`, and the timer remained disabled.

## Impact

Chezmoi installed the launcher and two user units before stopping, but
`~/scripts/second_brain` and its runtime modules were absent. Systemd was
never reloaded or enabled, no checkpoint ran, and the repository plus protected
Codex config remained unchanged.

## Evidence

The runtime package target did not exist after the failure, while the launcher
and unit files did. `systemctl --user is-enabled` reported `disabled` and
`is-active` reported `inactive`. Local and upstream Git refs both remained
at `fa80508`, and the protected config checksum remained
`3edd706e3cc03132764d9d0a1b741e0713f42e39dc16a6018ab205f9d1a85e2e`.

## Root Cause

Setup passed exact nested runtime-file targets to `chezmoi apply` but omitted
an explicit clean-install parent-creation step. A dry-run could render the
missing files, while the first real apply could not create the absent runtime
package directory. The fake chezmoi test fixture had hidden this by creating
that directory unconditionally.

## Resolution

An initial `--parent-dirs` candidate made the missing-parent tests pass, but an
independent real-filesystem review showed that it changed existing restrictive
directory modes from `0700` to `0775`; that candidate was rejected. Setup now
uses a descriptor-relative transaction to create only its missing launcher,
runtime-package, and unit parent directories. Newly created directories are
`0755`; existing modes are preserved; ownership, identity, non-symlink, and
real-directory checks run before the unchanged exact-file chezmoi apply; and a
pre-apply failure rolls back all directories created by that attempt.

## Verification

The clean-home, restrictive-mode, symlink, non-directory, injected-swap,
mkdir/open-failure, transaction-rollback, and exact-target regressions pass. A
real chezmoi clean-destination test installs exactly the intended 27 files.
Full regression evidence is recorded in the
[Second Brain ExecPlan](../../plans/integrate-second-brain.md). Real activation,
installed-file identity, timer state, next-trigger, journal, and final
repository/upstream evidence will be appended there after the fix is upstream.

## Follow-Up

- Exercise empty-destination first installs, not only dry-runs and upgrades.
- Keep exact nested file targets and test parent creation as a separate,
  rollback-safe invariant.
- Treat a dry-run as mapping evidence, not proof that destination creation can
  complete.
