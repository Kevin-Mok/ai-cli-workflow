# Cached Codex conversation search and resume

Build a local terminal command that searches decoded conversation text, shows each session's original directory and resume command, and optionally resumes a selection. Implement synthetic defining tests, add the cached search executable and abbreviation, document use, then verify runtime behavior and timings.

## Purpose and observable outcome

`codex-search [-i] [-F] [--all-text] [--pick] PATTERN` discovers every JSONL source recursively under resolved CODEX_HOME/sessions. Default CODEX_HOME is ~/.codex. Results are grouped once per UUID, newest activity first, with optional title, timestamp, cwd, UUID, snippets and shell-quoted `codex resume -C DIR UUID`. No arguments show usage; maintenance supports --rebuild-index and --clear-cache.

## Context and boundaries

Source: user-supplied implementation prompt. Relevant files: scripts/executable_codex (normal launcher), aliases/key_aliases.tmpl (cs already assigned; csg unused), tests/scripts/executable_codex_test.sh, README.md, docs/smoke-tests.md, .agent/PLANS.md. Title index is enrichment only. All tests use synthetic messages, never real conversation fixtures. No network/model calls in the tool and original sessions remain unchanged. No commit or push requested. No worktree.

## Settled decisions and assumptions

- Python standard library parses JSONL as a stream; rg performs matching on decoded text. Linux flock coordinates atomic cache updates and search snapshots.
- Private cache: ${XDG_CACHE_HOME:-~/.cache}/codex-search/<SHA256 resolved Codex home>, dirs 0700 and files 0600. Per-source conversation and tool files plus a versioned metadata manifest permit incremental stat-based refresh and deleted-source removal.
- Normal text uses public response_item/message user/assistant input_text/output_text, with event_msg user_message/agent_message fallback for legacy/event-only logs. Avoid duplicated mirrored event/response representations. Exclude system/developer, context blocks and reasoning; --all-text adds known tool call/output records, not system instructions.
- Warn about malformed/incomplete data on stderr without printing private payloads. Record missing cwd but never invent it; picker requires an absolute existing directory and valid UUID.
- The installed CLI is 0.160.1; its resume help verifies -C and UUID. fzf is absent. Missing picker dependency is actionable; ordinary search needs only Python 3 and rg.
- Public primary schema: https://github.com/openai/codex/blob/main/codex-rs/protocol/src/protocol.rs (SessionMeta and message events); models.rs (ResponseItem/ContentItem); rollout/src/session_index.rs (id/thread_name/updated_at; append-only latest name wins); rollout/src/recorder.rs (JSONL serialization). Current main may be newer than installed; synthetic tests cover established records and unknown record tolerance.
- Ruling: supplied plan already settles design; execute in Default mode with a living ExecPlan (mode switching is unavailable). Canonical opt-in worktree rule overrides skill workspace advice. Store progress here; no task commits until separately authorized.
- Pre-flight shared interfaces: decoded cache filenames ↔ rg JSON path mapping; manifest source metadata ↔ refresh deletion/version invalidation; picker row UUID ↔ resume argv. Keep these covered by defining tests.

## Protected initial state

Initial git status captured through approved execution before writes. Existing tracked dirties: README.md, aliases/key_aliases.tmpl, aliases/key_dirs.tmpl, docs/phone-ssh-public-ip.md, docs/smoke-tests.md, incident references api-contracts-fixtures/artifact-verification/execution-environments and sources.json, scripts/executable_backup-pc, tasks/lessons.md, txt/exclude-dirs-backup-full.txt, txt/exclude-dirs-backup.txt.tmpl. Existing untracked backup docs/scripts/tests, sandbox reports, other plans and benchmark prompt remain untouched. Use additive patches for shared docs/aliases/ledger and verify initial content survives.

## Implementation checklist

- [x] Capture status, read relevant instructions/preferences/source and inspect installed CLI.
- [x] Finish public schema verification before implementation.
- [x] Write synthetic tests and observe expected RED without implementation.
- [x] Implement streaming extraction, versioned incremental cache, locking, rg results, safe picker resume.
- [x] Add csg while preserving cs; README, operator guide, grouped smoke checks and handoff prompt.
- [x] Run focused tests, existing launcher regression, fresh review and safe refresh-config.
- [x] Measure cold/warm local timings and manually verify printing, picking and real no-prompt resume if permitted.
- [x] Record final evidence, limits and rollback.

