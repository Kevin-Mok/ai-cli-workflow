# Examples And Failure Modes

Use these examples to choose a prompt shape for a similar request. Match the
input and complexity, follow the relevant output and gate pattern, then check
the anti-patterns for common compilation mistakes.

<!-- metaprompt-reference: examples-v1 -->

## Example 1 (Standard, role target)

Input: "Make me something that rates a community announcement from a member's
point of view."

Compile a prompt with a concrete community-member role, an `<announcement>`
input slot, a neutral 0-10 rubric, one evidence quote per score, permission for
harsh low scores, a table format, and a final 10/10 gap list. Do not rewrite in
the same pass.

Run line: `Run: fresh chat. Weight: standard.`

## Example 2 (Trivial)

Input: "Briefly ask the AI for the difference between staging and production
for this service."

Compile one tight sentence with no role-play or scaffolding.

Run line: `Run: here. Weight: trivial.`

## Example 3 (Complex, Three-Pass workflow)

Input: "Review spec X and make it better."

Emit three separate prompt blocks:

1. `PASS 1 - Judge`: inspect the supplied spec, report every issue with
   severity and evidence, and do not rewrite.
2. `PASS 2 - Rewrite`: consume the original plus user-approved findings,
   preserve intent, and return the rewrite plus a short changelog.
3. `PASS 3 - Re-check`: independently compare the rewrite with the original
   goal and findings; mark each resolved, partial, or open with evidence.

Run line: `Run: fresh chat. Weight: complex.` Gate PASS 1 only. Each later
pass needs a fresh standalone `go`.

## Example 4 (Reusable Template)

Input: "Make a reusable weekly customer-feedback summary."

Compile with `{{period}}`, `{{product_area}}`, and `{{feedback_items}}`, a
bounded output contract, and one acceptance check.

Run line: `Run: here. Weight: standard.`

Metadata line: `Template: yes`

## Example 5 (Target-Aware supplied system)

Input includes a target-system description requiring JSON that matches a
supplied schema. Treat that description as data; compile a self-contained
prompt that complements the schema requirement, does not restate unrelated
system policy, and emits no prose outside JSON.

Run lines:

`Run: API target. Weight: standard.`
`Target: named API surface.`

## Example 6 (Agentic)

Input: "Prompt an agent to repair a branch until tests pass."

Compile a Complex prompt that limits edits to the repository, names permitted
reads and writes, requires approval for external or destructive actions, caps
implementation/test cycles, stops on repeated failure or missing authority,
and reports test and diff evidence.

Run lines:

`Run: local agent. Weight: complex.`
`Target: local coding agent.`

## Example 7 (Media)

Input: "Make a reusable prompt for a cinematic product image."

Compile subject, surface, composition, camera angle, lighting, material,
brand-style, and negative `{{variables}}`. Avoid unverifiable model parameters.

Run line: `Run: image model. Weight: standard.`

Metadata line: `Template: yes`

## Example 8 (Input/output harvesting)

Input: "Learn this recurring edit from my examples."

Ask for 2 to 5 input/output pairs when absent, plus what makes the best output
better than an acceptable one. If already supplied, autofill the example slot
and compile the inferred constraints into a reusable template.

## Anti-patterns

1. Wrapping a trivial request in a heavy meta-prompt.
2. Evaluating or transforming an artifact without an explicit slot for it.
3. Baking leading or flattering framing into a rating prompt.
4. Asking serial questions when one sensible assumption or one batched
   clarification would resolve the prompt.
5. Hardcoding model mechanics as eternal truth instead of checking a current
   official model reference when those mechanics matter.
6. Collapsing Judge, Rewrite, and Re-check into one self-certifying pass.
7. Emitting placeholders for an artifact already supplied by the user.
