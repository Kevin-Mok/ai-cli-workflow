---
name: feedback-memory
description: >-
  Use for durable user corrections or preferences about workflow, formatting, style, tooling, review or communication, and sessions needing prior feedback.log guidance.
---

# Feedback Memory

Carry forward reusable user feedback across sessions with one canonical
append-only log. Read the existing preferences, apply them to the current
work, and append new durable corrections when the user gives them.

## Log Path

Use this resolution order:

1. Prefer `~/linux-config/dot_agents/skills/feedback-memory/feedback.log` when it exists. In this chezmoi-managed setup, that is the canonical log because `~/linux-config` is the source state.
2. Otherwise, fall back to `feedback.log` in this installed skill folder.
3. If both files exist, read and append only the repo-tracked path.

## When to use

Use this skill when:
- starting a session and prior durable feedback may matter
- the user gives a correction or preference that should change future behavior
- the feedback is about workflow, style, formatting, review expectations, tooling habits, or communication

## When not to use

Do not log:
- personal-context conversations, automatic private learning, project knowledge,
  source facts, or life-derived learnings,
  including workflow/communication preferences learned in that private setting;
  their sole owner is `/home/example/coding/personal-context`; use the
  personal-context skill for relevant compact retrieval and never mirror its
  contents into this log
- task-specific instructions tied to the current ticket, branch, file, or investigation
- one-off requests or temporary preferences
- ephemeral facts that will age out quickly
- details that duplicate the current task context instead of generalizing beyond it

## Required workflow

1. Resolve the canonical log path using the rules above.
2. Before doing anything else in the session, read the canonical `feedback.log`.
3. Treat the log as durable operating guidance. Apply it throughout the session unless the user overrides it explicitly.
4. When the user gives new durable feedback outside the private personal-context boundary above, append it to the canonical log immediately before continuing. Only independently public-safe operating feedback belongs here.
5. Do not create, update, or reconcile a second log when the repo-tracked path exists.
6. Keep the file append-only. Do not rewrite, reformat, dedupe, or move old entries unless the user explicitly asks.
7. If the feedback is ambiguous, log only the durable part that would still help in a different future task.
8. After a run where the user corrected a skill-driven workflow, ask: one-time fix, or should this be in the skill forever? Log it here or edit that skill's `SKILL.md` only when it is permanent.

## Consolidation (repeated wins become skills)

Method borrowed from the `continuous-learning-v2` skill in
[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning-v2)
(MIT, (c) 2026 Affaan Mustafa): atomic patterns, evidence-backed confidence,
then promotion. Its hooks, observer agent, and storage are not used here.

1. Candidate: one atomic trigger -> action pattern from `feedback.log` or `tasks/lessons.md`.
2. Threshold: propose promotion only after it applied successfully 3+ times in separate sessions, each with cited evidence (date plus commit, PR, or log line). Fewer or uncited = keep it as a lesson.
3. Target: prefer merging into an existing skill's `SKILL.md` and avoid growing the skill count; a new skill needs a stated reason no existing skill fits.
4. Shrink: each proposal names the lesson entries it retires. Once applied, append `YYYY-MM-DD - consolidated into <skill>: <entries>`; never delete or rewrite old lines in append-only files.
5. Ask the user before writing any skill (the step 8 one-time-or-permanent question); show the target, diff, evidence, and retired entries.

## What to log

Log reusable notes such as:
- formatting and response-style preferences
- review expectations and quality bars
- tooling habits or workflow preferences
- corrections that would prevent repeating the same mistake

## Entry format

- Prefix each entry with `YYYY-MM-DD - `
- Use one line for brief durable preferences.
- For nuanced corrections, add one short continuation line indented by two spaces.
- Keep entries concrete and operational.

## Rule Of Thumb

Log it only if it would still be useful in a different future task.
