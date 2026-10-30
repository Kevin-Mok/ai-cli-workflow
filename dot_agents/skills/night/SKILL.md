---
name: night
description: Use only when I explicitly invoke `night` before stepping away, optionally with the task to build tonight. Work unattended on one self-verifiable job on a new local branch, never stop to ask questions, commit and push after every commit, and leave an untracked `NIGHT_NOTE.md` hand-off for `morning`.
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
3. Create a new branch named `night/<yyyy-mm-dd>-<slug>`, where the slug is a
   few words describing tonight's task (for example `night/2026-10-29-pmo-backtest`),
   and change things only there. Commit in small steps and push the branch after every
   commit (see "Push After Every Commit").
4. Do not deploy, delete files, touch secrets or CI config, run `chezmoi apply`,
   or call paid APIs.
5. Never stop to wait for me. When unsure, take the safest option, record the
   choice in `NIGHT_NOTE.md`, and keep going.
6. When done, run the relevant tests. If you cannot, write down why.
7. Finish `NIGHT_NOTE.md` with: branch name, what you did, how you tested it,
   what is still untested, and the questions for me in the morning, each with
   2-3 options (A/B/C) and your recommendation. Put the questions in their own
   section at the end so I can answer them quickly.

## Before Stepping Away

- Keep the machine awake (e.g. `systemd-inhibit --what=idle:sleep sleep infinity`
  on Linux, `caffeinate -i` on macOS) and keep it plugged in. A running agent
  turn may block idle suspend by itself, but do not rely on that between turns.
- Use an approval mode that will not pause for edits or commands.
- Check on the session, for example with a scheduled read-only watcher that
  alerts only on a stall, a block, or repeated test failures.

## Running It As A Goal

An agent session that finishes its goal goes idle and may ignore rules added
afterwards. To keep it going until a deadline, set a goal that repeats
everything it needs, so it does not depend on earlier messages:

- the end time (for example "until 10:00 AM tomorrow") and "do not ask me
  anything"
- the files to read first: the task file, the plan, and `review-notes.md`
- the commit rule and the push rule
- the order of work, and the stop-at-first-failing-gate rule

If the goal completes early, set a new one with the same text and the new
work.

## Push After Every Commit

Always push the night branch right after each commit, so work is safe off the
machine and a reviewer can read it.

- Push the night branch under its own name, with
  `git push -u origin night/<yyyy-mm-dd>-<slug>`, so it never shares a branch
  with other work, and never reuse a branch from an earlier night. Push only
  that branch. Never push `main` or the default branch, never
  force-push, and never push `NIGHT_NOTE.md`.
- Prefer a private remote. If the repo has no remote, or the only remote is
  public and the work is not meant to be public, keep committing locally and
  note it in `NIGHT_NOTE.md`.
- Before every push, scan the staged files for secrets, `.env` files, and
  machine-local logs.
- If a push is rejected, do not retry with force. Note it in `NIGHT_NOTE.md`,
  keep committing locally, and try the next push normally.

## Optional: Outside Reviewer

When another agent or person reviews commits overnight, give them one shared
file, `review-notes.md`, next to the task file. They append dated notes with
an id. The working session re-reads it between steps, applies each note, and
records in `NIGHT_NOTE.md` what it applied or skipped and why. Reviewers
advise only; they do not edit code on the night branch.

## Optional: Trading And Backtest Work

For strategy or backtest tasks, add these rules to the task text:

- Signals use closed bars only and fill at the next bar's open. Higher
  timeframe values use the last completed bar, never the forming one.
- Fees and slippage are always on, and results are compared to an
  exposure-matched baseline.
- Split the data in time order, cap the number of trials, and leave the
  final holdout untouched until one last run.
- Paper trading only: no live keys and no real orders.
