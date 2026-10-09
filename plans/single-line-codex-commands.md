# Single-line Codex commands

Make shell commands copied from Codex usable in fish while keeping reading code highlighted. The current follow-up separates bare runnable lines from tagged reading blocks, syncs the guidance and records actual copying/color limits. Earlier sections retain historical evidence; current decisions and status are in the final follow-up.

## Original scope and decisions

- One physical line per shell command: no leading indentation, inserted newlines, or backslash continuations. Keep all flags on the same line and omit shell prompt markers.
- Visual wrapping by the terminal is acceptable; command text must remain one physical line.
- Current scope: canonical policy, append-only feedback, one Codex TUI startup setting, corresponding README/smoke guidance, one local verification lesson, and this plan. Required incident bookkeeping and tracked learning are bounded companions. The TUI setting was added in the follow-up after the screenshot invalidated the original formatting-only assumption.
- The user requested formatting, not a change to notification behavior, fish, or terminal width. No commit or push was requested.
- Initial `git status --short` captured before modifications. Policy, feedback, README, smoke docs and incident ledger were already dirty; snapshots of the four policy/doc files are under `/tmp/codex-single-line-commands-before`. Preserve their prior contents.

## Checklist

- [x] Inspect canonical policy, current preferences, local instructions and relevant docs.
- [x] Append the durable formatting preference without rewriting historical entries.
- [x] Add the one-line command rule and align README/smoke guidance.
- [x] Run required refresh-config and verify installed policy and canonical feedback routing.
- [x] Review the session diff, incident coverage and final handoff.

## Verification

This is a prose instruction update; an implementation-mirroring automated test adds no useful coverage. Review the added text directly, parse the user-provided example with fish without executing notifications, run refresh-config, and compare installed policy with the source; confirm the installed feedback skill routes to the canonical append-only repo log. The manual check copies a long command from a fresh Codex reply into fish and verifies that all flags arrive on one physical line without cleanup. Paste examples use supported permission, worker, empty, completion and all scenarios from the existing notification smoke helper. These are examples for the formatting rule, not changes to event behavior.

## Risks and rollback

The terminal may visually wrap long commands; this instruction governs actual command text, not terminal rendering. Fresh sessions are needed to observe automatic adherence to newly installed guidance. Refresh-config snapshots live Codex/Git configuration and applies chezmoi, so inspect any additional changes and preserve pre-existing work. Roll back only this session's added rule and appended entry; never restore entire dirty files from HEAD.

## Progress and review notes

- Native thread title: Keep commands on one line.
- Default shell sandbox failed before execution; approved scoped reads succeeded. The required [task incident](../docs/postmortem/2026-10-09-single-line-command-policy-sandbox.md) records this and the two verification limitations; its reviewed ledger entry adds no new finding.
- `fish -n -c 'python3 -B scripts/smoke_codex_notification_events.py --installed --case permission --plain'`: expected silent syntax success; observed no output, exit 0.
- `fish -c 'refresh-config'`: expected normal snapshot/apply/shortcut stages; observed REFRESH COMPLETE, exit 0. The tracked Codex TOML snapshot remained byte-identical.
- `fish -c 'python3 -B scripts/smoke_codex_notification_events.py --installed --case all --plain'`: expected supported isolated scenarios PASS; observed all eight PASS, exit 0. Completion recorded one synthetic playback; worker, empty, missing, unknown, ambiguous, parent and permission recorded zero. The player is silent and isolated.
- `python3 -B tests/test_ai_workflow_contract.py`: observed 11 passing checks and one failing existing push-policy literal assertion, exit 1. The named commit skills are byte-identical to HEAD, and the expected literal is absent in both HEAD and the working tree. No unrelated policy/test repair was made.
- Direct byte comparison: installed `~/.codex/AGENTS.md` equals the source; the canonical feedback log preserves every baseline byte and appends the new preference. The installed feedback skill routes to that canonical log. Observed exit 0.
- The first installed-feedback comparison incorrectly assumed an optional installed feedback.log existed. Corrected verification above uses the canonical log; no second feedback writer was created. This assumption failure is recorded in the task incident.
- Session-only diff reviewed against before-edit snapshots: one policy bullet, one append-only preference, the README paragraph, and the existing smoke-handoff expectation. Notification implementation and unrelated dirty state preserved.
- Fresh-session manual copy behavior is not yet observed; installed guidance and fish/runtime example syntax are verified. Terminal visual wrapping remains outside this instruction change.

