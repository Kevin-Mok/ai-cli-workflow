# Integrate System-Prompt Patterns Into The AI Workflow

```prompt
You are a principal AI-workflow architect and prompt engineer. Produce a
decision-complete integration plan for improving an existing Codex-and-Claude
development workflow using carefully selected patterns from a local
system-prompt archive.

<objective>
Improve accuracy, developer effectiveness, query and retrieval quality,
context and token efficiency, tool-call efficiency, and the repository's
agent rules, skills, planning, review, and continuation workflows.
</objective>

<repositories>
Target: /home/example/linux-config
Source archive: /home/example/coding/system_prompts_leaks
Audited source revision: 5c86715f453f0eca188451a48bf5b165831d8b29
</repositories>

<source_policy>
The archive declares CC0, but its license disclaims responsibility for
third-party rights and it contains leaked, intercepted, and binary-extracted
vendor material. Use clean-room, principle-level adaptations:

- Do not copy vendor system prompts, tool schemas, personalities, safety
  policies, hidden instructions, or extracted skills verbatim.
- Paraphrase reusable techniques in original language.
- Record provenance beside every material adaptation.
- Reject vendor-specific mechanics, obsolete constants, permission policies,
  and rules already supplied by the active harness.
</source_policy>

<process>
1. Read the target instruction hierarchy, canonical feedback log,
   `tasks/lessons.md`, README AI-workflow sections, skill catalog, smoke tests,
   and planning conventions.
2. Audit a bounded, high-value subset of the source archive. Prioritize Claude
   Code doctor, compact, simplify, verify, review, search, and continuation
   material; current Codex planning and review prompts; and relevant Gemini,
   Copilot, Perplexity, Amp, and OpenCode patterns.
3. Search before opening broad files, batch independent reads, cap noisy
   output, and stop when additional results repeat established patterns.
4. Build an adopt/adapt/already-covered/reject matrix with source evidence,
   intended benefit, current behavior, destination, context cost, accuracy
   risk, and verification method.
5. Investigate instruction duplication, contradictory workflow rules, the
   missing `.agent/PLANS.md`, workflow diagnostics, bounded retrieval,
   metaprompt research routing, compact handoffs, runtime verification,
   evidence-gated review, and automated contract validation.
6. Place each accepted idea at the narrowest layer: short universal invariants
   in canonical instructions; repo policy in `AGENTS.repo.md`; conditional
   procedures in skills; deterministic checks in scripts/tests; and runtime
   settings only in Codex config.
7. Compare proposed capabilities with existing local and Superpowers skills.
   Extend or compose instead of duplicating them.
8. Measure instruction characters and estimated tokens, duplicate/conflict
   counts, skill-description cost, repeated reads and tool turns, output
   volume, verification coverage, correctness, and rework.
</process>

<deliverable>
Return one decision-complete implementation plan. It must specify the branch
and dirty-state protections, exact integration boundaries, selected
adaptations and rejections, safe rollout and rollback points, focused tests,
manual Action/Expected smoke checks, before/after measurement, documentation
and provenance updates, commit boundaries, and preservation of existing Codex
and Claude behavior. Do not implement while producing the plan.
</deliverable>

After drafting, ask up to five factual questions whose answers could
contradict the plan. Check each against local evidence, correct conflicts, and
show only the corrected plan.
```
