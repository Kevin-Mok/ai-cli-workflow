# Installed memory verification counted an excluded Python cache

The scoped skill deployment succeeded, but the source/live comparator included a generated Python cache that is intentionally not deployed. Compare only deployable artifacts, then verify exact installed content and preserve protected settings.

## Symptom and impact

The post-apply assertion listed `scripts/__pycache__/postmortem_memory.cpython-312.pyc` as missing from the installation. The verification stopped before creating the new Claude link. No config snapshot or broad apply occurred.

## Evidence and current status

An earlier import-based discovery generated the source cache. The checked source directory is new task-owned content; Python caches are local generated output. Deployment itself exited 0. Corrected package/link/installed-layout verification passed after preserving concurrent learning.

## Root cause and resolution

The comparator walked all files instead of matching the deployable file set. Confirm chezmoi cache exclusions and filter generated caches from source/live comparison, retaining exact equality for every intended package file.

## Verification and next steps

Search shared memory before retrying verification; rerun the corrected comparator, installed-layout search and protected-byte assertions. Add the result to this report and tracked knowledge, then reapply only the updated skill.

The first corrected comparator also detected a real source/installed content mismatch and stopped before link creation. The subsequent targeted check correctly rejected this still-unregistered living report; neither result proves deployment complete. Inspect the exact mismatch before another apply and record both diagnoses here.

Mismatch diagnosis: only sources.json differs. A concurrent task appended its own reviewed kitty inspection report and serialized an existing Unicode dash literally. This is legitimate new tracked learning, not evidence that the apply corrupted content. Lookup `concurrent source installed bytes` identifies the scoped-state/stale-preservation findings; preserve the new entry, validate its current source hash and synchronize the latest knowledge. Source comparisons must account for the deployment boundary and concurrent writers.

A later comparator reached the protected-byte assertion after package/policy equality and Claude link creation, then detected a changed long-lived protected baseline. The scoped apply excluded scripts and never selected config snapshots or unrelated source files. Treat this as concurrent-state evidence, not permission to restore stale source bytes. Preserve current content, inspect changed path names, and verify exact mutation-boundary hashes for the final owned apply.

Resolution: exact equality now passes for all 13 deployable source/installed files and the owned Claude link; installed-layout lookup succeeds from /tmp. Excluded generated caches are not deployment defects. The changed long-lived Codex source baseline is retained as current unrelated work; this task ran no config snapshot, broad apply, or source-config write. The isolated refresh regression uses temporary HOME and TEST_CODEX_TARGET, not the real source. Verify fresh protected hashes immediately around the final exact-target apply rather than asserting a stale cross-task baseline.
