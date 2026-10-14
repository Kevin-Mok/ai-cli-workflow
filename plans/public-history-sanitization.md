# Public History Sanitization ExecPlan

This plan turns this private-dotfiles copy into a public-safe Git repository. It inventories every reachable commit, rewrites sensitive paths, values, metadata, and messages while preserving provenance wherever safe, adds public setup guidance, and proves the rewritten history is clean before the private remote is removed.

## Purpose And Observable Outcome

- Every commit reachable from every retained branch is free of secrets and the personal or third-party information named in the request.
- Original commit messages, primary-author attribution, timestamps, topology, and order remain unchanged except where sanitization requires a replacement; commits are removed only if they become empty.
- Local-only files are ignored, personal values are documented as local inputs, the existing MIT license remains present, and `private-origin` is absent.
- No push, deployment, or mutation outside this repository occurs. Temporary safety/audit artifacts may live under `/tmp` and the final report is `/tmp/ai-cli-dotfiles-public-REPORT.md`.

## Context And Scope Boundaries

- Repository: `/home/example/ai-cli-dotfiles-public`; branch `main`.
- Baseline: 698 commits reachable across all refs, 689 on `main`, 19 local/remote-tracking ref tips, and no tags observed before rewriting.
- Baseline remote: one `private-origin` HTTPS remote; it must be removed only after verification.
- Protected pre-existing working-tree state: four Git LFS media paths appeared modified when LFS filters were disabled. Their exact bytes and metadata were copied to `/tmp/ai-cli-dotfiles-public-protected-20261013/` before classification. All four were later judged unsuitable for publication; the backup remains private only until final verification and cleanup.
- The sandbox cannot write `.git/lfs/tmp`; Git/ref mutation requires the narrow approved execution route. A living report is at `docs/postmortem/2026-10-13-lfs-status-sandbox.md`.
- `gitleaks`, `trufflehog`, and `detect-secrets` were not on `PATH` at initial inspection. Use any scanner that is already available later, plus a repository-local or temporary deterministic scanner and manual review; do not make external installation a prerequisite.
- Do not use a worktree, push, publish, deploy, or touch another project. Do not run `refresh-config`, because it writes outside this repository and could import live private values, contrary to the user's explicit scope.

## Settled Assumptions And Decisions

- The checked-in MIT copyright holder is intentionally public because the user explicitly required the license to remain. The same primary-author display name may remain in Git attribution; all email addresses and all other human names are replaced with neutral public identities.
- Retain all non-sensitive branch histories. Remote-tracking branches with unique history become local archival branches before `private-origin` is removed, using safe names if audit finds a sensitive ref name.
- Prefer exact value replacement or chezmoi template variables for ordinary configuration. Remove a path from all history only when the file class itself is unsafe to publish (private keys, credentials, sessions/cookies, browser/history data, or irreducibly personal notes).
- Replacement rules and raw findings must never be committed. Store them only in a mode-`0600` temporary area under `/tmp`, refer to findings by category/label in tracked docs, and delete the temporary raw audit artifacts after the final rescan.
- Preserve commit topology and order. Preserve messages unless a matched fragment is sensitive. Preserve author/committer timestamps. Drop only commits whose rewritten tree and sanitized metadata add no change relative to their rewritten parent.
- Rewrite all retained refs in one deterministic pass. Keep a temporary private backup bundle in `/tmp` until rewritten-history verification succeeds, then delete it and expire/prune unreachable private objects from this copy.
- Add one final public-readiness commit for `.gitignore`, `README.md`, this ExecPlan, task status, and the completed incident record. The final commit is new and is not counted as an original historical commit.

## Ordered Implementation Checklist

- [x] Record baseline status, refs, remotes, commit counts, available scanners, and protected dirty paths.
- [x] Save byte-for-byte backups of protected pre-existing LFS worktree files under `/tmp`.
- [x] Inventory every reachable path, unique blob, commit message, author/committer identity, and ref name without emitting raw findings.
- [x] Classify findings into exact replacement, chezmoi template substitution, safe whole-file placeholder, or all-history path removal.
- [x] Build a mode-`0600` temporary rule set and a deterministic audit/rewrite harness; validate it on representative fixtures before real history mutation.
- [x] Create and validate a temporary private backup bundle; record original per-ref tips, topology/order signatures, and commit counts.
- [x] Rewrite every retained ref, including commit messages and author/committer emails/names, preserving timestamps and topology.
- [ ] Convert safe unique remote-tracking histories to local archival branches and remove `private-origin` without pushing.
- [x] Remove the four protected LFS media paths from public history, add public-safe `.gitignore` entries, and add README guidance for supplying personal values locally.
- [x] Confirm the MIT license remains byte-for-byte unchanged unless sanitization proves its public author line conflicts with the stated assumption.
- [ ] Run full-history secret/PII scans, manual grep/review, sensitive-path checks, commit-message/identity checks, and unreachable-object checks; resolve every confirmed finding or mark uncertainty explicitly.
- [x] Run repository regression checks and the README recruiter-sync gate without applying live chezmoi state.
- [ ] Update this plan, task status, incident report, harness handoff, and `/tmp/ai-cli-dotfiles-public-REPORT.md` with exact evidence.
- [ ] Obtain an independent evidence-reviewer claim table, fix incorrect claims, and retain unresolved items visibly.
- [ ] Commit the public-readiness changes with their matching plan/status docs, verify again, prune private unreachable objects, and confirm no remote remains.
- [ ] Delete temporary raw findings and private backup material from `/tmp`; keep only the requested final report.

