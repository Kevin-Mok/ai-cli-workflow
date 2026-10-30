---
name: night
description: Use only when I explicitly invoke `night` before stepping away, optionally with the task to build tonight. Work unattended on one self-verifiable job on a new local branch, never stop to ask questions, commit without pushing unless I said to push to a private repo's night branch, and leave an untracked `NIGHT_NOTE.md` hand-off for `morning`.
argument-hint: "[what to build tonight]"
disable-model-invocation: true
disallowed-tools: AskUserQuestion
---

# Night

I'm stepping away. Work on this tonight: $ARGUMENTS

In Codex, the task is whatever text follows `$night` in my message.

## Required Workflow

1. If I gave no task, pick one thing in this repo you can finish tonight and
   verify yourself (recent commits, TODO/FIXME comments, open issues via `gh`
   when it is set up). Skip anything that needs my call.
2. Before changing anything, write one line in `NIGHT_NOTE.md` at the repo root
   saying what you are doing. Never stage or commit `NIGHT_NOTE.md`.
3. Create a new branch (for example `night/<yyyy-mm-dd>-<slug>`) and change
   things only there. Commit to it when done; do not push unless I said to
   (see Optional Push Mode).
4. Do not deploy, delete files, touch secrets or CI config, run `chezmoi apply`,
   or call paid APIs.
5. Never stop to wait for me. When unsure, take the safest option, record the
   choice in `NIGHT_NOTE.md`, and keep going.
6. When done, run the relevant tests. If you cannot, write down why.
7. Finish `NIGHT_NOTE.md` with: branch name, what you did, how you tested it,
   what is still untested, and the questions for me in the morning, each with
   2-3 options (A/B/C) and your recommendation.

## Before Stepping Away

- Keep the machine awake (e.g. `systemd-inhibit` on Linux, `caffeinate -i` on
  macOS) and use an approval mode that will not pause for edits or commands.

## Running It As A Goal

- If I start this as a `/goal`, put the end time, the branch rule, and any push
  rule in the goal text itself, and repeat them whenever the goal is reset. A
  session that finishes its goal early goes idle and ignores rules I add later
  in chat until a fresh `/goal` carries them.
- Do not start a second session on the same repo. Extra sessions edit the same
  files and conflict.

## Optional Push Mode

Only when I say so in the task or goal: after each commit, push the night
branch to the private repo I named, with `git push origin <night-branch>`.
Never push `main`, never force-push, never open or merge a pull request, and
run a secret scan on the diff before the first push. If a push is blocked,
record why in `NIGHT_NOTE.md`, keep committing locally, and carry on.

## Optional Watcher And Reviewer Notes

- A separate watcher (another agent or routine) may check the session and
  review each commit. It must not edit code or push.
- Keep a `review-notes.md` next to `NIGHT_NOTE.md` for outside reviewers to
  append findings (commit hash, file, change wanted). Re-read it before each
  stage and after each commit, and apply what it asks or record why not.
