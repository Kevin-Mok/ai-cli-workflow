# cg shortcut helper path inspection

A read-only helper inspection assumed sync-shortcuts was a Fish function. Discover the actual script path before reading it; no video command was executed.

- Symptom/evidence: cat of dot_config/fish/functions/sync-shortcuts.fish exited 1 because that file does not exist.
- Impact: inspection only; no tracked or installed configuration was modified by the failed read.
- Lookup: query `sync-shortcuts missing path fish inspection` matched `local-discover-paths-before-reads`, verified_workaround. It applies because the inspection guessed a helper suffix.
- Root cause: sync-shortcuts is an external script, not an autoload Fish function.
- Resolution/verification: rg --files located scripts/executable_sync-shortcuts; its complete source was read successfully.
- Status: resolved inspection error; shortcut deployment remains separate.
- Follow-up/learning: no new reusable learning; the existing path-inventory finding already covers this exact failure mode. Avoid guessed helper paths.
