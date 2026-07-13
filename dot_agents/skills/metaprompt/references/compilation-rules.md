# Compilation Rules

<!-- metaprompt-reference: compilation-rules-v1 -->

## Two input modes

1. **Compile fresh:** The user describes intent; build a new prompt.
2. **Sharpen existing:** The user supplies a prompt or skill. Do not silently
   rebuild it. Compile a prompt that preserves the original intent, checks it
   against this recipe, and on execution produces the improved version plus a
   two-to-four-line changelog. For a high-stakes reusable target, produce a
   judge pass first and keep rewriting as a separate pass. For an everyday
   sharpen, one run may produce the improvement and changelog.

Both modes still return a compiled prompt plus the gate. The improved artifact
is the output of running that prompt, never a substitute for the prompt.

## Complexity gate

Match prompt weight to the task:

1. **Trivial:** A quick fact, one-line rewrite, simple lookup, yes/no, or
   format-only request. Return one or two direct sentences without role-play or
   scaffolding.
2. **Standard:** Focused content, analysis, or one artifact. Use role, task,
   output format, and one example only if useful.
3. **Complex / high-stakes:** A spec, multi-step build, evaluation, reusable
   artifact, or downstream dependency. Use the full recipe, artifact slot,
   self-critique, and verification.

When uncertain, choose Standard. The quality block must remain shorter than
the task instructions it wraps; otherwise drop one weight.

## Quality core

### Trivial

Insert no quality block. It adds cost and ceremony without improving the task.

### Standard

Emit this in the user's language, scoped to the whole output:

```text
Treat your first complete answer as a draft floor, not the submission. Before you deliver, name the single biggest weakness of the draft against the goal, then fix it. Apply this to the whole response, not just the first part. Show only the final version.
```

Use one internal critique pass, no written rubric and no candidate tournament.
For a German target, emit this verbatim:

```text
Behandle deine erste vollstaendige Antwort als Boden, nicht als Abgabe. Bevor du lieferst, nenne die groesste Schwaeche des Entwurfs gegenueber dem Ziel und behebe sie. Wende das auf die ganze Antwort an, nicht nur den ersten Teil. Zeig nur die finale Version.
```

### Complex / high-stakes

Use this task-derived bar in the user's language:

```text
<quality_bar>
Before writing, define the 3 to 5 dimensions that separate an exceptional answer for THIS task from a merely correct one. Derive them from the task, not generic quality words; for each, one concrete observable thing a top answer does. Set the bar as if your first draft will fall short.
If the task is too underspecified to derive concrete dimensions, say so and ask one clarifying question instead of inventing generic ones.
Then write the deliverable. Treat your first complete answer as the floor: stop at the answer an expert could not improve in one more pass, not the longest one. Apply the bar to every section, not just the first.
Then map each dimension to where the result meets it; if one is weakly met, do exactly one targeted revision of that part, then stop. One revision, no looping.
Keep the bar as brief working notes; show only the final deliverable plus the one-line-per-dimension check.
</quality_bar>
```

Keep it single-pass. Do not embed a three-approach tournament: self-anchoring and
self-grading can reduce quality. True best-of-N belongs in separate passes only
when the user explicitly requests a tournament.

For a German target, emit this verbatim:

```text
<quality_bar>
Bevor du schreibst, definiere die 3 bis 5 Dimensionen die eine herausragende Antwort fuer GENAU diese Aufgabe von einer bloss korrekten trennen. Leite sie aus der Aufgabe ab, nicht aus generischen Qualitaetswoertern; pro Dimension eine konkrete beobachtbare Sache die eine Top-Antwort tut. Setz die Latte so, als wuerde dein erster Entwurf sie verfehlen.
Wenn die Aufgabe zu unterspezifiziert ist um konkrete Dimensionen abzuleiten, sag das und stell eine Rueckfrage statt generische zu erfinden.
Dann schreib das Deliverable. Behandle deine erste vollstaendige Antwort als Boden: hoer bei der Antwort auf die ein Experte in einem weiteren Durchgang nicht verbessern koennte, nicht bei der laengsten. Wende die Latte auf jeden Abschnitt an, nicht nur den ersten.
Dann ordne jede Dimension der Stelle zu wo das Ergebnis sie erfuellt; wenn eine schwach erfuellt ist, mach genau eine gezielte Revision dieses Teils und stopp dann. Eine Revision, keine Schleife.
Halt die Latte als kurze Arbeitsnotizen; zeig nur das finale Deliverable plus den Ein-Zeilen-pro-Dimension-Check.
</quality_bar>
```

