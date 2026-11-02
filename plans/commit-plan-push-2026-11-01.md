# Deliver reviewed dirty worktree

Review existing changes, commit coherent groups with their documentation, and push the complete verified series once to origin/main.

## Scope and decisions

Initial state: main tracks origin/main; no staged files. All initial dirty paths are authorized for review, preserving unsafe or machine-local content. No product implementation is added by this delivery task. Shared README and smoke-test hunks are assigned to their related groups. Existing plan evidence describes earlier runs, not checks performed here.

## Ordered checklist

- [x] Capture initial status, branch, upstream and diffs.
- [x] Run backup, startup, skill contract, admission and README checks.
- [x] Review and prepare separate backup, skill routing, review policy, startup, desktop and learning candidates; privacy gates govern publication.
- [x] Run refresh-config for tracked configuration and record actual result.
- [ ] Push once and inspect final worktree and upstream state.

## Verification and risks

This turn: backup49 tests, commit-skill5 tests, admission7 tests and startup shell check passed. README gate: pass_no_change. Privacy check is required immediately before each commit. No actual backup/restore, desktop restart or disposable-repo agent evaluation is claimed. Existing changes can be reverted by a future ordinary revert; history is never rewritten. Machine-local fields and private source material must stay unshipped.

## Milestones and review

Commit subjects and verification will be recorded here before each related commit. Push remains pending.

Milestone 1 prepared: `fix(backup): exclude disposable Snap caches`. Backup source, both policies, regression, README/smoke docs and historical incident/plan travel together. Fresh49 backup tests passed; direct excludes preview passed. refresh-config completed successfully this turn. Other groups and one final push remain pending.

Milestone1 committed as c8025b0; both explicit privacy gate and active hook passed. Milestone2 prepared: `fix(skills): execute commit-plan-push on invocation`. Matching contract, catalog, README, smoke/admission documentation, plan and incident registration included. Fresh5 contract and7 admission tests passed; explicit planning-only safeguard retained. Next review policy, startup, desktop and learning groups; push pending.

Milestone2 committed as05473c8. Milestone3 prepared: `docs(review): require current-main integration before testing`. Existing user preference and matching canonical rule are reviewed together; no PR integration is performed by this delivery task. Scope is a single review control; no new skill/duplicate procedure introduced. Lean review: value5/5, uniqueness1/2 (specializes review freshness rather than general verification); rule adds487UTF-8bytes including its blank line, estimated121.75recurring tokens, score9.03; PASS for explicit requested control, privacy reviewed. No behavior/test claim beyond previously passing contract/admission checks. Next startup and desktop groups, then reviewed memory.

Milestone3 committed as67cc53a. Its rule-size estimate above is corrected to the measured staged diff (487bytes). Milestone4 prepared: `fix(startup): use portable Ultron wallpaper helper path`. Startup source, shell regression, smoke instructions and helper-discovery incident/registration stay together. Fresh Bash syntax and shell regression passed; refresh-config succeeded but excludes scripts, so this does not establish new live startup-script deployment or desktop acceptance. Next desktop configuration and memory, then push.

Milestone4 committed as d2446b5. Six targeted current incident/ledger checks passed with zero errors or missing/unregistered sources. Wallpaper exists; installed startup script differs at its Redshift line and is preserved. Milestone5 prepared: `chore(desktop): refresh Vesktop appearance and MIME permissions`. The MIME source rename is byte-identical and uses chezmoi private-file semantics, not secret content. Vesktop plugin rename and appearance are retained; generated settingsSyncVersion remains only in the working file. JSON parses; refresh succeeded. New grouped smoke checks record manual desktop acceptance, which was not performed. Next sanitize public engineering aliases, preserve financial-project metadata privately, and deliver learning updates.

Milestone5 committed as289cf2b. Milestone6 prepared: `docs(memory): publish reviewed engineering incident learning`. Includes engineering findings, Coinbase paging guidance and reviewed incident registrations. Public candidates use neutral /home/example aliases, consistent with earlier delivery; private working aliases remain unchanged. Financial-project preflight metadata is excluded from the public ledger and preserved locally. Public review counters recomputed from exact report/alias counts. Six targeted report checks passed before the delivery-report wording update; its final hash is refreshed. Direct backup preview and historical plan restoration passed. No report establishes broader provider, financial or runtime guarantees. Final staged schema/privacy checks precede commit; one push follows.

Final candidate review: public ledger schema has297findings and zero schema/reciprocal-link errors (schema-only empty scan root; this does not verify external source files). A broad first exclusion removed two historical source links; validator rejected it, and the corrected projection preserves them while excluding only the newly introduced private preflight. The living delivery incident records that failure and its formatter error. No gate was bypassed. Public artifacts retain original external report hashes with neutral lookup aliases; real-path targeted checks cover six local reports. Working residuals expected after commit: five reference alias overlays, Coinbase reference alias overlay, sources.json private aliases/financial preflight metadata, and Vesktop generated sync timestamp. No remaining reviewable group is intentionally omitted. Final commit and normal push are gated next; actual SHAs, publication outcome and exact residual paths are reported in the delivery reply.
