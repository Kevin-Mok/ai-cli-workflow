# Examples And Failure Modes

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

## Example 3 (Complex, evaluation with separate rewrite)

Input: "Review spec X and make it better."

Compile a senior-reviewer prompt with an `<input>` slot, the task-derived
`<quality_bar>`, coverage mode, and a table of issue, severity, and evidence.
Keep the rewrite in a separate pass after the user reads the evaluation, then
verify the rewrite in a fresh pass. Do not let the model grade its own rewrite.

Run line: `Run: fresh chat. Weight: complex.`

## Anti-patterns

1. Wrapping a trivial request in a heavy meta-prompt.
2. Evaluating or transforming an artifact without an explicit slot for it.
3. Baking leading or flattering framing into a rating prompt.
4. Asking serial questions when one sensible assumption or one batched
   clarification would resolve the prompt.
5. Hardcoding model mechanics as eternal truth instead of checking a current
   official model reference when those mechanics matter.
