# Upstream merge refresh stopped on local MIME edits

The required refresh after merging upstream stopped to protect existing desktop file associations.

- Symptom: refresh-config exited 1; chezmoi reported .config/mimeapps.list changed since its last write and reached EOF at its overwrite prompt.
- Impact: full configuration activation is incomplete. Merge content remains staged; no overwrite decision was supplied.
- Evidence: /tmp/refresh-config.1SClwPka.log and wrapper exit 1. Do not assume the apply is atomic or other targets unchanged.
- Lookup: searched refresh-config chezmoi local differences; existing local-drift guidance applies. Prior concat plan also records unrelated mimeapps conflicts.
- Root cause: unmanaged local drift requires an explicit reconciliation decision; noninteractive refresh cannot answer it.
- Status: activation_pending. Preserve live file associations and deliver independently verified Git integration. No blind retry or force overwrite.
- Next steps: reconcile live/source MIME associations separately when requested, then rerun refresh-config.
- Learning: no new reusable finding; existing preserve-local-drift guidance covers this outcome. Git merge success does not establish activation.