### Dosing and swaps

1. Hard-cap the bar at 3 to 5 dimensions and exactly one targeted revision.
2. Never add blanket "always be thorough" or "go above and beyond" language.
3. Build and analysis prompts get: "When you choose an approach, commit;
   revisit only on information that directly contradicts your reasoning."
   Omit it when comparing approaches is itself the deliverable.
4. For factual or claim-heavy output, use a contradiction-check tail instead
   of the bar: "After your draft, list up to 5 short factual questions whose
   answers could contradict it, answer each, correct on any conflict." Skip it
   for creative or values-based tasks. Never run bar and contradiction-check
   tail in one prompt.
5. For pure rating or evaluation, require harsh evidence-bound scoring, a
   quote per score, and low verdicts; do not rewrite in the same pass.
6. Audit, review, and evaluation prompts add: "report every issue, do not
   filter; a downstream step ranks."
7. Conversational, normative, and values-based asks stay Standard even when
   important; Complex scaffolding makes them over-hedge.
8. When a target lacks hidden reasoning, keep bar notes terse and separate or
   internal so scratch work does not leak into the visible answer.

The core is a same-pass floor raiser. A real grade, launch decision, or other
high-stakes external call still separates judge and author across passes.

## Compile recipe

Apply only what fits:

1. **Role in one or two sentences.** State a concrete job, not a grand persona.
2. **Show, do not describe.** If examples exist, add an
   `<examples>...</examples>` slot. If the task evaluates or transforms an
   artifact, include an explicit `<input>...</input>` slot and tell the user to
   paste it. Never evaluate an unattached artifact.
3. **Specify output format.** Name the table columns, list length, JSON schema,
   or code-block form. Reused or machine-parsed output makes format a contract.
4. **Use neutral framing.** Remove leading language that telegraphs the desired
   answer. For reviews, invite harsh or low verdicts and require concrete
   evidence for every claim.
5. **Separate judge from author.** If a task evaluates and rewrites, evaluate
   first, let the user read it, rewrite in a fresh pass, then re-evaluate in a
   fresh pass. Do the same for explicit best-of-N tournaments. Everyday
   same-pass quality checks are different and remain allowed.
6. **Apply the Quality core** at Standard and Complex weights.
7. **Verification / stop conditions.** Complex prompts end with a check:
   re-read against the goal, run the test, or validate the format. Define done
   and instruct the model to ask rather than fabricate when input is missing.
8. **Decompose** multi-job asks into ordered steps.

## Prompt mechanics

Treat model mechanics as volatile facts to verify against current official
references rather than permanent doctrine:

1. Some models accept only adaptive reasoning and reject custom sampling or
   explicit thinking-budget parameters.
2. Some families reject last-assistant-turn prefill. Prefer structured output
   for forced JSON; use "respond directly without preamble" when appropriate.
3. Strong models follow literally and may not generalize a rule across items.
   Scope universal instructions to every section; use coverage mode for audits.
4. For an external or different model, keep prompts self-contained. XML tags
   and explicit formats remain portable.

## Target awareness

When a role or system is named or obvious, tailor the prompt to its job and
constraints, including response format, style, ask-before-build rules, and
verification expectations. Keep the output paste-portable: target context may
shape the prompt but must not become a dependency. Write in the user's language
and honor their established house style.
