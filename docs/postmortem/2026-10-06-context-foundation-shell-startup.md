# Context foundation shell startup failure

This report records a command-runner startup failure during private context implementation and the scoped workaround used to continue repository work.

## Symptom and impact

Initial status/source reads failed before shell execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. Two root calls and one delegated source read encountered the same infrastructure symptom; no repository command ran through that path.

## Evidence and lookup

Read the canonical postmortem-memory skill. Query `bwrap loopback Failed RTM_NEWADDR` matched local-sandbox-loopback-approved-route and ext-sandbox-loopback. Applicable because the wrapper failed before executing commands. Approved require_escalated status and source reads succeeded with exit 0.

## Status, cause and resolution

Verified workaround: use the approved host-shell route for the same authorized task scope. Underlying namespace policy is unchanged and unresolved; no host security settings were modified. Evidence supports runner startup failure, not an application defect.

## Verification and follow-up

Host-shell `pwd`, `git status --short`, source reads and memory search returned exit 0. Preserve normal sandbox diagnosis as separate work. No new reusable learning beyond the already reviewed workaround.