## Verification

Automated: `python3 -m unittest discover -s tests -p 'test_codex_search*.py'`; `bash tests/scripts/executable_codex_test.sh`; `git diff --check`. Tests cover conversation-only/default, tool opt-in, rg regex/literal/case, Unicode/escaped/newline text, incomplete title index, directory and UUID grouping, malformed/trailing data, stat refresh/deletion, version rebuild, concurrent cache updates and private permissions. Stub codex/fzf verify exact argv, cancellation, malformed selection, spaces/metacharacters and missing cwd. CLI commands run from unrelated directories.

Manual: no-argument help; synthetic search and picker with stubs; installed abbreviation expansion; local corpus search redirecting private output to private /tmp files and emit only aggregates; compare cold rebuild and warm runs with monotonic timings. Real resume must display history and correct cwd without submitting a new prompt; never infer success from stub tests.

## Risks and rollback

Full first parse of ~5.8 GB takes time and disk; cache contains private decoded text and must stay local. Individual huge records use memory proportional to that record; no full corpus read. Regex is line-oriented as rg defaults. Stat metadata cannot detect intentional content changes that preserve all metadata. Concurrent append may require next-run refresh. fzf and interactive terminal availability limit live picker verification. Refresh-config can adopt unrelated live files or snapshot configs; inspect dry-run and preserve dirty source via scoped application if needed. Rollback: remove only this session's executable, csg and documentation additions, run refresh-config with the same protection; codex-search --clear-cache removes this Codex home's cache only. Sessions never need restoration.

## Progress and evidence

2026-10-06: normal command sandbox cannot initialize loopback; approved scoped commands succeed. Incident docs/postmortem/2026-10-06-codex-search-sandbox-startup.md registered with explicit no-new-learning decision; targeted check exit 0. Public source lookup guesses returned 404; current rollout paths discovered and source lookup incident recorded. No private payload inspection attempted, respecting previous automatic review rejection.

## Review notes

Final independent review completed; review security boundaries, cache consistency after interruption, rg options/environment, duplicated records, missing metadata and picker argument safety. Documentation and plan updates belong with implementation in any future commit. Suggested subject: feat(codex): add cached session search and resume.

RED evidence: `python3 -m unittest discover -s tests -p 'test_codex_search*.py'` exit 1, 15 tests / 24 failures including subtests, all at the explicit missing-implementation assertion. Tests exist before executable; this is intentional RED, not an incident. Message mirrors are deduplicated by role/text digest with event fallback for unique event messages, preserving event-only data.

GREEN evidence: defining suite exit 0, 15 tests in 3.423s. Existing launcher regression `bash tests/scripts/executable_codex_test.sh` exit 0. Public rollout wire format also verified from history/src/rollout_payload.rs before implementation (type + payload, response metadata outside payload). Additive edits preserve pre-existing README/alias/smoke content. Fresh reviewer /root/review_codex_search is auditing the implementation read-only.

Final review fixes: malformed response/event discriminants and isolated Unicode surrogates independently reproduced (each focused regression exit 1 with the expected TypeError/UnicodeEncodeError). Narrow per-record type validation and Unicode skip handling preserve valid neighboring data; full-suite verification follows.

Final: Ruling: regrade raw control-character resume paths and noisy pipe cancellation as Important because they break safe terminal output and normal pipe usage. Reject non-printable cwd for resume and put BrokenPipeError handling before OSError; explicit final flush prevents delayed interpreter errors. Both focused tests observed RED, then full-suite GREEN below. No deferred minor code findings; live picker/resume require runtime verification, not review inference.

Additional synthetic coverage: picker forged output/default binds, IDE context prefix and JSON tool arguments. A defining fixture initially encoded a Windows path as JSON \t; changed fixture construction to json.dumps while keeping the literal-path assertion unchanged. This is a fixture correction, not changed matching behavior.

