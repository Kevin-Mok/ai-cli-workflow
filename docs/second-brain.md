# Second Brain Operator Guide (Simplified)

Use these commands to keep private work notes and save approved summaries
that you can reuse next time. Check status, capture notes, confirm a focus,
then close out and validate the vault; use the later sections for
checkpoints, reminders, and migrations.

## What Second Brain is

- `second-brain/` is the tracked, plain-Markdown workspace.
- Private, raw session text lives outside Git and is handled separately.
- Confirmed writes are gated by strict schemas and safety checks.

Think of it as:

- Private journal = transient capture (not in Git)
- Tracked vault = durable, shareable context for context-aware sessions

## Trust boundaries

- Never place secrets, tokens, credentials, or highly sensitive personal details in
  tracked files.
- Confirmed public-safe writes only happen through the command flow below.

## Canonical owner map

| Information | Canonical owner |
| --- | --- |
| Durable workflow preference | `dot_agents/skills/feedback-memory/feedback.log` |
| Repo-specific engineering lesson | `tasks/lessons.md` |
| Implementation state / decisions / verification | `plans/` |
| Temporal facts / relationships | `Graphiti` |
| Trackable tasks and closeout notes | `Taskwarrior` / `Taskopen` |

## Daily workflow (start here)

1. Check your current session state

   ```bash
   second-brain status --format text
   ```

2. Capture session notes privately

   ```bash
   second-brain capture --kind raw-session --payload -
   ```

3. Set a focus for this session

   ```bash
   second-brain focus --payload -
   ```

4. Finish with a closeout

   ```bash
   second-brain closeout --payload -
   ```

5. Validate structure and safety before trusting changes

   ```bash
   second-brain doctor --format json --check
   ```

## Useful commands

- `second-brain status --format text|json`
- `second-brain capture --kind raw-session --payload PATH_OR_DASH`
- `second-brain capture --kind personal-decision --payload PATH_OR_DASH`
- `second-brain focus --payload PATH_OR_DASH`
- `second-brain closeout --payload PATH_OR_DASH`
- `second-brain doctor --format text|json [--check]`
- `second-brain checkpoint --dry-run`
- `second-brain checkpoint --no-push`
- `second-brain checkpoint`
- `scripts/executable_setup-second-brain-timer --check`
- `scripts/executable_setup-second-brain-timer --enable`
- `scripts/executable_setup-second-brain-timer --disable`

## Private reminders

Use `second-brain defer --payload -` with `"target_date": null` to keep a
private task in the someday queue. It stays outside Git and never becomes a
focus automatically. Use `second-brain schedule-deferred --payload -` to assign
a future Toronto-local date; the 04:00 persistent user timer promotes due dated
items to the private Inbox. Status shows only counts.

- `second-brain defer --payload PATH_OR_DASH`
- `second-brain schedule-deferred --payload PATH_OR_DASH`
- `second-brain process-deferred`
- `second-brain list-deferred --state inbox|someday --format json`
- `second-brain resolve-deferred --payload PATH_OR_DASH`

## Checkpoint (what it does)

`second-brain checkpoint` validates and prepares a protected daily commit path for
allowed paths only:

- `second-brain/00 Context/`
- `second-brain/01 Inbox/`
- `second-brain/02 Projects/`
- `second-brain/03 Areas/`
- `second-brain/04 Resources/`
- `second-brain/05 Daily Notes/`
- `second-brain/06 Archive/`
- `second-brain/07 Attachments/`
- `dot_codex/config.toml`

Run `--dry-run` first to preflight safely. Use `--no-push` for a local checkpoint
only.

## Timer

A user-level timer runs the daily checkpoint around 16:20 local time.

- Check setup: `setup-second-brain-timer --check`
- Enable: `setup-second-brain-timer --enable`
- Disable: `setup-second-brain-timer --disable`

## Private daily Codex work digest

Keep a private record of work across all local Codex projects, then review it
when you choose. Check status for freshness
and run review for a recap of the five most recently active work conversations.
This requires no ExampleProject focus and sends no notifications or startup prompts.

```bash
second-brain sessions refresh --format json
second-brain sessions review --format text
second-brain sessions review --details
```

Plain `second-brain sessions review` shows the five most recently active work
conversations across projects, newest first, whether or not they have open checks.
Each numbered entry includes title, project, Toronto-local activity, up to two
wrapped progress lines, and one next step when reported. Native Guardian/spawned
helpers are excluded, with title fallback for older records. Duplicate session
IDs occupy one slot, using their latest activity.

Review options:

