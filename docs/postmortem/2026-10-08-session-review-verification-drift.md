# Recent session review verification source drift

Recheck source identity when a verified suite suddenly reports the old CLI contract. Preserve both versions and reapply only the authorized changes if the working file exactly matches the captured baseline.

## Symptom and impact
After 77 session tests passed, `scripts/second_brain/sessions.py` reverted byte-for-byte to the initial v2 baseline (SHA-256 `48eac1364adb81b6f22d2fe19fdfe4da7d6bfdabe780da0834edaee120800653`). Its modification time was 12:54:15 Toronto. The subsequent 328-test broader run had 11 failures and 9 errors, including missing new review arguments, plus the known unrelated vault-inventory failure. CLI activation is paused pending restored-source verification.

The native task-title tool also became unavailable with a transport failure to its local MCP endpoint. The last successfully set title remains `Improve recent session reviews`; title activity does not control repository work.

## Lookup and evidence
`concurrent source overwrite changed file` matched `local-stale-preservation-baseline` and `local-deployable-file-set-verification`. Read-only comparison established the working file exactly equals the initial captured source and the old installed module; other changed CLI modules remain intact. The independent reviewer confirmed its reproducers only imported the baseline in memory and wrote disposable fixtures. No writer has been identified; do not attribute this to tests or another user without evidence.

`thread title tool connection refused transport` produced no matching transport remedy. No transport retry or host change is required to continue the authorized task.

## Resolution, verification and remaining limits
The reverted file exactly matched the preserved baseline, so only this task's recorded implementation was reapplied. The session suite then passed 77 tests and the broader suite passed 327 of 328 (only the known vault-inventory failure). A before/after SHA-256 guard confirmed the source stayed unchanged throughout that full run. Later ASCII-mode tests raised the session total to 79, all passing; installed fixture checks also pass. Rollback copies were saved before scoped CLI installation.

Source-drift cause remains unresolved; no other file was reset or attributed to a writer. The native title transport remains unavailable; continue using the last saved title rather than modifying another conversation or host settings.

During the later schema-runtime installation guard, the installed runtime no longer matched its pre-change snapshot. Direct byte comparison showed it already exactly matched the newly verified source. The guard made no writes; source-equivalent installed content was accepted, and a baseline rollback copy was saved. This provides further evidence of concurrent synchronization, without identifying its writer. No unrelated installed content was overwritten.
