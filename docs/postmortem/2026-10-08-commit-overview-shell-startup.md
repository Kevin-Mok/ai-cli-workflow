# Commit overview shell startup failure

The commit-reporting preference update encountered a command-runner startup failure. Scoped approved execution allowed repository reads and the documentation update to proceed; the default sandbox remains unresolved.

- Symptom: two initial read-only calls exited 1 before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: those calls performed no repository changes; subsequent reads used approved scoped execution.
- Lookup: `bwrap loopback Failed RTM_NEWADDR` matched `local-sandbox-loopback-approved-route` and `ext-sandbox-loopback`, both verified workarounds. Identical errors on independent harmless reads establish applicability.
- Cause: the runner could not initialize loopback; host policy was not investigated.
- Resolution/evidence: scoped approved reads captured repository status and required skills with exit 0. This verifies only an execution workaround.
- Additional inspection error: a guessed `scripts/executable_refresh-config` path was absent (rg exit 2). File discovery located and read `dot_config/fish/functions/refresh-config.fish`; no edits relied on the guessed path.
- Status: verified workaround; default sandbox repair is outside this task.
- Learning: no new reusable learning; existing sandbox and path-discovery guidance covers these symptoms. Register this reviewed report in the tracked ledger and run its targeted check.
- Verification: focused policy/public-document diff review and targeted ledger coverage passed (exit 0). `fish -ic 'refresh-config'` exited 0 and printed `REFRESH COMPLETE`; log: `/tmp/refresh-config-20261008-141706-1987053.log`. Refresh adopted the existing live `scripts/second_brain/cli.py` and `scripts/second_brain/session_review.py` targets during its normal conflict recovery. The default sandbox was not repaired.
- Follow-up: host sandbox repair remains outside this documentation task; the requested policy update is applied.
