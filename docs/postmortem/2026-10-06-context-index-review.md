# Context index review and source lookup

This report records review findings and a failed helper-path lookup during private project index implementation. Fixes are verified with synthetic data; no private source contents belong in this report.

## Symptoms and impact

Review found that deleted source projects retained current-looking summaries; a root-ancestor substitution could escape read-only source containment; absent stores with an existing directory initialized cache/lock files; forgetting a technical finding retained the same pattern in project summaries. Mode drift also prevented safe cache erasure or unchanged-store privacy repair. These were reproduced deliberately with synthetic tests before changes.

Separately, a delegated read-only rg check guessed nonexistent scripts/project_store.py and exited 2. It changed no files or private data. Correct bundled modules are inventoried with rg --files before reads.

## Lookup and applicability

For the guessed path, query `rg No such file or directory guessed path` matched local-discover-paths-before-reads, a verified workaround directly applicable to the guessed suffix. No new general learning beyond that existing guidance.

For source traversal, query `symlink ancestor race O_NOFOLLOW` matched local-clean-install-parent-transaction: related descriptor-relative traversal technique, activation_pending/code, different destination workflow. Current read-only defect was reproduced independently; do not promote that prior finding's activation state.

## Resolution and current status

Availability reconciliation retains qualified historical evidence with explicit unavailable scope, excludes unavailable projects from current recurring findings, and supports targeted missing-project refresh. Source opening walks descriptors from `/` with O_NOFOLLOW for each ancestor. Missing authoritative stores return empty projections without creating cache or lock. Forget suppression removes technical patterns and observations from project records and projections. Authorized writes repair safely owned private modes; failed forgetting cleanup is reported rather than silently accepted.

User narrowed scope to committed contributions by example-user Mok. Initial unqualified derived records were purged privately. Authored-source tests pass; actual foundation now contains 97 qualified projects and 1,048 source records. Sampled 14 sources match current committed bytes, latest author and recorded hashes.

## Verification and follow-up

Synthetic deleted-project and mode-drift checks observed RED then GREEN; source ancestor-race check observed RED then GREEN. Integrated authored-source suite passed 58 tests; additional bounded-history check is included in the final run. Preserve these executable regressions and safe metadata evidence in the active plan. Original project sources and personal Markdown remain unchanged.

## Installation validation

After a successful refresh-config, installed-file comparison returned false while implicit metadata was enabled. Only project_sources.py differed because source implementation finished after the first refresh. Final refresh-config succeeded; all six installed files match the finalized package and implicit metadata is enabled. Lookup `installed skill new module missing after refresh` returned installer/current-source guidance without a closer direct remedy; actual comparison established the stale installation. No personal contents were printed. A broad recursive mode check also reported false because it included three pre-existing unmanaged auxiliary files. All five managed file/directory modes and the ai-context directory pass 0600/0700; unrelated sources were preserved.
