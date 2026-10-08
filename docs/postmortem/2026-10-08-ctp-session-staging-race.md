# ctp session commit staging race

This report records an unintended mixed commit and preserves the evidence needed to recover without losing concurrent work.

- Symptom: Reviewed staged scope contained five ctp-session files. At commit time it contained twelve files, including another session's README, directory alias, fish skill, tests, plan and incident.
- Impact: Local commit 5451db5 includes unauthorized other-session content. It was not pushed by this session. Working tree bytes remain preserved.
- Lookup: Searched shared index concurrent staging commit; reviewed local-skip-worktree-and-scoped-state. It requires direct scope evidence but does not resolve a staging race. No applicable verified recovery found.
- Root cause: Shared index changed between scoped review and git commit. The final staged stat showed unexpected paths, but the command continued into commit without enforcing the reviewed path set.
- Evidence: Earlier staged stat had five files; final stat and commit output had twelve. git ls-remote origin refs/heads/main returned f66f9386191b0bb7266c5ec071e990347e26faa0 after commit creation, confirming 5451db5 was local at that check.
- Status: Unresolved. Delivery paused before push. Rewriting the local commit requires explicit user authorization under active policy.
- Proposed recovery: With permission and concurrent writers stopped, rebuild this local commit from its parent using only scoped session additions; preserve all other work unstaged. Use a temporary isolated index and verify exact tree bytes before commit.
- Follow-up: Enforce the reviewed path/blob set before commit; do not rely on a shared staged index remaining unchanged. No reset, amend, rebase, or force-push has been performed.

## Recovery checkpoint

The user authorized correcting the local commit and pushing. Fresh inspection then found HEAD and origin/main both at f8f044eab832bc6fd29340c86d3472114554839b, with 5451db5 as its parent. git ls-remote independently confirmed that remote hash. Another session has published the mixed commit and a subsequent fish verification commit. The local-only recovery assumption is invalid; no reset or rewrite has been attempted. Published-history rewriting would require an explicitly authorized force-push and preservation of the later commit. Await the user's choice between a history-preserving documentation correction and splitting the published mixed commit.

## Final disposition

The user chose to keep published history intact. Commits 5451db5 and f8f044e remain unchanged. A focused follow-up records the accurate delivery state and shared-index learning. This closes delivery by user decision; the underlying staging-race prevention remains unverified. Future scoped commits must enforce explicit file scope rather than consume all shared staged content. The follow-up uses git commit --only with the four reviewed documentation paths. No configuration behavior is changed and no force-push is needed.
