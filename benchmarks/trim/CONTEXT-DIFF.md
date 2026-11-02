# Before/after session context

Compare pinned current-main text with the trimmed branch, separating recurring description context from optional body loads. Inspect both token methods, then review each skill and the limits.

Baseline: `8662fa3c30da549fbdb20b8477c80e015e7d5236`. Candidate measured surfaces: `92a516ab704a086d3d2eb7c9cc5e31c7f6e038c6` (unchanged by this documentation pass).

## Session context totals

| Surface | Before bytes/4 tokens | After bytes/4 tokens | Difference | Change | Real tokenizer before → after |
| --- | ---: | ---: | ---: | ---: | ---: |
| AGENTS policy | 6,050.5 | 2,419.75 | -3,630.75 | -60.01% | 4,990 → 2,027 |
| Skill descriptions | 3,472.75 | 1,180 | -2,292.75 | -66.02% | 2,724 → 941 |
| Always-loaded: AGENTS + descriptions | 9,523.25 | 3,599.75 | -5,923.5 | -62.20% | 7,714 → 2,968 |
| Skill bodies: on-demand inventory | 109,142.5 | 53,435.75 | -55,706.75 | -51.04% | 97,588 → 47,085 |
| Config developer instructions (separate) | 179.25 | 0 | -179.25 | -100.00% | 135 → 0 |
| Existing collector total (includes developer) | 9,702.5 | 3,599.75 | -6,102.75 | -62.90% | 7,849 → 2,968 |

## Skill-by-skill context diff

| Skill | Loaded before | Loaded after | Mark / gate | Description bytes before → after | Description tokens (bytes/4) before → after |
| --- | --- | --- | --- | ---: | ---: |
| adapt | yes | no | removed by cull | 143 → 0 | 35.75 → 0 |
| ai-ux-deslop | yes | yes | added-then-denied; retained, new on main | 165 → 86 | 41.25 → 21.5 |
| ai-workflow-doctor | yes | yes | kept | 200 → 158 | 50 → 39.5 |
| animate | yes | no | removed by cull | 134 → 0 | 33.5 → 0 |
| arrange | yes | no | removed by cull | 151 → 0 | 37.75 → 0 |
| audit | yes | no | removed by cull | 194 → 0 | 48.5 → 0 |
| bolder | yes | no | removed by cull | 132 → 0 | 33 → 0 |
| brand-system-designer | yes | yes | kept | 383 → 383 | 95.75 → 95.75 |
| clarify | yes | no | removed by cull | 124 → 0 | 31 → 0 |
| colorize | yes | no | removed by cull | 130 → 0 | 32.5 → 0 |
| commit-dirty | yes | yes | kept | 354 → 159 | 88.5 → 39.75 |
| commit-plan | yes | no | merged into commit-plan-push | 343 → 0 | 85.75 → 0 |
| commit-plan-push | yes | yes | kept | 394 → 155 | 98.5 → 38.75 |
| commit-session | yes | yes | kept | 434 → 245 | 108.5 → 61.25 |
| context-handoff | no | yes | added on trim branch | 0 → 173 | 0 → 43.25 |
| critique | yes | no | removed by cull | 179 → 0 | 44.75 → 0 |
| delight | yes | no | removed by cull | 143 → 0 | 35.75 → 0 |
| design-taste-frontend | yes | no | removed by cull | 202 → 0 | 50.5 → 0 |
| distill | yes | no | removed by cull | 111 → 0 | 27.75 → 0 |
| extract | yes | no | removed by cull | 180 → 0 | 45 → 0 |
| feedback-memory | yes | yes | kept | 338 → 166 | 84.5 → 41.5 |
| find-skills | yes | no | removed by cull | 303 → 0 | 75.75 → 0 |
| fish-alias | yes | yes | kept | 166 → 132 | 41.5 → 33 |
| frontend-design | yes | yes | kept | 254 → 106 | 63.5 → 26.5 |
| full-output-enforcement | yes | no | removed by cull | 203 → 0 | 50.75 → 0 |
| gh-fix-ci | yes | no | removed by cull | 313 → 0 | 78.25 → 0 |
| grok-cli-handoff | no | yes | added on trim branch | 0 → 123 | 0 → 30.75 |
| hallmark | yes | yes | added (new on main, kept); PASS | 252 → 97 | 63 → 24.25 |
| harden | yes | no | removed by cull | 169 → 0 | 42.25 → 0 |
| high-end-visual-design | yes | no | removed by cull | 234 → 0 | 58.5 → 0 |
| imagegen | yes | no | removed by cull | 328 → 0 | 82 → 0 |
| impeccable | no | yes | added on trim branch | 0 → 92 | 0 → 23 |
| last30days | yes | yes | kept | 246 → 246 | 61.5 → 61.5 |
| lean-instructions | no | yes | added on trim branch | 0 → 69 | 0 → 17.25 |
| leetcode-init | yes | no | removed by cull | 216 → 0 | 54 → 0 |
| long-task-harness | yes | no | merged into context-handoff | 365 → 0 | 91.25 → 0 |
| metaprompt | yes | yes | kept | 222 → 130 | 55.5 → 32.5 |
| metaprompt-alxve | yes | no | removed by cull | 488 → 0 | 122 → 0 |
| metaprompt-run | yes | yes | kept | 221 → 221 | 55.25 → 55.25 |
| minimalist-ui | yes | no | removed by cull | 145 → 0 | 36.25 → 0 |
| morning | yes | yes | kept | 257 → 257 | 64.25 → 64.25 |
| next-tasks | yes | yes | kept | 423 → 127 | 105.75 → 31.75 |
| night | yes | yes | kept | 300 → 148 | 75 → 37 |
| normalize | yes | no | removed by cull | 67 → 0 | 16.75 → 0 |
| onboard | yes | no | removed by cull | 149 → 0 | 37.25 → 0 |
| open-pr | yes | no | removed by cull | 286 → 0 | 71.5 → 0 |
| openai-docs | yes | no | removed by cull | 372 → 0 | 93 → 0 |
| optimize | yes | no | removed by cull | 138 → 0 | 34.5 → 0 |
| overdrive | yes | no | removed by cull | 228 → 0 | 57 → 0 |
| pdf | yes | no | removed by cull | 248 → 0 | 62 → 0 |
| personal-context | yes | yes | kept | 358 → 261 | 89.5 → 65.25 |
| playwright | yes | yes | kept | 209 → 209 | 52.25 → 52.25 |
| playwright-interactive | yes | no | removed by cull | 94 → 0 | 23.5 → 0 |
| polish | yes | no | removed by cull | 123 → 0 | 30.75 → 0 |
| postmortem-memory | yes | yes | kept | 160 → 124 | 40 → 31 |
| quieter | yes | no | removed by cull | 116 → 0 | 29 → 0 |
| readme-recruiter-sync | yes | yes | kept | 236 → 98 | 59 → 24.5 |
| redesign-existing-projects | yes | no | removed by cull | 225 → 0 | 56.25 → 0 |
| screenshot | yes | no | removed by cull | 220 → 0 | 55 → 0 |
| second-brain-session | yes | yes | kept | 278 → 278 | 69.5 → 69.5 |
| shadcn | no | yes | added on trim branch | 0 → 98 | 0 → 24.5 |
| skill-eval | no | yes | added on trim branch | 0 → 107 | 0 → 26.75 |
| smoke-test-capture | yes | yes | kept | 194 → 194 | 48.5 → 48.5 |
| teach-impeccable | yes | no | merged into frontend-design | 148 → 0 | 37 → 0 |
| transcribe | yes | no | removed by cull | 216 → 0 | 54 → 0 |
| typeset | yes | no | removed by cull | 140 → 0 | 35 → 0 |
| ui-ux-pro-max | yes | no | removed by cull | 147 → 0 | 36.75 → 0 |
| vercel-react-best-practices | no | yes | added on trim branch | 0 → 78 | 0 → 19.5 |

