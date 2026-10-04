# Compile the terminal workflow research prompt

This records the earlier prompt-authoring stage: save and verify the research
instructions, then hand them off. The later research, implementation, and
authorized session commit are recorded in the
[Kitty scrolling plan](kitty-codex-scrollback.md).

## Purpose and observable outcome

Save a paste-ready terminal research prompt. The latest version is
[choose-terminal-workflow-2.md](../prompts/choose-terminal-workflow-2.md),
which prioritizes long Codex output, a draggable scrollbar, transparency, and
minimal modern styling. Preserve the
[original approved prompt](../prompts/choose-terminal-workflow.md).
Both ask a future research agent to determine whether configuring Kitty,
updating it, or switching terminals offers the greatest practical benefit.
This task authors the prompts; it does not execute the embedded research.

## Context and scope

The user invoked `metaprompt`, approved the proposed prompt, requested
implementation, and then requested continuation after an interruption.
The planning turn inspected Kitty, tmux, i3, terminal documentation, the supplied
screenshot, applicable feedback, and relevant lessons. It observed Kitty 0.49.2
on Ubuntu 24.04 with i3/X11.

The original three documents are the first prompt, this plan, and the
[sandbox incident note](../docs/postmortem/2026-10-04-terminal-prompt-sandbox-startup.md).
The user's subsequent clarification adds the second prompt version. Each prompt
file contains only the compiled prompt; the original approved text is preserved.
No terminal settings, software, skills, APIs, or public interfaces change.

## Assumptions and decisions

- The approved artifact requires an interactive scrollbar per terminal window;
  independent scrollbars for every tmux pane are not required.
- Shift+PageUp/PageDown is the selected history-navigation shortcut.
- The revised objective is excellent navigation through long Codex output,
  including stable reading position during streaming and a usable draggable
  scrollbar. Generic shell scrolling alone is insufficient.
- Preserve Kitty-like background transparency, starting from the observed 0.9
  opacity, with readable text and scrollbar contrast.
- Thin, auto-hiding appearance is a preference, not a hard eligibility rule;
  the thumb must remain easy to find and grab.
- An optional clarification asked whether "rounded progress" meant the
  scrollbar, window corners, or both. Pending a reply, the stated default is a
  rounded scrollbar thumb/track; outer window corners remain optional. The
  research must distinguish terminal styling from compositor responsibilities.
- Replacement candidates need at least 1,000 verified GitHub stars and must
  fit the existing Ubuntu/i3/X11 workflow.
- The research must distinguish terminal, tmux, and application-owned history
  and must not assert performance gains without relevant evidence.
- This continuation finishes prompt authoring. Research, terminal migration,
  benchmarks, installation, commit, and push remain outside the approved scope.

## Ordered checklist

- [x] Capture current Git status before writing and confirm interruption state.
- [x] Read applicable instructions, prompt context, preferences, and lessons.
- [x] Confirm the intended paths have no collisions or nested instructions.
- [x] Save the exact approved prompt and record the deferred sandbox incident.
- [x] Read back the files, check references and whitespace, and inspect scope.
- [x] Record verification evidence and prepare the saved-prompt handoff.
- [x] Inspect the user's Codex-focused refinement and relevant compositor context.
- [x] Save the revised prompt at a new suffix without changing the original.
- [x] Verify revised requirements, artifact links, whitespace, and change scope.

## Protected dirty state, risks, and rollback

The pre-write status contains modified `aliases/key_dirs.tmpl`,
`docs/phone-ssh-public-ip.md`, and `docs/smoke-tests.md`, plus these pre-existing
untracked files:

- `docs/postmortem/2026-09-30-secret-audit-shell-sandbox-startup.md`
- `docs/postmortem/2026-10-03-benchmark-prompt-sandbox-startup.md`
- `docs/postmortem/2026-10-03-phone-ssh-diagnostic-shell-startup.md`
- `plans/compile-metaprompt-benchmark.md`
- `plans/diagnose-phone-ssh-access.md`
- `prompts/benchmark-metaprompt-skills.md`

