# Best-effort Codex picker startup

Open crg using available session metadata before full archive indexing finishes.
Skip malformed records quietly, refresh usable rows in the background, then verify
that cold-cache and cached startup reach the actual UI promptly and resume safely.

## Purpose and scope

The user explicitly requested ignoring malformed/incomplete input and displaying
the UI to the best available ability. Fix recent picker startup and diagnostic
ownership; retain full text-search indexing, priority semantics, controlled recap
generation, exact UUID/cwd resume, cancellation and read-only original history.
Plan Mode is unavailable; maintain this ExecPlan in the active Default mode.

## Settled assumptions

Cached metadata and bounded native session metadata are enough for initial rows.
Missing dialogue stays pending until background indexing supplies validated data.
No warning flood or full-archive parse should delay or overwrite the picker.
Explicit details can expose skipped-record counts; malformed input must never leak
its raw payload. Cache ownership/symlink guards remain strict. No commits/pushes,
worktrees or provider calls are requested for verification.

## Checklist

- [x] Capture current dirty state; read sources, lessons and relevant incident guidance.
- [x] Record reported failure and independent investigation scope.
- [x] Define and observe failing startup/quiet-malformed runtime tests.
- [x] Implement prompt initial metadata rows and quiet background best-effort refresh.
- [x] Verify existing priority/resume/cancellation and focused new edge cases.
- [x] Update README, guide and grouped smoke checks; reconcile incident learning.
- [x] Run protected refresh-config and verify installed behavior.
- [x] Record final evidence, review and handoff.

## Risks and protected work

Most CLI scripts and docs are concurrently dirty from an emoji rollout and prior
tasks. Preserve fresh file bytes and edit only focused hunks. A running archive
refresh can hold the cache lock; picker startup must not wait behind it. Unknown
initial metadata must not trigger invalid or duplicate inference. Background
failure must keep usable rows available, with ongoing concise in-UI progress.
Do not promise all history is ready before a background scan completes. Preserve
safe cancellation and reaping; do not make warning suppression hide fatal cache
ownership errors. Roll back only this task's hunks and reinstall those scripts.

## Verification and review

Use synthetic sessions with an intentionally delayed old source and malformed
neighbors. Assert actual fzf startup precedes archive completion for cold/cache
paths, no default warning flood, valid rows still selectable, and details retain
diagnostics. Run focused checks then full Codex search regressions, real Guardian
priority fixture, launcher check and task-scoped whitespace/README gates. Verify
installed source bytes and native picker on available local metadata without a
provider prompt. No sudo is needed. Record exact RED/GREEN and runtime evidence.

## Progress

2026-10-09: screenshot and source trace confirm foreground full archive refresh
before fzf and per-source skipped warnings repeated for cached entries. Prior
synthetic priority fixture had only tiny sources, so it did not cover this scale.
Independent investigators reviewing bootstrap/security and defining tests.

Focused RED: cold/cached-lock/render checks failed as expected; a separate watcher
check reproduced repeated terminal warnings. GREEN: five CLI/header/preview/watcher
checks pass in 1.484s. Index helper's 16 defining checks and all 43 recap checks
pass. Full search/priority/fzf suite is running. Cold rows remain provisional,
background passes release the lock, and skipped diagnostics stay inside the UI.
Independent review caught premature recap pruning on partial archive scans;
maintenance now waits for complete discovery with no pending sources.
One oversized source can exceed the nominal one-second pass target, but parsing
occurs after the UI opens. Native header bootstrap is capped at 200 usable rows,
1,000 candidates and a one-second between-file budget; warm cache also caps 200.

Final evidence: all 160 Codex search tests pass in 88.946s (exit 0), including real
Guardian append/rename, cached priority/newest-first modes, query/UUID preservation,
elapsed recap progress, cancellation and cleanup. Installed actual CLI startup
passed cold 0.817s, cached 1.076s, locked 0.688s, malformed 0.682s and details 0.620s
with zero provider calls, exact resume and unchanged disposable sources. Native
installed history showed 199 usable rows in 1.968s; Escape removed its watcher/UI
without inference or resume. Required refresh-config succeeded; all six deployed
modules match source and 1,540 repository files plus three live configs were
unchanged by refresh. README gate reports pass_no_change; focused whitespace passes.

