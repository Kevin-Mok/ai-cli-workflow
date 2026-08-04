# Second Brain ELI5 Guide

## Purpose and observable outcome

Create a standalone beginner guide at `docs/second-brain-eli5.md` that lets a
new user understand the normal Second Brain routine without reading the
operator manual: start a session, confirm one focus, capture useful context,
and close out with a handoff.

## Context and scope

- `docs/second-brain-beginner.md` and `docs/second-brain-for-beginners.md` are
  protected pre-existing drafts and will not be changed.
- The guide must match `dot_agents/skills/second-brain-session/SKILL.md` and
  its routing reference: raw capture is private, while tracked writes are
  public-safe and confirmation-gated.
- This is explanatory documentation only. It does not change the CLI, vault,
  installed configuration, or smoke-test workflow.

## Assumptions and decisions

- The user explicitly chose the standalone path `docs/second-brain-eli5.md`.
- The primary beginner interface is a conversation with Codex, because the
  skill safely performs structured CLI operations after required confirmation.
- Include only low-risk inspection commands users can run themselves; avoid
  asking beginners to hand-write JSON payloads.

## Implementation checklist

- [x] Record protected dirty state before editing: existing aliases, docs,
  config, feedback, vault, and setup-script changes; three existing beginner
  documentation drafts remain out of scope.
- [x] Read the session-skill contract, routing reference, vault README, and
  existing beginner documentation.
- [x] Create `docs/second-brain-eli5.md` with a plain-language purpose,
  four-step routine, privacy boundary, folder map, and safe recovery command.
- [x] Verify Markdown structure, links, and command spelling against the
  documented entrypoints.
- [x] Record final evidence and review notes in this plan.

## Risks, rollback, and protected state

- Risk: presenting raw captures as tracked notes could expose private text.
  Mitigation: state that raw capture stays outside Git and requires no manual
  vault editing.
- Risk: beginners might use direct structured-write commands without the
  required confirmation. Mitigation: route focus and closeout through Codex.
- Rollback: delete only the newly created guide if it is rejected; do not
  alter the protected drafts.

## Verification

- Run `rg -n '^#|second-brain (status|doctor)' docs/second-brain-eli5.md` to
  confirm the expected sections and inspection commands exist.
- Run `git diff --check -- docs/second-brain-eli5.md plans/second-brain-eli5.md`
  to detect whitespace errors.
- Manually compare workflow claims with the session skill and routing
  reference already read for this plan.

## Progress, evidence, and review notes

- 2026-07-22: Added the standalone guide without modifying the three protected
  pre-existing beginner-guide drafts.
- Verification: `rg -n '^#|second-brain (status|doctor)'
  docs/second-brain-eli5.md` found the title, all seven guide sections, and
  the documented `status` and read-only `doctor --check` commands (exit 0).
- Verification: `git diff --check -- docs/second-brain-eli5.md
  plans/second-brain-eli5.md` exited 0 with no whitespace errors.
- Review: The guide intentionally directs focus and closeout through Codex so
  beginners do not need to construct confirmation-gated JSON payloads.
- Rollback remains removal of only the two newly created files.
- Final verification: `git diff --check --no-index /dev/null` against each new
  file returned its expected exit 1 for a new-file diff, with no whitespace
  diagnostics; the wrapper then checked that expected status and exited 0.
