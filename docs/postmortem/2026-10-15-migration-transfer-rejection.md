# Migration transfer rejected a synthetic test assignment

The authorized apply attempt stopped during reviewed transfer before cutover. Preserve its private recovery directory, reproduce the scanner mismatch in a disposable repository, correct the fixture source without weakening scanning, and validate a new retry directory before another live attempt.

## Symptom and impact

The helper reported secret/private-content rejection and rollback. Read-only journal inspection confirms phase `rolled_back`, no archive, and a retained independent candidate. The original active checkout remains present. The offending path is `tests/test_second_brain_config_snapshot.py`; no values or raw patches are recorded here.

## Lookup and evidence

Postmortem-memory query `migration secret transfer rejected scanner synthetic credential false positive` returned no applicable scanner-specific finding. Repository auditor returns no categories for the offending source, while the migration helper’s supplementary guard rejects two synthetic local variable assignments. The prior overlay preflight used only the repository auditor and therefore did not exercise the exact transfer predicate. A direct content-only diagnostic reproduced this mismatch without invoking apply.

## Status and next steps

Verified in code and read-only preflight; live retry not yet executed. Defining integration test reproduced the user’s exact rejection (RED), then passed after renaming Python local identifiers without changing runtime sentinel values. The migration scanner remains unchanged. Keep scanners intact; rename ambiguous test variables while retaining exact runtime test values and coverage. Add an integration test that transfers the actual snapshot regression source through the production predicate. Preserve the failed recovery directory and prepare a distinct retry directory. Do not rerun blindly using the rolled-back journal. No live refresh or cutover has occurred.

## Resolution and verification

The previous readiness review exercised only `scan_content` from the public history auditor; apply also invokes the supplementary `content_safe` guard. Local synthetic variable assignments matched that extra guard. Readiness checks now use the exact combined predicate for every reviewed path. Added regression coverage for transferring the actual snapshot-test source, path-only `--details` diagnostics, and preserving rolled-back attempts while requiring a new state directory.

Fresh tests: migration 34/34; snapshot 19/19; refresh shell integration exit 0. A disposable independent sanitized clone accepted all 25 then-current reviewed files using production transfer logic; actual rendering and shortcut rehearsal backed up 1,558 entries privately, and production pending-content audit passed. Subsequent changes are documentation/incident evidence only and are rehashed/rechecked. No live configuration writes or cutover were performed by these checks.

The failed default recovery directory remains intact with phase `rolled_back`, candidate retained, no archive and no live-start marker. The retry will use a distinct directory. Another shared-checkout shipping session was active, so another live apply was not launched automatically. Scanning remains bounded; no absence-of-all-secrets claim is made.

## Historical attempt boundary

This report records its specific attempt, not the latest checkout state. The
later cutover completed; current state and read-only follow-up are recorded in
[the migration plan](../../plans/migrate-sanitized-repo.md#current-state-completed).
Preserve prior journals privately and do not rerun these historical next steps.
