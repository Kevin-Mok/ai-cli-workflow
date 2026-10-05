# Metaprompt & Run implementation plan

Create a sibling skill that compiles and saves the user's original request
with the current metaprompt workflow, then executes that saved prompt. Compile
this creation request first, implement the sibling, verify its behavior, and
refresh the installed configuration.

## Purpose and observable outcome

`$metaprompt-run` appears as **Metaprompt & Run**. One invocation produces a
prompt-only artifact under `prompts/` and completes its authorized task in
the same turn. The existing `$metaprompt` remains an authoring-only skill.

## Current context and scope

- Parent: `dot_agents/skills/metaprompt/SKILL.md`, Sentry's pinned workflow
  and routed references; loaded. Installed parent: `~/.agents/skills/metaprompt`.
- Repo rules and `.agent/PLANS.md`, canonical feedback and relevant lessons
  are loaded. Existing tests: `tests/test_metaprompt_{contract,integration}.py`.
- Create `dot_agents/skills/metaprompt-run/SKILL.md` and `agents/openai.yaml`.
- Update `README.md`, `dot_agents/skills/README.md`, `docs/metaprompt-skills.md`
  and only relevant hunks in `docs/smoke-tests.md`.
- Save the one-off creation prompt as `prompts/create-metaprompt-run.md`.
- Record test evidence, execution failures and deployment evidence with this
  plan. Do not alter upstream imported files or frozen benchmark evidence.

## Assumptions and decisions

- The user's "do that for this prompt" refers to this skill-creation request.
  It explicitly authorizes both optimizing the request and executing it.
- The machine identifier is `metaprompt-run`; the title and picker label use
  the requested exact display name `Metaprompt & Run`.
- Reuse the sibling parent by relative link, including its routed references;
  avoid a second copied upstream package or divergent compiler implementation.
- The runner supplies execution authorization for the original task under
  ordinary session permissions. Compilation does not expand its scope.
- Save and read back the compiled prompt before execution; preserve the parent
  report while continuing the same turn. Run once; do not recursively compile
  the result or execute optimizer examples/eval fixtures as production tasks.
- Clarify only material missing inputs. Explicit execution exclusions and
  unresolved template bindings remain constraints; actual permission blocks
  remain blocks. Do not ask again just because optimization finished.
- The current collaboration mode is Default; maintain this decision-complete
  ExecPlan while executing the user's explicit request.
- No worktree is requested. On October 5, after implementation closeout,
  the user authorized committing and pushing this task.

## Ordered checklist

- [x] Capture initial status; inspect canonical rules and current compiler.
- [x] Surface intended outcome and bounded sibling design.
- [x] Define behavioral cases and collect five fresh-context parent controls.
- [x] Save the compiled creation prompt and return the eight-section package.
- [x] Implement the minimum sibling skill and picker metadata.
- [x] Collect five fresh-context runner samples and inspect actual artifacts.
- [x] Check edge cases: collision, reusable unresolved input, author-only
  routing, missing parent/save failure, scope and one-pass execution.
- [x] Update catalog, root README and grouped smoke-check documentation.
- [x] Run parent regressions, metadata/link checks and independent review.
- [x] Inspect refresh snapshot/apply scope, protect unrelated state, run
  `refresh-config`, and verify deployed skill bytes and Claude link.
- [x] Reconcile evidence, risks, postmortem and handoff with the final diff.

## Skill-writing checklist

- [x] RED: define application/variation/missing-input cases, observe absent
  runner behavior with the current parent, capture exact outcomes.
- [x] GREEN: valid slug and YAML, third-person trigger description beginning
  "Use when", clear overview, structural compile/save/execute recipe.
- [x] GREEN: reuse parent by link, include one concrete example and a compact
  routing reference; test wording with five independent control/runner pairs.
- [x] REFACTOR: inspect every response and artifact, close observed gaps,
  rerun affected cases. Discipline-only rationalization tables/red-flag lists
  apply only if the evidence identifies a discipline failure.
