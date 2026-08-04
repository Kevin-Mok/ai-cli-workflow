# ExecPlan: Add the global commit-plan-push skill

## Purpose and observable outcome

Create `/home/example/.agents/skills/commit-plan-push/SKILL.md`. On explicit
request, it plans coherent dirty-worktree commits in chronological order,
executes only a safe and verified plan, then pushes once after the full series.

## Current context and scope

- Companion skills: `/home/example/.agents/skills/commit-plan/SKILL.md` and
  `/home/example/.agents/skills/commit-dirty/SKILL.md`.
- Repository planning rules: `.agent/PLANS.md`.
- Protected pre-existing dirty state: `README.md`, `docs/smoke-tests.md`,
  `dot_agents/skills/metaprompt/SKILL.md`,
  `tests/test_metaprompt_contract.py`, `plans/aerc-multi-account-mail.md`,
  `plans/save-metaprompt-prompts.md`,
  `scripts/executable_setup-aerc-mail.sh`, and
  `tests/scripts/executable_setup-aerc-mail_test.sh`.
- In scope: the new global skill and this design/plan record. No existing
  dirty file is part of this task.

## Assumptions and decisions

- The user approved a global companion skill named `commit-plan-push`.
- “Push immediately” means execute the inferred plan without a second user
  confirmation after safety checks, not push each intermediate commit.
- Ambiguous mixed changes, missing upstreams, failed checks, and README-gate
  blockers remain stop conditions.
- The global skill is not a tracked repository configuration change, so
  `refresh-config` and a root README update are not applicable.

## Checklist

- [x] Capture the initial Git status and identify protected dirty state.
- [x] Inspect companion skills, feedback, and the ExecPlan contract.
- [x] Record the approved design and file-level scope.
- [x] Write a temporary contract test and observe its expected RED failure.
- [x] Create the global `commit-plan-push` skill with precise trigger and
  workflow guidance.
- [x] Run the contract test for GREEN and inspect the rendered skill text.
- [x] Record verification evidence and review notes.

## Risks, edge cases, and rollback

- Risk: agents might bundle unrelated work. Mitigation: require a stop and one
  short clarification when boundaries cannot be inferred safely.
- Risk: agents might push a partial series. Mitigation: state one final push
  after the entire verified sequence unless the user explicitly asks otherwise.
- Risk: the global skill location is outside this repository. Rollback is
  removal of only `/home/example/.agents/skills/commit-plan-push/` if requested.

## Verification

- RED: a temporary contract test checks for the missing skill and exits 1.
- GREEN: the same test validates frontmatter plus required safety, order,
  validation, and reporting language and exits 0.
- Manual: inspect the final file for concise, non-contradictory workflow
  language and compare it to the approved design.

## Progress, evidence, and review notes

- 2026-08-04: Design approved by the user. Existing dirty files are protected
  and excluded.
- 2026-08-04: Inspected the installed global skill at
  `/home/example/.agents/skills/commit-plan-push/SKILL.md`. Its required
  workflow directs agents to execute the inferred safe plan immediately,
  create commits oldest-to-newest, and push once after the verified series.
  It retains stops for ambiguous mixed changes, failed verification, README
  gate blockers, and unclear or rejected upstreams.
- 2026-08-04: The historical temporary RED contract run cannot be replayed
  because the global skill now exists and its temporary test was not retained
  in this repository. Fresh verification for this documentation milestone is
  the README gate, Markdown/diff validation, and direct inspection of the
  installed skill’s trigger, guardrail, and push-cadence language.
- Review: The design now makes the no-second-confirmation behavior explicit;
  it does not authorize bypassing the listed safety stops. Roll back by
  reverting this documentation commit; the external global skill is unchanged.
