# Postmortem: Design Skills Timer Verified Before Its Helper Was Deployed

**Incident date:** 2026-08-19
**Severity:** Low — local configuration deployment only
**Status:** Resolved

## Symptom

The design-skills timer unit passed its static assertions but
`systemd-analyze verify` failed because its `ExecStart` helper had not yet
been deployed to `~/scripts/sync-design-skills`.

## Impact

The daily timer was not enabled. No external source, UI/UX Pro Max bundle,
account, or paid media operation was changed by the failed verification.

## Evidence

`python3 -B -m unittest tests.test_design_skills_sync -v` reported:

```
design-skills-sync.service: Command /home/example/scripts/sync-design-skills
is not executable: No such file or directory
```

## Root cause

The unit was verified before chezmoi deployed its tracked `ExecStart` target.
`systemd-analyze verify` resolves executable paths, so source-level unit
validity alone could not prove the installed unit was valid.

## Resolution

Applied only `~/scripts/sync-design-skills` and the two
`design-skills-sync` unit targets through chezmoi, reran the test suite, and
then enabled the timer through the hardened setup command.

## Verification

- `python3 -B -m unittest tests.test_design_skills_sync -v`: 6 passed.
- `scripts/executable_setup-design-skills-timer --check`: passed.
- `setup-design-skills-timer --enable`: passed.
- `systemctl --user list-timers design-skills-sync.timer --no-pager`: next
  activation is 2026-08-20 05:00 EDT.

## Follow-up

Keep deployment-order verification in the regression suite: apply the helper
and units before calling live `systemd-analyze verify` or enabling the timer.

## Tooling note
