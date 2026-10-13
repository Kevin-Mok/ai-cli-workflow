# tmux session commit index reconciliation

Preserve the successful scoped commit and repair index reconciliation using an atomic rename on the Git filesystem. Then verify that unrelated staging and working files remain intact before pushing.

## Symptom, impact and evidence

The isolated-index commit succeeded as 8d2d0da (fix: make tmux scrolling and copying intuitive), with exactly16 reviewed session-owned paths. The subsequent os.replace of /tmp/tmux-commit-review-7x0cvba5/reconciled-index into /home/example/linux-config/.git/index failed with OSError18 Invalid cross-device link. The commit remains intact; no push attempted yet. The real index still reflects its pre-commit state. The script released its owned index.lock in finally.

## Lookup and diagnosis

Searched `Invalid cross-device link atomic rename index` before remediation. Top results concerned unrelated artifacts/ledger contracts, so no applicable reviewed remedy was found; diagnose this filesystem boundary directly. Source and destination are different filesystems; os.replace cannot cross that boundary. This is delivery-helper behavior, not tmux runtime behavior.

## Status and next steps

Repair verified. Verify the original index still matches its captured backup, guard concurrent writes, copy the prepared reconciled bytes to a temporary file inside .git, then atomically rename there. If the real index changed, inspect and rebuild reconciliation instead of overwriting it. Do not reset/amend/rebase the existing commit or alter unrelated work. Verify parent/scope and residual staging, record resolution/learning in a focused follow-up documentation commit, then push the complete series once.

## Resolution and verification

The real index matched the captured original bytes, so no concurrent staging was overwritten. Acquired an owned index.lock; copied prepared reconciliation bytes to a temporary file inside .git, flushed/fsynced it, retained index permissions and atomically replaced the index on the same filesystem. Verified same device, exact intended bytes, successful commit8d2d0da still at HEAD, and an empty staged diff. Released only the owned lock and temporary file. No history rewrite or working-file replacement.

Follow-up documentation/knowledge commit records this correction, preserves the original sixteen-file implementation and all other dirty work, and updates its matching plan. Root cause confirmed: cross-filesystem os.replace is invalid; generate the publication temporary file beside its destination. Remaining step: one configured origin/main push of the completed verified series. No tmux runtime regression or production session/history changes.
