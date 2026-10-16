# Migrate to sanitized repository

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


Replace the active checkout with independent sanitized history, preserve the complete old checkout and worktrees privately, and prevent refresh from importing private configuration. Build and rehearse recovery before the authorized live cutover. Do not commit, push, delete archives, rewrite history, or rotate credentials.

## Context and boundaries

Active source: `~/linux-config`, branch main, origin is the old ai-cli-dotfiles repository. Chezmoi source-path resolves here. Initial `git status --short` captured before edits: README and smoke tests, three postmortem-memory files, bash/zsh configs, mimeapps and Vesktop settings modified; home-storage-offload docs/plan/script/tests and three postmortems untracked. Preserve all initial work in the archive; review content before transferring functionality. Linked worktrees include nested `.worktrees/` and external sibling paths.

## Decisions and assumptions

- User supplied the full implementation specification in the calling request.
- Use this existing checkout because the task replaces this very path; no branch or history edits.
- Private recovery state must be outside both repositories, mode 0700; outputs report paths/status only, never values or patches.
- Only explicitly reviewed paths transfer; existing sanitized templates take precedence. Reject ambiguous machine configuration and private payloads. Scanning is a supplementary check, not proof of absence of secrets.
- Use supported chezmoi exclusions for scripts/externals; inventory removals and hooks before file application. Arbitrary installer effects are not covered by backups.
- Runtime changes outside the workspace require the normal scoped sandbox escalation, already authorized by the user task.

## Checklist

- [x] Capture initial dirty status and map refresh/snapshot callers.
- [x] Inspect independent sanitized clone and local data requirements.
- [x] Define synthetic tests covering transfer, worktrees, failure/recovery, rollback, repeat execution, redaction, and refresh isolation; observe RED.
- [x] Implement `scripts/executable_migrate-ai-cli-workflow` with dry-run/apply/verify/rollback and private recovery journal.
- [x] Fix refresh/snapshot/adoption paths, maintaining trust boundaries.
- [ ] Finish review of newly arrived concurrent edits; initial transfer set reviewed without values.
- [x] Rehearse full migration and rollback with synthetic HOME and repositories; run regression tests.
- [x] Update README, smoke checks, related public guides, and this plan.
- [ ] Run reviewed live migration, switch cwd to replacement, verify fresh fish refresh and history/pending audits.
- [x] Independent implementation review, blocker regressions, and focused worktree verification.
- [ ] Live cutover verification and final migration handoff.

## Risks and recovery

Old Git history and worktree contents remain sensitive; parent archive permissions provide privacy without deleting recovery. Cutover must reject changed checkout/live state. Journal phases must make interrupted rename/repair/apply recoverable. Rollback checks fingerprints before restoring so later user edits cannot be overwritten. Record all destination files/links plus chezmoi state/config before writes. Do not render missing identity keys as example placeholders.

## Verification

RED/GREEN: synthetic repositories and temporary HOME only. Include dirty tracked/untracked files, nested/external dirty worktrees, unknown secrets rejected, required-data failures, failed clone/render/apply, interrupted recovery, rollback conflicts, repeat execution, and redacted output. Focused refresh tests plus existing snapshot/checkpoint checks. Live: script dry-run, apply, verify; sanitized auditor and separate pending-content review; fresh fish refresh; check origin/upstream/source-path and mapped worktree common directories.

## Progress and review notes

2026-10-15: initial inventory complete. HTTPS clone in default sandbox failed DNS before modifying a checkout; scoped network escalation requested. See living incident `docs/postmortem/2026-10-15-migration-network.md`. No cutover attempted.

2026-10-15: RED observed before migration script existed; 25 synthetic integration tests now pass, including actual chezmoi, isolated history, nested/external dirty worktrees, failures, SIGKILL recovery and refusal of subsequent edits. Refresh safety: 57 focused tests passed; slow-apply heartbeat and actual excluded hook/external/removal checks passed. Full sanitized history auditor: 683 commits / 5,111 unique blobs, 0 findings (exit 0). Read-only render: 1,542 targets, identity data extracted privately. Live dry-run: 40 linked worktrees inventoried, no writes beyond Git LFS temporary inspection metadata; no cutover yet.

