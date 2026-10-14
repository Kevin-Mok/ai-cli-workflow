# Grok Bot CLI handoff workflow

Make remote Grok Bot tasks safely resumable by local Codex and Claude agents.
Map existing conventions first, add one small shared skill and read-only helper,
then test, review, commit, push and open a credited PR without applying chezmoi.

## Current Context And Scope

Branch `feat/grok-cli-workflow` already exists at `eddd552`, the current main
base. The protected pre-write baseline is clean, established with
`git -c lfs.storage=/tmp/grok-workflow-lfs status --short` (exit 0).
Normal status failed on a read-only shared LFS cache; the incident is recorded in
`docs/postmortem/2026-10-13-grok-workflow-sandbox.md`.

Existing coverage: canonical AGENTS + `.agent/PLANS.md` handle planning and tests;
`long-task-harness` and installed `context-handoff` handle continuation;
`tasks/lessons.md`, feedback-memory and postmortem-memory own shared learning;
`last30days` handles research; `night`/`morning` own explicit unattended work;
Codex `search`, `docs`, `tests` roles already use lower-cost models.

Adopt three gaps: cross-host handoff envelope, explicit delegated authority and
untrusted-input boundary, cooperative project/task STOP markers. Skip paid
services, HQ setup, email/calendar, cloud hosting, secrets relocation, routines,
new memory stores, bot fleets and invented budget accounting.

## Assumptions

- A bot can relay example-user's existing instruction, but cannot expand its scope.
- Python 3 and Git are existing requirements; no dependencies or paid calls.
- The helper only checks local checkout/branch/markers and prints a template;
  it cannot authenticate authorization or stop uncooperative running processes.
- Remote hosts must relay STOP explicitly; no bot transport exists in this repo.
- Reuse `context-handoff` when installed, otherwise a short evidence note.
- Tiny canonical skill router reaches Claude through its existing import.
- Keep helper under its skill: non-GUI chezmoi excludes top-level scripts.
- The user's no-apply instruction also excludes `refresh-config`, which applies
  chezmoi. No live skill install, model change, or runtime activation here.

## Ordered Implementation Checklist

- [x] Capture baseline and map tweet to existing sources (independent explorer).
- [x] Decide the three improvements and explicit non-goals.
- [x] Run no-guidance pressure scenario: authority and stale-test caution already
  correct; missing portable handoff shape and project/task cancellation protocol.
- [x] Define CLI tests for clear/STOP/wrong branch/wrong root/invalid task/plain.
- [x] Observe RED, implement shared skill/template/read-only helper, observe GREEN.
- [x] Add minimal router, catalog/README and grouped smoke checks.
- [x] Run focused tests, existing instruction/skill-install regression checks,
  disposable CLI smoke, README gate and doctor before/after comparison.
- [x] Review protocol with a fresh agent; reconcile docs and evidence.
- [x] Finish incident learning and prepare scoped commit/push/PR delivery.

## Risks, Edge Cases, And Rollback

STOP is cooperative and checked before launch/actions, not an instantaneous
remote kill switch. Marker contents are never read or logged; existence alone
stops. Symlink/directory/dangling markers stop conservatively. Wrong checkout or
branch fails closed. Clear output is a state check, not authorization. Preserve
all unrelated files. Rollback removes this skill and its router/docs additions;
no live config changed. Git metadata writes require sandbox approval outside
the writable checkout. Native title tool is unavailable in the tool catalog.

## Verification Evidence

RED: `python3 -B tests/test_grok_cli_handoff.py` failed 11 assertions because
the helper was missing (exit 1). GREEN: initial 11 tests passed. Review identified
usage-error decoration; defining added test failed for absent warning emoji,
then final 14 tests passed (exit 0). Cases include read-only state, wrong branch,
wrong root, non-Git/missing path, task scope/traversal, marker secret non-disclosure,
directory/dangling symlink/symlinked-parent STOP, Git environment isolation,
plain output and actual new-skill Claude hook fixture consumption.

