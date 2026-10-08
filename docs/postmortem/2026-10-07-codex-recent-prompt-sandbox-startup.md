# Recent-session prompt sandbox startup failure

Repository reads failed before shell execution. Use the approved scoped execution route to save the supplied prompt; leave host sandbox repair to a separate task.

- Date: 2026-10-07.
- Symptom: Two initial read-only commands exited 1 with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` and no command-body output.
- Impact: Context retrieval was delayed; neither failed command changed files.
- Lookup: `bwrap loopback Failed RTM_NEWADDR` matched `local-sandbox-loopback-approved-route` (verified_workaround), in `references/execution-environments.md`. The startup error and absence of command output establish applicability. Approved retrieval reads were prerequisites to this lookup.
- Evidence: Approved scoped repository-status and skill reads returned exit 0. Initial dirty state was captured before writes.
- Root cause: The wrapper could not configure loopback; underlying host restrictions were not investigated.
- Resolution/current status: Approved scoped execution unblocks prompt authoring. Default sandbox startup remains unresolved.
- Verification: Repository status, canonical instructions, source contracts, and matching incident guidance were read successfully through the fallback.
- Next steps/follow-up: Preserve unrelated dirty work, save and verify the supplied prompt, and investigate sandbox startup separately. No tool implementation, configuration repair, commit, or push is authorized by the prompt-authoring scope.
- Learning: No new reusable lesson beyond `local-sandbox-loopback-approved-route`; register this report with that explicit no-new-learning decision and run its targeted ledger check.