## Risks, Edge Cases, Rollback Points, And Protected State

- A missed alias, encoded token, historical-only blob, LFS object, commit message, or identity could leak on publication. Scan decoded text, high-entropy candidates, Git object content, LFS pointers/objects, metadata, and paths separately.
- Broad name or URL replacement can corrupt source code or public documentation. Require category-aware review and exact rules rather than blanket word deletion.
- History tools can leave original refs, reflogs, replace refs, or unreachable objects. Inspect all refs, expire reflogs, repack/prune, and rescan `git cat-file --batch-all-objects` before declaring the local copy clean.
- Rewriting multiple branches can collapse commits or alter merge topology. Compare ordered parent-count/date/message signatures after normalizing only approved replacements, and explain any count delta.
- LFS clean/smudge behavior can misreport or overwrite protected media. Keep filters disabled for source status comparisons until the sanitized graph is installed; verify the removed payloads are absent from refs and the final LFS store.
- Until destructive rewrite starts, rollback is the current repository. During rewrite, rollback is the temporary `/tmp` bundle. After verification and private-object pruning, rollback is intentionally unavailable in this copy.
- The final report must describe categories and labels only; it must never reproduce a discovered value.

## Automated And Manual Verification

- Baseline and final counts: `git rev-list --all --count`, `git rev-list main --count`, and per-ref first-parent/topology summaries.
- Ref hygiene: `git for-each-ref`, `git remote -v`, `git replace -l`, and reflog enumeration show only retained public refs and no remote/replace/original refs.
- Full object scan: deterministic scanner reads every reachable commit/tree/blob plus commit/tag metadata and fails on confirmed secret, credential, key, PII, private host/URL, employer/client, or personal-note rules.
- Independent scanner: run `gitleaks`, `trufflehog`, or `detect-secrets` against full Git history if one becomes available; otherwise explicitly record unavailability and compensate with pattern, entropy, path, and manual review.
- Manual review: inspect every scanner candidate by category, every rewritten placeholder/template, all remaining email/name/URL/IP/hostname matches, and the final path inventory without copying sensitive values into reports.
- Repository state: the MIT license checksum matches baseline; README and `.gitignore` contain the public-local-values guidance; removed LFS paths and payloads are absent; repository tests and documentation checks pass.
- Object eradication: after removing backup/original refs and expiring reflogs, `git fsck --unreachable --no-reflogs` reports no retained private commits/blobs and the scanner over all remaining objects is clean.
- Delivery safety: `git remote -v` is empty and no push command appears in the execution record.

## Progress And Evidence

- 2026-10-13: baseline status was captured with LFS filters disabled after the normal status command failed on sandboxed `.git/lfs/tmp`; four pre-existing LFS worktree files were protected under `/tmp`.
- 2026-10-13: baseline counts were 698 unique commits across all refs, 689 commits on `main`, and 19 branch or remote-tracking refs.
- 2026-10-13: three independent read-only audits were dispatched for Git metadata/messages, historical paths, and blob content.
- 2026-10-14: the rewrite retained 688 of 698 historical commits; 10 became
  empty after sanitization. Eighteen public-safe local heads preserve the main
  and unique archival histories.
- 2026-10-14: six large screenshots/mockups and all historical audio were
  removed. All 258 retained binary objects are small PNG UI/icon assets reviewed
  through a retained-only manifest and contact sheet. Evidence review found a
  contact number embedded in the remaining JPEG LFS payload, so that path was
  removed from every retained commit and its sole local LFS object was pruned.
- 2026-10-14: a case-insensitive all-object audit passed after checking 688
  commits and 5,128 unique blobs, with zero findings and zero unreachable
  objects. A rule-location regression is covered by the 11-test audit/sanitizer
  suite.
- 2026-10-14: the public README, local-only ignore rules, account templates,
  feedback placeholder, and private-vault placeholder were restored after the
  final rewrite. Final-tip commit, source-repository transplant, remote removal,
  and post-commit rescan remain.
- 2026-10-14: the original LICENSE blob was restored in every retained tree where it exists and
  now matches the source checksum. Independent preservation verification mapped
  all 688 retained commits to original dates and approved message rewrites;
  parent expansion produced zero topology mismatches. The 10 dropped commits
  are exactly the empty rewrite results. Rewrite invalidated and removed 170
  historical commit signatures as expected.
- 2026-10-14: all 11 focused auditor/sanitizer tests pass, the current 1,721-file
  worktree scan has zero findings, and the README recruiter-sync gate reports
  `pass_no_change`. Dedicated gitleaks/trufflehog-style scanners remain
  unavailable, so the deterministic all-object scanner and independent manual
  metadata/path/blob/binary reviews are the recorded compensating evidence.
- 2026-10-14: targeted postmortem-memory checks classified all 30 task incident
  reports as new and produced no other check error. Registering their hashes and
  findings in the separate canonical private repository remains intentionally
  outstanding because this task explicitly forbids modifying another folder.

## Review Notes

- The user directly authorized destructive history rewriting and remote removal, but explicitly prohibited pushing. No separate approval is needed for those in-repository actions; sandbox elevation remains narrowly scoped to `.git` mutation.
- The plan treats the existing license identity as intentionally public and author emails as private. If scanning produces contrary evidence, pause and revise this assumption before rewrite.
- Final publication commands belong only in the external report and are for the user to run later; this task will not execute them.
