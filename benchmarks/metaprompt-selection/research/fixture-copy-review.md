# Fixture copy-boundary review

Reviewed 2026-10-03 before heldout freeze. Scope: all 26 fixture authoring requests, raw task prompts, compiler context, solver packets/template bindings, answer keys, reference solutions, and all seven coding docstrings/public and private assertions. No models were called and no fixtures were edited. Only the reported development copy-span ambiguity was exposed as runtime evidence; heldout recommendations below come from static contract comparison.

## Required clarification before heldout freeze

Apply each applicable clarification to both `task_prompt` and the corresponding text in `authoring_request`, preserving template placeholders. Documentation alone cannot define a requirement withheld from the compiler. Leave answer values and packets unchanged. Do not apply a global punctuation-stripping rule: punctuation inside copied content must remain intact.

| Cases | Exact clarification to add | Reason |
| --- | --- | --- |
| `selection-sharpen-summary-corrections`, `selection-template-handoff` | `Copy the action/job as the text inside square brackets, without the brackets. Copy the owner as the name token and the date/due as the YYYY-MM-DD token, excluding surrounding separators and sentence punctuation.` | The supplied final date is followed immediately by a period; the key excludes that period but the copy boundary is not explicit. This is the material heldout analogue of the development ambiguity. |
| `selection-create-summary-handoff`, `selection-sharpen-summary-injection` | `Copy action/task text from inside square brackets without the brackets; copy supplied person/owner names and dates without the surrounding field separators or sentence punctuation.` | Makes the same handoff convention explicit across fixtures; existing order/missing-value instructions remain authoritative. |
| `selection-create-writing-draft`, `selection-template-draft` | `A subject or fact string is the remainder of its Subject: or Fact: line after the label and its separating space; exclude the label and newline, and preserve the remainder verbatim.` | Keys exclude labels and separator spaces, whereas “supplied subject/fact strings” does not explicitly delimit the copied field. |
| `selection-sharpen-writing-correction` | `A subject or correction string is the remainder of its Subject: or Correction: line after the label and its separating space; exclude the label and newline, and preserve the remainder verbatim.` | Same line-label boundary issue as the draft fixtures. |
| `selection-create-research-policy`, `selection-create-research-conflict`, `selection-sharpen-research-scope`, `selection-template-policy`, `selection-template-conflict` | `In sources, use the bare source ID from inside its square brackets, without the brackets.` | Packets label sources `[A]` etc.; exact-match keys require `A` etc. Both notations are plausible source IDs unless the output notation is defined. |
| `selection-create-research-policy`, `selection-template-policy` | `Copy a quoted policy value as the text inside its quotation marks, without the quote delimiters or following sentence punctuation.` | Exact quoted-value extraction should not depend on an unstated syntactic convention. Preserve the string type already required by the task. |
| `selection-create-extraction-orders`, `selection-sharpen-extraction-duplicates` | `For quoted code/key fields, copy the value inside the quotation marks without the quote delimiters.` | Low-risk conventional interpretation, but explicit boundaries avoid exact-match penalties for alternate literal-copy readings. |

These are generic span definitions, not fixture answers or additional evidence. No change is needed to the existing JSON object/array types, integer/null distinctions, array ordering, duplicate preservation, missing-value sentinels, conflict/precedence rules, or strict greater-than filter. CSV quoting is already an explicit parsing requirement and the reference correctly decodes doubled quotation marks.

## Development history

`selection-dev-create-brief` says to copy wording after `Decision:` from `Decision: audit the kiosk. It was ...`; its key omits the terminal period. That boundary was undefined at development time. Preserve and identify the original development result as an ambiguous historical probe rather than using it as evidence of candidate quality. If a new development version is used, define the span explicitly, for example: `Copy the first sentence after Decision:, excluding the label, separating space, and terminating sentence period.` A revised probe must have its own input version; do not relabel the existing output as having followed the revised instruction.

## Checked without further findings

All 19 noncoding keys and references agree on JSON structure, value types, order, and supplied evidence. Missing/unavailable-attachment cases require unknown plus an empty sources array, so they do not expose a copied-value boundary. Template filter uses JSON record values with explicit string output and a strict greater-than threshold. All six heldout coding contracts and the development coding contract match the private assertions and reference implementations; no private assertion adds an unstated boundary, mutation, error, or ordering requirement. Coding output is explicitly complete source without fences, and the target-only/public-signature/public-test stop rules are already stated.

No heldout outputs were inspected. No request to tune keys, loosen scoring, or change case semantics is made.
