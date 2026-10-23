# Trim comparison

Reproduce instruction costs from committed Git blobs, compare the original with HEAD,
then inspect real pass commits and their recorded verification. An optional working
draft is reported separately and never counts as a committed pass.

Always-loaded tokens per session: **9,404.75 → 7,408**
(-1,996.75 tokens, -21.23%).

Original: `3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c`. HEAD: `bc0360c9a59610469526c45d83efefb82f296382`.

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
| dot_codex/AGENTS.md lines | 353 | 356 | +3.00 |
| dot_codex/AGENTS.md bytes | 22,750 | 22,985 | +235.00 |
| dot_codex/AGENTS.md approx_tokens | 5,687.5 | 5,746.25 | +58.75 |
| Developer-instruction tokens | 179.25 | 179.25 | +0.00 |
| Skill-description tokens | 3,365.5 | 1,310 | -2,055.50 |
| SKILL.md body bytes | 403,458 | 138,102 | -265,356.00 |
| Canonical skill count | 59 | 22 | -37.00 |
| Always-loaded tokens/session | 9,404.75 | 7,408 | -1,996.75 |
| Trigger exact-set accuracy | unavailable | 15/17 (88.24%) | unavailable |
| Automated tests passed | unavailable | 82 | unavailable |

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

## Always-loaded cost by commit

```text
Original   ######################################## 9,404.75 tokens
bc0360c    ################################         7,408 tokens
```

## Largest canonical skill bodies

| Rank | Original skill | Body bytes | HEAD skill | Body bytes |
| ---: | --- | ---: | --- | ---: |
| 1 | dot_agents/skills/playwright-interactive/SKILL.md | 31,604 | dot_agents/skills/last30days/SKILL.md | 29,889 |
| 2 | dot_agents/skills/last30days/SKILL.md | 29,889 | dot_agents/skills/frontend-design/SKILL.md | 9,634 |
| 3 | dot_agents/skills/design-taste-frontend/SKILL.md | 21,146 | dot_agents/skills/commit-session/SKILL.md | 9,532 |
| 4 | dot_agents/skills/redesign-existing-projects/SKILL.md | 15,010 | dot_agents/skills/lean-instructions/SKILL.md | 8,818 |
| 5 | dot_agents/skills/high-end-visual-design/SKILL.md | 10,542 | dot_agents/skills/personal-context/SKILL.md | 8,384 |
| 6 | dot_agents/skills/delight/SKILL.md | 9,761 | dot_agents/skills/metaprompt-run/SKILL.md | 7,922 |
| 7 | dot_agents/skills/overdrive/SKILL.md | 9,676 | dot_agents/skills/commit-plan-push/SKILL.md | 7,191 |
| 8 | dot_agents/skills/imagegen/SKILL.md | 9,577 | dot_agents/skills/next-tasks/SKILL.md | 5,540 |
| 9 | dot_agents/skills/commit-session/SKILL.md | 9,532 | dot_agents/skills/fish-alias/SKILL.md | 5,437 |
| 10 | dot_agents/skills/frontend-design/SKILL.md | 9,178 | dot_agents/skills/commit-dirty/SKILL.md | 5,416 |

## What moved the needle

| Rank | Technique | Net loaded tokens saved |
| ---: | --- | ---: |
| 1 | Evidence-ranked cull, overlap merges and calibration maintenance | +1,996.75 |

## Verification provenance

Optional `benchmarks/trim/pass-evidence.json` records `pass`, `technique`,
`commit_subject`, `tests: {passed, command}`, and
`trigger: {exact_matches, case_count, method, scope}`. The subject must match
the commit; absent, stale or invalid counts are unavailable. Store only safe
aggregate evidence here, never raw session logs or private data.

| Commit | Trigger method and corpus | Automated command |
| --- | --- | --- |
| bc0360c | deterministic lexical proxy; not model triggering; 17 unchanged original keeper/none cases; pre-cull 13/17. Not comparable to original 50-case corpus. | python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py |

## Uncommitted working draft

Excluded from committed pass rows and savings ranking. These measurements
come from current files and may change during parallel edits; they do not
prove that pass commits, privacy gates or required checks have completed.

| Metric | Working draft | Change versus original |
| --- | ---: | ---: |
| AGENTS.md lines | 16 | +0.00 |
| AGENTS.md bytes | 690 | +0.00 |
| AGENTS.md approx_tokens | 172.5 | +0.00 |
| dot_codex/AGENTS.md lines | 357 | +4.00 |
| dot_codex/AGENTS.md bytes | 23,106 | +356.00 |
| dot_codex/AGENTS.md approx_tokens | 5,776.5 | +89.00 |
| Developer-instruction tokens | 179.25 | +0.00 |
| Skill-description tokens | 1,434.5 | -1,931.00 |
| SKILL.md body bytes | 179,494 | -223,964.00 |
| Canonical skill count | 27 | -32.00 |
| Always-loaded tokens/session | 7,562.75 | -1,842.00 |
| Trigger exact-set accuracy | 41/46 (89.13%) | corpus-dependent |
| Automated tests passed | 192 | unavailable |

Trigger scope: deterministic lexical proxy; not model triggering; All27 local names; includes unchanged17keeper/none cases. Original proposal baseline41/46; keepers15/17..
Automated command: python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py tests/test_grok_cli_handoff.py tests/test_file_size_guard.py tests/test_ai_workflow_contract.py tests/test_pre_commit_privacy_gate.py tests/test_checkpoint_privacy_gate.py.

## Regeneration

From the repository root, run `python3 benchmarks/trim/update-comparison.py`
after inspecting actual commits. Add `--include-working` only to show a
separately labeled draft. `scripts/trim-benchmark --ref REF --json` exposes
the full inventory for any commit; `--ref` skips current working-tree budgets
and cannot be combined with `--check`. The original immutable BASELINE.json
supplies comparisons and is never rewritten.
