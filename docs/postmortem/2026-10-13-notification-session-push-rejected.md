# Notification session push rejected

Preserve scoped notification work, inspect divergent upstream commits and integrate a compatible change with an ordinary merge before retrying delivery.

## Symptom and impact
Notification commit a76d6d4 succeeded on main. Its push to origin/main exited 1 with fetch-first rejection because the remote had advanced independently. The notification commit remained intact; the first delivery attempt did not succeed.

## Lookup and applicability
Query `git push rejected fetch first remote contains work` returned no specific reusable push remedy. Narrowed `non-fast-forward` search found local-ignored-merge-collision-preflight: applicable to checking collision safety, not evidence of an ignored-file problem here. Incoming changes modify two existing tracked files with no local dirty work or ignored-path collision.

## Root cause and resolution
Fetch advanced origin/main from 6260e09 to a5df44e, `fix(shell): source key_aliases from $HOME`. Only dot_bashrc and dot_zshrc differ, replacing an absolute source path with its equivalent HOME-based path. Reviewed those diffs and confirmed unrelated dirty files do not overlap. Ordinary `git merge --no-commit origin/main` succeeded. No amend, rebase, reset or force push; local notification commit and unrelated dirty work preserved.

## Verification and delivery boundary
Git merge completed without conflicts and staged only the two already-committed upstream shell changes. Add this incident and matching session learning/plan updates to the merge commit, refresh configuration, verify syntax and notification checks, then retry the configured push. Final commit hashes and remote-delivery outcome are reported in the Codex handoff. The underlying divergence is resolved locally; this document does not substitute a future push prediction for observed remote evidence.

## Learning
No new reusable finding: upstream races require inspecting divergence and protecting dirty paths before ordinary integration. Existing collision-preflight guidance covers that safety boundary; the push rejection was not a repository behavior defect.

## Verified local integration
Merged staged content passes five notification tests, Bash syntax, targeted incident-learning validation, README gate and cached diff checks. Zsh is not installed; its equivalent one-line path change was reviewed. refresh-config reported REFRESH COMPLETE, exit 0. Commit and retry delivery through origin/main; final remote status is reported with the commit hashes in Codex output.