- Final `python3 -B dot_agents/skills/postmortem-memory/scripts/postmortem_memory.py check --postmortem /home/example/linux-config/docs/postmortem/2026-10-09-single-line-command-policy-sandbox.md`: observed document_count 1, errors/new/changed/missing_sources/unregistered_aliases all empty, exit 0. Root independently confirmed the reviewed hash/alias and explicit no-new-learning decision.
- After the final tracked ledger update, `fish -c 'refresh-config'` again reported REFRESH COMPLETE, exit 0; fresh byte comparison confirmed the installed policy still matches the source.
- Formatting update complete and synced; no commit/push requested. Final handoff provides five standalone single-line paste examples using the existing silent notification helper. Full workflow suite remains limited by the confirmed pre-existing push-policy assertion.

## Follow-up: rendered code-block padding

The user's new screenshot invalidates the earlier assumption that a one-line source command is sufficient. The old fish/runtime checks remain true but do not verify copying a wrapped TUI line. Preserve their historical evidence.

- [x] Reproduce the remaining spaces from the previous reply and user screenshot.
- [x] Save the clarified preference for standalone unindented plain-text command paragraphs.
- [x] Update the canonical rule and matching public verification guidance.
- [x] Sync and verify installed policy and effective raw-output startup.
- [ ] Verify actual copied wrapped command in a fresh or toggled Codex TUI (user action pending).
- [x] Finish the living incident, reviewed ledger and final handoff.

Decision revised after official documentation lookup: enable the supported `tui.raw_output_mode = true` copy-friendly scrollback setting in `dot_codex/config.toml` and sync it to the live config. This is a reversible startup preference, not a Codex binary or terminal patch. Installed npm package version is 0.162.0; the official config reference documents `/raw` and Alt+R to toggle the current session. Keep command paragraphs free of fences, inline backticks, list indentation, blockquotes and prompts, so raw view contains clean command text. Copy from a deliberately wrapped command in the real TUI is the manual reproducer; config parsing and fish syntax cannot establish clipboard acceptance.

Defining RED: both live and tracked `tui.raw_output_mode` were unset, and the intentional assertion that live startup enables copy-friendly mode failed (exit 1). This expected RED is exempt from incident creation. Source and live TOML were byte-identical before implementation. Scope now includes this one TOML setting plus existing policy/docs/feedback and required incident guidance. The user explicitly requires copied spaces/newlines not to break fish commands; the active-session toggle remains a user action because this toolset cannot operate the open terminal.

Official evidence: fetched https://developers.openai.com/codex/config-reference/#tui describes raw scrollback as copy-friendly terminal selection, default false, toggled with `/raw` or default Alt+R. No indentation-only config setting was established. Root has captured a new git status before edits and snapshots under `/tmp/codex-wrapped-command-padding-before`.

### Follow-up verification evidence

- Scoped `chezmoi apply --force /home/example/.codex/config.toml`: observed silent success, exit 0. Applying this target before refresh preserves the new setting through the live-to-source snapshot.
- Existing `IsolatedCodex._probe` strict app-server `config/read`, with repository isolation and effective MCP servers disabled: expected raw-output true; observed `Codex effective tui.raw_output_mode: True`, no thread/inference request, live/source bytes match, exit 0. This verifies config parsing/effective startup, not an active TUI paste.
- `fish -c 'refresh-config'`: observed REFRESH COMPLETE, exit 0. Fresh checks confirmed installed policy matches source and live raw_output_mode remains true.
- Session-only diff reviewed against before-edit snapshots: exactly one startup setting plus comment, plain-text reply guidance, README and real wrapped-selection smoke guidance. Added one local engineering lesson about verification scope; durable formatting preference remains separate in feedback.log.
- Requested direct active-session comparison after Alt+R or `/raw`. Manual copy acceptance remains pending; no terminal/clipboard repair claim is made.

