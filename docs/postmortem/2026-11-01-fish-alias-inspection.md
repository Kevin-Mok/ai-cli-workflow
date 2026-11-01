# Fish alias inspection environment

This report records inspection failures while adding a directory shortcut and an immediate commit step to the skill.

## Symptom and impact

A guessed scripts/*refresh* glob matched nothing (exit 2); a guessed sync-shortcuts function path was also absent. chezmoi confirmed the installed skill is unmanaged. A normal fish inspection triggered startup writes denied by the read-only home sandbox: fnm multishell links, universal variables and the installed shortcut catalog. No intended mapping had been applied; work continued using direct file reads and no-config fish.

## Lookup and cause

Read canonical postmortem-memory and searched `missing executable path glob inspection`. Existing execution-environment guidance applies: discover actual helper locations and avoid normal shell initialization for read-only inspection. Evidence: refresh-config is an autoload function under dot_config/fish/functions, while fish startup attempts writes outside the workspace.

## Resolution and status

Use the existing helper for the reviewed alias edit; run refresh-config with authorized home-write access. Read-only checks use fish --no-config. The inspection issue is resolved. The existing executable was found under ~/scripts; targeted live catalog and skill edits were deployed with approved home-write access, refresh-config exited 0, generated Fish syntax passed and the repeated request returned changed=false. Live activation verification is recorded in plans/fish-alias-immediate-commit.md. No production command was executed by inspecting the abbreviation.

## Follow-up

No new reusable learning: helper discovery and no-config inspections are already established practices. Preserve unrelated dirty work.
