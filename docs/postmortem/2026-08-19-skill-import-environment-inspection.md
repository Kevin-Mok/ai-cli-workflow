# Postmortem: Skill Import Environment Inspection Failures

**Incident date:** 2026-08-19
**Severity:** Low — local agent workflow only
**Status:** Resolved with a safe alternate inspection path

## Summary

While preparing a managed import of public design skills, an initial sandboxed
read failed with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
A later repository-layout probe also assumed a `.chezmoiscripts` directory that
does not exist in this checkout. Neither command changed tracked source files
or the live skill installation.

## Impact

The import was briefly delayed while the correct read-access mode and the
actual repository layout were established. No skills, configuration, secrets,
or user files were altered.

## Detection and evidence

- Initial read-only inspection returned the Bubblewrap loopback-permission
  error before producing command output.
- A final plan search reproduced the same error in the restricted sandbox;
  the approved read-only rerun returned the expected source lines.
- The normal repository patch helper then failed to read the same files for the
  same reason; an approved narrow edit applied the pre-reviewed text.
- The equivalent inspection with approved workspace access completed
  successfully.
- `rg --files .chezmoiscripts` returned an explicit no-such-directory error;
  the repository later established that local skill sources are under
  `dot_agents/skills/` and are documented in the root README.

## Root cause

The restricted sandbox cannot create the loopback address needed for that
initial shell invocation. Separately, the inspection used an obsolete assumed
directory name instead of enumerating the repository before targeting it.

## Resolution

Subsequent read-only inspections use approved workspace access, and repository
layout discovery uses `rg --files` from known existing roots. The import plan
now treats `dot_agents/skills/` as the managed source of truth and avoids the
absent directory.

## Verification

- The rerun inspection read the relevant instructions, existing skills, and
  dirty-worktree baseline successfully.
- `./scripts/executable_ai-workflow-doctor --repo . --check` exited 0 with no
  objective errors. Its single duplicate-skill warning pre-dated the work.

## Follow-up

- Validate a directory exists before passing it as a required `rg` target.
- Keep managed skill import verification focused on the discovered source and
  deployment roots.
- Use approved read-only workspace access when the restricted shell reports
  this known Bubblewrap loopback limitation.
