# Fish shortcut verification sandbox restriction

A read-only shortcut check started normal fish initialization, which attempted writes outside the workspace. This report records the initial restriction and the verified installed-shortcut repair below.

- Symptom: fish startup reported read-only errors for fnm multishell links, universal variables, and generated aliases.
- Impact: normal-shell verification was inconclusive; no alias edits were necessary.
- Evidence: helper preview found tv ~/coding/jay-tradingview in the cdn section, changed=false, conflicts=0. The installed key_abbr.fish lacked tv; fish -n passed.
- Lookup: searched fish read-only universal variable fnm. Returned remote-login and benchmark-startup findings did not establish a remedy for local sandbox restrictions.
- Cause: normal startup performs writes beyond the permitted workspace.
- Initial status: source mapping verified, installed activation unverified. The follow-up below supersedes this initial assessment.
- Next steps: inspect or refresh from an authorized normal user environment if tv is unavailable interactively.
- Learning: no new reusable finding; environment-specific verification restriction, with no application bug demonstrated.

## Follow-up: installed shortcut repaired

The user confirmed tv did not work. A no-config fish reproducer sourcing installed key_abbr.fish returned 1 for abbr --query tv. Refresh completed but the reproducer still failed: chezmoi reported ~/aliases/key_dirs as unmanaged, and that file lacked tv despite the source template containing it. The installed file was older than the template.

Preserved all installed mappings and appended the existing source entry to the unmanaged installed directory file, then ran refresh-config successfully. A fresh no-config fish sourcing installed key_abbr.fish now returns 0 and shows abbr -a -- tv 'cd ~/coding/jay-tradingview'. fish -n also returns 0. Existing interactive shells may need to source the regenerated file.

Lookup: local-shortcut-stored-text-verification recommends isolated fish inspection and applies to verifying exact expansion. No generator code change was needed. The initial missing-file exploratory commands also failed because guessed source paths did not exist; actual generator is scripts/executable_sync-shortcuts.

Learning: source idempotence does not establish deployed activation. For this incident, the verified repair is installed-file reconciliation plus regeneration; general unmanaged-source deployment policy remains outside this shortcut request.
