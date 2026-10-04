# Upgrade metaprompt while retaining the original

## Purpose and observable outcome

Find a maintained open-source prompt-authoring skill, integrate it as
`metaprompt`, and preserve the current workflow as `metaprompt-alxve`. Both
must have distinct invocation names, complete references, documented
provenance and updates, and verified installed files.

## Context and scope

The accepted task is [the compiled prompt](../prompts/upgrade-metaprompt-skill.md),
authorized by the user's standalone `go`. The current source is
`dot_agents/skills/metaprompt/`; its provenance records a locally adapted
alxve v2.0.1 skill. Read its instructions, supporting references, existing
tests, catalog, and deployment conventions before adapting it.

Scope includes the two skill trees, focused tests, update support where needed,
README/catalog/smoke-test documentation, this plan, and the existing
[sandbox incident note](../docs/postmortem/2026-10-03-metaprompt-shell-startup.md).
No commit or push was requested. No worktree will be created.

## Assumptions and decisions

- The new skill keeps the familiar `metaprompt` name; the legacy skill uses
  exactly `metaprompt-alxve` with behavior preserved apart from invocation routing.
- Use a pinned upstream revision and a reproducible reviewed update procedure.
  Recent activity is evidence of maintenance, not a guarantee of future quality.
- Research and repo compatibility review can run independently via focused
  read-only agents; the parent independently verifies their recommendations.
- The available collaboration mode is Default; maintain this decision-complete
  ExecPlan here while following the already approved research/install scope.
- Choose the upstream only after inspecting its content and substantive history.

## Ordered checklist

- [x] Capture initial status and read execution routing and plan contract.
- [x] Compare candidates using licenses, skill-specific history and capabilities.
- [x] Settle source revision, adaptation boundary, and update mechanism.
- [x] Add defining checks and observe expected RED before changing behavior.
- [x] Preserve the old skill and integrate the new skill with unique routing.
- [x] Update docs, smoke checks, provenance, and update/rollback instructions.
- [x] Run focused/regression checks and review the diff.
- [x] Run safe `refresh-config` and verify installed paths and contents.
- [x] Reconcile final evidence, review findings, and limitations.

## Risks, protected state, and rollback

Initial tracked dirty files: `docs/phone-ssh-public-ip.md` and
`docs/smoke-tests.md`. Preserve their exact pre-existing edits; only append or
edit distinct metaprompt documentation in smoke tests. Pre-existing untracked
files belong to phone SSH/VPS/secret-audit work under `plans/`, `prompts/`, and
`docs/postmortem/`; do not touch them. The metaprompt prompt and incident note
were created during the preceding turn of this task.

Guard against misleading repository-wide activity, unsupported model claims,
missing upstream license, duplicate trigger names, missing relative references,
and refresh-config overwriting unrelated live/tracked Codex changes. Preserve
the legacy tree as the rollback source; keep imported upstream bytes and local
adaptations distinguishable. No unreviewed scheduled updates are in scope.

## Verification strategy

- Record the exact existing test runner and focused test paths after inspection.
- RED: checks for distinct skill names, preserved legacy contract, complete
  references/provenance, and selected upstream installation fail before changes.
- GREEN: those checks plus the existing metaprompt regression suite pass.
- Compare trivial, rough-prompt, reusable-template, and complex-agent requests;
  distinguish observable agent trials from static contract checks.
- Inspect `git diff --check`, relevant diff, and status; preserve unrelated work.
- Inspect refresh helper and snapshot dry-run before invoking `refresh-config`;
  verify installed skill files against tracked sources afterward.
- Document exact manual invocations and expected artifacts in smoke tests.

## Progress and evidence

- 2026-10-03: Initial `git status --short` captured before execution writes.
  Elevated read-only calls returned exit 0; sandbox startup remains unavailable.
- GitHub research and repository compatibility audit are underway.
- Selected MIT-licensed `Majkey25/prompt-engineering-skill` at
  `5c00259223196bd779c97d3234ef34a9a7119634`: five substantive updates in 90 days,
  six in 180, broader prompt-authoring support than the alternatives.