- `--limit N` shows the newest N sessions (1–20; default 5).
- `--refresh-limit N` caps recap generation independently (0–20; defaults to
  the display limit). Zero discovers current sessions without inference.
- `--details` expands the selected sessions with full evidence, source paths,
  resume commands and stable check IDs.
- `--all` selects the complete eligible historical work inventory; it cannot be
  combined with an explicit `--limit`. Its default refresh budget is 20.
- `--plain` provides ASCII output without emoji, escaping non-ASCII content.
  Text uses no ANSI colors and respects `NO_COLOR`.
- `--format text|json` selects output format (default text). JSON retains the
  existing report structure and complete evidence for the selected sessions.

Review screens changed sources before displaying or summarizing them. Discovery
runs independently of the background backlog, so old pending work cannot crowd
out recent sessions. The first review scans uncached sources and can take longer;
subsequent reviews reuse safely screened metadata. Only selected missing or stale
recaps are generated, newest first, within the refresh budget. Unchanged dialogue
requires no model calls, including activity-only updates. Metadata fingerprints
and successful-summary hashes are separate; older state migrates without losing
check dispositions. Ambiguous old summary freshness requires regeneration.
Raw conversation text is never cached here.

Next steps come from the saved recap's remaining work or checks that it currently
reports as unresolved. Historical retained checks remain available in details
and private state; they do not become new recap tasks. A failed refresh keeps the
previous recap and labels it stale. Problems appear next to affected recaps;
global coverage, backlog and hidden-session counts stay in details/JSON.
The private `digest.md` continues to retain the full stored evidence.

Background `refresh` retains its fair queue and initial seven-day coverage
window. Its `--limit N` still bounds queued changed-source processing (1–20;
default 20), and text/JSON output stays metadata-only. Use
`refresh --limit 1 --format json` for a bounded live check. Review has no seven-day
display cutoff and does not enroll historical discoveries in the background
queue. Both operations use one inference worker with a 120-second per-session
timeout and share the private-state lock.

Treat reported completion as a conversation claim and recorded verification as
cited evidence, not independent proof. Recent activity does not establish that a
session is running. `status --format json` exposes only safe freshness/count/
coverage metadata. Review remains an explicit user action.

After explicitly deciding that a check is checked or dismissed, pipe JSON on
stdin to `second-brain sessions resolve --payload -`:

```json
{
  "schema_version": 1,
  "check_id": "copy-the-stable-id-from-review",
  "disposition": "checked",
  "confirmed": true
}
```

Dispositions persist across regeneration; open checks persist when their source
session ages out. Inferred checks never create tasks, reminders, or commitments.
The existing confirmation rules for public notes, focus, closeout, and deferred
reminders still apply.

Private structured state and readable Markdown are under
`${XDG_STATE_HOME:-~/.local/state}/second-brain/sessions/`, with 0700 directories
and 0600 files. No raw transcript copies or existing recap caches are imported. Discovery uses file fingerprints; background refresh screens at most its queue limit, while explicit review screens changed sources independently.
Personal-context sessions are conservatively skipped when safe separation is
unavailable, and likely secrets are redacted before inference and persistence.
Malformed or oversized sources are skipped rather than inferred, because privacy screening is incomplete. Status separates scan freshness (`refreshed_at`) from successful summary freshness (`summary_updated_at`). Native session titles are used when available; generated fallback titles are labeled inferred. Model inference is ephemeral, tool-disabled, and isolated from source sessions.
Scheduled/manual refreshes share a lock. Failed session inference retains prior
valid summaries while updating safe coverage/error metadata; state-write failures
preserve the last valid state. Authentication/quota failures stop the batch and expose safe metadata. Refresh
and review exit 1 when a safe refresh error is reported; queued/partial coverage
alone is not an error. Summaries remain fallible, consume Codex allowance, and may have visible queued coverage.

## Migration and upgrade

For larger moves, use the read-only / approval-first flow:

- `second-brain migrate inventory --source ...`
- `second-brain migrate plan --inventory ...`
- `second-brain migrate apply --plan ... --approve SHA256`
- `second-brain migrate verify --ledger ...`
- `second-brain upgrade --dry-run`
- `second-brain upgrade --apply --approve SHA256`

Use copy-first, resumable, and approval-bound steps only.

## Quick reference for common outputs

- Exit `0`: success or safe noop
- Exit `1`: check-only (`doctor --check`) found objective errors, or sessions refresh/review reported a safe refresh error
- Exit `2`: input/schema/approval/safety gate was invalid

If you need the older, more detailed operator notes, use the specific command help
for each entrypoint.
