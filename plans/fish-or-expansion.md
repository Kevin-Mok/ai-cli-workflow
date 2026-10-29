# Fix Fish or expansion

Make the requested directory shortcut expand interactively while retaining logical or.

## Context and scope
Generator scripts/executable_sync-shortcuts, existing fixture tests, and smoke docs. Preserve all pre-existing dirty work (status captured); commit-session now authorizes only directly observed session changes.

## Decisions
Fish3.7 skips command-position abbreviations for or. Anywhere alone breaks logical operators. Use a generated function guarded to a buffer containing only leading whitespace and or. Retain the existing directory mapping.

## Checklist
- [x] Reproduce normal rule failure and anywhere expansion in interactive PTYs.
- [x] Add RED interactive regression covering expansion and preserved logical or.
- [x] Implement guarded generated rule, update smoke docs and incident memory.
- [x] Deploy reviewed generator, refresh, run focused suite and live PTY verification.

## Verification
python3 -B tests/test_reserved_fish_shortcut.py; fish -n generated file; interactive capture after Space (never execute mapping). Expected cd destination, logical false; or unchanged.

## Risks and rollback
Only or directory mapping gets the special rule. Buffer guard deliberately restricts expansion to a fresh command line; logical operators and arguments must remain untouched. Revert generator hunk and regenerate to roll back. Existing open shells require sourcing regenerated abbreviations.

## Evidence and review
RED manual PTY capture was "or "; anywhere capture was the desired cd. Full refresh currently passed after MIME mode reconciliation.

Final evidence: standalone regression RED literal or, GREEN one test; live PTY passed standalone/logical/argument captures; bash -n and installed fish -n exit0; refresh exit0. Original fish-alias suite blocked by pre-existing invalid Python identifier; used standalone test. Reviewed generated guard and existing dirty work preserved. Commit-session authorized on main -> origin/main. Scope helper returned unsafe (no detected writes); use direct-write evidence and the initial dirty baseline. README gate pass_no_change and fresh focused regression/bash syntax passed.

## Delivery milestone
- Prepared `fix(fish): expand reserved or directory shortcut`: directory mapping, guarded generator, PTY regression, smoke instructions, three incident records and their scoped memory additions. Commit and push pending; all unrelated baseline changes excluded.
- Remaining limitation: expansion starts only on a fresh command line; the pre-existing broad test syntax error remains outside scope.
