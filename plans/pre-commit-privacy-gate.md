# Pre-commit privacy gate implementation plan

Implement the saved privacy-gate specification by testing disposable commits,
sharing the history scanner, installing a reversible local hook, and documenting
its coverage. No real commit, staging, push, history rewrite or credential change.

## Purpose and scope

Spec: `prompts/pre-commit-privacy-gate.md`. Use Python standard library and Git.
Files: shared history auditor, new privacy gate and disposable regression suite,
Second Brain checkpoint caller, three commit skills, README and smoke tests.
The initial `git status --short` was captured before writes: many existing tracked
and untracked changes are protected, including README, smoke tests and checkpoint
adjacent modules. Only append separable relevant documentation; leave all existing
hunks intact. Current hook directory has samples only; hooksPath is unset.

## Decisions and assumptions

- Scan the entire exact index snapshot (including unchanged candidate blobs and
  paths); deletions disappear. No working-copy substitution. Support an immutable
  `--tree` candidate for commit-tree callers. Honor GIT_INDEX_FILE.
- Reuse byte patterns and private mode-0600 literal/path rules. Add provider token
  patterns and quoted credential keys. Default sample domains remain fixtures;
  public Git identities require exact private-rule approval, scoped to metadata.
- Read local LFS payloads without downloads; refuse missing/unreadable payloads.
  Raw binary bytes are scanned but compressed/encrypted/visual data is not decoded.
- Install a local hook and scanner snapshot, preserve any existing hook and
  hooksPath, and expose install/status/uninstall. Hook changes are reversible.
- No external service, dependency installation, model calls or live test commit.

## Ordered checklist

- [x] Read policy/scanner/callers; capture protected baseline.
- [x] Define disposable tests and observe absent-gate RED (exit 1, safe assertion).
- [x] Implement exact-candidate scanner, redacted CLI and reversible installer.
- [x] Gate Second Brain immutable trees and three agent-driven commit paths.
- [x] Run disposable actual-commit, edge-case and history regression checks.
- [x] Document activation, bypass boundary, limits, repair and rollback.
- [x] Activate locally after disposable GREEN, verify status, run safe refresh.
- [x] Review final diff and record evidence and unresolved risks.

## Verification

Defining RED: `python3 tests/test_pre_commit_privacy_gate.py` exited 1 with
`privacy gate entry point is absent` before implementation (test author observed).
GREEN commands and actual outcomes will be recorded below. Required focused
checks cover commit refusals without HEAD/index changes, repair, partial staging
both directions, initial/rename/delete/weird paths, conflicts/unreadable objects,
private rules, hook chaining/reinstallation and linked worktrees.

## Risks and rollback

Git hooks are local and bypassable with --no-verify, alternate hooksPath,
commit-tree or removal; this is not server enforcement or all-history auditing.
Rules are heuristic and cannot find every secret. No raw matches or filenames
may enter gate diagnostics. Do not copy live rules into source. Uninstall restores
the prior hook; preserve any changed hook rather than overwriting it. Refresh may
encounter unrelated local drift; report its actual result without adopting files.

## Progress and review notes

Implementation and local activation verified. Inline execution authorized by the saved prompt;
Plan Mode is not available in this harness. Search and test work delegated per
repository policy. No commits are authorized by this task.

## Final verification evidence

- Initial defining RED: absent entry point, exit 1 (test author). Separate
  checkpoint helper RED: `python3 -m unittest discover -s tests -p
  test_checkpoint_privacy_gate.py`, exit 1, expected missing-helper assertion.
- Independent review identified refs/replace substitution. New executable
  regression observed unsafe original index bytes incorrectly passing (exit 0)
  before disabling replacement objects. The same test now checks the index,
  frozen tree and actual refused commit. History object reads also disable
  replacement refs; its new original-byte regression passes.
- `python3 tests/test_pre_commit_privacy_gate.py`: 38 tests, exit 0. Includes
  actual initial/safe/repair commits and token/key/runtime/private-path/identity
  refusal without HEAD/index changes; --author and environment author overrides;
  both staging divergence directions; rename/delete/unusual byte-safe paths;
  conflict, unreadable object/rules/scanner, binary/local LFS/missing LFS;
  exact metadata-only public identity approval; hook preservation/reinstallation,
  hooksPath, mutation-after-first-scan and linked worktree behavior.
