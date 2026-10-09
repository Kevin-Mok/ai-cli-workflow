# Single-line command policy: task verification failures

The default command runner failed before the preference-update task could read
repository context. Approved scoped execution unblocked the task; the default
sandbox remains unresolved and host repair is outside this task.

- Symptom: `pwd` and
  `cat /home/example/.agents/skills/superpowers/using-superpowers/SKILL.md`
  each exited 1 before command launch with
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: those command bodies did not run and caused no repository changes.
  Initial context reads were delayed; existing dirty work was preserved.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR` in the tracked
  postmortem-memory helper. Findings `ext-sandbox-loopback` and
  `local-sandbox-loopback-approved-route` both have `verified_workaround`
  status and `workaround` verification scope. Their startup-error and approved
  execution evidence applies because both independent harmless commands failed
  with the identical pre-launch error.
- Cause: the evidence supports denial of Bubblewrap loopback initialization in
  the runner. The underlying host policy or configuration was not investigated.
- Workaround and verification: approved `require_escalated` source reads,
  `git status --short`, `rg` inspection and Python reads executed with exit 0.
  This verifies scoped alternate execution; it does not prove default-sandbox
  recovery. No default-route retry or host-security change was performed.
- Status and next steps: continue the authorized preference update through
  approved scoped execution. Default sandbox startup remains unresolved and
  requires separate host investigation if repair is requested.
- Learning: no new reusable learning. The identical startup symptom, successful
  scoped workaround and unresolved default route are already covered by
  `ext-sandbox-loopback` and `local-sandbox-loopback-approved-route`. Register
  this fully reviewed report with an empty findings list and check its current
  hash/alias using the targeted postmortem-memory check.

## Unrelated workflow-contract baseline failure

- Symptom: `python3 -B tests/test_ai_workflow_contract.py` ran 12 tests;
  11 passed and `test_push_policy_is_consistent_in_active_workflows` failed
  because `dot_agents/skills/commit-dirty/SKILL.md` lacks the asserted exact
  `PUSH_POLICY` sentence. These commit skills and the assertion are untouched
  by this task; the separate fish syntax parse passed with exit 0.
- Lookup: searched `push policy exact literal stale workflow contract` using
  the tracked helper. Finding `local-push-policy-baseline-contract` at
  `references/artifact-verification.md#local-push-policy-baseline-contract`
  records an unresolved baseline with confirmed diagnostic evidence and no
  verified remedy. It applies to the same exact-literal workflow assertion.
- Diagnostic evidence: the parent verified inspected commit-skill files equal
  HEAD byte-for-byte. The exact literal is absent in both HEAD and the working
  tree for `commit-dirty` and `commit-session` SKILL/openai.yaml files and is
  present in `commit-plan/SKILL.md`. The assertion failure therefore predates
  this preference update.
- Impact and status: this broader check cannot establish a green full workflow
  suite. The pre-existing mismatch remains unresolved; no commit skill or test
  was changed. Report the limitation and repair it only in separately
  authorized work.
- Learning: no new reusable learning; the confirmed baseline mismatch and
  separate-scope repair boundary are already covered by
  `local-push-policy-baseline-contract`. The report's ledger decision retains
  an empty findings list and cites this finding alongside the sandbox findings.

## Optional installed-feedback verification assumption

- Symptom: a post-refresh Python comparison verified
  `~/.codex/AGENTS.md` matches the tracked source, then raised
  `FileNotFoundError` for `~/.agents/skills/feedback-memory/feedback.log`.
- Impact: the read-only verification stopped at an assumed installed log path.
  This is a verification assumption failure, not an application or config
  failure. `fish -c 'refresh-config'` already exited 0 with `REFRESH COMPLETE`.
- Cause and status: the check incorrectly assumed an installed feedback-log
  copy is required. The feedback skill resolves the canonical repository log
  first; an installed copy is not required and must not become a second writer.
  Verification was corrected to inspect the canonical log and installed
  SKILL resolution policy. No feedback copy or unrelated file was created.
- Lookup: searched `feedback log canonical installed missing path verification`
  with the tracked helper; search exited 0. `ext-optional-path-discovery` at
  `references/paths-ownership.md#ext-optional-path-discovery` broadly applies
  to an assumed optional path. `ext-missing-shared-feedback-path` describes a
  narrower layout issue and does not apply because the canonical log exists.
  The authoritative `feedback-memory/SKILL.md` explicitly prefers the repository
  log and prohibits maintaining a second log when that path exists.
- Corrected verification: the parent's checks exited 0. Installed
  `~/.codex/AGENTS.md` matches its source exactly; the canonical feedback log
  starts with all before-edit bytes plus the new appended formatting entry;
  installed `~/.agents/skills/feedback-memory/SKILL.md` contains the canonical
  repository-log resolution path. The optional installed log is irrelevant and
  `dot_codex/config.toml` is unchanged by the successful refresh.
- Learning: no new reusable learning. Existing optional-path guidance and the
  authoritative canonical-log policy already cover the mistaken assumption;
  no additional finding or reference rewrite is needed.
