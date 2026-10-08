# Fast directory sizes

Implement a read-only wrapper around an existing GitHub disk-usage CLI, verify allocated accounting, and measure responsiveness and completion without claiming universal speed gains.

## Context and scope

Execute `prompts/fast-directory-sizes-2.md` once. Scripts follow `scripts/executable_*`. Preserve all initial dirty files (README, smoke tests, ledger and lessons already dirty); edit only task-related sections. No commits, push, worktrees, backup repair, sudo source reads or cache drops. Default current directory, explicit depth, safe unusual paths, no repeated tree scans.

## Assumptions and decisions

Backend is not installed; research via gh and inspect primary source before selection. Download an isolated pinned backend to /tmp for verification; provide reusable setup. Display depth does not bound metadata traversal. Mode remains Default because no mode-switch tool is exposed; this document supplies the required decision-complete plan. Failure lookup and workaround are recorded in the matching sandbox postmortem.

## Ordered checklist

- [x] Capture initial status and read prompt/instructions/preferences.
- [x] Compare GitHub backends and settle accounting/output/error semantics.
- [x] Write defining contract tests and observe expected RED.
- [x] Implement wrapper and reusable setup with minimum safe behavior.
- [x] Test fixtures against equivalent GNU du and bounded benchmarks.
- [x] Run one bounded selected-backend probe and equivalent allocated and logical baseline probes on reference tree.
- [x] Update docs, README and smoke tests; run applicable sync and fresh verification.

## Risks and rollback

Rotational USB may punish concurrency. Permission failures and live tree mutation prevent complete claims. Sparse files need allocated bytes; hardlink attribution may differ with traversal order. Interruptions must reap subprocesses. Source tree is read-only. Remove only newly created task files to roll back; restore task-added hunks only in pre-existing dirty docs/ledger. Downloaded tools stay outside Git.

## Verification

Run `python3 -B tests/test_directory_sizes.py` (RED before implementation, GREEN after). Real backend fixture checks cover sparse, nested, empty, hardlink, symlink, spaces, dash, newline paths. Run `python3 -B tests/scripts/directory_sizes_benchmark.py` for bounded fixture and real probes; record all elapsed/output/progress/error measurements and cache conditions. Read fresh diff and targeted postmortem check. Configuration refresh applies only if tracked configuration changes; new executable utilities/docs alone do not change configuration.

## Progress, evidence and review

Initial tools: gh 2.86.0, GNU du/sort 9.4, Go available; gdu/dust/dua/ncdu absent. Failed default shell startup, approved route successful. Backend research delegated as independent read-only task per repository instructions. Final commands and results will be added below.

## Final evidence and review

- Research via gh: Dust 1.2.6, gdu 5.38.0, dua 2.45.1 tagged docs/source. Dust selected for directory-only nested output plus allocated directory accounting; stderr gate and explicit backend limits documented.
- RED: initial executable-existence test failed because implementation absent; newline-render contract failed before JSON renderer; benchmark interruption contract failed at 4.40 seconds before cleanup fix. GREEN: `DIRECTORY_SIZES_REAL_BACKEND=/tmp/directory-sizes-installed/bin/dust python3 -B tests/test_directory_sizes.py`: 9 tests, exit 0.
- Setup helper installed Dust 1.2.6 into /tmp/directory-sizes-installed, exit 0; all four Python artifacts parse successfully. Separate real permission fixture at uid 1000: exit 1, stdout empty, permission path shown.
- Three final fixture runs: wrapper 0.2554/0.2514/0.2493s; direct Dust 0.1603/0.1659/0.1908s; du/sort 0.0942/0.0855/0.0830s. Uncontrolled warm fixture caches; du was faster.
- Reference, once per command, 20s limit: wrapper indexing 0.2414s and no totals; du allocated and logical sorted pipelines no output. All incomplete and reaped. Provisional 557700 indexed files/493GiB cannot establish total. Final renderer changed after reference probe; scanner unchanged; final fixtures remeasured without repeating real probes.
- Read-only reviewer identified benchmark Ctrl-C orphan risk; executable RED reproduced it, final cleanup now TERM/waits on every exit path, including startup errors. Signal/process cleanup tests pass.
- Documentation: docs/directory-sizes.md and measurements JSON, scoped README command row and smoke section. No tracked configuration files changed; no refresh-config required. No commit/push/worktree performed.
- Broader postmortem suite: 25/26 passed; test_actual_ledger_reference_status_and_coverage fails for existing unregistered .worktrees aliases. Targeted task checks recorded separately. Native title tool initially worked then local HTTP transport became unavailable; existing native title retained.
- Risks: no atomic snapshot, silent backend metadata races, Dust over-preallocation cap, logical directory metadata difference, rotational/cache-dependent speed. No complete real reference comparison; permissions/stability unknown after bounded interruption.
- Handoff/rollback: docs contain exact setup/use/test commands and Cursor prompt. Suggested subject `feat(scripts): add guarded Dust directory size reports`. Preserve all initial dirty content; rollback only task-owned new files and inserted doc/ledger/lesson hunks.

- Fresh final verification: nine focused tests passed in 1.967s, exit 0. Readable small-directory report succeeded; depth-zero JSON root children were empty. All three task postmortem targeted checks exited 0 with no errors/new/changed/unregistered entries. Scoped git diff --check exited 0. No nested AGENTS files were found in the task directories.
