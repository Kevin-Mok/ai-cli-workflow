---
name: next-tasks
description: Use only when I explicitly invoke `next-tasks`, typically to spend leftover weekly quota before it resets. Don't start yet; read the repo's recent commits, TODO/FIXME comments, and open issues (via `gh` if set up), list up to 5 things you can finish and prove on your own, wait for me to pick one, do only that, then show the diff and verification results.
argument-hint: "[optional focus area]"
disable-model-invocation: true
---

# Next Tasks

My weekly limit is about to reset with quota left. Find work you can finish
right now. Optional focus: $ARGUMENTS

In Codex, the focus is whatever text follows `$next-tasks` in my message.

## Required Workflow

1. Don't start yet. Read this repo's recent commits, the TODO / FIXME comments
   in the code, and open issues (if `gh` is set up and authenticated). If there
   are none, just read the code.
2. Then list 5 things you can finish on your own in one go. For each, say:
   - what you'll do,
   - which files you'll change,
   - how you'll prove it's done (which test to run, or what result to look for).
3. Only list things you can verify once done. Leave out anything that needs my
   call, uses a paid service, touches production, or deletes data. No vague
   filler like "optimize performance" or "improve the docs".
4. Put the ones with the biggest impact on this project first. If there aren't
   5 good ones, list fewer. Don't pad the list.
5. Stop and wait for me to pick one. Change nothing before I pick.
6. Do only the task I picked. When you finish it, stop and show me the changes
   (the diff) and the verification results (test output or observed result).
   Never claim a check passed if it did not run or failed.
7. Only list the next round after I confirm.

## Explaining

If there's something I don't understand or have forgotten, explain it again in
a way a 10-year-old could understand.

## Credit

Adapted from @Voxyz_ai on X:
https://x.com/Voxyz_ai/status/2107214251408433365