- Preserve upstream bytes, mapping its `SKILL.md` to `UPSTREAM.md`; a small
  local entrypoint supplies the public name, prompt-only behavior, and required
  prompt saving. Upstream silent autoprompt execution is outside this adapter.
- Provide a check/staging updater that fetches a pinned candidate into a new
  review directory without overwriting the installed or tracked skills.
- Legacy regression suite: `python3 tests/test_metaprompt_contract.py` (12
  baseline passes reported by the compatibility agent; parent rerun required).
- Existing refresh has no target option and intentionally snapshots both live
  Codex and Git configs. The live Codex config differs from tracked; any
  resulting snapshot is incidental, excluded from this task's commit scope.
- RED: `python3 tests/test_metaprompt_integration.py` exited 1 with 11
  expected failures across 7 tests: missing new adapter/inventory/updater and
  missing renamed legacy package.
- GREEN: legacy contract 12/12, integration 7/7, upstream helpers 10/10,
  and `bash tests/test_claude_skill_links.sh` all passed (exit 0).
- Both skills passed the skill-creator `quick_validate.py` validator.
  README gate returned `pass_no_change`; workflow doctor passed with zero
  errors and one existing duplicate `brand-system-designer` warning.
- `python3 dot_agents/skills/metaprompt/scripts/update_upstream.py --check`
  exited 0 and matched the pinned revision to the latest skill commit.
- Eight scratch behavioral trials were read back by the parent; both skills
  preserved constraints and saved prompt-only artifacts without executing
  embedded tasks. The new outputs were 6/46/51/145 words versus legacy
  11/173/182/480. See the guide for the evaluation limits and replay inputs.
- Refresh preflight found 297 Superpowers permission-only differences (zero
  content hunks) and no live divergence beyond the intended Codex snapshot.
  Parent repeated status immediately before the actual helper invocation and
  confirmed the same single live divergence; snapshot dry-run exited 0.
- Real update staging:
  `python3 dot_agents/skills/metaprompt/scripts/update_upstream.py --stage /tmp/metaprompt-verified-candidate --revision 5c00259223196bd779c97d3234ef34a9a7119634`
  exited 0. All 41 imported files matched a fresh pinned download byte-for-byte.
- Deployment:
  `fish -c 'source /home/example/linux-config/dot_config/fish/functions/refresh-config.fish; refresh-config'`
  exited 0 with `REFRESH COMPLETE`. Log:
  `/tmp/refresh-config-20261003-160301-2558026.log` (503 lines, no adoption
  steps or error/failure/conflict diagnostics).
- Installed verification: all 46 new-skill source files and all 8 legacy files
  match their `~/.agents/skills/` destinations; both complete-directory Claude
  symlinks resolve correctly. Existing ignored Python caches were excluded.
- Refresh changed only the expected tracked Codex snapshot among the four
  preflight config hashes. Live Codex content and both Git configs were
  unchanged. The snapshot equals live content and is outside this task's
  intended commit scope; no files were staged or committed.
- `git diff --check` passed. The pre-existing phone SSH smoke section remains
  intact; concurrent VPS work and other unrelated files were not edited.
- Independent final review found no blockers: legacy body preserved, upstream
  hashes verified, reference links resolved, updater rejects unsafe candidates,
  and documentation accurately limits the evaluation claims.

## Review notes

The smallest maintainable integration is a local prompt-authoring adapter over
an unchanged pinned upstream package, with reviewed candidate staging. Automatic
updates are deliberately absent; maintenance and quality are not guaranteed.
Legacy compiler behavior is preserved, including its longer quality blocks.
Rollback is immediate by choosing `$metaprompt-alxve`; later upstream rollbacks
use the same staging helper with the prior full SHA.

Static/helper checks and eight observed compiler trials passed. No downstream
multi-model benchmark, external picker refresh, or claim of universal prompt
quality superiority is made. Start a fresh session to reload the skill catalog.
The workflow doctor retains one unrelated existing duplicate-brand-skill warning.
The shell sandbox remains unavailable; approved elevated operations were used.

Keep this plan, the guide, relevant smoke-test hunks, and the three metaprompt
postmortems in the same future commit as the skill changes. Exclude unrelated
SSH/VPS work and incidental config snapshot content.