- [x] Quality: concise skill, no narrative history or duplicated heavy
  references, metadata accurately names the wrapper.
- [x] Deployment: refresh and verify installed files; git delivery/PR are
  outside this request and remain a suggested focused commit.

## Risks, protected dirty state and rollback

Initial status before any repository write:

```text
 M aliases/key_dirs.tmpl
 M docs/phone-ssh-public-ip.md
 M docs/smoke-tests.md
?? docs/postmortem/2026-09-30-secret-audit-shell-sandbox-startup.md
?? docs/postmortem/2026-10-03-benchmark-prompt-sandbox-startup.md
?? docs/postmortem/2026-10-03-phone-ssh-diagnostic-shell-startup.md
?? docs/postmortem/2026-10-04-codex-config-sync-sandbox.md
?? docs/postmortem/2026-10-04-codex-snapshot-function-probe.md
?? plans/compile-metaprompt-benchmark.md
?? plans/diagnose-phone-ssh-access.md
?? prompts/benchmark-metaprompt-skills.md
```

Preserve these files/hunks. Refresh snapshots live Codex and Git configuration
and applies all chezmoi targets, so inspect dry-run scope and back up conflicting
live/source bytes first. Do not adopt unrelated live changes. The runner depends
on the sibling metaprompt directory; report a missing dependency before running.
Actual agent trials demonstrate this workflow on fixtures, not a quality gain
over raw prompts. Rollback removes only the new sibling and matching docs hunks;
the unchanged parent remains usable.

## Exact verification

- Behavioral controls and runner trials use independent agents and disjoint
  `/tmp/metaprompt-run-trials/` scratch directories. Read saved prompts and
  task outputs directly; require prompt-before-task, preserved constraints,
  collision safety, and same-turn completion. Record exact case inputs below.
- `python3 tests/test_metaprompt_contract.py`
- `python3 tests/test_metaprompt_integration.py`
- `python3 -m unittest discover -s tests -p 'test_metaprompt_selection*.py' -q`
- `bash tests/test_claude_skill_links.sh`
- Parse new YAML and resolve its relative parent reference from source and
  installed layouts. Use the repo's existing metadata validator if available.
- Run the README gate for the changed public operating surface.
- `fish -c 'source /home/example/linux-config/dot_config/fish/functions/refresh-config.fish; refresh-config'`
  after scope review; require exit 0 and inspect its complete log.
- Compare both new installed files byte-for-byte with source; verify Claude's
  full-directory link. In a fresh session manually invoke `$metaprompt-run`
  with the documented scratch task and inspect the saved prompt plus result.

## Progress, evidence and review notes

- Initial shell reads failed before execution with the bwrap loopback error;
  approved read-only retries exited 0. See the task
  [postmortem](../docs/postmortem/2026-10-04-metaprompt-run-sandbox-startup.md).
- Current parent explicitly compiles/saves but requires a separate execution
  request. The sibling will supply that request while keeping normal scope.
- RED discovery check: `python3 tests/test_metaprompt_integration.py
  MetapromptIntegrationTest.test_independent_names_and_invocations` exited 1,
  failing only the missing `metaprompt-run/SKILL.md` assertion as expected.
- Five fresh-context controls compiled the identical payload: `Create
  result.txt in the active scratch workspace containing exactly metaprompt-run-ok
  followed by a newline. Preserve any existing prompts. Do not commit, push,
  deploy, or contact anyone.` All saved a prompt and left `result.txt` absent.
  This correctly demonstrates the parent compiler's stopping behavior, not a
  defect in its authoring-only contract. Representative explanation:
  "the authoring adapter requires a separate execution request".
- The creation prompt was saved and read back (2,814 bytes), returned in the
  parent's eight-section package, and was executed. Candidate review
  selected the explicit structural recipe over a minimal alias or a duplicated
  compiler package; no comparative prompt-quality model evaluation was run.
