# Shared postmortem memory

Create a compact troubleshooting skill backed by reviewed incident knowledge. Discover eligible sources, test the read-only helper, distill findings, add mandatory lookup and learning rules, then verify coverage and installed behavior.

## Purpose And Observable Outcome

Codex reads `$postmortem-memory` and searches before remedial actions for reported bugs or unexpected failures. New or materially updated postmortems have matching tracked knowledge during the same task. Search distinguishes verified fixes, workarounds, unresolved diagnoses, and activation pending.

## Current Context And Scope

Source intent is the supplied implementation plan and prompt, saved unchanged at `prompts/build-postmortem-memory.md`. Source of truth: `dot_agents/skills/postmortem-memory/`. Supporting surfaces: canonical `dot_codex/AGENTS.md`, skills catalog, root README, smoke tests, focused tests. Do not change metaprompt or original source incidents. Include ignored/historical external copies; deduplicate exact content, retain aliases.

Initial git status captured before writes in `/tmp/postmortem-memory-initial-status.txt`: protected modified `aliases/key_dirs.tmpl`, `docs/phone-ssh-public-ip.md`, and `docs/smoke-tests.md`; protected untracked five September/October incident reports, two plans, and a benchmark prompt. Append only separable smoke-test entries. Initial implementation authorization excluded commit/push; the subsequent explicit commit-session request authorizes scoped commit and upstream push. No worktree, timers, interception, or automatic repairs.

## Assumptions

- The user authorized execution of the supplied decision-complete plan; Default mode executes it with this ExecPlan (no available mode-switch tool).
- Ruling: preserve the already compiled prompt verbatim rather than optimize it again; metaprompt remains prompt authoring only.
- Agents review independent local/external corpora; helper discovery independently reconciles their output. Codex authors guidance; no keyword extraction pretending to be review.
- Private directories and personal-context names are excluded before reads; dependency/build/git directories and all symlinks are pruned. Explicit exclusions are documented.
- Findings carry status and evidence scope separately. Code verification never proves runtime activation. Original reports remain untouched.
- Standard-library CLI uses JSON structured output; exit 0 for successful scan/search (including no matches), exit 1 for incomplete check or unreadable discovery, exit 2 for invalid input/data.
- Tracked knowledge preferred by explicit location; installed fallback is read-only and never a mutation target.

## Implementation Checklist

- [x] Capture initial status, read policy/context, record startup failure immediately.
- [x] Delegate bounded independent source review and baseline evaluation.
- [x] Save prompt, define helper and workflow tests; observe expected RED.
- [x] Implement deterministic discovery, read-only search, ledger/reference/targeted coverage checks.
- [x] Review every eligible unique report, reconcile aliases, author eight topic references and ledger.
- [x] Add compact skill, metadata, canonical rules, catalog/README/smoke entries.
- [x] Execute agent replay comparisons and synthetic cross-repo learning check.
- [x] Run focused tests, workflow regressions/doctor, README gate, diff check.
- [x] Honor user-selected scoped deployment after ownership preflight, verify installed copies, reconcile incident updates.
- [x] Record final evidence/review/rollback and report outstanding limitations.

## Risks, Edge Cases, And Rollback

Exact-byte dedup does not merge similar versions. A revised hash requires fresh human review; copying an existing reviewed report still requires registering its alias. Unreadable paths and absent default roots fail visibly. Pruning private material is conservative, including personal-context incident filenames. Avoid absolute-source links interpreted as missing runtime dependencies by the doctor. Preserve protected dirty work byte-for-byte. Refresh snapshots live config and Git config, applies all targets, regenerates shortcuts and reloads fish; preflight must inspect snapshot ownership and diff before running it. If unrelated live divergence threatens protected work, report the blocked action. Rollback removes the new skill/tests/prompt/plan and restores only the new policy/catalog/README/smoke additions.

## Verification Evidence

RED and GREEN recorded below for `python3 -B tests/test_postmortem_memory.py`. Coverage: `python3 -B dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py scan` and `check`; targeted check for current task report. Existing checks: `python3 -B tests/test_ai_workflow_contract.py`, `python3 -B tests/test_ai_workflow_doctor.py`, doctor `--repo /home/example/linux-config --check`, README sync, `git diff --check`. Manual: cross-repository lookup and temporary synthetic report update via reusable fixture script. Agent evaluation: sandbox startup, stale patch, API mismatch, unfamiliar issue, before and after skill; measure order and recording, not statistical quality claims.

## Progress

2026-10-05: default sandbox startup fails before command execution; reviewed execution path works. Living report `docs/postmortem/2026-10-05-postmortem-memory-sandbox-startup.md` records workaround, unresolved host cause, and corrected catalog path. External reviewer initially finds 87 aliases/76 hashes; counts await scanner reconciliation.

## Review Notes

