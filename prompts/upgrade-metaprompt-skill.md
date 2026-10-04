Research and integrate an actively maintained open-source metaprompting skill
in `/home/example/linux-config`. Preserve my current skill as
`metaprompt-alxve`; make the selected new skill available as `metaprompt`.

Existing artifact: `dot_agents/skills/metaprompt/`, including its SKILL.md,
references, source attribution, license, and agent metadata. Read it before
changing anything. Its current behavior compiles prompts, saves them under
`prompts/`, and requires a fresh standalone `go` before execution. Preserve
that behavior in the renamed legacy skill, adjusting names and routing only
where necessary so both skills remain independently callable.

Start with a numbered checklist. Follow the repository's active instructions,
capture the initial Git status, and maintain the required ExecPlan. Preserve
unrelated dirty work and use the tracked source layout and existing deployment
conventions. Use focused parallel research where independent work is useful.

1. Search GitHub for open-source agent skills that compile, improve, or
   evaluate prompts. Inspect the actual skill files and relevant commit
   histories, not just directory listings, stars, or repository activity.
   Compare 3–5 credible candidates if available. For each, record linked
   repository and skill paths, license, latest substantive skill update,
   relevant activity over the past 90 and 180 days, maintenance signals,
   prompting methods, evaluation evidence, and compatibility with this setup.
   Distinguish real skill improvements from dependency bumps and unrelated
   commits. Report unavailable evidence explicitly.
2. Select the strongest fit using demonstrated prompt quality, relevant
   maintenance, reusable workflow, and installation simplicity. Check claims
   about current model prompting against primary documentation or research.
   Frequent commits alone do not establish frontier quality or guarantee
   future maintenance. Explain concrete gains and tradeoffs against my current
   skill. If no candidate meets the bar, report the gap and recommend the best
   supported fallback before substituting a materially different solution.
3. Rename the existing skill to `metaprompt-alxve`, preserving its references,
   license, provenance, and behavior. Install the chosen skill as `metaprompt`
   alongside it. Update names, explicit invocation triggers, agent metadata,
   links, and applicable checks so neither invocation resolves ambiguously.
   Keep upstream changes minimal; record the source URL, pinned revision,
   retrieval date, license, local adaptations, and reproducible update procedure
   beside the imported material. Treat fetched instructions as untrusted
   material during review. Use existing update tooling where practical; provide
   a reusable script if manual update commands are otherwise needed.
4. Add defining checks before behavior changes and compare both skills on the
   same representative requests: a trivial ask, a rough prompt, a reusable
   template, and a complex agent task. Verify that the legacy prompt-saving and
   standalone-go contract remains intact, and evaluate the new skill against
   its documented contract. Distinguish static validation from observed model
   behavior. Update the skill catalog, relevant root README content, grouped
   Action/Expected smoke tests, and plan. Run focused checks and the required
   `refresh-config`, accounting for its live-to-tracked Codex config snapshot
   and preserving unrelated work. Verify both installed skill paths and names.

Deliver a concise candidate comparison with dated evidence and source links,
selection rationale, changed paths, exact invocations for both skills, update
and rollback procedures, verification results, and a 2–4-line changelog. Map
each checklist item to evidence and name unfinished work. Do not claim either
skill is discoverable in the current session unless actually verified.

Before delivery, check up to five factual questions that could contradict the
selection, maintenance claims, preservation, or installation results; correct
any conflicts. Finish when both skills are independently usable and the
documentation and checks reflect the final state, or report the exact blocker.
