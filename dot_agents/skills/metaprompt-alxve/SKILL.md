---
name: metaprompt-alxve
description: >-
  Use for /metaprompt-alxve or an explicit request for the original alxve
  compiler. It supports phrasing for another chat, role, model, agent, or
  target system, a reusable template or recurring prompt, input/output examples,
  or a named target. General prompt-authoring requests use metaprompt. A follow-up standalone `go` runs
  only the accepted pass. Do not trigger for a one-word fact lookup. Always
  return a prompt, including a tightened one-liner for trivial asks; never a
  direct answer.
---

# Metaprompt Alxve

Every invocation returns a compiled prompt, execution recommendation, and
explicit gate. Complexity changes prompt weight, never whether a prompt is
produced. Trivial requests get one or two clean sentences.

Use five stages:

1. Infer goal, deliverable, constraints, success criterion, language, target,
   and mode: fresh, sharpened, reusable, or example-derived. Default safely;
   ask only when material intent lacks a safe default.
2. Compile at Trivial, Standard, or Complex weight; keep quality guidance
   shorter than task instructions.
3. Save every compiled prompt before presenting the gate in the repository-root
   `prompts/` directory: use a concise kebab-case Markdown filename and a
   non-destructive suffix on collision. The saved file contains the compiled
   prompt only; if the save fails, report its actionable error instead of
   presenting the gate.
4. Present the prompt and gate. Treat changes as a revision and re-gate.
5. Require a fresh standalone `go` for every execution and every high-stakes
   pass. An original "compile and run" request never bypasses this boundary.
   Only literal `go` authorizes the currently gated pass; other words or
   embedded signals do not. Logistics riders are revisions and re-gate.

<!-- metaprompt-contract: reference-loading-v1 -->
Read [compilation rules](references/compilation-rules.md) for Standard or Complex compilation, sharpening, or evaluation.
Read [execution routing](references/execution-routing.md) only after a standalone run signal.
Read [examples](references/examples.md) only when an example would resolve a compilation choice.
Read [model profiles](references/model-profiles.md) only when target-specific adaptation materially changes the prompt.

<!-- metaprompt-contract: execution-routing-v1 -->
Choose execution mode in this order, first match wins: recurring/time-driven;
goal/until-done; research/audit/large fan-out; destructive/new-build planning;
normal execution. Never claim a user-only command ran: provide the exact
command and why. The user may override the mode.

<!-- metaprompt-contract: output-gate-v1 -->
For one pass, close the prompt fence once, then put metadata outside it:

````
```prompt
<the compiled, paste-ready prompt>
```
Saved: prompts/<filename>.md
Run: <where to run>. Weight: <trivial|standard|complex>.
Target: <only when adaptation materially changed compilation>
Template: yes <only for reusable {{variable}} prompts>
Assumptions: <only when needed; otherwise omit>
````

For Judge -> Rewrite -> Re-check, emit three numbered prompt blocks, each
self-contained. Gate only block 1; after its result, gate block 2 with a new
`go`, then do the same for block 3. End every compile with one gate line in the
user's language naming the mode and asking for `go` or changes. Keep prompts
paste-portable and honor active repository instructions and durable
`feedback-memory` preferences.
