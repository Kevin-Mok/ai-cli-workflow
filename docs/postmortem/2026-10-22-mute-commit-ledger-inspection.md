# Mute commit ledger inspection

Record a read-only inspection error during session-only staging and the corrected schema lookup.

## Symptom and impact

A staging preparation script raised `KeyError: 'sources'` while looking up the current incident entry. Exit status was 1. It printed the actual top-level ledger keys before failing; no index or working-tree files were modified by that inspection.

## Cause and resolution

The ledger filename is sources.json, but reviewed report entries live under `reports`, not `sources`. Inspect the actual schema and select `reports` before extracting the session's entry. Build the staged ledger from HEAD plus only explicitly owned report entries, preserving unrelated dirty ledger edits.

## Verification and learning

The corrected lookup extracts the mute report from `reports`. Targeted checks initially reported unregistered live aliases after public placeholder normalization. Retain live aliases only in the unstaged working ledger, and stage public placeholder aliases for the same reviewed hashes. The exact candidate diff and privacy gate are checked before committing. No new reusable learning: inspect actual schema before assuming field names, and preserve unrelated mixed-file hunks. This is a staging preparation error, not a mute feature failure.
