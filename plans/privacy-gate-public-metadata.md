# Allow public metadata in the commit privacy gate

Make ordinary home-path documentation, Git author/committer identities, and recovery-named source/docs eligible for commit. Add regressions before changing the shared gate, deploy its source and installed snapshots, then commit and push the policy change and the dependent Discord cap fix.

## Scope and decisions

- User explicitly authorizes these defaults and commit-session delivery. “Git creds” means the author/committer identity emails just discussed; actual authentication secrets remain blocked.
- Change only the commit gate, not the standalone historical auditor or migration scanner. Built-in home-path findings are permitted at the gate boundary, including local LFS payloads. Explicit private literal/path restrictions still override all defaults.
- Permit ordinary filenames containing recovery; preserve exact recovery/recoveries/backup directories and credential/vault/raw-run paths as private archive locations.
- Git identity metadata no longer needs a name/email allowlist. Keep legacy private policy validation compatible, preserve blob email detection, and continue scanning metadata for credentials/tokens and explicit private literals.
- Files: scripts/privacy_gate.py; tests/test_pre_commit_privacy_gate.py; canonical dot_agents/skills/commit-session/SKILL.md; README.md; docs/smoke-tests.md; this plan; incident/lessons; append-only feedback; scoped postmortem memory records/guidance. Preserve all baseline dirty files and hunks, including unrelated feedback, source ledger and state-security guidance edits.
- Baselines: status captured for both repositories before new writes. Existing Twitter cap candidate has ten staged session files; README outage footer and October 7 incident/prompt remain excluded. Use direct-write fallback where runner scoping cannot detect edits.
- Memory lookup: privacy gate home_path recovery identity matched local-privacy-reviewed-content-approvals. Exact private rule precedence and installed snapshot advice apply; the old metadata-only approval requirement is superseded by this explicit user policy change.

## Atomic plan

- [x] Write gate regressions and observe expected RED for home paths, public identity and recovery source/docs; retain actual-secret and explicit-private-policy cases.
- [x] Make minimum gate and commit-session instruction changes; update README and smoke expectations.
- [x] Run gate/history/checkpoint regressions, compilation, type checks if available, exact-candidate gate and independent review.
- [x] Apply managed skill update with refresh-config, preserving newer live sources and unrelated dirty work; refresh installed scanner snapshots as needed and verify actual checks.
- [x] Review and stage only current-session changes in each repository; include plans, lessons, incidents and scoped memory changes.
- [ ] Commit policy prerequisite, commit cap fix, then push each configured upstream once; record actual results and remaining live verification.

## Risks and rollback

Home paths and Git identities are intentionally public metadata under this policy; explicit private prohibitions remain authoritative. No blanket exemption for the content of recovery files: token/key/password and other private-content checks still run. Installed hooks use snapshots and require refresh after policy edits. Revert the focused source/skill change and reinstall to restore prior defaults. No history rewrite or credential changes.

## Verification and handoff

Pending. Commands: python3 tests/test_pre_commit_privacy_gate.py; python3 tests/test_audit_public_history.py; python3 -m unittest discover -s tests -p test_checkpoint_privacy_gate.py. Direct CLI checks use shared gate on the real cap candidate and disposable hooked repositories for negative secrets; never stage real secrets. Bot verification remains its 224-test suite and three preview scenarios. README and smoke checks must describe the final policy.

Cursor prompt: Read this plan and plans/keep-new-tweet-pair.md in the bot repository. Preserve unrelated staged/dirty work. Verify public home paths, Git metadata and recovery-named source/docs pass while actual secrets and explicit private policy block. Check installed snapshots before committing; keep each plan with its implementation and push only the configured upstream. Suggested commits: fix: allow public metadata in commit privacy checks; fix: preserve new tweets during paired cap cleanup.


Verification so far: seven intentional commit-rejection RED failures across home/recovery filenames, ordinary/author-option/environment identities and LFS; remaining secret/private-rule cases passed. After the change: 49 gate tests, 14 history-audit tests and one immutable-tree checkpoint integration passed (exit 0). Syntax compilation and scoped whitespace checks passed. Source gate passes both the staged cap candidate and current linux-config index. Basedpyright ran: one existing dynamic-import error/110 warnings versus HEAD's same error/114 warnings; no type-clean claim. Installed hook refresh and deployment still pending.


Activation evidence: refresh-config initially stopped at exact Kitty permission drift. Source/live bytes for all four drifted files matched; only reviewed file modes were reconciled via exact-target chezmoi apply, preserving unforced broad conflict checks. Retried refresh-config completed all phases, exit 0. Installed skill/scanner hashes match source; existing linux-config hook snapshot was refreshed, status is current, and actual hook passed with unchanged HEAD/index. No unrelated repository source changes resulted.

Independent reviewer verified all nine current behavior/security claims and found no implementation blocker. Original RED was worker-observed; full type-check baseline/current logs are retained privately at /tmp/privacy-policy-type-baseline.log and /tmp/privacy-policy-type-current.log. Existing import typing error remains and is reported rather than hidden. Historical auditor policy is unchanged.

## Delivery milestone — fix: allow public metadata in commit privacy checks

Session scoping helper cannot recognize writes from this runner, so direct-write evidence and the captured baselines define scope. Include only the gate, its defining tests, canonical commit-session skill, matching README/smoke/lesson/plan/incident, the newly appended durable preference and scoped postmortem guidance/ledger entries (including the earlier cap incident registration). Preserve all unrelated dirty feedback, ledger/guidance, desktop configuration, plans, prompts and incident edits. README recruiter-sync passes: hook/stack/navigation precede setup; documented check/install/status options and policy examples match observed source/runtime behavior. Rollback is a focused source revert plus snapshot reinstall.

Completed: policy implementation, tests, installed activation and review. Remaining: inspect exact staged candidate, privacy gate, policy commit, dependent bot commit and one push per configured upstream. Both repositories use main -> origin/main. No implementation blocker; Discord activation and the pre-existing type-check error remain outside this delivery.

Learning: report hash 482327c6d64888827a6d6697a46f4ca65fb5a2ddc1ae3376782c111b1ca744ab registered under local-gate-public-metadata-defaults; targeted checks passed for both the policy incident and cap incident with no errors or uncovered current aliases.


Final delivery note: staged-memory snapshot validation passes without including unrelated dirty memory records. A later broad refresh stopped on unrelated MIME mode drift (live0600/source0664; bytes match). Preserve the more restrictive live mode. The requested skill/scanner already match installed source and the existing hook snapshot is current; earlier full refresh and actual hook check passed. No pending privacy-policy activation blocker. Remaining broad-refresh MIME conflict is reported separately, not repaired by changing unrelated configuration.
