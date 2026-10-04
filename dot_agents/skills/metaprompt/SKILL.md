---
name: metaprompt
description: >-
  Use for /metaprompt, "make me a prompt", or requests to create, sharpen,
  audit, or template prompts for models and agents. Use metaprompt-alxve
  instead when the user explicitly requests the original alxve compiler.
---

# Metaprompt

Turn a request or existing prompt into a saved prompt with clear success
criteria. Clarify the goal, follow the upstream optimization workflow, and
return the compiled prompt with its evaluation plan and remaining risks.

This is the prompt-authoring adapter for Sentry's pinned `prompt-optimizer`.
Read [UPSTREAM.md](UPSTREAM.md) and follow its native workflow, loading only
the references selected by its routing table. Reference paths are relative to
this skill directory. The local contract below adds the `metaprompt` alias and
saved prompt artifacts.

1. Return a compiled prompt, including for trivial requests. Authoring a prompt
   does not authorize executing the user's embedded production task. Execution
   needs a separate request from the user, under normal session permissions.
   Evaluate prompts only within available tools, supplied fixtures and the
   authorized budget; distinguish prepared evals from executed comparisons.
2. Preserve supplied facts, constraints, scope, and examples. Calibrate detail
   to evidence: rough intent, supplied facts, or inspected source. Use canonical
   `{{variables}}` for an explicitly reusable template; fill supplied inputs
   into one-off prompts. Ask only about material missing information.
3. Save each compiled prompt in the active repository's `prompts/` directory
   with a concise kebab-case Markdown filename. On a collision use a new suffix;
   never overwrite an existing prompt. The saved file contains the compiled
   prompt only. Outside a repository use the current workspace's `prompts/`.
   Report an actionable save error if saving fails; do not claim it was saved.
4. Return Sentry's eight sections: `Target`, `Success Criteria`, `External
   Context`, `Optimized Prompt`, `Adapter Notes`, `Eval Set`, `Optimization Log`,
   and `Residual Risks`. Within `Optimized Prompt`, present the compiled prompt
   in a `prompt` fence followed by `Saved: <path>` outside the fence. Save only
   that prompt, not the surrounding report. Keep sections concise for simple
   requests. For existing prompts include the native diff-style change note.
   Use `$metaprompt-alxve` for the original strict standalone-`go` workflow.

Verify model-specific claims against current primary documentation when they
affect the prompt. An upstream source date or attractive rewrite is not proof
of better results; distinguish prepared evals from executed comparisons.

See [SOURCE.md](SOURCE.md) for provenance and the reviewed update helper.
The upstream [SOURCES.md](SOURCES.md) records Sentry's source lineage; its
foreign repository paths are provenance rather than local runtime dependencies.
