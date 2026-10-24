# Native-session Failure Candidates

This report supplies aggregate evidence for the later CASD-style instruction
pass. It screens native logs in place, separates complaint candidates from tool
failure candidates, and maps observations to preventive rules to retain. It does
not establish root causes or change AGENTS policy.

## Window And Coverage

The fixed window is **2026-08-24 01:00 UTC through 2026-10-23 01:00 UTC**
(60 days). The reviewed aggregate snapshot is [failure-counts.json](failure-counts.json).

| Coverage | Count |
| --- | ---: |
| Native JSONL files inventoried | 6,796 |
| Files older than the window by modification time | 4,157 |
| Candidate files screened | 2,639 |
| Eligible distinct sessions | 416 |
| Records inspected in those retained session files | 193,797 |
| Eligible user messages after filtering | 1,413 |
| Policy, quote, code or long-blob user messages filtered | 884 |
| Outside-window or undated user messages in retained files | 1 |
| Event/response user-message mirrors removed | 0 |

| Entire-file exclusions | Count |
| --- | ---: |
| Helper/subagent origin | 2,184 |
| Private-context use or invocation | 15 |
| Record larger than the 2 MiB screening bound | 22 |
| Duplicate native session identity | 2 |

No incomplete, changed-during-read, unsafe, invalid-metadata or over-64-MiB file
reached the retained sample in this run. These exclusions are tested with
synthetic files; their absence here is not a claim that such files never occur.
Eligible sessions are only 15.8% of candidate files, predominantly because
helper sessions are excluded. Do not generalize this sample to every interaction.

## Complaint Candidates And Rules To Retain

The seven conservative regex classes were declared before the first native
scan. **Frequent** means at least 3 eligible sessions across at least 2 UTC
dates. One message can match multiple classes. None met that threshold.

The examples below are carefully generalized pattern paraphrases, not quotes
or individually adjudicated incidents. No transcript excerpts, source filenames,
identities, projects, private paths or native session IDs are published.

| Candidate class | Messages | Sessions | Dates | Generalized example | Current preventive rule |
| --- | ---: | ---: | ---: | --- | --- |
| Copy/paste issue | 3 | 2 | 2 | A provided command cannot be copied or pasted successfully. | Retain standalone runnable commands, fish syntax, and actual wrapped-copy verification in **Bugs, Tests, And Implementation**. |
| Unsupported completion | 2 | 2 | 2 | A reported fix still fails when used. | Retain fresh evidence before completion claims and disclose unverified activation in **Verification And Completion**. |
| Excessive verbosity or cost | 1 | 1 | 1 | The response or execution consumes too much time or text. | Retain the simplest correct implementation and task-proportionate checks; use concise progress and handoffs. |
| Repeated approval request | 0 | 0 | 0 | No eligible match; the class targets renewed approval questions for authorized work. | Preserve current user authorization and **Scope, Safety, And Clarity** safeguards; zero matches do not justify adding or deleting a rule. |
| Incomplete scope | 0 | 0 | 0 | No eligible match; the class targets omitted required work. | Retain decision-complete scope, plan checkboxes, and requirement verification in **Planning And Coordination** and **Verification And Completion**. |
| Overwritten work | 0 | 0 | 0 | No eligible match; the class targets lost or reverted user edits. | Retain preservation of pre-existing work, selective staging, and destructive-action safeguards as safety rules regardless of frequency. |
| Stale context | 0 | 0 | 0 | No eligible match; the class targets continued use of an obsolete request. | Retain current-request reconciliation and source/plan inspection; assess long conditional procedures separately. |

The policy locations above refer to the current
[canonical AGENTS document](../../dot_codex/AGENTS.md). This is a retention map,
not a claim that every mapped rule was causally validated by the matcher.

## Tool Failure Candidates — Separate Signal

There were **1,767 failed-completion candidates across 328 eligible sessions**.
Status comes from explicit nonzero exit/error fields, nested returned JSON, or
recognized exit-status text. Each candidate receives one fixed generic category
(first match wins); the table exposes no raw error payloads.

