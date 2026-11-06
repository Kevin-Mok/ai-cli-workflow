# Automatic Lavish creator connection test

Run one command to create a disposable dark page and Codex creator, verify their
connection, submit an edit through Lavish, verify the result, clean up and exit.
The test requires no URL/ID entry, Send click or manual ending. This plan records
the final implementation and its delivery evidence; detailed incident history
is in docs/postmortem/2026-11-06-lavish-feedback-listener.md.

## Context and scope

Lavish 0.1.89 identifies sessions by artifact path and does not persist a creator
Codex-thread route. An open page or owner label cannot establish the connection.
The test captures the actual creator thread.started UUID and requires a fresh
nonce, delivered receipt, correct self-reported ID and resumed live listener.

Owned implementation: scripts/executable_lavish-connection-test (orchestration),
scripts/lavish_connection.py (protocol and result parsing),
scripts/lavish-manual-test.js (SDK queue+send), scripts/lavish-test-page.html
(preset), tests/test_lavish_connection.py plus lavish_connection_* fixtures and
cases. Related README, smoke checklist, feedback and incident learning belong
in the same commit. Preserve all unrelated baseline dirty work, including
Firstmate docs, other incident records, configuration and other ledger findings.

## Settled decisions

- Bare mode starts normal configured codex exec with automatic approval review,
  an owned private temporary directory and the bundled preset. No model override,
  ignored configuration, sandbox bypass, or persistent global changes.
- The creator copies the preset exactly, registers with lavish-axi --no-open,
  explicitly opens Google Chrome and keeps a foreground feedback poll attached.
- Read live /health and matching local state identity; never trust cached CLI
  inventory. Observe chat without consuming a competing poll.
- Send exactly one nonce then one SDK edit. The expected ID is never in the
  nonce challenge; the agent reads its own CODEX_THREAD_ID. Only the fresh owned
  page is automatically edited. Explicit URL/--expect-thread mode stays nonce-only.
- After nonce and preset checks, queuePrompt then sendQueuedPrompts submits the
  edit in the actual browser path. Terminal/chat explain the expected result.
- EDIT TEST PASS requires real h1 text, helper removal, delivered/done request,
  subsequent parsed own-ID confirmation and resumed matching listener. HTMLParser
  excludes commented/script headings; mere ID mentions cannot pass.
- Startup is bounded to120s. --timeout independently bounds nonce/edit phases
  (default60s); in-flight socket I/O can add up to5s before failure. No late PASS.
  Four stages and5s elapsed progress replace repetitive waiting/manual steps.
- TEST COMPLETE follows confirmed readable ended-page state and owned process
  group cleanup, including descendants/late registration after leader exit.
  Unknown state or end-command exit0 alone cannot mean cleanup succeeded.

## Checklist

- [x] Capture baseline and inspect applicable instructions/preferences/source.
- [x] Reproduce missing listener, manual completion and non-concluding review.
- [x] Observe defining no-click SDK-send/edit-deadline regressions RED.
- [x] Implement automatic flow and preserve explicit existing-page checker.
- [x] Correct parser, lifecycle, partial-state and cleanup issues with regressions.
- [x] Run real configured no-input acceptance and independent source review.
- [x] Update README, smoke checks, feedback and incident hash/learning.
- [x] Split oversized new code/tests mechanically to meet20k-byte file guard.
- [x] Re-run all36 cases after split and review exact scoped staged diff.
- [x] Prepare focused commit milestone; preserve unrelated work and push configured upstream after commit.

## Verification evidence

Before implementation, tests reproduced missing auto-send, unbounded manual wait,
wrong/stale/undelivered replies and false cleanup completion. Review regressions
also reproduced commented/script fake headings, wrong own-ID with expected-ID
mentions, process descendants surviving leader exit and late page registration.
Each was corrected without weakening the defining assertions. Fixture nested
quoting and partial JSON read/timer teardown errors are recorded in the incident.

Independent final behavioral checks before the mechanical split:
- python3 -B -m unittest discover -s tests -p test_lavish_connection.py -v:
  36/36 passed,21.399s, exit0. Help, Python compile and Node syntax checks passed.
- Bounded source review verified5/5 claims, no unresolved material finding.
- Real bare invocation with no stdin/UI input created creator
  01a1b2fd-49c9-77a3-83d7-8352a84cda02 and pagefd6a9b92bbc5a68b. Nonce
  c36955e81a3c482da40776a1ede1130b passed, actual SDK sent the edit, EDIT TEST PASS
  and TEST COMPLETE followed cleanup; command exited0.
- Independent host state read: statusended, exactly2 user messages,
  edit_verified=true, owned listener absent. Other editors remained untouched.

Commit prerequisite: new-file guard caps files at20,000bytes. Moved protocol/
parsing helpers verbatim to a local module; entry still re-exports helpers and
works from any cwd/runpy. Split tests into fixtures/protocol/smoke modules, with
all36 method bodies verified unchanged by AST source ranges. Public discovery
command remains the same. Plan condensed to final decisions/evidence; detailed
historical milestones remain in the living incident and prior task-status file.

Manual check: run scripts/executable_lavish-connection-test with no arguments;
observe preset, expected notice, automatic edit and successful exit. Repeat with
--plain for ASCII. Existing-page mode must send only nonce and leave page intact.
Do not run a model session solely for help/invalid-timeout validation.

## Risks and rollback

One small configured Codex session is used per real smoke. Internal Lavish API
contracts can change; malformed state/deadlines fail closed. A test proves its
page at test time, not automatic wake-up or unrelated editors. Real phones,
other browser engines and the unrelated full repository suite were not tested.
Rollback this focused change without deleting other review pages or rewriting
append-only feedback. Explicit checker and normal user review semantics remain.

## Delivery milestone

Subject: test(lavish): automate creator connection smoke test.
Scope helper missed orchestrated writes for session
01a1b293-7daf-76d1-b910-392c3a9a4dec; use directly observed edits and isolated
hunks in mixed README/smoke/feedback/ledger files. Earlier theme preference commit
cc8ca34 was already pushed; this milestone ships the subsequent E2E work.
Validation and staged review pending below; push configured origin/main once
this single focused commit passes its gates. No force/amend/rebase requested.

Post-split fresh checks:36/36 unittest passed20.656s, pytest collected exactly36,
help and runpy from /tmp work, all split modules compile. README gate passed.
New authored files are below20k bytes; legacy oversized README/smoke/guidance/
ledger warnings are non-safety validation findings, not permission to stage
unrelated formatting or change guard policy. Commit milestone pending staged
review/privacy gate, then push origin/main.

Staged review:15files, only session hunks; all new code/tests/plan are below20k
bytes. File-size check returned1 for growth in4 already-oversized legacy files:
README, smoke checklist, browser guidance and sources ledger. Recorded as a
non-safety warning under best-effort delivery; no hook or guard policy changed.
Active pre-commit/pre-push privacy hooks stay intact. Required privacy gate is
the last check before commit; all implementation work is complete.
