# Codex recent-session browser implementation plan

Build the supplied recent-session browser on the existing local index, prove the async recap and resume boundaries with synthetic fixtures, then update operator documentation and run the protected configuration refresh. The original specification was the user-supplied local `prompts/codex-recent-sessions.md`; that pre-existing untracked prompt is outside this session commit. The requirements and verification below make this delivery self-contained.

## Purpose and observable outcome

From any directory, `codex-search --recent` prints the newest 20 conversations and cached recaps without inference. `codex-search --recent --pick` and fish `crg` open all discovered conversations, show live recap previews, and resume an exact UUID in its recorded directory without adding a prompt. Ordinary search/help remain compatible.

## Context and boundaries

Existing source is `scripts/executable_codex-search` (index, parser, presentation, fzf). Existing contracts: `tests/test_codex_search.py`, `docs/codex-session-search.md`, `plans/codex-session-search.md`. Source discovery remains `CODEX_HOME/sessions/**/*.jsonl`; title index is optional. No cloud/archive expansion, model-service dependency or source-session write. Implementation initially ended uncommitted; the subsequent `$commit-session` request authorizes scoped delivery, and the user explicitly requested a new worktree.

Split reusable indexing into `scripts/codex_search_index.py`, recap cache/generation into `scripts/codex_search_recaps.py`, and the recent picker into `scripts/codex_search_recent.py`; leave ordinary rendering and main entrypoint in the executable. Python standard library, installed rg/fzf/Codex remain the stack.

## Assumptions and settled decisions

- The supplied detailed prompt authorizes implementation and verification; no repeated design approval is needed. This runtime is Default mode with no mode-switch tool, so this ExecPlan supplies the required planning record.
- Retain current deduplication by latest recorded activity; compare timestamps as instants. Cache mtime never orders sessions.
- Cache version 2 adds canonical role-labelled dialogue JSONL and its SHA-256, sharing the existing exclusion parser. Normalized dialogue ignores source metadata and tools; identical dialogue keeps a recap valid.
- Recap identity includes UUID, dialogue hash, resolved model and format version. Private atomic writes and separate per-session flock prevent duplicate concurrent inference; never hold the index lock during inference. Maintenance must preserve active lock inode identity.
- Model calls occur only inside recent picker, with default newest 20 eligible sessions, one worker, one attempt per UUID per opening, 120 seconds maximum. `--summary-count 0` disables automatic work, Ctrl-G stays available; `--no-summaries` disables every model call. Listing reads cached data only.
- Use installed supported CLI isolation controls and verify effective config before inference. Never infer isolation from an empty deep-merged MCP map. Preserve login and configured model; temporary runs are ephemeral and do not resume source UUIDs.
- Dialogue input is bounded to 32768 UTF-8 bytes, preserving first request/latest dialogue; omissions mark partial. Structured fields headline/goal/progress/state/next_steps total at most 150 words and cannot claim unreported completion.
- Picker rows/preview are terminal-sanitized. Exact UUID selection and validated recorded cwd produce `codex resume -C DIR UUID`; worker and descendants are stopped/reaped first.

## Ordered implementation checklist

- [x] Read supplied prompt, canonical guidance, relevant feedback/lessons, existing source/tests/docs/plan; capture initial dirty status.
- [x] Assign independent read-only isolation/fzf investigations and bounded index work, as canonical instructions request parallel agents for independent tasks.
- [x] Add synthetic defining tests and observe RED for recent CLI/index, recap validation/cache/worker and picker behavior.
- [x] Implement index module and CLI recent mode without changing ordinary search/help.
- [x] Implement bounded dialogue/validated recaps, independent atomic cache and cancellation-safe isolated worker.
- [x] Implement immediate fzf open, live preview, Ctrl-G and selection preservation; add unused `crg`.
- [x] Run all specified automated checks and real fzf with deterministic synthetic recap subprocess; verify cancellation/resume and unchanged sources.
- [x] Independent review, resolve findings with defining tests, and rerun relevant checks.
- [x] Update operator guide, README, grouped smoke checks and this plan; protect unrelated dirty files and run actual scoped refresh-config.
- [x] Verify installed command/abbreviation, record exact evidence, usage, limitations and rollback; finish the initial implementation uncommitted.

