# Metaprompt skills

The installed `$metaprompt` now uses the pinned **Sentry `prompt-optimizer`**
workflow, replacing the Majkey adaptation at the user's request on October 4,
2026. The completed [native skill selection](metaprompt-selection.md) chose it
among the popular, maintained native finalists:
14/16 successes versus Wshobson's 13/16 and Senior's 11/16. Raw and minimal
instructions both reached 15/16 at lower cost, so direct instructions remain
the practical choice for already explicit tasks. The report links pinned source
and maintenance receipts, adapter limitations, costs, and optional installation
and rollback. The eight native files are preserved behind the existing
`metaprompt` name; the local adapter adds prompt saving and ordinary execution
boundaries. Use
`$metaprompt-alxve` for the original compiler, including its strict standalone
`go` boundary. Both save compiled prompts under the active repo's `prompts/`
directory with non-destructive collision suffixes.

| Invocation | Behavior |
| --- | --- |
| `$metaprompt Make me a prompt to summarize meeting notes.` | Returns Sentry's eight-section package, saves only the Optimized Prompt, and reports its path. Labels prepared versus executed evals. Does not execute the embedded production task. |
| `$metaprompt-alxve Make me a prompt to summarize meeting notes.` | Preserves original weight selection, prompt/Saved/Run/Weight metadata, and fresh standalone `go` gate for every pass. |

Tracked sources install through chezmoi to `~/.agents/skills/<name>`.
The existing Claude installer links complete directories under
`~/.claude/skills/`. Start a fresh agent session to reload the skill catalog;
file verification alone does not prove a running session refreshed its picker.

## Selection evidence

This section records the earlier **Majkey maintenance-based choice**, superseded
by the Sentry replacement. Its source history and observations are retained as
historical evidence and are not attributed to the new skill. The earlier
[downstream benchmark](metaprompt-benchmark.md) uses pinned sources, executable
fixtures and a 50-request pilot on gpt-6.1-sol at medium reasoning. Raw, minimal,
Talki and GitHub tied on the tested summary case; tight episode limits prevented
a useful coding-quality ranking. No optimizer demonstrated a gain over the
baselines, and creation/template workflows remain untested. Neither this
maintenance table nor the four compiler examples below establishes downstream
superiority. The subsequent complete [selection report](metaprompt-selection.md)
is the basis for the current Sentry choice.

Researched on **2026-10-03** using actual skill files, licenses, GitHub path
histories, and substantive commit diffs. The 90-day window starts July 5; the
180-day window starts April 6. Counts exclude initial additions, directory
moves, unrelated repository changes, and packaging-only updates.

