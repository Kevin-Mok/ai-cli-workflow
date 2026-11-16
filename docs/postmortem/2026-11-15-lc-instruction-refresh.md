# lc instruction refresh blocked

The prompt shorthand is saved in the canonical source; live activation remains pending.

## Evidence and status

`fish -c refresh-config` exited 1: sandbox read-only errors prevented fnm,
Fish universal variables, alias generation and chezmoi state writes.
Live AGENTS also differs substantially from source; no wholesale overwrite attempted.
The canonical rule and admission entry remain saved. No retry performed.

Lookup: `refresh-config read-only file system` returned existing environment
and path-ownership findings. Existing restricted-environment guidance applies;
no new learning. Ledger inspection briefly assumed a `sources` key; actual
schema uses `reports`. No data was changed by that failed inspection.

## Next steps

Reconcile live/source instruction drift before refreshing outside this sandbox.
Diff checks verify source only; they do not prove live activation.

## Admission verification

Initial admission tests exceeded the ledger 20KB limit after the new entry.
Moved the detailed entry to a linked document, matching the existing ZIP entry.
Inventory check reports three existing calibration findings: stale builtin
openai-docs and missing agents/claude no-mistakes entries. No skills changed.

Final verification: all 7 admission tests pass after shortening the ledger link.
Commit-session README gate: pass_no_change. Live refresh remains pending.
