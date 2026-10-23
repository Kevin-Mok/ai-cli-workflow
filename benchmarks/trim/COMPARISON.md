# Trim comparison

Reproduce instruction costs from committed Git blobs, compare the original with HEAD,
then inspect real pass commits and their recorded verification. An optional working
draft is reported separately and never counts as a committed pass.

Always-loaded tokens per session: **9,404.75 → 3,779**
(-5,625.75 tokens, -59.82%).

Original: `3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c`. HEAD: `c24871f2f765bb9f5e3517607c513b77ac4e3e9b`.

Estimates use UTF-8 bytes / 4, not model tokenizer usage. The headline includes
root AGENTS.md + canonical dot_codex/AGENTS.md + config developer_instructions +
canonical dot_agents skill descriptions. Skill bodies are on-demand. Skill names,
paths, runtime wrappers, external installs and the duplicate .agents catalog are
excluded from the headline. External install changes require separate evidence.

## Original versus HEAD

| Metric | Original | HEAD | Change |
| --- | ---: | ---: | ---: |
| AGENTS.md lines | 16 | 16 | +0.00 |
| AGENTS.md bytes | 690 | 690 | +0.00 |
| AGENTS.md approx_tokens | 172.5 | 172.5 | +0.00 |
| dot_codex/AGENTS.md lines | 353 | 145 | -208.00 |
| dot_codex/AGENTS.md bytes | 22,750 | 8,982 | -13,768.00 |
| dot_codex/AGENTS.md approx_tokens | 5,687.5 | 2,245.5 | -3,442.00 |
| Developer-instruction tokens | 179.25 | 179.25 | +0.00 |
| Skill-description tokens | 3,365.5 | 1,181.75 | -2,183.75 |
| SKILL.md body bytes | 403,458 | 181,892 | -221,566.00 |
| Canonical skill count | 59 | 27 | -32.00 |
| Always-loaded tokens/session | 9,404.75 | 3,779 | -5,625.75 |
| Trigger exact-set accuracy | unavailable | 42/46 (91.30%) | unavailable |
| Automated tests passed | unavailable | 230 | unavailable |

Trigger and test counts are unavailable without matching committed evidence.
Routing scores from different corpora are not comparable; lexical proxy scores
do not establish actual model routing. Test counts cover only their recorded command.

## Pass commits

Every row comes from `git log --reverse ORIGINAL..HEAD`; no draft, planned pass
or inferred test result is promoted to a commit. L/B/T means lines/bytes/tokens.
The two delta columns measure always-loaded tokens.

| Commit | Pass | Technique | Root AGENTS L/B/T | Canonical AGENTS L/B/T | Developer T | Description T | Body B | Skills | Largest body B | Trigger | Tests | Loaded T | Δ previous | Δ original |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| bc0360c | Approved cull | Evidence-ranked cull, overlap merges and calibration maintenance | 16/690/172.5 | 356/22,985/5,746.25 | 179.25 | 1,310 | 138,102 | 22 | dot_agents/skills/last30days/SKILL.md: 29,889 | 15/17 (88.24%) | 82 | 7,408 | -1,996.75 | -1,996.75 |
| 60c6e70 | Pass 2 approved intake | Privacy-screened complementary imports and pinned same-slot replacement | 16/690/172.5 | 357/23,106/5,776.5 | 179.25 | 1,434.5 | 179,494 | 27 | dot_agents/skills/last30days/SKILL.md: 29,889 | 41/46 (89.13%) | 192 | 7,562.75 | +154.75 | -1,842.00 |
| 6e9934c | Pass 3 admission gate | Evidence-priced additions and mandatory PASS ledger | 16/690/172.5 | 357/23,147/5,786.75 | 179.25 | 1,434.5 | 183,100 | 27 | dot_agents/skills/last30days/SKILL.md: 29,889 | 41/46 (89.13%) | 198 | 7,573 | +10.25 | -1,831.75 |
| f0a1cbb | Pass 4 CASD conditional policy | Log-informed conditional policy routing | 16/690/172.5 | 145/8,982/2,245.5 | 179.25 | 1,434.5 | 184,312 | 27 | dot_agents/skills/last30days/SKILL.md: 29,889 | 41/46 (89.13%) | 200 | 4,031.75 | -3,541.25 | -5,373.00 |
| 60f75a4 | Pass 5 body concision | Repeated technique prose compressed in place | 16/690/172.5 | 145/8,982/2,245.5 | 179.25 | 1,434.5 | 180,084 | 27 | dot_agents/skills/last30days/SKILL.md: 29,889 | 41/46 (89.13%) | 200 | 4,031.75 | +0.00 | -5,373.00 |
| 5efb06a | Pass 6 owned descriptions | Trigger words retained; procedure stays in bodies | 16/690/172.5 | 145/8,982/2,245.5 | 179.25 | 1,181.75 | 180,989 | 27 | dot_agents/skills/last30days/SKILL.md: 29,889 | 42/46 (91.30%) | 200 | 3,779 | -252.75 | -5,625.75 |
| c24871f | Pass 7 agent tool output | Summaries with complete explicit diagnostics | 16/690/172.5 | 145/8,982/2,245.5 | 179.25 | 1,181.75 | 181,892 | 27 | dot_agents/skills/last30days/SKILL.md: 29,889 | 42/46 (91.30%) | 230 | 3,779 | +0.00 | -5,625.75 |

