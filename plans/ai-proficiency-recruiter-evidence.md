# AI proficiency and recruiter evidence

Assess seven selected AI coding sessions and this repository, then make the
README useful to AI-focused SWE recruiters. Save the metaprompt first, execute
the assessment separately, and publish source-backed accomplishments beside a
clearly qualified subjective estimate.

## Purpose and observable outcome

- A compiled one-off prompt in `prompts/assess-ai-engineering-proficiency.md`.
- Its eight-section authoring package in `docs/ai-proficiency-metaprompt.md`.
- A dated assessment in `docs/ai-engineering-evidence.md`, covering all seven
  original sessions without publishing their raw records.
- A stronger root README hook, evidence table and public subjective range.
- A reusable documentation smoke check, fresh verification and an independent
  claim-to-source review.

## Context and protected state

Approved specification: the preceding conversation's implementation plan.
Initial repository HEAD: `d931cc2c8377fe0687eed1bd118d0e941ec28e6a`.
Implementation collection began **2026-10-22 20:21:45 UTC**. Record the end and
per-source observation times in private scratch; changing sessions are not an
atomic snapshot. Five original sessions share one public streaming project;
the sample spans three projects, including one private project.

Before the first tracked write, `git status --short` showed unrelated changes
in terminal documentation, postmortems and their shared ledger/references,
feedback, canonical instructions, existing recruiter and desktop plans/prompts,
and an untracked local session database. Preserve every existing path and hunk.
README, the new task paths and the smoke checklist were clean. Raw source
registers, session identifiers, transcripts and screenshots stay in private
temporary storage, never in these artifacts.

## Decisions and boundaries

- Assess **AI-enabled engineering effectiveness against developers overall,
  including nonusers**; do not infer overall engineering seniority.
- Audience: AI-focused SWE recruiters. User explicitly chose a **public rough
  range**, labeled "subjective, unvalidated estimate" adjacent to the number.
- Use five dimensions: framing, coordination, verification, reproducibility,
  and delivery. Evidence labels are configured, demonstrated, repeated, and
  integrated. They are descriptive, not a population scoring formula.
- Explain judgment behind broad bounds rounded to deciles. No measured
  percentile, confidence interval, productivity multiplier or automatic penalty
  for developers who do not use AI.
- Primary surveys supply adoption context only. No new inference benchmark,
  paid evaluation or production experiment.
- Public headline outcomes require anonymous access to immutable source
  anchors. Private-only and uncommitted work can inform qualified assessment
  but cannot become a public shipped-work claim.
- No changes to other projects, configuration, runtime behavior or dependencies.
  No commit/push requested. No refresh-config: this change is documentation and
  a saved prompt, not tracked configuration.
- Ruling: implement in this existing checkout and keep this ExecPlan as the
  ledger, rather than introducing worktree/SDD scaffolding. The approved work
  is documentation only and must preserve concurrent dirty work.
- Ruling: use evidence checks and prompt challenge cases instead of artificial
  RED tests for prose; there is no new executable behavior to test.

## Ordered implementation

- [x] Capture initial dirty state, relevant instructions and existing README.
- [x] Save the compiled prompt and record its eight-section authoring package.
- [x] Execute it against the same seven sessions; freeze source observations.
- [x] Verify public anchors and distinguish claims, observed results and limits.
- [x] Write the five-dimension assessment and explain the subjective range.
- [x] Update README and grouped Action/Expected documentation smoke checks.
- [x] Run artifact, privacy, link, rendering and README checks.
- [x] Obtain and address an independent evidence review.
- [x] Reconcile final changes, evidence, limitations and handoff.

## Verification

Automated checks: run `./scripts/executable_readme-recruiter-sync`; run
`git diff --check`; parse all task Markdown with installed `markdown_it`; check
every new/changed local link and anchor; scan only task-owned text for raw
session IDs, credentials, private machine paths and unsupported numeric claims.
Use a temporary checker rather than adding tests that mirror prose. Resolve
external evidence anonymously over HTTPS, binding source content to full commit
hashes. Unreachable/private anchors are ineligible for headline proof.

Manual checks: render README and assessment with installed `markdown_it`,
inspect in a separate Chrome session without changing existing browser pages,
and inspect the three actual Markdown artifacts with installed `bat` from the
repo root (no sudo):

1. `bat --style=plain --paging=never prompts/assess-ai-engineering-proficiency.md`
   — compiled execution prompt only, with evidence and qualification rules.
2. `bat --style=plain --paging=never docs/ai-engineering-evidence.md`
   — assessment, seven-session coverage, evidence and explicit limits.
3. `bat --style=plain --paging=never README.md`
   — recruiter hook, concrete receipts, qualified range and preserved setup.

