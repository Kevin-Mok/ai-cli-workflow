# Second Brain: How to Use the Examples

This hands-on tour shows how to use the real examples in
[`second-brain/`](../second-brain/) to carry useful context between work
sessions. Check status, choose one outcome, capture discoveries, then save
a reviewed closeout; the later examples cover health checks and approved
migrations. Second Brain complements Git, Taskwarrior, Graphiti, and private
journaling.

## The basic loop

Use this loop when work may continue later:

```text
status -> choose one outcome -> capture useful discoveries -> do the work -> closeout
```

Start with the installed command:

```bash
second-brain status --format text
```

The current example vault reports three active projects, an empty Inbox, and
the latest daily note. Read only the notes relevant to the work instead of
loading the entire vault.

## Where each example belongs

| Example | Use it for | Current example |
| --- | --- | --- |
| `00 Context/` | Stable identity, privacy, decisions, writing style, and memory ownership | [`Memory Map`](../second-brain/00%20Context/Memory%20Map.md) |
| `01 Inbox/` | Confirmed material that has not earned a better home yet | [`Brain Dump`](../second-brain/01%20Inbox/Brain%20Dump.md) |
| `02 Projects/` | Active outcomes with a goal and current state | [`ExampleProject`](../second-brain/02%20Projects/ExampleProject.md) |
| `03 Areas/` | Ongoing responsibilities that do not have an end date | [`AI Workflow`](../second-brain/03%20Areas/AI%20Workflow.md) |
| `04 Resources/` | Reusable knowledge and references | [`Linux Automation`](../second-brain/04%20Resources/Linux%20Automation.md) |
| `05 Daily Notes/` | A dated session or day summary | [`2026-07-14`](../second-brain/05%20Daily%20Notes/2026-07-14.md) |
| `06 Archive/` | Inactive material, only after explicit approval | [`Archive README`](../second-brain/06%20Archive/README.md) |
| `07 Attachments/` | Indexes and approved binary references, not automatic copies | [`Attachments README`](../second-brain/07%20Attachments/README.md) |

The root [`second-brain/README.md`](../second-brain/README.md) is the front door.
In Obsidian, its `[[...]]` links provide the same navigation.

## Example 1: use project context before coding

Suppose you are working on the Linux configuration workflow. Start with:

```bash
second-brain status --format json
```

Then open:

- [`Linux Config AI Workflow`](../second-brain/02%20Projects/Linux%20Config%20AI%20Workflow.md)
  for the goal, current state, and implementation evidence.
- [`AI Workflow`](../second-brain/03%20Areas/AI%20Workflow.md) for the ongoing
  responsibility.
- [`Linux Automation`](../second-brain/04%20Resources/Linux%20Automation.md)
  for reusable technical patterns.

The distinction matters: a project describes a result you are actively trying
to produce; an area describes something you maintain continuously; a resource
is reference material you may reuse.

For ExampleProject, use the [`ExampleProject` project note](../second-brain/02%20Projects/ExampleProject.md)
and choose one measurable outcome for the session. Do not turn every idea in
[`Beginner Python Teaching Sites`](../second-brain/02%20Projects/Beginner%20Python%20Teaching%20Sites.md)
into a task automatically.

## Example 2: capture something you learned

Capture discoveries, decisions, failures, and next steps that future you would
otherwise have to rediscover. Raw capture is private and is not added to Git.
Pipe JSON through standard input so secrets are not put in shell history:

```bash
second-brain capture --kind raw-session --payload - <<'JSON'
{
  "schema_version": 1,
  "event_id": "linux-config-example-20260715-01",
  "source": "terminal",
  "timestamp": "2026-07-15T14:00:00-04:00",
  "session_id": "linux-config-example-20260715",
  "role": "user",
  "text": "The Fish config is managed by chezmoi, so the tracked template is the edit point."
}
JSON
```

Do not capture passwords, API keys, tokens, proprietary code, or sensitive
personal details. The command redacts likely secrets, but privacy still starts
with what you choose to send.

If the fact is already durable and safe to track, use the confirmed decision
shape instead:

```bash
second-brain capture --kind personal-decision --payload - <<'JSON'
{
  "schema_version": 1,
  "event_id": "decision-example-20260715-01",
  "source": "terminal",
  "timestamp": "2026-07-15T14:05:00-04:00",
  "title": "Keep interests separate from projects",
  "summary": "Ask before promoting an interest into an active project or task.",
  "target": "00 Context/Decisions.md",
  "links": [],
  "visibility": "public-sanitized",
  "confirmed": true
}
JSON
```

Use this tracked form only after the summary is public-safe and explicitly
confirmed. Route information to its canonical owner instead of copying it
everywhere:

- workflow preferences -> `dot_agents/skills/feedback-memory/feedback.log`
- repository lessons -> `tasks/lessons.md`
- implementation state and verification -> `plans/`
- tasks -> Taskwarrior/Taskopen
- temporal facts and relationships -> Graphiti
- profile, projects, areas, resources, Inbox, and daily summaries -> this vault

