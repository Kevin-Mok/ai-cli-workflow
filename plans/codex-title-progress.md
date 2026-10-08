# Visible progress for missing Codex titles

Show live queue position and elapsed time beside Guardian review and untitled
rows, then replace their generic title with the AI headline when it is available.

## Context and decisions

The picker already refreshes recap status through authenticated local fzf.
SummaryManager has a serial queue and one attempt per UUID per opening. Generic
rows currently show no visible wait activity and only Guardian adopts headlines.
User requested percentage/time progress for Guardian and untitled titles. Total
provider work is unknown: use actual phase elapsed time and queue position,
without inventing percent complete or an ETA. Keep generation policy, exact
UUID/directory resume and meaningful native titles unchanged. No new model calls
are needed for development checks. Default mode has no mode-switch tool.

## Scope and protected state

scripts/codex_search_recaps.py: transient monotonic queue/generation clocks.
scripts/codex_search_recent.py: generic title detection and compact progress.
Tests cover the real manager and real fzf reload path with local runtimes.
README, operator guide and shared smoke checks describe final behavior.
Initial git status captured; unrelated dirty files and prior Guardian title work
must remain intact. No configuration changes or worktrees. The subsequent
$commit-session request authorizes scoped commit and upstream push.

## Atomic checklist

- [x] Read queue/render code, relevant docs, feedback/lessons and required skills.
- [x] Present bounded design: queued position, elapsed time and untitled adoption.
- [x] Observe defining queue/timing/render tests RED.
- [x] Add phase clocks and compact placeholder badges with minimum changes.
- [x] Exercise live ticks, queued-to-generating-to-headline, exact resume and cleanup.
- [x] Update docs and independently review concurrency/selection behavior.
- [x] Run focused/full search regression, install exact modules and verify them.
- [x] Record final evidence and limitations.

## Risks and rollback

Clock metadata stays ephemeral, uses monotonic time, and is integer seconds to
avoid excessive reloads. Waiting position excludes the active request. Manual
reprioritization preserves total queue wait; generation begins a fresh timer.
Ready/failed/disabled states omit active progress. Another picker's timer only
measures observed activity, not its unknown original start. Generic-title query
re-filtering remains normal. Roll back only task hunks and reapply exact modules.

## Verification and handoff

Automated from /home/example/linux-config, no sudo:
python3 -m unittest discover -s tests -p 'test_codex_search*.py'
python3 tests/scripts/codex_recent_live_check.py
Manual: reopen crg once, filter by directory, select an uncached Guardian/untitled
row and Ctrl-G; see queued position/wait time, then generating elapsed time
advance, then its AI headline replace the badge. Missing outside the batch has
no active timer and shows Ctrl-G; disabled rows show recaps off, and failed rows
show unavailable. Cached/disabled views do not pretend to be generating.

Cursor prompt: Review plans/codex-title-progress.md and the final title-progress
changes, preserve unrelated work, run its full search and live terminal checks,
confirm exact UUID resume and timer cleanup, and include this plan plus related
docs in any subsequently requested feature commit.
Suggested commit: feat(codex): show title generation progress.

## Progress, evidence and review

Independent design review: snapshot queue/state/timestamps under the condition
lock; derive current queue position, preserve wait start on reprioritization,
suppress progress for ready/failed states, and clean timers on halt/close. Keep
existing generating transition after lock acquisition to avoid phantom activity.


Defining RED observed for queued status (missing instead), absent progress badges,
untitled headline adoption, and stopped generating metadata. Idle/off/failure
hints also observed RED before implementation. Focused manager/picker checks
passed. Real-manager terminal checks show a visible 1s tick, queued position/wait,
a fresh 0s generating timer, then AI title with exact UUID resume.

Initial broader run: 97 tests with one descendant-state observation race. Recorded
and repaired its fixture with bounded kernel-exit observation while retaining
strict leader/child shutdown checks. Final broader run: 98 tests in 37.099s, exit0.
Independent final review: no blocking findings. Changes remain ASCII and transient;
JSON/ordinary recent listing format and generation policy remain unchanged.

Unexpected patch-context rejection and descendant observation race have living
reports; their reviewed learning/checks remain part of this task. User interrupted
then resumed; resumed status captured at /tmp/codex-title-progress-resumed-status.txt.


Final activation: chezmoi apply --force -- /home/example/scripts/codex_search_recent.py
/home/example/scripts/codex_search_recaps.py exited0. Both installed modules match
source bytes. The full recent live fixture imported both installed modules and
passed visible timers, queue transitions, untitled title adoption, exact resume,
cancellation and worker cleanup, exit0; no provider calls were made.

Both unexpected-incident reports are registered at their current reviewed hashes.
Targeted postmortem checks exited0 with no errors; git diff --check exited0.
README, operator guide and shared smoke checks describe the final behavior.
No configuration changed, broad refresh, commit or push was performed. Existing
pickers need one reopen to load the new modules; subsequent timers/titles update
live. Manual CLI generation uses the existing newest-session window and model;
unknown progress is shown as phase/elapsed time rather than percentage or ETA.

## Delivery milestones and current overview

1. Prerequisite ae2e3aa shipped compact Toronto timestamps, abbreviated directories
   and recent-picker layout in this conversation; it was already pushed.
2. feat(codex): show title generation progress ships the live Guardian/untitled AI
   titles, queue position/wait time, generating timers and idle/off/failure hints,
   with regression fixtures, operator docs and all related plans/incidents.

Completed: implementation, exact-module activation, independent review and docs.
Fresh verification: real-fzf fixture passed both result lines, exit 0; all 98
search tests passed in 38.034s, exit 0. Commit verification found and repaired a
cached-fixture startup race; cached verification now launches zero workers while
uncached cases retain refresh/Ctrl-G coverage. README gate passed without repairs.
The code is installed byte-for-byte; only the test fixture changed afterward.
No implementation blockers remain. Remaining user check: reopen an old picker
once and inspect a real missing Guardian/untitled row. Next step after delivery:
use the recorded smoke commands; provider completion time remains unknown.

Scope helper returned unsafe because it found no successful repo-writing actions
in this native session log. Directly observed successful writes establish the
fallback: only the two modules, three test files, both task plans, six task
postmortems, the search guide, and separable picker README/smoke/learning hunks.
Other-session backup, Second Brain, notification, shortcut and instruction work
stays uncommitted. Reconstruct mixed files against current HEAD in a private
index and inspect that exact diff, preserving the working files and other index
entries. No history rewriting or broad configuration refresh is needed.
Rollback: revert the focused feature commit when explicitly authorized, then
reapply the two exact modules. The saved native names and generation policy are
unchanged. The Cursor prompt and automated/manual checks above remain current.

Final scoped review: all six targeted checks against the reconstructed staged
learning ledger exited 0 with no errors; private-index git diff --cached --check
exited 0. Mixed-file diffs contain only this task's two lessons, two reviewed
findings/six source records, picker README paragraph and two smoke checks.
The actual repository index remains untouched until this focused commit.
