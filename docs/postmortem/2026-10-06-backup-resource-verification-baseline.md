# Backup resource verification baseline observations

This report tracks verification outcomes outside the resource fixture tests. Preserve current user settings and unrelated work while installing the verified backup change.

- Symptoms: a protected refresh preflight byte comparison found live Codex config differs from tracked source; repository-wide unittest discovery printed a failure marker and remains running.
- Impact: no refresh or config overwrite was performed at the mismatch; no running backup was stopped. Focused backup suite passes 43 tests. Broader-suite failure needs attribution before completion.
- Config evidence: parsed TOML differs only in model_reasoning_effort (live high, source max). Snapshot dry-run passed; Git config equality passed. The current setting must be preserved, and refresh-config is explicitly defined to snapshot current live settings into tracked source.
- Lookup: relevant artifact-verification guidance and the existing Codex-search refresh audit corroborate concurrent model_reasoning_effort drift; no stale source restoration. Baseline tests must be compared before attributing unrelated failure to compression.
- Status: investigation in progress; collect exact broader test name/error and complete protected refresh with a fresh boundary snapshot.
- Next steps: preserve current configuration, attribute broader failure by inspecting its source/baseline, run focused regression and scoped installation equality.

## Broader test result and attribution

Repository-wide discovery completed 665 tests in 103.506s, exit 1 with seven failures:
- test_ai_workflow_contract.AIWorkflowContractTest.test_push_policy_is_consistent_in_active_workflows: exact policy sentence absent from commit-dirty skill.
- test_metaprompt_integration.MetapromptIntegrationTest.test_legacy_references_and_license_are_unchanged: four subtests (execution-routing.md, examples.md, model-profiles.md, compilation-rules.md) have disputed frozen hashes. Reviewed local-legacy-integrity-baseline already documents these exact committed-baseline failures.
- test_postmortem_memory.WorkflowTest.test_actual_ledger_reference_status_and_coverage: full selected-root coverage includes newly authored reports from concurrently active track-codex-sessions work plus this then-unregistered living report. Register this task's report; other repository evidence remains out of scope.
- test_second_brain_vault.SecondBrainVaultTest.test_exact_sanitized_tree_exists_without_unapproved_files: extra tracked 05 Daily Notes/2026-07-22.md.

These surfaces are unrelated to backup compression. Preserve their files and expectations; matching source/tests are unchanged against HEAD for the push sentence, legacy hash fixtures and vault paths. Scope-specific backup tests pass 44 checks after independently reviewed XZ environment and thread-reduction notice fixes. Global incident coverage remains unsettled while other tasks author reports. This report's targeted check validates only owned incident coverage, not all external roots.

Configuration resolution: refresh intentionally snapshots current live model_reasoning_effort=high; preserve that current setting. Do not restore stale max from source. Other current edits are checkpointed at the refresh boundary.

## Resolution evidence

Owned verification completed: 44 backup tests pass; syntax/diff and README checks pass. Required refresh finished REFRESH COMPLETE, exit 0; installed backup-pc bytes match source and every checkpointed unrelated/task file hash was preserved. Source Codex configuration intentionally captured current live high setting. Actual-machine preflight passes and selects nine threads under the available-memory ceiling. Broader unrelated failures remain documented and out of scope; no blanket repository success claim. Status: scoped verification and installation complete, unrelated baseline issues unresolved.
