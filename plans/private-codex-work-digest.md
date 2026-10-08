# Private daily Codex work digest

Implement a private incremental digest of local Codex sessions and an independent daily Toronto timer. Review refreshes changed sessions on demand, without notifications or automatic commitments.

## Context and scope

Canonical instructions, Second Brain session skill and routing, Second Brain CLI/state helpers, Codex parser and isolated runtime govern this work. Existing recap modules and many README/smoke/ledger edits are pre-existing dirty work and must be preserved. Initial git status captured on 2026-10-07 before mutation. No commit, push, worktree, or other timer activation.

## Decisions

Use fresh filtered session parsing rather than unfiltered recap caches. Skip whole sessions on actual personal-context invocation/retrieval; ignore injected policy. Single worker, 20 attempts, 120-second inference deadlines; persistent fair queue. Initial seven-day window, then new/changed sessions and persistent check identities. Private versioned state plus derived Markdown, shared lock, atomic writes. Safe failure metadata only. Existing configured Codex authentication/model with verified ephemeral isolation. Explicit resolve payload requires confirmed disposition.

## Ordered checklist

- [x] Capture initial state and inspect required instructions.
- [x] Inspect parser/state/runtime interfaces; write synthetic RED tests.
- [x] Implement filtering, incremental queue, validated state and isolated inference.
- [x] Integrate CLI/status and independent timer helper with tests.
- [x] Update skill/routing, guide, README and grouped smoke tests.
- [x] Run focused and broader regression checks, review implementation.
- [x] Run refresh-config preserving live snapshot and unrelated edits.
- [x] Enable only digest timer; bounded live refresh, next-trigger/permissions/no-op verification.

## Verification

Focused digest and timer tests; `python3 -m unittest discover -s tests -p 'test_second_brain*.py'`; `python3 -m unittest discover -s tests -p 'test_codex_search*.py'`; syntax/compile and diff whitespace checks. Live timer check, bounded refresh, repeat unchanged refresh with zero model calls, private file permissions. Test privacy exclusions, redaction, malformed input, duplicate IDs, appends, aging, dispositions, fair backlog, auth/quota halt, lock contention and failure preservation.

## Risks and rollback

Summaries are reported conversation evidence, not independent proof. Conservative exclusions and bounds leave explicit coverage gaps. Model consumes allowance. Disable only new timer through dedicated helper; keep private state for review. Existing mutable files require additive edits. refresh-config snapshots live Codex config before chezmoi apply; inspect snapshot behavior first.

## Progress and evidence

Initial default shell failed before executing due to bwrap loopback permissions; approved read succeeded. Incident recorded with reviewed no-new-learning decision. Delegated bounded timer and CLI/docs tasks; root owns privacy/state/inference and verification.

## Review notes

User supplied decision-complete implementation intent; executing in Default mode because mode switching is unavailable. No further design confirmation needed. No commits requested.

Synthetic RED: absent sessions module, absent CLI operation/helper; new-import and missing-source assertions failed before their implementation. Focused sessions suite passes (32 cases at review); timer suite passes (43). Existing command suite passes (34). Review required semantic dialogue hash (lifecycle-only append no call), whole-session malformed-source exclusion, lazy optional dependencies and verified deployed recap helper prerequisites. New/changed old imports after initial scan are processed; absent sources remain explicitly stale.

Ruling: bounded live inspection revealed 4,899 native files / 6 GB, with 614 modified in seven days / 658 MB. Initial full-history privacy parsing took over three minutes before inference. Stop the intentional live probe; revise refresh to discover metadata/fingerprints first, enqueue changed sources, and screen only up to the invocation limit. Persist only safe placeholder metadata and fingerprints before screening; no transcript inputs. Unchanged nonqueued sources use strong size/mtime/ctime/dev/inode fingerprints. Queue remains fair and coverage explicitly pending. This makes the 20 changed-source limit apply to screening as well as inference and bounds live --limit 1 to one source.

## Final evidence and limitations

- Focused: `python3 -m unittest discover -s tests -p 'test_second_brain_sessions*.py'` — 54 passed, exit 0.
- Broad Second Brain: specified discovery command — 305 run, 304 passed; existing exact-tree fixture omits committed July 22 note (exit 1). Neither the note nor fixture was changed.
- Codex search: specified discovery command — 89 passed, exit 0; pre-existing recap work preserved.
- `basedpyright --level error scripts/second_brain/sessions.py scripts/second_brain/session_digest_input.py scripts/second_brain/session_digest_runtime.py` — 0 errors/warnings, exit 0.
- `git diff --check` — exit 0.
- `refresh-config` — completed, exit 0; live and tracked Codex snapshot SHA-256 remained 48fa436c13c18864caa429efbee0689016e29dd516c22c113bacbd50b891cc5f. Concurrent unrelated .gitattributes/README/smoke changes preserved.
- Installed helper --enable and --check — exit 0. New timer active/enabled, next trigger October 7, 2026 at 16:00 EDT. Checkpoint active/enabled and deferred inactive/disabled unchanged.
- First live refresh succeeded (the attempted stop raced with completion); it exposed expensive full-history screening. Final metadata-first --limit 1 live refresh completed in 15.24 seconds with 1 inference attempt; scan and successful summary freshness October 7 at 13:50:07 EDT. Version 1→2 migration preserved old checks. Final counts: 3 open checks, 613 queued sources, 237 excluded, 1 partial, 375 unknown, 1 stale, no refresh error. Counts can overlap (excluded entries queued for migration rescreening).
- `python3 tests/scripts/second_brain_sessions_live_check.py` — one unchanged summarized native source, zero model calls; isolated temporary structured state, unchanged live backlog, no raw copies (exit 0).
- Live private directory 0700; state.json, digest.md, refresh.lock 0600. No source transcript writes, notifications, focus/reminder creation, or Git shipping by this job.

Independent review found and verified fixes for MCP privacy events, malformed/regular-file screening, stable check identities and canonical collisions, Markdown-failure state rollback, deployed runtime dependencies/PATH, bounded discovery, migration and native title safety. Previously screened safe summaries remain explicitly stale while queued changed sources await screening; no new text/title is imported from those sources before screening. Inference remains fallible; the initial backlog is large and coverage intentionally incomplete. Discovery assumes ordinary file metadata reflects native appends; restored timestamps can delay initial selection until a detected change. Interrupted two-file publication retains atomically valid structured state and last Markdown; later refresh regenerates the derived Markdown.

Rollback: `setup-second-brain-sessions-timer --disable`, no sudo; only the new timer is disabled and private state retained. Exact operational commands/manual check are in docs/second-brain.md and docs/smoke-tests.md. Paste-ready continuation prompt is prompts/daily-codex-work-digest.md. Suggested future commit subject: `feat: add private Codex work digests`; no commit or push requested or performed.
