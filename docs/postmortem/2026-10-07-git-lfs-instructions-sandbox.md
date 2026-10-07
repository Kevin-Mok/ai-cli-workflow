# Git LFS instruction edit: shell sandbox startup

The initial read-only commands failed before execution. Approved scoped execution
allowed the instruction edit to proceed without changing host sandbox policy.

- Symptom/evidence: two command launches exited 1 with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: repository status and instruction reads were initially unavailable; no command body ran.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; reviewed `local-sandbox-loopback-approved-route` in execution-environments.md. The startup signature matched this task.
- Cause: sandbox loopback initialization was denied; underlying host policy remains unresolved.
- Resolution/status: verified workaround; approved scoped reads completed with exit 0 and captured pre-existing Git changes before editing.
- Additional lookup issue: a search included nonexistent `scripts/executable_refresh-config`; the real function was located at `dot_config/fish/functions/refresh-config.fish`. No file was modified by that search.
- Verification: approved status/source reads returned expected content; the canonical instruction edit is checked separately with Git diff.
- Follow-up: use the existing scoped fallback; do not change host security policy for this documentation task.
- Learning: no new reusable learning; existing sandbox startup and exact-path guidance covers these symptoms.
