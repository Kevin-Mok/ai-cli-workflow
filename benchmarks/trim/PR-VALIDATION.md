# Isolated skills review against exact main

Compare exact main 410feaa with the integrated skills proposal before activation. Read the measured costs, inspect the common routing cases, then review the isolated test results and limitations.

## Fresh comparison

| Measure | Main 410feaa | Integrated candidate |
| --- | ---: | ---: |
| Loaded bytes | 37,908 | 14,399 |
| Estimated tokens (bytes / 4) | 9,477 | 3,599.75 |
| Core AGENTS bytes | 23,039 | 8,982 |
| Skill body bytes (on demand) | 403,458 | 179,490 |
| Canonical skills | 59 | 27 |
| Common keeper proxy matches | 12/16 | 15/16 |

Loaded estimate falls 62.02% against exact main. Original pre-improvement 3e898a0f measured 37,619 bytes; main adds a 289-byte rule. The integrated version retains that rule verbatim in mandatory delivery guidance and explicitly routes repository creation there. No original budget was relaxed.

## Isolated execution evidence

- Candidate focused suite: 240 tests and 391 subtests passed, exit 0. Exact command: the command in benchmarks/trim/pass-evidence.json plus tests/test_trim_main_integration.py.
- Shared suite files: main 65 tests/14 subtests; candidate 64 tests/8 subtests, both exit 0. Files: tests/test_pre_commit_privacy_gate.py, tests/test_checkpoint_privacy_gate.py, tests/test_metaprompt_integration.py. Counts differ because the files evolved with approved culls; this is not a claim of identical cases.
- Core-budget integration reproducer: expected RED at 9,271 bytes; retained rule relocated to mandatory delivery, then GREEN at 8,982 bytes. Repository-creation route assertion also observed RED then GREEN.
- Original frozen keeper cases are filtered mechanically only where expected skill labels exist in both catalogs. Excluded instructions-edit (new lean-instructions skill absent on main); all other 16 prompts and expectations unchanged. Before 12/16, after 15/16; no previously correct case lost. Remaining false positive: none-language selects morning. Full candidate keeper corpus: 16/17. Active intake corpus: 42/46. All are lexical proxies, not real model routing.
- Fresh benchmark budgets PASS; targeted rule-retention checks PASS; README gate pass_no_change.

## Reproduce

Use scripts/trim-benchmark --ref 410feaa --json for exact-main metrics and scripts/trim-benchmark --check --plain for the current candidate. scripts/trigger-eval --check --plain exercises active routing. For historical snapshots, use git archive of each pinned commit into disposable directories; expose source Git history read-only for tests that call git show. Overlay the integration's reviewed delta into the candidate snapshot. The same current collector (runpy.run_path('scripts/trim-benchmark')['collect']) measures all three trees, avoiding missing baseline budget-file assumptions.

The disposable content trees are under /tmp/skills-pr-validation-20261023. Their .git files reference source history for read-only assertions; this is content isolation, not a separate OS or installed environment. Raw local logs are not committed. Machine-readable metrics, per-case outcomes and log hashes are in pr-validation.json. Initial setup failures are documented separately and do not count as final product failures.

## Merge boundary and limitations

Main is not merged or activated. No refresh-config, home configuration changes, installs, real model trials, latency or billing measurement. Full repository suite is not claimed green; inherited collection defects were previously recorded. Review skill removals and conditional guidance before merging. Revert the proposal with a new commit if needed.