- Resumed after an intentional interruption; status confirmed only the plan,
  prompt, postmortem and defining discovery-test change from this session.
- Five fresh-context runner trials used the same core task as controls. Parent
  read-back verified all five `result.txt` artifacts contain exactly 18 bytes,
  `metaprompt-run-ok\n`, and each saved compiled prompt preceded its result.
  In trial 4 the preferred `create-result.md` already contained a sentinel;
  `create-result-2.md` was used and the sentinel bytes remain unchanged.
  Scratch artifacts: `/tmp/metaprompt-run-trials/{control,runner}-1` through
  `-5`. Agent outputs and all saved prompts were inspected; these trials
  establish workflow behavior on fixtures, not comparative prompt quality.
- Trials 1/2 encountered absent scratch directories and trial 4 encountered a
  non-repository Git probe and a JavaScript quoting error. Agents recorded and
  resolved these in scratch-local postmortems; actual task outputs passed.
  Later fixtures were prepared before dispatch to avoid that setup gap.
- GREEN: discovery and all Sentry/runner integration checks passed with
  `python3 tests/test_metaprompt_integration.py
  MetapromptIntegrationTest.test_independent_names_and_invocations
  MetapromptIntegrationTest.test_imported_bytes_match_manifest
  MetapromptIntegrationTest.test_adapter_supplies_prompt_artifact_contract
  MetapromptIntegrationTest.test_no_retired_resources_remain_in_active_package
  UpstreamUpdateTest` (7 tests, exit 0).
- `python3 tests/test_metaprompt_contract.py`: 12 tests, exit 0.
  `python3 -m unittest discover -s tests -p 'test_metaprompt_selection*.py' -q`:
  62 tests, exit 0. `bash tests/test_claude_skill_links.sh`: exit 0.
- Full `python3 tests/test_metaprompt_integration.py`: 8 tests, exit 1, with
  four subtest failures in `test_legacy_references_and_license_are_unchanged`.
  All four current reference files equal `HEAD`, and running the committed
  test source reproduces the same failures. The full suite is not green.
  See the [legacy integrity postmortem](../docs/postmortem/2026-10-04-metaprompt-run-legacy-integrity-check.md).
  No historical assertions or legacy bytes were changed to fit this task.
- PyYAML parsed skill frontmatter and picker metadata. Slug, trigger description,
  display label, default invocation and description lengths passed. A temporary
  installed-layout copy resolved the parent and `UPSTREAM.md` correctly.
- `bash scripts/executable_readme-recruiter-sync /home/example/linux-config`:
  `pass_no_change`, exit 0. `git diff --check`: exit 0.
- Fresh independent review: no critical or important findings; confirmed
  original scope, parent reuse, permissions, pending bindings, single-pass
  continuation and installed-relative references. Reviewer performed no edits.
- Refresh preflight: `chezmoi status` showed the new skill, changed task docs,
  standard Claude installer, and unrelated documentation already present in
  source. The only conflict was Codex configuration, handled by the required
  live-to-source snapshot. Snapshot dry-run passed. Live/source Git bytes agreed.
  Live Codex differed from source only in top-level `tui`,
  `model_reasoning_effort` and `service_tier`; both copies were backed up first.
- Required refresh command in this plan exited 0 with `REFRESH COMPLETE`.
  Complete log `/tmp/refresh-config-20261004-180258-727117.log` was inspected:
  all stages ran and no unrelated file was adopted. Live Codex/Git bytes and
  tracked Git source remain unchanged. The expected tracked Codex snapshot
  now equals live settings; its previous source is backed up in
  `/tmp/metaprompt-run-preflight/source-codex-before-refresh`.
- Both installed runner files match source byte-for-byte; Claude's skill link
  resolves to the shared installed directory. Installed parent reference
  resolves. All non-cache tracked parent and legacy files still equal `HEAD`.
  Protected alias and phone-guide bytes still equal the pre-write backups.