Review rulings: retain active path, independently clone with an empty Git template, bind reviewed source/destination hashes, preserve local integrations through private ignore data, and disable external-template evaluation using private offline data because chezmoi evaluates templates even when externals are excluded. Directory/file backups cover only excluded-hook file application. Record expected rendered outputs before writes; rollback refuses unknown output. Worktree fingerprints include bytes, not only porcelain status. Keep machine-specific offload settings private; generalize only the reviewed helper's destination argument.

2026-10-15: Independent review identified five additional gaps; fixes and defining regressions now cover resumable rollback repair, atomic live restore, complete intended-output verification, staged-only pending changes, and no fsmonitor/filter execution during preview. Inventory no longer calls Git status; read-only dry-run succeeds without escalation. All shortcut outputs and sourcing files are privately rehearsed and journaled before refresh. Current focused suite: 31 migration tests passing; 19 snapshot tests passing. Broader original-checkout run: 1,232 tests, 51 failures / 49 errors / one skip; not claimed green. Two stale checkpoint path expectations identified and corrected, focused rerun pending. Other failures include external network, desktop, private-context and source-resolution surfaces; no baseline claim without comparison.

Concurrency gate: new unrelated tmux/notification/instruction/feedback edits appeared after initial inventory. Active task list also shows other sessions in this checkout. Asked user about safe cutover timing; no cutover until that consequential concurrent-write ambiguity is resolved. Preserve and review newly arrived edits too. Documentation overlays are prepared privately from sanitized sources to avoid overwriting public templates with old identity data.

## Current handoff

Implementation is ready for review; live migration is **not performed**. Latest focused evidence: 32 migration tests (including strict no-write preview, staged-only paths, interrupted rollback, ignored-file edits, real chezmoi, and shortcut rehearsal) passed; snapshot 19, timer 34, checkpoint modules 33, fish output 9 passed; refresh shell integration and 11 portable offload tests passed. The broad original-checkout suite remains non-green; two task-related stale path expectations are fixed and their focused modules pass. Remaining broad failures are reported, not silently classified as baseline.

A live snapshot CLI dry-run in the old checkout failed while resolving its chezmoi mapping because the old external template requires network access in the sandbox. It did not write source or live config. Migration's private offline gate is independently rendered and tested; do not run a real old-checkout refresh to bypass this.

Private prepared artifacts: `/tmp/migration-reviewed-overlay/`, `/tmp/migration-reviewed-transfer.json`, `/tmp/migration-offload-overlay/`, and independent inspected clone `/tmp/ai-cli-workflow-inspect/`. Rebuild the manifest from final reviewed bytes after concurrent writers stop. No default migration state/archive directory exists. Target recovery location after authorized apply: `~/.local/state/ai-cli-workflow-migration/archive`. No commits, pushes, history rewrites, credential changes, or live apply occurred.

Review summary: initial unsafe shell duplicates, unsupported MIME associations, generated Vesktop state and private incident-memory records are quarantined by omission from the proposed transfer set; all remain in the old checkout. Safe home-storage helper is generalized through required `--destination`; original machine settings remain recoverable. More concurrent work must be reviewed after writers finish. Source/destination hashes are binding; refresh overlay and plan changes require manifest regeneration.

## Isolated continuation after user direction

The user answered the concurrent-writer timing question with “new worktree”. Created `.worktrees/migrate-sanitized-repo` on `feat/migrate-sanitized-repo` at the original HEAD. Its directory is mode 0700, and `.worktrees` was already ignored. The native worktree API cannot select the user-required repository-local path, so the Git fallback was used with hooks disabled. No commit was created.

All subsequent implementation and verification uses this isolated worktree. Copied only task-owned code, portable storage overlay, plan/progress/prompt, incident record, and precise public-guide hunks. Did not copy unrelated concurrent tmux/alias/feedback edits into this branch. Existing shared-root edits were left intact rather than risking another session's work. Full migration source remains the original active `~/linux-config`; `--repo` must continue to identify that ordinary main checkout, not this linked worktree.

The first worktree status attempt encountered the known Git LFS temporary-metadata sandbox restriction. A scoped status command succeeded; no user file was lost. Because the fresh worktree was created by Git before copying, no pre-existing worktree edits existed; successful current status records only the task file set. Read-only migrator inventory avoids Git status and fsmonitor entirely.