## Test and interface contracts

Index exports existing SearchError/visible/security/cache/refresh/search/titles functions plus `recent_entries(entries)`. Entries retain existing fields and add `dialogue` and `dialogue_hash`. Recap module consumes an entry and private root, exposes cache identity/status/read and bounded generation management; recent picker owns display snapshots and callbacks. Lock/cache maintenance interfaces are finalized before integration and recorded here.

RED cases cover activity ordering across dirs with duplicate UUIDs; default 20 and limit 0; no pattern/help/ordinary search; tool/instruction exclusion and normalized hash; 32 KiB UTF-8 bound; model/version invalidation; 150-word schema and malformed output; automatic cap/order/one worker; disabled generation; timeout/cancel/process reaping; auth/rate-limit stop; source immutability; forged picker selections and exact argv.

Exact regressions:

```bash
python3 -m unittest discover -s tests -p 'test_codex_search*.py'
bash tests/scripts/executable_codex_test.sh
git diff --check
```

Real-fzf fixture will use only synthetic sessions and a deterministic local recap executable. Verify original query/highlight after generation, Ctrl-G for an older session, Enter exact argv, Esc/Ctrl-C no resume and no remaining worker. At most one real model smoke request, containing only synthetic dialogue; no real private session sent by validation.

## Risks, protected state and rollback

Initial status and shared-file byte copies are private in `/tmp/codex-recent-initial`. README, aliases, smoke tests, lessons, postmortem ledger/topic guidance and backup/SSH work were already dirty. Preserve those edits; add only attributable hunks. Pre-existing untracked prompt is the user-supplied specification, not newly authored here.

Fail closed if isolation cannot be verified; keep local browsing usable with clear unavailable status. Avoid global environment changes and broad chezmoi application. Compare live/tracked Codex/Git config ownership and snapshot dry-run before actual refresh; restrict unrelated deployment targets using the established protected wrapper. Re-snapshot immediately before preservation verification, avoiding stale baselines amid parallel edits.

Rollback: remove only this task's added modules/tests/`crg` and restore this task's executable/doc hunks, preserving prior edits; clear this Codex home's cache and use the protected refresh to reinstall the prior command. Session sources stay unchanged. Plan updates travel with related changes in any later authorized commit.

## Progress, evidence and review notes

2026-10-07: Initial shell reads failed before startup with known bwrap loopback RTM_NEWADDR error. Approved scoped execution unblocks reads/writes; incident `docs/postmortem/2026-10-07-codex-recent-implementation-sandbox.md` registered with reviewed no-new-learning decision; targeted check exit 0. Default sandbox remains unresolved.

Initial inspection: existing fzf 0.44.1, index v1, no `crg` alias. Installed Codex supports ephemeral/rules/config controls; effective isolation investigation in progress. `mcp_servers={}` alone does not clear inherited servers.

## Handoff

Atomic delivery includes implementation/modules, synthetic tests/live fixture, alias addition, README/operator guide/smoke changes, this plan and related incident-learning records. Paste-ready Cursor prompt: `Review plans/codex-recent-sessions.md and docs/codex-session-search.md in the feature worktree; preserve unrelated source-workspace changes. Verify only outstanding delivery items with the listed synthetic checks. The single allowed live model request and protected refresh-config are already complete; do not repeat live inference. Keep implementation, tests, docs and plan together in the authorized session commit.` Suggested subject: `feat(codex): browse recent sessions with cached AI recaps`.


