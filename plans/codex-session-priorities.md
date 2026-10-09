# AI priority and Guardian refresh in crg

Make the recent Codex picker show sessions most worth returning to and refresh
that order as Guardian or another session produces new evidence. Add validated
AI priority to recaps, safely refresh local sources, preserve UUID selection,
then verify with disposable sessions and real fzf before installing.

## Purpose and observable outcome

`crg` uses AI priority by default: urgent, actionable, unknown, waiting, complete.
Within each tier, latest source activity wins. Preview explains priority and its
freshness. Updates to titles/dialogue/activity/new sessions are reflected while
open, with stale priority labelled until new inference completes. `--sort recent`
retains newest-first. Listing alone remains newest-first unless explicitly sorted.

## Context and boundaries

Existing modules: scripts/codex_search_recent.py, codex_search_recaps.py,
codex_search_index.py and executable_codex-search. Tests use synthetic dialogue
and external-runtime stubs; real fzf verifies selection. Guardian is the native
approval reviewer and writes ordinary local session/title evidence, with no
separate repo callback. Do not alter original sessions, native Guardian settings,
ordinary pattern search, existing model isolation, or account limits. No commit,
push, worktree or private payload copies are requested.

## Settled assumptions and decisions

User approved the in-chat design on 2026-10-09. AI assigns a bounded priority
and reason in the existing isolated recap call, not a separate ranking service.
Unknown evidence stays unknown; urgent/actionable precede it, waiting/complete
follow it. Cached legacy recaps remain readable, with priority unknown until
regenerated. The automatic window remains the newest summary-count sessions.
A changed dialogue can receive a new attempt; unchanged data cannot cause a
model loop. Preserve filter and selected UUID across rank changes, including
safe zero-match Enter. Refresh polling is throttled and background work must be
reaped before resuming. Plan Mode is unavailable; maintain this ExecPlan.

## Implementation checklist

- [x] Capture baseline; read sources, instructions, lessons, existing plans.
- [x] Obtain approval for priority order and automatic Guardian refresh.
- [x] Write/observe RED tests for AI validation, ranking, live source refresh,
  changed-digest generation and exact UUID selection during reorder.
- [x] Add backward-compatible priority schema/prompt and generation-key attempts.
- [x] Add priority sorting and throttled safe refresh with stable UUID selection.
- [x] Update help, README, session-search guide and grouped smoke checks.
- [x] Run focused regressions, existing CLI checks and real fzf fixture.
- [x] Run protected refresh-config; verify installed command/source and shortcuts.
- [x] Reconcile final diff, evidence, review notes and handoff.

## Risks and protected work

Pre-existing README.md, docs/smoke-tests.md, docs/commit-status-overviews.md,
dot_codex/AGENTS.md, feedback log, incident ledger and untracked incident notes
must remain intact. Read fresh bytes before edits. Before refresh verify protected
source/live configs and limit broad apply to task targets if necessary. Index
maintenance can replace/delete dialogue files during inference: prepare bounded
input under the index lock and keep worker snapshots independent of cleanup.
Old generation results must not overwrite newer evidence. fzf 0.44 tracks input
positions, so every reordered reload must restore the highlighted UUID rather
than relying on --track. Polling large trees can be expensive; use a background
throttled reader, do not block the UI or run models for metadata-only changes.

## Verification

RED: focused new unittest cases and deterministic real-fzf reorder/refresh mode
fail for missing behavior before production edits. GREEN/regression:
`python3 -m unittest discover -s tests -p 'test_codex_search*.py'`;
`bash tests/scripts/executable_codex_test.sh`;
`python3 tests/scripts/codex_recent_live_check.py`;
`python3 tests/scripts/codex_priority_live_check.py --scenario all`;
`python3 tests/scripts/codex_priority_live_check.py --command /home/example/scripts/codex-search --scenario all`;
`git diff --check`. Manual: crg, newest-first override, cached-only priority,
zero automatic generation with Ctrl-G, priority listing/details, and live
Guardian update preserving query/UUID. Use synthetic runtime without live
provider calls. No sudo required. Record exact outcomes below.

