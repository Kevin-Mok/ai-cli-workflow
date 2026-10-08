---
name: second-brain-session
description: Use when starting, continuing, capturing, or closing a example-user work session that needs established project/session context, ExampleProject progress, persistent instructions, or Second Brain retrieval. Personal-context retrieval and learning are a separate private workflow.
---

# Second Brain Session

Review private work or connect a session to targeted context, one confirmed
ExampleProject outcome, and a confirmed closeout. The vault is public-safe; private
raw capture stays outside Git.

Explicit discussions, automatic personal-context retrieval, project knowledge,
and learnings stay solely in `/home/example/coding/personal-context`. Use the
personal-context skill; exclude content from raw session capture, tracked
notes, and Graphiti. It does not trigger session lifecycle workflows.

## Private work review

For a recap request or an explicit skill invocation, run
`second-brain sessions review --format json` to refresh changed sessions.
Present a recap and ask which outstanding check example-user wants to handle.
Review requires no ExampleProject outcome. Summaries report conversation claims,
not independent proof. Never prompt automatically at startup or send notifications.
Inferred checks remain review items; resolve only requested
checked/dismissed dispositions via `second-brain sessions resolve --payload -`.
See references/routing.md for the schema.

## Start

For a ExampleProject session:

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
5. Pipe confirmed JSON through `second-brain focus --payload -`. If a
   focus already exists, reuse it; never replace it with a second outcome.

## Capture

Capture available session text events privately within this workflow. Exclude personal-context conversations, briefs,
and learnings.

second-brain capture --kind raw-session --payload -

The command must redact likely secrets. Never put payload text in arguments.
Route durable information through references/routing.md. Tracked summaries
require public-safe content and explicit confirmation.

Do not turn an interest into a project or task without asking example-user.

## Deferred Reminders

When example-user explicitly defers a task, create the private reminder immediately with `second-brain defer --payload -`; use
`"target_date": null` when no date is chosen. Report only safe result metadata.

At session start, use the status someday count. If it is nonzero, say the count
and ask whether example-user explicitly asks to review it. Only then run
`second-brain list-deferred --state someday --format json`. Date with `second-brain schedule-deferred --payload -` with a future local date.

A deferred reminder never creates a focus automatically. Dated reminders
require a separate focus, dismiss, or pending decision.

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