2026-10-07 implementation evidence: initial recent CLI tests failed with unrecognized `--recent`; index/recap/runtime/picker defining tests failed for missing implementation before code. Index now exports cache v2 normalized chronological dialogue and activity sorting. Root integration retains all 29 original search tests. Recap cache uses `recaps/inventory.json` plus epoch invalidation, stable per-UUID locks and short maintenance flock. The index lock is acquired by a separate actual CLI fixture while a deterministic inference is still running, proving inference is outside it.

Picker decision: verified fzf 0.44.1 tracks input indexes across reload, so freeze UUID order and use --no-sort/--track with fuzzy search restricted to immutable activity/directory/title fields. Authenticated loopback reload-sync updates recaps/preview without restarting fzf or resetting query/selection. Real PTY fixture verifies Enter, Esc, Ctrl-C and SIGTERM, Ctrl-G outside the automatic window, and reaped workers.

Independent review found/fixed disappearing cache reads, stuck competing-generation state, abandoned atomic tmp files and cancellation during runtime construction. Each defining reproducer observed RED, then passed after correction. Latest focused runs: 18 recap tests, eight recent CLI tests and seven picker tests GREEN. Full integration previously passed75 tests before these added cases; final full run pending.

Runtime proof: installed Codex0.160.1 app-server effective settings/hooks/MCP checks and exact final cwd pass, retaining configured login/model. Intercepted synthetic localhost provider catalog shows no shell/web/MCP capabilities, and Code Mode host is disabled/fails closed. No upstream inference in those diagnostic probes. Runtime standard tests16 GREEN. One optional real synthetic request is running; no real session dialogue is sent.

Type validation: cached Pyright entrypoint initially missed its typeshed and emitted irrelevant stdlib errors. Explicit bundled --typeshedpath exposed14 optional-value narrowing issues; explicit verified-value guards corrected them. Fresh Pyright result: zero errors/warnings. No extra type-checker dependency installed.

Protected refresh preflight: snapshot-codex-config --dry-run passes; tracked Codex/Git source files are clean. Git source/live match; live Codex model/model_reasoning_effort differ from clean tracked source. Required refresh is authorized to snapshot this current live configuration; preserve that snapshot rather than restore stale source. Broad chezmoi status includes unrelated pending removal, so exact task targets will be used with the established scoped wrapper.

Diagnostic incident: an agent's deliberately failing runtime assertion printed inherited environment containing SUPABASE_DB_URL and CTT_BOT_TOKEN in tool output. Tests now use only synthetic environment dictionaries and boolean membership assertions; no credential values in repository or diagnostic logs, no external request carried the environment dump. User informed; credential rotation remains outside this implementation. See runtime-probe incident and tracked reviewed learning.


## Final verification and delivery

- `python3 -m unittest discover -s tests -p 'test_codex_search*.py'`:89 tests,16.137s, exit0. Includes existing29 ordinary-search cases, real fzf, providers/errors/cache/timeout/disabled-generation/concurrency, synthetic source immutability and exact resume arguments.
- `bash tests/scripts/executable_codex_test.sh`:exit0. `git diff --check`:exit0. README recruiter-sync:pass_no_change, exit0.
- Cached Pyright with its explicit bundled typeshed checked the executable and all four modules:0 errors,0 warnings, exit0.
- `python3 tests/scripts/codex_recap_isolation_check.py`:exit0; actual Codex0.160.1 accepted verified isolation, one intentionally rejected localhost synthetic request, zero upstream requests, configured MCP canary never started. Catalog only generic disabled-host Code Mode wrappers, no usable shell/web/MCP capability.
- `python3 tests/scripts/codex_recap_live_check.py --live`:exactly one real synthetic request, ready, configured model resolved to gpt-6.1-sol at execution. Recap correctly says a proposal was reported but implementation/tests were not run. Source bytes unchanged; zero new browsable session files. Earlier model discovery saw gpt-6-astra; this reflects current live settings changing, not a hardcoded model choice. No further live requests.
- Actual protected `refresh-config`:exit0/REFRESH COMPLETE, log `/tmp/refresh-config-20261007-123450-3015792.log`. All70 captured source hashes preserved except the explicitly required live Codex snapshot; captured live bytes match the resulting source. Git config preserved. All five installed executable/module files match source.
- Generated Fish effective abbreviations verified:crg=`codex-search --recent --pick`, csg=`codex-search`, cs retains terminal clear. Installed recent command run from `/` with synthetic CODEX_HOME returned0, correct UUID/directory/missing-recap label and unchanged source.
- Initial implementation ended with no staged files, commits, pushes or worktrees. Existing backup/SSH/alias/README/smoke/incident work was preserved. The subsequent authorized delivery is tracked below.