- Latest user request: provide commands to check in a new Codex window. This requests a manual handoff, not confirmation that copied text is fixed. The exact current conversation ID `01a12202-5536-78a2-8e5d-d2326d15919f` is registered in the live session index, so a fresh `codex resume` invocation can display this same handoff with the new startup setting.
- Fresh `python3 -B scripts/smoke_codex_notification_events.py --installed --case all --plain` ran all eight cases successfully, exit 0, using the silent isolated player. This supplies exact output labels for the manual paste examples, not clipboard verification.
- Manual handoff: from `/home/example/linux-config`, resume this conversation in a fresh Codex window; copy each standalone permission/completion/worker/empty/all command into fish and verify `--plain` reaches the same invocation without cleanup. No sudo is needed. Current-session Alt+R or `/raw` is an alternative to a fresh launch.

- Root independently reviewed the final [rendered-copy incident](../docs/postmortem/2026-10-09-codex-wrapped-command-padding.md), ledger finding and matching guidance. Targeted `check --postmortem /home/example/linux-config/docs/postmortem/2026-10-09-codex-wrapped-command-padding.md` returned document_count 1, errors/new/changed/missing_sources/unregistered_aliases empty, exit 0. Finding remains activation_pending/supported/code.
- Final refresh after the tracked learning update passed; live and source config/policy match. Implementation and manual-example handoff are ready. Actual copying a wrapped command in the user's fresh Codex window remains the only required acceptance check.

## Follow-up: syntax colors with raw copying

The user requires syntax highlighting as well as clean wrapped copying. A plain command paragraph appears in one uniform color in the supplied screenshot. Keep raw-output startup enabled and test a language-tagged shell block as the smallest change. No binary, terminal or theme change is required if this works.

- [x] Record fresh git status and preserve current policy/docs snapshots before edits.
- [x] Read current raw/theme settings and official raw/theme documentation.
- [x] Manual defining baseline: the user's raw-view screenshot displays the previous plain-text command uniformly.
- [x] Emit the same long command inside a top-level fish code block; user reports "Different syntax colors" in raw mode. This establishes visible syntax coloring, not paste acceptance.
- [x] Correct policy, append-only feedback and matching docs to permit tagged shell blocks in raw mode.
- [ ] Verify the same highlighted command pastes cleanly and reaches PASS permission (user action pending).
- [x] Update the existing living incident/learning, run refresh-config and independently verify final source/install state.

Decision: language-tagged top-level fish/bash fences provide the requested colors in the observed raw session. Each command inside remains one physical line without indentation or prompt markers. Retire the blanket plain-paragraph/no-fence restriction; preserve history and keep paste acceptance separate. The native task title is Highlight copy-friendly commands.

- Replaced the blanket no-fence rule with language-tagged top-level shell blocks in the policy, README and existing smoke check. Raw-output startup and the existing theme remain unchanged. Copied highlighted-block acceptance is still pending.

- Syntax colors are established by the user's direct reply "Different syntax colors" to the raw-mode fish-block comparison. The same-block copying question is still pending; preserve that distinction in the final report.
- `fish -c 'refresh-config'` reported REFRESH COMPLETE, exit 0, after the revised policy and feedback. Fresh source/install byte comparison passed, live raw_output_mode remained true, and the append-only feedback preserved every baseline byte. Session-only policy/README/smoke diffs were reviewed; no theme, Codex binary or shell-helper change was needed.

- Root independently read the updated rendered-copy incident and ran targeted memory check: document_count 1; errors/new/changed/missing_sources/unregistered_aliases all empty; exit 0. Reviewed hash 45d9636d03cfe581e2c4bf3251535edc8c77e1660a4097743b53e191f068ea10. User-confirmed syntax colors are recorded separately; overall copying remains activation_pending.
- Final refresh after the tracked learning update passed, and fresh installed policy/source equality plus live raw-output true checks passed. The syntax-highlighting preference is installed. Actual same-block paste/execution acceptance is the remaining manual check.

## Follow-up: separate runnable commands from displayed code

Update the command/code distinction, save the compiled prompt, sync the installed guidance, and measure actual terminal copying and syntax colors independently. Earlier follow-ups above are historical evidence; their fenced-runnable-command decision is superseded by this user request.

### Context, boundaries and decisions

