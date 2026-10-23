# Trim progress

Current milestone: **pass 1 cull validated; staging and exact privacy review
now proceeding after Git metadata access was restored**. The next pass has not started. Final totals and recommendations
will appear here only after the remaining passes and saturation audit. Earlier
prepared milestones below are historical runs; current cull evidence is separate.

| Pass | Technique | Surface | Old bytes | New bytes | Reduction | Skills |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Baseline | Pre-edit inventory | Loaded | 37,619 | 37,619 | 0% | 59 |
| 0 (prepared prerequisite) | Measurement + required technique record | Loaded | 37,619 | 37,756 | -0.36% | 60 |
| 1 — cull | Approved relevance cull, merges and calibration sync | Loaded | 37,756 | 29,632 | 21.52% | 22 |

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
