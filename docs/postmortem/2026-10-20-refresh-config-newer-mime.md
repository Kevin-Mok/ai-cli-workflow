# Refresh stopped on newer local MIME associations

Refresh stopped to protect local app associations. Compare timestamps and the target diff, preserve newer local changes in source, then retry the normal unforced refresh.

- Symptom: reported refresh log ended with a mimeapps.list changed-since-write prompt and EOF.
- Impact: refresh stopped before shortcut regeneration.
- Lookup: postmortem-memory search for “refresh-config chezmoi changed EOF mimeapps” matched local-mime-drift-reconcile. Its reviewed source-reconciliation remedy applies; broad force remains unnecessary.
- Evidence: local MIME file dated October 19 was newer than source dated October 16. Target diff showed source missing only the grokbot and sand protocol handlers.
- Resolution: preserved both local handlers in source; recorded the newer-local-file rule in canonical AGENTS.md and appended durable feedback.
- Verification: target-scoped chezmoi diff is empty, exit 0; git diff --check passed. Full refresh emitted REFRESH COMPLETE, exit 0.
- Status: resolved; normal unforced refresh completed.
- Next step: no further remediation required. Preserve all pre-existing dirty files; commit-session now authorizes a focused commit and push.