- Source of intent: the supplied optimized prompt, saved without wrapper text in [prompts/codex-command-formatting.md](../prompts/codex-command-formatting.md).
- Files: canonical policy, append-only feedback, README, existing smoke entries, this plan and the compiled prompt. Required startup incident and its reviewed ledger are bounded companions. No commit or push is authorized.
- Initial status captured before successful writes. Target files were already dirty; snapshots in `/tmp/codex-command-formatting-before` protect that state. Apply only narrow session changes; never restore whole files from HEAD.
- Settled distinction: runnable commands are bare, column-zero, one-line fish text; reading material and expected output retain normal tagged fences and indentation. “Raw” applies to command presentation, not every part of the conversation.
- Configuration baseline: live and tracked raw_output_mode are true. Keep persisted rendering settings unchanged unless an actual supported alternative meets copying and highlighting requirements. No binary, renderer, terminal or theme patches.
- Official current reference documents raw startup, /raw or Alt+R toggling, and a syntax theme setting, but provides no selective per-content rendering guarantee. Source: [configuration reference](https://developers.openai.com/codex/config-reference/), fetched via official documentation MCP on 2026-10-09.
- Ruling: execute the supplied plan in the current checkout with this existing ExecPlan; no new worktree or planning-only pause, because the user explicitly authorized implementation and forbids unrequested worktrees/commits.
- This is a prose-policy change. Review the conflicting baseline and revised text directly; do not add implementation-mirroring tests. Actual UI selection/paste is the acceptance reproducer and cannot be replaced by a fish syntax check.

### Ordered checklist

- [x] Capture status, inspect source/history, preserve dirty target snapshots and record startup incident.
- [x] Replace the conflicting canonical rule, append the superseding preference and align README/smoke checks.
- [x] Save only the compiled prompt in the planned artifact.
- [x] Emit all five cases in the installed TUI, compare code colors and inspect native selected bytes; run source commands in fresh fish processes.
- [ ] Accept exact wrapped-command selection/paste/execution in a fresh fish terminal (unverified; automation boundaries did not establish acceptance).
- [x] Run refresh-config and verify installed guidance plus preserved rendering settings and append-only feedback.
- [x] Review the complete session diff and record evidence, limits and rollback.

### Evaluation cases

Use a mixed Codex response with the five runnable cases below plus indented Python, JSON and diff fenced blocks. Working directory: `/home/example/linux-config`; no sudo. Select the visibly wrapped command from the actual TUI and paste it into a newly opened fish terminal; inspect clipboard bytes before pressing Enter. Compare raw and formatted views using the session toggle only, restoring the initial view afterwards. Keep commands below as one physical line each.

Long wrapped command:

python3 -c 'import sys; print("wrapped: " + " ".join(sys.argv[1:]))' --message=deliberately-long-value-used-to-force-this-command-to-wrap-across-narrow-and-wide-terminal-windows-without-changing-its-physical-line --plain

Example expected output:

```text
wrapped: --message=deliberately-long-value-used-to-force-this-command-to-wrap-across-narrow-and-wide-terminal-windows-without-changing-its-physical-line --plain
```

Quoted spaces and punctuation:

printf '%s\n' 'quoted: spaces; punctuation & $ (literal)'

Example expected output:

```text
quoted: spaces; punctuation & $ (literal)
```

Pipeline:

printf '%s\n' beta alpha | sort

Example expected output:

```text
alpha
beta
```

Fish substitution:

printf 'substitution: %s\n' (string upper fish)

Example expected output:

```text
substitution: FISH
```

Mixed response command (follow with reading blocks below):

printf 'mixed: %s\n' 'ready'

Example expected output:

```text
mixed: ready
```

Reading material, not runnable command lines:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

```json
{
  "ready": true,
  "count": 2
}
```

```diff
-old = False
+new = True
```

### Verification, risks and rollback

- Automated/prose checks: inspect session-only diffs against the snapshots, verify feedback starts with every baseline byte, compare installed/source policy and TOML, and run targeted postmortem-memory coverage. No application behavior changed, so unrelated test suites do not establish this formatting acceptance.
- Runtime: record exact selected clipboard contents, hard-newline/padding presence, fresh-fish pasted/executed output and visible token colors for each mode. Captured ANSI or a tagged fence alone is insufficient proof of visible colors.
- refresh-config is required after final tracked changes; it snapshots live Codex config into tracked source, applies chezmoi, regenerates shortcuts and reloads fish. Inspect any resulting extra source changes without overwriting unrelated work.
- Risk: instruction-compliant Markdown may still wrap or lose colors in this installed renderer. Report observed limits and leave acceptance pending when either requirement is unproved.
- Rollback: reverse only session-added/replaced hunks and the exact appended preference; preserve historical evidence and all initial dirty work. Persisted rendering settings remain protected.
- Startup failure and known workaround are in [the task incident](../docs/postmortem/2026-10-09-command-formatting-sandbox-startup.md); the reviewed ledger explicitly records no new reusable learning.

### Current progress and review notes

- Guidance and prompt edits reviewed by a fresh-context read-only reviewer: no substantive findings. Prompt contains only the compiled intent; feedback baseline remains an exact byte prefix. Runtime acceptance was explicitly outside that review.
- Five saved cases executed with `fish --no-config -c COMMAND`; each produced exact documented stdout, empty stderr and exit 0. All separate `fish --no-config -n -c COMMAND` checks passed. Commands came from the Evaluation cases section; these checks do not prove selection/paste.
- Actual raw screenshot: literal Python/JSON/diff fences and uniform pink text. Actual formatted screenshot: distinct Python/JSON token colors and red/green diff; reading-code indentation preserved. Native formatted selected bytes contain hard breaks and two-space command prefixes, but outer boundaries were wrong; no invalid selection was executed.
- Actual exact clipboard-to-fresh-fish acceptance remains unverified: initial probes had zero selection, later probes selected real terminal bytes with wrong boundaries. The raw exact-match failures are not evidence that raw copying fails. Original raw session view restored through supported Kitty send-key; saved raw startup/theme were not changed.
- Rendering limitation and current tracked finding are in [the mixed-content comparison](../docs/postmortem/2026-10-09-codex-mixed-content-rendering.md). Keep overall acceptance pending; no supported alternative demonstrated both requirements.
- Ruling: preserve persisted rendering settings because observed comparison does not meet both requirements. Cost if wrong: the operator still needs to perform the documented native copy check or identify a better supported view.
- Protected concurrent change: config reasoning effort differs from the initial snapshot, while the entire TUI table remains unchanged. Preserve that live/user change; do not attribute it to this rendering task.
- `fish -c 'refresh-config'`: observed normal snapshot/apply/shortcut stages and REFRESH COMPLETE, exit 0. Fresh byte comparisons confirm installed `~/.codex/AGENTS.md` equals the source and live/source TOML matches. The entire TUI table equals its protected pre-refresh value; no tracked file changed during that refresh interval.
- Separate targeted memory checks for each current report returned document_count 1, no errors/new/changed/missing_sources/unregistered_aliases, exit 0. Reviewed startup/probe hash: `ed9aeeba7b54083e26dbc7191f2c145afb9b54d5ed1e6c27afa2ee478f2d2e62`; mixed-content hash: `e09884b40a10eb36638e117257f5a0c6512852e1cad8c148d912a61b7d8ec51d`. The current report links reciprocally to `local-codex-rendered-command-copy`; the incidental helper report has an explicit no-new-learning decision.
- Final root review read the session-only canonical/README/smoke diffs against protected snapshots. Added lines have no trailing whitespace; prior feedback bytes remain an exact prefix. The fresh reviewer found no substantive guidance/prompt issues; actual runtime acceptance remained outside that review.
- Original clipboard and primary selections and task focus restored; the original raw session view remains active. Screenshots and disposable probes stay under `/tmp`, outside version control.
- Documentation/instruction implementation and sync are complete. Runtime acceptance is explicitly unresolved: no reliable exact wrapped selection/paste into a fresh fish terminal was established, and no supported view satisfied both required results. Keep the pending acceptance checkbox above unchecked. Final handoff provides the five saved copy probes and reading blocks, with no copying-repair claim.
- No commit or push was performed. Current scoped changes include the policy/docs/prompt, append-only preference, plan, one local lesson, two task reports and their tracked reviewed learning. The separate reasoning-effort change is preserved and is not a rendering change.
