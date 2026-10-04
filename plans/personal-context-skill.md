# Personal-context chatbot

Build an explicitly invoked chatbot that learns through conversation and helps
example-user make development and design choices. Add a private structured memory
helper, keep personal information outside this repository, then validate and
install the skill without disturbing existing work.

## Purpose And Observable Outcome

`$personal-context` starts an adaptive discussion, asks one useful question at a
time, and connects answers to development choices. Meaningful learnings persist
privately with source, date, scope, and evidence labels. Ordinary coding requests
do not activate this skill. The approved handoff is
[`prompts/create-personal-context-skill.md`](../prompts/create-personal-context-skill.md).

## Current Context And Scope

- New source: `dot_agents/skills/personal-context/`, installed by existing chezmoi
  and Claude skill-link mechanisms. No installer redesign is needed.
- Private source: `/home/example/coding/personal-context`; human-readable notes
  remain source material. New machine memory is `ai-context/context.json` there.
- Canonical agent instructions, feedback-memory, and Second Brain currently
  overlap on personal context; add narrow routing/privacy exceptions.
- Update catalog, root README, smoke checks, synthetic tests, and this plan.
- Baseline captured before writes in `/tmp/personal-context-session-baseline.json`
  (status, HEAD, hashes of 1,235 tracked files). Pre-existing modifications:
  `aliases/key_dirs.tmpl`, `docs/phone-ssh-public-ip.md`, `docs/smoke-tests.md`.
  Preserve all pre-existing untracked postmortems, benchmark/SSH plans and prompt.
- `dot_codex/config.toml` has skip-worktree set and differs from the live file.
  Inspect the refresh snapshot before installation; preserve the existing flag
  and configuration, and attribute any required snapshot separately.

## Assumptions And Decisions

- User approved implementation of the final chatbot-first plan. No further
  design approval is required. No worktree, commit, push, or scheduler.
- Explicit invocation only, including routes from other skills; UI metadata sets
  `allow_implicit_invocation: false`.
- Auto-save direct statements and useful, clearly labeled interpretations during
  invoked conversations. Interpretations never silently become instructions.
- Seed only relevant source-backed context, preserving uncertainty and dates.
  Raw transcripts and detailed private appendices are outside default ingestion.
- Existing Markdown is preserved. JSON owns new structured learnings; source
  changes are checked selectively rather than automatically replacing memory.
- Root writes chatbot guidance/integration; a bounded agent owns the storage
  helper and its tests. Independent synthetic behavioral evaluation and a final
  code review complement the automated checks.
- Use this ExecPlan as the implementation ledger. The approved plan and repo's
  no-worktree/no-commit boundaries supersede generic skill workflow defaults.

## Interfaces

- Helper: `python3 scripts/context_store.py [--root PATH] read [--topic TOPIC]
  [--include-inactive]`, `validate`, or `update --payload -`.
- Default root is the external private directory. Test roots are synthetic
  temporary directories. The exact designated default may be its own private
  Git repository; linux-config, arbitrary Git roots, Git ancestors, and installed
  skills are rejected. The helper never stages or commits private data.
- JSON v1 contains revision/update metadata, entries, questions, and forgotten
  keys/question IDs. Entries distinguish `user_stated`, `source_reported`, `observed`, and
  `inferred`; interpretations are unconfirmed. Updates merge under a lock.
- New corrections supersede earlier entries for the same stable key; forgotten
  keys suppress automatic reimport. Failed validation preserves existing bytes.
- Source/schema reference is the exact contract for supported helper fields.

## Ordered Implementation Checklist

- [x] Capture baseline and reread relevant instructions/preferences.
- [x] Inspect actual private source names and existing memory routes.
- [x] Record synthetic baseline behavior before writing chatbot guidance.
- [x] Write defining storage tests, observe RED, implement minimum GREEN helper.
- [x] Author skill, explicit invocation metadata, and storage reference.
- [x] Add routing/privacy exceptions and update user-facing documentation.
- [x] Run synthetic conversational and storage regression scenarios.
- [x] Seed and validate the external store without copying personal data here.
- [x] Review independently and resolve material findings.
- [x] Safely run refresh-config and verify installed skill/helper/link.
- [x] Reconcile final diff, privacy, baseline protection, and evidence.

## Risks, Edge Cases, And Rollback

- Protect personal data across every artifact, log, prompt, test, and memory
  route. Synthetic fixtures and metadata-only validation results are sufficient.
- Source dates are evidence dates, not current confirmation. Follow current
  explicit instructions and project audience requirements over inferred taste.
