# Model Profiles

Adapt a compiled prompt to its named model or runtime using supported facts.
Check the profile date and source tags, apply the relevant guidance, and keep
unsupported behavior marked unknown.

Cache stamp: 2026-07-14. Re-verify on a model-family or API behavior change, or
when this file is older than 90 days.

Use profiles as conservative compile-time hints, not marketing truth. Every
attribute ends with one provenance tag:

- `[official: <direct URL>, verified 2026-07-14]`
- `[heuristic]`
- `[unknown]`

If the named version is not covered, use only family-wide facts that still
apply and leave the rest unknown.

## Unknown target

- scaffolding_weight: medium explicitness; avoid target-specific mechanics [heuristic]
- instruction_style: clear goal, inputs, constraints, and output contract [heuristic]
- long_context_layout: bulk context first and final query last [heuristic]
- structured_output_path: explicit prompt schema when no native path is known [heuristic]
- sampling_constraints: unknown [unknown]
- surface_notes: keep the prompt self-contained and paste-portable [heuristic]
- detection_hints: no reliable target name or surface context [heuristic]

## OpenAI GPT API or ChatGPT

- scaffolding_weight: lean to medium; state each instruction once and retain examples only when they encode a real requirement [official: https://developers.openai.com/api/docs/guides/latest-model.md, verified 2026-07-14]
- instruction_style: state goal, context, hard constraints, approval boundaries, success criteria, and output format [official: https://developers.openai.com/api/docs/guides/latest-model.md, verified 2026-07-14]
- long_context_layout: unknown across the full family [unknown]
- structured_output_path: prefer an available API schema; otherwise specify the exact shape in the prompt [heuristic]
- sampling_constraints: unknown unless the caller supplies a documented model-specific API contract [unknown]
- surface_notes: define autonomy and confirmation boundaries for agentic work [official: https://developers.openai.com/api/docs/guides/latest-model.md, verified 2026-07-14]
- detection_hints: system or user names ChatGPT, OpenAI API, Responses API, or a GPT model [heuristic]

## Claude API or chat

- scaffolding_weight: medium; use clear direct instructions and explicit output constraints [official: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, verified 2026-07-14]
- instruction_style: use descriptive XML slots and 3 to 5 relevant examples when examples materially steer the result [official: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, verified 2026-07-14]
- long_context_layout: place long documents above the query and ask for quote grounding [official: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, verified 2026-07-14]
- structured_output_path: specify the desired positive format and use consistent descriptive tags [official: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, verified 2026-07-14]
- sampling_constraints: unknown unless a version-specific official API page is supplied [unknown]
- surface_notes: last-assistant-turn prefill support varies by model generation; do not rely on it without version verification [heuristic]
- detection_hints: system or user names Claude, Claude API, Opus, Sonnet, or Haiku [heuristic]

## Gemini API or chat

- scaffolding_weight: medium; use direct, well-structured instructions and explicit constraints [official: https://ai.google.dev/gemini-api/docs/prompting-strategies, verified 2026-07-14]
- instruction_style: use one consistent delimiter style and define ambiguous parameters [official: https://ai.google.dev/gemini-api/docs/prompting-strategies, verified 2026-07-14]
- long_context_layout: supply large context first and place the specific query at the end [official: https://ai.google.dev/gemini-api/docs/prompting-strategies, verified 2026-07-14]
- structured_output_path: prefer the API structured-output feature for complex JSON schemas [official: https://ai.google.dev/gemini-api/docs/prompting-strategies, verified 2026-07-14]
- sampling_constraints: keep defaults unless current version-specific official guidance says otherwise [heuristic]
- surface_notes: reference each modality explicitly when combining text, image, audio, or video [official: https://ai.google.dev/gemini-api/docs/prompting-strategies, verified 2026-07-14]
- detection_hints: system or user names Gemini, Google AI Studio, or Gemini API [heuristic]

## Small or local models

- scaffolding_weight: high explicitness with short steps and compact examples [heuristic]
- instruction_style: narrow the task and repeat critical constraints near their output fields [heuristic]
- long_context_layout: keep only relevant context and place the task after it [heuristic]
- structured_output_path: provide a small exact schema plus a valid example [heuristic]
- sampling_constraints: model and runtime dependent [unknown]
- surface_notes: validate output externally and split complex work into smaller passes [heuristic]
- detection_hints: user names a local, small, or open-weight runtime [heuristic]
