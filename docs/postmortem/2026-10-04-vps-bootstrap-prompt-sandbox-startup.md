# VPS bootstrap prompt inspection: shell sandbox startup failure

Date: 2026-10-04

## Symptom and impact

The first read-only repository inspection commands could not start. Each
returned exit status 1 with:

```text
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

No requested shell command ran in those attempts, so they produced no
repository changes. Inspection was delayed; no installer or AWS action ran.

## Evidence and root cause

The failure occurred while bubblewrap configured the loopback interface,
before the requested commands executed. The exact host restriction causing
that denial has not been established. This is an execution-environment
failure, not evidence of a problem in the repository's bootstrap code.

A subsequent explicitly reviewed read-only command outside that sandbox
returned exit status 0 and exposed the expected repository status and files.
Later read-only inspections used the same working execution route.

## Resolution and current status

Repository inspection resumed through the reviewed execution route. The
underlying sandbox restriction remains unresolved.

The incident happened during Plan Mode, which prohibited file writes.
This record was deferred until the user authorized saving the
[VPS/AWS implementation prompt](../../prompts/bootstrap-vps-aws.md).

## Verification and follow-up

- Initial sandboxed inspection: exit 1; commands did not start.
- Reviewed read-only inspection: exit 0; repository instructions and status read.
- Prompt-authoring continuation: read-only status and artifact-name checks
  returned exit 0 before any new files were created.
- Keep the restriction visible in future execution attempts; do not claim that
  the sandbox itself was repaired.

Keep this record with the [prompt-authoring plan](../../plans/compile-vps-aws-bootstrap-prompt.md)
if this task is committed later.
