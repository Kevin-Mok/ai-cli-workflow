---
name: ai-ux-deslop
description: >-
  Use when an AI agent is designing, building, or reviewing any web or desktop
  UI (landing pages, tools, dashboards) and the result must not look like
  generic AI slop.
---
# AI UX de-slop

Goal: ship UI that looks designed by a person with a point of view, not generated. Run this BEFORE writing UI code, and again as a gate before calling the UI done. Sources: Anthropic's frontend-design skill, Impeccable (pbakaus/impeccable), Hallmark (Nutlope/hallmark), X threads by @the_rza_, @sakikoazu, @Voxyz_ai, and Kevin's rule on replacing secondary text with intuitive design.

## 1. Write a plan before code (design brief, ~15 lines)
- Who uses it and the single job of the page (one sentence).
- Token plan: 4-6 named hex colors (one accent), 1-2 typefaces and their roles, a real type scale (headline, number, body, small), 8px spacing steps, max content width.
- ASCII wireframe of mobile (390px) and desktop.
- Review the plan for "generic default" picks (Inter by default, purple-blue gradient, cream + terracotta, near-black + acid green) and replace them with a deliberate choice. Keep it in a `DESIGN.md` in the repo so later edits stay on-brand.
- Use a concrete reference instead of adjectives: name a look ("Hacker News / Craigslist plain, one column, 640px, black on white") or paste real screenshots/URLs.

## 2. Replace secondary text with intuitive design (Kevin's rule, apply first)
For every line of helper, explainer, caveat, label or hint text, ask: can the design make this unnecessary? Rework the UX so the interface explains itself, then delete the text.
- Inventory all secondary text (subtitles, helper lines, placeholders that explain, "how it works", disclaimers, tooltips). Each one must either be deleted, replaced by a design change, or demoted to the header/hamburger.
- Replacements that work: a clear input placeholder that is the example itself (e.g. an address shape) instead of a sentence above it; a button label that says the action and outcome; progressive disclosure (show a field or note only when it applies); sensible defaults so no instruction is needed; inline validation that shows the fix at the moment of error; visual hierarchy (size, weight, position) so the order of use is obvious; icon + one word only where the icon is universal; showing the result with its unit ("2.385 ETH") so no explanation of units is needed.
- Keep only text that carries information the user cannot infer: the result, a visible data-quality flag (e.g. "partial history"), and errors with a fix. Everything else lives behind one quiet header link or mobile hamburger.
- Test: show the screenshot to a fresh reviewer with no explanation and ask what to do and what the result means. If they hesitate, fix the design, not by adding text.
- Target: at most one short line of non-interactive secondary text on the main screen.

## 3. Cut content first (restraint)
- Show only what the job needs. For a single-input tool: headline, input, button, result.
- Put the boldness in ONE place (usually the result number); keep everything around it quiet. "Remove one accessory."
- No hero blobs, feature-card rows, "why choose us" sections, stat badges, testimonials, or emoji as icons.
- Structure must mean something: no numbered 01/02/03 markers, eyebrow labels, dividers, or borders unless there is a real sequence.
- Motion: one purposeful moment at most. No fade-slide on every section, no hover effect on every card. Motion that answers a user action is fine. Respect prefers-reduced-motion.

## 4. Banned tells (fail the review if present)
- Inter/system-default look with no thought; purple-to-blue gradients; glassmorphism; glowing or identical soft shadows on rounded cards.
- Cards inside cards; a rounded icon tile above every heading; grey text on colored backgrounds.
- Tracked ALL-CAPS eyebrows; "A · B · C" meta strings; "→" added to every button; one colored or italic word in a headline.
- Lines over ~80 characters; more than two typefaces.

## 5. Copy rules
- Plain, specific, human: "You've spent 2.385 ETH on gas", not "Unlock insights into your on-chain journey".
- Name things the way users do. Buttons say the action ("Calculate", "Download CSV"), not "Submit". Keep the verb through the flow (Calculate -> Calculated). Sentence case.
- No filler words (seamless, powerful, effortless, robust, leverage), and don't put an em dash in every line.
- NEVER invent facts: no fake metrics, customer counts, testimonials, or placeholder data presented as real.

## 6. States and feedback
- Loading shows real progress ("checked 1,200 of 4,300"), not a decorative spinner.
- Errors say what went wrong and how to fix it, without apologizing. Empty states invite the next action.
- Edge cases handled: overflow, long values, zero results, partial data (label it visibly, never mix silently).
- Minimum bar: works at 390px, visible keyboard focus, sufficient contrast, tap targets >= 44px.

## 7. Verify with a gate, not vibes
1. Run the real flow in headless Playwright; capture screenshots at 390px and 1280px (and the error/empty/loading states).
2. Have the agent (ideally a fresh-context reviewer) critique the screenshots against sections 2-6 and a short written brief. Score typography, hierarchy, spacing, color, and how much secondary text remains. Fix every MUST item, then re-shoot. Repeat until clean.
3. If available, run a deterministic linter as a gate: `npx impeccable detect` (62 slop rules, no LLM) or `/hallmark audit <path>`.
4. Give the agent a checklist it must pass, not a paragraph begging it to avoid purple gradients.
5. For changes, name a narrow move ("tighten the result block spacing") instead of "make it pop".

## Optional tools
- `npx skills add anthropics/skills --skill frontend-design`
- `npx impeccable install` then `/impeccable init` (commands: critique, audit, polish, harden, onboard)
- Nutlope/hallmark, Leonxlnx/taste-skill, nextlevelbuilder/ui-ux-pro-max-skill, vercel-labs/agent-skills web-design-guidelines, samigiman/anti-slop-skills (deslop-ui, deslop-copy), awesome-design-md for a DESIGN.md starting point.
- Playwright (headless) for screenshots.

## Done means
Brief written, secondary-text inventory resolved (deleted, designed away, or moved to the menu), banned-tell list passes, copy has no filler or invented facts, mobile + desktop screenshots reviewed, linter (if used) clean, and the page still does its one job in the fewest elements.
