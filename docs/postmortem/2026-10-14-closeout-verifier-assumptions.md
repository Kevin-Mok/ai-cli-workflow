# Closeout Verification Assumed The Wrong Command Inputs

This postmortem records two read-only closeout checks that failed because their
inputs were not derived from the artifacts they were verifying.

## Symptom

The report-structure check expected five section titles that differed from the
actual report headings. A follow-up `rg` command then treated an option-like
search pattern as a command-line flag because the pattern was not preceded by
the option terminator.

## Impact

Both commands exited unsuccessfully and produced no repository or report
changes. The sanitized Git graph, external report content, and prior evidence
review remained intact, but closeout paused while the verifier was corrected.

## Evidence

- The first assertion listed only missing expected headings; the corrected
  worktree count was already present.
- Listing the report's actual level-two headings showed the same required
  sections with title-case wording.
- The second command reported an unrecognized flag beginning with the search
  pattern; retrying with `--` before the pattern returned the intended skill
  instruction line.

## Current status

Resolved. The final report check uses the report's actual headings, verifies
the corrected count, runs the generic privacy scanner, and checks the exact
task-prefixed `/tmp` inventory.

## Root cause

The checks embedded unverified assumptions about prose labels and argument
parsing instead of first reading the artifact shape and terminating option
parsing for a pattern that begins with hyphens.

## Resolution

Derive structural assertions from the current report headings, then assert the
required semantic sections and counts. Use `rg -- <pattern>` whenever a search
pattern could be parsed as an option.

## Verification

- The corrected report-structure and generic-privacy check passes.
- Independent evidence review confirms the corrected 1,726-file count, zero
  generic report findings, unchanged repository state, and report-only `/tmp`
  inventory.
- The terminal audit correctly caught an unrelated unsafe identity in the first
  closeout commit attempt. That finding is resolved and verified in the linked
  [commit-identity incident](2026-10-14-closeout-commit-private-identity.md).

## Follow-up

- Inspect artifact structure before encoding prose headings in one-shot
  verification commands.
- Terminate option parsing explicitly for user- or artifact-derived patterns.