## Always-loaded cost by commit

```text
Original   ######################################## 9,404.75 tokens
bc0360c    ################################         7,408 tokens
60c6e70    ################################         7,562.75 tokens
6e9934c    ################################         7,573 tokens
f0a1cbb    #################                        4,031.75 tokens
60f75a4    #################                        4,031.75 tokens
5efb06a    ################                         3,779 tokens
c24871f    ################                         3,779 tokens
```

## Largest canonical skill bodies

| Rank | Original skill | Body bytes | HEAD skill | Body bytes |
| ---: | --- | ---: | --- | ---: |
| 1 | dot_agents/skills/playwright-interactive/SKILL.md | 31,604 | dot_agents/skills/last30days/SKILL.md | 29,889 |
| 2 | dot_agents/skills/last30days/SKILL.md | 29,889 | dot_agents/skills/lean-instructions/SKILL.md | 12,705 |
| 3 | dot_agents/skills/design-taste-frontend/SKILL.md | 21,146 | dot_agents/skills/impeccable/SKILL.md | 11,985 |
| 4 | dot_agents/skills/redesign-existing-projects/SKILL.md | 15,010 | dot_agents/skills/frontend-design/SKILL.md | 9,634 |
| 5 | dot_agents/skills/high-end-visual-design/SKILL.md | 10,542 | dot_agents/skills/commit-session/SKILL.md | 9,532 |
| 6 | dot_agents/skills/delight/SKILL.md | 9,761 | dot_agents/skills/personal-context/SKILL.md | 8,384 |
| 7 | dot_agents/skills/overdrive/SKILL.md | 9,676 | dot_agents/skills/skill-eval/SKILL.md | 8,095 |
| 8 | dot_agents/skills/imagegen/SKILL.md | 9,577 | dot_agents/skills/metaprompt-run/SKILL.md | 7,922 |
| 9 | dot_agents/skills/commit-session/SKILL.md | 9,532 | dot_agents/skills/vercel-react-best-practices/SKILL.md | 7,359 |
| 10 | dot_agents/skills/frontend-design/SKILL.md | 9,178 | dot_agents/skills/commit-plan-push/SKILL.md | 7,191 |

## What moved the needle

| Rank | Technique | Net loaded tokens saved |
| ---: | --- | ---: |
| 1 | Log-informed conditional policy routing | +3,541.25 |
| 2 | Evidence-ranked cull, overlap merges and calibration maintenance | +1,996.75 |
| 3 | Trigger words retained; procedure stays in bodies | +252.75 |
| 4 | Repeated technique prose compressed in place | +0.00 |
| 5 | Summaries with complete explicit diagnostics | +0.00 |
| 6 | Evidence-priced additions and mandatory PASS ledger | -10.25 |
| 7 | Privacy-screened complementary imports and pinned same-slot replacement | -154.75 |

## Verification provenance

Optional `benchmarks/trim/pass-evidence.json` records `pass`, `technique`,
`commit_subject`, `tests: {passed, command}`, and
`trigger: {exact_matches, case_count, method, scope}`. The subject must match
the commit; absent, stale or invalid counts are unavailable. Store only safe
aggregate evidence here, never raw session logs or private data.

