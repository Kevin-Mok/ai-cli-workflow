# Binary rendered-output verification caused migration rollback

The live migration reached configuration application and fresh fish refresh, then automatically restored the original checkout and settings after final output verification failed. Preserve retry-2 and its independent candidate, reproduce the binary-render mismatch with a synthetic repository, and correct expected-byte calculation before using a new recovery directory.

## Symptom, impact and evidence

Final verification reported `Live apply did not match the recorded intended output`. Retry-2 is `rolled_back`, its archive path is absent and its candidate is retained. Comparing recorded intended and applied states identifies exactly eight PNG skill-icon files differing only in SHA-256; no configuration values are included here. Fresh comparison of every journaled live backup against the restored machine found zero differences. All 48 old linked worktrees were restored by the recorded recovery path.

## Lookup and investigation

Lookup `migration intended live apply output mismatch shortcut` returned unrelated fixture/refresh guidance; none establishes a remedy for binary data. The suspected boundary is reconstructing expected file bytes from JSON text returned by `chezmoi dump`: invalid UTF-8 bytes cannot round-trip through a JSON string. Confirm this with a real installed-chezmoi fixture before changing code; retain complete output verification and rollback guards.

## Current status and next steps

Original configuration is restored; no successful cutover is claimed. A real installed-chezmoi synthetic fixture reproduced invalid-UTF-8 verification failure and refusal to roll back a changed binary whose intended bytes were wrong (RED). Expected bytes now come from raw `chezmoi cat` output whenever JSON contains a replacement character; complete output verification remains enabled. The same fixture passed apply, verify and restoration of differing original binary bytes (GREEN). Independent review caught a temporary variable collision affecting the private-config hash; an added assertion reproduced that mismatch and passed after the rendered bytes received their own variable.

Fresh focused checks passed 71 tests and refresh isolation. Read-only production rehearsal verified all eight intended PNG hashes against source bytes and completed rendering/shortcut preparation. Lookup `binary UTF8 chezmoi dump expected bytes` found no applicable binary-specific finding. Register this new code-level finding and reviewed report in the canonical private ledger; live retry remains unverified. Preserve retry-2 and use unused retry-3 for the guarded retry.

## Historical attempt boundary

This report records its specific attempt, not the latest checkout state. The
later cutover completed; current state and read-only follow-up are recorded in
[the migration plan](../../plans/migrate-sanitized-repo.md#current-state-completed).
Preserve prior journals privately and do not rerun these historical next steps.
