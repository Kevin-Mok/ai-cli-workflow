# Second Brain Operator Guide

The Second Brain is a deterministic, plain-Markdown context layer shared by
Codex and Claude. The tracked vault stays public-sanitized and inspectable;
private raw session capture stays outside Git. This guide covers the verified
Task 2 command surface. The daily Git checkpoint and timer remain a separate
Task 3 concern.

## Trust And Memory Boundaries

The tracked vault lives at [second-brain/](../second-brain/) and uses a
PARA-style layout for profile context, Inbox navigation, active projects,
ongoing areas, curated resources, daily summaries, archive material, and
attachment indexes. It must never contain credentials, tokens, proprietary
code, raw journals, or sensitive relationship or health details.

Private raw capture lives below XDG_STATE_HOME/second-brain/raw, or below
HOME/.local/state/second-brain/raw when XDG_STATE_HOME is unset. Directories
use mode 0700 and event files use mode 0600. Migration resume ledgers use the
same private state root under second-brain/migrations. Neither belongs in Git.

One fact still has one canonical owner:

| Information | Canonical owner |
| --- | --- |
| Durable workflow or communication preference | dot_agents/skills/feedback-memory/feedback.log |
| Repository-specific engineering lesson | tasks/lessons.md |
| Implementation state, decision, or verification | plans/ |
| Bounded continuation artifact | context-handoff |
| Temporal fact or relationship | Graphiti |
| Actionable task and attached note | Taskwarrior/Taskopen |
| Profile, Inbox, daily summary, project context, curated knowledge | second-brain/ |

The complete payload schemas and routing rules live in
[the session routing reference](../dot_agents/skills/second-brain-session/references/routing.md).
Send payload text through a file or standard input, never a shell argument.
Tracked focus, decisions, and closeout writes require explicit confirmation.

## Entrypoints And Exit Codes

From this source checkout, use scripts/executable_second-brain. After
chezmoi apply, use the installed second-brain command from any directory.
Neither entrypoint needs sudo.

| Exit | Meaning |
| --- | --- |
| 0 | Command completed, including an idempotent noop. |
| 1 | doctor --check or migrate verify found objective errors. |
| 2 | Input, schema, approval, path, permission, or lock state was invalid or unsafe. |

Machine output is compact, key-sorted JSON. Errors name the failed field or
invariant without echoing payload or rejected source content. Capture
mutations report created, updated, or noop.

## Daily Session Workflow

Start with targeted retrieval:

    second-brain status --format json

The shared second-brain-session skill reads only relevant context, proposes
exactly one measurable ExampleProject result with a completion test and evidence
location, and waits for confirmation. It then persists the first focus for
that Toronto-local date. Later sessions reuse it rather than replacing it.

Raw events may be captured privately with:

    second-brain capture --kind raw-session --payload -

A confirmed public-safe personal decision uses kind personal-decision. At
closeout, the skill first shows Planned, Completed, Evidence, and Blocker in
boss-readable language. Only after confirmation does it call:

    second-brain closeout --payload -

The planned value must exactly match that date's confirmed ExampleProject focus.
Stable event IDs make identical retries noops; reusing an ID with different
content is rejected.

Protected-note updates acquire a fail-closed Linux write lease, validate the
displaced bytes after an atomic exchange, and verify the installed bytes. A
note that is open elsewhere or changes during the operation is never silently
overwritten. Review the competing edit, close the editor if appropriate, and
retry with the same payload.

If an error says that conflict recovery was preserved, stop and keep both the
visible note and its hidden `.NAME.RANDOM.tmp` sibling. The sibling contains
the displaced or concurrently changed bytes. Compare them before choosing an
authoritative version; do not delete the recovery file merely to make the
doctor pass.

## Vault Doctor

The doctor is read-only:

    second-brain doctor --format text
    second-brain doctor --format json --check

It audits the required manifest, regular-file, hard-link, and symlink
boundaries, frontmatter, visibility, unresolved placeholders, likely secrets,
duplicate canonical preference/lesson content, imported-note source hashes,
and attachment Git LFS coverage. Secret-like filenames are always rejected.
Vault and canonical-owner content scanning reads only UTF-8 candidates strictly
smaller than 1,000,000 bytes. Larger media is not loaded into memory and is
still checked for LFS coverage, while oversized Markdown or canonical-owner
files are errors. Finding keys and JSON ordering are stable. Without --check,
findings are reported with exit 0; with --check, any error produces exit 1.

## Copy-First Text Migration

Migration is deliberately multi-step. Inventory and plan are read-only. Apply
requires the exact approval SHA printed by the plan, preflights every source
before the first copy, never modifies a source, and never overwrites a
destination.

Inventory and plan controls contain private operational metadata: absolute
source roots, relative filenames, and eligible titles. Keep them in a private
state directory, create files under `umask 077`, and never stage or commit them.

