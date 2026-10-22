# Task status

This document records delivery milestones and verification for completed repository work.

## tbo shortcut — chore(fish): add tbo OBS directory shortcut

- Complete: tbo expands to `cd /mnt/usb-8tb/obs` in the existing directory-related command section; no conflicts were commented.
- Scope: directly observed session edits only; stage separate smoke-test and postmortem-ledger additions while preserving pre-existing hunks.
- Verification: refresh-config completed with exit 0; generated fish syntax passed; registered expansion inspected; repeat helper preview returned changed=false. README gate returned pass_no_change; all 21 fish-alias tests passed (43.858s); targeted postmortem ledger check passed.
- Delivery: commit on main and push to origin/main after focused checks and staged review.
- Remaining: unrelated dirty work excluded; default sandbox startup remains unresolved with a verified approved-route workaround.
- Rollback: remove the tbo mapping and refresh configuration.

## Vesktop shortcuts — chore(fish): add Vesktop and Discord shortcuts

- Complete: applications mappings `v vesktop`, `kav killall vesktop`, and `kad killall discord`; previous `v ./start.sh voice` preserved as a comment.
- Scope: session 01a136c2-4774-7b12-88c6-333b2b1bb714; helper could not detect successful writes, so direct conversation write evidence governs. Only session additions in mixed smoke-test and ledger files are eligible.
- Verification: refresh-config exited 0; generated fish syntax passed; all three installed expansions inspected without executing mapped commands; repeat previews returned changed=false. README gate returned pass_no_change; all 21 fish-alias tests passed in 27.697 seconds. Targeted incident ledger check passed.
- Delivery: commit on main and push to origin/main after staged review.
- Remaining: unrelated baseline dirty work stays excluded; default sandbox startup remains unresolved with the verified approved execution workaround.
- Rollback: remove these mappings, uncomment the previous v definition, and run refresh-config.

## Jenkins history scrub — security: scrub historical CI credentials

- Complete: rewrote all 18 local branch histories to replace two Jenkins API
  tokens and one hard-coded third-party bearer credential with explicit
  placeholders; restored the SSH `origin` without pushing.
- Scope: 691 commits mapped; 430 commit IDs changed, 261 stayed identical, and
  none were dropped. Messages, identities, timestamps, and topology were
  preserved except object IDs necessarily changed by sanitized content.
- Verification: exact-value scan found zero occurrences across 5,883 objects;
  the independent public-history auditor found zero issues across 691 commits
  and 5,192 blobs; all 18 tips map correctly; reflogs and unreachable-object
  inventories are empty before final closeout verification.
- Delivery: one local security/documentation closeout commit; explicitly no
  push. Exact force-with-lease commands live in
  `/tmp/ai-cli-jenkins-REPORT.md`.
- Remaining: GitHub still holds the pre-rewrite graph until the operator runs
  the report commands. Credential rotation/revocation remains an external
  operational responsibility.
- Rollback: the verified temporary bundle is retained only through final local
  verification, then destroyed so the scrubbed checkout cannot recover the
  removed values.

## Commit confirmation — docs: repeat commit and push confirmation

- Complete: canonical AGENTS guidance requires the commit hash and actual push status at both ends of delivery replies; durable feedback records the preference.
- Scope: direct-write attribution for session 01a15a20-5ada-7791-b991-6d09afcb0242; only the new refresh incident ledger entry is included from the mixed ledger file.
- Verification: README gate returned pass_no_change; diff whitespace and targeted postmortem ledger checks passed.
- Delivery: commit on main, then push to origin/main after candidate privacy review.
- Remaining: unrelated tmux/postmortem/prompt changes excluded. Full refresh remains blocked by unrelated live MIME settings drift.
- Rollback: remove the four-line delivery rule; preserve the append-only feedback history.

## Expanded confirmation — docs: include full commit message in handoff

- Complete: bottom confirmations include the full Git subject/body, a plain-language change summary, hash, and actual push status.
- Scope: directly observed AGENTS.md and append-only feedback edits; helper could not detect writes for this session.
- Verification: README gate pass_no_change; scoped diff whitespace check passed; exact candidate privacy review required before commit.
- Delivery: commit on main and attempt push to origin/main; earlier commit efacead remains local after a non-fast-forward rejection.
- Remaining: unrelated postmortem references/ledger and tmux prompt excluded; configuration refresh still blocked by existing MIME settings drift.
- Rollback: restore the prior confirmation wording; preserve append-only feedback history.

## Remote integration — chore: merge upstream before guidance push

- Complete: merged origin/main at 94eef13 with the two local confirmation guidance commits, preserving both histories.
- Verification: automatic merge completed without conflicts; README, merge whitespace and exact candidate privacy checks run before commit.
- Delivery: push the merged main to origin/main after commit; preserve unrelated edits via the named commit-confirmation-push-preserve-local stash until restoration.
- Remaining: full refresh remains blocked by existing MIME settings drift; unrelated postmortem edits and tmux prompt stay outside the commit.

## Summary ending — docs: put full commit message last in summaries

- Complete: canonical instructions and durable feedback put skipped checks/risks before the bold commit status, with the full recorded commit message last.
- Scope: direct-write fallback for session 01a15b52-f3a9-7e12-8679-288fba9267a0; the scope helper could not recognize this conversation's writes. Only AGENTS guidance, the appended feedback entry, and this milestone are included.
- Verification: refresh-config exited 0; README gate returned pass_no_change; scoped whitespace check passed. Exact candidate privacy gate must pass immediately before commit.
- Delivery: commit on main and push to origin/main after candidate review.
- Remaining: pre-existing postmortem references, staged/unstaged ledger edits, incident documents, plan, and prompts remain excluded; no implementation changes or runtime tests needed.
- Rollback: restore the previous AGENTS wording; retain append-only feedback history.