## Progress and evidence

2026-10-09 baseline captured. Sandbox startup workaround and incidental lookup
errors recorded in docs/postmortem/2026-10-09-codex-priority-inspection.md; targeted
incident-memory check passed. Native fzf version 0.44.1 verified. No code edited
before defining tests.

## Review notes and rollback

Rollback only this task's module/CLI/doc/test hunks and reinstall prior scripts
through protected refresh; native session files require no rollback. Recap
versioning invalidates priority without deleting useful legacy summaries. Final
review must verify query stability, UUID identity, cache freshness, model caps,
isolation, cancellation, installed bytes, and preservation of initial dirty work.

## Coding handoff

Atomic steps: validated priority and bounded-input worker; live ordering/refresh
with real-fzf identity checks; documentation and protected installation.
Cursor prompt: Read plans/codex-session-priorities.md; review priority semantics,
source-change invalidation, UUID-preserving reload and model-call caps. Run the
listed synthetic and real-fzf checks; preserve unrelated dirty work and do not
commit or push unless asked.
Suggested commit: feat(codex-search): rank recent sessions by AI priority

2026-10-09 implementation: strict seven-field recap schema and format 2, legacy
stale/unknown cache compatibility, 36 worker tests green, per-key attempts and
same-key file-replacement recovery. Priority/CLI/watcher defining tests observed
RED, then GREEN; native filter listing includes reasons in details. Real fzf
0.44 lacks generic transform, so use supported capture/load callbacks. Only
actual order changes restore UUID; ordinary text refresh retains native tracking.
Resume/recap keys are guarded while reordered input loads. Watcher is a cancellable
child process and ExitStack reaps it before runtime directory removal. One
standalone identity check passed, but a later timing-dependent fixture failure
requires root-cause investigation before completion. Full CLI Guardian synthetic
fixture and final protected installation remain in progress.

2026-10-09 final implementation review: immutable per-revision row files and
serialized capture/load/executed acknowledgements resolve delayed reload identity
and uncertain HTTP delivery. Load callbacks write actions for the parent rather
than posting to their own listener. Enter uses the visible UUID; cancellation
after listener closure follows normal cleanup. Defining lost-restoration replies
observed RED, then GREEN for both startup and reordered positions. Priority fixture
inference is released only after the defining selection exists. Narrow preview
checks scroll while awaiting asynchronous final content. A lock probe now retries
brief watcher ownership for at most 2s while inference remains active for 60s;
the expanded 13-scenario terminal fixture has a 60s aggregate budget and bounded
8s phase checks. Focused lock, plain 20/58-column ASCII output, and full real-fzf
checks pass. Actual CLI Guardian/cache/recent fixture passed three complete fresh
repetitions with no provider calls, exact UUID/cwd resume, zero added cached model
calls and no watcher/worker leaks. Final full-suite and installed evidence pending.

2026-10-09 fresh final source evidence: search unittest discovery passed all 122
tests in 69.796s, exit 0; shell launcher passed, exit 0; full real-fzf fixture
passed all modes, exit 0; README gate pass_no_change; git diff --check exit 0.
Read-only independent review found no generation/lifecycle blocker in executed
acknowledgements. Stable selection is tested with a fixed query; simultaneous
query editing during the brief positional restore interval is not separately
proved. Normal refilter/zero-match behavior is covered and Enter always uses
the visibly supplied UUID. Synthetic inference verifies plumbing/cache/runtime,
not the quality of a live model's priority judgment. Installation pending.

