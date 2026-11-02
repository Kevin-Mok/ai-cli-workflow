---
name: metaprompt
description: >-
  Use for /metaprompt, "make me a prompt", or requests to create, sharpen,
  deepen, audit, or template prompts for models and agents.
---

# Metaprompt

Turn a request or existing prompt into a saved prompt with clear success
criteria. Clarify the goal, deepen it the way a field-leading expert would,
follow the upstream optimization workflow, and return the compiled prompt with
its evaluation plan and remaining risks.

This is the prompt-authoring adapter for Sentry's pinned `prompt-optimizer`.
Read [UPSTREAM.md](UPSTREAM.md) and follow its native workflow, loading only
the references selected by its routing table. Reference paths are relative to
this skill directory. The local contract below adds the `metaprompt` alias, a
depth pass, and saved prompt artifacts.

1. Return a compiled prompt, including for trivial requests. Authoring a prompt
   does not authorize executing the user's embedded production task. Execution
   needs a separate request from the user, under normal session permissions.
   Evaluate prompts only within available tools, supplied fixtures and the
   authorized budget; distinguish prepared evals from executed comparisons.
2. Preserve supplied facts, constraints, scope, and examples. Calibrate detail
   to evidence: rough intent, supplied facts, or inspected source. Use canonical
   `{{variables}}` for an explicitly reusable template; fill supplied inputs
   into one-off prompts. Ask only about material missing information.
3. Depth pass (after upstream Step 1, before Step 4 shaping). Make the task
   deeper, not bigger: do not add scope, deliverables, or permissions the user
   did not ask for. Answer briefly, from the task's field:
   - Expert gap: what a top professional would do here that the request omits.
   - Raw material: the rawest available source they would start from (logs,
     data, source code, primary docs) instead of pre-digested summaries; name
     exact paths/inputs when known, otherwise a `{{variable}}` or a question.
   - Methods and tools: the specific techniques and instruments they would use
     (a database and statistical test, for example, rather than a markdown
     table). Name methods, not personas; a role line alone changes vocabulary,
     not method.
   - Outside judge: what, other than the model or the user, shows the result
     is right (tests, a runnable check, holdout data, a primary source,
     reproduction). Prefer one the executor can run itself.
   Fold accepted answers into the compiled prompt as concrete inputs, method
   steps, and verification steps, and into `Success Criteria` and `Eval Set`.
   Skip or shorten the pass for trivial asks. In `Optimization Log`, name each
   depth tweak that entered the prompt, plus skipped items and rejected scope
   growth. Optional, and only when it would materially change the task: record
   Altitude (the goal beyond the stated goal) and Range (other fields whose
   methods would help) in that log. Never silently substitute either for the
   requested task. Leave an unaccepted option out of the saved prompt.
4. Save each compiled prompt in the active repository's `prompts/` directory
   with a concise kebab-case Markdown filename. On a collision use a new suffix;
   never overwrite an existing prompt. The saved file contains the compiled
   prompt only. Outside a repository use the current workspace's `prompts/`.
   Report an actionable save error if saving fails; do not claim it was saved.
5. Return Sentry's eight sections: `Target`, `Success Criteria`, `External
   Context`, `Optimized Prompt`, `Adapter Notes`, `Eval Set`, `Optimization Log`,
   and `Residual Risks`. Put the four depth-pass answers in compact form under
   `Target` (one line each). Within `Optimized Prompt`, present the compiled
   prompt in a `prompt` fence followed by `Saved: <path>` outside the fence.
   Save only that prompt, not the surrounding report. Keep sections concise for
   simple requests. For existing prompts include the native diff-style change
   note.

Verify model-specific claims against current primary documentation when they
affect the prompt. An upstream source date or attractive rewrite is not proof
of better results; distinguish prepared evals from executed comparisons. Do
not let the model grade its own output as the only success check.

See [SOURCE.md](SOURCE.md) for provenance and the reviewed update helper.
The upstream [SOURCES.md](SOURCES.md) records Sentry's source lineage; its
foreign repository paths are provenance rather than local runtime dependencies.
The depth pass adapts Felix Rieseberg's "deeper, not bigger" prompt from
https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
(Depth section, published 2026-10-13).
