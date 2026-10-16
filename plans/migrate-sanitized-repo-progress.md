## Goal and Done Criteria

This is the completed migration record. Use the current-state section for
read-only verification, and preserve private recovery data before considering
any separately authorized future migration.


## Current state: completed

The live cutover completed after the retry-2 rollback. The active checkout uses
the public repository and main upstream; the private completed journal records
69 accepted files and 48 archived linked worktrees. Preserve recovery data
privately. Historical pending/retry instructions below are superseded: use only
read-only verification now, and obtain a new task before another cutover or
rollback. Accepted files have since changed during normal development, so an
old exact-byte migration verification can legitimately refuse those changes.

The current shipping pass reviews and commits safe migrated functionality and
adds destination-ancestor containment regression coverage; it does not perform
another migration, restore old objects, or publish the private journals.

Goal: replace `~/linux-config` with independent sanitized history and preserve private recovery.
- DC1: tested migration helper and refresh isolation.
- DC2: safe pending functionality reviewed and portable docs prepared.
- DC3: live cutover, recovery archive, fresh refresh and final verification.

## Constraints
- No commits/pushes/deletion/history rewrite/credential rotation. Preserve all concurrent edits. Do not run real refresh against the old checkout. Recovery state must remain outside Git with restrictive permissions.

## Decisions
- User's supplied prompt is implementation authority. Follow `plans/migrate-sanitized-repo.md`.
- Use private hash-bound overlays; sanitized templates take precedence. Preserve local integrations via private data/ignored targets. Disable external-template evaluation offline. Restore atomically and refuse unknown subsequent edits.

## Current State
- Original main checkout remains active, with pre-existing and concurrent edits intact. Development now runs in `~/linux-config/.worktrees/migrate-sanitized-repo` on `feat/migrate-sanitized-repo` per the user’s “new worktree” answer.
- 23 proposed transfer paths are in `/tmp/migration-reviewed-transfer.json`; overlays at `/tmp/migration-reviewed-overlay/`. Manifest must be rebuilt after any edits.
- Live apply has not run. No archive exists at the default recovery location.

## Evidence and Failed Attempts
- DC1 — met — From the isolated worktree: 32 migration, snapshot 19, timer 34, checkpoint modules 33, fish output 9 and portable offload 11 tests passed (138 total); refresh shell integration passed — see active plan.
- DC2 — open — initial 23-path proposed transfer set has zero sanitized content-scanner findings; new concurrent notification/shortcut/instruction work still needs final review — inspect current status and regenerate manifest.
- DC3 — open — dry-run inventoried 40 worktrees, rendering/shortcut rehearsal succeeded; no live cutover — resume only after concurrency answer.
- Failure: sandbox DNS/external evaluation — scoped HTTPS clone succeeded; offline rendering tested; old snapshot mapping remains network-blocked. Retry live activation only after safe cutover timing.
- Failure: broad suite — 1,232 tests, 51 failures/49 errors/one skip; two stale task-related assertions fixed and focused suites pass. Remaining surfaces are not claimed green. Private log `/tmp/migration-regression-full.cIbPzN.log`.

## Artifacts
- `plans/migrate-sanitized-repo.md`: scope, decisions and evidence.
- `scripts/executable_migrate-ai-cli-workflow`: dry-run/apply/verify/rollback.
- `prompts/migrate-sanitized-repo.md`: paste-ready continuation prompt.
- `/tmp/ai-cli-workflow-inspect/`: independently cloned sanitized source, history audit passed.
- `/tmp/migration-offload-overlay/`: portable storage helper and 11 passing tests; originals unchanged.

## Blockers
- Concurrent writers: new unrelated edits and multiple active tasks in this checkout observed. User chose a new development worktree; the active-path cutover still requires a writer-free window.

## Ordered Next Actions
1. Owner: implementing agent — Action: inspect current writer activity and main-checkout pending hunks, then review new hunks path by path — Expected: writers idle and safe changes identified — Stop if: sessions still write or ownership is ambiguous.
2. Owner: implementing agent — Action: update `/tmp/migration-reviewed-overlay/` and rebuild `/tmp/migration-reviewed-transfer.json` with source/destination SHA-256 bindings — Expected: only reviewed safe bytes, no scanner findings — Stop if: private values or template conflicts appear.
3. Owner: implementing agent — Action: run `python3 scripts/executable_migrate-ai-cli-workflow --apply --review /tmp/migration-reviewed-transfer.json` with scoped filesystem/network access — Expected: private archive, repaired worktrees, reviewed apply/fresh refresh and verification — Stop if: fingerprints change or preflight refuses.
4. Owner: implementing agent — Action: switch tool cwd explicitly to replacement `~/linux-config`, verify script/history/pending content, and update the active plan with observed results — Expected: truthful final handoff — Stop if: intended live settings differ.

## Transfer-rejection repair

The user’s first live attempt aborted at the content gate before cutover. Its default journal is `rolled_back`, with candidate retained and no archive/live-start marker. Fixed only synthetic variable names in snapshot tests; scanners remain intact. New regression transfers actual snapshot-test source, and diagnostics show only JSON-escaped paths under `--details`. Rolled-back retry error now explicitly requires a new `--state-dir`. Migration 34/34, snapshot 19/19 and refresh shell checks pass. Actual production transfer/render/shortcut/pending-audit preflight passed on a disposable independent sanitized clone. Next apply/verify/rollback must consistently use `~/.local/state/ai-cli-workflow-migration-retry-1`; preserve the failed default directory. Root shipping session was active at the last check. See `docs/postmortem/2026-10-15-migration-transfer-rejection.md`.

