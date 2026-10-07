# Metaprompt runner fresh-conversation plan

Update the runner so it saves a complete task prompt and immediately starts a new Codex conversation to execute it. Establish the old behavior, edit only the runner and related documentation, then verify launch, regressions and installed files.

## Purpose and observable outcome

One $metaprompt-run invocation saves and reads back the compiled prompt and starts exactly one new fresh-context task without a go gate. Required missing inputs and actual permissions still apply. Report launch separately from verified completion.

## Context and scope

Loaded canonical rules, .agent/PLANS.md, current runner/metadata, parent/upstream/routed references, relevant feedback and lessons, existing plan and docs. Source of truth is dot_agents/skills/metaprompt-run/, installed through chezmoi into ~/.agents/skills/metaprompt-run/. Scope: runner, picker metadata, root README, skill catalog, metaprompt guide, smoke tests, this plan, saved implementation prompt and required sandbox incident/ledger. Parent/legacy/upstream packages and benchmark data are protected.

## Assumptions and decisions

- User requests a durable skill update; supplied current skill clarifies the requested change.
- Default collaboration mode is fixed by developer instructions; use this ExecPlan without switching modes.
- Native create_thread is available and starts a separate task with inherited cwd/model; prompt limit is 1,000 UTF-8 bytes. Use an absolute-file handoff, no fork or chat history.
- Saved prompt includes all task-local facts/exclusions or accessible exact source references, without optimizer report/eval fixtures.
- Missing inputs stop dependent execution. Missing creation capability or launch error is reported without same-session fallback. Retry only after confirming no duplicate task exists.
- A successful creation is launch evidence, not completion. Execution thread verifies its work; parent may observe via native read/wait tools.
- Initial implementation requested no worktree, commit or push; subsequent $commit-session authorization is recorded below.

## Ordered checklist

- [x] Capture initial git status and read required context.
- [x] Compile, save and read back the implementation prompt.
- [x] Establish old behavior through five read-only application scenarios.
- [x] Update runner workflow and picker metadata; preserve save/missing-input/scope rules.
- [x] Update matching documentation and grouped manual checks.
- [x] Independently evaluate five scenarios and run a harmless native fresh-thread execution.
- [x] Run existing focused regressions and skill validator; inspect diffs.
- [x] Review live snapshot/apply scope; run refresh-config and compare installed bytes.
- [x] Record final evidence and review/handoff.

## Risks, dirty state and rollback

Initial status includes unrelated backup scripts/tests/docs, aliases, phone-SSH docs, feedback, lessons, postmortem-memory ledger/references, benchmark prompts/plans. README and smoke tests are already dirty: change only runner sections. Ledger additions append two reviewed no-new-learning reports and preserve prior entries. Refresh snapshots live Codex/Git configuration and applies all managed targets; inspect ownership first and record incidental snapshots separately. Restore only this task's specific changed hunks to roll back; do not reset whole dirty files. Tool availability may differ in other runtimes: report that limitation without execution-context substitution.

## Verification

RED: agent baseline reads old workflow and identifies current-session execution for supplied-task cases. GREEN: independent read-only application cases cover fresh launch, long prompt, missing inputs, exclusions and unavailable launch tool. Runtime: save harmless prompt under /tmp with supplied facts and >1,000 bytes, start a native task pointing at it, read actual output and task messages. Automated: python3 tests/test_metaprompt_contract.py; python3 tests/test_metaprompt_integration.py; python3 /home/example/.codex/skills/.system/skill-creator/scripts/quick_validate.py dot_agents/skills/metaprompt-run; bash tests/test_claude_skill_links.sh. Deployment: inspect chezmoi status and snapshot dry-run, fish -ic 'refresh-config', compare installed SKILL.md and agents/openai.yaml. Manual checks are in docs/smoke-tests.md.

## Progress and review notes

Initial sandbox reads failed before execution; approved scoped commands work. Living incident docs/postmortem/2026-10-07-metaprompt-run-sandbox-startup.md was registered with explicit no-new-learning decision; targeted ledger check passed with no errors. Underlying sandbox remains unrepaired. Baseline investigation was delegated read-only; parent independently verified the report and inspected resulting runtime artifacts.

RED evidence: independent runner_baseline agent evaluated five hypothetical application cases against the original file. Supplied literal, notes and >1,000-byte prompt all selected current-session execution; missing notes stayed pending. Exact conflicting instruction: workflow step 5 "in the current session". These are read-only interpretations, not executed model/tool runs. At the baseline stage GREEN/runtime checks were pending; their completed evidence appears below.

## Final verification evidence

