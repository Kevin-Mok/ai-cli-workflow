# Largest daily file size

## Purpose and scope

Add a reusable command that scans a directory recursively, groups regular files by their local modification date, and prints up to three dates with the greatest total file size in human-readable binary units. The command reads files only; it does not modify the scanned directory.

## Context and decisions

- Existing commands live under `scripts/` with an `executable_` source prefix.
- Use Python's standard library for safe filename handling and timestamp conversion.
- Skip symlinks; break equal totals in favor of the earliest date.
- Show the top three days, or all available days when fewer than three exist. Use binary units (`B`, `KiB`, `MiB`, `GiB`, and larger) with one decimal place above bytes.
- Protect all changes listed by the initial `git status --short`, including existing README and smoke-test edits. Add only focused text to those documents.

## Checklist

- [x] Capture initial status and inspect instructions and nearby script conventions.
- [x] Add a failing CLI test for grouped totals, recursion, ties, and input errors.
- [x] Implement the smallest command that passes the test.
- [x] Document usage and a manual smoke check.
- [x] Run focused tests, review the diff, and record evidence.
- [x] Extend the CLI tests for top-three ranking, ties, and human-readable units; observe RED.
- [x] Update the command, README, and manual smoke check; observe GREEN.
- [x] Recheck the README gate, focused and broader tests, and final diff.

## Risks and rollback

Local dates depend on `TZ`; daylight-saving transitions follow the local timezone. Files changing during the scan can alter totals. Remove the new script, test, and documentation additions to roll back.

## Verification and review notes

- RED: `python3 -m unittest tests/test_largest_day_file_size.py` exited 1 with three failures because the command did not yet exist.
- GREEN: The same command exited 0 with four passing tests after implementation.
- `./scripts/executable_largest-day-file-size --help` exited 0 and showed the positional directory argument.
- `./scripts/executable_readme-recruiter-sync` exited 0 with `pass_no_change`.
- `git diff --check` exited 0.
- Broader `python3 -m unittest discover -s tests -p 'test_*.py'` ran 398 tests and exited 1 with one unrelated Second Brain vault fixture failure, recorded in `docs/postmortem/2026-09-27-daily-size-broad-suite-vault-failure.md`.
- Review: kept the new command read-only and standard-library only. Existing README and smoke-test edits remain preserved. No configuration change was made. Rollback consists of removing this task's new files and focused additions to those two documents.
- Follow-up RED: the updated focused test exited 1 with three expected output failures while the command still printed one raw-byte row.
- Follow-up GREEN: the focused test exited 0 with six cases, including a sparse 30.5 GiB file and top-three ranking. An initial sparse fixture failed because truncation reset its modification time; the fixture was corrected and recorded in `docs/postmortem/2026-09-27-daily-size-sparse-fixture-mtime.md`.
- The README gate again returned `pass_no_change`; `git diff --check` exited 0; `--help` described the top-three output.
- The final broad discovery run executed 400 tests and exited 1 with only the existing Second Brain vault fixture failure.
- `chezmoi diff /home/example/scripts/largest-day-file-size` showed only this command's output changes, and targeted `chezmoi apply /home/example/scripts/largest-day-file-size` exited 0. The installed command was updated without applying other targets.
- A direct `TZ=UTC largest-day-file-size <sparse-fixture>` run exited 0 and printed `2026-08-21 30.5 GiB`, `2026-08-20 2.0 KiB`, and `2026-08-19 1.0 KiB`; `cmp` confirmed installed and source scripts match. A final focused test, whitespace check, and README gate all exited 0.