| Commit | Trigger method and corpus | Automated command |
| --- | --- | --- |
| bc0360c | deterministic lexical proxy; not model triggering; 17 unchanged original keeper/none cases; pre-cull 13/17. Not comparable to original 50-case corpus. | python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py |
| 60c6e70 | deterministic lexical proxy; not model triggering; All27 local names; includes unchanged17keeper/none cases. Original proposal baseline41/46; keepers15/17. | python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py tests/test_grok_cli_handoff.py tests/test_file_size_guard.py tests/test_ai_workflow_contract.py tests/test_pre_commit_privacy_gate.py tests/test_checkpoint_privacy_gate.py |
| 6e9934c | deterministic lexical proxy; not model triggering; All27 local names; includes unchanged17keeper/none cases. Original proposal baseline41/46; keepers15/17. | python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py tests/test_grok_cli_handoff.py tests/test_file_size_guard.py tests/test_ai_workflow_contract.py tests/test_pre_commit_privacy_gate.py tests/test_checkpoint_privacy_gate.py tests/test_skill_admissions.py |
| f0a1cbb | deterministic lexical proxy; not model triggering; All27 local names; includes unchanged17keeper/none cases. Original proposal baseline41/46; keepers15/17. | python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py tests/test_grok_cli_handoff.py tests/test_file_size_guard.py tests/test_ai_workflow_contract.py tests/test_pre_commit_privacy_gate.py tests/test_checkpoint_privacy_gate.py tests/test_skill_admissions.py tests/test_trim_casd.py |
| 60f75a4 | deterministic lexical proxy; not model triggering; All27 local names; includes unchanged17keeper/none cases. Original proposal baseline41/46; keepers15/17. | python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py tests/test_grok_cli_handoff.py tests/test_file_size_guard.py tests/test_ai_workflow_contract.py tests/test_pre_commit_privacy_gate.py tests/test_checkpoint_privacy_gate.py tests/test_skill_admissions.py tests/test_trim_casd.py |
| 5efb06a | deterministic lexical proxy; not model triggering; All27locals; frozenintake46 before41 after42, allpreviouspositives retained; keeper15/17 to16/17. | python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py tests/test_grok_cli_handoff.py tests/test_file_size_guard.py tests/test_ai_workflow_contract.py tests/test_pre_commit_privacy_gate.py tests/test_checkpoint_privacy_gate.py tests/test_skill_admissions.py tests/test_trim_casd.py |
| c24871f | deterministic lexical proxy; not model triggering; All27locals; frozenintake46 before41 after42, allpreviouspositives retained; keeper15/17 to16/17. | python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py tests/test_grok_cli_handoff.py tests/test_file_size_guard.py tests/test_ai_workflow_contract.py tests/test_pre_commit_privacy_gate.py tests/test_checkpoint_privacy_gate.py tests/test_skill_admissions.py tests/test_trim_casd.py tests/test_ai_workflow_doctor.py |

## Uncommitted working draft

Excluded from committed pass rows and savings ranking. These measurements
come from current files and may change during parallel edits; they do not
prove that pass commits, privacy gates or required checks have completed.

| Metric | Working draft | Change versus original |
| --- | ---: | ---: |
| AGENTS.md lines | 16 | +0.00 |
| AGENTS.md bytes | 690 | +0.00 |
| AGENTS.md approx_tokens | 172.5 | +0.00 |
| dot_codex/AGENTS.md lines | 145 | -208.00 |
| dot_codex/AGENTS.md bytes | 8,982 | -13,768.00 |
| dot_codex/AGENTS.md approx_tokens | 2,245.5 | -3,442.00 |
| Developer-instruction tokens | 179.25 | +0.00 |
| Skill-description tokens | 1,181.75 | -2,183.75 |
| SKILL.md body bytes | 182,828 | -220,630.00 |
| Canonical skill count | 27 | -32.00 |
| Always-loaded tokens/session | 3,779 | -5,625.75 |
| Trigger exact-set accuracy | 42/46 (91.30%) | corpus-dependent |
| Automated tests passed | 231 | unavailable |

Trigger scope: deterministic lexical proxy; not model triggering; All27locals; frozenintake46 before41 after42, allpreviouspositives retained; keeper15/17 to16/17..
Automated command: python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py tests/test_grok_cli_handoff.py tests/test_file_size_guard.py tests/test_ai_workflow_contract.py tests/test_pre_commit_privacy_gate.py tests/test_checkpoint_privacy_gate.py tests/test_skill_admissions.py tests/test_trim_casd.py tests/test_ai_workflow_doctor.py.

## Regeneration

From the repository root, run `python3 benchmarks/trim/update-comparison.py`
after inspecting actual commits. Add `--include-working` only to show a
separately labeled draft. `scripts/trim-benchmark --ref REF --json` exposes
the full inventory for any commit; `--ref` skips current working-tree budgets
and cannot be combined with `--check`. The original immutable BASELINE.json
supplies comparisons and is never rewritten.
