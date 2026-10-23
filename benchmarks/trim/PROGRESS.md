# Trim progress

Current milestone: **passes1–6 committed; pass7 tool output validated for commit**.
Static loaded context37,619→16,127B (9,404.75→4,031.75 estimated tokens,
−57.13%). Conditional reference loads remain additional; actual runtime context
is not measured. Later description/body/output passes and saturation remain open.

| Pass | Technique | Surface | Old bytes | New bytes | Reduction | Skills |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Baseline | Pre-edit inventory | Loaded | 37,619 | 37,619 | 0% | 59 |
| Pre-cull prerequisite (included in pass 1) | Measurement + required technique record | Loaded | 37,619 | 37,756 | -0.36% | 60 |
| 1 — cull | Approved relevance cull, merges and calibration sync | Loaded | 37,756 | 29,632 | 21.52% | 22 |
| 2 — approved intake | Bounded complementary imports and pinned swap | Loaded | 29,632 | 30,251 | -2.09% | 27 |
| 3 — admission gate | Evidence-priced additions and mandatory PASS ledger | Loaded | 30,251 | 30,292 | -0.14% | 27 |
| 4 — CASD | Log-informed conditional policy routing | Loaded | 30,292 | 16,127 | 46.76% | 27 |
| 5 — body concision | Repeated technique prose compressed in place | lean body | 15,125 | 10,897 | 27.95% | 27 |
| 6 — descriptions | Trigger words retained; procedure stays in bodies | Loaded | 16,127 | 15,116 | 6.27% | 27 |
| 7 — agent output | Summaries with full explicit diagnostics | CLI output | 16,243 | 124 | 99.24% | 27 |

Baseline body bytes: 403,458 (100,864.5 approximate tokens). Loaded estimate:
9,404.75 tokens; UTF-8 bytes/4, not actual model tokenizer usage. See BASELINE.json
for every description/body/file and instruction count. The duplicate `.agents`
brand entry is measured separately, excluded from canonical loaded totals.

Planning: saved prompt and metaprompt report; native Plan Mode unavailable in
this Default-mode harness. ExecPlan precedes implementation. Imported sources
are protected. No pushes, refresh-config or chezmoi apply are authorized.

Baseline tests: focused contract/doctor 35 passed, 33 subtests passed, 3 failed;
full tests interrupted on six pre-existing SyntaxErrors. Relevant checks will
be repaired or scoped with explicit evidence before commits; no false green.
Pass 0: defining tests observed RED (missing CLI), then GREEN; review reproducers
for missing instruction comparisons and malformed snapshots also observed RED
then GREEN. Latest benchmark tests: 8 passed, 9 passing subtests; budgets pass.
The required lean-instructions skill adds one skill, a 58-byte description and
a 79-byte AGENTS pointer: 137 loaded bytes / **34.25 estimated tokens added**.
The baseline remains immutable; the initial budget explicitly includes this
user-requested addition. Measurement itself saves zero tokens. Commit subject:
`test(trim): baseline instruction costs and budgets`.
Status: **prepared, uncommitted**. Staging failed with exit 128: shared Git
metadata is on the read-only `/home` mount. No privacy gate or commit ran.
Do not count this row as a committed optimization pass; no token reduction yet.
What worked: separating loaded and body metrics prevents inflated savings claims.
Review-driven fixes compare lines/bytes/token estimates for AGENTS, developer
instructions and every skill; malformed snapshots exit 2 cleanly. PTY cases
cover interactive decoration and CODEX/CLAUDECODE/plain overrides. Technique rule,
rationale, before/after costs, mistakes and checklist live in
`dot_agents/skills/lean-instructions/SKILL.md`; every later pass must update it.
Independent pass-0 review is in `checks.md`; all reported implementation defects
have covering fixes. Doctor snapshot comparison retains the same existing 38
errors/1 warning, with no changed findings and catalog now 60/60. Final fresh
focused run passed 34 tests/42 subtests, exit 0; README gate and diff check also
passed. Raw test output remains private at `/tmp/trim-final-pytest.log`.
Next: move conditional AGENTS procedures with an auditable section mapping;
protect curated imports rather than trying to hit their old suggested size goals.

