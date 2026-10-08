# ctp alias command inspection failures

This report records command-runner obstacles while adding the ctp shortcut and the verified route used to continue.

- Symptom: Two initial read commands failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Later inspections guessed `scripts/executable_refresh-config` and `docs/task-status.md`, which do not exist.
- Impact: Inspection was delayed; no requested command or mutation ran in the failed initial launches.
- Lookup: Searched `bwrap loopback Failed RTM_NEWADDR`; matched `local-sandbox-loopback-approved-route` (verified workaround). Applicable because failure occurred before command output. Reviewed its execution-environments reference before subsequent task operations.
- Root cause: The runner cannot initialize loopback; exact host policy remains uninvestigated. The refresh helper is a fish function, not a script at the guessed path.
- Resolution: Approved scoped execution returned repository status and source reads with exit 0. File discovery located `dot_config/fish/functions/refresh-config.fish`.
- Verification: Approved preview exited 0 and proposed only `ctp "codex-time projects"` in work, with zero conflicts. `rg --files` located the actual refresh source.
- Status: Verified workaround; default sandbox remains unresolved. Alias implementation and refresh completed successfully; commit delivery is tracked in plans/commit-ctp-session.md.
- Follow-up: Use file discovery before opening guessed helper paths; do not change host security settings for this task.
- Learning: No new reusable learning: existing sandbox approved-route guidance and helper discovery guidance cover these observations. Targeted ledger check is required after registration.
