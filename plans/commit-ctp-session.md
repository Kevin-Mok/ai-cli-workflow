# Commit ctp shortcut session

Ship the ctp shortcut and its verification documentation as one focused commit, then push main to origin/main while preserving other sessions' work.

## Scope and decisions

Session: 01a11cfa-b056-7ef0-b9e9-dbde91247324. The scope helper returned unsafe because it detected no successful writes; direct conversation write evidence establishes ownership. The initial status was captured before edits. Include aliases/key_aliases.tmpl's single ctp line, only the ctp paragraph in docs/smoke-tests.md, the ctp incident and only its ledger record, and this plan. README, directory aliases, fish skill/tests, fish-home plan/incident, and unrelated ledger/smoke hunks remain protected. No command mapped by ctp is executed.

## Ordered checklist

- [x] Read instructions, scope helper, baseline, diff, upstream, and README contract.
- [x] Add ctp to work with zero conflicts; refresh-config exits 0.
- [x] README gate: pass_no_change; no README repair needed.
- [x] Run fresh syntax, expansion, no-op and targeted incident checks.
- [x] Stage only reviewed session hunks and inspect staged diff.
- [x] Prepared commit milestone: feat(aliases): add Codex time projects shortcut.
- [ ] Push the verified commit to origin/main and report residual dirty state.

## Verification

fish -n ~/.config/fish/key_abbr.fish must exit 0. Inspect abbr --show filtered to ctp: codex-time projects. Repeat helper preview with JSON input ctp codex-time projects: changed false, conflicts 0. Run targeted postmortem check: errors empty. git diff --cached --check must pass. Verify staged JSON independently of other dirty records. README gate returned pass_no_change.

## Risks and review

Shared working tree contains concurrent edits. Stage mixed files from HEAD plus explicit session additions; never stage entire mixed files. Ordinary sandbox is unavailable; approved scoped execution works. No code logic changed, so syntax and exact source/runtime assertions provide proportionate verification. Rollback is removal of the single mapping followed by refresh-config; retain incident evidence. No history rewrite is authorized.

## Commit milestone overview

Completed: ctp expansion installed; smoke documentation and incident learning recorded. Verified: refresh-config exit 0, prior syntax/expansion and no-op checks, README gate. Fresh verification: fish syntax exits 0; installed ctp equals codex-time projects; repeat preview changed false with zero conflicts; targeted incident check errors empty. Staged diff and JSON reviewed; no unrelated hunks included. Milestone is ready for commit and upstream push; push result is reported in the final handoff. Blockers: none for delivery; sandbox workaround remains necessary. Next: stage scoped additions and deliver one commit.
