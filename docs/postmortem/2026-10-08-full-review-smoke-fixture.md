# Full review smoke fixture assumed nonexistent checks

The disposable smoke check failed while verifying the new full report. Inspect the fixture's actual check state, correct only the expectation, and rerun source and installed verification.

## Symptom and impact
The source smoke script asserted `Current checks:` for the newest directory, but the fixture deliberately clears summary checks before creating those sessions. The terminal renderer correctly shows `Checks: None reported.` The assertion prevented pager verification; no installed files or real private state changed.

## Evidence and status
Command: `python3 -B tests/scripts/second_brain_sessions_review_check.py --runtime-dir scripts --pager-check`, exit 1 at line 127. `summary['checks']=[]` occurs before newest fixture sessions are created. The 103 focused tests passed. Status: investigating fixture expectation; next step correct the expectation to the data and separately verify retained disposition display using Work 1.

## Lookup and diagnosis
Query: `smoke fixture assertion expected nonexistent checks`. Reviewed `ext-realistic-fixture-boundaries` in API contracts/fixtures; its general principle applies (expectations must match real fixture state), while Discord-specific remedies do not. No product defect was demonstrated. The first correction exposed a second incorrect expectation: Work 1 still has its saved current summary check, although the check was explicitly dismissed; clearing the generator affects later summaries only. It correctly belongs to Current checks, with Dismissed disposition. Retained-earlier behavior is covered independently by renderer tests.

A third obsolete comparison compared no-pager output with a report captured before a later budgeted refresh. The new full footer correctly reveals changed global cache coverage and latest recap time. Compare equivalent snapshots at the same workflow point rather than hiding counters or asserting stale output equality. This is the same fixture-assumption root cause.

## Resolution and verification
Corrected fixture assertions to require empty checks where none exist, current dismissed checks for Work 1, and equivalent report snapshots for pager bypass. Production behavior was not weakened. Source smoke with `--runtime-dir scripts --pager-check` now exits 0, verifying five directories/three sessions, zero unchanged inference, preserved dismissals, default/details parity, JSON/ASCII, and real bat/less scrolling and q. The focused suite passes 105 tests; broader Second Brain suite passes 355/356 with only the known unrelated vault inventory failure. Status: fixture repair verified in source and installed smoke with real PTY, both exit 0; the task plan records installed command acceptance.

## Learning
No new reusable rule: this repeats the reviewed fixture-state boundary principle. Register the report's current reviewed hash with this explicit decision. Retain the report with the relevant smoke implementation and plan changes.
