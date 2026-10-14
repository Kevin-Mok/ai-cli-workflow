# Progress: Public History Sanitization

Updated: 2026-10-14

## Files

- `plans/public-history-sanitization.md`: active decision-complete ExecPlan.
- `.harness/public-history-sanitization/task.md`: acceptance criteria and scope.
- `.harness/public-history-sanitization/checks.md`: independent evidence review and resolution table.
- `.harness/public-history-sanitization/progress.md`: current handoff.
- `docs/postmortem/2026-10-13-lfs-status-sandbox.md`: living record for the initial Git LFS status failure.
- `/tmp/ai-cli-dotfiles-public-REPORT.md`: final redacted report retained after closeout cleanup.

## Done / Checks Run

- Captured LFS-disabled baseline status: four pre-existing modified LFS media paths; no other tracked/untracked changes reported.
- Counted history: 698 unique commits across all refs, 689 on `main`, 19 branch or remote-tracking tips, no tags.
- Confirmed baseline remote: `private-origin`; no push performed.
- Checked scanner availability: `gitleaks`, `trufflehog`, and `detect-secrets` not found on `PATH`; `rg` and Git are available.
- Copied protected dirty-file bytes and metadata to a mode-restricted `/tmp` directory.
- Started independent read-only audits of metadata/messages, paths, and unique blob content.
- Completed the independent audits: metadata covered all 698 original commits,
  path review covered 2,596 unique paths, and blob review covered 5,280 unique
  blobs (5,012 text and 268 binary).
- Rewrote all retained refs in an isolated clone. The sanitized historical graph
  contains 688 commits on 18 public-safe local heads; 10 original commits became
  empty, and no unreachable objects remain.
- Removed private credential/key/state paths, all historical audio, six large
  screenshot/mockup images, and the final JPEG LFS asset after evidence review
  found embedded contact information. Manually reviewed the 258 retained binary
  PNG UI/icon assets through a retained-only manifest and contact sheet; the
  candidate now has no LFS paths or payloads.
- Added account templates, local-only ignore rules, public-vault and feedback
  placeholders, and README guidance for supplying private values outside Git.
- Added deterministic audit/sanitize CLIs and 11 passing behavioral tests. The
  latest all-object audit checked 688 commits and 5,128 unique blobs with zero
  findings.
- Restored the original MIT license blob in every retained tree where it exists and verified
  its checksum. The preservation comparator matched all 688 retained commits by
  original dates plus approved message transformations and found zero topology
  mismatches; 10 original commits were pruned empty and 170 invalidated commit
  signatures were removed.
- Expanded the focused suite to 11 passing tests, including exact reviewed
  placeholder paths. The current 1,726-file worktree scan has zero findings and
  the README recruiter-sync gate reports `pass_no_change`.
- Ran the canonical postmortem-memory targeted check for all 35 task incident
  reports: all were classified as new, with no other helper error. The required
  external ledger registration is outside the authorized folder and remains an
  explicit follow-up rather than an in-scope write.
- Committed the public-readiness tip as `f497ac7`, then used a guarded transplant
  that verified the exact source status, byte-matched all four protected media
  backups, and copied the complete pre-reset overlay before changing refs.
- Installed 18 neutral local heads, removed `private-origin` without pushing,
  expired reflogs, pruned unreachable Git objects, and removed all four local
  LFS payloads. The post-transplant audit passed across 689 commits and 5,175
  blobs; Git/LFS fsck, ref hygiene, license, and clean-status checks passed.
- Independent final-source review reported no incorrect claim and verified the
  live ref/object/LFS state, retained binaries, documentation, templates, and
  ignores. Its transient-evidence and local-no-push qualifications are retained
  explicitly in the external report.
- Wrote and privately scanned the external report, then deleted 44 temporary
  rewrite/review/backup artifacts. The final audit-rule file is deleted after
  the staged private-rule scan and before the verification-only commit.
- Independent closeout review verified the report's corrected 1,726-file count,
  zero generic report findings, an unchanged clean repository, and an exact
  report-only task inventory under `/tmp`.
- Recorded and corrected two no-impact closeout-verifier assumptions, then used
  the terminal all-object gate to catch and replace an unsafe ambient identity
  in the unpushed closeout commit. The task now has 37 incident reports; the
  final milestone includes both records, local lessons, and matching evidence.

## Decisions

- Existing MIT attribution and the matching primary-author display name are public by explicit license-preservation intent; emails and other human identities are sanitized.
- Use exact replacement/chezmoi variables where viable; delete only intrinsically unsafe file classes or irreducibly personal notes.
- Preserve all safe unique branch history by converting remote-tracking tips to local archival branches before remote removal.
- Do not run `refresh-config`; the user's no-other-folder constraint takes precedence and prevents live private values from being imported.

## Remaining Work

- No implementation or history-rewrite work remains. Publication is intentionally
  left to the user using the commands in the external report.

## Next Action

Review the external report, rotate the three identified credentials, and use
its publication commands only when ready. No push was performed by this task.
