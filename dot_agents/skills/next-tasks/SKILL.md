---
name: next-tasks
description: >-
  Use only for explicit `next-tasks` or leftover weekly quota: propose evidence-backed tasks, wait for a choice, then execute it.
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
   - **Recent agent sessions run in this repo** (see below): what I asked
     for vs what got committed, work abandoned mid-session, follow-ups the
     agent promised, and requests I had to repeat.

3. Then list 5 things you can finish on your own in one go. For each, say:
   - what you'll do,
   - which files you'll change,
   - how you'll prove it's done (which test to run, or what result to look for),
   - the evidence that led to it: a commit sha, a doc path with a line
     number or short quote, or a session file with a short quote. No evidence,
     no task.
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

## Agent Sessions

Use sessions from whatever repo you are running in. Resolve it at runtime;
never hardcode a repo name or path.

```sh
root=$(git rev-parse --show-toplevel)
git worktree list --porcelain | sed -n 's/^worktree //p'   # root + worktrees
```

Codex writes one rollout per session to
`${CODEX_HOME:-$HOME/.codex}/sessions/YYYY/MM/DD/rollout-<timestamp>-<id>.jsonl`
(some may be compressed as `.jsonl.zst`; skip those or read them with `zstdcat`).
Each line is `{"timestamp", "type", "payload"}`. The first line has
`type: "session_meta"`, and its payload holds `cwd`, `timestamp`, and usually
`git` (`commit_hash`, `branch`, `repository_url`). Useful later lines:
`event_msg` with `payload.type` `user_message` (`.message` is my prompt),
`agent_message` (`.message`), and `task_complete` (`.last_agent_message`, the
final answer for that turn). Ignore `response_item`, tool output, and
reasoning records.

Keep it cheap: look only at the newest ~200 rollout files, keep at most ~15
matching sessions, and read only the first line of each file to match.

```sh
sessions="${CODEX_HOME:-$HOME/.codex}/sessions"
ls -t "$sessions"/*/*/*/rollout-*.jsonl 2>/dev/null | head -200 |
while read -r f; do
  head -n1 "$f" | jq -r --arg f "$f" \
    'select(.type=="session_meta") | [.payload.cwd, (.payload.git.branch // "-"), .payload.timestamp, $f] | @tsv'
done | while IFS=$'\t' read -r cwd branch ts f; do
  for wt in $(git worktree list --porcelain | sed -n 's/^worktree //p'); do
    case "$cwd/" in "$wt"/*) printf '%s\t%s\t%s\n' "$ts" "$branch" "$f"; break;; esac
  done
done | head -15
```

Then pull out only prompts and final answers from a matching file, trimmed:

```sh
jq -r 'select(.type=="event_msg") | .payload
  | select(.type=="user_message" or .type=="task_complete")
  | "\(.type): \((.message // .last_agent_message // "") | .[0:400])"' "$f" | head -60
```

Match sessions to commits by time and branch: compare the session's
`timestamp` and `git.branch` with `git log --format='%h %cI %D %s'`; a commit
made during or soon after a session on the same branch most likely came from
it.

If no sessions match, or the directory does not exist, skip this source
quietly. If Claude Code is used, its sessions live in
`~/.claude/projects/<cwd with / replaced by ->/*.jsonl`; treat them the same
way (records with `type` `user` / `assistant`, filtered by `cwd`).

Privacy: summarize sessions in a sentence or two and quote at most a short
line as evidence. Never paste long transcripts, and never surface secrets,
tokens, keys, or personal data found in logs.

## Explaining

If there's something I don't understand or have forgotten, explain it again in
a way a 10-year-old could understand.

## Credit

Adapted from @Voxyz_ai on X:
https://x.com/Voxyz_ai/status/2107214251408433365
