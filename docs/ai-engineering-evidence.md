# AI engineering evidence

This assessment explains what seven selected coding sessions and the public
workflow repository demonstrate about AI-assisted engineering. Start with the
conclusion, inspect the linked implementation receipts, then read the evidence
limits before using the estimate in recruiting conversations.

## Assessment

**Public positioning: approximately 90th-percentile AI-enabled engineering
effectiveness among developers overall, including nonusers — subjective,
unvalidated self-estimate.** The user selected this punchier positioning after
the evidence review, using the upper end of its original range below. It is a
presentation choice, not a new measured result or an upgraded independent rating.

**Subjective, unvalidated estimate: 70th–90th percentile for AI-enabled
engineering effectiveness among developers overall, including nonusers.**
This is an AI-assisted qualitative judgment dated **October 22, 2026**, not a
measured population rank, statistical interval, certification, or assessment of
overall engineering seniority. Another informed assessor could choose different
bounds. The concrete evidence below is more defensible than the number.

The strongest demonstrated capability is turning agent use into an inspectable
engineering workflow: versioned shared instructions, reusable automation,
privacy boundaries, explicit regression contracts and scoped commits. The
sample also shows product feedback and correction of misleading measurements.
It does not establish a productivity multiplier or independent mastery of all
the implementation work performed by agents.

The README's **six concurrent AI coding agents** is the user's reported workflow
scale. It describes sessions coordinated in parallel, not a measured sixfold
speedup or six independent projects. The fixed seven-session review below
remains the original evidence sample; the count is not retroactively changed.

## Public receipts

Every source below uses an immutable commit. On October 22, anonymous HTTPS
requests returned 200 for all eleven linked source files and their GitHub blob
pages; downloaded source bytes matched the reviewed local Git objects. This
verifies publication and source identity. It does not rerun historical tests.