Preserve these files. Never overwrite an existing prompt; use a new suffix if a
collision appears before creation. Rollback removes only this task's four new
documents, after confirming they have no subsequent user edits. The refinement
alone can be rolled back by removing the second prompt version and reverting
only its accompanying plan edits.

Repository instructions, configuration, and reusable manual procedures are
unchanged. The existing README and smoke-test documentation remain accurate;
no `refresh-config` invocation is needed for this document-only task. The
prepared research acceptance cases are not executed terminal checks or model
evaluations. No new regression test is warranted for saving approved prose.

## Verification plan

- Read the new files in full. Confirm that prompt files contain only the
  compiled text without the surrounding eight-section report or a code fence.
- Check UTF-8 readability, final newlines, trailing whitespace, and all local
  repository references in the prompt. Validate the plan/postmortem links.
- Run `git diff --check` and inspect `git status --short`; explicitly inspect
  untracked files because Git's diff check alone does not cover them.
- Manually confirm the four prepared cases: Kitty already meets requirements;
  an alternative lacks a Linux scrollbar; tmux/Codex owns the history; and
  comparable performance evidence is unavailable. This checks prompt coverage
  only, not downstream agent performance.
- For the refinement, also check: a passive indicator is insufficient; Codex
  history differs from shell history; streaming preserves reading position;
  a thin thumb stays grabbable; transparency preserves readability; rounded
  styling may be unsupported or owned by the compositor.
- Verify that the original prompt's SHA-256 remains
  `3d19b1a39ef336a5966e05e2c2076798e237a4d1f3cd0710cdfae2b5e0b9235e`.

## Progress, evidence, and review notes

- 2026-10-04: The approved prompt was prepared in Plan mode, so file writes and
  the required incident note were deferred until implementation was authorized.
- Fresh elevated reads exited 0 after continuation. Status matched the prior
  dirty snapshot, all intended paths were absent, and no nested instruction
  files applied to the new document locations.
- The active Sentry adapter has no source `prompt_lint.py`; an old cache entry
  is not a callable validator. Use direct artifact checks and manual review.
- No comparative prompt evaluation, terminal benchmark, or terminal capability
  research has run. Keep this plan and the incident note with the prompt in any
  future related commit.
- Artifact verification exited 0: all three documents are readable UTF-8 with
  final newlines, no trailing whitespace, and valid local Markdown links. The
  prompt has no response wrapper or code fence, and all five repository source
  references exist. Full prompt readback matches the approved compiled text.
- Manual review confirmed both selected preferences and all four prepared
  cases are covered. These are coverage checks, not executed model evaluations.
- Scoped `git diff --check` produced no findings; explicit Python checks covered
  the new untracked documents. Final status contained only the three expected
  additions beyond the protected initial state. No tracked file was edited.
- Suggested future commit subject, if requested:
  `docs: add terminal workflow research prompt`. No commit was created.
- 2026-10-04 refinement: The user prioritized long Codex output, a grabbable
  scrollbar, current transparency, minimal modern appearance, and "rounded
  progress." The earlier objective was too broad, dragging was only implicit,
  and transparency was context rather than a requirement. The revised prompt
  makes these explicit and adds concrete Codex scrolling acceptance scenarios.
- Selected a focused revision of the existing structure. No downstream agent
  trials or comparative prompt evaluations were executed, so no measured
  improvement is claimed. The new version keeps the original requirements for
  window-level scrollbars, Shift+PageUp/PageDown, popularity, and X11 support.
- Refinement verification exited 0: the original prompt's SHA-256 matches the
  recorded baseline; the new prompt and updated plan have final newlines, no
  trailing whitespace, and valid local links. All six repository references
  in the new prompt exist. The prompt contains no report wrapper or code fence.
- Readback confirmed the Codex-specific objective, draggable scrollbar,
  transparency, rounded-thumb assumption, streaming/history scenarios, and
  distinction between proposed checks and executed evidence. Scoped
  `git diff --check` exited 0. Status adds only the second prompt path beyond
  the turn's initial status; the existing session plan was the only edited file.
