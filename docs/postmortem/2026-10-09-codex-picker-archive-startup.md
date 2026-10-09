# Codex picker startup blocked by archive indexing

This records the reported failure where crg prints malformed-record warnings
instead of reaching its UI. Reproduce startup with invented slow/broken archive
sources, open from available metadata promptly, and verify background refresh
without letting diagnostics cover the terminal picker.

## Symptom and evidence

The user supplied a screenshot of many per-source `skipped 1 malformed/incomplete
records` warnings from older session logs and reported that the UI never opens.
The original CLI ran full `refresh` under the index lock before
calling fzf. Refresh walks and parses the archive and warns for every source with
skipped records, including unchanged cached entries. The background watcher uses
the same warning path while fzf owns the terminal.

## Lookup and applicability

Query `codex-search malformed incomplete records picker startup index` matched
local-codex-search-json-boundary and local-fzf-ui-stream-and-resume-fixture.
The former verifies skipping invalid records beside good data; the latter verifies
UI stream visibility and exact resume. Neither proves bounded first UI latency
with a large archive, nor prevents repeated watcher warnings. Preserve both
contracts while creating a defining delayed-archive reproducer.

## Status and next steps

Confirmed foreground full-index dependency and repeated warning emission.
The defining cold/cached-lock/render tests observed RED, and a separate watcher
test reproduced the repeated warning flood. Five startup/header/preview/watcher
checks now pass in 1.484s; 16 index-helper and 43 recap regressions pass separately.
Final full regressions and installed activation are verified below.

Recent picker startup reads available cached metadata without taking the archive
lock, or bounded native headers on a cold cache. Provisional dialogue stays
explicitly pending; recap inference waits for validated data. The watcher updates
in 20-source passes with a between-source one-second budget, releases the lock
between passes, and writes diagnostics into a private disposable log. Default UI
progress and one concise accuracy notice replace the terminal warning flood;
--details exposes a bounded diagnostic tail. Source history remains read-only.
Independent review caught recap deletion maintenance on incomplete scans; it now
waits until the source inventory is complete and no files remain pending.

One oversized file can exceed the pass budget after the picker has opened.
Metadata-only cold activity is preliminary until parsing completes. Ordinary
text search and an explicit --rebuild-index still perform their complete scan.
Prior priority/UUID/worker cleanup and all unrelated dirty work are preserved.

## Verification fixture failures

The first actual-UI fixture attempt used an unsupported --json flag to warm the
cache. The production CLI correctly rejected it; the fixture now uses supported
--recent --plain plus the private manifest to validate warm state.
The first complete search run passed all existing checks but failed its newly
created live-startup fixture during a single unguarded fzf listener read inside
selection: TimeoutError after cold UI opened. The existing fzf fixture guidance
applies to listener synchronization and exact identity assertions, not a weakened
UI deadline. Move that read into the existing bounded polling helper, retain the
exact UUID/cwd assertion, then rerun actual UI and the complete suite. Current
observed broader run: 151 tests, 92.447s, one fixture failure; completion unclaimed.

Read-only preparation commands guessed an obsolete refresh helper filename and
a non-template Git config filename; both reported file missing and changed no
files. The repo inventory and `chezmoi source-path` resolved the actual function
and dot_gitconfig.tmpl before installation. Use those mappings instead of assumed
names; no additional reusable failure pattern beyond existing path guidance.

An abbreviation source lookup likewise assumed non-template fish filenames;
the inventory resolved config.fish.tmpl. A final report patch referenced a removed
line and was rejected atomically, changing no files; fresh plan/report reads
supplied the current context. These read/patch preparation failures caused no
product change and add no separate finding beyond inventory/context guidance.

The next broader run passed 157 checks but failed the existing synthetic
Guardian-progress fixture: the fzf list became a blank row before its elapsed
generation badge could tick (158 tests, 88.230s, one failure). Investigation is
checking the newly enabled missing-directory watcher against fixtures with
invented manager entries and no native source files. Do not weaken the visible
badge, query/UUID or missing-directory recovery assertions; reproduce the exact
progress phase and distinguish synthetic source ownership from actual empty
archive behavior before changing code or fixture setup.

The Guardian-progress root cause was fixture ownership: its real manager exposed
a home with no native sources/titles, so the new watcher correctly replaced the
invented list with an empty archive. Build consistent native records, index and
title metadata in that phase. Its exact reproducer now passes the 1s badge,
queued position, query, UUID, Ctrl-G and cleanup assertions.

Installed startup checks pass all five phases (0.620–1.076s); the user's actual
native picker shows 199 usable rows in 1.968s and Escape cleans up without recap
generation or resume. Refresh preserved 1,540 repo files, three live configs and
installed all six source-identical modules. The next complete run passed those
new checks and Guardian-progress but hit the older priority fixture's identical
unguarded GET-selection timeout in its cached phase (160 tests, 85.771s, one
failure). Apply the same bounded listener-read and observe-without-replay rule,
preserving actual priority/UUID/cached-generation assertions, then rerun.

## Learning

Reviewed finding local-picker-metadata-first-readiness is verified_fix with runtime
scope and confirmed cause. The tracked ledger links the current report hash to
its API/fixture reference section; tasks/lessons.md records the repo lesson.

## Final resolution and verification

Resolved and installed. All 160 Codex search tests pass in 88.946s (exit 0),
including startup, malformed/discovery recovery, pending/manual recap behavior,
Guardian priority updates, query/UUID preservation, progress and cancellation.
The exact Guardian progress reproducer and corrected actual priority fixture also
pass separately. Prior unsuccessful fixture attempts remain above as evidence;
their assertions were retained rather than relaxed.

Required refresh-config completed successfully with exact search-script targets.
All six installed modules match source; 1,540 repo files and three live configs
kept their pre-refresh hashes. Installed actual CLI/real-fzf startup phases pass
in 0.620–1.076s; native history displays 199 usable rows in 1.968s and Escape cleans
up without inference/resume. README gate passes and task-scoped whitespace is clean.
Limits are preliminary metadata and soft between-source budgets documented above;
provider inference is covered synthetically, not invoked on private history.
No commit/push or worktree; protected unrelated changes remain intact.

A daemon restart discarded the last exec handle (unknown process id on recovery).
The repository and all six installed modules retained their verified hashes; no
prior verification PID remained. Repeat only that installed Guardian check:
live append/rename, cached priority and newest-first modes all pass with exact
UUID/cwd resume and cleanup. All recent-picker PTY modes also pass after cosmetic
emoji progress updates. These checks use synthetic inference and make no provider
calls. The lost handle was recovery state, not evidence of a product failure.
