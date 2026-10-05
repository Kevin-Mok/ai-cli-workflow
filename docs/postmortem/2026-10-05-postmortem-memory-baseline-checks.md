# Shared-memory baseline workflow checks

Two existing workflow gates fail before this implementation. Retain their evidence separately so new memory changes can be checked for regressions without rewriting unrelated skill policy or provenance.

## Symptom and impact

The workflow contract suite has one failing push-policy assertion. The doctor audit reports one invalid metaprompt provenance record and one nonblocking duplicate-skill warning. These baseline issues prevent an all-green existing-workflow claim.

## Evidence and current status

Before implementation, `python3 -B tests/test_ai_workflow_contract.py` ran 12 tests: 11 pass, `test_push_policy_is_consistent_in_active_workflows` fails because commit-dirty does not contain the expected exact policy text. `python3 -B tests/test_ai_workflow_doctor.py` passes all 19 tests. Doctor `--repo /home/example/linux-config --check` exits 1: invalid_source_provenance for metaprompt/SOURCE.md; duplicate_active_skill_slug warning for brand-system-designer. Full output is in task-local `/tmp/postmortem-memory-baseline-*.txt` files.

## Root cause and resolution

The policy string assertion and doctor provenance schema disagree with pre-existing skill text. No repair is authorized in this incident's scope; it remains unresolved. New memory work must introduce no additional failures. Prompt authoring remains owned by metaprompt.

## Verification and next steps

Rerun the same checks after implementation and compare exact failures. Record fresh results here. Do not reinterpret a baseline failure as passing, and do not change unrelated provenance to hide it.

Fresh postimplementation comparison: workflow contract again passed 11/12 with the same exact commit-dirty push-policy assertion (exit 1). Doctor regressions passed 19/19 (exit 0). The repository audit still reports the same one metaprompt provenance error and one duplicate brand-system-designer warning, with no additional findings (exit 1). README gate passes with pass_no_change (exit 0). These baseline issues remain unresolved and separately attributed.
