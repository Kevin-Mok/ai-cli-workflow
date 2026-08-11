# fn-progress Days and Rounding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Display elapsed and remaining C7S3 days in `fn-progress` and round
the active-season percentage to the nearest whole number.

**Architecture:** Retain the helper's fixed timestamps and inactive branches.
Use its existing duration and elapsed-seconds values to calculate integer day
counts, replace the ceiling-style `bc` expression with nearest-integer
rounding, and add one labeled output line. The existing Fish-level shell test
will exercise the real function with a deterministic `date` executable.

**Tech Stack:** Fish shell, `bc`, Bash regression test, chezmoi, Markdown
documentation.

## Global Constraints

- Preserve the fixed C7S3 schedule and pre-season/ended output unchanged.
- Render both counts as `⏱️ Days: <elapsed> elapsed, <remaining> remaining`.
- Round `89.9%` to `90%`; do not retain ceiling behavior.
- Do not stage or edit the pre-existing untracked
  `scripts/executable_install-tmux-tpm.sh`.
- Run `refresh-config` after the tracked Fish configuration change and inspect
  its effects before finalizing.

## Current Context, Scope, and Decisions

- Approved design: `docs/superpowers/specs/2026-08-11-fn-progress-days-and-rounding-design.md`
  in commit `ca805aa`.
- `dot_config/fish/functions/fn-progress.fish` derives timestamps in seconds
  and currently applies a `+ 0.9999` ceiling calculation through `bc`.
- `tests/test_fn_progress.sh` replaces `date` with fixed values: start `100`,
  current `150`, end `200`, producing 50 elapsed seconds of 100 total.
- Scope is limited to the helper, its deterministic regression test, the
  relevant smoke-test check, a linked incident postmortem, and this plan.
- The pre-existing untracked installer script is protected. No other initial
  dirty work was present when `git status --short` was captured.

## Risks, Edge Cases, and Rollback

- Day counts use complete 24-hour units by integer division; the frozen 50 of
  100-second fixture intentionally verifies the rounding behavior rather than
  treating mocked seconds as calendar days.
- The calculation must not leak fractional output from `bc`.
- The simple rollback is restoring the prior Fish helper and its matching
  test/documentation files; no remote state is changed.

### Task 1: Define the active-output regression

**Files:**
- Modify: `tests/test_fn_progress.sh`

**Consumes:** The sourced real `fn-progress` Fish function and a mocked
`date` executable.

**Produces:** A regression assertion that fails while the helper retains
ceiling rounding and lacks day counts.

- [x] **Step 1: Write the failing assertions**

  Extend the fixture to represent 89.9% elapsed progress with a 10-day
  schedule: `START_SECONDS=0`, `CURRENT_SECONDS=776736`, and
  `END_SECONDS=864000`. Assert exactly these output fragments:

  ```bash
  if [[ "$output" != *'⏱️ Days: 8 elapsed, 1 remaining'* ]]; then
    printf 'expected elapsed and remaining whole-day output\n%s\n' "$output" >&2
    exit 1
  fi

  if [[ "$output" != *'✅ Fortnite C7S3 is **90%** complete!'* ]]; then
    printf 'expected 89.9 percent to round to 90 percent\n%s\n' "$output" >&2
    exit 1
  fi
  ```

- [x] **Step 2: Run the focused test to verify RED**

  Run: `bash tests/test_fn_progress.sh`

  Expected: exit 1 because the unmodified helper neither prints the `Days:`
  line nor rounds 89.9% to `90%`.

### Task 2: Implement the minimal active-branch calculation

**Files:**
- Modify: `dot_config/fish/functions/fn-progress.fish`
- Test: `tests/test_fn_progress.sh`

**Consumes:** `TOTAL_DURATION` and `TIME_PASSED` in seconds.

**Produces:** Integer day counts and a nearest-whole percentage in active
season output.

- [x] **Step 3: Add integer day calculations and nearest rounding**

  Replace the ceiling-only calculation with Fish `math` integer divisions and
  an integer `bc` nearest-rounding expression, then add the output line:

  ```fish
  set ELAPSED_DAYS (math -s0 "$TIME_PASSED / 86400")
  set REMAINING_DAYS (math -s0 "($END_SECONDS - $CURRENT_SECONDS) / 86400")
  set PROGRESS_PERCENT (echo "scale=0; (($TIME_PASSED * 100) + ($TOTAL_DURATION / 2)) / $TOTAL_DURATION" | bc)
  # ... existing date output ...
  echo "⏱️ Days: $ELAPSED_DAYS elapsed, $REMAINING_DAYS remaining"
  ```