Current sequence follows the latest instruction: finish, validate and commit the
cull before another optimization pass. Git staging is blocked, so no pass has a
commit SHA. Measurement prerequisites are prepared; no CASD policy trimming,
private intake or admission-scoring implementation belongs in the cull pass.

## Required trigger baseline (prepared, separate commit boundary)

The user extended `.trim-prompt.md` before any description-shortening pass.
`scripts/trigger-eval --plain --check` ran on the unchanged descriptions:
**40/50 exact-set accuracy (80%)**, micro precision/recall/F1
87.23% / 85.42% / 86.32%. Corpus: 36 single-label, 6 multi-label, 8 none cases.
This is a frozen deterministic TF-IDF names-and-descriptions proxy, not observed
model routing. No model/API call or skill body enters the scoring features.
The 9 defining tests passed after observed RED; the gate permits description
changes and rejects score regression, corpus changes or algorithm-ID changes.
Keep the original corpus/baseline and capture a JSON before-edit report for
every description pass. Use it as `--baseline PATH` on the after-edit check;
revert any decline from the previous accepted score, even above the original 80%.
The corpus names 38 of 60 skills; uncovered branches still need semantic review.
This measurement milestone saves zero tokens itself and is uncommitted.
What worked: separate negative and multi-label cases expose over-triggering.
Next: use log-mined evidence to choose which conditional rules can move safely;
perform each actual optimization only within its own verified commit boundary.

## Log-mined evidence (prepared, separate commit boundary)

The frozen 60-day scanner completed read-only in 12 seconds: 2,639 candidates,
416 eligible sessions and 1,413 eligible user messages. Six complaint candidates
(copy/paste 3, unsupported completion 2, verbosity/cost 1) met no predeclared
frequency threshold. The 1,767 tool-completion candidates include intentional RED,
negative fixtures and mirrors; they are not 1,767 unexpected incidents.
See failure-modes.md/counts for exclusions and safe paraphrases; no native logs,
identifiers or raw excerpts are exported. Eight synthetic tests pass.
What worked: whole-file privacy screening avoids drawing public policy from
private/context/helper traffic. Next: retain safety/evidence/command-usability
controls and move unsupported conditional detail in the later CASD rule pass.

## Approved cull (prepared, separate commit boundary)

The approved ranking overrides the original no-drop constraint for these names.
Exactly 39 local sources were removed after clean-state checks. `last30days` and
both brand copies remain. `context-handoff` absorbs the harness; the retained
`commit-plan-push` preserves read-only planning. Canonical local count is 22;
external keepers and built-ins are measured separately.

Net loaded cost: **37,756 → 29,632 bytes**, saving **2,031 estimated tokens
(21.52%)** against the prepared pre-cull inventory. Against original HEAD:
37,619 → 29,632 bytes, **1,996.75 estimated tokens saved (21.23%)**.
Descriptions: 13,462 → 5,240 bytes. Current SKILL.md bodies: 138,102 bytes,
compared with the original 403,458; body savings are on-demand, not recurring.
The latest required calibration-sync description/router costs add 89 loaded
bytes (22.25 tokens) to the earlier 29,543-byte cull draft; they are included.

Routing: unchanged keeper/none cases improved **13/17 → 15/17 (88.24%)**.
After the calibration-sync trigger expansion, the score remains 15/17 against
its immediately preceding 15/17 snapshot. The original 50-case corpus/baseline
is immutable; its 40/50 result is a different scope. No model calls were used.

Fresh focused check: **82 tests and 217 subtests passed**, exit 0, covering cull
contracts, merge behavior, metaprompt references, emoji output, benchmark,
trigger scoring, miner fixtures, design sync, retired Superpowers controls and
calibration inventory/history/description fidelity. The exact command is saved
in pass-evidence.json; final logs are `/tmp/trim-cull-final-*.log`.
`bash tests/test_claude_skill_links.sh` passed silently. AI workflow contracts:
9 passed / 3 failed; the same inherited feedback/push-policy/routing-shim defects
were previously reproduced at original HEAD. This is not whole-suite green. A fresh workflow doctor found the merged
context-handoff provenance omission; SOURCE.md was added with actual pinned
input and template digest. The rerun has 35 inherited errors/1 warning and
zero new finding keys versus the saved baseline.
A read-only working-file privacy preflight found no categories across 66
modified/new regular files, excluding the three private user inputs. It is not
immutable staged-candidate clearance. The required exact check awaits writable Git
metadata; the earlier unchanged-index PASS does not clear these new files.

