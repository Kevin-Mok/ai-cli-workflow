# Claude Code Router evaluation and integration

Evaluate the published router against this repo's two-agent workflow, then ship
a pinned, opt-in installation if it is safe and useful. Keep the review draft
local and leave live chezmoi configuration untouched.

## Purpose and observable outcome

The user's request is the specification: inspect upstream README/install/code,
both agents, security/telemetry/licence and existing overlap; install through an
idempotent pinned `run_onchange_` script and declarative safe config; document
tradeoffs in untracked `PR_BODY.md`; commit on the existing branch without push.
If clearly unsafe or fully redundant, commit a short docs note instead.

## Context and boundaries

Branch: `feat/tool-claude-code-router`. Relevant files: root README stack table,
`dot_claude/settings.json`, `dot_codex/config.toml`, Ponytail installer, cached
`github/feat/install-rtk` and `github/feat/codex-ponytail-plugin` refs, shared skill
catalog. No AGENTS changes, no branch/worktree creation, no chezmoi apply,
refresh-config (it applies chezmoi), GitHub push or PR creation.

Protected baseline, captured before edits with command-local LFS bypass:
`dot_agents/skills/last30days/assets/dog-original.jpeg` and the three MP3 files
`scripts/can-i-ask-you-a-question.mp3`, `scripts/Voice Contributor-celebrate.mp3`,
`scripts/Voice Contributor-intro.mp3`. Do not stage or alter them.

## Assumptions and decisions

- Installation does not imply routing every normal session. Provider/model
  choice and paid-provider keys are not supplied; preserve existing sessions.
- Compare the published npm artifact with main; do not assume current main
  advertising describes an older release.
- Prefer loopback, logging disabled, no credentials in Git, no hooks/MCP changes
  unless required. Evaluate security before settling the implementation.
- Read-only upstream research is authorized; delivery has no GitHub mutations.
- Default collaboration mode is fixed by the harness; maintain this ExecPlan
  without claiming a mode switch. User supplied concrete execution scope.

## Ordered checklist

- [x] Read instruction/plan contracts, preferences, lessons; capture baseline.
- [x] Inspect primary upstream docs, release artifact and execution paths.
- [x] Compare current repo and cached branch overlap; settle add/skip decision.
- [x] Write defining offline checks, observe expected RED if installing.
- [x] Implement pinned installer, safe declarative config and usage docs.
- [x] Write `PR_BODY.md` with all requested evaluation sections; keep untracked.
- [x] Verify idempotency, prerequisites, routing safety and chezmoi rendering
  without apply; complete README gate and source/security review.
- [x] Update plan, review incidents, stage only owned changes and inspect diff.
  Package the single local commit; report its resulting hash and three direct
  verification commands in the handoff.

## Risks, edge cases and rollback

Router intermediates prompts/keys; model conversion can change tools, reasoning
or cache use. Cheaper API models can increase retries and cost. Dependency pins
must be distinguished from a top-level version pin. Never overwrite local
credentials or activate persistent global routing. Test already-installed,
missing/old Node, failed install and existing conflicting binaries/configs.
Rollback removes only the new installation/config and ends opted-in sessions;
the existing agent defaults remain intact.

## Verification plan

Defining tests should execute the installer with strict command fixtures in a
temporary HOME/prefix and verify exact pinned argv, retries/no-op, no server or
agent launch and no settings writes. Inspect rendered chezmoi targets/config
without apply. If feasible run the pinned real CLI against a temporary synthetic
loopback provider with no paid credentials; do not treat that as quality/cost
verification. Run shell syntax and relevant regression checks, README gate,
staged secret/size review and direct workflow checks. Record exact results here.

## Progress, evidence and review notes

Initial `git status` hit read-only common Git LFS storage. Command-local filter
bypass completed exit 0; no repository Git configuration changed. See the
[environment incident](../docs/postmortem/2026-10-13-router-evaluation-environment.md).
Primary upstream main now advertises both agents; published artifact research
and overlap analysis run as bounded read-only tasks.

### Final decision and evidence

Recommendation: add as an installed/unstarted opt-in trial. Published npm 3.1.3
supports both agents; verified SHA-512 is in the installer. Source-to-bundle
reproducibility and the floating transitive dependency graph are not proven.
No existing tool duplicates routing: Ponytail is merged; cached RTK branch
`14cbb59f` is not, and compresses shell output rather than routing providers.

