# Alpha Intro Regression Baseline

Record the unrelated metaprompt runtime failure discovered while validating
the saved alpha digest introduction. Confirm whether the failure exists in
the original base, report its scope, and preserve the prompt-only change.

## Symptom and impact

`python3 -m unittest discover -s tests -p 'test_metaprompt*.py' -v` ran
139 tests: 138 passed and one failed, exit 1. The failure is
`RuntimeBoundaryTests.test_live_skill_envelope_removed_candidate_and_fixture_text_preserved`
in `tests/test_metaprompt_benchmark_runtime.py:250`: the expected
`host_skill_envelope_removed` event is absent; the output instead contains
`blocked_host_context_structure`.

The new alpha intro test passes. No prompt runtime is added by this change.

## Lookup and applicability

The query `blocked_host_context_structure host_skill_envelope_removed metaprompt`
matched `local-benchmark-host-context-guard` in the reviewed
`references/state-security.md` guidance. Its installed-root recognition and
fail-closed framing checks apply. The prior fix does not establish a fix for
this environment-dependent fixture failure.

## Cause and baseline verification

The test hard-codes `/home/example/.agents/skills/...` at line 239, while
`benchmarks/metaprompt/runtime.py:47-50` derives installed roots from
`Path.home()`. The synthetic root is unrecognized here, so the later guard
retains and blocks the envelope instead of emitting a removal event.

Exported only `benchmarks/metaprompt` and the failing test from pristine
`origin/main` (`4366ee0cdc2317bd56b9b9fbd66afe434f26b5f6`) into a disposable
directory using `git archive`. The diagnostic command
`python3 -m unittest discover -s tests -p test_metaprompt_benchmark_runtime.py
-k test_live_skill_envelope_removed_candidate_and_fixture_text_preserved -v`
reproduced the same failure, exit 1. This establishes a baseline failure.

The new alpha intro test passes (1 test), and the directly related
metaprompt contract and integration suites pass (12 and 9 tests respectively).

## Status and learning

The unrelated fixture defect remains unresolved. No parser or fixture remedy
is implemented in this prompt-only PR. Disclose the failure in the PR and
handoff; any future fixture correction needs its own defining regression.

No new reusable learning: existing host-context guidance already requires
exact installed-root recognition and fail-closed handling of unknown framing.
Register this report's reviewed hash and alias in the tracked memory ledger;
no change to that guidance or claimed prior verification is warranted.

The first ledger-registration attempt stopped before writing because its
format-preservation assertion did not match the existing JSON formatting.
The prematurely run coverage check consequently reported the report as new.
The corrected registration uses a targeted insertion that preserves the
existing formatting; the targeted check verifies its final reviewed hash.
No existing ledger entries were changed by the refused attempt.