| Capability or result | Inspectable evidence | What the evidence establishes |
| --- | --- | --- |
| One policy across coding tools | [Claude import](https://github.com/Kevin-Mok/ai-cli-workflow/blob/d931cc2c8377fe0687eed1bd118d0e941ec28e6a/dot_claude/CLAUDE.md.tmpl), [tracked Codex defaults](https://github.com/Kevin-Mok/ai-cli-workflow/blob/d931cc2c8377fe0687eed1bd118d0e941ec28e6a/dot_codex/config.toml) | The template imports the canonical instructions; committed settings declare approval, sandbox, multi-agent and MCP controls. This is configured policy, not proof that every session follows it. |
| Privacy-aware session reuse | [Session parser](https://github.com/Kevin-Mok/ai-cli-workflow/blob/d931cc2c8377fe0687eed1bd118d0e941ec28e6a/scripts/second_brain/session_digest_input.py), [unsafe-source regressions](https://github.com/Kevin-Mok/ai-cli-workflow/blob/d931cc2c8377fe0687eed1bd118d0e941ec28e6a/tests/test_second_brain_sessions_unsafe_source.py), [metadata regressions](https://github.com/Kevin-Mok/ai-cli-workflow/blob/d931cc2c8377fe0687eed1bd118d0e941ec28e6a/tests/test_second_brain_sessions_metadata.py) | Root-author filtering, helper-session exclusion and invalidation when sources become private are implemented with regression cases. This is a bounded control, not a universal privacy guarantee. |
| Evaluation with provenance and negative results | [Skill source record](https://github.com/Kevin-Mok/ai-cli-workflow/blob/d931cc2c8377fe0687eed1bd118d0e941ec28e6a/dot_agents/skills/metaprompt/SOURCE.md), [benchmark report](https://github.com/Kevin-Mok/ai-cli-workflow/blob/d931cc2c8377fe0687eed1bd118d0e941ec28e6a/docs/metaprompt-benchmark.md) | Upstream material and local adaptation are distinguished. The capped synthetic pilot publishes failures and explicitly finds no supported overall winner or coding-quality ranking. Raw historical runs are private, so public re-audit of those measurements is limited. |
| A scoped player-notice change | [Implementation](https://github.com/Kevin-Mok/twitch-grid/blob/29fd768688de19552ba0d6b2b6ab7189bcb43bf8/src/components/PlayerSurface.tsx), [browser regression](https://github.com/Kevin-Mok/twitch-grid/blob/29fd768688de19552ba0d6b2b6ab7189bcb43bf8/tests/quality-notice.spec.ts) | A public commit suppresses the fallback overlay; its regression checks continued iframe identity through a sidebar toggle. It does not prove live upstream playback. |
| A layout fix with explicit geometry checks | [Sizing implementation](https://github.com/Kevin-Mok/twitch-grid/blob/78e88d0e9cfc7c82643f87f6542ba79d17f2e9d3/src/components/PlayerSurface.tsx), [geometry regression](https://github.com/Kevin-Mok/twitch-grid/blob/78e88d0e9cfc7c82643f87f6542ba79d17f2e9d3/tests/narrow-panels.spec.ts) | The one-line content-box correction has 2×2 geometry and overflow assertions at 1280×900, 1440×730 and 2048×973, plus retained-iframe checks. The session reports successful focused browser checks; no application suite was rerun for this assessment. |

These are AI-assisted outcomes and workflow integrations. Git author metadata
does not establish that the human independently wrote the code. Imported tools
and skills retain their upstream authorship; the contribution assessed here is
their integration, task direction, review process and resulting artifacts.

## Seven-session snapshot

The original seven screenshot sessions were retained even as their titles
changed. Session collection ran **20:22:21–20:23:07 UTC on October 22, 2026**;
implementation collection began at 20:21:45 UTC. Source publication was checked
afterward. The selected sample spans three projects: five tasks share the same
streaming checkout, one concerns a public reporting CLI, and one concerns
private operational work. It is not seven independent projects or a random
sample of developer performance. This calling assessment session is excluded.

| Original task | Observed state at collection | Evidence and limits |
| --- | --- | --- |
| Recovery automation | Uncommitted; operator authentication blocked live acceptance | Agent recap reports automated preparation and test checks. Underlying test output is truncated; end-to-end acceptance remains pending. Private implementation details and links are excluded. |
| Reporting CLI latency | Active; uncommitted measurements | Progress shows 11 of 26 comparison cases complete. Recorded correctness checks and parity claims do not establish a final speedup; cold, changed-data and control measurements remain pending. |
| Quality notice | Public committed result | Source and regression are in the receipts above. Isolated test/build/browser success is recorded by the session, not freshly reproduced here. |
| Combined stream rate | Uncommitted follow-up | Latest work changes units to MB/s and adds an overlay total. Validation is reported; playback-rate estimation is distinct from measured network throughput. The stuttering cause remains unresolved. |
| 2×2 layout | Public committed result | A new scoped commit appeared during collection. Source and geometry assertions are directly inspectable; focused browser success is reported. Earlier whole-checkout failures included another session's deliberate RED work. |
| Chat cropping | Uncommitted | A percentage crop and persistent full-chat escape are reported with fixture checks. A fixed crop can hide content when the provider layout changes; live acceptance remains unverified. |
| Default quality | Uncommitted; follow-up reopened | Earlier validation and live resolution checks are reported, but the newest turn still investigates the user's persistent mismatch. Do not describe the reported bug as fully resolved. |

Session IDs, raw messages, local paths and collection records remain private.
Most human scope decisions appear in saved prompts or agent recaps rather than
fully visible original turns; that weaker attribution is retained. The human
selected tasks, supplied concrete UI feedback and refined acceptance criteria.
Diagnosis, code generation and command execution belong to the AI-assisted
workflow unless independent human evidence supports a narrower attribution.

## Five dimensions

Evidence labels describe observations: **configured** means a policy exists;
**demonstrated** means source or an observed result supports it; **repeated**
means it appears across selected cases; **integrated** means durable workflow
artifacts connect it to normal use. These are not numeric population scores.

| Dimension | Evidence level and strength | Counterevidence or missing proof |
| --- | --- | --- |
| Task framing | Demonstrated: concrete layout/notice requests, follow-up feedback and acceptance refinement | Terse prompts delegate substantial diagnosis; original decision evidence is sometimes a recap. |
| Decomposition and coordination | Demonstrated, mixed: parallel bounded tasks and scoped public commits | Five agents share a checkout; overlapping files and deliberate RED tests complicate other sessions' validation. Pane count does not measure throughput. |
| Verification and review | Demonstrated in source; repeated checks reported across sessions | Fixture regressions, isolated validation and review records are stronger than completion prose. Several live acceptance checks and the latest quality follow-up remain open. |
| Reproducibility and context | Integrated in committed config, shared policy, provenance and session-source filters | Live settings differ from the committed public snapshot. Configuration is not proof of consistent compliance or measured benefit. |
| Delivered results | Demonstrated: two scoped streaming commits are publicly inspectable | Five current tasks remain uncommitted or incomplete in this snapshot. Production reliability, team delivery and matched time/cost comparisons are unmeasured. |

## Why this subjective range

The **70th-percentile lower bound is judgment**, reflecting the combination of
durable tool integration, source-aware evaluation, privacy controls and
inspectable regression-backed changes. That combination supports a stronger
assessment than merely having access to a coding assistant. There is no dataset
establishing this cutoff or proving superiority over a particular nonuser.

The **90th-percentile upper bound is also judgment**, allowing for practiced
agent direction while recognizing limited proof of reliable integration,
completed live acceptance, independent technical reasoning and sustained
delivery. The sample cannot distinguish a top-decile developer from a capable
user whose agents perform most of the engineering. The wide range deliberately
does not imply precision or a confidence interval.

Including developers who do not use AI defines the requested comparison group;
it does not assign them a low score. An effective nonuser can outperform this
workflow. Comparing real effectiveness would require representative developers,
matched tasks, independently judged outcomes, and recorded quality, time and
cost. None of that population experiment was performed.

For context only, the [2026 Stack Overflow AI tool-use data](https://survey.stackoverflow.co/2026/ai/data/ai-select)
reports 4,582 of 17,464 respondents (26.2%) selecting agents or automated
workflows and 3,003 (17.2%) selecting no AI tools. This optional multiselect
question measures reported adoption. It does not measure proficiency or supply
the bounds above. The [survey methodology](https://survey.stackoverflow.co/2026/methodology)
describes recruitment through Stack Overflow channels; respondents are not a
random sample of all developers. Data attribution: Stack Exchange Inc., 2026,
ODbL 1.0.

## Validation and next evidence

Source publication and identity were checked directly. Session command evidence
was inspected where available, and recorded claims remain labeled. No production
operations, application suites or new paid/model benchmarks were run. Existing
benchmark limitations were preserved; this task does not show metaprompt
superiority. An independent review checks claim support, not percentile truth.

The most useful next evidence is completed integration with current live
acceptance, a finished fair latency comparison, and a small matched delivery
study that records review time and rework. Those are future opportunities, not
additional work authorized by this assessment.

The [saved execution prompt](../prompts/assess-ai-engineering-proficiency.md)
and [implementation record](../plans/ai-proficiency-recruiter-evidence.md)
describe the method and checks. Revisit this dated assessment when the source
sample changes; do not silently promote subsequent work into this snapshot.
