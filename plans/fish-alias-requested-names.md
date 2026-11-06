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