- Missing data allows conversation from supplied context; invalid/unsupported
  stores are not overwritten. External permission failures have no repo fallback.
- Serialize concurrent writes, use atomic replacement, constrain paths, reject
  symlink/hardlink destinations, and keep store files private.
- Existing smoke-test modifications must remain intact. Installation can update
  unrelated config through refresh; inspect ownership and report actual effects.
- Rollback removes this new skill's installed files and reverts only this task's
  hunks. Preserve private memory unless example-user explicitly requests deletion.

## Verification Evidence

Expected automated checks: helper tests validate selective reads, provenance,
corrections, idempotency, forgetting, questions, invalid input, concurrent writes,
containment, permissions, and preservation on failure. Skill/integration checks
cover metadata and whole-directory installation. Exact commands:

```sh
python3 -B tests/test_personal_context_store.py
python3 -B tests/test_personal_context_skill.py
python3 -B tests/test_second_brain_skill.py
python3 -B tests/test_ai_workflow_contract.py
bash tests/test_claude_skill_links.sh
python3 /home/example/coding/codex-skills/skills/.system/skill-creator/scripts/quick_validate.py dot_agents/skills/personal-context
./scripts/executable_readme-recruiter-sync
git diff --check
```

Manual/behavioral checks: bare invocation asks a relevant question; a dilemma
guides follow-ups; learning preserves evidence labels; skipped topics stay
skipped; later invocation resumes usefully; unrelated tasks do not load private
context; life-derived preferences do not enter other memories; client design
requirements remain authoritative. Record actual executions and limitations.

## Progress And Review Notes

- 2026-10-04: Execution authorized. Planning inspection identified the private
  export's real filename and existing routing conflicts. No private values are
  reproduced in this plan or the saved handoff prompt.
- 2026-10-04: Planning-time shell startup failure prevented commands from
  executing; read-only escalation succeeded. Deferred failure record can now be
  saved under the implementation authorization.
- Complete: implementation, review fixes, private initialization, installation,
  and scoped verification. The existing broad push-policy test remains a known
  unrelated baseline failure. No commit or push was requested or performed.
- Synthetic baseline (executed by an independent agent before new guidance):
  a request to discuss motivations/handoff friction invoked Second Brain,
  proposed a ExampleProject outcome and confirmation gate, and planned a tracked
  profile summary. This violates the approved conversation/privacy contract.
  The baseline's exact gate was: "Shall we use this as today's ExampleProject
  outcome?" No actual profile or memory writes occurred.
- Baseline commands: `python3 -B tests/test_second_brain_skill.py` passed 11/11
  (exit 0); `bash tests/test_claude_skill_links.sh` exited 0. Broad
  `python3 -B tests/test_ai_workflow_contract.py` passed 11/12, exit 1, due to
  pre-existing literal push-policy drift in commit-dirty. See the linked
  [baseline record](../docs/postmortem/2026-10-04-personal-context-baseline-contract.md).
- Integration RED: `python3 -B tests/test_personal_context_skill.py` ran three
  cases and exited 1 because the new skill package/metadata were absent. Storage
  RED: `python3 -B tests/test_personal_context_store.py` ran 13 cases and all
  failed due to the absent helper (reported by its implementer; parent will
  independently verify GREEN). Both were deliberate defining tests.
- Parent independently verified initial GREEN: helper 13/13 and installed skill
  3/3 passed. Skill-creator validation, Second Brain 11/11, and diff whitespace
  also passed. Review then identified related-question forgetting and permission
  validation gaps; defining regression tests and fixes are in progress.
- Executed five synthetic conversational cases with a separate agent using the
  written skill: bare invocation, adaptive follow-up, temporary/forgotten answer
  and client-brand priority, unrelated parser request, and resumed invocation.
  Responses asked one relevant question, retained uncertainty, respected declined
  topics, and avoided other memory workflows. These were simulated responses and
  planned payloads, not live persistence or a statistical quality comparison.
- Refresh preflight: snapshot dry-run exited 0 without mutation. Live/source
  config differs on model, reasoning effort, and one trusted-project entry;
  values were withheld. Source is already different from HEAD under skip-worktree.
- Parent verification: all 19 synthetic personal-context tests passed; helper
  basedpyright reported 0 errors, 0 warnings, 0 notes. README check returned
  `pass_no_change`. External initialization then safely rejected its root before
  writing because that directory now has its own `.git` marker.
- Ruling: allow a Git marker only on the exact designated external default root;
  retain all other repository and containment guards. The earlier inspected
  source plan's non-Git assumption is stale, and the user's privacy boundary is
  linux-config, not a prohibition on the external source's own version control.
  Synthetic regression and minimal guard fix precede another initialization.