Implementation review and coverage are complete, with baseline push-policy assertion and metaprompt provenance failures recorded separately. Delivery now follows the explicit scoped commit-session authorization below.

RED evidence: `python3 -B tests/test_postmortem_memory.py` intentionally failed all 21 defining contracts because the helper and skill do not exist yet; full output in `/tmp/postmortem-memory-red.txt`. No production helper authored before RED.

Ruling: a verified remedy may have a supported root-cause explanation (for example an updater demonstrably repairs extraction without isolating its upstream change). Keep causal confidence separate from verified remedy; reject hypothetical causes or absent code/runtime evidence for verified_fix. Defining confidence regression observed RED, then validator adjusted without promoting unresolved reports.

Ownership decision: user explicitly chose to preserve repository settings and deploy only this task’s owned targets. Full refresh-config is superseded for this task because its snapshot would overwrite protected skip-worktree config (three differing setting keys). Use exact skill/policy/link targets, no snapshot or broad apply. Git live/source agree; snapshot dry-run passed.

Skill RED evaluation: five fresh no-skill agents each answered four scenarios (20 decisions). Lookup 0/20 and shared-learning updates 0/20; living reports and evidence/status distinctions 20/20. Missing required elements, not unsafe-diagnosis rationalizations, motivate explicit lookup and learning records.

Current GREEN: `python3 -B tests/test_postmortem_memory.py` passed 26/26 (exit 0); helper subset 24/24. Defining template/missing-source regressions and malformed-link diagnostics observed RED then GREEN. Standard-library helper and no-write snapshot smoke passed. `python3 -B scripts/smoke_postmortem_memory.py` printed PASS: cross-repo canonical lookup, stale hash rejected, reviewed update checked, activation_pending retained, fixture removed (exit 0).

Corpus: 177 exact-content unique reports / 264 aliases / 131 findings, with three explicit no-new-learning report decisions. 76 external reports/87 aliases, 94 current eligible local reports, 7 distinct historical local versions and their aliases. Seven local personal-context operational filenames and external private directories excluded conservatively before reads. No templates or plans/prompts/skills narrative were counted. Counts measure coverage, not independent incident recurrence. Full unique reads and independent hash/alias reconciliation completed.

Integration: workflow 12 tests/11 pass/one unchanged push-policy failure (exit 1); doctor tests 19/19 (exit 0); doctor audit same one metaprompt-provenance error and one duplicate-skill warning (exit 1), active instructions 13,624 bytes / ~3,405 character-estimated tokens. README gate pass_no_change (exit 0). Claude directory-link regression and isolated refresh-config regression both exit 0.

## Final Evidence And Review

Fresh final tests: 26/26 helper/workflow tests pass (exit 0); cross-repo synthetic smoke prints PASS (exit 0). Full `scan`/`check` pass with 179 unique content hashes, 266 aliases, 132 findings, four no-new-learning decisions and no new/changed/unregistered/missing/unreadable source errors. All five task-created living reports pass targeted checks (exit 0). This includes a concurrent task's reviewed kitty report; it was preserved and read, not authored here. The original source reports were not changed by this task.

Agent evidence: ten fresh agents, five controls/five with-skill reps across four scenarios (40 decisions). Lookup control0/20 vs with20/20; shared-learning/check prescription0/20 vs20/20. Both arms already pass applicability/status20/20. Actual retrieval executed; writes/remedies prescribed only. The smoke fixture and task-local incident updates prove actual author/check behavior. Extra with-arm output allowance and explicit skill availability limit causal/general claims. See `docs/troubleshooting-memory-evaluations.md`.

Final audit remains baseline-equivalent: one metaprompt-provenance error/one duplicate-skill warning; no new findings (exit 1). Latest active context is 14,760 bytes/~3,687 character-estimated tokens after another task added its title policy. Doctor regressions19/19 pass; contract11/12 retains only the expected push-policy failure. README gate pass_no_change; `git diff --check` passes (exit 0). No full unrelated suite or live application repair is claimed.

Deployment: user explicitly chose exact owned targets in place of conflicting full refresh. `chezmoi apply --no-tty --exclude=scripts ~/.agents/skills/postmortem-memory ~/.codex/AGENTS.md` exits0; all13 deployable package files and policy match installed bytes, and owned Claude directory link resolves. Final skill-only apply exits0; its fresh before/after protected hashes match. Python caches are deliberately excluded by .chezmoiignore. A concurrent writer changed the earlier Codex source baseline to match live settings; preserve current state and do not restore stale snapshots. This task did no source-config write, config snapshot or broad apply. The refresh regression is isolated under temporary HOME/TEST_CODEX_TARGET. Protected pre-existing work and concurrent source-policy/title additions remain untouched by scoped source edits.