| Candidate | Latest substantive skill change | Updates: 90 / 180 days | License | Decision |
| --- | --- | --- | --- | --- |
| [Majkey25 prompt-engineering](https://github.com/Majkey25/prompt-engineering-skill/tree/5c00259223196bd779c97d3234ef34a9a7119634/prompt-engineering) | 2026-10-03 | 5 / 6 | MIT | Earlier choice, replaced by Sentry after the complete selection benchmark. |
| [talki-io prompt-optimizer](https://github.com/talki-io/prompt-optimizer/blob/e5f5efe5925ce47073f143001d0a8e9de23b392a/SKILL.md) | 2026-09-29 | 4 / 4 | MIT | Maintained, but excludes creation from scratch; direct invocation also applies the optimized prompt. |
| [getsentry prompt-optimizer](https://github.com/getsentry/skills/tree/c190d369bcbaa6cfdd95e9edfdba040506b4db76/skills/prompt-optimizer) | 2026-05-04 | 0 / 2 | Apache-2.0 | Useful contract/holdout evaluation workflow; no substantive update in the recent window. |
| [GitHub prompt-optimizer](https://github.com/github/awesome-copilot/blob/b010c5ebfacdd78a45702481b77ec55ba033e373/skills/prompt-optimizer/SKILL.md) | Initial addition: 2026-05-14 | 0 / 0 | MIT | Chat-only and prohibits template placeholders; active repository does not establish active skill maintenance. |

Majkey's counted updates are [July 6](https://github.com/Majkey25/prompt-engineering-skill/commit/4f63ef5435639d609bc8d765c441514ebfca68df),
[August 7](https://github.com/Majkey25/prompt-engineering-skill/commit/782f41bbbe63774b011f85033ad76a92a0f13e66),
[September 25](https://github.com/Majkey25/prompt-engineering-skill/commit/16311aee15b0549683f39d54dfa6ca2132f76e9f),
[September 26](https://github.com/Majkey25/prompt-engineering-skill/commit/63d5a8288e9cb342f130f2848d53bf3e73157181),
and [October 3](https://github.com/Majkey25/prompt-engineering-skill/commit/5c00259223196bd779c97d3234ef34a9a7119634),
plus [June 3](https://github.com/Majkey25/prompt-engineering-skill/commit/8f932e589bf6ace5ed285a3e16ebcb77ca28b3a6)
in the longer window. May's import/packaging change is excluded.

Selection favors relevant maintenance and observable evaluation, not stars or
claims of guaranteed frontier performance. No published comparative benchmark
was found that proves this skill universally outperforms the alternatives.
Maintenance is concentrated in a small upstream project. The local adapter
keeps the familiar prompt-authoring use case; upstream silent autoprompt
execution is disabled, and references load only when relevant.

The provider-specific approach agrees with current primary guidance:
[OpenAI](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
prefers simple direct reasoning prompts and trying zero-shot first;
[Gemini](https://ai.google.dev/gemini-api/docs/prompting-strategies) recommends
examples while warning about overfitting; [Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
starts from success criteria and empirical tests. These differences support
testing techniques on the actual target rather than making one universal rule.

## Updating and rollback

The [source record](../dot_agents/skills/metaprompt/SOURCE.md) documents the
exact pin, hashes, license, and the reusable `update_upstream.py` helper.
Use `--check` to discover a newer skill commit, or `--stage NEW_DIRECTORY`
with optional `--revision FULL_SHA` to prepare a candidate for review. Updates
are intentionally reviewed; checking does not silently replace the skill.

Keep local `SKILL.md`, `agents/openai.yaml`, `SOURCE.md`, and the update helper
separate from the immutable imported inventory. Review candidate changes,
update the pin and matching checks together, and run the regression commands
below before deployment. Review both source content and model behavior;
passing text checks is not evidence of better prompt results.

For the original compiler, invoke `$metaprompt-alxve`; its four
references and license are byte-identical to the pre-migration package.
To roll back a later upstream import, stage the prior full SHA through the
same helper and restore only its reviewed imported inventory and pin. Leave
the legacy skill and unrelated working-tree files intact. The Sentry updater
cannot fetch old Majkey revisions: restore the complete outgoing package from
the backup recorded in [the replacement plan](../plans/replace-metaprompt-with-sentry.md)
if reversing this replacement. The backup is machine-local and temporary.

Before deployment inspect `chezmoi status` and the live Codex snapshot dry-run.
The required `refresh-config` snapshots live Codex and Git configs, applies
chezmoi, regenerates shortcuts, and reloads fish abbreviations. It has no
target flag and can adopt conflicting live files; preserve unrelated edits.
Deployment evidence and any scope restrictions belong in the active plan.

## Automated and manual verification

From the repository root:

```bash
python3 tests/test_metaprompt_contract.py
python3 tests/test_metaprompt_integration.py
python3 -m unittest discover -s tests -p 'test_metaprompt_selection*.py' -q
bash tests/test_claude_skill_links.sh
```

The legacy suite covers its saved-prompt and standalone-go contract; the new
suite covers independent identities, preserved legacy bytes, exact Sentry
content against the frozen candidate, retired-resource removal, and safe
update staging. The selection tests are offline and do not rerun models.
The retired Majkey linter, eval-manifest generator and helper test suite are
no longer part of the active package.

Replay these four independent requests against each skill in a fresh scratch
workspace. Verify actual saved files, no task execution, and preserved intent:

1. Make me a prompt that asks an AI for the capital of France.
2. Sharpen this: Summarize the supplied meeting notes into decisions, owners,
   and deadlines. Do not invent missing owners or dates.
3. Create a reusable template for summarizing `{{meeting_notes}}` into
   decisions, owners, and deadlines; mark missing values unknown.
4. Write a coding-agent prompt to fix flaky checkout tests in the repository
   it can inspect. Preserve payment behavior, do not deploy, and stop after
   the focused regression checks pass. We suspect timing but have no logs.

Check Sentry's eight named sections and prompt-only saved file, preserved
missing-data rules, template variables,
no invented stack/files/root cause, payment preservation, no deployment,
and the supplied stopping condition. For legacy, additionally verify the
gate and that embedded `run` text does not authorize execution. Stable manual
checks also live in [smoke tests](smoke-tests.md#skills-and-docs).

### Sentry replacement verification

On October 4, 2026, all 129 metaprompt-focused tests passed, including the
eight-test Sentry packaging/updater suite and the preserved alxve contracts.
The broader suite passed 549/551 with the same two unrelated commit-policy and
vault-inventory failures. Metadata and Claude-link checks passed.

One independent gpt-6.1-sol/medium agent used the updated adapter to create a
checkout investigation template in a temporary workspace. Parent read-back
confirmed canonical `{{test_output}}`/`{{repo_context}}` variables, missing
evidence marked unknown, payment preservation, no deployment and the focused
stop condition. The existing filename stayed unchanged; the new prompt used
`checkout-flake-template-2.md`. Its response retained all eight native sections
and labeled five prepared eval cases as unexecuted. This single check establishes
observed adapter behavior, not downstream efficacy or a new benchmark score.

The required `refresh-config` completed. All 13 installed non-cache files match
source; 43 obsolete backed-up files were removed after byte comparisons.
Claude's metaprompt symlink resolves to the updated shared directory. Start a
fresh Codex/Claude session to reload the skill catalog. Full evidence and
rollback location are in the [replacement plan](../plans/replace-metaprompt-with-sentry.md).

### Historical Majkey adapter trials

On 2026-10-03, separate evaluator agents applied alxve and the former Majkey
adapter to these same
requests in scratch workspaces. The parent read back all eight saved prompts.
Both preserved the supplied constraints and returned prompts without executing
their tasks. Prompt-word counts (excluding surrounding metadata):

| Case | Original alxve | Former Majkey metaprompt |
| --- | ---: | ---: |
| Trivial fact prompt | 11 | 6 |
| Sharpen meeting summary | 173 | 46 |
| Reusable template | 182 | 51 |
| Checkout coding agent | 480 | 145 |

The new sharpening result was directly usable; the legacy result asked a
second model to perform another rewrite. The new complex prompt retained the
stop condition without the legacy fixed quality block. This is a small
observed compiler trial, not a downstream task benchmark or proof that shorter
prompts always perform better. Each evaluator handled four cases within one
session, so the cases are not statistically independent. Initial scratch
artifacts were under `/tmp/metaprompt-{legacy,new}-trials/` and are ephemeral.

Historical tradeoffs: the Majkey adapter loaded a longer entrypoint and selected from
34 references; it does not reproduce legacy weighting or gate metadata. One
upstream coding-context template includes literal style-skill directives while
other upstream guidance makes them conditional. The observed trials correctly
omitted those directives. Upstream source dates and helper tests alone do not
establish improved task success.

## Coding handoff

The [atomic replacement plan](../plans/replace-metaprompt-with-sentry.md) tracks
scope, evidence, rollback, and remaining limitations. A paste-ready Cursor
prompt for a future update:

> Review the candidate staged by the metaprompt update helper against its
> current UPSTREAM.json. Preserve the local prompt-authoring adapter and
> metaprompt-alxve behavior. Apply only reviewed upstream files and matching
> pin/provenance changes. Run the automated commands and four behavioral
> trials in docs/metaprompt-skills.md, update docs/smoke-tests.md and the active
> plan, then refresh safely and verify installed files. Preserve unrelated
> dirty work and report unverified surfaces.

Suggested replacement commit: `feat(skills): use Sentry for metaprompt`.
