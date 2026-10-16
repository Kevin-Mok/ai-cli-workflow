# Pre-push worktree setup blocked by sandbox

The requested fetch and worktree setup needed writable Git metadata. Use the
normal approval mechanism for those operations, then continue in the worktree.

## Symptom and impact

The initial fetch exited 255 because FETCH_HEAD was on a read-only filesystem.
No repository source changed and implementation had not started.

## Evidence and lookup

The permission profile mounts Git metadata read-only. Postmortem-memory lookup
for `FETCH_HEAD Read-only file system` returned broad environment/path guidance,
but no specific matching remedy. That guidance does not diagnose this incident;
the command error and permission profile establish the cause directly.

## Resolution and verification

The same authorized fetch and requested worktree creation succeeded through the
normal escalation mechanism (exit 0). The feature branch starts at origin/main,
502ac1f. No source workaround, permission weakening or force push was used.

## Follow-up

Use approval for subsequent Git metadata mutations in this environment.
This is an environment limitation with a verified workaround; there is no new
repository implementation defect or reusable learning beyond existing sandbox
permission guidance.

## Related verification invocation correction

The README gate was mistakenly invoked with Python, producing a syntax error
before execution. Its shebang specifies Bash. Lookup `explicit-wrapper-shell`
returned `ext-explicit-wrapper-shell`, whose interpreter-inspection guidance
applies. Invoke the existing Bash helper directly; no implementation fix is
needed. The corrected Bash invocation exited 0 with `pass_no_change`.

A later plan-only patch included an unrelated context line and was rejected before
writing. Lookup `patch context` returned `ext-stale-patch-context`; its exact-context guidance applies; the plan was updated
using its actual current text. No source behavior or verification was affected.