2026-10-09 installation evidence: protected `fish /tmp/codex-priority-refresh.fish`
ran the real refresh-config snapshot/Codex+Git sync/shortcut generation/reload,
scoping only broad apply to the six Codex search targets. REFRESH COMPLETE,
exit 0; all 46 snapshotted workspace files unchanged during refresh. All six
installed files match tested source bytes and installed codex-search is executable.
Installed help exposes --sort and --plain. The actual installed CLI Guardian
fixture with --scenario all exited 0: appended dialogue/title/activity refreshed,
urgent became complete below actionable, query/UUID survived, exact UUID/cwd
resumed, cached/recent openings made zero extra model calls, runtime processes
and temporary directories were removed. No provider calls or private history
were used. Final incident hash/diff/handoff reconciliation pending.

2026-10-09 final handoff: all scoped work installed and verified, no remaining
implementation or installation blocker. Final incident learning records
local-fzf-serialized-reload-acknowledgement (runtime) and
local-recap-same-key-input-replacement (code); reviewed report SHA256
d208d1f149b834680ced90cb2217ad08b7f7479beb3596c24b86f302a98a768a.
Targeted incident-memory check passed exit 0 with no coverage/contract errors;
final scoped diff --check passed exit 0 and README gate pass_no_change.
README, session-search guide and smoke checks match installed options and criteria.
No commit/push/worktree requested or performed. Preserve all unrelated dirty work.
Outstanding evidence limits remain stated above: simultaneous changing-query
restoration intent and live model judgment were not independently evaluated.

Final shared-workspace check saw a concurrently added EOF blank line in the
unrelated editing-shell-transport reference; preserve it. Fresh task-scoped
whitespace check passed exit 0. The separate final-whitespace incident and its
no-new-learning registration passed targeted validation. This does not invalidate
the 122 tests, installed runtime evidence or completed task-owned changes.

## Authorized session delivery

The user invoked `$commit-session` after completing priority and the related
metadata-first startup fix. Deliver both phases together as
`feat(codex-search): prioritize sessions and open picker promptly`; the paired
startup plan, operator docs, defining tests and three reviewed incidents belong
in that same commit. No worktree or history rewrite is authorized.

The scope helper returned `unsafe` because nested code-mode `exec` writes were
not recognized. Use its documented direct-write fallback: preserved before-write
snapshots, this session's recorded patch/command evidence and independently
reviewed HEAD-plus-owned-hunk blobs. Exclude concurrent CLI decoration,
notification/audio, command-policy, VPS and configuration work. Preserve all
working bytes; shared README/smoke/ledger/reference/lesson files are staged only
at the reviewed hunk scope.

- [x] Attribute both implementation phases and prepare isolated candidate blobs.
- [x] Reconcile inspection report learning after temporary scope-check mistakes.
- [x] Verify the isolated candidate, README gate, exact runtime behavior and scope.
- [ ] Create the single scoped commit and push the configured `origin/main`.

Latest reviewed inspection SHA-256:
`833710b502f21f6bd9484a46ea1c2246fd7f7c2c51905b0aa4479a8fd0829741`.
Fresh targeted incident check passes with no changed/unregistered records.
Completed implementation/install evidence remains above. The next step is
the authorized commit and push. No product blocker.

Delivery milestone `feat(codex-search): prioritize sessions and open picker promptly`:
the exact isolated 27-file candidate passes all 160 Codex-search tests in 88.504s,
exit 0. The launcher check exits 0; candidate README gate is `pass_no_change`;
all three candidate incident checks pass. Fresh installed real-fzf startup:
cold 0.509s, cached 0.572s, locked 0.531s, malformed 0.539s, details 0.534s;
all exact-resume/source-preservation/cleanup checks pass with no provider calls.
Fresh installed Guardian/live/cached/recent modes pass exact query/UUID/cwd,
source refresh, priority reorder, zero additional cached calls and cleanup.
All six installed modules match current source. The 27 scoped files are below
3 MB; unrelated workspace bytes and existing staging are protected. Review the
temporary index against this candidate, commit once, then push `origin/main`.
Report the resulting hash and push outcome in the handoff; implementation,
verification and documentation have no remaining blocker. Rollback remains
limited to owned hunks and protected script installation; native sources are
read-only. Simultaneous query-edit intent and live AI judgment retain the stated
verification limits.