- Independent review accepted two additional findings: reject backdated
  distinct-ID user corrections and initialize exclusive temporary-file modes
  before validating them under restrictive umask. Focused RED/GREEN fixes are
  in progress; see the [review record](../docs/postmortem/2026-10-04-personal-context-storage-review.md).
- Final parent GREEN: `python3 -B -m unittest discover -s tests -p
  'test_personal_context*.py' -v` passed all 22 tests (exit 0). This includes the
  designated Git root, older corrections, restrictive umask, permissions,
  forgetting questions, and installed-layout regressions. `basedpyright
  dot_agents/skills/personal-context/scripts/context_store.py` returned 0 errors,
  0 warnings, 0 notes (exit 0). The reviewer found no other material issues;
  the parent inspected the exact root exception and review fixes.
- Private initialization succeeded (exit 0): revision 1, nine entries and three
  open questions, zero suppressed keys/IDs. The external Git status was captured
  before the write. Every existing Markdown source hash remained unchanged.
  Only metadata was returned to repository evidence; no private payload was saved
  here. Seed entries preserve source-report/inference distinctions and uncertainty.
- Final broad workflow run still passed 11/12 with only the identical recorded
  pre-existing commit-policy mismatch. No test was weakened or unrelated policy
  changed. Existing dirty aliases, SSH documentation, and feedback log hashes
  remained unchanged before refresh.
- Before the required refresh, exact tracked/live Codex and Git configs were
  preserved in a 0700 temporary backup with 0600 files; its location is stored in
  `/tmp/personal-context-refresh-backup-location`. The mandated live-to-source
  snapshot is expected to update the local skipped Codex source; no configuration
  values or backups belong in a commit for this feature.
- `fish -c 'refresh-config'` exited 0 with `REFRESH COMPLETE`. All four installed
  skill files match source bytes; explicit-only metadata, the Claude symlink,
  and the installed canonical AGENTS match were verified. The installed helper's
  `validate` exited 0 and returned only revision/count metadata. Store mode is
  0600; source/config skip-worktree flag remains `S`.
- Refresh changed only the expected tracked Codex snapshot beyond session-owned
  edits. Live Codex/Git settings and tracked Git settings stayed byte-identical
  to their private backups. Existing aliases, SSH docs, and feedback log remain
  untouched. A seed-statement scan found zero matches in implementation artifacts.
- Post-refresh Second Brain regression passed 11/11; Claude link test passed;
  README returned `pass_no_change`; `git diff --check` passed. The original
  machine-local system validator path became unavailable after refresh. Located
  the existing upstream checkout copy, ran it successfully (`Skill is valid!`),
  and made smoke tests depend on the repository's own reproducible metadata and
  installed-layout tests instead. See the [validator record](../docs/postmortem/2026-10-04-personal-context-validator-after-refresh.md).
- Final review of scope: generic task artifacts and two repo-specific engineering
  lessons accompany implementation. Pre-existing smoke-test edits remain intact;
  unrelated dirty files and historical feedback were not modified. Private
  source notes were preserved. The tracked Codex snapshot change is a required
  refresh side effect, remains under its pre-existing skip-worktree flag, and
  must be excluded from a future feature commit unless separately authorized.
- Remaining practical limit: actual chat responses were evaluated in five
  synthetic agent cases, not a new interactive user session. Installed metadata
  and complete package linking were verified; invoke `$personal-context` in a
  fresh Codex session to begin the live conversation.

## Commit Boundary

Shipping authorized on 2026-10-04 through `$commit-session`. Include this plan,
matching documentation, tests, generic task postmortems, and implementation in
one focused commit: `feat(skills): add private personal-context chatbot`.

The scope helper returned `unsafe` for thread
`01a108a1-fbc2-7600-9bbb-9e56171e4da8`: its session log contains no detected
repository writes or baseline. Use the active conversation's directly observed
writes and saved pre-write status/hash baseline for attribution. Stage only the
personal-context section of `docs/smoke-tests.md`; preserve its pre-existing
phone SSH section. Exclude unrelated aliases, SSH docs, benchmark/SSH plans and
prompt, pre-existing postmortems, and the machine-local skipped Codex snapshot.

Fresh shipping checks passed: 22 personal-context tests, 11 Second Brain tests,
helper basedpyright with zero findings, Claude link checks, README gate
(`pass_no_change`), and diff whitespace. The previously recorded broad workflow
failure remains an unrelated limitation. Push the verified commit to
`origin/main`; report its result and the remaining unrelated worktree state.
