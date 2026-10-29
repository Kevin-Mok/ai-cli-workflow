# Public portfolio prerequisite pre-push inspection

This report records the failed shared-repository push and safe recovery. The academic portfolio branch was published independently; the shared fix uses a separate clean worktree to preserve concurrent remote changes and unrelated dirty local work.

## Symptom and impact

On 2026-10-29, the shared main push was refused with privacy-gate inspection incomplete. Local commits 72b1d33 and 286566c remained intact. Portfolio commit c9266ee was successfully published on feat/academics, with the existing resume hook intact. GitHub redirected the former portfolio repository location to nextjs-portfolio-showcase.

## Evidence and lookup

The shared remote advertised 911b869 while the local tracking ref was still bd39cd1. A Git object-availability probe confirmed that the advertised remote commit was absent locally. The privacy pre-push implementation requires that object when enumerating outgoing commits, so the stale local view prevented inspection. The canonical lookup returned local-git-fetch-before-ancestry and local-gate-public-metadata-defaults; their guidance was read before recovery.

## Root cause and resolution

An authorized fetch retrieved the missing object. Both ancestry checks then correctly returned false: local and remote main had diverged. Repeating the same pre-push inspection after fetching exited 0, recorded in /tmp/academics-checks/privacy-fetch-diagnostic.log. This establishes recovery of the inspection, not a successful main push.

To preserve unrelated dirty canonical files and avoid bundling concurrent skill additions, a clean fix/public-portfolio-privacy worktree was created from the two local scoped commits. It normally merged the already-published upstream commit 98e2aaf, which fixes new-branch inspection to exclude history already on remote-tracking refs. No histories were rewritten; no checks or hooks were bypassed. The existing shared hook snapshot was refreshed from this integrated source, retaining its prior hook protocol.

## Verification and publication status

The merged pre-commit privacy suite passes all 60 tests, including exact public approval, changed-byte revocation, private/secret rejection, the new-branch boundary, and unsafe non-tip outgoing ancestry. The immutable-tree integration also passes. Logs with exit statuses are /tmp/academics-checks/privacy-merged-precommit.log and privacy-merged-checkpoint.log. A final exact-candidate check is required before the normal integration commit and branch push. Actual push receipt is reported in Codex output; do not infer a main deployment from the diagnostic PASS.

## Follow-up and learning

Fetch the authorized remote branch before ancestry/outgoing-object inspection when advertised hashes are unavailable locally. Preserve dirty work through a separate worktree for integration, and publish a reviewed branch when concurrent unrelated main updates make direct publication inappropriate. This applies existing reviewed fetch-first and hook-protocol guidance; it adds no new general remedy. Register the current report hash and targeted check with the canonical ledger. Keep all other dirty source, docs and learning entries outside this scoped integration.
