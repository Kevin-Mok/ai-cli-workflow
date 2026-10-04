---
name: second-brain-session
description: Use when starting, continuing, capturing, or closing a example-user work session that needs established project/session context, ExampleProject progress, persistent instructions, or Second Brain retrieval. An explicitly invoked personal-context chatbot discussion is a separate private workflow.
---

# Second Brain Session

Keep a work session connected to relevant personal and project context. Load
targeted notes, confirm one ExampleProject outcome, route useful information to its
owner, and prepare a confirmed closeout. The tracked vault is public-safe;
private raw capture stays outside Git.

Personal-context chatbot discussions and their learnings belong solely in
`/home/example/coding/personal-context`. They do not trigger this skill's Start,
Capture, Deferred Reminders, or Close workflows. Do not read that directory
implicitly or copy its content into raw capture, tracked notes, or Graphiti.
Use the separately requested session workflow for its established purpose.

## Start

1. Run second-brain status --format json.
2. Read second-brain/README.md, relevant personal context, Inbox state, the last
   two or three Daily Notes, and active project summaries. Do not load the entire
   vault.
3. Propose exactly one measurable ExampleProject outcome with:
   - Today: one numbered result.
   - Done when: the completion test.
   - Evidence: the visible artifact.
4. Always wait for example-user's confirmation before treating it as today's
   commitment.
5. Pipe the confirmed JSON through `second-brain focus --payload -`. If a
   focus already exists, reuse it; never replace it with a second outcome.

## Capture

Capture available session text events within this session workflow privately
with the command below. Exclude personal-context chatbot conversations and
learnings under the private boundary above.

second-brain capture --kind raw-session --payload -

The command must redact likely secrets. Never place payload text in shell
arguments. Route durable information through the ownership table in
references/routing.md. Add a tracked Second Brain summary only when it is
public-safe, useful for navigation, and explicitly confirmed.

Do not turn an interest into a project or task without asking example-user.

## Deferred Reminders

When example-user explicitly says to defer a task or return to it later, create the
private reminder immediately with `second-brain defer --payload -`; use
`"target_date": null` when no date is chosen. Report only safe result metadata.

At session start, use the status someday count. If it is nonzero, say the count
and ask whether example-user explicitly asks to review it. Only then run
`second-brain list-deferred --state someday --format json`. To set a date later,
use `second-brain schedule-deferred --payload -` with a future local date.

A deferred reminder never creates a focus automatically. A dated Inbox reminder
still requires example-user's separate focus, dismiss, or pending decision.

## Close

At a natural or explicit end:

1. Draft one boss-readable ExampleProject record containing Planned, Completed,
   Evidence, and Blocker.
2. Wait for example-user's confirmation.
3. Send confirmed JSON through second-brain closeout --payload -.
4. Report only the updated paths and operation result.

Never commit or push from this skill. The checkpoint, once installed, owns Git
shipping.

Read references/routing.md for schemas, memory ownership, privacy boundaries,
and recovery behavior.
