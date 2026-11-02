# Fish alias immediate commit and ChartClutch shortcut

Update fish-alias to commit verified shortcut changes immediately, then add cc for ChartClutch, activate it and commit/push this focused change.

## Scope and decisions

Change the tracked skill and aliases/key_{aliases,dirs}.tmpl. Keep cc Calcurse as a comment; store ~/coding/chartclutch in cdn. Update the existing smoke checklist with only this task’s hunk. Existing README, backup, Vesktop, memory-ledger and report edits are protected and excluded. Current branch main tracks origin/main at Kevin-Mok/ai-cli-workflow. No worktree or history rewrite.

## Checklist

- [x] Capture baseline git status and inspect skill and alias sources.
- [x] RED: independent skill review confirms no immediate scoped commit or no-op rule. Helper preview identifies one active Calcurse conflict.
- [x] Add immediate commit instruction and apply reviewed mapping.
- [x] Refresh, verify installed abbreviation and repeated-request no-op; review updated skill.
- [ ] Run README gate, review exact scoped staged diff, commit and push origin/main.

## Verification and risks

Use helper preview/apply JSON, fish -n and isolated abbr --show; do not execute mapped commands. Review skill for immediate commit, protected unrelated changes and no-op exclusion. Manual: source key_abbr.fish in existing Fish, type cc Space, inspect expansion and cancel. Risks: older live catalogs may be ignored by chezmoi; reconcile only the reviewed mapping before refresh. Refresh can preserve live files into source, so inspect and exclude incidental changes. Rollback restores the commented Calcurse mapping and removes the directory mapping, then refreshes.

## Progress and review

Scope is documentation and a template mapping; helper implementation unchanged. See docs/postmortem/2026-11-01-fish-alias-inspection.md for inspection-only failures. Baseline review RED confirmed; live checks and delivery pending.

Fresh evidence: refresh-config exited 0 with approved home-write access. Live catalogs and installed skill were unmanaged; only reviewed cc lines and the commit paragraph were reconciled. fish -n exited 0; repeated helper preview returned changed=false, conflicts=0. Independent review confirmed GREEN for immediate commit, scoped staging and no-op behavior. README gate returned pass_no_change; no README changes included. Full helper suite skipped because helper implementation is unchanged; manual interactive typing is not exercised.

Atomic plan complete except delivery: focused commit `feat(fish): commit shortcut changes immediately and add cc`, then push origin/main. Verification uses the installed helper preview and isolated abbreviation inspection. Rollback uses the source edits described above. Cursor continuation prompt: “Read this plan; preserve baseline dirty work, verify cc and the installed commit paragraph, review only this task’s staged diff, then commit and push the configured upstream without rewriting history.”