- `python3 -B tests/test_claude_code_router.py`: defining seven checks RED
  before implementation (missing installer); final nine checks GREEN, exit 0.
  Covers private prefix, exact release/checksum boundary, repeat no-network
  install, old Node/missing npm, intentional hash/npm failures, plain output,
  wrapper catalog/host/version and real chezmoi seed mapping/0600/create-only.
- Create-file attribute ordering RED exposed the wrong target filename;
  corrected `create_private_config.json` passes real chezmoi dump/diff checks.
  Isolated source omits unrelated external templates; no apply was run.
  Final isolated-source `managed` output contains only the new seed, launcher
  and install script; `ignored` prints `PR_BODY.md` as intended.
- `python3 -B scripts/smoke_claude_code_router.py --package-dir
  /tmp/ccr-runtime-3.1.3/node_modules/@musistudio/claude-code-router`: exit 0.
  Actual pinned CLI/native SQLite, temporary HOME, help/version, management
  startup with disabled gateway, safe config migration/persistence, invalid
  token 401, no Claude/Codex files and cleanup. Loopback needed scoped approval.
- `bash -n run_onchange_after_install-claude-code-router.sh.tmpl
  dot_local/bin/executable_ccr`: exit 0.
- `bash tests/test_claude_skill_links.sh`: exit 0, neighboring shared-skill
  integration unchanged.
- `./scripts/executable_readme-recruiter-sync`: `pass_no_change`, exit 0 after
  adding the truthful stack row/onboarding link.
- Ancillary `python3 -B tests/test_postmortem_memory.py`: 25/26 pass; shared
  full-corpus `test_actual_ledger_reference_status_and_coverage` fails on
  external incident coverage. Report as a warning, not a router regression.
- Canonical postmortem-memory targeted `check --postmortem` for this report:
  exit 0, no errors/new/changed/missing aliases. Reviewed hash/explicit
  no-new-learning decision appended in this branch and canonical ledger,
  preserving the canonical checkout's pre-existing dirty entries.

### Review notes and validation limits

Independent bounded source review found no blocking issue; reviewer reran nine
tests successfully. Clarified that `ui --no-gateway` reuses existing daemons and
does not stop a running gateway. SQLite takes precedence over first-run JSON;
existing installations remain user-owned, not automatically hardened. New
profiles must use `ccr` scope. No ongoing SQLite policy enforcement is claimed.
Wrapper suppresses catalog refresh, not all possible provider/UI network calls
or the agents' own telemetry. Runtime credentials can be plaintext on disk.

Paid requests, actual agent profile launches, cost/latency/quality, streaming
and tool fidelity, browser traffic and full CVEs remain unverified. Live
installation/activation is deliberately pending the user's later apply.

### Atomic follow-up and Cursor handoff

There is one delivery unit: pinned installer + launcher + first-run seed +
tests/smoke helper + README/operator/smoke docs + matching plan/incident review.
Keep `PR_BODY.md` untracked. Suggested subject:
`feat(ai): add opt-in Claude Code Router`.

Paste-ready Cursor prompt:

```text
Read plans/claude-code-router.md and docs/claude-code-router.md. Review the
committed opt-in CCR 3.1.3 integration without chezmoi apply, refresh-config,
push or PR creation. Preserve existing agent/CCR credentials and databases.
Run the documented offline checks and isolated management smoke test. Report
the shared corpus warning separately. Only with explicit provider-trial
authorization, use a disposable Only opened from CCR profile to compare
quality, streaming/tools, latency and total cost including retries against
direct agent use; update docs/smoke-tests.md and this plan with evidence.
```

## Delivery milestone

Milestone subject: `feat(ai): add opt-in Claude Code Router`. Research,
implementation, docs and focused checks are complete; review has no blocking
findings. Shared corpus coverage is a validation warning; activation and paid
evaluation remain future work. The staged owned-file diff passes whitespace
checks and excludes all baseline media and `PR_BODY.md`. This single milestone
packages the completed implementation and matching docs/plan for local delivery;
the resulting hash is reported by Codex after committing. Next step is the
user's later push/PR workflow, then deliberate installation/provider evaluation.
No push or activation is authorized here. `PR_BODY.md` remains untracked.
