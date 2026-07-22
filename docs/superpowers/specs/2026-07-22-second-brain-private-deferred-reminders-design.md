# Second Brain Private Deferred Reminders

## Goal

Let a session explicitly defer a full private reminder to a future local date.
At 04:00 local time on that date, Second Brain moves it into a private Inbox.
The item remains pending until example-user resolves it; it must never silently create
a focus, task, or tracked-vault entry.

## Scope

- Add a versioned, idempotent private deferred-reminder event.
- Add a daily 04:00 user timer that promotes due reminders to the private
  Inbox queue.
- Report private Inbox counts from `second-brain status`.
- Surface the full private text at the next Second Brain session and require
  confirmation before any focus is created.
- Support explicit, idempotent resolution after a focus is confirmed or the
  reminder is dismissed.

Out of scope: desktop notifications, automatic focus creation, Taskwarrior
integration, and writing private reminder text to `second-brain/01 Inbox/`.

## Data and Privacy Model

All reminder records live under the existing XDG private-state root, outside
the repository and with private directory and file permissions. A deferred
event contains schema version, event ID, source, timestamp, target local date,
session ID, and full text. The write path redacts likely secrets before storage
and rejects unsafe payloads without echoing them.

The timer changes an eligible item from `deferred` to `inbox` in the same
private store. It never copies the text into the Git-tracked vault. A resolved
item retains a minimal private audit record, including its resolution action,
so retries are safe and a repeated event ID is a no-op.

## Commands and Status

`second-brain defer --payload -` creates a deferred private item. The command
uses the existing JSON-on-stdin convention, validation behavior, mutation lock,
and content-safe errors.

`second-brain process-deferred` promotes every item due on or before the local
calendar date into the private Inbox. It is safe to run more than once; the
timer is simply its scheduled caller.

`second-brain resolve-deferred --payload -` resolves a private Inbox item only
after example-user chooses a disposition: `focused` after a separate confirmed focus,
or `dismissed`. It does not invoke `focus` itself.

`second-brain status --format json` gains private Inbox and deferred-item
counts. The text format reports counts only. Full reminder text is retrieved
only by the session workflow from the private queue.

## Scheduling and Session Flow

A systemd user service invokes `second-brain process-deferred`; its paired
timer runs at 04:00 in the user’s local timezone and is persistent so a missed
boot runs the next time the user service manager is available. The timer uses
the existing safe installer/enable/check conventions and does not require
privilege escalation.

When a Second Brain session starts, the skill checks status and reads due
private Inbox items. For each item it presents the full private wording and
asks example-user whether to use it as the day’s separate focus, dismiss it, or leave
it pending. Choosing a focus still follows the existing single confirmed
ExampleProject focus rule. If the daily focus is unavailable or example-user skips the
prompt, the item stays pending.

## Failure Handling

- A missing or unsafe private-state path fails before writing and reports a
  content-safe error.
- Timer failures leave records deferred; the next successful run promotes them.
- Invalid dates, duplicate IDs with different content, invalid resolution
  states, and lock contention fail without partial writes.
- A missing daily note or an already-confirmed daily focus does not resolve the
  private Inbox item.

## Verification

Tests will cover schema validation and secret handling, private permissions,
idempotent defer/process/resolve operations, 04:00 and missed-day promotion,
no tracked-vault writes, status count output, timer installation and calendar
schedule, plus the session-skill routing language. Documentation will cover the
new commands, privacy boundary, and timer lifecycle.

## Review Notes

The design intentionally keeps the full Felix-method wording private. Only a
later focus that example-user explicitly confirms may appear in the tracked Daily
Note, and it should remain public-safe.