A development worktree resolves implementation isolation, but cannot make the final rename of an actively used shared checkout safe. Live cutover remains unperformed until concurrent writers finish; no migration archive or recovery journal exists. Focused verification is rerunning from this new path to establish layout correctness. The prepared private sanitized-overlay manifest must be refreshed from final bytes and newly arrived edits reviewed before live apply.

Final isolated-checkout evidence: 32 migration + 19 snapshot + 33 checkpoint + 34 timer + 9 fish-output + 11 portable-offload tests passed (138 total); refresh shell integration also passed. No nested-worktree path-layout defect was observed. Earlier whole-repository discovery remains a reported non-green run; it was not repeated globally after the two task-related stale assertions were fixed. Current worktree has no commits from this task. Another shared-checkout session was still active at the latest check, so live cutover and real refresh remain unperformed.

Canonical instruction correction: updated only the refresh-description paragraph in `dot_codex/AGENTS.md`, preserving the mandatory refresh requirement while replacing stale raw-snapshot guidance with the verified apply-only boundary. The public overlay uses the sanitized canonical baseline, preserving neutral values.

## Live attempt rejected before cutover

User’s authorized apply attempt reached the transfer gate and rejected snapshot regression source. Confirmed journal `rolled_back`, no archive, independent candidate retained. Root cause: earlier public-auditor-only preflight missed the stricter supplementary guard, which matched two synthetic local variable assignments. Added integration test transferring the actual snapshot-test source: RED reproduced the exact user error. Renamed only Python local identifiers, preserving runtime sentinel values and all boundary tests; no scanner weakened. Added RED tests for value-free path diagnostics and actionable rolled-back retry guidance. Details: `docs/postmortem/2026-10-15-migration-transfer-rejection.md`.

Private manifest preflight now checks both the public auditor and exact supplementary transfer predicate. All 25 reviewed paths pass. Prior default recovery directory is retained untouched; next attempt must use a new state directory consistently for apply/verify/rollback. Actual cutover remains pending concurrent shipping work in the shared checkout.

## Preparation-concurrency refusal

The retry passed transfer/render/history audit but refused a changed active fingerprint before cutover. Its initial fingerprint was not recorded, so the exact changed field in that attempt is unknown. A later read-only audit window observed actual HEAD/index/worktree-registration changes, confirming current concurrent activity. Preserve default and retry-1 directories, both rolled back with no archive/live-start marker.

Separately reproduced and fixed a metadata-only false refusal: raw index hashing treated stat-cache refresh as a material change. Semantic fingerprint includes entries/stages/modes/flags, cached diff (intent-to-add) and resolve-undo; raw index is still archived intact. Defining RED then GREEN tests and independent docs review cover these controls. Added private initial/difference recording and category/count-only --details; dry-run also compares before/after inventory without writes. Latest focused evidence: 40 migration + 19 snapshot + 9 fish-output tests pass (68 total); shell refresh passed. One separately reported timer fixture remains network-dependent. Do not offer another live retry until root writers stop. See `docs/postmortem/2026-10-15-migration-checkout-change.md`.

## Best-effort live snapshot completed

At the user’s direction, captured a private live recovery snapshot at `~/.local/state/ai-cli-workflow-live-snapshot-20261015T180312Z` without replacing active paths. Two copy passes captured the main checkout and 41 linked worktrees (42 total), plus 1,271 recorded live configuration files/links. Snapshot root is mode 0700; logs/manifests are private. Copied worktree pointers were repointed only inside the snapshot; source pointers and live settings were not rewritten. Original Git configuration bytes are retained separately, with snapshot hooks/fsmonitor disabled.

Observed evidence: 5.3 GiB; both copy passes completed without errors; zero copy/metadata issues; copied Git connectivity exit 0; SHA-256 verification passed for 79,400 snapshot files/links; 41 copied worktree pointer pairs resolve within the snapshot. Before/after recorded Git state did not change during capture. A disposable capture self-check verified dirty/untracked/nested/external preservation and unchanged source config/index/pointers. Read-only verification helper is `verify-snapshot.py` inside the private snapshot (`--status`, `--verify`, `--verify-worktrees`).

This is best-effort live recovery material, not an atomic filesystem snapshot. It does not establish a single-instant view of all working files. No migration cutover, live refresh, commit, push or credential rotation was performed. Preserve the snapshot privately; do not import its old Git history into the sanitized clone.

