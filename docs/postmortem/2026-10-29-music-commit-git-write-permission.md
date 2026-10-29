# Music commit Git write permission

The session-only commit reached staging but Git object writes required the normal
approved permission route. Preserve the scoped documentation and retry staging
with that route, then run the privacy gate before committing.

- Symptom: `git hash-object -w --stdin` returned exit 128 with “unable to create
  temporary file: Read-only file system”. No staging mutation completed.
- Impact: commit delayed; working files were preserved.
- Cause: the active filesystem profile explicitly mounts `.git` read-only.
- Lookup: `postmortem_memory.py search 'git read-only file system sandbox'`
  returned `ext-sandbox-loopback`. Its permission-route principle is relevant;
  its loopback diagnosis does not match this filesystem failure.
- Status: staging recovered through `require_escalated`; scoped Git object
  creation and index updates succeeded, exit 0. Default restrictions remain.
- Verification: only the five selected session paths were staged after recovery.
- Next steps: inspect the final candidate, privacy-check, commit,
  and push origin/main. Do not weaken filesystem policy or bypass Git hooks.
- Learning: no new reusable finding; explicit sandbox metadata already explains
  the boundary. Keep this factual operational record with the session commit.

The first ledger scan passed a file to directory-only `--root`; its JSON reported
that argument error. Targeted `check --postmortem` then verified this report.
Repeat discovery with the containing directory. This was a verification-command
argument mistake, with no product or source-data impact.
