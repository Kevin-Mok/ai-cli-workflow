# Existing push-policy contract failure during chatbot work

This record separates an existing workflow-test failure from the personal-context
implementation. Preserve the current commit policy and report the baseline while
validating the chatbot's own behavior and routing.

## Symptom, Impact, And Evidence

Before changing any skill or canonical routing instructions, running
`python3 -B tests/test_ai_workflow_contract.py` produced 11 passes and one failure
(exit 1). `test_push_policy_is_consistent_in_active_workflows` requires one exact
legacy sentence in `dot_agents/skills/commit-dirty/SKILL.md`.

The existing commit skill expresses the newer best-effort push policy in
different wording. That file is unchanged by this task. The existing Second
Brain suite passed 11 tests and the Claude skill-link script exited 0.

## Root Cause And Current Status

The literal-string contract and existing commit workflow have drifted. This
predates personal-context implementation. No chatbot failure or personal-data
exposure occurred. The broad workflow suite remains a known baseline failure.

## Resolution And Next Steps

Keep unrelated commit behavior and tests unchanged in this task. Run the suite
again after integration and compare the failing case with this baseline. A
separate commit-workflow maintenance change can reconcile the test with the
authorized best-effort policy. Do not claim the entire broad suite passes.

Post-integration verification repeated the full 12-test suite: the same single
case failed, and the other 11 passed. No additional failure was introduced by
personal-context routing. Status remains a pre-existing maintenance finding.