1. Prepare a mode-0700 control directory and inventory one or more explicitly
   selected absolute roots. The subshell creates a new mode-0600 control file.

       control_dir="${XDG_STATE_HOME:-$HOME/.local/state}/second-brain/migration-control"
       install -d -m 700 "$control_dir"
       (umask 077; second-brain migrate inventory --source /absolute/source-one --source /absolute/source-two > "$control_dir/inventory.json")

2. Inspect the inventory. Rejected records contain classification metadata,
   never file content. Keep or remove whole roots before continuing.

3. Build and inspect the deterministic plan.

       (umask 077; second-brain migrate plan --inventory "$control_dir/inventory.json" > "$control_dir/plan.json")

4. Copy approval_sha256 only after reviewing every mapping and destination,
   then apply that exact plan.

       second-brain migrate apply --plan "$control_dir/plan.json" --approve APPROVAL_SHA256

5. Verify copied destinations and unchanged sources using the private ledger
   path returned by apply.

       second-brain migrate verify --ledger /absolute/path/returned/by/apply.json

Initial migration is intentionally unapplied. In particular,
/home/example/coding is reference-only and is rejected as a migration root.
Choose narrower approved material elsewhere rather than bulk-copying code.

### Eligibility And Mapping

Only regular UTF-8 text files strictly smaller than 1,000,000 bytes are
eligible. Inventory, planning, and apply recheck the policy. They reject:

- files that are too large, invalid UTF-8, or contain a NUL byte
- secret-like filenames or content, including netrc credential stanzas
- logs, caches, editor/app data, and nested Git repositories
- symlinks, hard links, and other non-regular filesystem entries

Every source maps to 06 Archive/Imports/SANITIZED_SOURCE. Portable,
NFKC-normalized names avoid Windows device names and forbidden characters.
Case-insensitive or normalized collisions receive stable " 2", " 3", and later
suffixes. Non-Markdown filenames gain a .md suffix. Each copy receives
public-sanitized archive frontmatter while its original body bytes remain exact.

### Resume And Recovery

Apply creates a private 0700 ledger directory and a 0600 JSON ledger named for
the approval SHA. The ledger embeds the approved plan and records its paths,
checksums, and per-entry pending or copied state, so standalone verification
can recompute the plan binding. Apply and verify reject symlinked ledger parent
components, hardlinked ledgers, non-current ownership, directory modes other
than 0700, and file modes other than 0600. A retry adopts a matching copy,
skips a completed matching copy, and continues pending entries. A completed
retry is byte- and mtime-stable and reports noop.

If apply stops, do not edit destinations or the ledger. Run the same plan with
the same approval again, then run migrate verify. Pending entries and checksum
mismatches are errors. Preserve both sides and create a fresh inventory and
plan rather than forcing a stale ledger. Restore a changed tracked destination
from Git only after deciding which version is authoritative.

## Protected Vault Upgrades

Preview is always the first step:

    second-brain upgrade --dry-run

The initial schema-v1 vault currently has no pending operations, so its preview
contains an empty operations list. Future releases add immutable, append-only
upgrade specifications in code. A non-empty preview includes one approval SHA
for the complete batch. After inspection, apply only that exact preview:

    second-brain upgrade --apply --approve APPROVAL_SHA256

Apply rechecks the preview under the mutation lock and rejects stale approvals.
Keep the inspected preview until apply finishes. Before changing a protected
note, apply writes an exact-byte, dated backup below
second-brain/06 Archive/backups. An existing or late-arriving backup gets a
stable " 2" suffix instead of being overwritten. New files use an atomic
no-overwrite operation.

Each file operation is atomic, but a multi-operation batch is not
transactional. A late filesystem failure can leave earlier operations applied.
If apply fails, do not run it again immediately. Compare every operation in the
approved preview with its current target:

- for an update whose current bytes match `after_sha256`, use its dated backup
  when an explicit rollback decision is made
- for a create whose current bytes match `after_sha256`, explicitly decide
  whether to retain or remove that created file
- if any target does not match the preview, preserve it and stop rather than
  overwriting or deleting a changed or unrelated file

After the batch is deliberately restored or accepted, run the doctor and make a
new dry-run. An accepted, already-applied state produces an empty preview;
applying that current empty-batch approval reports `noop`. An exact rollback can
make the operations reappear, and a deterministic same-day preview can reproduce
the earlier approval SHA. Always recompute and review the current preview, then
use only the approval shown by that preview; never assume that an earlier value
is stale or reusable without comparing the current operations. Never edit
upgrade markers merely to make a preview disappear.

## Provenance

The design adapts PARA navigation, daily routines, copy-first migration,
protected upgrades, and optional Obsidian ideas from the MIT-licensed
Alxve99/second-brain-setup prompt at commit
90584269f7a4a47ea19f85a9029246873365aaf8. Local tests define the behavior,
and the adaptation preserves this repository's existing memory owners. See the
exact [source record](../dot_agents/skills/second-brain-session/SOURCE.md).
