# ExecPlan: Manage Commit Plan & Push Picker Metadata

## Purpose and observable outcome

Move the existing user-scoped `commit-plan-push` skill into the repo-tracked
`dot_agents/skills/` source, give its picker entry the exact label `Commit Plan
& Push`, and deploy the managed copy to `~/.agents/skills/`. The stable skill
slug remains `commit-plan-push`.

## Current context and scope

- Live but unmanaged source: `/home/example/.agents/skills/commit-plan-push/SKILL.md`.
- Managed companion patterns: `dot_agents/skills/commit-plan/` and
  `dot_agents/skills/commit-dirty/`.
- Documentation surfaces: `dot_agents/skills/README.md` and
  `docs/smoke-tests.md`; the root README already accurately describes the
  generic local-skill install path and needs no wording change.
- Protected pre-existing dirty state: `scripts/executable_install-tmux-tpm.sh`
  is untracked and excluded from this work.
- Scope excludes changes to the skill workflow, its slug, unrelated skills,
  the pre-existing untracked script, commits, and pushes.

## Assumptions and decisions

- Codex documents `interface.display_name` in `agents/openai.yaml` for the
  picker label but documents no picker-order or priority field. Use the exact
  requested title without inventing unsupported metadata; host ordering remains
  outside this repository's control.
- The tracked source is authoritative. `refresh-config` applies it to the live
  `~/.agents/skills/` path, but its live-to-repo Codex-config snapshot must be
  checked first to avoid overwriting unrelated work.
- The existing global skill text is preserved verbatim apart from the required
  managed metadata; this task changes presentation and persistence, not commit
  behavior.

## Checklist

- [x] Capture the initial Git status and identify protected dirty state.
- [x] Inspect the live skill, companion source patterns, feedback, lessons,
  smoke checklist, and official Codex metadata documentation.
- [x] Add a focused failing contract test for the managed skill source, picker
  title, catalog entry, and installed-copy parity.
- [x] Run the focused test and record the expected RED failure.
- [x] Create the managed skill source and exact `Commit Plan & Push` metadata.
- [x] Catalog the skill and update the existing installed-skill smoke check.
- [x] Run the focused contract test, skill validator, relevant workflow
  regression, and formatting checks for GREEN.
- [x] Run the protected config snapshot check, defer full `refresh-config`, and
  verify live source parity without touching protected unrelated work.
- [x] Record final evidence, review notes, rollback, and unresolved limits.

## Risks, edge cases, and rollback

- Risk: an unsupported metadata key could imply picker ordering without taking
  effect. Mitigation: use only the documented display metadata and record the
  host-controlled ordering limitation.
- Risk: `refresh-config` snapshots live `~/.codex/config.toml` into the tracked
  source. Mitigation: compare the protected source hash and snapshot dry-run
  before applying; stop if the snapshot would create unrelated changes.
- Risk: source and installed skill may drift. Mitigation: verify the installed
  `SKILL.md` and `agents/openai.yaml` match their tracked sources after apply.
- Rollback: remove the new managed source files and run `refresh-config`; no
  commit history or existing companion skill is changed by this task.

## Verification

- RED: `python3 -m unittest tests/test_commit_plan_push_skill.py -v` must fail
  before the managed source and picker metadata exist.
- GREEN: the same test validates the slug, exact title, catalog entry, smoke
  check, and installed-copy parity after deployment.
- Regression: run the relevant AI workflow contract, the skill validator, and
  `git diff --check`.
- Manual: open the Codex skill picker after detection or restart and confirm
  the visible title is `Commit Plan & Push`; picker placement is host-managed.

## Progress, evidence, and review notes

- 2026-08-11: Confirmed Codex 0.147.0 documents `interface.display_name` but
  no priority or ordering setting for standalone skills. The live
  `commit-plan-push` directory is unmanaged by chezmoi; its tracked source
  must be added before applying it.
- 2026-08-11: RED observed: `python3 tests/test_commit_plan_push_skill.py -v`
  failed because the tracked skill source, picker metadata, catalog entry, and
  smoke entry were absent. GREEN: all three focused tests passed after the
  managed source and documented metadata were added; the skill validator
  reported `Skill is valid!`, `python3 tests/test_ai_workflow_contract.py -v`
  passed 11 tests, and `git diff --check` passed.
- 2026-08-11: `snapshot-codex-config --dry-run` passed without changing files,
  but live `~/.codex/config.toml` differed from the clean tracked source. Full
  `refresh-config` was therefore deferred to avoid an unrelated overwrite.
  `chezmoi apply /home/example/.agents/skills/commit-plan-push` safely deployed
  only this target; both installed files matched their sources with `cmp -s`
  exit status 0.
- Review: rollback removes the managed skill directory and reruns its exact
  chezmoi target apply. Codex exposes no supported picker-priority metadata,
  so the exact title is deployed but the picker controls final placement.