## Example 3: set one focus

A focus is one measurable result, not a list of intentions. After example-user has
confirmed the outcome, send it to `focus`:

```bash
second-brain focus --payload - <<'JSON'
{
  "schema_version": 1,
  "event_id": "focus-example-20260715-01",
  "source": "terminal",
  "timestamp": "2026-07-15T14:10:00-04:00",
  "date": "2026-07-15",
  "project": "ExampleProject",
  "outcome": "Review one beginner Python lesson for clarity.",
  "done_when": "The lesson has one reviewed draft and no unresolved clarity issues.",
  "evidence": "docs/example-lesson-review.md",
  "confirmed": true
}
JSON
```

The first confirmed focus for a date is canonical. Reuse it across sessions;
do not silently replace it with a second outcome. The `evidence` field should
point to something a person can inspect.

## Example 4: close out with a handoff

At the end, write a boss-readable result. `planned` must exactly match the
confirmed focus outcome:

```bash
second-brain closeout --payload - <<'JSON'
{
  "schema_version": 1,
  "event_id": "closeout-example-20260715-01",
  "source": "terminal",
  "timestamp": "2026-07-15T16:00:00-04:00",
  "date": "2026-07-15",
  "project": "ExampleProject",
  "planned": "Review one beginner Python lesson for clarity.",
  "completed": "Reviewed the draft and resolved its clarity issues.",
  "evidence": "docs/example-lesson-review.md",
  "blocker": "",
  "decisions": [],
  "open": [],
  "next": "Choose the next lesson only after confirming a new outcome.",
  "confirmed": true
}
JSON
```

This is the handoff your next session should be able to understand without
reconstructing the whole conversation.

## Example 5: use Inbox, areas, resources, and archive correctly

The example Inbox is currently empty because raw capture does not land there
automatically. Add only confirmed, sanitized material with no clear owner. If
you can classify a note, place it directly in the right section:

- A reusable Fish or systemd pattern belongs in [`Linux Automation`](../second-brain/04%20Resources/Linux%20Automation.md).
- An ongoing teaching responsibility belongs in [`Teaching`](../second-brain/03%20Areas/Teaching.md).
- A durable cross-domain decision belongs in [`Decisions`](../second-brain/00%20Context/Decisions.md).
- An inactive note belongs in [`Archive`](../second-brain/06%20Archive/README.md) only after explicit approval.

The [`External Media Index`](../second-brain/07%20Attachments/External%20Media%20Index.md)
points to existing media; it does not copy pictures, PDFs, audio, or video into
the vault. Approved binary attachments require Git LFS and a passing doctor
check.

## Example 6: validate and checkpoint safely

Run the read-only health check when you are unsure whether the vault is valid:

```bash
second-brain doctor --format text --check
```

Use JSON for automation:

```bash
second-brain doctor --format json --check
```

Preview the allowlisted daily checkpoint before it changes Git state:

```bash
second-brain checkpoint --dry-run
```

The checkpoint can include Second Brain sections and `dot_codex/config.toml`,
but it does not include arbitrary dirty files. `--no-push` creates a local
checkpoint without pushing. The checkpoint owns Git shipping; the session
capture and closeout commands do not commit or push.

## Example 7: migrate selected external text

Migration is copy-first and approval-bound. It does not automatically import
`/home/example/Documents`, `/home/example/coding`, or the private journal. The
workflow is:

```bash
second-brain migrate inventory --source /home/example/Documents/some-export
second-brain migrate plan --inventory /path/to/inventory.json
second-brain migrate apply --plan /path/to/plan.json --approve SHA256_FROM_PLAN
second-brain migrate verify --ledger /path/to/private-ledger.json
```

Review the inventory and plan before applying them. Only explicitly selected
regular text files under the documented size limit are eligible; originals are
never moved, edited, or deleted.

For protected vault upgrades, preview first and apply only the exact approval
hash shown by the preview:

```bash
second-brain upgrade --dry-run
second-brain upgrade --apply --approve SHA256_FROM_PREVIEW
```

## Example 8: resume tomorrow

The next session starts with:

```bash
second-brain status --format text
```

Then read the latest daily note, the active project note, and the specific
resource or area that matches the work. For the current vault, that means the
2026-07-14 note plus the relevant one of ExampleProject, Linux Config AI Workflow,
or Beginner Python Teaching Sites.

The goal is not to remember everything. The goal is to make the next useful
step obvious.

## Quick rules

- Keep one confirmed measurable focus per day.
- Capture raw material privately; track only sanitized, confirmed summaries.
- Put each fact in one canonical owner.
- Keep project notes about active outcomes and area notes about ongoing duties.
- Use `doctor` before trusting a suspicious state and `checkpoint --dry-run`
  before a daily checkpoint.
- Never put secrets or sensitive personal details in tracked Markdown.

For the shorter beginner walkthrough, read
[`docs/second-brain-beginner.md`](second-brain-beginner.md). For the command-
oriented reference, read [`docs/second-brain.md`](second-brain.md).
