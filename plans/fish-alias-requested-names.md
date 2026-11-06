# Preserve requested fish shortcut names

Repair the literal `btw` abbreviation and make future file shortcut requests retain their requested name. Diagnose and test first, change the existing helper and skill, then deploy and verify the exact name before focused delivery.

## Scope and decisions

- New file requests use `$EDITOR <escaped path>` in `aliases/key_aliases.tmpl`; first token is the literal abbreviation. Existing key_files mappings keep their `n` prefix. No new catalog format or generator behavior.
- Keep previously delivered `nbtw` as a harmless compatibility shortcut. Do not execute either editor mapping. No notes content is read or committed.
- Change helper/tests, skill/README/smoke docs, admission costs and required progress/comparison evidence; include report and learning ledger. Preserve all initial dirty files/hunks (same unrelated state as preceding shortcut task).
- Refresh is scoped to reviewed skill/catalog deployment and shortcut generation because broad managed-file apply would affect unrelated work.

## Ordered implementation

- [x] Inspect helper/generator/callers and diagnose derived-name verification gap.
- [x] Observe RED for a requested file name, legacy preservation and conflict handling.
- [x] Record lean skill-edit PASS and make minimum helper/instruction change.
- [x] Run GREEN focused tests, admissions/routing/budgets and syntax checks; update docs/learning.
- [x] Deploy exact reviewed skill/catalog changes; run refresh and verify literal `btw` with real interactive Space without execution.
- [x] Prepare focused staging and delivery sequence; commit/push origin/main with normal hooks follows verified activation.

## Verification

Use `python3 -B tests/test_fish_alias.py` (including generated source readback for literal file names, legacy nre and no-op/conflicts); admissions unittest, trim/trigger gates and inventory check. After deployment run `python3 scripts/executable_check-fish-abbr btw '$EDITOR ~/coding/btw.md'`; run no-argument trial only if checker/generator changes. Manual: source installed abbreviations in an existing fish shell, type btw + Space and cancel. Opening the editor is intentionally skipped.

## Risks and rollback

Path metacharacters must remain escaped; file requests now report command storage. Legacy generators remain untouched. Existing shells need reload. Revert focused commit and remove only the new literal live row to roll back; preserve notes and the legacy nbtw row.

## Progress and review

Initial diagnosis is supported by source and previous activation output. Await RED evidence before implementation. Plan Mode unavailable in this active runtime; this ExecPlan records the implementation contract.

RED: focused literal-name regression ran 1 test and failed with actual nbtw versus expected btw (exit 1), after correcting an inherited invalid Python test identifier. Admission PASS recorded before skill edit; implementation adds only file-to-editor-command routing and preserves the generator.

GREEN: 22 shortcut tests passed, including exact literal-name readback, escaped spaces, legacy nre, conflict handling and no-op. Seven admission tests passed after matching benchmark body7085B. Frozen lexical routing 46/51 (90.20%) PASS; skill inventory241 entries/0 missing-stale PASS; helper AST valid. No configured repository type-check command exists. README gate pass_no_change. Trim gate still fails the exact same pre-edit canonical instruction byte/line and total-loaded-byte ceilings; no new budget failure. Independent diff review requested an escaped-space readback, now included and passing.

Cursor handoff prompt: Review plans/fish-alias-requested-names.md and verify the requested literal file shortcut, escaped paths, existing legacy names, and no-execution activation checks; preserve unrelated dirty work. Atomic commit: `fix(fish): preserve requested file shortcut names`.

Activation: reviewed installed skill body/helper updated (host path remapping retained; existing installed description preserved), only literal btw row added to preserved live command catalog. Scoped refresh exited0 and checker PASS `btw + Space -> $EDITOR ~/coding/btw.md; never executed`. Legacy nbtw remains. Manual existing-shell editor launch and wrapped terminal-copy behavior are unverified.

Delivery milestone: `fix(fish): preserve requested file shortcut names`; implementation and required docs complete, no implementation blockers. Next step is focused stage/review/commit and configured origin/main push; actual hash and push result are reported in the conversation. Revert this commit and remove only the literal live command row for rollback.

## Follow-up: explicit Neovim for file shortcuts

User requests nvim for key_files mappings and automatic nvim opening for file inputs to fish-alias. Preserve literal requested names for new mappings and existing prefixed names for legacy file rows. Scope: helper’s file command, generator’s Fish/Bash/Ranger editor selection, current btw command, tests, skill/README/smoke docs, admission costs, feedback and benchmark evidence. No general EDITOR setting change or editor launch.

- [x] RED: assert nvim for file requests and every generated consumer while EDITOR names a different editor.
- [x] Record skill-edit PASS; switch helper/generator/current btw mapping and update relevant docs.
- [x] GREEN: shortcut/admission tests, frozen routing/inventory, generator syntax, README gate. Compare existing broad budget failures.
- [x] Deploy only reviewed installed skill/helper/generator and btw row, refresh, run disposable trial and exact btw/nbtw/legacy file expansion checks without execution.
- [x] Prepare focused commit `fix(fish): open file shortcuts in Neovim` and configured origin/main push, preserving all unrelated work.

Rollback: revert this follow-up and restore prior reviewed live helper/generator/command row. Neovim exists at /usr/local/bin/nvim. Actual editor opening and existing-shell reload are manual checks; do not execute notes mappings during automation.

Neovim RED: two focused tests failed as expected, with actual $EDITOR vs expected nvim for new file requests and generated file mappings (exit1). Existing admission row refreshed before editing the skill; existing precedent/uniqueness and frozen shortcut case retained. Implementation changes editor selection only.

Neovim GREEN:23 shortcut tests and7 admission tests pass; frozen routing46/51 PASS; generator Bash syntax and helper AST pass; README gate pass_no_change. Broad trim failures match the pre-edit snapshot exactly. Inventory reports two unrelated installed no-mistakes calibration gaps (243 entries); recorded in docs/postmortem/2026-11-06-neovim-shortcut-inventory.md with no-new-learning ledger coverage. Independent diff review found no functional issue.

Neovim activation: installed helper preview reports target nvim ~/coding/btw.md and changed=false; scoped refresh exits0. Disposable trial passes and confirms removal. Real interactive checks pass for btw/nbtw→nvim ~/coding/btw.md and nre→nvim README.md; no mapped command executed. Installed helper/generator are updated for future runs; existing shells need reload. Delivery milestone `fix(fish): open file shortcuts in Neovim` is ready for focused stage/review/commit and configured origin/main push; actual hash and push status follow in the conversation. Remaining warnings: existing broad trim ceilings and unrelated two-entry no-mistakes calibration gap.

Delivery scope: concurrent feedback additions triggered the snapshot guard. Stage only the exact owned Neovim preference over HEAD; preserve all other concurrent feedback and earlier dirty work. No runtime source or activation result changed.