Live validation found a new picker display defect after reviewer scope ended: capture_output hid fzf stderr/UI. Cancellation still exited 0 and launched nothing. A defining stderr-display regression observed RED (missing Synthetic picker UI); stdout-only capture with inherited stderr is the minimal correction. Repeat real picker checks after GREEN; do not infer presentation from selection stubs.

Final runtime evidence: real fzf 0.44.1 extracted from Ubuntu package under /tmp displayed matching synthetic rows. Escape returned 0/no launch; Enter yielded exact resume argv. Real Codex 0.160.1 displayed saved user/assistant synthetic history; /status confirmed UUID 00000000-0000-4000-8000-000000000001, original temporary project directory with spaces, title and 0 input/output tokens. Only /status was entered; no new inference prompt. Corrected fixture exited 0. Actual Codex lifecycle writes are distinct from search immutability (verified before launch). The fzf binary is not on normal PATH; --pick needs optional installation there. Reusable fixture: tests/scripts/codex_search_live_check.py [--fzf PATH] [--real-resume].

Refresh evidence: snapshot dry-run exit 0; live/source Codex and Git configs byte-identical. Task-scoped fish wrapper ran the actual refresh-config function and restricted only its broad apply to ~/scripts/codex-search and ~/aliases/key_aliases because chezmoi status included unrelated removal/install-claude-skills.sh and concurrent source changes. REFRESH COMPLETE, exit 0; all 38 captured protected/source hashes unchanged; installed script bytes matched at that point. csg expands to codex-search, cs retains printf terminal clear.

Ruling: scoped refresh preserves unrelated removal and work-in-progress targets while retaining normal snapshot, exact config apply and shortcut generation. It costs delayed activation of unrelated changes, which is outside this task. No Git integration menu is needed: supplied intent explicitly separates commit authorization; leave implementation uncommitted.

Final separate benchmark: 4744 local JSONL sources; cold indexing alone (`python3 scripts/executable_codex-search --rebuild-index`) 61.687s, exit 0. Warm matching (`python3 scripts/executable_codex-search -F refresh-config`, private stdout suppressed) 1.024s, exit 0. The earlier 62.258s measurement included both rebuild and search; do not conflate it with indexing alone. Cache permission inventory confirmed owner-only modes; private output remains outside Git.

Final learning records: all five task incident reports reviewed. Sandbox/source lookup reports have explicit no-new-learning decisions; malformed-record and picker-UI reports link verified code/runtime findings local-codex-search-json-boundary and local-fzf-ui-stream-and-resume-fixture in tracked api-contracts-fixtures.md/sources.json. Targeted checks pass for current hashes. Repo-specific corrections appended to tasks/lessons.md, preserving older entries and concurrent work.

Delivery scope: scripts/executable_codex-search; tests/test_codex_search.py; tests/scripts/codex_search_live_check.py; additive csg alias, README and smoke checks; docs/codex-session-search.md; prompts/search-codex-sessions.md; this plan; five named codex-search incident reports; corresponding incident-guidance/ledger/lessons additions. All other initial and concurrently appearing files remain out of this task. No tracked private conversations, caches or package binaries. No staged files, commit or push.

Remaining limits: unsupported legacy, archived/compressed and shared-prefix lineage formats remain outside sessions/**/*.jsonl scope. Matching is line-oriented with five display snippets. Cache stat metadata can miss intentional metadata-preserving edits. Default shell sandbox remains broken; approved scoped execution is a verified workaround. No automatic approval rejection occurred in this implementation; prior private inspection rejection was respected through public schema research and synthetic fixtures.

Rollback and reproducibility: follow docs/codex-session-search.md#verification-and-rollback and its exact focused checks/live fixture; handoff prompt under prompts/search-codex-sessions.md. Reject non-printable resume cwd rather than emitting terminal controls; cost is refusing rare control-character directory names. Worktree avoidance/current-workspace execution costs no task isolation but follows canonical user policy. Scoped refresh delays activation of unrelated work. Final fresh suite/launcher/README/diff/installed-source checks recorded below.