## Screensaver shortcut — feat(i3): add Alt+Shift+S screensaver shortcut

- Complete: left Alt (keycode 64, Mod1)+Shift+S launches the existing media preview on key release; Super+Shift+S remains available. Tracked template, README, usage and smoke checklist agree.
- Scope: direct-write fallback for session 01a15bd7-794d-7263-bbaa-935a7367f78c; the helper reports no recognized writes despite the pre-write baseline and observed edits in the conversation. Include only the shortcut/doc hunks, its incident and corresponding no-new-learning ledger record, plus this milestone.
- Verification: defining assertion observed RED then GREEN; focused independent checks4/4passed. Live i3 validation exited0 with existing wheel-command deprecation warnings; refresh-config exited0; reload succeeded. Injected Alt+Shift+S emitted the expected IPC binding, displayed the screensaver and Escape dismissed it. README gate returned pass_no_change; targeted incident ledger check and whitespace check passed. Exact staged privacy review is required before commit.
- Delivery: commit on main and push to origin/main after scoped staged review and privacy checks. No remaining implementation work or blockers.
- Remaining: preserve all unrelated baseline dirty work, including other hunks in README, smoke tests and the ledger. Physical keyboard acceptance remains manual; injected X11 behavior is verified.
- Rollback: remove the new Alt binding from tracked and live i3 configuration, then reload i3. Live i3 is unmanaged by chezmoi; no private live configuration is committed.

## Left monitor DND — fix(i3blocks): show DND before volume

- Complete: the secondary bar includes the existing clickable DND helper immediately left of volume, refreshing every two seconds. Source and preserved live config were updated; i3 reloaded successfully.
- Scope: session 01a15f91-de0d-7691-ab2b-7b47ceafde79; the helper detected no writes, so directly observed conversation edits govern. Only the DND hunks in README, smoke tests and postmortem ledger are included.
- Verification: live protocol reproduced the absent block before the fix and emitted `dnd → volume → calendar` afterward. Pause state stayed false. Targeted postmortem check and whitespace check passed; README gate returned pass_no_change.
- Delivery: one focused commit on main, then push to origin/main after staged privacy review. Initial review blocked a machine-specific ledger home path; the public candidate uses the repository-standard placeholder.
- Remaining: unrelated dirty work excluded; full refresh stopped safely at the pre-existing media-screensaver conflict. Visual and click verification remain manual.
- Rollback: remove only the DND stanza from source and preserved live secondary config, then reload i3.

## Volume clicks — feat(i3blocks): mute and unmute with clicks

- Complete: left-click explicitly unmutes; right-click explicitly mutes. Middle-click and scrolling retain their behavior; pywal colors load from HOME.
- Scope: direct-write fallback for session 01a15fe6-bffc-72d2-90b7-01a0f98f2637; scope helper detected no writes. Include only session additions in mixed README, smoke tests and incident ledger.
- Verification: defining regression observed RED then GREEN; fresh regression and Bash syntax checks pass. Refresh exited 0; exact installed source comparison passed. Real mixer checks for buttons 3/3/1/1 returned off/off/on/on and restored the original unmuted state. README gate pass_no_change.
- Delivery: one focused commit on main, then push to origin/main after exact staged privacy review. No implementation blockers remain.
- Remaining: preserve all unrelated baseline work. Physical mouse clicks remain manual.
- Rollback: restore the prior two click handlers and apply the volume script.

## Super mute toggle — feat(i3): toggle speaker mute with Super+M

- Complete: left Super (keycode 133)+M uses the existing speaker mute toggle and refreshes i3blocks. AGENTS.repo and append-only feedback require validating and reloading i3 after successful rf when i3 configuration changes. README and audio smoke checks describe the shortcut.
- Scope: direct-write fallback from the active conversation; helper recognized no writes. Include only observed shortcut/guidance/doc edits, the desktop-access report and its no-new-learning ledger entry. Mixed files retain unrelated hunks; public ledger aliases use the established placeholder home.
- Verification: refresh-config exited 0; i3 config validation exited 0 with existing wheel-command deprecations; reload returned success. Two injected Super+M presses toggled mute yes/no/yes and restored the initial state. README gate pass_no_change; targeted incident-memory check and whitespace check passed. Exact staged privacy review is required before commit.
- Automated validation warning: postmortem-memory tests passed 25/26; full-corpus coverage fails on absent placeholder home roots. Targeted report check passes. No unrelated corpus repair included.
- Delivery: one focused commit on main, then push to origin/main after staged checks. No remaining shortcut implementation work or blockers.
- Remaining: preserve all pre-existing and unattributed dirty files. Physical keyboard and subjective listening checks remain manual.
- Rollback: restore the previous Super+M binding in tracked and preserved live i3 config, then reload i3. Preserve append-only feedback history.

## Tcu directory shortcut — feat(fish): add tcu directory shortcut

- Complete: tcu expands to cd ~/coding/track-codex-sessions in the cdn section; existing tcs remains available and no conflicts were found.
- Scope: direct-write fallback for session 01a1645a-7540-7161-97de-cd4af4ec8701; helper recognized no writes. Only the shortcut, inspection report, its ledger entry and this milestone are eligible.
- Verification: refresh-config exited 0; host-preserved alias template was explicitly deployed and regenerated. Generated fish syntax, loaded tcu query and tcu/tcs definitions passed. README gate pass_no_change; targeted incident-memory check passed.
- Delivery: commit on main and push to origin/main after isolated candidate privacy review. No remaining implementation work.
- Remaining: unrelated staged and unstaged changes excluded; interactive expansion was not executed. Existing fish sessions may need reloading.
- Rollback: remove only tcu from the directory template, deploy it and regenerate shortcuts.
