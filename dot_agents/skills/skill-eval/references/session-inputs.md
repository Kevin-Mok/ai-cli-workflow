# Bounded session input collection

Find real tasks that used the target skill without loading whole histories. Discover recent files, filter metadata, extract only relevant user inputs, then save safe cases and a brief coverage summary.

Use the record shapes and limits below; no optional session-reading skill is required.

## Limits and matching

- Start with at most the newest 200 files per client and retain at most 15
  matching sessions overall. Cap metadata reads at 64 KiB per file; stream
  relevant records within 2 MiB per retained file and 20 MiB total. Bound each
  JSONL line read to the remaining byte budget, rather than loading the file
  or an unbounded line. Skip truncated records and record the limit reached.
- Prefer the target repo's cwd and known worktrees using path-component
  containment, not string-prefix matching. If the repo is unspecified, ask
  which cwd(s) to search. A skill mention in an unrelated cwd is not enough.
- A matching cwd narrows discovery; require explicit skill invocation, a
  recorded skill read/use, or the user's confirmation to label a task as having
  used the target. Mere mention in a catalog or pasted transcript is not use.
- Deduplicate repeated exports, resumed turns and identical user inputs. Pick
  varied real tasks; record selection rationale. If bounded discovery yields
  too few, report coverage and ask for real inputs or permission to widen it.
  Missing directories are unavailable sources, not permission to fabricate.

## Codex records

Read `${CODEX_HOME:-~/.codex}/sessions/**/rollout-*.jsonl` (expand the home
fallback correctly in the host language). Discover with a bounded iterator;
keep only the newest 200 candidates without reading their bodies. Skip
compressed files unless bounded decompression is available.

The first record normally has `type: session_meta`; `payload.cwd`, timestamp,
and optional git metadata filter candidates. Extract task text from `event_msg`
whose `payload.type` is `user_message` (`payload.message`). Some versions also
store user turns in `response_item` messages with role `user` and text content
parts; use that as a fallback, not a second duplicate case. Exclude injected
environment/instruction wrappers. Inspect skill-use evidence locally without
exporting reasoning, tool results or assistant history as task inputs.

## Claude Code records

Read `~/.claude/projects/*/*.jsonl`. Encoded project-directory names are a
discovery hint; verify actual record `cwd` rather than trusting name decoding.
User records have `type: user`; extract text from `message.content` (a string
or a list of text blocks). Skip tool-result blocks and system/assistant records
as inputs. Assistant skill-use evidence can establish provenance locally.
Skip malformed, unsupported, truncated and ambiguous records with counts.

## Privacy and replay

Never dump raw JSONL or print a grep of session bodies. Preview at most 400
characters per candidate locally after secret/private-data screening; chat
gets one-sentence summaries and opaque case IDs. Do not export tokens, keys,
credentials, personal discussions, sensitive attachments or tool dumps.
Automated redaction is not proof of safety; review each selected full input.

Save full **safe** input text as-is, not the clipped preview or a paraphrase.
If a task contains secrets or needs missing conversational context, exclude
it and ask for a safe self-contained real replacement. If the user supplies an
edited replacement, label it user-supplied rather than an unchanged historical
input. Keep session paths/local provenance out of public reports when private;
never commit raw session logs or unreviewed benchmark artifacts.
