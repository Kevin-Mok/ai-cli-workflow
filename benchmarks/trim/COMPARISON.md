# Trim comparison

Reproduce instruction costs from committed Git blobs, compare the original with HEAD,
then inspect real pass commits and their recorded verification. An optional working
draft is reported separately and never counts as a committed pass.

Always-loaded tokens per session: **9,404.75 → 9,404.75**
(+0.00 tokens, +0.00%).

Original: `3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c`. HEAD: `3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c`.

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
| dot_codex/AGENTS.md lines | 353 | 353 | +0.00 |
| dot_codex/AGENTS.md bytes | 22,750 | 22,750 | +0.00 |
| dot_codex/AGENTS.md approx_tokens | 5,687.5 | 5,687.5 | +0.00 |
| Developer-instruction tokens | 179.25 | 179.25 | +0.00 |
| Skill-description tokens | 3,365.5 | 3,365.5 | +0.00 |
| SKILL.md body bytes | 403,458 | 403,458 | +0.00 |
| Canonical skill count | 59 | 59 | +0.00 |
| Always-loaded tokens/session | 9,404.75 | 9,404.75 | +0.00 |
| Trigger exact-set accuracy | unavailable | unavailable | unavailable |
| Automated tests passed | unavailable | unavailable | unavailable |

Trigger and test counts are unavailable without matching committed evidence.
Routing scores from different corpora are not comparable; lexical proxy scores
do not establish actual model routing. Test counts cover only their recorded command.

## Pass commits

Every row comes from `git log --reverse ORIGINAL..HEAD`; no draft, planned pass
or inferred test result is promoted to a commit. L/B/T means lines/bytes/tokens.
The two delta columns measure always-loaded tokens.

| Commit | Pass | Technique | Root AGENTS L/B/T | Canonical AGENTS L/B/T | Developer T | Description T | Body B | Skills | Largest body B | Trigger | Tests | Loaded T | Δ previous | Δ original |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |

No pass commits exist in the requested range.

## Always-loaded cost by commit

```text
Original   ######################################## 9,404.75 tokens
```

## Largest canonical skill bodies

| Rank | Original skill | Body bytes | HEAD skill | Body bytes |
| ---: | --- | ---: | --- | ---: |
| 1 | dot_agents/skills/playwright-interactive/SKILL.md | 31,604 | dot_agents/skills/playwright-interactive/SKILL.md | 31,604 |
| 2 | dot_agents/skills/last30days/SKILL.md | 29,889 | dot_agents/skills/last30days/SKILL.md | 29,889 |
| 3 | dot_agents/skills/design-taste-frontend/SKILL.md | 21,146 | dot_agents/skills/design-taste-frontend/SKILL.md | 21,146 |
| 4 | dot_agents/skills/redesign-existing-projects/SKILL.md | 15,010 | dot_agents/skills/redesign-existing-projects/SKILL.md | 15,010 |
| 5 | dot_agents/skills/high-end-visual-design/SKILL.md | 10,542 | dot_agents/skills/high-end-visual-design/SKILL.md | 10,542 |
| 6 | dot_agents/skills/delight/SKILL.md | 9,761 | dot_agents/skills/delight/SKILL.md | 9,761 |
| 7 | dot_agents/skills/overdrive/SKILL.md | 9,676 | dot_agents/skills/overdrive/SKILL.md | 9,676 |
| 8 | dot_agents/skills/imagegen/SKILL.md | 9,577 | dot_agents/skills/imagegen/SKILL.md | 9,577 |
| 9 | dot_agents/skills/commit-session/SKILL.md | 9,532 | dot_agents/skills/commit-session/SKILL.md | 9,532 |
| 10 | dot_agents/skills/frontend-design/SKILL.md | 9,178 | dot_agents/skills/frontend-design/SKILL.md | 9,178 |

## What moved the needle

No committed technique savings yet. Uncommitted reductions cannot establish a completed pass.

## Verification provenance

Optional `benchmarks/trim/pass-evidence.json` records `pass`, `technique`,
`commit_subject`, `tests: {passed, command}`, and
`trigger: {exact_matches, case_count, method, scope}`. The subject must match
the commit; absent, stale or invalid counts are unavailable. Store only safe
aggregate evidence here, never raw session logs or private data.

| Commit | Trigger method and corpus | Automated command |
| --- | --- | --- |
| 3e898a0 | unavailable | unavailable |

## Uncommitted working draft

Excluded from committed pass rows and savings ranking. These measurements
come from current files and may change during parallel edits; they do not
prove that pass commits, privacy gates or required checks have completed.

| Metric | Working draft | Change versus original |
| --- | ---: | ---: |
| AGENTS.md lines | 16 | +0.00 |
| AGENTS.md bytes | 690 | +0.00 |
| AGENTS.md approx_tokens | 172.5 | +0.00 |
| dot_codex/AGENTS.md lines | 356 | +3.00 |
| dot_codex/AGENTS.md bytes | 22,985 | +235.00 |
| dot_codex/AGENTS.md approx_tokens | 5,746.25 | +58.75 |
| Developer-instruction tokens | 179.25 | +0.00 |
| Skill-description tokens | 1,310 | -2,055.50 |
| SKILL.md body bytes | 138,102 | -265,356.00 |
| Canonical skill count | 22 | -37.00 |
| Always-loaded tokens/session | 7,408 | -1,996.75 |
| Trigger exact-set accuracy | 15/17 (88.24%) | corpus-dependent |
| Automated tests passed | 82 | unavailable |

Trigger scope: deterministic lexical proxy; not model triggering; 17 unchanged original keeper/none cases; pre-cull 13/17. Not comparable to original 50-case corpus..
Automated command: python3 -m pytest -q tests/test_skill_cull_contract.py tests/test_commit_plan_push_skill.py tests/test_metaprompt_integration.py tests/test_cli_emoji_skills.py tests/test_trim_benchmark.py tests/test_trigger_eval.py tests/test_trim_failure_mining.py tests/test_design_skills_sync.py tests/test_superpowers_release_timer.py tests/test_vetted_skills.py.

## Regeneration

From the repository root, run `python3 benchmarks/trim/update-comparison.py`
after inspecting actual commits. Add `--include-working` only to show a
separately labeled draft. `scripts/trim-benchmark --ref REF --json` exposes
the full inventory for any commit; `--ref` skips current working-tree budgets
and cannot be combined with `--check`. The original immutable BASELINE.json
supplies comparisons and is never rewritten.