The cull now includes the required calibration inventory/reference maintenance.
Every removal keeps its reason, evidence, survivor and date under Culled, with
an explicit pending SHA until a real commit exists. Reference drift checks must
pass before the cull can commit. Fresh plain/JSON checks pass: **228 source
entries, 38 configured ACTIVE, 190 installed-only, 0 missing/stale**. Five
built-ins are detectable. All 93 ranked candidates remain, plus 52 honest
unscored source identities and 60 retirement records. Actual public trigger
descriptions and jobs support overlap searches; text/hash/scope drift is tested.
The on-demand reference is 105,815 bytes and adds no recurring description
load. No history entry is deleted on re-admission.

Admission-only drafts are preserved at `/tmp/trim-post-cull-drafts-lr0ie7as/`.
Its `manifest.json` records eight original paths and hashes. Calibration reference
and tests were restored from that snapshot for the latest cull requirement; the
admission ledger/tests/cases and full admission sections remain deferred. Restore
shared-file deltas carefully after the cull; do not overwrite the newer cull body.
The host has fetched all seven approved `private/<branch>` refs and disabled
push on that remote. No PR source file has been imported. The earlier history
audit predates those fetched objects and is not a clearance for intake.

### Removed local sources

Description bytes contribute recurring cost; body bytes load on demand. Full
source bytes include supporting assets/data. Values are gross removals, not net
savings after survivors and required routing. `CULL.json` is the machine-readable
manifest; the table below records every approved local removal.

| Name | Reason | Description bytes | Body bytes | Full source bytes |
| --- | --- | ---: | ---: | ---: |
| adapt | Covered by retained frontend-design and external impeccable; approved cull. | 143 | 6,857 | 7,107 |
| animate | Covered by retained frontend-design and external impeccable; approved cull. | 134 | 7,414 | 7,637 |
| arrange | Covered by retained frontend-design and external impeccable; approved cull. | 151 | 7,150 | 7,390 |
| audit | Covered by retained frontend-design and external impeccable; approved cull. | 194 | 5,937 | 6,216 |
| bolder | Covered by retained frontend-design and external impeccable; approved cull. | 132 | 6,494 | 6,714 |
| clarify | Covered by retained frontend-design and external impeccable; approved cull. | 124 | 6,537 | 6,750 |
| colorize | Covered by retained frontend-design and external impeccable; approved cull. | 130 | 6,650 | 6,870 |
| commit-plan | Planning-only mode merges into commit-plan-push. | 343 | 7,351 | 8,259 |
| critique | Covered by retained frontend-design and external impeccable; approved cull. | 179 | 5,393 | 5,660 |
| delight | Covered by retained frontend-design and external impeccable; approved cull. | 143 | 9,761 | 9,993 |
| design-taste-frontend | Covered by retained frontend-design and external impeccable; approved cull. | 202 | 21,146 | 22,385 |
| distill | Covered by retained frontend-design and external impeccable; approved cull. | 111 | 6,050 | 6,250 |
| extract | Covered by retained frontend-design and external impeccable; approved cull. | 180 | 3,676 | 3,945 |
| find-skills | Unused discovery workflow; approved cull. | 303 | 5,129 | 6,221 |
| full-output-enforcement | Unused generic output workflow; approved cull. | 203 | 2,555 | 3,807 |
| gh-fix-ci | Low-use CI workflow; approved cull. | 313 | 3,286 | 33,424 |
| harden | Covered by retained frontend-design and external impeccable; approved cull. | 169 | 8,779 | 9,036 |
| high-end-visual-design | Covered by retained frontend-design and external impeccable; approved cull. | 234 | 10,542 | 11,821 |
| imagegen | Duplicate of retained Codex .system built-in. | 328 | 9,577 | 85,735 |
| leetcode-init | Unused practice scaffolder; approved cull. | 216 | 2,159 | 51,363 |
| long-task-harness | Acceptance, evidence review and progress procedure merges into context-handoff. | 365 | 3,145 | 3,556 |
| metaprompt-alxve | Overlaps retained metaprompt and metaprompt-run. | 488 | 2,922 | 31,011 |
| minimalist-ui | Covered by retained frontend-design and external impeccable; approved cull. | 145 | 7,947 | 9,096 |
| normalize | Covered by retained frontend-design and external impeccable; approved cull. | 67 | 3,966 | 4,125 |
| onboard | Covered by retained frontend-design and external impeccable; approved cull. | 149 | 8,256 | 8,494 |
| open-pr | Low-use PR authoring workflow; approved cull. | 286 | 5,741 | 12,691 |
| openai-docs | Duplicate of retained Codex .system built-in. | 372 | 4,919 | 47,899 |
| optimize | Covered by retained frontend-design and external impeccable; approved cull. | 138 | 7,632 | 7,860 |
| overdrive | Covered by retained frontend-design and external impeccable; approved cull. | 228 | 9,676 | 9,995 |
| pdf | Unused PDF workflow; approved cull. | 248 | 2,449 | 15,040 |
| playwright-interactive | Browser coverage retained in playwright. | 94 | 31,604 | 46,555 |
| polish | Covered by retained frontend-design and external impeccable; approved cull. | 123 | 8,021 | 8,232 |
| quieter | Covered by retained frontend-design and external impeccable; approved cull. | 116 | 4,899 | 5,104 |
| redesign-existing-projects | Covered by retained frontend-design and external impeccable; approved cull. | 225 | 15,010 | 16,287 |
| screenshot | Browser capture coverage retained in playwright. | 220 | 7,702 | 53,296 |
| teach-impeccable | Design context preparation merges into frontend-design. | 148 | 2,823 | 3,037 |
| transcribe | Unused transcription workflow; approved cull. | 216 | 2,624 | 25,762 |
| typeset | Covered by retained frontend-design and external impeccable; approved cull. | 140 | 5,551 | 5,780 |
| ui-ux-pro-max | Unused explicit design search workflow; approved cull. | 147 | 3,193 | 3,228,418 |
| **Total (39)** | Gross removed sources | **7,847** | **280,523** | **3,848,821** |