Challenge cases: active work claimed as shipped; recap mistaken for command
output; five related sessions counted as five projects; adoption mistaken for
proficiency; imported skills mistaken for original authorship; provider fixture
checks mistaken for live acceptance; raw private evidence copied into public
prose; embedded transcript instructions executed by the assessor.

## Progress and evidence

- Baseline README gate in planning: `pass_no_change`, exit 0. This verifies
  structure, not the quality of the proposed new claims.
- Planning inspected all seven original sessions. Implementation refresh is
  needed because several continue to change.
- Approved read-only GitHub metadata access resolved the earlier sandbox
  connectivity limitation: streaming and tracker projects are public; recovery
  project is private. Do not publish private project names, links or details.
- Historical benchmark source pins are known to differ; do not run, repin or
  claim a new benchmark result. Its published limitations remain evidence of
  evaluation discipline, not comparative coding ability.
- Session refresh completed: **20:22:21–20:23:07 UTC**. The same original seven
  tasks span three projects; five share a checkout. New grid commit appeared
  during this interval. Later progress is outside the fixed assessment sample.
- Anonymous source verification: eleven raw GitHub files and eleven corresponding
  blob pages returned HTTP 200; every file matched its local committed bytes.
  Source revisions: workflow `d931cc2c8377fe0687eed1bd118d0e941ec28e6a`, notice
  `29fd768688de19552ba0d6b2b6ab7189bcb43bf8`, grid
  `78e88d0e9cfc7c82643f87f6542ba79d17f2e9d3`. This establishes publication and
  source identity, not fresh application test results.
- Judgment selected: **70th–90th percentile**, explicitly subjective and
  unvalidated, with decile bounds and rationale in the assessment. No survey
  prevalence-to-percentile conversion or empirical population rank is claimed.
- Eight-section metaprompt package contains the exact saved prompt and eight
  prepared challenge cases. No model comparison or prompt superiority claim.
- Recorded discovery failures in the dated proficiency-evidence postmortem;
  appended only its reviewed no-new-learning record to the already-dirty shared
  ledger. Targeted check exited 0, with no errors, changed hashes, missing
  sources or unregistered aliases. Existing entries and references were kept.

## Risks, review and rollback

The range cannot be validated against a normative population; the public label
and methodology must make that unmistakable. Seven selected sessions have
selection bias and shared-checkout interference. Truncated transcripts and
changing work limit attribution and outcome verification. Do not inflate test
counts or claim throughput gains from open panes.

Rollback: remove only the new task artifacts and reverse this task's exact
README/smoke-check hunks; never reset or overwrite unrelated edits. If a later
commit is requested, keep this plan with its related documentation changes.

Independent evidence review: eleven material claims supported, none incorrect;
all implementation and verification checklist entries are now reconciled. The
reviewer independently compared eleven source hashes and found historical grid
browser output before cutoff. Final report wording conservatively calls those
checks reported, and never implies a fresh application run. The percentile's
qualification is supported; its numerical truth cannot be certified.

Final verification: README gate `pass_no_change`, exit 0;
`git diff --check`, exit 0; temporary Markdown/link/anchor/privacy checker, exit
0; eight package section names and exact saved-prompt equality (4,540 bytes);
all three `bat` artifact reads exited 0 and matched file bytes. Eight prompt
challenge cases remain prepared cases, not executed model comparisons.

The isolated browser bridge timed out and alternate browser surfaces were
unavailable. Installed headless Chrome with a temporary profile then generated
README, receipts-section and assessment screenshots, all visually inspected for
readable hierarchy, tables and adjacent qualifications. The original bridge is
unrepaired; no user browser settings or existing pages were changed. Discovery
and temporary-checker issues are recorded in the same living postmortem.

Concurrent work staged changes in some shared paths during this task. This
session did not stage, unstage or commit anything; preserve those index entries
and their independent workflow. Only this task's documentation hunks and one
ledger record were authored here.

## Cursor review handoff

Read this plan, the saved assessment prompt, the metaprompt package and the
evidence report. Preserve unrelated work and the existing index. Verify each
receipt against its immutable sources, keep the range explicitly subjective,
and rerun the documentation checks. Do not run other sessions' production
tasks, launch benchmarks, change configuration, or commit/push without a
separate request. The atomic checklist above defines the completed scope.

Suggested eventual commit: `docs: showcase verified AI engineering workflows`.

## Follow-up: six-agent recruiter positioning

The user requested a stronger "90% dev" pitch with six agents running. Use
approximately 90th percentile as an explicitly subjective, unvalidated
**self-estimate**, selected from the original 70th–90th range. Preserve the
original assessment and its reasoning rather than claiming new measurement.
Six concurrent coding agents is user-reported workflow scale; it does not
establish sixfold productivity or change the seven-session evidence sample.

