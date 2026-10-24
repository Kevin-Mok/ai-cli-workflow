# Deliver reviewed dirty worktree

Review every dirty path, commit safe changes in coherent groups, and push the
completed series once to the configured upstream. Preserve machine-local data
and record validation limits rather than guessing about runtime acceptance.

## Context, scope and decisions

Initial HEAD is `3e898a0` on `main`, tracking `origin/main` in
`Kevin-Mok/ai-cli-workflow` via the configured GitHub SSH remote. The index starts empty. All 23
initial dirty paths are reviewed; `:memory:.ses` is a machine-local session
marker and is excluded. No history rewrite or desktop manipulation is needed.

## Ordered checklist

- [x] Capture status, branch/upstream and applicable instructions before writes.
- [x] Inspect dirty docs, prompts, plans, policy, feedback and memory changes.
- [x] Independently review memory contracts; run README and focused smoke gates.
- [x] Commit restored working-directory paths in docs, prompts and their plans.
- [x] Commit reviewed incident evidence, references and ledger together.
- [x] Review repository-creation remote policy and matching durable preference for the final commit.
- [x] Attempt required refresh and review residuals; prepare one final upstream push.

## Verification and review

Fresh checks: `python3 scripts/smoke_postmortem_memory.py` exits 0;
`./scripts/executable_readme-recruiter-sync` exits 0 (`pass_no_change`);
ledger `check` against an empty temporary root exits 0 with 253 findings and no
contract errors. This validates reference/ledger consistency, not the external
source corpus. Scoped whitespace check exits 0. The memory review found 17 new
findings, two updated findings and reviewed source reconciliation. The three
changed local incident reports must pass targeted current-hash checks.

Immediately before each commit run `python3 scripts/executable_privacy-gate check`
against the reviewed staged candidate; scanner errors and findings block that
candidate. Preserve active hooks. Verify committed file scope and messages.
Run `fish -c refresh-config` for tracked managed changes; preserve newer live
files and stop on conflicts. Do not claim activation from source-only checks.

## Risks, rollback and protected state

Absolute paths and executor IDs restored in existing docs are ordinary metadata;
the mandatory privacy gate remains authoritative. External report aliases may
be unavailable or sanitized, so full-corpus coverage is unverified. No binaries
or files above 3 MB are expected. Preserve the session marker without staging
or deleting it. Rollback uses a new reviewed revert, never reset/amend.
The first privacy scan caught SSH-remote syntax in this task-owned plan as an
email; replace it with the repository name without changing scanner policy.

## Milestones

Documentation commit `349b65d` is verified; no push yet. Four targeted local report checks passed
before interruption (exit 0). Required refresh was attempted
with normal scoped approval and stopped (exit 1) on a pre-existing
`.config/mimeapps.list` conflict/EOF. No forced overwrite or shortcut regeneration.
Next: staged privacy review and commits. Helper discovery mistakes and their
existing-memory applicability are recorded in the matching delivery incident.

### Milestone 1 candidate: documentation paths

Prepare `docs: restore working checkout paths` with the nine reviewed docs,
prompts and existing plans plus this delivery plan. These are path-only
corrections; runtime behavior is unchanged. README gate and focused memory smoke
passed before interruption. Staging requires scoped approval because `.git` is
read-only in the sandbox. Commit only after a fresh staged privacy gate passes.


### Milestone 1 result and milestone 2 candidate

Milestone 1 completed as `349b65d`: ten intended paths, explicit and hook privacy
checks passed, no residual staged paths. No runtime changes. Next: memory group.

Prepare `docs(memory): reconcile reviewed incident evidence` with three restored
local incident reports, browser/grid/tracker findings, reviewed aliases and the
delivery-environment incident. All 102 same-hash record changes are alias-only;
the three replaced hashes match their modified report bytes. No finding was
removed. Run the exact candidate gate; external source corpus remains unverified.


### Milestone 2 result and final policy candidate

Milestone 2 completed as `694fc55` with exactly 13 intended paths and no residual
staging. Fresh memory smoke, 253-finding ledger contract check, four targeted
report checks and whitespace checks all exit 0. Explicit and hook privacy gates
passed. Full external corpus was not scanned.

Prepare `docs: preserve checkout when creating GitHub repos` with the existing
canonical-policy addition, its matching feedback preference, and this plan.
Review confirms it requires the newly created repository as origin, verified
fetch/push URLs, and retention of the current checkout. No scripts changed.
README gate remains pass_no_change; configuration activation was attempted and
stopped on the preserved pre-existing mimeapps conflict. Do not retry/force it.

After this candidate passes its staged gate and commits, check final commit scope
and residuals, then push `main` to `origin/main` once. Actual final SHA and push
result must be verified and reported in the delivery response; at this plan's
commit boundary that push has not yet run. Expected residuals are
`:memory:.ses` (machine-local session data) and two concurrently added policy
lines in `dot_codex/AGENTS.md` (UI copy and UX/DX/AX preferences), which appeared
after the reviewed baseline and remain outside this delivery candidate. No further source changes
or runtime tests are needed for the documentation-only policy addition.


The final staged diff exposed two concurrent policy additions before the privacy
check finished. Deliberately interrupted that check before any commit; exclude
only those two lines from the index while retaining their exact working bytes.
The final commit must contain only the previously reviewed repository-creation
hunk, feedback preference and plan. Do not claim a clean worktree.
