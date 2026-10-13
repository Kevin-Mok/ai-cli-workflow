---
name: morning
description: Use only when I explicitly invoke `morning` to pick up after a `night` run. Read `NIGHT_NOTE.md` and the night branch's git history, summarize what happened, list up to five numbered A/B/C questions with recommendations, then act only on the answers I give.
disable-model-invocation: true
disallowed-tools: AskUserQuestion
---

# Morning

I'm back. Report on the `night` run and get my decisions.

## Required Workflow

1. Read `NIGHT_NOTE.md` at the repo root first. If it is missing, say so and
   fall back to recent local branches and `git log`.
2. Use `git log` and `git diff <base>...<night-branch> --stat` to see what
   changed on last night's branch. If `gh` is installed and authenticated,
   also check CI status and new issues and PRs.
3. Start with three to five sentences on what was done overnight, including
   what was tested and what is still untested.
4. Then list the questions only I can answer, up to 5, numbered. Give each
   two or three options labeled A, B, C, and mark the recommended one with a
   one-line reason. Ask in plain text, not a question pop-up.
5. When I reply like `1A, 3B`, do what I picked. If I say "the rest as
   recommended", apply your recommendations for the rest. Do not touch
   anything I did not mention, and do not push or merge unless I ask.