Final preservation audit: an intermediate refresh returned REFRESH COMPLETE, but a hash comparison found four outside-scope shared incident/lesson paths changed during the interval. Attribution remains unconfirmed; no rollback performed. Verified installed bytes/session learning survived, consulted local-stale-preservation-baseline, then repeated against fresh byte snapshots: all 44 source files unchanged, exit 0/REFRESH COMPLETE, log /tmp/refresh-config-20261006-130510-167971.log. See docs/postmortem/2026-10-06-codex-search-refresh-audit.md; reviewed no-new-learning decision registered. Subsequent intentional changes are plan/incident documentation only, and are not silently compared with stale hashes.

Final evidence: `python3 -m unittest discover -s tests -p 'test_codex_search*.py'` 22 tests, 4.799s, exit 0; `bash tests/scripts/executable_codex_test.sh` exit 0; README gate pass_no_change, exit 0; git diff --check exit 0. Final corpus cache: 4,744 valid UUID sources, 145 malformed/incomplete records skipped with stderr warnings, 3,037,830,775 cache bytes (~2.83 GiB), all inspected cache file modes 0600 and directory mode 0700. At benchmark completion, sources totaled 5,846,486,471 bytes and continued normal session logging; no corpus payloads were printed or committed.

Outcome achieved: installed terminal search, automatic private incremental cache, safe optional picker resume, unchanged cs/csg expansion, synthetic RED/GREEN suite, real no-prompt resume, docs and rollback. Implementation is left uncommitted as requested; exact test commands, manual checks, atomic scope, Cursor prompt and suggested Conventional Commit are available in linked artifacts. No unresolved implementation review findings; limitations above are deliberate scope boundaries.

## Follow-up: activate the picker dependency

2026-10-06: user pasted working search results followed by the designed missing-fzf message. Interpret this as a request to make --pick usable on the current desktop. Captured current git status before doc changes; preserve all existing implementation and unrelated backup/incident edits. No search behavior change or system package installation required.

- [x] Confirm fzf absent and ~/.local/bin already on PATH.
- [x] Verify Ubuntu fzf_0.44.1-1ubuntu0.3_amd64.deb SHA-256 against apt package metadata: 345ab0b82c0a2dfc364d1da4404b61c438413fc6881daf8acecd9e3821578258.
- [x] Extract only the regular usr/bin/fzf member, install atomically to ~/.local/bin/fzf mode 0755 without sudo or overwriting an existing binary.
- [x] `fzf --version`: 0.44.1 (debian), exit 0. Fish resolves the same executable/version.
- [x] Real fzf smoke fixture on the normal PATH displayed the row; Enter passed exact resume/-C/synthetic-directory/UUID arguments to the stub, exit 0. No private history or prompt submitted.
- [x] Focused defining suite with fzf installed: 22 tests, 4.620s, exit 0; unavailable-dependency behavior still tested using an isolated PATH.
- [x] Update operator guide with the actual no-sudo local dependency installation and retry instruction.
- [x] Run scoped refresh-config: REFRESH COMPLETE, exit 0. All captured source hashes except the live Codex snapshot matched; source/live configs matched in the first inspection, and subsequent live CLI settings changed again; preserve both current states. Installed search bytes match; README gate pass_no_change and diff check exit 0.

The prior absent-fzf limitation is resolved for this desktop only. No new postmortem is needed: missing-fzf was an explicitly specified, deliberately tested failure path, and installation/verification commands succeeded. Package binaries remain outside Git. Rollback for this dependency is removing only ~/.local/bin/fzf; search still works and --pick returns its expected missing-dependency message. Keep earlier script/docs/ExecPlan commit scope intact if Git delivery is later authorized.

Follow-up refresh audit: preserved the live-originated Codex config snapshot, which is unrelated to the fzf installation and must remain outside any session-search commit. A HEAD-based diagnostic was invalid for preservation attribution; retained byte snapshots were checked against the immediate baseline instead. See updated refresh-audit incident and targeted learning check.

Final fzf follow-up boundary: retained byte baseline proves the refresh source changes were model/model_reasoning_effort only. Later live CLI settings continued changing independently; preserve those current states and stop unrelated config investigation. The dependency and normal-PATH picker are verified; no further package/config changes required.

## Follow-up: smoke documentation and help