- `python3 -m unittest discover -s tests -p test_checkpoint_privacy_gate.py`:
  1 test, exit 0. Frozen-tree checks survive relocation of checkpoint.__file__
  into an installed module layout and a divergent unsafe index.
- `python3 tests/test_audit_public_history.py`: 14 tests, exit 0.
- `python3 tests/test_second_brain_checkpoint.py`: 24 tests, exit 0, including
  a real shared-gate pipeline refusal before plumbing commit creation. Existing
  private-vault mechanics mock the new public-policy boundary alongside the
  pre-existing doctor/README boundaries; there is no production exemption.
- Python compilation and focused `git diff --check`: exit 0.
- `./scripts/executable_readme-recruiter-sync`: `pass_no_change`, exit 0.
- `python3 scripts/executable_privacy-gate check --plain`: expected refusal,
  exit 1, 16 findings; credential/email/provider_token/sensitive_path categories.
  No matched values or filenames printed. These are existing index candidate
  contents/effective metadata, not new staged work; left untouched for local review.
- `python3 scripts/executable_privacy-gate install`: exit 0 after disposable
  tests passed. `status --plain`: exit 0, scanner active/current. hooksPath remains
  unset; no prior active pre-commit hook existed, and other sample/hooks remain.
- `git hook run pre-commit` (actual installed hook, no commit): exit 1 against
  the current blocked candidate. Before/after HEAD and NUL-delimited index entry
  bytes compare equal. No real commit, staging or push occurred.
- `fish --no-config -c 'set -p fish_function_path
  /home/example/linux-config/dot_config/fish/functions; refresh-config'` (substitute
  actual checkout function directory): exit 0, REFRESH COMPLETE. This checkout's
  existing helper applies chezmoi with scripts/externals/removals excluded and
  regenerates/sources shortcuts. It did not snapshot live Codex settings; that
  pre-existing refresh implementation differs from the standing description and
  was preserved. Scripts are activated via the explicit gate installer.
- Independent source reviewer verified replacement-object and installed-layout
  fixes and found no remaining high-confidence source issue within scope.

## Remaining limitations and review

The focused total is 77 passing tests. The unrelated, pre-existing checkpoint
journal suite still has a setup failure because the sanitized public vault no
longer contains its Decisions.md fixture; no full-repository suite was claimed.
Current candidate findings are intentionally blocking; this task does not publish
or clean the user's pending contents. No secrets were rotated and no history was
rewritten. Gate patterns are heuristic; binary scanning covers raw bytes, not
compressed/encrypted/visual semantics. Commit messages, other plumbing callers,
external races and deliberate Git-hook bypasses remain outside local enforcement.
A configured shared hooks directory affects its other users as documented.

Docs updated: README activation/use/private policy/coverage/removal, grouped smoke
checks, this plan, and three commit skills. The dated operational report records
capability-discovery and pre-existing fixture issues; its memory review records a
no-new-learning decision. Preserve unrelated dirty hunks in all mixed files.
Rollback is the documented gate uninstall action, restoring the original hook.
Suggested future focused commit: `feat: enforce staged privacy checks before commits`.
No commit is part of this authorized task; include this plan with any later
related implementation commit.

## Atomic handoff and Cursor prompt

1. Keep the passing gate/scanner/caller/tests/docs as one focused implementation
   change; preserve the captured unrelated dirty baseline and private exclusions.
2. Re-run the four exact focused suites above, compilation, README check, then
   install/status and check the current candidate without making a live test commit.
3. If later authorized to commit, review and stage only attributable safe hunks,
   keep this plan with them, and let the active gate block unsafe candidates.

Paste-ready Cursor prompt:

> Review `prompts/pre-commit-privacy-gate.md` and
> `plans/pre-commit-privacy-gate.md`, then inspect the implemented privacy gate,
> shared history scanner, checkpoint caller and regressions. Preserve all existing
> pending work. Re-run the four documented focused suites and verify the installed
> scanner with status. Treat current candidate findings as blocking; inspect and
> repair only explicitly authorized contents locally. Do not echo matched values,
> stage unrelated work, bypass the gate, make a live test commit, or push. Report
> evidence and any scope gap before changing enforcement.

### Portable postmortem metadata warning

The operational report hash is reviewed with an explicit no-new-learning decision
in the tracked memory ledger. Its alias uses the existing neutral public prefix,
not a live machine home path. The required targeted postmortem-memory check was
run: the earlier real-path record passed (exit 0), then the final privacy-safe
neutral alias caused exit 1, `unregistered_aliases`, with no changed hashes or
schema errors. Outstanding: the existing memory helper needs a separately scoped
private mapping between neutral public aliases and local source paths. Do not
publish the actual home path just to clear that warning. No private rules/settings
were added to public source; the remaining warning does not affect enforcement.

