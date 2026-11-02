# Agent policy inspection triggered Fish startup writes

This report records why inspecting a Fish function emitted permission errors and why configuration activation remains pending.

- Symptom: `fish -c 'functions refresh-config'` loaded startup configuration, which attempted writes to fnm runtime links, universal variables and the aliases output outside the writable workspace. The outer command returned 0 despite those diagnostics.
- Impact: the requested two policy lines were added to tracked source; live activation was not performed. Existing source/live policy differences make a broad refresh unsafe without reconciliation.
- Evidence: stderr reported read-only filesystem errors and an aliases write traceback. A subsequent ledger inspection incorrectly assumed a `sources` key and raised KeyError; the actual ledger has `reports` and `findings`.
- Lookup: searched `fish startup read-only file system fnm aliases`; existing execution-environment and path-discovery guidance applies to inspection isolation, not evidence of activation.
- Root cause: using configured Fish for a read-only function inspection runs startup side effects; assuming a JSON key instead of inspecting its schema caused the secondary diagnostic failure.
- Resolution: read the tracked function directly and inspected ledger keys before recording this report. No live files or unrelated staged changes were intentionally changed.
- Verification: the two requested sentences occur exactly once in the canonical source; whitespace validation is recorded in task output. Runtime activation and UI outcomes remain unverified.
- Status and next steps: source edit complete; reconcile existing live/source drift before running refresh-config. Use `fish --no-config` for future isolated function inspection.
- Learning: no new learning; existing environment isolation and schema-discovery guidance covers these diagnostics. This report is recorded by hash in the tracked ledger.
