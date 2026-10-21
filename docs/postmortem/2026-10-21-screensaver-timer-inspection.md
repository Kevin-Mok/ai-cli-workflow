# Screensaver timer inspection path miss

A read-only inspection guessed a refresh-config script path. Use inventoried source paths; this incident did not affect the screensaver or user files.

## Symptom, impact and evidence

Reading scripts/executable_refresh-config returned “No such file or directory” and exit 2. The preceding bridge source read succeeded. No write or runtime action occurred.

## Lookup and resolution

Postmortem search “missing guessed script path” returned local-discover-paths-before-reads, which explicitly identifies refresh as a Fish function. Applicable: the failure was a guessed source name. No retry was needed; this task changes scripts and documentation, not managed configuration. Status: resolved inspection error. Verification: command output identifies only the nonexistent path; implementation tests are independent. Follow-up: use mapped paths. No new reusable learning beyond that existing finding.

## Regression environment failures

The test runner's initial sandboxed CLI run could not write /run/user/1000/media-screensaver/preview.lock; initial Xvfb execution also lacked a usable X11 display (one CLI failure and eleven environment errors). Scoped reruns passed: six focused CLI tests and all 57 screensaver tests, plus browser CJS. These establish environment restrictions, not product regressions; no production workaround was added. The runner inspected complete output. DRI2, deprecation and ResourceWarning diagnostics remain visible in Xvfb. Live desktop activation is unverified.

## Commit privacy gate

The pre-commit privacy scan rejected one home_path finding in the newly added postmortem-ledger alias. The physical alias is needed for local memory coverage but is not eligible for public delivery. Preserve that ledger addition locally and remove it from the staged candidate; do not approve or suppress the finding. The incident report and remaining task files are safe candidates. Verification: rerun the unchanged privacy gate on the narrowed index before committing.

Lookup “privacy gate home_path” returned local-privacy-reviewed-content-approvals; its neutral-alias/private-map limitation applies. This task uses the safer narrowed candidate instead of changing privacy policy. The reviewed local ledger retains physical coverage; its new entry remains uncommitted. No new reusable rule beyond existing privacy guidance.

Resolution verified: unchanged privacy gate passed the narrowed staged candidate (exit 0). No approval exceptions were introduced; the machine-specific ledger entry stays local.
