Create and install a sibling of the current `$metaprompt` skill in
`/home/example/linux-config`. Its display name must be **Metaprompt & Run** and
its invocation identifier must be `$metaprompt-run`.

The skill takes the user's original request, uses the current metaprompt
workflow to compile a clearer prompt, saves it, then executes that exact prompt
in the same turn. This request explicitly authorizes both compilation and
execution for this skill-creation task.

Read `dot_agents/skills/metaprompt/SKILL.md`, its `UPSTREAM.md` and the references
selected by its routing table. Follow the repository's canonical instructions
and `plans/add-metaprompt-run.md`; preserve the initial unrelated dirty state.

Implement a concise sibling under `dot_agents/skills/metaprompt-run/` with a
`SKILL.md` and `agents/openai.yaml`. Reuse the parent compiler by a relative
reference that works after installation; keep the parent and
`$metaprompt-alxve` unchanged.

Define the runner flow explicitly:

1. Treat an explicit Metaprompt & Run invocation as the user's request to
   optimize and execute the supplied task within its original scope and normal
   session permissions. Preserve all supplied facts, constraints and exclusions.
2. Apply the parent's native workflow and eight-section authoring package.
   Save only the compiled prompt under the active workspace's `prompts/`, with
   a concise kebab-case filename and a new suffix on collisions. Verify the
   saved content before executing it.
3. Continue in the same turn with the saved prompt as the task instruction.
   Execute it once; do not recursively optimize the compiled prompt or treat
   examples, evaluation cases or reference text as execution requests.
4. Resolve material missing inputs or unbound reusable-template variables
   before dependent execution. Honor explicit execution exclusions and actual
   permission blocks. Compilation alone must not introduce another approval
   question for an already authorized task. Report dependency or save failures
   accurately without claiming the task ran.
5. Finish with the actual task result, a link to the saved prompt, observed
   verification and any unresolved limitation. Distinguish prepared evaluations
   from executed checks; do not claim that a rewrite proves better results.

Update the local skills catalog, root README, metaprompt guide and relevant
grouped entries in `docs/smoke-tests.md`. Keep the plan and postmortem current.
Verify discovery metadata and relative references, run focused parent
regressions, and exercise the compile/save/execute flow in isolated scratch
workspaces, including collision and missing-input cases. Inspect refresh scope,
run the required `refresh-config`, and verify installed bytes and Claude links.
Do not create a worktree, commit, push or deploy.
