# Second Brain Session Routing

Save session information in its canonical home while preserving privacy and
confirmation boundaries. Choose the owner for each fact, prepare the matching
payload, obtain required confirmation, and use the relevant capture, focus,
reminder, or closeout command.

## Memory Ownership

Route one fact to one owner:

| Information | Canonical owner |
|---|---|
| Personal-context conversations, automatic private learning, extracted project knowledge, and life-derived learnings (including workflow preferences) | `/home/example/coding/personal-context` only; read/update through the personal-context skill when relevant or explicitly invoked |
| Durable workflow or communication preference | dot_agents/skills/feedback-memory/feedback.log |
| Repository-specific engineering lesson | tasks/lessons.md |
| Implementation decision, state, or verification | plans/ |
| Temporal fact or relationship | Graphiti |
| Actionable task and attached note | Taskwarrior/Taskopen |
| Profile, Inbox, daily summary, project context, curated knowledge | second-brain/ |

Link to another owner when navigation improves; do not copy its full content.

The private personal-context row takes precedence over overlapping categories.
Do not mirror those facts or conversations into tracked profiles, feedback,
Graphiti, raw session capture, or any other service. A personal-context
invocation does not start a ExampleProject focus or session lifecycle. For a relevant development choice, use the personal-context skill and its
compact interface; other memory services must not ingest its private source or
retrieval results.

## Private Codex work digest

`second-brain sessions refresh --format text|json` incrementally updates private
summaries. `second-brain sessions review --format text|json` refreshes changed
sessions before displaying the digest and open checks. Use review only when
example-user asks for a recap or explicitly invokes the session skill. Present a compact
recap, then ask which outstanding check he wants to handle; do not require a
ExampleProject outcome for a recap. Scheduled refresh never prompts or notifies.

Inferred checks are private review items, not tasks or commitments. After an
explicit checked or dismissed request, pipe this shape through
`second-brain sessions resolve --payload -`:

```json
{
  "schema_version": 1,
  "check_id": "copy-the-stable-id-from-review",
  "disposition": "checked",
  "confirmed": true
}
```

`disposition` accepts `checked` or `dismissed`. Stable IDs and dispositions
survive regeneration, and unresolved checks survive their session aging out.
Review separates intentions, reported results, and recorded verification;
conversation claims never independently prove implementation. Surface unknown,
partial, stale, skipped, failed, and queued coverage. Recent activity does not
prove a session is running.

State and Markdown live beneath the private XDG Second Brain state root,
outside Git. Personal-context use excludes the whole session when separation
cannot be established. Policy mentions alone are not invocations. Likely secrets
are redacted before inference and persistence; existing recap caches are not
imported. Preserve existing focus, closeout, public-note, and deferred-reminder
confirmation boundaries.

## Raw Session Payload

Pipe JSON on stdin to second-brain capture --kind raw-session --payload -:

    {
      "schema_version": 1,
      "event_id": "stable-event-id",
      "source": "codex",
      "timestamp": "2026-07-14T09:30:00-04:00",
      "session_id": "stable-session-id",
      "role": "user",
      "text": "available session text"
    }

This is private raw capture under the XDG state directory. The command must
redact likely secrets, use private permissions, and make a repeated event ID a
no-op. Online GPT content is available only after example-user exports or supplies it.

## Confirmed Tracked Capture

Pipe this complete shape to
second-brain capture --kind personal-decision --payload -:

    {
      "schema_version": 1,
      "event_id": "stable-decision-event-id",
      "source": "codex",
      "timestamp": "2026-07-14T09:30:00-04:00",
      "title": "Keep interests separate from projects",
      "summary": "Ask before promoting an interest into a project or task.",
      "target": "00 Context/Decisions.md",
      "links": [],
      "visibility": "public-sanitized",
      "confirmed": true
    }

Use public-sanitized visibility. Do not capture proprietary code, credentials,
raw journal content, or sensitive relationship or health details. Do not turn
an interest into a project or task without explicit approval.

## Confirmed Daily Focus

After example-user confirms exactly one measurable ExampleProject outcome, pipe this shape
to second-brain focus --payload -:

    {
      "schema_version": 1,
      "event_id": "stable-focus-event-id",
      "source": "codex",
      "timestamp": "2026-07-14T09:30:00-04:00",
      "date": "2026-07-14",
      "project": "ExampleProject",
      "outcome": "Validate 20 Grade 8 contest questions.",
      "done_when": "20 of 20 validations are complete.",
      "evidence": "https://example.invalid/example-project-evidence",
      "confirmed": true
    }

The first confirmed focus is canonical for that date. Reuse it across sessions;
do not replace it with another outcome.

## Deferred reminders

When example-user explicitly defers a task or says to return to it later, create a private reminder immediately with `second-brain defer --payload -`. Use `"target_date": null` when no date is chosen; this keeps the reminder in the private someday queue. At session start, report only the someday count from `second-brain status --format json`. Ask whether example-user explicitly wants to review those reminders before running `second-brain list-deferred --state someday --format json`. Never create a daily focus automatically. When example-user chooses a date, run `second-brain schedule-deferred --payload -` with a future Toronto-local date.

## Closeout

Keep the result boss-readable.

Before calling second-brain closeout --payload -, show example-user:

- Planned: the confirmed measurable outcome.
- Completed: the observed number and artifact.
- Evidence: a visible link or path.
- Blocker: the remaining gap, or none.

Wait for confirmation, then pipe this complete shape on stdin:

    {
      "schema_version": 1,
      "event_id": "stable-closeout-event-id",
      "source": "codex",
      "timestamp": "2026-07-14T16:00:00-04:00",
      "date": "2026-07-14",
      "project": "ExampleProject",
      "planned": "Validate 20 Grade 8 contest questions.",
      "completed": "17 of 20 questions validated.",
      "evidence": "https://example.invalid/example-project-evidence",
      "blocker": "Three questions need source verification.",
      "decisions": [],
      "open": ["Verify three remaining sources."],
      "next": "Finish the remaining three questions.",
      "confirmed": true
    }

`planned` must exactly match the confirmed daily focus. A repeated event ID
must be a no-op.

If validation fails, report the field-level error without echoing payload
content. Never commit or push; leave Git shipping to the checkpoint once
installed and verified.
