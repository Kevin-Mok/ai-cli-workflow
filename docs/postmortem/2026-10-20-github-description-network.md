# GitHub description inventory network boundary

The default sandbox could not connect to GitHub during the authorized description inventory. Scoped network escalation restored the read; continue the metadata task through that approved boundary.

- Symptom/evidence: `gh-axi api /users/Kevin-Mok/repos?per_page=100&type=owner --paginate --full` returned `error connecting to api.github.com`, exit 1.
- Impact: initial read only failed; no remote writes occurred in the failed command.
- Lookup: postmortem-memory search `error connecting api.github.com network sandbox` returned ext-sandbox-loopback and external access guidance. Applicable principle is separating execution/network restrictions from repository faults; no loopback startup failure was observed here.
- Root cause: restricted network access in the default sandbox, supported by the same inventory succeeding through scoped require_escalated execution.
- Resolution/verification: approved scoped gh-axi inventory read exited 0; exact JSON transport decoded 52 eligible public repositories.
- Status: verified workaround; default sandbox networking remains unchanged.
- Additional evidence: one besu-deploy source-blob read through scoped access timed out (`dial tcp ... i/o timeout`); this was read-only, so a targeted research retry is safe. No write ambiguity occurred.
- Final verification: scoped targeted besu-deploy source retry succeeded at commit 8c1b3ad699e85b5b348daff0d690d6cf09c0e1e5. All 45 authorized description updates and final 52/52 exact GitHub readbacks succeeded, exit 0.
- Next steps: none for this task; default sandbox networking remains restricted.
- Learning decision: no new reusable finding; existing sandbox permission-boundary guidance covers the workaround. Never infer repo/API failure from a sandbox connection error.