Fixture corrections retain assertions: real-manager progress now owns consistent
native sources/cache/titles; listener selection reads use bounded observation,
and uncertain position POSTs are never replayed. Independent review confirmed
no foreground archive lock, protected partial discovery and exact UUID acceptance.
No commits or pushes made; unrelated dirty work remains preserved. Blockers: none.

Daemon recovery: the previous exec handle disappeared after a server restart;
source/install hashes and protected files were unchanged and no prior fixture
process remained. Fresh installed Guardian all-mode verification passes (live,
cached and newest-first exact resume/cleanup), as do all recent-picker PTY modes.
Changed fixture progress/success messages now use default emojis with legacy
CLI_PLAIN=1 support; raw worker JSON and resume protocol markers stay unchanged.

## Exact verification plan

Run from /home/example/linux-config; no sudo is needed. Automated checks:

```bash
python3 -m unittest discover -s tests -p 'test_codex_search*.py'
python3 dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py check --postmortem /home/example/linux-config/docs/postmortem/2026-10-09-codex-picker-archive-startup.md
./scripts/executable_readme-recruiter-sync /home/example/linux-config
```

Direct manual/runtime checks use real fzf and the installed CLI. Inference is
synthetic in the priority fixture; no provider calls are made by either fixture:

```fish
python3 tests/scripts/codex_startup_live_check.py --command /home/example/scripts/codex-search --scenario all
python3 tests/scripts/codex_priority_live_check.py --command /home/example/scripts/codex-search --scenario all
codex-search --recent --pick --no-summaries
```

Expected: startup phases show usable rows within two seconds; exact synthetic
UUID/cwd resume, source bytes and cleanup pass. Guardian updates move completed
work below actionable work without losing query/selection; cached modes add no
calls. Native picker opens with usable metadata; press Esc to cancel. Uncached
AI priority remains unknown until validated dialogue and recap generation finish.

Docs updated: README.md, docs/codex-session-search.md, docs/smoke-tests.md,
the living incident, tracked memory ledger/reference and tasks/lessons.md.

## Handoff

Atomic steps: readiness/diagnostic tests; metadata-first picker and background
refresh; docs, incident learning and protected installation.
Paste-ready Cursor prompt:

```text
Read plans/codex-picker-best-effort-startup.md and docs/codex-session-search.md. Review metadata-first startup, malformed/unreadable input tolerance, pending inference, complete-discovery recap maintenance, background progress, exact UUID resume and process cleanup. Run the exact automated and installed runtime verification commands in the plan. Preserve unrelated work and do not commit.
```

Suggested commit: fix(codex-search): open recent picker before archive indexing

## Authorized session delivery

The subsequent `$commit-session` request authorizes delivery with the earlier
priority/Guardian phase in one focused commit:
`feat(codex-search): prioritize sessions and open picker promptly`.
Commit both plans, implementation, tests, operator docs and the three session
incidents together; preserve unrelated working-tree changes and native history.
No worktree or history rewrite is needed.

- [x] Prepare HEAD-based candidate blobs using direct session-write evidence.
- [x] Run isolated-candidate regressions, README and learning gates, runtime checks.
- [ ] Commit the verified scope and push its configured `origin/main` upstream.

The scope helper's `unsafe`/empty result reflects unrecognized nested code-mode
writes. Its direct-write fallback excludes concurrent emoji/notification/policy/
VPS/configuration work rather than treating the entire dirty tree as eligible.
The inspection report records temporary preparation mistakes and their verified
causes; its reviewed hash is reconciled and targeted validation passes.
Implementation and protected installation are complete. Remaining delivery is
one commit and push; no product blocker.

Delivery milestone `feat(codex-search): prioritize sessions and open picker promptly`:
the exact 27-file HEAD-plus-owned candidate passes all 160 search tests in 88.504s
and the launcher check, exit 0. Candidate README gate reports `pass_no_change`;
all three final incident-memory checks pass. Fresh installed startup reaches
real fzf in cold 0.509s, cached 0.572s, locked 0.531s, malformed 0.539s and details
0.534s, all below 2s with exact resume, source preservation and cleanup. Installed
Guardian all-mode checks pass priority refresh/reorder, exact query/UUID/cwd,
cached/recent zero-added-call behavior and cleanup; no provider calls.
All six installed files match the current protected source. Implementation,
verification, docs and installation are complete; delivery is one reviewed
session-only commit followed by the configured upstream push. Its resulting hash
and push outcome are reported in the handoff. Preserve every unrelated working
byte and existing index entry; no product blocker or new rollout is needed.