## Current blocker after retry-1

Retry-1 refused changed preparation state, rolled back before cutover; default and retry-1 journals/candidates remain intact. Exact prior difference unknown because old journals omitted initial fingerprint. A later read-only probe observed actual HEAD/index/worktree-registration changes in the original checkout. Do not run another live apply while root sessions write.

Code update: semantic index fingerprint excludes stat-cache refresh while preserving indexed blobs/modes/stages/flags, intent-to-add and resolve-undo; new private journals store initial and changed fingerprints; --details prints categories/counts; dry-run detects material drift during inventory without state creation. Latest 40 migration, 19 snapshot and 9 fish-output tests pass. The next unused state directory is retry-2, but only prepare a live retry after writers stop and manifest is reviewed/refreshed. Incident: `docs/postmortem/2026-10-15-migration-checkout-change.md`.

## Best-effort live snapshot completed

At the user’s direction, captured a private live recovery snapshot at `~/.local/state/ai-cli-workflow-live-snapshot-20261015T180312Z` without replacing active paths. Two copy passes captured the main checkout and 41 linked worktrees (42 total), plus 1,271 recorded live configuration files/links. Snapshot root is mode 0700; logs/manifests are private. Copied worktree pointers were repointed only inside the snapshot; source pointers and live settings were not rewritten. Original Git configuration bytes are retained separately, with snapshot hooks/fsmonitor disabled.

Observed evidence: 5.3 GiB; both copy passes completed without errors; zero copy/metadata issues; copied Git connectivity exit 0; SHA-256 verification passed for 79,400 snapshot files/links; 41 copied worktree pointer pairs resolve within the snapshot. Before/after recorded Git state did not change during capture. A disposable capture self-check verified dirty/untracked/nested/external preservation and unchanged source config/index/pointers. Read-only verification helper is `verify-snapshot.py` inside the private snapshot (`--status`, `--verify`, `--verify-worktrees`).

This is best-effort live recovery material, not an atomic filesystem snapshot. It does not establish a single-instant view of all working files. No migration cutover, live refresh, commit, push or credential rotation was performed. Preserve the snapshot privately; do not import its old Git history into the sanitized clone.

## Readiness refresh — 2026-10-16

Live swap remains pending. Fresh dry-run passed with 1,956 paths and 47 linked worktrees; other listed tasks were idle, and no main-checkout drift occurred during inventory. Original private origin/main remains active. Default and retry-1 journals are rolled back with no archives; retry-2 is unused. Public main and the inspected candidate match; all 28 existing source/destination manifest hashes match.

New concrete gate: the current checkout advanced beyond the snapshot (41 linked worktrees) and transfer review. Root-versus-snapshot blob review identifies omitted notification/audio, source-context capture, Context Mode/metaprompt handoff, and editor/desktop changes. Existing manifest would archive these but not preserve them in the active public source. Review/port safe functionality against sanitized templates, update overlays including newer plan evidence, and refresh the private snapshot before final rehearsal/apply. Do not treat intentionally sanitized overlay differences as automatically stale or copy old private templates wholesale.

Fresh snapshot status, full checksum verification of 79,400 files/links, and 41 copied worktree-link checks passed (exit 0). No live settings, checkout paths, commits or remotes changed. Remaining action evidence belongs in the active plan.

## Authorized execution checkpoint — 2026-10-16

User directed implementation and live cutover. Fresh private recovery snapshot captured 49 checkout/worktrees (48 linked), 1,276 recorded live files/links, zero copy/metadata errors, Git connectivity exit 0 and no recorded Git-state drift. Full checksum verification passed for 93,597 files/links; all 48 snapshot-only pointer pairs verified. Existing failed journals and prior snapshot remain intact.

Reviewed portable runtime overlays carry notification/source-context, tmux/Dunst, Markdown doctor, metaprompt handoff and editor fixes. Sanitized templates stay in source; existing machine integrations remain private. Claude target preservation and neutral project-contract protection each reproduced RED before the minimal fix, then passed GREEN. Template-dependent optional integrations retain installed state; installer execution is excluded, and their full bootstrap wiring is not transferred. Pstack scheduled refresh requires separate reviewed external registration; preserving installed plugin files alone does not establish automatic updates.

This checkpoint is frozen into the hash-bound transfer. Runtime completion and final evidence are recorded in the private migration journal and final handoff, so writing documentation after cutover does not invalidate accepted-file verification or recovery fingerprints. No cutover success is asserted by this pre-execution record.

Final pre-cutover gate: 70 migration/snapshot/fish tests, 134 transferred-feature tests, 37 composite doctor/tmux/socket checks and refresh isolation shell passed. Independent evidence review found no new code blocker. Rendering/shortcut rehearsal completed for 1,555 targets; all history and pending-content checks passed. Runtime state will be recorded privately under `~/.local/state/ai-cli-workflow-migration-retry-2`; the verified fresh snapshot is `~/.local/state/ai-cli-workflow-live-snapshot-20261016T172433Z`. No installer hooks will execute.

Retry-2 reached fresh fish refresh but automatically rolled back after an intended-byte mismatch on8 PNG icons. Every recorded live backup was verified restored; all48 linked worktrees restored. A real invalid-UTF-8 fixture reproduced the issue, raw rendered-byte handling passed GREEN, and the corrected rehearsal matches all8 icons. Private-config hash integrity also has RED/GREEN coverage. Preserve retry-2; current execution journal is the unused `~/.local/state/ai-cli-workflow-migration-retry-3`. See `docs/postmortem/2026-10-16-migration-binary-render.md`; no subsequent live success is asserted here.
