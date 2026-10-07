# Automatic private personal and project context

Enable relevant personal learning and source-backed project knowledge while returning compact briefs. Implement portable code and synthetic tests here, build the actual foundation only under the external private root, then verify installation and routing.

## Outcome and scope

Extend the existing v1 personal store without schema changes. Add project-knowledge.json and rebuildable cache/topic-briefs.json inside external ai-context. Preserve Markdown, project sources, other memory systems, existing commands, and unrelated dirty work. Implementation was initially uncommitted; the subsequent $commit-session request authorizes scoped commits and upstream pushes in linux-config and personal-context.

## Context and settled decisions

Sources: dot_codex/AGENTS.md, personal-context skill/helper/storage reference, existing personal-context and Second Brain tests, feedback.log and tasks/lessons.md. User supplied plan supersedes explicit-only activation. Default retrieval: eight records and 6,000 serialized characters; explicit detail retains full evidence.

Ruling: execute in Default mode with this ExecPlan because mode switching is unavailable; user explicitly requested implementation. No worktree or commits. Independent discovery and routing/documentation tasks are delegated under canonical coordination instructions; root owns storage/retrieval and integration.

User correction: only index committed contributions attributed by Git author name to example-user Mok. Eligible sources are HEAD-tracked, unchanged against committed bytes, and their latest modifying commit has exact case-insensitive author name example-user Mok. Nested manifests resolve their actual Git owner; no author-by-directory inference. Purge legacy unqualified summaries and derived cache before rebuilding.

Ruling: foundational observations are technical evidence, never inferred personal preference, exclusive ownership, project activity, or capability. Selected docs/manifests/code/test inspection is bounded and reports omissions; source fingerprints support relevant refreshes.

## Protected initial state

Initial git status captured before modifications. Pre-existing edits: README.md, docs/smoke-tests.md, aliases/key_aliases.tmpl, aliases/key_dirs.tmpl, docs/phone-ssh-public-ip.md, feedback-memory/feedback.log, postmortem-memory references and sources.json, backup scripts/exclusions, tasks/lessons.md. Pre-existing untracked backup/SSH/benchmark plans, prompts, tests and incident reports are excluded. Only separable personal-context README/smoke sections and append-only incident ledger additions may overlap.

## Implementation checklist

- [x] Read authority, relevant sources and preferences; capture baseline.
- [x] Write defining RED tests for discovery, compact retrieval, cache and privacy operations.
- [x] Implement bounded project inspection and recurring technical findings.
- [x] Extend retrieval, authoritative project storage, cache, locking and forgetting.
- [x] Update automatic routing, metadata, integrations, README and grouped smoke checks.
- [x] Run synthetic tests and README gate; measure compact retrieval reduction.
- [x] Build real private foundation in bounded batches; verify safe coverage and sampled evidence.
- [x] Run refresh-config, inspect snapshot changes and installed sources/metadata.
- [x] Review complete change with a fresh reviewer; record routing/runtime evidence and limitations.

## Risks and rollback

Private roots require reviewed host-shell writes outside workspace; scope is explicitly authorized by user. Never stage private payloads here or in /tmp. Invalid authoritative data must remain unchanged and fail visibly. Caches are expendable but link/permission failures require safe direct projection. One lock serializes personal/project writes and cache changes. Interrupted forgetting must remain suppressed by authoritative tombstones on all reads/rebuilds. Rollback portable changes individually; do not discard pre-existing work. Preserve original private Markdown sources and canonical v1 context.

## Exact verification

RED then GREEN: python3 -B -m unittest discover -s tests -p 'test_personal_context*.py' -v
Regression: python3 -B -m unittest discover -s tests -p 'test_second_brain_skill.py' -v
README: ./scripts/executable_readme-recruiter-sync
Private runtime: foundation --coding-root /home/example/coding --batch-size 8; validate, bounded briefs/projects/topics, sampled detail hashes vs read-only source files. Log only counts and safe metadata here.
Installation: fish -c refresh-config (live Codex snapshot first); compare portable installed files and allow_implicit_invocation. Fresh sessions: one plausible development choice and one explicit personal-context conversation, plus mechanical-work exclusion; record actual evidence or pending status.
Review: inspect session diff, suppression/concurrency/containment/error cases; verify outputs <= budget and deterministic cache hashes/revisions.

## Progress and evidence

2026-10-06: default shell startup failed twice before execution: bwrap loopback Failed RTM_NEWADDR. Approved host-shell status/read succeeded; matching reviewed workaround found. Living incident registered separately. Actual sandbox path remains unresolved.

## Review notes

Keep matching plan and documentation with implementation if a future commit is requested. Suggested subject: feat(personal-context): add private project foundation and compact retrieval.

2026-10-06: expected RED: nine new compact tests failed unsupported commands; routing tests failed explicit-only policy; source tests missing module. GREEN: 43 personal-context tests, including original 19 storage regressions. Sibling import failure diagnosed/recorded and resolved. Project/cache cap independent16 MiB; context v1 cap stays 2 MiB.

2026-10-06: initial broad pass (261 projects/2,660 sources/nine findings) is superseded by explicit example-user Mok authorship scope. Removed all 261 unqualified derived project records privately, preserving original Markdown and context.json. Rebuild pending committed-source authorship tests. Review fixes: mode drift cleanup and unavailable-project handling observed RED then GREEN.

