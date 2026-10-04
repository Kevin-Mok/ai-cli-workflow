---
name: metaprompt
description: >-
  Use for /metaprompt, "make me a prompt", or requests to create, sharpen,
  audit, or template prompts for models and agents. Use metaprompt-alxve
  instead when the user explicitly requests the original alxve compiler.
---

# Metaprompt

This is the prompt-authoring adapter for the pinned Majkey25 skill. Read
[UPSTREAM.md](UPSTREAM.md), then load only its references relevant to the
request. All upstream `references/` and `scripts/` paths are relative to this
skill directory. The local contract below specializes upstream behavior.

1. Return a compiled prompt, including for trivial requests. Upstream
   **autoprompt** and silent task execution are disabled in this adapter.
   Its action and verification guidance belongs in the generated prompt;
   it does not authorize executing the embedded task. Execution needs a
   separate request from the user, under normal session permissions.
2. Preserve supplied facts, constraints, scope, and examples. Calibrate detail
   to evidence: rough intent, supplied facts, or inspected source. Use canonical
   `{{variables}}` for an explicitly reusable template; fill supplied inputs
   into one-off prompts. Ask only about material missing information.
3. Save each compiled prompt in the active repository's `prompts/` directory
   with a concise kebab-case Markdown filename. On a collision use a new suffix;
   never overwrite an existing prompt. The saved file contains the compiled
   prompt only. Outside a repository use the current workspace's `prompts/`.
   Report an actionable save error if saving fails; do not claim it was saved.
4. Present the prompt in a `prompt` fence followed by `Saved: <path>` outside
   the fence. Add assumptions, a brief fix list, or evaluation notes only when
   useful or requested. No execution gate is required by this version; use
   `$metaprompt-alxve` for the original strict standalone-`go` workflow.

Verify model-specific claims against current primary documentation when they
affect the prompt. An upstream source date or attractive rewrite is not proof
of better results; distinguish prepared evals from executed comparisons.

Optional helpers are in [scripts/](scripts/). Lint exact intended prompt files;
findings are heuristics and cannot override user requirements. For the eval
manifest generator, prefer `--out -`: its file output overwrites existing
paths, and a generated manifest still needs real cases and executed runs.

See [SOURCE.md](SOURCE.md) for provenance and reviewed updates.
