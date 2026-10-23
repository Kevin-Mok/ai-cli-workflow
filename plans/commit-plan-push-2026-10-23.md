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
- [ ] Commit reviewed incident evidence, references and ledger together.
- [ ] Commit repository-creation remote policy and matching durable preference.
- [ ] Run required refresh, review residuals and push the complete series once.

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