2026-10-06: final authored foundation command exit 0: 97 qualified projects, 1,048 inspected committed sources, six recurring findings, 273 unavailable/excluded source markers, 680 uninspected markers, zero projects without readable sources. Purged initial unqualified 261 records before rebuild. Sampled 14 sources across eight projects: exact current HEAD bytes, latest example-user Mok author evidence and source hash match. Human Markdown/project files preserved.

Bounded actual outputs: topics 816 chars/eight records; catalog 5,692 chars/five records; Python catalog 4,367 chars/three; architecture brief 5,360 chars/four; design brief 5,663 chars/eight. All <=6,000/eight with omissions and detail IDs. Cache repeated byte-identical. Synthetic full retrieval 27,663 chars vs brief 5,337: 80.7% character reduction. All managed ai-context modes 0700/0600; broader recursive check includes three pre-existing unmanaged files and is not the managed-store contract.

refresh-config succeeded twice, including live-to-tracked Codex snapshot, chezmoi application, shortcuts generation/reload. No dot_codex/config.toml or dot_gitconfig diff introduced. After source finalization all six installed personal-context files match; implicit metadata true.

Three fresh codex exec --ephemeral sessions completed exit 0 without persistent transcripts or private payload logs: implicit architecture task used compact retrieval (six helper calls, no legacy full read); explicit conversation used compact retrieval then a legacy read for deeper context and returned one question; mechanical presence check used zero private retrievals. This tests observed routing in these prompts, not every future task.

Limitations: source slices <=32 selected files, <=128KiB/file, <=four directory levels; complete Git history limited to10,000 commits/32MiB/20s, fail-closed. The conservative latest-author criterion excludes earlier example-user contributions subsequently rewritten by others, untracked/dirty files, unreadable or out-of-budget evidence. Git attribution does not establish exclusive ownership, capability or project activity. No commit/push.


## Final review and reproducible handoff

Fresh reviewer identified stale catalog availability, ancestor substitution and absent-store initialization; all are addressed with deliberate RED/GREEN regressions in the final 59-test suite. Source-budget overflow and technical forgetting/mode drift were also checked and repaired. No deferred review findings. Static checker initially found an untyped module boundary; an explicit validated ProjectEnvelope/Protocol and CLI namespace now describe it.

Atomic change: helper modules + synthetic tests + relevant skill/routing/catalog/README/smoke updates + this plan + related incident/ledger updates; preserve all unrelated pre-existing work. No staging, commit, push or worktree.

Paste-ready Cursor prompt: [authored project context prompt](../prompts/enable-personal-context-for-dev-choices.md). Exact automated commands are above; add basedpyright dot_agents/skills/personal-context/scripts/context_store.py. Manual checks are grouped in docs/smoke-tests.md under Personal Context: compact topics/catalog/brief/detail, authorized foundation/targeted refresh, private correction/forgetting and fresh automatic/explicit/mechanical sessions. Actual private runtime and routing evidence is recorded above.

Suggested commit: feat(personal-context): index authored projects with compact private briefs
Rollback: revert only this task's portable files/hunks; caches can be rebuilt. Preserve original context.json/Markdown, private user records, tombstones and qualified evidence. This task has not modified or committed any project evidence sources.

Final fresh gates: 59 personal-context tests and 12 Second Brain tests pass (exit0); basedpyright typed helper reports0 errors/warnings/notes; README pass_no_change; git diff --check clean. Typed-helper final refresh completed exit0. No unresolved review findings; original sandbox startup defect remains a host issue covered by approved scoped execution.

Final privacy-boundary check: synthetic storage overrides cannot redirect real /home/example/coding evidence outside the designated private root. A mocked no-source-read defining test observed expected RED (guard absent), then a symmetric root/source guard was added; final GREEN below.

Final post-guard verification: 60 personal-context +12 Second Brain tests pass, exit0; basedpyright0 errors/warnings/notes; README gate pass_no_change. Destination guard also rejects parent-traversal aliases and synthetic overrides for nested/ancestor scopes containing the real coding tree; all were exercised without actual source reads. Final refresh-config exits0.

## Authorized session delivery

2026-10-06: User requested $commit-session, then explicitly included both linux-config and /home/example/coding/personal-context. Scope helper reports unsafe/no detected writes for session 01a113a3-55dd-7c71-8147-fa44618e19cb because wrapped tool/subagent writes are not attributed. Use captured initial Git baseline and directly observed writes. Stage only portable personal-context implementation, synthetic tests, related routing/docs/plan/prompt and five reviewed incident reports; isolate personal-context hunks in README/smoke-tests, the helper-boundary lesson and five appended ledger records. Preserve all other dirty backup, SSH, benchmark, feedback and incident-reference work. In the private repository commit only the newly built authoritative project-knowledge.json; exclude its rebuildable cache and runtime lock. Both repositories use main with origin/main upstream. Earlier no-commit statements describe the implementation phase. Delivery checks and results are reported with the commit.

Delivery verification: fresh 60 personal-context and 12 Second Brain tests pass; basedpyright zero errors/warnings/notes; README pass_no_change; private validate succeeds with 97 projects/six findings; refresh-config REFRESH COMPLETE. Scoped staged diff passes whitespace checks. Ledger formatting assertion was stopped before its write, documented in context-session-ledger-staging, repaired with structural HEAD-plus-five-record equality and targeted check (no errors). Final delivery scope is 26 portable files/hunks plus one private authoritative store; excluded cache/lock and all pre-existing work.
