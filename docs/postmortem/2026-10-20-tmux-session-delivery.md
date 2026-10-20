# Concurrent edits during tmux session delivery

Preserve the verified session commit and unrelated ongoing work when a post-commit preservation check observes another writer's changes. Verify the committed tree separately, record the boundary, and continue the authorized push without overwriting newer working bytes.

## Symptom and impact

The tmux commit succeeded, but the post-commit check returned1 because the unrelated state-security reference no longer matched its pre-commit hash. The push was gated off by that assertion. No commit or user work was discarded.

## Evidence and status

The commit tree and parent match the exact reviewed candidate. This session never edited state-security.md; its unrelated counter-reconciliation section changed concurrently. The assertion identifies changed bytes, not their cause. Treat preservation assertions on concurrently edited unrelated files as observations, not proof of an overwrite. Keep the latest bytes and do not restore the older snapshot.

## Next steps

Inspect the committed path set and clean index, preserve all unrelated work, record the existing concurrency lesson as no new learning, then complete the requested upstream push. Physical-desktop tmux acceptance remains pending independently of delivery.

## Resolution and reviewed learning

Query `concurrent protected working files commit scope` matched local-stale-preservation-baseline and local-skip-worktree-and-scoped-state. They apply directly: a hash change across concurrent work is not evidence of scope contamination. Exact tree/parent checks pass, the committed set contains exactly the12 reviewed tmux files, and the index is clean. Both unrelated reference and ledger changed while the original prompt remained identical. No restoration or implementation change is needed; retain the verified commit and current working files.

No new reusable learning: existing reviewed concurrency guidance covers this observational assertion. Record this report/hash with that explicit decision. The commit remains intact; the authorized push follows the short documentation milestone. No history rewrite, additional test rerun or unrelated staging is warranted.

## Push refused by an active hook

Both local commits succeeded with exact-candidate privacy PASS. The one requested `git push origin main` returned1: an active hook reported Privacy gate ERROR, inspection incomplete, operation refused; Git then reported failed push. Local commits35e9363/afb659c remain intact and the index is clean. Do not bypass the hook or report a successful push. Inspect the active pre-push path, scanner installation and scoped diagnostics before deciding whether a safe normal retry is possible.

## Upstream inspection and integration

The advertised upstream commit was not locally available. Fetching origin/main succeeds and the exact installed auditor command with full remote/local OIDs exits0 with zero findings. A diagnostic using symbolic revision names was rejected by its full-OID input contract and was corrected. The installed gate does support pre-push; its different version from tracked source is not proof of a broken invocation. No hook replacement is needed.

Upstream advanced with two already-published UI skill commits. A normal merge-tree preview is conflict-free. Because another session actively stages unrelated changes in the original checkout, integration moved to .worktrees/tmux-session-delivery on codex/tmux-session-delivery, based on afb659c. Six baseline routing tests pass; normal no-ff/no-commit merge succeeds and retains both histories. Only owned report/plan changes were transferred; original versions were restored without index changes.

The merged tracked privacy check passes. The installed check initially blocks one known upstream Angular empty-password form-control example because its policy snapshot lacks the upstream approval. Exact path/content/category/reason review confirms the sole new manifest entry is the already-published synthetic example approval. Synchronizing only that manifest entry makes the installed check pass; both hooks and all scanner/auditor executable bytes remain identical. No new exemption, blanket allowance, private rule change or hook bypass was introduced.

Final integration:36 tests pass in45.038s and both terminal shell regressions exit0 (/tmp/tmux-merge-tests.log). README gate returns pass_no_change. Existing fetch-before-ancestry, stale-preservation and exact-reviewed-approval guidance covers these boundaries; no new reusable finding is needed. Final merge commit and normal push follow the exact-candidate checks. Physical desktop acceptance remains pending.

Full merge-relative whitespace validation reports pre-existing trailing whitespace in the incoming pinned vendor design_system.py. Preserve upstream bytes and record this non-safety warning; the session diff relative to origin/main passes whitespace validation. No tmux implementation, privacy or regression check failed. This warning does not justify changing unrelated vendored code or withholding the eligible commit.

Automatic approval review rejected a combined canonical-hash/staging command because it also wrote into the original active checkout. No part of that command executed. Read-only proof then isolated this session's one owned report record; a separately approved compare-before-write update changed only its SHA field, preserving every other byte and the original index. Delivery staging stays in the isolated checkout. This applies existing ownership/concurrency guidance without bypassing the rejection.