### External exposure and manual follow-ups

Repository config retires the 21st, review-animations, scroll-world and
Superpowers installers/discovery links, preserving Impeccable and Higgsfield.
No upstream file or live timer was changed. Superpowers refresh is a no-op;
`--enable` is refused, `--check` reports config only, and `--disable` remains
explicit legacy-host cleanup. README and smoke checks now describe this.

Direct retired exposure descriptions total 6,450 bytes. Recursive disabled
sources total 14,288 description bytes (3,572 potential tokens). Neither is
included in the repository headline or claimed as live savings. Existing host
copies, plugin copies and timers can remain active until a separately authorized
activation/cleanup. Additional externally installed cull candidates without repo
install controls need manual review: banner-design, brand, design, design-system,
motion-primitives, no-comments, paper-shaders, pstack, slides, trickle-ui, ui-styling.
Preserve upstream repositories and inspect stale discovery links before cleanup.

What worked: keep gross deletion, net merge/router overhead, installed state and
configured state separate; test planning-only behavior before removing its entry.
The calibration-sync requirement prevents the audit from silently forgetting
removed candidates. Next: finish the cull's reference sync and verification,
stage/review/privacy-check and commit `refactor(skills): cull approved overlaps`.
No subsequent pass starts while that commit is blocked. COMPARISON is generated
from actual Git history and labels this cull as an uncommitted working draft.

## Pass 1 commit checkpoint

Normal staging now succeeds after the host granted the main .git writable
access. Fresh pass1 tests:82 passed/217 subtests; budgets PASS; routing15/17
PASS. Session scope helper returned unsafe (no recognized successful writes);
the initial two-input baseline and directly observed session edits establish
cull attribution. Exclude .trim-prompt.md, .trim-spec.md and .skills-relevance.md,
plus the deferred admission drafts kept outside the active tree.

Routing misses were inspected before committing; both already failed on the
original catalog with the identical frozen algorithm/cases:

