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
