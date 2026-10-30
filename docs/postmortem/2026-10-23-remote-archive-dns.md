# Remote archive deletion: restricted DNS

The first remote listing could not resolve GitHub. This report records the execution restriction and successful permitted retry.

- Symptom: `git ls-remote --heads origin` exited 128 with `Could not resolve hostname github.com: Temporary failure in name resolution` in restricted execution.
- Impact: Initial inventory blocked; no remote mutation occurred in that attempt.
- Lookup: Read postmortem-memory; queried `github.com Temporary failure in name resolution`. Results included unrelated Supabase endpoint guidance; that provider-specific remedy does not apply.
- Evidence and cause: The identical listing succeeded with permitted network execution, supporting an execution-environment restriction rather than a repository access defect.
- Resolution: Used permitted network execution. Atomic push deleted public-archive/snapshot-01 through snapshot-17 and the privacy gate passed.
- Verification: Fresh remote listing returned exactly the same four nonarchive branches and SHAs as before deletion, with zero archive branches.
- Status: Resolved; verified workaround for restricted execution, not a change to DNS configuration.
- Learning: No new reusable guidance; use normal permission escalation for a required network operation. Existing provider-specific findings are not evidence for this environment.
- Next steps: None for branch deletion.