| Case | Expected | Original prediction | Cull prediction | Decision |
| --- | --- | --- | --- | --- |
| multi-feedback-failure | feedback-memory + postmortem-memory | feedback-memory | feedback-memory | Accept unchanged lexical-proxy limitation: top-relative threshold omits the second job; both trigger descriptions still explicitly cover the request. |
| none-language | none (translate good morning) | morning + polish | morning | Accept pre-existing lexical phrase ambiguity; removal reduces false positives. The morning description requires explicit invocation and disables model invocation; translation is outside that workflow. |

No gold labels, scorer thresholds or descriptions were tuned to these misses.
The cull improves the fixed keeper slice13/17 to15/17 and preserves its score
after required calibration changes. These are acceptable cull nonregressions,
not proof of real model routing. A later description pass must still preserve
the immediately preceding score.

## Pass 2 — approved private-source intake

Pass1 is committed as `bc0360c9a59610469526c45d83efefb82f296382`; its exact
staged privacy gate passed. COMPARISON has been regenerated from that real
commit. The two lexical routing misses and their unchanged original predictions
were reviewed and accepted before commit, without changing the scorer/gold.

This pass imports only the approved four skill dirs, pinned Impeccable swap,
size-guard sources and feedback consolidation. Source audit screened104 files
(2,546,797 bytes):one home-path candidate, sanitized before public import; no
credential or private-policy candidates. Personal/private evaluation examples
and missing private-only links were removed or replaced with honest local docs.
No PR was mutated, no branch merged, no network provider called.

Four new complementary skills add406 description bytes (101.5 recurring tokens).
Their original proposal descriptions were498 bytes;92 bytes/23 tokens are
avoided intake growth, not savings from an existing catalog. shadcn's entry
shrinks20,669→6,727 bytes, with workflows/rules preserved on demand. Impeccable
adds92 local description bytes and replaces its moving external installer;
54,577 bytes of unused native/TOML inputs are omitted while required web assets,
fallbacks and licenses remain. Do not count old external description savings in
the repo-only headline. No installed upstream copy was deleted.

Catalog:27 canonical local skills including the required lean-instructions;
external CTO/plugin/built-in entries and the readonly brand mirror are separate.
The apparent one-over-roster difference is the explicitly required lean skill.
The original23-skill keep/last30days roster includes external keepers; counts
from different discovery surfaces must not be silently added.

The new46-case corpus covers every27-local name and retains the unchanged17
keeper/none cases. Its baseline uses immutable pass1 keepers plus original
approved proposal descriptions, frozen before scoring local transforms:
41/46 (89.13%). After intake:41/46, and keepers remain15/17. Corpora and scorer
are unchanged. All prior frozen corpora remain available.

The local file-size gate checks exact staged authored bytes, preserves earlier
privacy-hook vetoes and defaults new files to20,000 bytes (5,000 estimated
tokens). Existing oversized files may stay unchanged or shrink. Only reviewed
exact-path finite ceilings permit this pass's necessary legacy-doc growth.
Neither hook installer nor real configuration activation is run here.
Feedback grows3,503→4,670 body bytes with unchanged description; the append-only
feedback log is untouched. AGENTS.repo shrinks2,036→1,122 bytes while preserving
stricter repo protections. Stale public contract assertions were repaired from
current policy rather than fabricating historical feedback entries.

Calibration reflects the pinned local replacement; all60 pass1 retirement
records now cite its real commit SHA. The new replacement history is pending
until pass2 exists, and will be resolved in the next pass. Existing93 ranking
rows retain their numeric evidence; old Impeccable moves to MERGED-INTO.
Actual source descriptions/jobs and logical install scopes remain searchable.

Validation limitations: generic quick_validate rejects supported explicit-only
metadata; this matches the existing reviewed validator incident, so invocation
boundaries stay intact and repository contracts are used. Live Impeccable
engine/provider execution and real agent-catalog activation remain unverified.

What worked: immutable source baselines prevent tuning the exam after imports;
separate new capability costs, moved entry text and retired external exposure.
Next: commit this intake after focused tests, inventory/budget/size/privacy
checks, then enforce the scored admission gate in its own pass.

Measured pass2 loaded cost: 29,632→30,251 bytes (+619; +154.75 estimated tokens). Against original37,619 bytes: 19.59% lower. SKILL body bytes: 138,102→179,494; on-demand additions are not recurring savings.