## Loaded only before

adapt, animate, arrange, audit, bolder, clarify, colorize, commit-plan, critique, delight, design-taste-frontend, distill, extract, find-skills, full-output-enforcement, gh-fix-ci, harden, high-end-visual-design, imagegen, leetcode-init, long-task-harness, metaprompt-alxve, minimalist-ui, normalize, onboard, open-pr, openai-docs, optimize, overdrive, pdf, playwright-interactive, polish, quieter, redesign-existing-projects, screenshot, teach-impeccable, transcribe, typeset, ui-ux-pro-max.

## Loaded only after

context-handoff, grok-cli-handoff, impeccable, lean-instructions, shadcn, skill-eval, vercel-react-best-practices.

## Measurement limits

“Loaded” in the skill table means its description is included in the static canonical repository catalog. It does not prove that a host exposed it or that a model invoked its body. Body-loaded flags are unknown (JSON null); the body row prices the complete on-demand inventory, not a typical session or an instruction to load every body. Explicit-only descriptions are conservatively counted, even if a runtime hides them.

The main baseline already contains ai-ux-deslop and hallmark, so both are loaded-before and loaded-after; “added” refers to their arrival since410feaa, not an extra after-only entry. AI UX remains denied and retained. Always-loaded here follows the requested AGENTS+descriptions boundary; the existing collector additionally counts config developer instructions, shown separately to reconcile its9,702.5→3,599.75 estimate.

Real tokenizer counts use tiktoken o200k_base on the actual public text, summed independently per file/description/body. They are real counts for that encoding, not verified tokenizer counts for the configured model, provider billing, cache behavior, system/developer prompts, history or tool output. No live session trace was sampled. External/built-in/plugin catalogs, names, paths, wrappers and triggered references are excluded; their before-host state is unavailable. The duplicate tracked .agents brand mirror is measured separately in JSON and excluded from canonical totals, as in the existing collector. No installed catalog or configuration was activated.