Ruling: shared sources.json is now used by concurrent tasks. Preserve all their current records and explicit no-new-learning decisions; no stale initializer rerun. Future rollback must preserve independently added knowledge and policy hunks rather than delete the whole package or restore old source snapshots blindly. This implementation uses instructions and evaluated retrieval, without a runtime interception hook. Helper scan deliberately requires a valid reviewed ledger; search can work without originals, full coverage cannot.

## Atomic Delivery And Cursor Handoff

Implementation was initially delivered without stage, commit or push; the subsequent explicit $commit-session request authorizes only directly attributed scoped commit and upstream push. Eligible eventual task commit groups new skill/helper/knowledge, tests/smoke script, task-created reports, saved prompt, plan, evaluations, lessons and only related README/catalog/smoke/policy hunks. Preserve pre-existing smoke and title-feature changes plus another task's report ownership; inspect scoped hunks and refresh source attribution before staging. Suggested subject: `feat(skills): add shared postmortem memory`.

Paste-ready Cursor prompt:

```prompt
Review the implemented shared postmortem memory in /home/example/linux-config. Read plans/postmortem-memory.md and dot_agents/skills/postmortem-memory/SKILL.md, then inspect the helper, ledger and topic references. Preserve existing/concurrent dirty work and shared learning. Run python3 -B tests/test_postmortem_memory.py, python3 -B scripts/smoke_postmortem_memory.py, the documented full/targeted coverage checks, existing workflow checks, README gate and git diff --check. Keep baseline push-policy and metaprompt-provenance failures separately attributed. Do not stage, commit, push, create a worktree or overwrite protected config. For any newly found issue, consult memory before remedies, reproduce it, update its living report and tracked learning, then run targeted coverage.
```

Exact manual check: from another repository run the canonical helper search for bwrap loopback; it must return the workaround and applicability/source references. Run `python3 -B /home/example/linux-config/scripts/smoke_postmortem_memory.py` to perform the isolated changed-report update/check (no sudo). For installed fallback verification use `search "bwrap loopback" --knowledge /home/example/.agents/skills/postmortem-memory`; never write the installed ledger. Public docs updated: rootREADME, local skills catalog, smoke tests, workflow/reference package, evaluation record and this plan.

## Session Delivery (2026-10-05)

User now authorizes commit-session. Branch main, upstream origin/main, push URL user@example.invalid:example-user/ai-cli-dotfiles.git. Session01a10c85-5c59-7fa1-b9b0-8f01285c293f: session_scope returns unsafe with no detected writes/baseline. The saved actual pre-write status and successful conversational write evidence establish fallback scope; no timestamp attribution. Existing local-session-attribution-direct-evidence guidance applies. Living scope-helper report and its tracked review decision are added in this same task.

- [x] Read commit-session, run required helper, inspect actual initial state and directly observed writes.
- [x] Define own whole files and separable README/instruction/smoke hunks.
- [x] Run fresh focused checks/README gate; stage and independently inspect exact scope.
- [x] Finalize attribution workaround report/ledger; targeted coverage exits0 and scoped installed sync matches all13 files without protected source/config changes.
Delivery sequence after this verified source snapshot: commit related implementation/docs/plan together, push origin/main once, then verify actual commit scope, remote equality and protected residual work. Report the actual SHA and results in the delivery response; no remote success is claimed in advance.

Scope includes all13 non-cache skill files; this session's helper tests, reusable smoke script, evaluations, saved prompt, six task-created living reports, plan, catalog/lessons additions, and three mixed-file selections. Raw prior reports, phone SSH files, alias changes, Kitty i3 config and title-feature policy/README/smoke/plan/report stay out. Initial curated knowledge includes a current Kitty report read/reviewed by this session: preserve that metadata as source coverage, while its independently authored original report stays uncommitted. External and untracked source metadata are inputs to this knowledge task, not authorization to ship raw sources.

Staged 29 paths. Mixed-file index blobs contain current HEAD plus only directly observed own additions in README, policy, smoke and lessons; no mixed working file was replaced. Four mixed-file and protected source/config before/after hashes matched. A concurrent Kitty plan edit was recaptured and preserved. Re-read the current Kitty report and its matching diagnostic-workaround finding as corpus inputs; preserve its learning metadata without staging its original report or foreign lesson. Latest full coverage is 180 hashes / 267 aliases / 133 findings / four no-new-learning decisions, including this session-scope incident. Fresh focused tests26/26, synthetic smoke, README pass_no_change and staged whitespace checks pass. Retain skip-worktree config and all foreign dirty work. Suggested single commit remains feat(skills): add shared postmortem memory.

Final scoped review: independent reviewer and root inspect the same29 staged paths, including the four mixed-file selections. No cache paths, private report aliases or credential signatures were found. Source/report metadata is intentionally curated input; raw prior reports and foreign implementation/docs/lessons remain excluded. Commit and remote verification happen after this plan snapshot, with actual results reported in the delivery response.
