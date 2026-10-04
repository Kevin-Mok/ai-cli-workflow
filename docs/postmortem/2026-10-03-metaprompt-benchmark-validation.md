# Benchmark validation corrections

- Date: 2026-10-03
- Symptom: The first GREEN run passed eight scoring/accounting tests but the
  collision test raised `FileExistsError` instead of the public `ValueError`
  used by the restricted filesystem interface.
- Impact: Harness validation was incomplete; no model trials ran.
- Evidence: `python3 -m unittest discover -s tests -p
  'test_metaprompt_benchmark.py' -v` exited 1 with that single error.
- Root cause: Exclusive file creation correctly protected the prior artifact,
  but its filesystem exception was not translated at the tool boundary.
- Resolution: Translate the collision to an actionable `ValueError`; retain
  exclusive creation so a concurrent collision cannot overwrite an artifact.
- Current status: Collision correction verified; all ten initial behavioral
  tests passed. Subsequent complete boundary suite passed 21 tests.
- Next steps and follow-up: Verify the full harness before freezing trials;
  maintain this postmortem with any further validation findings.

## Independent review before scored execution

A reviewer found two accounting/extraction defects before any model output:
an artifact could hide ambiguous prompt fences, and a quota stop between a
completed compiler and an unstarted solver could be classified as pending.
Added executable regressions, observed failures, then rejected ambiguous
outputs and introduced `quota_truncated` in the attempted denominator. Native
prompt/save/legacy-gate violations are now recorded as compilation failures.
These are harness corrections before held-out execution, not candidate tuning.
# Review path correction

A report edit later included an out-of-order trailing context hunk and was
rejected atomically. No report or benchmark input changed. The final report is
rewritten from the completed results instead of retrying that stale hunk.

During the read-only outcome audit, a reviewer projection assumed a solver
object existed on a compiler-limit failure and raised `TypeError`. No evidence
or quota changed. The reviewer corrected the projection to tolerate absent
stages; capped and compiler-failed trials legitimately have no solver object.

A later combined patch missed a wrapped prose line in this incident file. The
patch applied no hunks. Inspection confirmed that atomic failure, and the
patch was reapplied with exact
context. No trial or quota evidence changed.

## Public signatures and standalone report integrity

Independent review reproduced two more pre-holdout gaps: a variadic replacement
could pass positional hidden tests while breaking the promised public signature,
and standalone report generation did not validate its frozen inputs. Defining
tests failed for both expected reasons. Grading now checks actual callable
parameter names, kinds and defaults against the existing fixture; optional type
annotations are accepted. Reports validate the frozen inventory and use its
schedule before rebuilding results. Existing output and quota evidence is
preserved. No held-out outputs were used for these corrections.

During the final read-only review, a command used lowercase `protocol.md`
instead of the inventoried `PROTOCOL.md` and exited 1. No files or trial
evidence changed. The reviewer corrected the filename and continued. This
incident has no scoring impact; use inventoried case-sensitive paths.

## Contradictory saved and displayed prompts

Final review found that one saved prompt could disagree with the displayed
native prompt fence while passing the contract. No held-out trial had started.
The defining regression failed with `saved_prompt_mismatch` absent. Both native
validation and extraction now reject the discrepancy, allowing only terminal
newline differences. This preserves workflow failures instead of selecting a
preferred artifact. The focused benchmark suite verifies the correction.
