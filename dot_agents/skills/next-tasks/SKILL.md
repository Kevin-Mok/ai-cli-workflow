---
name: next-tasks
description: Use only when I explicitly invoke `next-tasks`, typically to spend leftover weekly quota before it resets. Don't start yet; infer work from recent git history (messages and diffs), repo docs, and prompt docs, list up to 5 things you can finish and prove on your own, each citing its evidence, wait for me to pick one, do only that, then show the diff and verification results.
argument-hint: "[optional focus area]"
disable-model-invocation: true
---

# Next Tasks

My weekly limit is about to reset with quota left. Find work you can finish
right now. Optional focus: $ARGUMENTS

In Codex, the focus is whatever text follows `$next-tasks` in my message.

## Required Workflow

1. Don't start yet. First find where this repo keeps its docs and prompts.
   Look around instead of assuming paths: list the top level, check for
   directories such as `docs/`, `plans/`, `prompts/`, `tasks/`, and `notes/`,
   and search for `*.md` files (`rg --files -g '*.md'`), including `README.md`,
   `AGENTS*.md`, `SKILL.md` files, and any skills catalog README.
2. Read these sources to infer tasks:
   - **Recent git history, messages and diffs** (for example
     `git log --stat -n 40` and `git show <sha>` on the interesting ones).
     Look for momentum, half-finished threads, follow-ups a commit promised,
     reverted or partial work, and files or areas that churned.
   - **Repo docs:** READMEs, plans, notes, roadmaps, `AGENTS.md`, and the
     skills README. Look for plans whose steps never landed, open questions,
     and documented behavior the code no longer matches.
   - **Prompt docs:** prompt files, `SKILL.md` files, and metaprompt outputs.
     Look for gaps between what a doc or prompt says should exist and what
     actually exists, stale instructions (wrong paths, renamed commands,
     removed files), and features or skills with no tests.
   If there is a lot, start with recently changed files and the most recent
   commits.
3. Then list 5 things you can finish on your own in one go. For each, say:
   - what you'll do,
   - which files you'll change,
   - how you'll prove it's done (which test to run, or what result to look for),
   - the evidence that led to it: a commit sha, or a doc path with a line
     number or short quote. No evidence, no task.
4. Only list things you can verify once done. Leave out anything that needs my
   call, uses a paid service, touches production, or deletes data. No vague
   filler like "optimize performance" or "improve the docs".
5. Put the ones with the biggest impact on this project first. If there aren't
   5 good ones, list fewer. Don't pad the list.
6. Stop and wait for me to pick one. Change nothing before I pick.
7. Do only the task I picked. When you finish it, stop and show me the changes
   (the diff) and the verification results (test output or observed result).
   Never claim a check passed if it did not run or failed.
8. Only list the next round after I confirm.

## Explaining

If there's something I don't understand or have forgotten, explain it again in
a way a 10-year-old could understand.

## Credit

Adapted from @Voxyz_ai on X:
https://x.com/Voxyz_ai/status/2107214251408433365