Remaining limits:local sessions scope only; no cloud/archive expansion. Recap text is excluded from fuzzy filtering to preserve highlighted UUID during updates. Discovery order is frozen per opening. Long dialogue recaps are labelled partial. Unsupported CLI isolation/managed requirements/MCP-name syntax disables generation while local browsing works. Default command sandbox remains broken; approved scoped execution was used. Diagnostic credential exposure is recorded above and in the runtime incident; rotation remains the user's follow-up.

Rollback and exact usage are in docs/codex-session-search.md. Atomic scope and paste-ready Cursor continuation prompt remain in Handoff above. No remaining implementation/review items; final post-documentation diff and learning checks follow without another model request.

Final post-learning refresh also returned REFRESH COMPLETE with five installed files byte-identical and a fresh preservation audit passing for72 sources, with no source changes. Evidence `/tmp/codex-recent-final-refresh-output.txt`. All six current task postmortem targeted checks pass; final git diff --check passes and index is empty.

## Authorized session delivery

- [x] User requested `$commit-session`, then explicitly requested a new worktree. Created `.worktrees/codex-recent-sessions` on `feat/codex-recent-sessions` from `b666222`; clean baseline and 29 original search tests pass.
- [x] Scope helper reported unsafe: "No successful repo-writing actions were detected in the current Codex session." Session `01a11717-f9ed-72d3-9980-4954032b0b2b` therefore uses direct-write evidence and `/tmp/codex-recent-initial` baseline snapshots. Transferred whole owned implementation/tests/docs/reports and only session hunks in README, aliases, smoke checks, lessons and learning records. Excluded the pre-existing prompt, backup, phone SSH, notification and unrelated learning changes. Original workspace remains untouched.
- [x] Fresh worktree verification: 89 tests pass in 18.740s; shell regression exits 0; Pyright reports zero errors/warnings; real-fzf query/selection/Ctrl-G/cancellation/cleanup check passes; actual-CLI isolation fixture makes one rejected local request and zero upstream requests, with its MCP canary never started. README gate returns pass_no_change; all six report checks against candidate knowledge pass; whitespace and scoped diff review pass.
- [x] Prepare the verified atomic commit, keeping matching plan/docs/learning records together. Delivery target is `origin/feat/codex-recent-sessions` in user@example.invalid:example-user/ai-cli-dotfiles.git`; Git history and upstream tracking record the ensuing commit/push result. Original workspace dirty changes remain in place.

The implementation bytes match the final installed/refresh-verified source snapshot. Moving those same bytes into this worktree adds no new configuration behavior and requires no repeat global refresh. No further live model request is authorized by the original validation limit.

### Delivery result

Implementation committed as `ce90d62` (`feat(codex): browse recent sessions with cached AI recaps`). The sole normal push to origin was rejected by GitHub with Internal Server Error; no upstream is configured. Local commits are preserved and publication remains unresolved. A separate documentation commit records the push incident and reviewed learning without rewriting the implementation commit. The original main workspace and its dirty work are preserved. See `docs/postmortem/2026-10-07-codex-recent-branch-push.md`.
