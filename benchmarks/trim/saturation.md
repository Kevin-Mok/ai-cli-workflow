# Final Saturation Review

This review closes the existing optimization loop. Compare candidates against
current costs and frozen routing, retain safeguards, and stop when no further
safe meaningful pass remains. It does not establish a global mathematical optimum.

Endpoint: `79d1a8cb` (pass 12). The plan's unchanged meaningful criterion is at
least 1% of the relevant pass surface or 100 estimated tokens, with no lost
trigger branch, rule or required workflow. Description-pass surface is the full
4,727-byte catalog; body passes use their affected entry bodies. All estimates
are UTF-8 bytes/4, not measured provider usage.

## Description candidates

Read-only preflight tested all 32 combinations for five remaining owned
candidates: commit-dirty, morning, second-brain-session, commit-plan-push and
context-handoff. Only two combinations preserved all prior correct cases at
42/46. The best saved 49B / 12.25 tokens, but omitted the context-window-boundary
cue. Restoring complete retrieval, split-and-ship and boundary cues produced
another 32 combinations. Again two preserved all prior correct cases; the best
saved 22B / 5.5 tokens (0.47% of descriptions, 0.15% of loaded bytes). No candidate
was applied. The aggregate is in [saturation.json](saturation.json); private
preflight output remains outside the repository. Frozen gold/scorer unchanged.

## Owned-body review

All owned entry bodies were inspected, covering these groups:

- skill-eval, commit-session, personal-context and metaprompt-run;
- commit-plan-push, commit-dirty, night, morning, next-tasks, feedback-memory
  and postmortem-memory;
- context-handoff, grok-cli-handoff, fish-alias, ai-workflow-doctor,
  readme-recruiter-sync, smoke-test-capture and metaprompt.

Safe meaningful conditional candidates became passes 10–12: explicit dialogue,
planning-only/consolidation/learning procedures, and the handoff artifact format.
Their entries save 1,388 estimated tokens in the applicable nontriggered branches;
triggered reference loads add overhead, disclosed in the pass log. These savings
are separate from recurring context and cannot be added to the headline.

| Remaining candidate | Disposition |
| --- | --- |
| Personal project-index section (~2.6KB) | Keep shared privacy, authorship and source-qualification controls in the entry. |
| Grok STOP section (1,398B) | Keep marker, owned-job, explicit-resume and cancellation boundaries visible before dispatch. |
| Next-tasks Agent Sessions (2,578B) | Primary required evidence source; normal invocations would still load it. |
| Other owned bodies above | Remaining substantial sections define core behavior, not unused conditional branches; moving them gives no legitimate invocation saving. |
| lean-instructions (15,855B) | Required gate and every technique's five fields remain in the body; further minification harms readability. |
| Canonical AGENTS (8,982B/145lines) | Shared authority/safety/planning/tests/evidence stay standing; all 91 mapped blocks survive exactly once. |

The entry savings sum 406.5 + 762.25 + 219.25 = 1,388 tokens. Explicit dialogue adds 89.5
combined-load tokens, the three conditional procedures add 331 if all trigger,
and artifact formatting adds 103.75; no runtime frequency was measured.

## Protected sources and follow-ups

Largest protected retained entries: last30days 29,889B, Impeccable 11,985B,
frontend-design 9,634B and Vercel 7,359B; shadcn retains pinned rules on demand.
Do not rewrite these for an arbitrary size target. The identical 191-line brand
copies remain in both roots because no ownership/removal contract authorizes
removing either. Approved culls and explicitly bounded intake are the documented
exceptions, not permission to rewrite other imports.

External source configuration is disabled where supported, but 191 detectable
installed-only entries remain on this host. No timer, live discovery tree,
provider, hook or runtime engine was activated or removed. Review those only
under a later explicit activation/cleanup request.

## Earlier audit dispositions

The primary task calls `.trim-spec.md` earlier audit input. Its findings were
verified rather than treated as overriding active user policy:

| Finding | Outcome |
| --- | --- |
| F1 high/xhigh effort | Confirmed and preserved exactly. Recommend a representative-task experiment with medium default/high planning before any preference change. |
| F2 long core/developer duplication | CASD refs and pass9;9KB/150line target met, all controls preserved. Approved cull superseded splitting playwright-interactive. Brand mirror retained. |
| F3 reduced planning/title/postmortem/handoff ceremony | Deferred: conflicts with active AGENTS requirements. Preserve exact wording and route conditional procedure; no weakened policy claim. |
| F4 strict global commit policy/Claude permission cleanup | Deferred: active best-effort commit policy remains authoritative; permission cleanup is a separate safety/config review, not a token-reduction pass. Claude settings remain byte-identical. This series itself required green selected checks plus size/privacy gates. |
| F5 agent output | Real PTY/pipe/agent/plain/NO_COLOR checks;124B inventory summary with full errors/JSON/details retained. |
| F6 delegation/Claude routing | Claude already imports canonical AGENTS; specialist delegation remains explicit there. No duplicate policy added. |


### Intake sources.json disposition

The requested manual merge was reviewed, not replaced wholesale. PR33's pinned
source-ledger delta adds exactly one private authoring-incident record, with an
absolute local alias, no finding links and an explicit no-new-learning decision.
Its underlying private report is outside the approved skill paths and was not
imported. Privacy/scope disposition: exclude that record; do not create a dangling
public ledger entry. PR37 changes neither sources.json nor README. The public
ledger remains its newer489report/236finding snapshot; no reusable skill-runtime
learning delta is missing. README's relevant intake lines were merged by hand.
This is separate from outstanding canonical learning registration for incidents
created during this task. No private report text or local alias is published.

## Verification limits

Final selected suite239 tests / 391 subtests PASS;42/46 lexical routing and 233 source
entries / 0 drift PASS. Six inherited sanitized Python syntax errors prevent full
repository collection; the broader postmortem suite also retains one inherited
missing-fixture failure. Fresh final doctor: 35 inherited errors / 1 warning; zero new keys versus
pass0 and pass8. CLI exit0, audit status remains fail for inherited findings.
No claim of full-suite or whole-repository health is made.

Exact committed-tree privacy receipts cover all 12 passes. Precommit timing and
staged-size passes are root-observed; current retrospective privacy receipts are
separate evidence. The old history audit's1,604 candidates remain unadjudicated;
no clean-history claim or rewrite is authorized. Canonical postmortem-learning
registration outside the writable workspace remains outstanding; installed copies
were not edited. Native Plan Mode/title tool unavailable; written ExecPlan used.

Actual model triggering, provider usage, user review time, live install/apply,
GUI wrapped-copy behavior and production runtimes were not measured. No push,
chezmoi apply, refresh-config, model or effort change occurred.