| Generic category | Completion candidates | Sessions | Dates |
| --- | ---: | ---: | ---: |
| Missing resource | 353 | 169 | 25 |
| Permission or read-only boundary | 262 | 218 | 28 |
| Validation or assertion | 427 | 134 | 24 |
| Timeout | 134 | 70 | 17 |
| Network | 6 | 3 | 3 |
| Other or unclassified | 585 | 217 | 29 |

These are **not 1,767 unexpected failures**. They can include intentional TDD
RED, negative tests, expected probes, returned fixture data, and mirrored
event/response tool completions. Tool completions are not mirror-deduplicated.
The classifier does not adjudicate those cases or prove a recurring root cause.

Retain source/path inspection, permission and unrelated-work boundaries,
defining tests, fresh verification, and honest reporting of failed or skipped
checks. Timeout/network candidates also support retaining ongoing progress for
long operations. Existing controls cover these generic classes; the counts alone
do not justify another standing rule or an incident report for every candidate.

## Method And Limits

- Enumerate native JSONL files read-only; modification time selects candidate
  files. User/tool observations must also have record timestamps inside the UTC
  window. Files restored with misleading old modification times can be missed.
- Reuse the anchored native `source_reader`, helper-origin detection,
  private-tool checks, private-use patterns, conversation filtering and tool
  string decoder. Do not invoke the digest parser or create its caches/indexes.
- Exclude the entire file on helper/private evidence, an incomplete/malformed
  record, excessive file/line size, missing/conflicting session identity, unsafe
  source, or a file signature change/replacement while reading. All local
  observations remain provisional until the file passes screening.
- Reject injected AGENTS/environment/goal context and long instruction blobs;
  strip fenced/inline code and quoted lines before matching complaint text.
  Count repeated user messages while removing mirrored event/response copies
  by in-memory text hashes and representation counts. Native identifiers and
  hashes remain memory-only; duplicate session files contribute once.
- Read and screen the full bounded source, including out-of-window records for
  privacy. The record-inspection coverage count includes those records. Live
  logs can append after a file is checked; this is a per-file stable read, not
  an immutable snapshot of the complete archive. Repeated scans can differ.
- Precision and recall are **not measured**. Requests for future behavior may
  resemble complaints; different wording, multilingual corrections, images,
  long messages and excluded sessions may hide real failures. Regex matches
  are candidates, not proven root causes, instruction violations or incidents.
  Sparse or zero counts are not evidence that a safeguard is unnecessary.
- Publish only aggregate counts and generalized paraphrases. No raw session
  data is copied, indexed, exported, sent to a model or retained in artifacts.

## CASD Decision Input

Keep all safety rules regardless of counts. Retain completion-evidence and
command-usability controls for the observed complaint classes. No complaint
class meets the predeclared frequency threshold, and the generic tool classes
are already covered, so this evidence warrants **no new AGENTS rule**.

In the separate policy pass, review unsupported conditional procedures for
on-demand relocation rather than treating no regex match as permission to
delete safeguards. Preserve required behavior, record each policy decision and
measure the net token change, including any new router text.

## Reproduce And Verify

From the repository root, without sudo, run the read-only scanner. It prints
aggregate JSON to stdout and activity/elapsed time to stderr at least every
10 seconds during the scan. `--plain` makes progress ASCII-only. Native logs
may change, so identical window bounds do not promise identical counts.

python3 benchmarks/trim/mine-failures.py --now 2026-10-23T01:00:00Z

Synthetic verification: `python3 -m pytest tests/test_trim_failure_mining.py -q`
passed **8 tests**, exit 0. Observed RED covered the absent scanner, quote/fence
filtering, nested JSON exit status and per-category session/date aggregation.
Tests also cover late privacy markers, helpers, mirrors and real repeats,
incomplete/replaced files, size/symlink boundaries and aggregate-only exports.
The native scan completed in 12 seconds, exit 0, with a periodic progress update.
No AGENTS rule was added, removed or moved in this measurement step.
