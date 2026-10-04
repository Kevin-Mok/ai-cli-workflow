# Instructional document overviews

Make the repository's how-to documents easy to understand before asking the
reader to follow commands. Review the document inventory, add concise openings
where needed, then check that each overview matches the existing procedure.

## Purpose and observable outcome

Every maintained instructional document begins directly below its title with
plain language explaining what the reader can accomplish and the main steps.
Existing clear openings remain. Detailed commands, policy requirements,
frontmatter, links and historical evidence retain their original meaning.

## Context and scope

The user requested this sweep after adding the overview rule to canonical
`dot_codex/AGENTS.md`. The working repository is `/home/example/linux-config`.
The user explicitly confirmed `linux-config` as the target repository.
The related VPS guide already has the new overview and is outside this sweep.

Review operator documentation in `docs/`, root and nested READMEs, maintained
skill instructions/references, the plan contract, and other procedural Markdown
or templates discovered by the inventory. Classify each as edited, already
clear, or outside instructional scope. Preserve frozen benchmark candidates,
licenses, provenance records, generated caches, historical plans/postmortems,
standalone prompt artifacts, personal context notes and reference data.
Inspect ambiguous documents before deciding; location alone is not proof that
a file is a how-to. Frozen benchmark protocol/result evidence stays intact.

## Baseline and risks

`git status --short` was captured before edits. Existing dirty work includes
README, aliases, SSH/smoke docs, AGENTS/feedback from the preceding preference
change, terminal configuration, lessons/tests, and untracked plans/prompts and
incident records. Preserve those hunks and all existing files. The initial
request covered documentation edits; subsequent commit and push authorization
is recorded below. No worktree or VPS action is requested.

Avoid generic introductions, technical jargon, unsupported promises and
redundant summaries. Read each procedure before summarizing it. Skill trigger
metadata and machine import templates must remain valid. Rollback removes only
this sweep's introductory edits and associated coverage record.

## Implementation checklist

- [x] Capture baseline and inventory document locations.
- [x] Read the overview rule, preferences and ExecPlan contract.
- [x] Complete coverage classification for every instructional document family.
- [x] Update operator guides with tailored purpose and main-step overviews.
- [x] Update maintained instructional references that lack clear openings.
- [x] Review other README/template/procedural edge cases.
- [x] Check wording, body preservation, links, frontmatter and diff whitespace.
- [x] Apply managed instruction/doc changes through required refresh-config.
- [x] Record exact coverage, results and any exclusions here.

## Verification

This is an editorial change; no software feature tests are added or run.
Inspect each changed opening against its full body. Compare before/after
content to verify that commands and substantive requirements were preserved.
Run `git diff --check`; inspect relative links and title/frontmatter placement
for changed files. Check the final file list against the classified inventory.
When managed files change, preflight `snapshot-codex-config --dry-run`, run
`fish -ic 'refresh-config'`, and verify corresponding installed files match.

Manual review: read only the title and overview, state the intended outcome
and broad sequence, then compare that description with the detailed sections.
The existing smoke check for instructional overviews records this expectation.

## Coverage and results

The opening inventory contained 496 repository-owned Markdown/template paths.
The focused skills pass also checked 12 license/notice files. Existing clear
openings stayed in place; historical evidence, generated material and output
forms were classified rather than rewritten.

**98 instructional documents received an overview or placement improvement.**
Five import records also received the user-approved dated note explaining the
local editorial additions: 103 existing documents changed in this sweep.
The plan and two incident records are separate task records.

| Document family | Overview edits | Scope |
| --- | ---: | --- |
| Public README and operator guides | 14 | Root README; Docker Compose, VPS Codex repair, FlaviBot, Graphiti, metaprompt, phone SSH, five Second Brain guides, smoke checks and yt-dl |
| Skill entry points | 46 | Every `dot_agents/skills/*/SKILL.md` except the already-clear `commit-plan-push` and `metaprompt-alxve` |
| Skill reference guides | 25 | Listed below |
| System-design guides | 7 | Architecture, business strategy, coding standards, knowledge base, student packages, trusted sources and UI design |
| Plan contract | 1 | `.agent/PLANS.md` |
| Prompt-skill update/rollback guide | 1 | `dot_agents/skills/metaprompt/SOURCE.md` |
| Repository-local brand copies | 2 | `.agents/skills/brand-system-designer/SKILL.md` and its brand checklist |
| Other instructional entry points | 2 | `second-brain/README.md` and `txt/ubuntu/backup-script-prompt-ubuntu-h7.md` |

The 25 reference edits are:

