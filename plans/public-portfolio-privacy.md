# Preserve reviewed public portfolio content

This living ExecPlan accompanies the shared privacy-gate prerequisite for shipping the portfolio academic explorer. Keep verification and delivery notes current with the implementation.

## Purpose / Big Picture

Intentionally public professional contact details and reviewed portfolio media should pass precise content review while secrets and private material remain blocked.

## Progress

- [x] (2026-10-29) Captured clean target-file baseline and reviewed the actual blocked blobs and existing approval mechanism.
- [x] (2026-10-29) Observed installed-hook RED, then extended accepted reviewed categories by one line.
- [x] (2026-10-29) Passed five focused checks, all 59 privacy tests, one frozen-tree integration and no-write syntax/whitespace checks.
- [x] (2026-10-29) Added 12 exact-path/full-hash approvals after reviewing intended public contacts, article URLs and incidental SVG/compressed-media matches; actual portfolio candidate passes.
- [x] (2026-10-29) refresh-config completed and the existing canonical hook snapshot was refreshed; exact isolated candidate privacy check passed.
- [x] (2026-10-29) Committed prerequisite 72b1d33 with preserved hooks and isolated scope; portfolio feature committed as c9266ee in its new worktree.
- [x] (2026-10-29) Moved the three reviewed incident aliases into the committed feature worktree, preserved unrelated learning entries, and prepared scoped verification closeout.
- [ ] Publish the verified commits normally; resulting remote receipts are reported in Codex output.

## Surprises & Discoveries

The gate checks the full candidate tree, including unchanged portfolio files. Existing exact-hash approval schema excluded email/IP categories even for reviewed public content. One supplemental syntax check could not write a cache; no-write compile verification passed instead. An automatic approval capacity error prevented the first delivery-note write; no rejected action was executed or bypassed.

## Decision Log

2026-10-29: Add only email and ip_address to the existing reviewed category set. Do not add a repo exemption or binary skip. Keep private literal/path precedence and all credential/token/key checks. The user explicitly authorized this public-portfolio interpretation and commit/push.

2026-10-29: Ship the canonical prerequisite separately from the portfolio feat/academics branch. Use an isolated temporary index so unrelated linux-config changes remain untouched. Publish normally; do not rewrite history.

## Outcomes & Retrospective

The actual portfolio gate passes without deleting existing public content. Approval is revoked after byte edits; explicit private policy and secrets still block. The portfolio also passes 11 academic tests, typecheck, lint and full build in its new worktree. The prerequisite milestone is identified by subject fix(privacy): support reviewed public portfolio content; resulting hashes and push status are reported by Codex.

## Context and Orientation

scripts/privacy_gate.py validates reviewed categories. scripts/privacy_gate_approvals.json binds each entry to an exact path reference, full content hash, category and reason. tests/test_pre_commit_privacy_gate.py exercises installed hooks; tests/test_checkpoint_privacy_gate.py covers immutable-tree checks. Public portfolio intent is recorded in that project's AGENTS.repo.md.

## Plan of Work

Extend the category validation, add synthetic installed-hook boundary regressions, review and register the 12 real findings, then check the exact staged portfolio candidate. Activate reviewed configuration and commit only the source, tests, approvals, this plan and the new README paragraph through an isolated index. Inspect the immutable candidate and preserve hooks before pushing the prerequisite and feature branches.

## Concrete Steps

From this repository run python3 tests/test_pre_commit_privacy_gate.py and python3 tests/test_checkpoint_privacy_gate.py; expect 59 and one passing tests. Run the canonical executable_privacy-gate check with --repo pointing to the portfolio worktree; expect PASS. Before each commit use the same isolated GIT_INDEX_FILE for the gate and commit.

## Validation and Acceptance

A reviewed synthetic contact/IP blob passes; any byte edit revokes approval. An explicit private literal, provider token, credential, private key or private path still blocks despite approved public categories. The actual portfolio remains unchanged and passes. Do not stage raw transcript PDFs, identifiers, machine-local files or unrelated dirty hunks.

## Idempotence and Recovery

Preserve existing approvals and reject duplicates. Removing these reviewed entries restores the portfolio block. Reverting category support also requires removing its new entries to keep the schema valid. Preserve existing hooks and avoid history rewriting.

## Artifacts and Notes

The portfolio incident records before/after evidence. No raw personal values are stored in the approvals. Existing hook snapshots require explicit refresh after policy edits; refresh-config excludes scripts. The portfolio initially has only its existing resume pre-push hook. The canonical README was already dirty; only the newly added public-portfolio approval paragraph is staged through the isolated index, preserving all prior README edits.

## Interfaces and Dependencies

No dependency, schema shape, public API or CLI flag changes. load_approvals accepts two additional category values; path/full-content hash binding and private-policy precedence remain intact.

Revision note: Created with the minimal shared prerequisite and individually reviewed approvals, keeping the delivery and safety evidence in the same change.

Delivery closeout: the public-portfolio gate prerequisite is 72b1d33; the academic feature is c9266ee on feat/academics. Only this plan and the three session-owned reviewed report records enter the verification follow-up. All other dirty canonical files and learning records remain excluded. No code changed after the passing suites.
