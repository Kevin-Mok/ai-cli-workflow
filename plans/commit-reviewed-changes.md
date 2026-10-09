# Commit and push reviewed changes

Deliver the reviewed dirty worktree as seven coherent commits, oldest to newest, and push the complete verified series once to origin/main. Split shared-file hunks without discarding their full working-tree contents.

## Context and decisions

User approved the commit plan and explicitly requested commit and push. Initial state: main at bf51890 tracking origin/main, 15 modified tracked files and 13 untracked files, empty index. Initial snapshots are under /tmp/linux-config-commit-series/initial. No worktree or history rewrite. Related plans, README, smoke checks and incident learning belong with their implementation.

Feedback repair restores the HEAD byte prefix and appends all seven new entries; no original historical entry is removed. Public documentation uses direct verification terminology. Vesktop's disabled-plugin/window/cloud-default changes are reviewable; its generated settingsSyncVersion is excluded from the index and preserved in the working tree. External learning chronology is partly inferred from dated reports and companion-file timestamps; final recovery documentation and Vesktop are placed after the formatting follow-up.

## Ordered checklist

- [x] Capture status, review every dirty file, confirm upstream and inspect skill contracts.
- [x] Repair append-only feedback and stale smoke-check terminology; preserve initial snapshots.
- [x] Run focused notification, speech/setup, type, private daemon, README and targeted learning checks.
- [x] Run refresh-config, inspect all resulting source changes and verify installed event probes.
- [x] Commit delivery policy and inspection incident.
- [x] Commit October 8 session-insight learning.
- [x] Commit VPS lookup evidence.
- [x] Commit notification eligibility and companion plans/docs/tests.
- [x] Commit final command-formatting guidance and pending acceptance evidence.
- [x] Commit graphical recovery learning and manual checks.
- [x] Commit Vesktop settings excluding generated sync-version metadata.
- [x] Verify local delivery checks and prepare one upstream push; report its observed result in the final handoff.

## Verification and limits

Fresh checks: python3 -B tests/test_codex_notification_sound.py; python3 -B tests/test_codex_notification_speech_setup.py; python3 -B tests/test_codex_question_notification.py; basedpyright --level error on changed Python handlers; checkout and installed silent-event probes; xvfb-run private Dunst check; README gate; git diff --check; targeted postmortem-memory checks for added reports. JSON semantic comparisons and report hashes precede staging. Review each staged diff.

Historical notification defining RED is recorded in plans/fix-unnecessary-question-audio.md; do not invent fresh RED for an already-implemented fix. Historical broader checks had an unrelated picker/fzf failure and a workflow exact-literal mismatch; focused checks are reported separately. Actual hardware listening, exact wrapped command clipboard acceptance and external guest recovery remain manual acceptance.

## Risks, protected work and rollback

Concurrent work may appear: compare status and snapshots before staging, and leave unattributed changes untouched. refresh-config snapshots live Codex and Git config before chezmoi application, regenerates shortcuts and reloads fish; inspect any adopted drift. The generated Vesktop sync version is intentionally residual. Commit rollback requires a separately authorized revert; never reset or amend delivered history. Remote push failure leaves local commits intact.

## Progress and review notes

README gate returned pass_no_change. Independent notification review found no safety issues: 60 focused tests passed in 16.785s; type check reported zero errors/warnings. Root independently verified actual checkout/installed silent-event CLI and private Dunst behavior. Initial inspection failures and no-new-learning decision are in docs/postmortem/2026-10-09-commit-series-inspection.md.

## Commit milestones

Milestones below are updated before each corresponding commit and retained through the series. Runtime acceptance limits above remain explicit.

Fresh root evidence: checkout/installed silent probes passed all14 cases; completion1, valid questions2 and all rejected events0. Private Dunst1 PASS (2.747s); setup7 PASS; question12 PASS. All nine local targeted learning checks report no errors/new/changed/missing_sources/unregistered_aliases. refresh-config exit0, REFRESH COMPLETE, /tmp/refresh-config-20261009-180809-99754.log; no additional source paths changed. README gate pass_no_change.

### Milestone 1: docs(workflow): require direct verification handoffs

Delivery policy, append-only feedback repair and inspection incident are reviewed; README gate and local report hash checks pass. Remaining: six groups, generated Vesktop timestamp and remote delivery. Next: October 8 external learning.

### Milestone 2: docs(postmortem): capture session insight findings

Session insight reference and four reviewed external report records are included with their three findings; aliases and available source hashes were independently checked. Remaining: five groups and remote delivery. Next: VPS lookup evidence.

### Milestone 3: docs(postmortem): record VPS backup lookup limits

VPS lookup report and its exact reviewed hash are included; targeted learning check has no errors or changed aliases. No backup or restore acceptance is claimed. Remaining: four groups and remote delivery. Next: notification eligibility.

### Milestone 4: fix(notifications): silence non-user-facing completions

Notification code, tests, public docs, original/follow-up plans and learning are atomic. Fresh60 notification tests,7 setup tests,12 question tests and type check pass; source/installed14-case silent probes and private Dunst check pass. Remaining: three groups and remote delivery; hardware listening remains manual. Next: final formatting guidance.

### Milestone 5: docs(codex): separate runnable commands from reading code

Final runnable-command/reading-code policy, compiled prompt, historical/current reports and learning are included together. Exact wrapped clipboard acceptance stays pending. Remaining: recovery/Vesktop groups and remote delivery. Next: graphical recovery lessons.

### Milestone 6: docs(recovery): capture graphical VPS verification lessons

Graphical recovery reference sections, signed metadata/current-boot findings and corresponding smoke checks are included. Guest GNOME/runtime acceptance remains external/manual. Remaining: Vesktop settings and remote delivery. Next: reviewed desktop settings.

Final pre-commit refresh: fish -c refresh-config completed with REFRESH COMPLETE, exit0. Source status contains only the remaining reviewed Vesktop file; no new configuration drift. Remote delivery is intentionally reported after the final local commit, so milestone notes below retain their commit-time state.

### Milestone 7: chore(vesktop): refresh plugin and window settings

Vesktop disabled-plugin/window/cloud defaults are included; generated settingsSyncVersion is excluded and preserved locally. All seven reviewed groups are committed in order after this milestone. Verification: fresh focused suites, type, daemon, silent CLI probes, README, JSON and report hashes pass; diff checks pass. Remaining: push origin/main and report its observed result; exact clipboard/hardware/external guest acceptance stay manual. Next: one upstream push.
