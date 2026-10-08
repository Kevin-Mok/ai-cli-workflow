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

## Private daily Codex work digest

Keep a private record of work across all local Codex projects, then review it
when you choose. Enable the dedicated daily timer, check status for freshness,
and run review for five recent work directories with three session recaps each.
This requires no ExampleProject focus and sends no notifications or startup prompts.

```bash
second-brain sessions refresh --format json
second-brain sessions review --format text
second-brain sessions review --details
setup-second-brain-sessions-timer --check
setup-second-brain-sessions-timer --enable
```

Plain `second-brain sessions review` shows the five most recently active
directories, ordered by their newest eligible conversation activity. Each
directory contains its three newest sessions (fewer when unavailable), whether
or not they have open checks. Each session includes title, Toronto-local activity and full wrapped sections for
goal, intentions, accomplishments, next step, remaining work, blockers and
verification reports. Session metadata, source paths, resume commands and check
IDs are included by default; no recap text is truncated. Native Guardian/spawned
helpers are excluded, with title fallback for older records. Duplicate session
IDs occupy one slot, using their latest activity.

Interactive text review opens in `bat` (or `batcat`) through `less`, with folder,
session, time, recap and next-step emoji cues. Use Space/Page Down to advance,
`/text` to search, `r` to refresh the displayed selection and recaps, and `q` to quit. The same applies to `--details`. If bat is
missing, it uses less; if no viewer is installed, it prints directly. JSON,
redirected output and `--plain` never open a pager. `NO_COLOR` disables bat
coloring. Review prints elapsed-time activity to stderr every five seconds
while discovery or recap generation runs, so machine-readable stdout stays clean.
Fast cached reviews emit no progress noise.

Review options:

- `--limit N` shows the newest N directories (1–20; default 5), each with up to three sessions.
- `--refresh-limit N` caps recap generation independently (0–20; defaults to
  three recaps per directory, capped at 20). Zero discovers current sessions without inference;
  missing recaps remain **Recap not generated**. Remove this option to generate
  or refresh recaps immediately. Inside the pager, `r` refreshes the snapshot and
  enables the normal recap budget after a zero-budget preview; explicit positive
  refresh budgets persist. Unchanged recaps are reused without inference.
- `--details` keeps the same full prettified report as the default; it is retained
  for compatibility. The private Markdown archive is not used for terminal output.
- `--all` selects the complete eligible historical work inventory; it cannot be
  combined with an explicit `--limit`. Its default refresh budget is 20.
- `--no-pager` prints directly while keeping emoji formatting.
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
and successful-summary hashes are separate; parser revisions re-screen metadata
without certifying old exclusions. Older state migrates without losing
check dispositions. Ambiguous old summary freshness requires regeneration.
Unknown executable input containing private-store paths is conservatively
excluded; inert source/test literals in such input may still cause an exclusion.
A compact warning states when private or uncertain sessions make recent work
incomplete.
Raw conversation text is never cached here. Public AGENTS policy output and
reads of the public personal-context skill do not count as private-store access.
Actual private-store tool invocations, private working directories and explicit
personal-context conversations remain excluded; tool output never enters recaps.

Next steps come from the saved recap's remaining work or checks that it currently
reports as unresolved. Historical retained checks appear under **Earlier checks**, including their
dispositions and resolution times; they do not become new recap tasks. A failed refresh keeps the
previous recap and labels it stale. Problems appear next to affected recaps;
a readable **Review coverage** footer includes refresh times, model calls,
backlog and hidden-session counts. JSON retains the complete machine-readable fields.
The private `digest.md` continues to retain the full stored evidence.

Background `refresh` retains its fair queue and initial seven-day coverage
window. Its `--limit N` still bounds queued changed-source processing (1–20;
default 20), and text/JSON output stays metadata-only. Use
`refresh --limit 1 --format json` for a bounded live check. Review has no seven-day
display cutoff and does not enroll historical discoveries in the background
queue. Both operations use one inference worker with a 120-second per-session
timeout and share the private-state lock.

The timer runs at 16:00 `America/Toronto`, persists missed runs, and never
activates or changes the checkpoint or deferred timers. It uses your existing
Codex authentication and configured model. No sudo is required. Disable only
this job with `setup-second-brain-sessions-timer --disable`; private digest state
is retained. The source helper is
`scripts/executable_setup-second-brain-sessions-timer`.

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
and 0600 files. No raw transcript copies or existing recap caches are imported. Discovery uses file fingerprints; background refresh screens at most its queued-source limit; explicit review screens changed sources independently.
Personal-context sessions are conservatively skipped when safe separation is
unavailable, and likely secrets are redacted before inference and persistence.
Malformed or oversized sources are skipped rather than inferred, because privacy screening is incomplete. The timer helper pins the active Codex/Node installation in a private service drop-in and checks matching installed parser/runtime files; run `refresh-config` before `--check` or `--enable`. `--disable` does not require those dependencies. Status separates scan freshness (`refreshed_at`) from successful summary freshness (`summary_updated_at`). Native session titles are used when available; generated fallback titles are labeled inferred. Model inference is ephemeral, tool-disabled, and isolated from source sessions.
Scheduled/manual refreshes share a lock. Failed session inference retains prior
valid summaries while updating safe coverage/error metadata; state-write failures
preserve the last valid state. Authentication/quota failures stop the batch and expose safe metadata. Refresh
and review exit 1 when a safe refresh error is reported; queued/partial coverage
alone is not an error. Summaries remain fallible, consume Codex allowance, and may have visible queued coverage.

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
- Exit `1`: `doctor --check` found objective errors, or sessions refresh/review reported a safe refresh error
- Exit `2`: input/schema/approval/safety gate was invalid

If you need the older, more detailed operator notes, use the specific command help
for each entrypoint.
