# Migration refused a changed preparation fingerprint

The retry stopped before cutover because the active-checkout fingerprint differed after preparation. Preserve both failed recovery directories, reproduce metadata-only differences separately from material changes, and retain strict concurrency protection.

## Observed state

Retry journal is `rolled_back`, no archive exists, and no live-start marker is set. Transfer and render preflight passed. No HEAD reflog events occurred near the clone-to-refusal window. A separate commit/push task remained active in the shared checkout. Initial fingerprint was not saved in the journal, so the exact field that differed in this attempt is unknown; do not claim harmless metadata was its proven cause.

## Lookup and investigation

Query `Git index stat refresh concurrent migration fingerprint` returned shared-index race and index-publication guidance. Apply the advice to preserve staged work, but no prior remedy establishes this attempt’s cause. The current guard hashes raw index bytes, including refreshable stat cache data. Define a synthetic cache-refresh-only reproducer and material-staging control before changing it. Add private initial/difference evidence and content-free `--details` counts so a future refusal is diagnosable.

## Status

Investigation open; no live retry launched. Preserve the guard against changed HEAD, indexed blobs/modes/flags, working-file bytes/modes, ignored entries, and linked worktrees. No archive deletion, reset, commit, push, or forced cutover authorized.

## Findings and code changes

A synthetic actual-apply reproducer confirmed that refreshing only Git’s index stat cache caused the same refusal with unchanged file bytes and unchanged staged content (RED). The fingerprint now uses indexed modes/object IDs/stages, assume-unchanged/skip-worktree tags, cached diff (including intent-to-add distinction), and resolve-undo metadata. It ignores only cache representation. The physical old index is still preserved by archiving, never reconstructed. Independent primary-document review identified resolve-undo as an important control, and a RED regression caught its omission before adding it.

New private journals save the initial checkout fingerprint and changed-path lists (fingerprints only, no file contents). `--details` prints category/count diagnostics without path values or config content. Dry-run now checks the active checkout again after inventory and refuses material changes without creating a journal. Existing file/head/staging/ignored/worktree checks remain in force.

A read-only live observation around the same history-audit phase subsequently detected real HEAD, index-entry and worktree-registration changes. Evidence is private `/tmp/migration-current-readiness.json`. This proves current concurrent activity, not the exact cause of the earlier attempt, whose initial snapshot was unavailable. Do not bypass the refusal or rerun live apply until other root sessions finish.

## Verification and limits

40 migration tests, 19 config-snapshot tests and 9 fish-output tests pass (68 total). Controls cover staging-only changes, assume-unchanged, intent-to-add, resolve-undo, working-file changes and no-write dry-run. Refresh shell check passed. A broader focused run had one known network-dependent failure: real timer chezmoi fixture evaluated the upstream release template without network; migration-specific offline handling is separately covered. No live retry was run and neither failed directory was changed. Both attempts remain rolled back, with no archive and no live-start marker.

Sources: Git’s official ls-files, diff and index-format documentation; independent reviewer confirmed the semantic entries and resolve-undo behavior in disposable fixtures. Code verification does not establish a successful live migration. The old attempt’s exact changed fields remain unknown.

## Historical attempt boundary

This report records its specific attempt, not the latest checkout state. The
later cutover completed; current state and read-only follow-up are recorded in
[the migration plan](../../plans/migrate-sanitized-repo.md#current-state-completed).
Preserve prior journals privately and do not rerun these historical next steps.
