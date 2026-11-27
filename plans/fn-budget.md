# Fortnite Inventory Budget

Use one command to plan how much Sprite Dust, how many Portable Extractors,
and how many Extraction Accelerators to use each day. Provide any combination
of the three balances to see their daily use and remaining stock together.

## Scope and decisions

Expose `fn-budget` with `--dust`, `--extractors`, and `--accelerators` flags.
Reuse the installed `dust-budget` implementation and preserve its positional
usage. Dust keeps the thousands shorthand. Gizmo balances are whole-item
counts. Each supplied resource gets its own integer allocation, with extra
units placed on the earliest days. Keep the December 4, 2026 local-midnight
cutoff, allow a cutoff override, and keep `--target` as the optional dust
reserve. Gizmo targets are zero. The calendar is shared and input balances are
supplied by the user on every run.

## Checklist

- [x] Commit the existing dust calculator and protect unrelated dirty work.
- [x] Run failing CLI regressions for flags, combined output and whole items.
- [x] Extend the existing calculator and add the managed umbrella command.
- [x] Update the README and shared smoke check.
- [x] Verify both installed entry points and the existing regressions.

## Verification and rollback

Run `python3 tests/test_dust_budget.py` and `bash tests/test_fn_progress.sh`.
With a November 26 start, run `fn-budget -d 187 -e 12 -a 5 --plain --as-of 2026-11-26`
and expect eight rows with final balances of zero. An extractors-only
invocation should use the exact item count. Confirm `dust-budget 187` remains
available. Apply only the reviewed managed targets if a broad refresh would
import unrelated edits. Roll back by removing the new link and restoring and
reapplying the previous managed executable.

## Observed evidence

- The standalone calculator was committed locally as `f0abd29`. The identical
  patch was published to `origin/main` as `cb257a2` from an upstream checkout.
  The README gate and privacy gate passed. The session helper lacked recorded
  writes, so the staged paths and documentation hunks were checked against
  edits observed in the conversation. Unrelated worktree changes were excluded.
- The new CLI tests initially failed on unsupported flags. The final run passed
  all seven tests. The existing `fn-progress` regression also passed.
- Verified the combined plan, extractor-only plan, and legacy dust invocation in
  fish. The eight-date combined plan used 23,375 dust, two extractors, and one
  accelerator on day one and reached zero across all three on December 3.
- The exact-target ChezMoi apply succeeded for both paths. The umbrella command
  resolves to the same executable. The broader refresh had pending unrelated
  updates. The README and smoke checklist document both entry points.

Suggested commit subject: `feat(cli): combine Fortnite inventory budgets`

## Cursor verification prompt

> Review the umbrella budget behavior in `plans/fn-budget.md`. Run
> `python3 tests/test_dust_budget.py` and `bash tests/test_fn_progress.sh`, then
> exercise the installed commands in the shared smoke checklist. Check that
> both entry points use the same implementation, the item flags take exact
> counts, and the last row respects the dust reserve and zero gizmo targets.

## Commit milestone

`feat(cli): combine Fortnite inventory budgets` includes the shared executable,
managed command link, tests, this plan, and the exact README and smoke-check
replacements. The session scope helper lacked recorded writes, so the candidate
was scoped to direct edits from this conversation. Unrelated edits to the
documentation and other worktree changes stay unstaged. Publish the same patch
from the upstream base to preserve the diverged local and remote histories.