- Independent forward review interpreted five scenarios: supplied literal/report isolation, supplied notes without inherited history, Unicode long prompt/path, missing inputs/withholding and unavailable/ambiguous creation. Save/collision/scope behavior is preserved. It identified an oversized path-handoff gap; final workflow now shortens optional wording and reports a still-unfittable handoff without executing. These are simulated applications, not executed model trials.
- Runtime fixture /tmp/metaprompt-run-fresh-context-check/prompts/verify-fresh-task.md was saved/read back at 2,789 UTF-8 bytes including Unicode task data. create_thread received an ASCII 299-byte handoff and returned task 01a116f0-0303-7101-8a5e-6ef7fabecdc4. No intervening user turn was needed. Native read_thread subsequently returned idle/completed and the executor’s verified result. Parent read result.txt independently: exact 33 bytes, SHA-256 9e597a3717e7d85c9fb8273c51473b4ea965dcd2328ffc078c97a70b87567113. This tests the saved-file handoff and executor, not the full compiler wrapper end-to-end.
- python3 tests/test_metaprompt_contract.py: 12 tests passed, exit 0. python3 tests/test_metaprompt_integration.py: eight tests ran with four failing legacy digest subcases, exit 1. git show HEAD confirms offending working files exactly equal committed blobs and committed test expects mismatching hashes; unrelated baseline remains unresolved.
- quick_validate.py dot_agents/skills/metaprompt-run: Skill is valid, exit 0. bash tests/test_claude_skill_links.sh: exit 0.
- chezmoi status inspected before refresh; live/source Codex config differed and many installed superpowers targets needed apply. snapshot-codex-config --dry-run passed with no writes. Initial tracked Codex/Git configs were clean; broad refresh is required by repo instructions. fish -ic 'refresh-config' returned REFRESH COMPLETE, exit 0; log /tmp/refresh-config-20261007-111723-2814036.log. Both installed runner files now match source byte-for-byte and Claude link resolves to ~/.agents/skills/metaprompt-run. No new config snapshot diff appeared.
- Unexpected verification failures are in docs/postmortem/2026-10-07-metaprompt-run-verification-baseline.md; tracked ledger review records confirmed baseline and no-new-learning decision. A functions.exec TextEncoder probe failed before task creation; the ASCII handoff length retry succeeded. Sandbox infrastructure workaround remains necessary.

## Review and coding handoff

Scope is the runner contract and matching documentation; parent/legacy/upstream files and test expectations remain untouched. No helper code is needed because the native tool already creates and starts tasks. Rollback is this task’s runner and documentation hunks only; preserve mixed pre-existing README/smoke-test/ledger changes. Implementation finished without committing; the user subsequently authorized $commit-session delivery below.

Paste-ready Cursor prompt:

> Review dot_agents/skills/metaprompt-run/SKILL.md and agents/openai.yaml against plans/update-metaprompt-run-fresh-context.md. Preserve parent compilation, prompt-only save/read-back, task facts/exclusions, collision and missing-input behavior. Verify exactly one immediate native create_thread launch using a <=1,000-byte absolute-file handoff, fresh context and truthful launch/completion reporting. Exercise the grouped runner cases in docs/smoke-tests.md, run the automated commands above, and document pre-existing legacy hash mismatches without weakening tests. If changing tracked configuration, inspect refresh scope, run refresh-config and compare installed bytes. Preserve unrelated dirty work.

Automated checks: the four commands in Verification plus targeted postmortem checks. Manual checks: supplied literal task, long Unicode data, collision, missing notes, withholding, absent native tool and ambiguous launch; inspect returned thread identity and saved data, then verify executor output. No Vercel/build/type checks apply to this Markdown/YAML skill change.

Suggested commit: feat(skills): run metaprompts in fresh conversations. Include this plan, prompt, related docs and incident updates with runner changes; stage only session-attributed hunks after the README gate if a commit is later authorized.

## Authorized session delivery

User invoked $commit-session after implementation closeout, authorizing a focused commit and one upstream push. Branch main tracks origin/main at example-user/ai-cli-dotfiles. Session 01a116ea-64c0-7f01-9f21-4538298828dc: scope helper returned unsafe because successful writes through the tool wrapper were not detected (first_write_at/baseline_at null). Use the actual initial status captured in this conversation and successful Python writes as direct-write evidence. This is the skill’s documented fallback, not ownership inferred from timestamps.

Eligible complete files: runner SKILL.md and agents/openai.yaml, skill catalog, docs/metaprompt-skills.md, this plan, prompts/metaprompt-run-fresh-context.md, and the two October 7 task incidents. Mixed-file scope: only runner block in README.md, runner expectations/long-prompt check in docs/smoke-tests.md, and the two task incident report entries in the postmortem ledger. Leave unrelated baseline work unchanged and unstaged.

Fresh delivery checks: README recruiter gate pass_no_change; legacy contract suite 12/12 passed; runner quick_validate passed; Claude skill-link check exit 0; both targeted postmortem checks returned no errors. Prior native task completed with exact independently verified output. Existing integration byte-pin failures remain documented warnings, not a reason to rewrite legacy files. Commit scope and index must be inspected before committing, and the actual push result is reported at delivery. Suggested subject remains feat(skills): run metaprompts in fresh conversations.