## Live-swap readiness check — 2026-10-16

Current readiness: **not ready to apply the existing transfer manifest**. The original private-history checkout remains active on `main`; default and retry-1 journals remain rolled back without archives, and retry-2 is unused. No cutover or live configuration write occurred during this check.

Fresh read-only dry-run with unused retry-2 state passed (exit 0): 1,956 tracked/pending paths and 47 linked worktrees, with no material main-checkout drift during inventory. Other tasks shown by the native task inventory were idle. This removes the previously observed active-writer blocker for that observation window, not for all future operations.

Public main still matches the independently inspected clone. All 28 reviewed overlay source hashes and sanitized destination hashes match their manifest. The development plan/progress files have newer evidence than those overlay copies and need review/hash refresh before transfer.

The active checkout advanced since the snapshot, which contains only 41 linked worktrees. Root-versus-snapshot blob comparison confirms functional changes omitted from the 28-path manifest: notification/audio behavior, source-context capture, Context Mode and metaprompt handoff, and Neovim/i3 behavior. Shared paths also need comparison against sanitized source; existing path presence does not establish feature parity. Applying the old list would preserve these changes in the old archive but would not carry them into active source. Review safe functionality and preserve sanitized templates before apply; retain rejected/private integrations through local configuration where needed.

- [x] Recheck live identity, unused recovery state, destination tip, manifest hashes, and non-mutating inventory.
- [x] Identify functional work arriving after the prior snapshot and transfer review.
- [ ] Review current functional changes against sanitized source and update the safe overlay/manifest.
- [ ] Refresh private recovery capture for the current checkout/worktree set and verify it.
- [ ] Rehearse final rendering/refresh, then perform authorized cutover with unchanged-state guards and verify the replacement.

The existing snapshot status, full checksum verification of 79,400 files/links, and all 41 snapshot-only worktree links passed fresh checks (exit 0). Snapshot integrity is not a freshness guarantee for the active checkout. No broad test rerun is claimed for this read-only readiness check.

## Authorized execution checkpoint — 2026-10-16

User directed implementation and live cutover. Fresh private recovery snapshot captured 49 checkout/worktrees (48 linked), 1,276 recorded live files/links, zero copy/metadata errors, Git connectivity exit 0 and no recorded Git-state drift. Full checksum verification passed for 93,597 files/links; all 48 snapshot-only pointer pairs verified. Existing failed journals and prior snapshot remain intact.

Reviewed portable runtime overlays carry notification/source-context, tmux/Dunst, Markdown doctor, metaprompt handoff and editor fixes. Sanitized templates stay in source; existing machine integrations remain private. Claude target preservation and neutral project-contract protection each reproduced RED before the minimal fix, then passed GREEN. Template-dependent optional integrations retain installed state; installer execution is excluded, and their full bootstrap wiring is not transferred. Pstack scheduled refresh requires separate reviewed external registration; preserving installed plugin files alone does not establish automatic updates.

This checkpoint is frozen into the hash-bound transfer. Runtime completion and final evidence are recorded in the private migration journal and final handoff, so writing documentation after cutover does not invalidate accepted-file verification or recovery fingerprints. No cutover success is asserted by this pre-execution record.

Final pre-cutover gate: 70 migration/snapshot/fish tests, 134 transferred-feature tests, 37 composite doctor/tmux/socket checks and refresh isolation shell passed. Independent evidence review found no new code blocker. Rendering/shortcut rehearsal completed for 1,555 targets; all history and pending-content checks passed. Runtime state will be recorded privately under `~/.local/state/ai-cli-workflow-migration-retry-2`; the verified fresh snapshot is `~/.local/state/ai-cli-workflow-live-snapshot-20261016T172433Z`. No installer hooks will execute.

Retry-2 reached fresh fish refresh but automatically rolled back after an intended-byte mismatch on8 PNG icons. Every recorded live backup was verified restored; all48 linked worktrees restored. A real invalid-UTF-8 fixture reproduced the issue, raw rendered-byte handling passed GREEN, and the corrected rehearsal matches all8 icons. Private-config hash integrity also has RED/GREEN coverage. Preserve retry-2; current execution journal is the unused `~/.local/state/ai-cli-workflow-migration-retry-3`. See `docs/postmortem/2026-10-16-migration-binary-render.md`; no subsequent live success is asserted here.
