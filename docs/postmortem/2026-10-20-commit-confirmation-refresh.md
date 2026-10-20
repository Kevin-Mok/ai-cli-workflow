# Commit confirmation guidance refresh blocked

The AGENTS.md delivery rule was updated, but full configuration refresh remains blocked by unrelated local MIME association drift.

## Symptom and impact

The sandboxed `fish -c refresh-config` exited 1 because live home/runtime paths were read-only. An authorized elevated retry also exited 1: ChezMoi prompted about `.config/mimeapps.list` and received EOF. Full refresh did not complete; the tracked instruction change is intact.

## Evidence and lookup

Private refresh logs: `/tmp/refresh-config.8vbaleHu.log` and `/tmp/refresh-config.qsynaELP.log`. Query: `refresh-config chezmoi conflict`. Existing finding `local-mime-drift-reconcile` applies to the exact MIME conflict; `local-refresh-snapshot-ownership` supports preserving unrelated live/source divergence. No broad overwrite was attempted.

## Status and next steps

The AGENTS.md diff passes `git diff --check`. Preserve unrelated MIME settings; full refresh needs separate reconciliation. No new reusable learning: existing findings already describe this conflict and ownership boundary. A later commit-session request authorized committing and pushing the scoped guidance; delivery is recorded in docs/task-status.md.