- `brand-system-designer/references/brand-checklist.md`.
- All seven `frontend-design/reference/*.md` guides.
- `imagegen/references/{cli,codex-network,image-api,prompting}.md`.
- All four `metaprompt-alxve/references/*.md` guides.
- Both `open-pr/references/*.md` guides.
- `openai-docs/references/{latest-model,upgrading-to-gpt-5p4}.md`.
- Both `playwright/references/*.md` guides.
- `readme-recruiter-sync/references/readme-contract.md`.
- `second-brain-session/references/routing.md`.
- `transcribe/references/api.md`.

These paths are relative to `dot_agents/skills/`. Twenty-one design skills
previously had no title after YAML; they now have an H1 before their overview.
All existing titles remain. The two brand copies match their canonical files.

### Already clear and excluded material

The 115-file skills/system-design/plan-contract inventory contains 80 overview
edits, five provenance updates, seven already-clear documents and 23 exclusions.
The already-clear documents are the skill catalog, brand scoring rubric,
`commit-plan-push`, `metaprompt-alxve`, image sample prompts, GPT-5.4 prompting
guide and system-design index. `docs/design-skills.md` also already explains
its purpose and installation flow.

The root AGENTS routing files and canonical policy already explain their
purpose and authority. The Claude template is a machine import directive.
The short archive/attachment READMEs state their boundaries; the memory map,
personal context, task lists and disk inventory are reference material.
The brand-guide template is an output form, so editor-facing prose was not
inserted into its deliverable. Pure provenance, licenses and notices remain
intact apart from the five explicitly approved local-change annotations.

Frozen benchmark candidates/protocols/results, historical plans and incident
records, standalone prompt artifacts and historical design records retain
their original content. The eight native metaprompt files retain their recorded
hashes; the edited local wrapper and maintenance guide are outside that
inventory. Future imports should retain or reapply these local overviews.

### Review and verification evidence

- Independent review covered 16 operator/edge documents, 45 initially edited
  skill entry points and 25 reference guides. Review corrected README wording
  about public-safe notes, made skill invocation explicit, and removed a
  redundant Open PR purpose heading. The parent also corrected the unchanged
  CI guide's redundant Overview heading and reviewed the system-design
  openings against their documented workflows.
- Before snapshots retain pre-existing dirty document bytes at
  `/tmp/instructional-overviews-before/<path>`. The final preservation audit
  compared all 103 changed files with their snapshots (exit 0): frontmatter, existing titles,
  fenced code and detailed instructions remain intact. Only introductory prose,
  title additions, redundant introduction labels and the five approved source
  annotations change. No new Markdown link destinations were introduced.
- `./scripts/executable_readme-recruiter-sync` returned `pass_no_change`.
- `git diff --check` returned exit 0.
- All eight hashes in `dot_agents/skills/metaprompt/UPSTREAM.json` match.
- `./scripts/executable_snapshot-codex-config --dry-run` passed before refresh.
- `fish -ic 'refresh-config'` completed with exit 0 and `REFRESH COMPLETE`;
  final log: `/tmp/refresh-config-20261004-164423-597407.log`. Its live-to-source
  snapshot, chezmoi application and shortcut reload completed successfully.
  The final post-refresh comparison matched all 84 changed managed documents
  and canonical AGENTS after the CI-title cleanup. Both local brand copies also
  match their canonical source.
- No software tests or documented runtime procedures were executed for this
  editorial task. This evidence proves document preservation and installation,
  not the operation of every procedure described by those documents.

### Incident resolution and scope preservation

The optional-file lookup issue is recorded in
`docs/postmortem/2026-10-04-instructional-overview-inspection.md`. Automatic
approval review initially rejected six SOURCE edits. The user approved the
prepared patch explicitly; it was applied cleanly and native hashes remained
intact. See
`docs/postmortem/2026-10-04-instructional-overview-scope-review.md`.

Unrelated work was preserved. Concurrent terminal-workflow commits appeared
during the sweep; this task did not stage, commit or push those changes.
No VPS operation was performed.

## Commit boundary

The user invoked `$commit-session` to commit and push this work on `main` to
`origin/main` (user@example.invalid:example-user/ai-cli-dotfiles.git`). Keep this plan,
three session incident records, the overview rule and feedback entry with the
matching editorial changes. Commit subject:
`docs: clarify instructional guide overviews`.

The helper identified thread `01a1084b-ff59-7003-bda3-b1494285c9e9` but reported
no detected writes through the session tool wrapper. Direct-write evidence and
exclusive original snapshots establish the fallback scope: 109 eligible paths.
The phone SSH guide contributes only its opening; smoke checks contribute the
opening and overview-rule check. Earlier endpoint instructions and their manual
check remain unstaged, along with aliases and unrelated plans, prompts and
incident records. No pre-existing staged paths were present.

Fresh commit checks passed: README gate (`pass_no_change`), whitespace check,
103-document preservation comparison and all eight pinned native hashes. The
scoped patch passes `git apply --cached --check`. No runtime test is needed for
these editorial changes. Inspect the exact index before committing and push
once after the verified commit; report the actual delivery result in chat.