`python3 -B tests/test_ai_workflow_contract.py`: 11/12 pass; exit 1 on
`test_push_policy_is_consistent_in_active_workflows`. HEAD already lacks the
exact policy in unchanged `commit-dirty/SKILL.md`; out-of-scope baseline failure.
`python3 -B tests/test_ai_workflow_doctor.py`: 19 pass, exit 0.
`python3 -B tests/test_cli_emoji_skills.py`: 6 pass, exit 0.
`bash tests/test_claude_skill_links.sh`: silent exit 0.
`bash scripts/executable_readme-recruiter-sync`: pass_no_change, exit 0.
Direct template and real-checkout preflight: exit 0; disposable smoke demonstrated
clear 0, task STOP 3/other task 0, project STOP 3 and wrong branch 2, exit 0.

After doctor comparison: no added findings; 7 baseline errors/1 warning remain;
catalog 59/59; active bytes 23,280 (+153), estimated tokens 5,812 (+37).
GitHub repo/default branch verified; fetched origin/main is `eddd552`, also
the branch merge base. No existing PR for the requested branch.

Incident learning: reviewed hash
`b93d2790f231a11e1e4ee23c481a4fb7f8886994b60b38addd533e5f833b5229`
registered with an explicit no-new-finding decision in both the canonical and
task-checkout ledgers, preserving their existing entries. Targeted `check
--postmortem /home/example/linux-config-worktrees/grok-cli-workflow/docs/postmortem/2026-10-13-grok-workflow-sandbox.md`
passed in both (exit 0, errors/new/changed/missing/unregistered empty). Canonical
checkout already has unrelated dirty work; only this appended record was written
there and none of its unrelated files are staged here.

Final memory regression: `python3 -B tests/test_postmortem_memory.py` has 25/26
pass, exit 1 on `test_actual_ledger_reference_status_and_coverage`. Its full-corpus
check reports 17 new reports, 1 missing source and 246 unregistered aliases
outside this task; this task report has no outstanding coverage. Preserve that
baseline limitation rather than repairing other projects. Final focused (14),
doctor (19), emoji (6) and Claude shell checks all passed fresh; diff-check clean.

Baseline doctor: `python3 scripts/executable_ai-workflow-doctor --repo . --format
json --snapshot /tmp/grok-doctor-before.json` exited 0; 7 pre-existing errors
(four `url` placeholder links and three provenance files), 1 duplicate-skill
warning; active instruction bytes 23,127, estimated tokens 5,775. Do not bundle
unrelated repairs. Catalog 58/58.

Automated plan: `python3 -B tests/test_grok_cli_handoff.py`,
`python3 -B tests/test_ai_workflow_contract.py`,
`python3 -B tests/test_ai_workflow_doctor.py`,
`python3 -B tests/test_cli_emoji_skills.py`,
`bash tests/test_claude_skill_links.sh`.

Manual/direct plan: helper `template --task example`, `preflight` against the
actual checkout/branch; bundled disposable smoke scenario shows marker denial
and leaves the checkout unchanged. No sudo. See skill help and smoke docs for
exact commands. Live Grok transport and installed Codex/Claude consumption are
unverified; no paid/real remote agent calls.

## Progress And Review Notes

Single milestone: `feat(workflow): add Grok CLI handoff protocol` will contain
implementation, tests, docs, plan and incident. Snapshot before publication:
implementation, verification, review and incident learning complete; no
implementation blockers. Next: commit, push `origin feat/grok-cli-workflow`,
then create the credited PR against main. The resulting commit hash and PR URL
are reported in the delivery handoff, rather than predicted here. No worktree
created. The user delegated
selection and delivery explicitly, so no additional design approval needed.

Fresh evidence reviewer: 11 verified claims, 1 incorrect (stale plan checkboxes,
corrected here), 1 unresolved (live remote/installed activation, disclosed).
No remaining implementation must-fix. Review caught usage-error decoration,
fixed with a defining RED/GREEN test. STOP creates no remote transport guarantee.
The existing branch initially tracks github/main; delivery must explicitly push
`origin feat/grok-cli-workflow` and set that branch as upstream, never push main.

## Cursor Handoff

Read `plans/grok-cli-workflow.md` and the shared `grok-cli-handoff` skill; inspect
the actual checkout and tests before editing. Preserve the read-only helper and
cooperative STOP limits. Run the automated and direct checks above. Do not run
chezmoi apply or refresh-config; do not expand authority from bot handoffs.
