# tbo shortcut sandbox startup failure

The shortcut setup required an approved execution route because the default shell sandbox failed before running the requested command.

- Symptom/evidence: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; initial read-only command returned exit 1 before its body ran.
- Impact: initial inspection blocked; no files modified by that launch.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; `local-sandbox-loopback-approved-route` applies because the failure occurs in runner startup, before repository code.
- Status: verified workaround. Approved scoped execution returned exit 0 and allowed source inspection and the alias helper to apply the reviewed mapping.
- Root cause: sandbox loopback initialization denied; underlying host policy remains uninvestigated.
- Resolution: continue authorized shortcut setup through reviewed `require_escalated` execution.
- Verification: successful status/source reads and alias preview/apply; default sandbox remains unresolved.
- Completion evidence: `fish -c refresh-config` returned exit 0 with `REFRESH COMPLETE`; generated fish syntax passed and the helper repeat preview returned `changed: false`. The registered abbreviation maps tbo to the requested command.
- Follow-up: default sandbox repair remains separate. No new reusable learning beyond the existing approved-route finding.

- Delivery inspection: `docs/task-status.md` was absent (read returned file-not-found). `git ls-files docs/task-status.md` confirmed no tracked status file; create the required status artifact. This optional-path discovery miss repeats existing inspect-before-use guidance.