- [x] **Step 4: Run focused GREEN verification**

  Run: `bash tests/test_fn_progress.sh && fish -n dot_config/fish/functions/fn-progress.fish`

  Expected: exit 0; the real Fish function emits `8 elapsed, 1 remaining`
  and `90%` against the deterministic fixture.

### Task 3: Record reproducible verification and deploy the tracked source

**Files:**
- Modify: `docs/smoke-tests.md`
- Create: `docs/postmortem/2026-08-11-fn-progress-days-and-rounding.md`
- Modify: `plans/fn-progress-days-and-rounding.md`

**Consumes:** Green test results and the source configuration change.

**Produces:** A current manual check, concise incident record, deployment
evidence, and completed ExecPlan.

- [x] **Step 5: Update user-facing verification documentation**

  Amend the existing Fish Helpers smoke-test expected result to require the
  C7S3 schedule, a whole-number percentage, and labeled elapsed/remaining day
  counts. Add a concise linked postmortem that records symptom, impact,
  deterministic RED evidence, root cause, resolution, verification, and the
  source-level rollback path.

- [x] **Step 6: Apply and verify tracked configuration**

  Run: `refresh-config`

  Expected: refresh completes successfully. Inspect `git status --short` and
  the `fn-progress` installed target; preserve unrelated generated or
  pre-existing work rather than staging it.

- [ ] **Step 7: Run final verification and complete the plan**

  Run: `bash tests/test_fn_progress.sh && fish -n dot_config/fish/functions/fn-progress.fish && git diff --check`

  Expected: all commands exit 0. Update this plan with the actual RED/GREEN,
  refresh, diff, and review evidence; mark only completed steps `[x]`.

- [ ] **Step 8: Commit the implementation milestone**

  Stage only the helper, test, smoke-test entry, postmortem, and this plan;
  inspect the staged diff; then commit with:

  ```bash
  git commit -m "fix: show fn-progress days"
  ```

## Progress, Verification Evidence, and Review Notes

- [x] Captured initial Git status before the first tracked-file modification:
  only `scripts/executable_install-tmux-tpm.sh` was untracked and remains
  protected.
- [x] User approved the design and then approved execution (`go`).
- [x] Created and committed the design specification in `ca805aa`.
- [x] Test RED evidence recorded.
- [x] Minimal implementation and GREEN evidence recorded.
- [ ] Full-suite verification and final review evidence recorded.
- [ ] Implementation milestone committed.

- RED evidence: `bash tests/test_fn_progress.sh` exited 1 after the fixture froze 89.9% progress; the old helper printed `89.9999%` and omitted the required day line.
- GREEN evidence: after the minimal Fish change, `bash tests/test_fn_progress.sh` and `fish -n dot_config/fish/functions/fn-progress.fish` exited 0.
- Refresh evidence: `refresh-config` completed snapshot, shortcut, and Fish-reload steps but full `chezmoi apply` could not obtain a TTY for the unrelated live Codex config prompt. `chezmoi apply --dry-run --verbose ~/.config/fish/functions/fn-progress.fish` showed only this helper; targeted `chezmoi apply ~/.config/fish/functions/fn-progress.fish` then completed, `cmp -s` returned 0, and the installed helper printed `66 elapsed, 7 remaining` and `90%`.
- Final review: `git diff --check` exited 0; the protected unrelated dirty paths are the pre-existing `scripts/executable_install-tmux-tpm.sh` and the refresh-created `dot_codex/config.toml` snapshot; both are intentionally excluded from this change.

- Broader regression blocker: `python3 -m unittest discover -s tests -p 'test_*.py' -v` ran 315 tests and failed only `test_second_brain_vault.SecondBrainVaultTest.test_exact_sanitized_tree_exists_without_unapproved_files`. The test allowlist excludes the tracked `second-brain/05 Daily Notes/2026-07-22.md`, introduced in commit `8c4ad43`; it is unrelated to this change. The 29 shell scripts were not run because the Python suite stopped the final all-green gate.
