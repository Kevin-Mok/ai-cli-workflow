# Alpha Digest Intro

Save the supplied six-hour bot introduction verbatim, verify its required
sections, and deliver a feature-branch PR. This plan records the isolated
change, test evidence, and delivery boundaries.

## Outcome and scope

- Add `prompts/alpha-digest-6h-intro.md` with a short purpose header for the
  AI Twitter Alpha six-hour scan and the exact supplied prompt body.
- Add `tests/test_alpha_digest_intro.py` using the existing unittest contract
  pattern, and document artifact review in `docs/smoke-tests.md`.
- Record the discovered baseline regression in its postmortem and register
  the reviewed report in the tracked postmortem-memory ledger.
- Work only in `.worktrees/alpha-digest-intro` on `feat/alpha-digest-intro`,
  created from fetched `origin/main` at `4366ee0`.
- Preserve the main checkout's unrelated changes. Do not apply configuration,
  touch secrets, push main, force-push, or bypass hooks.

## Decisions and risks

- No general prompts test exists; use a tiny file/nonempty/section-marker test.
- The five markers are `Collect.`, `Filter.`, `Admission filter`, `Report.`,
  and `open a PR for`. A separate exact-body comparison will verify the copy.
- Neither `dot_agents/skills/lean-instructions/references/vetted-skills.md`
  nor `docs/skill-admissions.md` exists on `origin/main`. Keep the supplied
  references and disclose this in the PR instead of creating those documents.
- This adds a saved prompt only; the external Grok Bot routine is not executed.
- Rollback is a normal revert of this additive change.

## Ordered checklist

- [x] Record protected main-checkout state; fetch and create the clean worktree.
- [x] Inspect prompt conventions, applicable instructions, and privacy hooks.
- [x] Write and run the defining test; observe missing-file RED.
- [x] Add the header and exact prompt body; observe GREEN and compare exact text.
- [x] Run related prompt contract tests and README audit; update smoke checks.
- [x] Review the final diff and stage only this task's files; pass privacy gate.
- [x] Commit with hooks, then publish the feature branch and open the PR to main
  as the post-commit delivery step (receipt belongs in the PR and handoff).

## Verification and review evidence

Run the new test with `python3 -m unittest discover -s tests -p
'test_alpha_digest_intro.py' -v`, expecting missing-file RED before the prompt
and one passing test afterward. Run the existing metaprompt contract and
integration modules as related regression checks. Compare the body against an
independent copy of the supplied text, including punctuation and line breaks.

Run `./scripts/executable_readme-recruiter-sync`, then the privacy gate against
the staged index, and keep the installed commit/push hooks enabled. Review
the saved Markdown as described in `docs/smoke-tests.md`. Confirm the PR's
base/head, remote commit, and unchanged main-checkout file hashes.

- RED: defining test ran before prompt creation, exit 1, one failure at line 11:
  `AssertionError: False is not true : missing alpha digest intro`.
- GREEN: same command after prompt creation, one test passed, exit 0.
- Exact copy: independent comparison found 2,163 identical body bytes, SHA-256
  `e557d676c04fc0fe8d090df8e11737f72deeb45de0da5bdbe854bf8842db01d4`.
- README gate: `./scripts/executable_readme-recruiter-sync` returned
  `pass_no_change`, exit 0. Privacy gate status is active and scanner current.
- Broader regression: `python3 -m unittest discover -s tests -p
  'test_metaprompt*.py' -v` ran 139 tests, 138 passed, one failed in unrelated
  host-context parsing. The same failure reproduces in a pristine base export;
  see [living incident](../docs/postmortem/2026-10-28-alpha-intro-regression-baseline.md).
- Directly related suites: `python3 -m unittest discover -s tests -p
  test_metaprompt_contract.py -v` passed 12 tests; the same command with
  `test_metaprompt_integration.py` passed 9 tests. Both exited 0.
- Review found no implementation issues; original RED evidence is recorded
  above. The final review also covers the baseline incident and ledger insertion.
- Postmortem-memory targeted check passed with no errors, new sources,
  changed sources, or unregistered aliases; exit 0. The registration preserves
  existing entries and records an explicit no-new-learning decision.
- Staged exact-index privacy check passed locally, exit 0, with no findings.
  `git diff --cached --check` passed; independent final review found no issues.

## Commit milestone

Milestone 1: `docs(prompts): add six-hour alpha digest intro` contains the saved
intro, defining test, smoke check, this plan, and the required baseline incident
record/ledger update. Prompt copy and directly related tests are verified;
the broader baseline failure is disclosed, with no unrelated runtime fix.
Staged review and the exact-index privacy gate are complete; commit hooks
will recheck the final candidate including this evidence update.
After the commit, push only `feat/alpha-digest-intro`, then create the PR to
`main` with the missing-reference and baseline-test notes. No blocking prompt
issues remain; the external routine remains untested.

Milestone 1 delivered: `16c01c18f2d26e12d24809f2758d6bc0419e5f59` committed
and pushed only to `origin/feat/alpha-digest-intro`, with index, commit, and
outgoing-history privacy PASS and no findings. PR
[#4](https://github.com/Kevin-Mok/ai-cli-workflow/pull/4) is open against main.
The initial SSH disconnect and successful gated retry are documented in
[the transport report](../docs/postmortem/2026-10-28-alpha-intro-push-transport.md).

Milestone 2: `docs: record alpha intro delivery recovery` records the verified
transport workaround, reviewed memory, and repo-specific lesson. No prompt,
test, runtime, or gate behavior changes. Finalize its ledger check and commit
with hooks, then push the documentation follow-up to the same PR. No further
implementation is needed; main-checkout dirty state remains protected.

Milestone 2 verification: transport-report targeted memory check passes,
exit 0, with no errors or uncovered/changed aliases. The reviewed source hash
is `3b23128e231d289bef51d52c2dfd564c9aac31c545a8b41b4bb6e8cad76ca2eb`.

Milestone 2 committed as `9989b4c` with privacy PASS. A final citation correction
uses the ledger's current reviewed hash instead of duplicating an outdated
abbreviation in guidance. This follow-up changes only that citation and this
record; both documentation commits will be pushed together to the existing PR.

Cursor review prompt: Review this additive prompt PR against the exact supplied
body and five required markers. Preserve all boundaries and unrelated work;
report the documented baseline regression without expanding this change.
