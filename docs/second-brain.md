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
- Exit `1`: check-only (`doctor --check`) found objective errors
- Exit `2`: input/schema/approval/safety gate was invalid

If you need the older, more detailed operator notes, use the specific command help
for each entrypoint.
