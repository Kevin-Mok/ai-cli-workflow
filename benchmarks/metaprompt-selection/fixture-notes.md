# Fresh selection fixture contract

26 entirely synthetic cases: two development and 24 held-out, six per native
workflow (create, sharpen, template, coding). The six content labels are research,
summary, extraction, writing, template, coding. Workflows carry equal case weight;
content labels intentionally do not imply an equal content-family distribution.
No case IDs, bound packets, outputs, or bugs from the earlier pilot are reused.
No model calls or usage statistics informed construction.

Requests are adapted from repository prompt patterns: local focused repair and
stopping, supplied-source research, action handoffs, draft-only authorization,
and canonical reusable inputs. `prompts/package-sudo-required-commands.md` informs
separation of prepared artifacts from authorization; `prompts/research-codex-token-efficiency.md`
informs evidence-only factual research. These are synthetic adaptations, not
historical user requests or usage prevalence evidence. Raw requests are ordinary
brief task instructions, not role-heavy fully optimized prompts. Explicit JSON
field contracts remain necessary for deterministic comparisons; answers and
format requirements never appear exclusively in hidden keys.

Compiler input is authoring_request plus compiler_context; do not expose answer
keys, reference-solutions, hidden tests, or held-out template bindings. Solver gets
the chosen prompt, solver_context, and supplied files. Template raw and compiled
arms receive exactly the same bindings after compilation. Named slots must remain
unchanged. Bind in one pass; treat bound values as data. Native prompt authors may
read their pinned skill references. All fixture facts are synthetic supplied
packets, not web facts; source labels are local IDs, not internet citations.

Noncoding acceptance is parsed JSON equality, ignoring object key order but
preserving array order/types. Pure JSON only: additional prose/fences fail.
Writing cases measure factual structured drafts and action boundaries; they do
not measure style, persuasion, elegance, or open-ended prose quality. Calling the
result a general writing-quality score would be misleading.

Coding cases require actual read, target-only write, and public_tests.py execution
via the provided tool contract, then stop after a successful run. Public tests
are readable files; hidden tests are separate assertions exercising additional
edge cases. Behavior is specified publicly in docstrings. `public_parameters`
protects names, parameter order/kinds, and required defaults. The deterministic
code grader is compatible with the old benchmark's restricted pure-function
boundary: no arbitrary imports, filesystem/process/network access, or classes.
Return complete target module source, without fences/commentary. A code-only
correct answer does not by itself prove file edits or public test execution;
the runner must grade those tool events separately and must not infer them.

reference-solutions.json maps each case ID to a correct downstream output string
(JSON text or Python code). It is private validation material, never trial input.
Use the old score_output read-only to check every reference passes and each
supplied buggy module fails hidden grading. Also execute supplied public tests
against original and reference modules: original RED, reference GREEN.

Freeze all four files before any scoring run. Changes after results appear need
a fresh benchmark version/run. Objective results cover these declared contracts;
no subjective quality score or causal generalization from a small selection is
claimed. Missing-fact, conflicting-source, unavailable-file, quoted-instruction,
authorization and stopping cases are deliberate. They require evidence-preserving
behavior without external browsing or real permissions.

## Construction verification

On 2026-10-03, read-only import of the original benchmark score_output passed
all 26 reference outputs. All seven buggy modules failed their hidden checks.
Public tests run in temporary directories failed for all seven original modules
and passed for all seven references. All six templates retained exact slot sets,
case IDs were unique and disjoint from the earlier suite, and every workflow had
six held-out cases. These are fixture checks, not model trials or skill scores.

Before freezing, every noncoding raw task and matching authoring request was
clarified with the same invariant: JSON only, exactly named fields and publicly
specified types, no extra prose/fences. Nullable numeric extraction fields permit
integer or null, source/fact arrays contain strings, and warranty months is an
integer. These are acceptance format requirements, not hidden answer hints.

Before held-out freeze, the independent copy-boundary review clarified fifteen public request contracts equally in raw and authoring text. Answer keys and reference solutions are unchanged. Development round1 retains its originally ambiguous decision span; round2 has input_version=2. See research/fixture-copy-review.md for exact rationale.