2026-10-06: user requested smoke-test documentation and a help flag. Existing
argparse -h/--help support is retained; improve its option descriptions,
readable examples, maintenance usage and guide/checklist paths. Rewrite only
the session-search smoke section as exact one-line command Actions, following
the canonical feedback preferences. Preserve unrelated shared-document work.

- [x] Capture status and read current help, smoke checks and applicable preferences.
- [x] Defining test first: -h and --help must explain matching flags, show a picker
  example and smoke-doc path, and work on an isolated PATH without indexing or
  launching Codex. Expected RED: 1 test, 2 subtest failures at missing ignore-case
  description, exit 1.
- [x] Improve help text and align README/operator-guide/smoke documentation.
- [x] Run focused suite, launcher regression, README gate and diff review.
- [x] Refresh the installed command with protected refresh-config; verify live help.

No search/cache/picker behavior changes, new dependencies, commit or push.
Rollback for this follow-up is restoring the earlier parser help copy and these
documentation additions, then running the same scoped refresh.

GREEN: focused help contract 1 test in 0.097s, exit 0; full defining suite
23 tests in 4.805s, exit 0; launcher regression exit 0; README gate
pass_no_change, exit 0. Source help manually inspected: separate examples,
matching-option descriptions, maintenance usage and guide/smoke paths.
The reusable live fixture's arguments and behavior match the new smoke entries.

Runtime: actual scoped refresh-config returned 0/REFRESH COMPLETE; installed
search bytes match source and installed --help displays the new content. The
46-file preservation guard observed unrelated tests/test_backup_pc.py drift
and exited 1; preserve it, do not repeat deployment for equality. Audit report
updated, reviewed hash/explicit no-new-learning decision recorded in tracked
postmortem memory; local-stale-preservation-baseline applies. No private sessions
were opened and the expensive corpus rebuild/clear checks were not repeated.

Final follow-up checks: installed --help and -h from /tmp exit 0 with expected
descriptions/doc path; installed/source byte identity confirmed. All 10 smoke
Actions are single-line commands without backticks. Targeted incident-learning
check reports no errors/current hash coverage, exit 0; final README gate
pass_no_change and git diff --check exit 0. Follow-up complete, uncommitted.

## Session-only Git delivery

2026-10-06: user invoked commit-session, authorizing a scoped commit and upstream
push. Branch main tracks origin/main. Session ID
01a11213-5551-74a0-af33-7be3e2a34b5a; the required helper returned unsafe because
it detected no successful repo-writing actions through the tool wrapper
(first_write_at/baseline_at null, empty candidate set). Use successful writes
observed in this conversation and the captured pre-write dirty state as the
skill's direct-write fallback; do not infer ownership from timestamps.

Eligible: complete search executable, both synthetic test helpers, guide,
handoff prompt, this plan and five named codex-search incident reports; only
search hunks in README, aliases, smoke tests, lessons, API guidance and the
corresponding five report/two finding records in sources.json. Leave backup,
phone SSH, feedback, other plans/prompts/incidents, live-originated config
snapshots and unrelated guidance/ledger records untouched and uncommitted.
Review and test the separated staged content before committing. Suggested
subject remains feat(codex): add cached session search and resume.

Fresh delivery verification: worktree defining suite 23 tests in 5.141s,
launcher regression and README gate exit 0. A private /tmp candidate built from
HEAD plus only observed session additions also passed the exact defining suite
(23 tests, 4.752s), launcher regression, README gate pass_no_change and all five
targeted postmortem-learning checks (no errors, exit 0). Reviewed all six
mixed-file candidate diffs: no backup/SSH/other-learning additions included.
Delivery scope totals 17 files; preserve the complete working copies while
staging only the reviewed candidate blobs for mixed files. Existing refresh
evidence and installed/source identity remain valid; no code changes followed
these fresh checks.

Staging-boundary correction: broad worktree equality guard stopped before index
writes because the shared sources.json changed during review. All five search
report records and both findings still exactly matched the reviewed candidate;
the index was empty. Preserve unrelated updates and compare only owned records,
then stage candidate blobs. Recorded this in the existing refresh-audit report
and updated its reviewed hash/explicit no-new-learning decision. Applicable
lookup: shared ledger changed staging baseline; matching
local-stale-preservation-baseline/local-deployable-file-set-verification guidance.
