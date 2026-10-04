# Independent harness review

Reviewed selection.py, selection_core.py, selection_mcp.py and the fresh fixture
contracts without models. Findings below were sent to the parent during active
implementation; they describe the reviewed intermediate version, not necessarily
the eventual frozen version. Recheck after parent corrections.

## Actionable findings

- Final extraction accepted the only saved artifact even when the author called
  it a draft and asked to refine it. An offline call with output `Here is a draft.
  Shall I refine it?` and artifact `prompts/draft.md` returned `only_saved_artifact`.
  Require a clearly final artifact or native completion evidence before stopping
  the authoring continuation. Extraction and native workflow completion are
  separate requirements. Candidate-specific requirements should come from the
  actual finalist source, rather than the earlier local skills' contracts.
- Recommendation eligibility required one attempted row per workflow, allowing
  four quota-truncated rows to count as complete. Offline summarize returned
  eligible_for_default=true for that synthetic incomplete set. Require the
  entire frozen paired schedule to finish; incomplete/infrastructure outcomes
  must not establish a default winner. Report practical operational failures
  separately from completed downstream task accuracy.
- The shared compiler instructions advertised run_skill_check even without a
  candidate's approved_helper. A normal call to an advertised tool then became
  unauthorized_tool_access. Advertise this helper only to its owning candidate;
  distinguish unavailable tool functionality from an actual scope violation.
- allocation(2) offered 48 held-out cases per arm and allocation(3) offered 28,
  exceeding this suite's 24 available cases. Clamp allocations to available
  fixtures or reject unsupported schedules before reserving trials.
- coding_actions required a GREEN after the last write, but did not reject
  additional work after the first successful public run. The user stopping
  instruction is public; record and enforce terminal successful verification.
- Restricted Python scoring labeled harmless unsupported constructs unsafe_code.
  stdlib-only tasks legitimately permit typing annotations and pure str methods
  such as splitlines/partition. Preserve the execution boundary, but expand exact
  safe allowlists or publish its limits and classify unsupported pure constructs
  as a measurement limitation, rather than an observed unauthorized action.

## Pure Python additions worth considering

For these fixtures, basic iter/next/pow/divmod and str splitlines/partition/
rpartition/rsplit/lstrip/rstrip/startswith/endswith/casefold, plus dict.setdefault,
are safe alternatives under existing CPU/memory limits. Exact typing imports
List/Dict/Tuple/Sequence/Iterable/Iterator/Mapping/Optional/Union/Any permit common
annotations without allowing introspection helpers. collections Counter,
defaultdict/deque and itertools chain/islice are plausible additional pure
implementations if both module and member names are explicitly allowed. No
fixture requires filesystem/process/network modules, arbitrary imports, eval,
getattr, or user-defined classes. Keep such code unexecuted. A rejected code
submission is not evidence that the host action actually occurred.

## Fixture and leakage review

Compiler inputs contain the native skill package, authoring request, and allowed
compiler context. Solver receives task packets and public files. Hidden keys,
reference solutions, and template bindings are absent from compiler input. No
hidden-key leak observed in the reviewed data flow. Coding compiler context is
sufficient for a generic agent prompt: the prompt must instruct downstream
inspection, not guess the unseen docstring behavior.

Before freeze, all 19 noncoding raw and authoring requests were clarified to make
JSON-only, exact keys and expected types public. This fixes deterministic false
negatives from reasonable extra prose/fields or string-valued numeric fields.
These acceptance requirements do not reveal held-out answers. Writing remains
structured factual drafting, not a broad writing-quality measure.

Fresh verification after clarification passed 26 reference scores, seven buggy
hidden-test REDs, seven public-test RED/GREEN pairs, six exact template bindings,
and six held-out cases per workflow. The original benchmark scorer was imported
read-only; no model requests or prior benchmark changes were made.

## Offline tool integration evidence

`python3 tests/test_metaprompt_selection_runtime.py` passed three actual Codex CLI
and real MCP tests: compiler reference reading and prompt saving; solver target
reading/writing/public tests/final code; approved-helper traversal denied before
process launch. The runtime upstream was synthetic and HTTPS transport forbidden.
Seven synthetic responses, zero model or remote upstream requests. Tool result
logs and actual temporary file effects were checked independently of model text.

## Pre-freeze resolution

All reported findings were addressed before any held-out output: explicit final-link extraction, complete balanced recommendation gate, candidate-specific helper exposure, insufficient-case rejection, stopping checks, safe Python additions, and public copy/type contracts. Native gates now live in selection_native.py and remain separate from objective downstream success. The second development round completed all compile/solve paths; three missed-link handoffs were recovered only into their unused solver stages with original records archived and every request still charged. The checker StopIteration issue is fixed with a passing reproducer. Focused selection suite:55 tests passed; no hidden keys were exposed.
