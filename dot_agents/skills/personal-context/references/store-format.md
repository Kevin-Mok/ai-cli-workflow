# Private conversation memory

Use the bundled helper to read relevant learnings and save validated updates
inside the external personal-context directory. Prepare a small JSON payload,
send it on stdin, and check the safe result metadata before reporting success.
The helper handles storage; the agent supplies evidence and conversational judgment.

## Location And Commands

Default root: `/home/example/coding/personal-context`. The only data destination
is its `ai-context/context.json`; existing Markdown sources remain untouched.
The helper requires Python 3.12 or newer and uses only the standard library.
Use the absolute installed helper path:

```sh
python3 ~/.agents/skills/personal-context/scripts/context_store.py read
python3 ~/.agents/skills/personal-context/scripts/context_store.py read --topic design
python3 ~/.agents/skills/personal-context/scripts/context_store.py read --include-inactive
python3 ~/.agents/skills/personal-context/scripts/context_store.py validate
python3 ~/.agents/skills/personal-context/scripts/context_store.py update --payload -
```

`read` intentionally returns private content to the active conversation; never
redirect that output into a repository artifact or validation log. Default reads
include active statements and unconfirmed interpretations. Include inactive
entries only when reviewing history. Missing memory reads as an empty store
without creating directories; missing memory does not pass `validate`.

`update` accepts JSON only on stdin. Use structured subprocess input or a
single-quoted heredoc; do not interpolate a private payload into shell arguments.
When staging a payload file is necessary, keep it under the private root with
0600 permissions and remove it after the successful update. The global `--root`
option is for explicit synthetic test directories, never repository storage.

## JSON Version 1

The document contains `schema_version: 1`, `revision`, `updated_at`, `entries`,
`questions`, `forgotten_keys`, and `forgotten_question_ids`. The helper owns
revisions and write timestamps. The last two arrays contain key/ID-only
suppression markers, with none of the removed statements or questions.

Each entry has:

| Field | Meaning |
| --- | --- |
| `id` | Stable ID for this particular learning; reuse for an exact retry |
| `key` | Stable concept key, reused for corrections and forgetting |
| `topic` | Retrieval category, such as design, workflow, interests, or capability |
| `statement` | One concise learning, preserving the person's meaning |
| `basis` | `user_stated`, `source_reported`, `observed`, or `inferred` |
| `source` | `{ "ref": "file/section or conversation reference", "as_of": "date or null" }` |
| `recorded_at` | Recording timestamp; preserve original source dates separately |
| `scope` | Where the learning applies, including project-specific limits |
| `status` | `active`, `unconfirmed`, or `superseded` |
| `implication` | Supported development implication, or null when not established |

The update payload accepts only `entries`, `questions`, `forget_keys`, and
`forget_question_ids`.
Entry recording time and status can be assigned by the helper. New inferred
entries are always unconfirmed. Do not label imported prose as a new direct
statement or describe a file-modification date as personal confirmation.

Question updates use `id`, `topic`, `question`, `reason`, and `status` (`open`,
`answered`, or `declined`); the stored record also has helper-maintained
`updated_at`, which must not be submitted. Update the same question ID when its
disposition changes. `reason` explains which development choice its answer
could improve. An answered/declined ID cannot be reopened by a stale payload.
If example-user explicitly revisits the topic, create a new question ID with the new
context, rather than resetting the old disposition.

IDs, concept keys, and topics are lowercase slugs of 1–120 characters using
letters, digits, dots, underscores, colons, or hyphens, beginning with a letter
or digit. Text fields are nonempty and at most 4,096 characters; `scope` allows
512 and `source.ref` 1,024. `implication` may be null. `source.as_of` is null,
`YYYY-MM-DD`, or a UTC ISO timestamp ending in `Z`. Recording/update timestamps
use UTC ISO format ending in `Z`. JSON documents and payloads are limited to
2 MiB. Unknown fields, duplicate IDs/JSON keys, and invalid types are rejected.

## Synthetic Update Example

This fixture is invented; the agent must supply actual evidence only in the
external store. The helper path must resolve to the installed skill, and private
payloads must never be saved in this repository.

```json
{
  "entries": [{
    "id": "example-design-options-1",
    "key": "design.option-comparison",
    "topic": "design",
    "statement": "Prefers comparing two options before choosing a direction.",
    "basis": "user_stated",
    "source": {"ref": "synthetic-conversation:example", "as_of": null},
    "scope": "Early visual exploration",
    "implication": "Offer two grounded alternatives when choosing a direction."
  }],
  "questions": [{
    "id": "example-options-reason",
    "topic": "design",
    "question": "What makes comparing options useful to you?",
    "reason": "Choose the right amount of visual exploration.",
    "status": "open"
  }]
}
```

## Corrections, Forgetting, And Freshness

An explicit correction uses a new entry ID and the same concept key. Prior
matching entries become inactive. An interpretation cannot supersede a stated
preference. Imported reports must not displace a newer explicit correction.
Backdated user corrections are rejected: an incoming `recorded_at` must not
precede the active user-stated record for that key. Preserve recording times
when replaying delayed evidence; omit the field only for a new learning now.
Source dates describe the underlying evidence and do not determine correction
order or establish a current confirmation.
Exact-ID retries are no-ops; changing an existing ID is a conflict rather than
a silent overwrite. Review the latest store before preparing a correction.

Send `{"forget_keys": ["design.option-comparison"]}` to erase every version of
that concept from structured memory and retain a key-only suppression marker.
Also inspect question text and reasons; remove any that contain the forgotten
information using `forget_question_ids` in the same update. Those IDs are
suppressed against replay. A generic question that contains none of the forgotten
information can remain. Do not bypass suppression by renaming keys or IDs.
Raw source documents remain
unchanged; be clear about the scope of forgetting. Restoration requires a new
explicit user request and is outside this helper's v1 update interface.

On later invocation, inspect source changes only when their topic matters.
Store concise references and evidence dates, not a second copy of the source.
Ask about time-sensitive constraints when they affect a choice; do not treat
all dated context as current or turn every unknown into a question.

## Failure And Privacy Contract

Updates lock the read/validate/merge/replace sequence and use atomic replacement.
The helper rejects malformed data, unsupported versions, unsafe destinations,
and incompatible updates without replacing existing memory. The memory directory
and files use 0700/0600 permissions. Reads/validation reject unsafe permissions;
authorized updates repair the modes of safely owned regular files, including
otherwise unchanged retries. The exact designated default root may itself be
a separate private Git repository; the helper performs no Git mutations.
Arbitrary repository roots, roots inside a Git ancestor, installed skill
directories, and nested Git stores cannot serve as data destinations; symlink
escapes are rejected. Nothing is stored inside linux-config.

Update/validation results report safe metadata only. On failure, preserve the
store, explain the operation that failed without echoing payloads, and continue
the conversation using available context. Fix a corrupt store only through an
explicit repair request; never silently reset it. No network or other memory
service is part of this helper.
