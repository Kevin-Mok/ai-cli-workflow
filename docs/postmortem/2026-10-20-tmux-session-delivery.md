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