Final pass2 focused run:192 tests/231 subtests PASS, including both privacy suites
and the repaired AI workflow contract. Earlier budget tests raced the in-progress
budget freeze; the fresh targeted2 and complete rerun both pass. Budget, expanded
routing, keeper routing, vetted inventory and README gates pass. Actual command:
pass-evidence.json. Inventory233 sources/42ACTIVE/191installed-only/0drift.
Reviewed finite legacy-doc growth ceilings are in config/file-size-guard.json;
they are exact byte ceilings, not wildcard exclusions or live hook installation.

Pass2 committed: `60c6e70f` (`feat(skills): intake approved complementary
workflows`) after192 tests/231subtests, bothrouting corpora, inventory and budgets
passed; exact staged size and privacy gates passed.123 reviewed paths, no
private inputs/model config/live installation/push. COMPARISON regenerated from
actual pass1+pass2 history. Intake retirement history now cites its real commit.

## Pass 3 — scored admission gate (in progress)

Enforce every local skill's measured PASS, record rejected PR reasons/change
conditions, compare2–3precedents and duplicate jobs before scores. Preserve the
explicit last30days exception and unmeasured body-load assumption. This pass
adds a quality control rather than claiming a token reduction. Source privacy
and scope checks are not waived by score or user ranking.

## Pass 3 — scored admission enforcement

The mandatory one-line gate costs155→196bytes (+10.25 recurring estimated
tokens); loaded30,251→30,292B (+0.14%; cumulative original−19.48%). Descriptions
remain5,738B and27locals; bodies179,494→183,100B (+901.5 on-demand tokens).
The lean entry remains237body lines, under300. Ledger19,754B fits20KB.

The35 entries record27localPASS,1rulePASS and7rejected-PRDENY, each with2closest
vetted precedents. Shared checks avoid repeating invariant review references.
All current measured costs, rubric arithmetic and frozen46case IDs are tested;
last30days score0.989211 remains an explicit KEEP exception, not inflated.
Semantic evidence/privacy review remains human judgment; the lexical score is
not real model routing. Calibration retains the actual intake retirement SHA.

What worked: shared checks fit the complete ledger under20KB without stripping
reasons or fabricated evidence. This pass buys enforcement, saves0tokens.
Next: use the already-mined failure evidence to move conditional AGENTS detail
to mandatory on-demand homes, preserving every observed preventive/safety rule.
Commit:feat(skills): enforce scored admission decisions. No push/live apply.

Fresh pass3 verification:198 tests/239subtests PASS; loaded budgets PASS; frozen
intake routing41/46 unchanged; inventory233sources/0drift. README gate
pass_no_change. Exact staged privacy/size clearance runs immediately before commit.

## Pass 4 — CASD conditional procedures

Canonical23,147→8,982B;357→145lines. Static loaded30,292→16,127B
(−14,165B/3,541.25estimatedtokens,46.76%); description5,738B and27skills
unchanged. Bodies183,100→184,312B charges the required technique record.
Seven mandatory reference homes preserve42moved blocks; all91original blocks
retain exact wording/hash and appear exactly once in casd-map.json. Core retains
safety, authority, defining tests and completion evidence. The title checkpoint
stays standing; details load for native-tool discovery/change. Other routers
cover system design, failures, CLI/fish, memory, docs/config and delivery.

The416screened sessions support completion/copy-paste safeguards. No complaint
met3sessions/2dates; no speculative new rule was added. The gate records a PASS
for replacement routing:1,250B/312.5static tokens of overhead included in net
savings, public source only, case instructions-edit,91block preservation.
Reference text is retained; actual loads/cache/tokenizer use are unmeasured.

What worked: exact block retention proves more than heading searches; required
routers avoid silently losing policy. Contract tests resolve real moved homes.
Next: trim owned descriptions against the saved41/46 corpus and preceding
accepted snapshot, retaining explicit-only invocation and all trigger branches.
Commit:refactor(instructions): route conditional procedures on demand.

Fresh CASD selected200tests/330subtests PASS; frozen41/46routing unchanged,
233sources/0inventorydrift, budgetsPASS, READMEpass_no_change. Exact staged
size/privacy clearance precedes the dedicated pass4commit.

## Pass 5 — technique-body concision