Completion title update encountered an unavailable local transport; the original
objective title remains. This did not affect enforcement or verification.

## Follow-up: make reviewed public candidates actionable

User reported the 16-finding refusal and asked how to fix it. Exact-index triage
confirmed ten reviewed source/fixture findings, four public recovery-document
path findings, and two effective Git email findings. Preserve all unrelated
pending work and leave the index unchanged. No raw matches are printed.

- [x] Reproduce and classify the exact existing findings privately.
- [x] Observe RED: unchanged reviewed source blob blocked, exit 1.
- [x] Add exact path-reference/blob-SHA256/category approvals with public reasons;
  snapshot/validate the manifest and prove changed bytes still block.
- [x] Resolve Git identity using the user's answer and private mode-0600 rules;
  never add the actual identity to public source.
- [x] Add a reusable redacted status/verification path and clarify smoke docs.
- [x] Run regressions, refresh, reinstall and verify the live check/hook.

Ruling: immutable reviewed-content approvals are smaller and safer than guessing
whether arbitrary credential-shaped source expressions are public. There is no
directory-wide exemption. Any edit to an approved blob requires fresh review.
The pending identity choice blocks only identity-dependent work.


### Follow-up completed evidence

- Added 14 exact path-reference/content-SHA256/category approvals, reviewed
  independently against indexed bytes: ten code-reference/synthetic fixtures and
  four public Markdown recovery documents. No broad directory exemptions.
- Defining reviewed-source RED preceded implementation. Two further RED tests
  caught approvals suppressing explicit private rules; the fix separates public
  heuristics from private literal/path findings and applies private findings last.
  Identity approvals also cannot override explicit forbidden identity literals.
- User selected keeping the current identity and approving it explicitly as
  public. Only private external mode-0600 policy and local privacyGate.rules changed;
  user.name/email and all existing literal/path policy were preserved.
- `python3 tests/test_pre_commit_privacy_gate.py`: 45 pass, exit 0.
- `python3 -m unittest discover -s tests -p test_checkpoint_privacy_gate.py`:
  1 pass, exit 0.
- `python3 tests/test_audit_public_history.py`: 14 pass, exit 0.
- `python3 tests/test_second_brain_checkpoint.py`: 24 pass, exit 0.
- README gate: pass_no_change, exit 0; compilation/focused whitespace checks pass.
- Reinstalled tested snapshot and ran refresh-config successfully (exit 0).
- Final source check: PASS, exit 0. Installed status: active/current, exit 0.
  Actual `git hook run pre-commit`: PASS, exit 0. HEAD/index entries unchanged.
  Rules location verified external, permissions 0600. No real staging/commit/push.
- Reviewer verified exact hashes, public reasons, category-specific scope,
  unsuppressible LFS payload findings and private-rule precedence. No remaining
  high-confidence issue within scope.

The earlier 16-finding block is now resolved for the actual current index, not
merely documented as pending. Approvals intentionally become stale on any byte
edit; re-review the changed candidate rather than auto-refreshing approval hashes.
Other privacy detection/coverage/bypass limits and the unrelated journal fixture
warning remain. The public postmortem ledger still needs a separate private
mapping for neutral aliases; no real machine home paths were added to clear it.
The existing atomic handoff/Cursor prompt above remains applicable; rerun the
updated counts and treat any future findings as blocking. Suggested focused
follow-up commit: `fix: retain reviewed public privacy fixtures safely`.

Follow-up learning recorded as `local-privacy-reviewed-content-approvals` in the
tracked memory ledger and state-security reference. Report hash is current;
targeted `check --postmortem` ran and exited 1 solely for the known neutral-public
alias versus actual-local-path mismatch (no changed hash/schema errors). Private
machine paths were not published to suppress that warning.

## Authorized shipping milestone

The later explicit commit-plan-push request authorizes committing and pushing all
safe reviewed dirty work. The coordinated notification wait is complete and its
peer commit is preserved. This privacy milestone is the final group of the
series in plans/commit-dirty-series.md. Every earlier candidate passed the exact
index gate and normal installed hook; final privacy regression evidence remains
45+1+14+24 passing checks. Private identity approval stays outside Git.
