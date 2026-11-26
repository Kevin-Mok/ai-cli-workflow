# Season Dust Budget

Use `dust-budget` to split a current balance across the remaining spending days
and see the target balance after each day. Enter the season cutoff date and,
optionally, how much dust to keep.

## Scope and decisions

The existing `fn-progress` helper reports a December 4, 2026 midnight cutoff.
Use the same cutoff convention and accept an explicit date so future seasons and
other games work without source edits. Count today's local calendar date through
the day before the cutoff. Default the reserve to zero. Use integer dust units,
put one extra unit on the earliest days when division has a remainder, and
reject an expired cutoff or a reserve above the current balance. The command is
stateless. Keep the existing season helper and unrelated worktree edits intact.

## Checklist

- [x] Capture the initial dirty state and inspect the existing helper.
- [x] Add and run a failing CLI test for the example, reserve, and invalid input.
- [x] Implement the Python CLI in `dot_local/bin/executable_dust-budget`.
- [x] Document the CLI in the README and add a durable smoke check.
- [x] Verify the CLI, installation, and unchanged season countdown.

## Verification and review

Run `python3 tests/test_dust_budget.py` and `bash tests/test_fn_progress.sh`.
Run the managed command with `178k 2026-12-04 --as-of 2026-11-25` and expect
nine rows, whole-unit daily budgets of 19,777–19,778, and a final balance of zero.
Rerun with `--target 25k` and verify the last balance is 25,000. A cutoff on the
starting date should give an actionable error. Verify the target is available on
fish's PATH. Review deployment scope before applying configuration because the
checkout contains unrelated changes. Rollback is removal of the installed
command and withdrawal of the files and documentation added here.

## Observed evidence

- The new CLI suite failed first because the command was missing. After
  implementation, all three tests passed. The existing season countdown suite
  exited 0.
- The installed command ran on fish's PATH and matched the source byte for
  byte. The zero-reserve and 25,000-reserve examples matched the expected
  schedules. The cutoff-day case exited 2. A two-day plan with only one
  spendable unit allocated 1 on the first day and 0 on the second.
- The scoped ChezMoi dry run and exact-target apply exited 0. The full refresh
  was skipped because it would import an unrelated modified plan.
- The README command table and shared smoke checklist document the behavior.
  `git diff --check -- README.md docs/smoke-tests.md` exited 0.

Suggested commit subject: `feat(cli): add season dust budget calculator`

## Cursor verification prompt

> Review the season dust calculator in
> `dot_local/bin/executable_dust-budget` against `plans/dust-budget.md`.
> Run `python3 tests/test_dust_budget.py` and `bash tests/test_fn_progress.sh`,
> then run the `dust-budget` examples in `docs/smoke-tests.md` against the
> installed command. Confirm that the last row lands on the reserve and the
> cutoff date has no spending row. Preserve unrelated worktree edits.

## Default-season shortcut

- [x] Observe a failing regression for `dust-budget 187` and its default cutoff.
- [x] Make an omitted cutoff default to December 4, 2026. Treat a bare
  positional balance as thousands. Accept explicit `k` and comma-grouped
  balances and use `d` for exact balances such as `187d`. Keep reserve
  amounts in their existing units and allow a positional cutoff override.
- [x] Update the README and smoke check, verify the revised command, and
  reapply its managed target. Roll back by restoring the previous script and
  applying the same managed target.

The RED run exited 1 with the two new cases failing. The GREEN run passed all
five budget tests, and `bash tests/test_fn_progress.sh` exited 0. Verified
`dust-budget 187` in fish with the local date of November 25. It planned nine
days at 20,777–20,778 dust per day and ended at zero. The smoke-check reserve
variant spent 18,000 per day, and the explicit-date exact-balance variant
spent 100 and kept 87. The installed executable matches the source. Applied
only the managed command because the broad refresh had unrelated pending
changes. The README and smoke check document the shortcut.

Suggested commit subject: `feat(cli): default dust budget to season cutoff`

## Commit milestone

`feat(cli): add season dust budget calculator` records the executable,
regression checks, plan, and the scoped README and smoke-check entries.
All five CLI tests, the season countdown regression, and the README gate
passed. Source attribution comes from the files and hunks edited in this
session. The scope helper could not identify those writes in its log.
The umbrella command is the next milestone. Local main and its upstream
have diverged, so publishing must preserve upstream history and exclude
unrelated local commits.