All8existing technique records plus the new concision record retain rule, why,
repo before/after token example, mistakes and checklists. Mandatory duplicate
search,2–3precedents, rubric, explicit exceptions, privacy/provenance, frozen
previous-case floors, size checks and cull history remain. No technique moved.
Lean body15,125→10,897B saves1,057estimated on-demandtokens (27.95%),177lines;
description69B unchanged. Overall bodies184,312→180,084B; loaded16,127B and
27skills unchanged. This pass saves0recurring tokens.

What worked: remove repetition within five fixed fields rather than moving
required technique details out of the skill. The aspirational10KB target was
not forced at the expense of safeguards; the actual300line budget passes.
Next: apply description candidates only after replaying the unchanged current
41/46snapshot, then address agent tool output and four audit-format findings.
Commit:refactor(skills): condense the lean technique log.

Fresh pass5 selected200tests/330subtests PASS; budgetsPASS,41/46routing
unchanged, inventory233/0drift. Exact staged size/privacy gates before commit.

## Pass 6 — owned description trimming

Fresh baseline before any description edit:41/46, saved in description-before.json.
After8owned edits:42/46 (91.30%), keeper15/17→16/17; every previously correct
case retained. No cases/scorer/algorithm changed. The formerly missed compound
feedback+failure case now passes; translation/morning remains a lexical limitation.
Several draft combinations and shortened morning were rejected for no-skill
misfires. Descriptions below retain natural trigger branches and explicit-only
metadata; all8skill bodies are byte-identical to the preceding commit.

| Skill | Old description B | New B | Estimated recurring tokens saved |
| --- | ---: | ---: | ---: |
| commit-session | 434 | 245 | 47.25 |
| next-tasks | 423 | 127 | 74 |
| night | 288 | 143 | 36.25 |
| feedback-memory | 338 | 166 | 43 |
| personal-context | 358 | 261 | 24.25 |
| fish-alias | 166 | 132 | 8.5 |
| postmortem-memory | 160 | 124 | 9 |
| ai-workflow-doctor | 200 | 158 | 10.5 |

Descriptions5,738→4,727B, loaded16,127→15,116B:252.75estimated recurring
tokens saved,6.27% thispass/59.82% cumulative. Both old description-size
exceptions retire; all descriptions now≤400B. Calibration descriptions/hashes
and measured admission costs update together. The required technique record
adds905bodyB, overall180,084→180,989B; it is separate from recurring savings.

What worked: reject new misfires as well as aggregate declines; global lexical
weights can affect an unchanged skill. Keep longer wording when it preserves
correct no-skill routing. Next: terse agent CLI checks, preserving interactive,
plain, JSON/protocol and explicit diagnostic behavior.
Commit:refactor(skills): shorten owned routing descriptions.

Fresh pass6 selected200tests/330subtests PASS; budgetsPASS,42/46routing
vs previous41/46, inventory233/0drift. Staged size/privacy gates before commit.

## Pass 7 — agent CLI output

Same plain vetted check16,243B/235lines→124B/3lines saves16,119B/4,029.75
estimated OUTPUTtokens per invocation (99.24%). Staticloaded15,116B and27skills
unchanged; this saves0recurring instructiontokens. Required technique adds903
bodyB:180,989→181,892B.

Existing README/doctor helpers suppress decoration in pipes or CODEX_*/
CLAUDECODE environments; real humanTTY remains decorated, including NO_COLOR.
Explicit --plain/CLI_PLAIN work. Bash captures originalstdout before command
substitution. Doctor and vetted --check return agent summaries; --details and
JSON retain complete diagnostics/inventory. Every inventory error, protocol
status and failure exitcode remains. Existing full-diagnostic test callers now
request --details, preserving their assertions.

What worked: test realPTY and agentenv, not only mockedisatty. Output savings
are separate from catalog cost; no new helper framework is needed. Next: fix
the4intake provenance field-format findings using actual pinned source evidence,
then remove the already-audited redundant developerinstruction block.
Commit:perf(cli): summarize agent workflow checks.

Fresh pass7 selected230tests/381subtests PASS; budgetsPASS,42/46routing
unchanged, inventory233/0drift, READMEpass_no_change. Staged gates beforecommit.