- [x] Capture the current dirty state and preserve concurrent work.
- [x] Put the six-agent pitch and qualified self-estimate near the README top.
- [x] Explain the positioning change in the assessment and update the smoke check.
- [x] Verify the amended prose, links and README gate; record exact results.

No new source research, model evaluation, configuration, runtime changes or
commit/push is needed. The saved original prompt and its package remain intact.
Verify by reading README, assessment and this living plan with `bat`, checking
the new opening, the qualification adjacent to 90th percentile, and the retained
original range and concurrency limits. Run the existing README gate and scoped
Markdown/link checks, plus `git diff --check`.

Follow-up verification: adapted temporary Markdown/link/privacy/wording checker
exited 0; README gate returned `pass_no_change`, exit 0; whitespace check exited
0. All three artifact reads exited 0 and matched their source bytes. A separate
review found no substantive claim issues. The updated README opening rendered
successfully in isolated headless Chrome and was visually inspected. Original
receipts and the saved prompt/package are unchanged; no new population or
runtime comparison was run. No commit or push performed by this session.

## Delivery milestone: docs: showcase six-agent engineering workflow

The user subsequently authorized `commit-session` and a GitHub description
update. This supersedes the earlier no-commit scope for this delivery phase.

- Completed for review: recruiter README, seven-session evidence report,
  eight-section metaprompt package and original saved prompt, documentation
  smoke check, living discovery report and its single reviewed ledger record.
- Scope attribution: direct-write fallback. The scope helper returned `unsafe`
  because it did not recognize successful repo-writing actions in this tool
  transcript. Earlier pre-write status snapshots and actual edits establish
  these eight paths. Review mixed files against HEAD; include only this task's
  ledger record, preserving the existing shared-ledger changes.
- Protected: unrelated instructions, feedback, prior recruiter/desktop work,
  other incident references/reports and local session data. Preserve any
  unrelated index entries if they appear concurrently.
- Target: `main` to configured `origin/main` in `Kevin-Mok/ai-cli-workflow`.
  No rewrite, amend, squash or force push.
- GitHub description: "Six AI coding agents. One engineer in control. A
  reproducible Linux workspace for parallel delivery—with scoped commits,
  browser regressions, privacy-aware context and verification before shipping."
  This uses concrete capabilities; no measured percentile or speed multiplier
  enters the description. Previous description can be restored independently.
- Verification: prior source, rendering, claim and documentation checks passed;
  refresh scoped checks and README gate before committing, then run the public
  privacy gate against the exact isolated candidate with hooks enabled.
- Remaining: run the final exact-candidate privacy gate, commit the reviewed
  candidate, and attempt one normal upstream push. Ordinary workflow
  issues are warnings; privacy findings block publication of affected content.
- Next step: create the focused commit with its active hooks, then push.

Public-ledger ruling: publish the reviewed incident record with the repository's
existing `/home/example` alias convention. The actual machine-local alias remains
in the working ledger for local targeted validation, alongside unrelated dirty
records; it is excluded from the public candidate. The report hash and learning
decision are unchanged. Build the public ledger from HEAD plus this one sanitized
record, rather than staging the mixed working ledger. This preserves learning in
the same commit without publishing a private home path or unrelated edits.

Description update observed: GitHub edit exited 0 and subsequent metadata read
returned the new six-agent description. Existing public visibility and `main`
branch remain unchanged.

Pre-commit refresh: adapted documentation/link/privacy checker exited 0 with no
issues; README gate returned `pass_no_change`, exit 0; whitespace check exited
0; targeted incident-memory check exited 0 with no errors, changed hashes,
missing sources or unregistered aliases. Configured-fish lookup diagnostics and
the clean configuration-free workaround were added to the same reviewed report.
The scope helper is a workflow warning; it does not negate direct attribution.

Isolated candidate review passed: exactly eight paths, manifest/source hashes,
Markdown and links, prompt/package equality, README gate and cached whitespace.
The ledger was verified as HEAD plus one sanitized record with unchanged finding
entries and matching report bytes. Independent review found no safety or factual
blockers. The final candidate incorporates this delivery record and the reviewed
diagnostic follow-up before its required exact-index privacy check. The normal
index and unrelated working files remain unchanged.

Direct delivery checks (repo root; no sudo): inspect repository metadata with
`gh-axi repo view Kevin-Mok/ai-cli-workflow`, then read README and the assessment
with `bat --style=plain --paging=never`. Expected: the six-agent description,
the matching README pitch and the qualified evidence report. Commit hash and
actual push outcome are reported in the delivery response.