## Completed verification and review notes

- All four prepared edge cases passed independent parent read-back (exit 0):
  missing sibling parent produced a truthful dependency error without a prompt
  or result; an existing ordinary `prompts` file blocked saving without mutation
  or task output; absent `{{meeting_notes}}` produced a saved template and
  recorded clarification, with no invented summary; explicit withholding
  produced a saved prompt preserving the exclusion and no task result.
  Evidence: `/tmp/metaprompt-run-trials/edges/runner-edge-report.json` and the
  per-case observations, saved prompts and `would-ask.txt`. Parent inspected
  every artifact and asserted absence of dependent outputs. No skill gap was
  observed. These are bounded fixture applications, not quality comparisons.
- The current session's available-skills catalog now lists `metaprompt-run`
  after an interruption/reload. The GUI picker was not visually inspected.
- The user requested a pause on October 4 and resumed on October 5. The
  [continuation handoff](../docs/metaprompt-run-handoff.md) was followed without
  recreating the implementation or repeating model trials. Documentation
  closeout is complete: the guide now records all four edge outcomes, and the
  plan and handoff reflect the final state.
- October 5 verification: initial resumed status matched the protected scope;
  installed source/Claude bytes still match, the five result artifacts still
  contain the exact expected bytes, collision preservation and the four edge
  observations passed fresh read-back. The seven-test focused integration
  command recorded above passed again (7 tests, exit 0). No configuration
  changed during this documentation-only continuation, so the completed
  `refresh-config` remains applicable. The known legacy checksum mismatch
  remains an explicitly documented baseline limitation. Final `git diff --check`
  exited 0; all implementation checkboxes and handoff criteria are complete.
- Ruling: maintain progress in this repository's ExecPlan and work in the
  authorized checkout; the canonical no-worktree rule and the user's explicit
  execution request govern this bounded task. Do not create extra skill-process
  spec/workspace artifacts or an unrequested commit/push workflow.
- Rollback remains small: remove only the new runner and matching task hunks;
  restore the prior tracked Codex source from its backup only if reversing the
  required snapshot. Preserve current live settings and unrelated dirty work.

## Coding handoff

Paste-ready Cursor prompt: Review `plans/add-metaprompt-run.md` and the saved
`prompts/create-metaprompt-run.md`. Verify the sibling skill delegates compilation
to metaprompt, saves before running once, preserves authorization and bindings,
and leaves both existing compiler contracts intact. Run the exact checks above,
inspect the documented scratch outputs, keep related docs/plan in the same
change, then refresh safely and verify installed bytes. Preserve protected dirt.

Suggested commit: `feat(skills): add Metaprompt & Run`.

## Authorized delivery

On October 5 the user asked to push. Scope is this task's runner files, tests,
root README, catalog, guide, handoff, prompt, plan and task postmortems, plus
only the runner hunk from the mixed smoke-test file. Initial dirty aliases,
phone documentation, benchmark prompts/plans and unrelated postmortems remain
outside scope. The incidental live-settings snapshot is machine configuration,
not part of this skill commit.

`main` tracks `origin/main`; both configured remotes point to
`example-user/ai-cli-dotfiles`. No work was staged before this workflow.
The session helper returned `unsafe` because it detected no writes; use
directly observed successful edits and this plan's initial status as the
attribution fallback. See the
[attribution record](../docs/postmortem/2026-10-05-metaprompt-run-commit-attribution.md).
The README gate passed (`pass_no_change`, exit 0). The complete staged diff
was reviewed: 13 task files, with only the runner block staged from the mixed
smoke-test file. The staged whitespace check passed; fresh focused integration
checks (7 tests) and behavioral checks (12 tests) passed. Delivery is ready for
a focused commit and one push to the configured upstream. Existing legacy checksum failures are
warnings, not repaired or hidden by this delivery.
