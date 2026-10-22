# Proficiency evidence discovery checks

This report explains two read-only discovery problems encountered while preparing
an AI workflow assessment. Resolve helper paths from the installed inventory,
verify network access through normal approval, and separate public source access
from authenticated repository metadata before publishing evidence.

## Symptom and impact

During planning, a guessed helper filename was absent, and sandboxed GitHub
metadata reads returned `error connecting to api.github.com`. Web fetches of
GitHub pages also returned cache misses. These checks did not modify application
state; public visibility and source accessibility remained unverified.

Plan Mode prohibited writing this report at the time. It is recorded during the
authorized implementation phase, retaining that limitation rather than claiming
immediate recording in planning.

## Lookup and evidence

- Lookup: `helper script No such file path discovery`. The reviewed
  `ext-optional-path-discovery` finding applies: use observed inventory rather
  than assumed optional entrypoints. Reading the installed directory identified
  the actual helper; its subsequent read-only retrieval exited 0.
- Lookup: `error connecting api.github.com`. Broad matches did not establish
  GitHub reachability or repository visibility. No prior remedy was treated as
  proof of current access.
- Four sandboxed repository metadata checks exited 1 during planning. They
  established a connectivity limitation, not repository absence or privacy.
- During implementation, normal approved read-only metadata requests exited 0.
  They distinguished public evidence candidates from a private project.
- Web cache misses remain inconclusive about anonymous source accessibility;
  verify public source bytes separately before using a headline receipt.

## Cause, resolution and current status

Helper lookup used an assumed filename instead of the installed inventory.
The corrected path is verified. Network requests succeeded through approved
execution; the evidence supports an access-path workaround, not a diagnosed
GitHub outage. No permission controls were disabled.

Status: **verified workaround** for read-only discovery. Public source content
verification belongs to the assessment's separate evidence register. No
production behavior, credentials, repository visibility or remote refs changed.

## Follow-up and learning

Keep raw retrieval output private and use immutable, anonymously accessible
sources for public claims. No new durable learning: optional-path discovery and
the separation of failed access from destination state are existing guidance.
Register this report's reviewed hash with that explicit no-new-learning decision
and run the targeted postmortem-memory check.

## Rendered-document verification follow-up

The temporary Markdown render succeeded. Starting a separate browser review
session then returned `BRIDGE_NOT_READY` after its 30-second startup deadline,
before any page or screenshot was obtained. Existing user pages were untouched.
Lookup for `BRIDGE_NOT_READY bridge startup timeout` and a broader browser-startup
query returned application findings with historical browser limitations, not a
verified startup remedy. They were not applied as fixes. The installed bridge
entrypoint was absent and its path override unset; this does not establish the
precise cause of the startup timeout. The alternate browser-surface inventory
was empty.

Resolution: installed headless Chrome rendered the temporary local HTML using
an explicit task-owned temporary profile. README, receipts-section and assessment
screenshots were written successfully and visually inspected. The source Markdown
rendered with readable tables and adjacent estimate qualifications. No dependency
installation, user-profile change, application interaction or security bypass was
needed. Stopping the task's failed bridge session returned `stopped (no-op)`.
This verifies static documentation rendering through a fallback, not repair of
the original bridge or live application acceptance.

The temporary link checker also initially reported a false missing anchor due
to its own parsing logic. The checker was corrected and its final run passed;
no source Markdown was changed to satisfy that false result. Record the final
checker evidence separately from the initially unsuccessful diagnostic.

Final learning decision: no new durable finding. Observed entrypoint discovery,
scope-limited fallback verification and keeping recorded evidence distinct from
fresh checks are already established practices. The original bridge startup
remains unresolved; the documentation verification workaround is verified.

A final plan-bookkeeping patch also failed its context check because it included
an unnecessary stale context line. The patch was rejected before modifying the
plan. Re-read the current text and apply only the intended checkbox and review
status edits; this does not invalidate the already-passing artifact checks.

Lookup `patch context stale line rejected` matched `local-stale-patch-context`.
The current plan still had both pending entries, confirming this failed patch
had not applied them. Its narrow replacement succeeded. This is existing
guidance, with no new durable finding; run the focused document and whitespace
checks again after the corrected bookkeeping and reviewed-hash update.

## Commit-phase shell lookup

A read-only command lookup launched configured fish. Its startup attempted
runtime symlink, universal-variable and generated-alias writes outside the
sandbox, printing read-only-filesystem diagnostics even though the lookup itself
returned the executable and exit 0. Do not treat that exit status as a clean
startup check. No configuration repair or refresh is needed for this docs-only
delivery; use a configuration-free lookup and preserve the live shell setup.
Record the matching reviewed guidance and final check before committing.

Lookup `fish fnm multishell read-only startup` returned remote-shell guidance;
that remedy is not directly applicable to this local lookup. A subsequent
`fish --no-config` lookup returned the same executable with exit 0 and no startup
diagnostics. No new durable learning: avoid loading unrelated startup side
effects for a command-availability check and inspect diagnostics, not just exit
status. This is a scoped verification workaround, not a live-shell fix.

The first temporary candidate-verification invocation also had malformed shell
expansion and called `git write-tree` against the normal index. The read-only
filesystem refused the object write; index and working-file comparisons showed
no change. Explicit isolated-index environment handling then verified the intended
candidate successfully. Keep this diagnostic failure separate from the later
passing candidate check; do not use shell expansion to construct Git arguments.

Lookup `shell expansion command substitution git write-tree` returned generic
sandbox-route guidance, which does not diagnose this quoting error. Explicit
argument/environment construction and unchanged-index comparison supply the
actual evidence. No new durable finding is needed for this temporary verifier.
