# Compile a metaprompt benchmark request

## Purpose and observable outcome

Save and present a paste-ready prompt that requests an executed, reproducible
comparison of the installed metaprompt skill and the documented alternatives.
This turn authors the prompt; it does not execute its embedded benchmark.

## Context and scope

Read `docs/metaprompt-skills.md`, `plans/upgrade-metaprompt-skill.md`, the
installed metaprompt adapter and upstream evaluation references, canonical
instructions, feedback, and relevant lessons. The guide records a small compiler
trial, not downstream task success. Scope is a new prompt, this plan, and the
required sandbox-startup postmortem. Preserve all pre-existing dirty work.

## Assumptions and decisions

- The explicit `$metaprompt` invocation requests prompt compilation under its
  supplied contract; execution needs a separate request.
- Compare the deployed Majkey adapter, alxve, three documented alternatives,
  and raw/minimal baselines. Separate compatibility from task performance.
- Determine the execution model and budget during the future benchmark;
  neither is supplied in this request. No model superiority claim is made.
- Default mode is active. Maintain this small document-authoring plan without
  changing runtime mode or creating a Git worktree.

## Ordered checklist

- [x] Capture initial status and inspect the source and applicable guidance.
- [x] Record the unexpected sandbox startup failure and successful read retry.
- [x] Compile the comparison prompt with measurable success and fair controls.
- [x] Verify the saved prompt, review heuristic findings, and inspect scope.
- [x] Prepare the final response with the exact prompt and its saved path.

## Risks and rollback

Avoid claiming that prepared evaluations or shorter wording establish quality.
Separate unknown capabilities, unsupported use cases, and measured failures.
Protect the existing README, guide, skill trees, tests, smoke tests, lessons,
and SSH/VPS changes recorded by the initial `git status --short`.
Rollback removes only this session's three new documents. No configuration,
installation, README behavior, or reusable manual procedure changes here;
`refresh-config` and smoke-test changes are therefore outside this turn's scope.

## Verification

- Read back `prompts/benchmark-metaprompt-skills.md` and confirm the compiled
  prompt is the complete file, with no surrounding response metadata.
- Run `python3 dot_agents/skills/metaprompt/scripts/prompt_lint.py
  prompts/benchmark-metaprompt-skills.md --mode general --context verified
  --fail-on never`; review findings as heuristics, not benchmark results.
- Run `git diff --check` on the three session documents and check their status.
- Manually check candidate coverage, downstream execution, holdout isolation,
  repeated trials, cost controls, uncertainty, and conditional recommendations.

## Progress, evidence, and review notes

- 2026-10-03: Initial read calls exited 1 during sandbox startup. Elevated
  reads exited 0 and captured status before any write. See the new
  `docs/postmortem/2026-10-03-benchmark-prompt-sandbox-startup.md`.
- No benchmark, installation, commit, or push was executed. Keep these plan
  updates with the prompt and incident note in any future related commit.
- The exact-file linter command above exited 0 with no heuristic findings.
  Saved-file readback confirmed the complete compiled prompt without fences
  or response metadata. Explicit Python checks for all three new files found
  terminal newlines and no trailing whitespace (exit 0); these cover untracked
  files, which `git diff --check` alone does not inspect.
- Scoped `git diff --check` exited 0; scoped status showed exactly the three
  new untracked documents. Manual review confirmed all seven main variants,
  capability coverage, fresh downstream sessions, holdout separation, budget
  controls, paired uncertainty, and a conditional recommendation. The benchmark
  remains unexecuted; no best-skill claim is made by this authoring task.
