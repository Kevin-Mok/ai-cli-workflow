# Codex wrapped commands retain display padding

The one-line formatting rule did not make wrapped Codex commands copy cleanly
into fish. This report separates source text, rendered terminal selection, and
paste acceptance, then records the supported raw-output setting and remaining
active-session verification.

## Symptom and impact

The user's screenshot `/tmp/codex-clipboard-LuwuM3.png` shows the final reply's
fenced one-line command wrapping before `--plain`, with two leading spaces
remaining. The user confirmed those spaces break clean copying into a new
terminal. No notification or shell behavior changed.

## Reproducer and diagnostic evidence

- The previous final reply used a top-level fenced fish code block containing
  one physical command line. The screenshot and reported copied text reproduce
  padding before the wrapped `--plain` flag.
- Fish syntax parsing and silent notification probes verify command execution,
  not renderer or clipboard behavior. Their earlier passing results did not
  establish the user's copying requirement.
- A standalone plain command paragraph was emitted for comparison. The user
  reiterated the general leading-space and newline problem; the paragraph's
  rendered-copy acceptance was not confirmed either way.
- The inspected repository wrapper passes CLI arguments through without
  transforming assistant text. Installed Codex is the npm launcher, version
  0.162.0; no Rust source checkout was found at the inspected known location.
- Supported cause: verification addressed source-line syntax while the failure
  occurs in rendered terminal selection. Code-block display padding is a
  supported explanation, not a confirmed diagnosis of clipboard bytes or the
  terminal's wrapping behavior.

## Lookup and supported option

- Initial query `codex code block wrapping indentation copied command leading
  spaces` returned unrelated Python indentation, backup and Codex-isolation
  findings. Follow-up query `Codex wrapped command leading spaces raw output
  terminal copy paste` likewise established no applicable renderer-copy remedy.
- The current official [Codex configuration reference](https://developers.openai.com/codex/config-reference/#tui)
  documents boolean `tui.raw_output_mode`: copy-friendly raw scrollback, default
  false, with `/raw` or Alt+R for the current session. This is a supported
  rendering option; documentation alone does not prove clipboard repair here.
- Both live and tracked `tui.raw_output_mode` were unset before implementation.
  The intentional assertion requiring true observed RED with exit 1; this is
  the expected configuration baseline, not an unexpected command failure.

## Resolution, status and next steps

The parent enabled only `tui.raw_output_mode = true` in tracked Codex config.
Scoped `chezmoi apply --force ~/.codex/config.toml` exited 0. The existing
`IsolatedCodex._probe` strict `config/read` check, with effective MCP servers and
isolation features disabled and no thread/inference request, reported
`Codex effective tui.raw_output_mode: True`; live and tracked TOML bytes matched,
exit 0. `fish -c 'refresh-config'` then exited 0 with `REFRESH COMPLETE`
(log: `/tmp/refresh-config-20261009-151015-931723.log`). Fresh installed AGENTS
byte comparison and live `raw_output_mode = true` verification also passed with
exit 0. No Codex binary or terminal-renderer code was changed.

The subsequent raw-view highlighting check corrects the blanket no-fences
instruction. Current npm Codex remains 0.162.0; live and tracked raw_output_mode
are true and the theme is `one-half-light`. A screenshot showed a plain raw
command in one uniform color. The parent emitted the same long command in a
top-level `fish`-tagged fenced block and asked whether raw mode showed syntax
colors or literal fence markers with one uniform color. The user answered
“Different syntax colors.” This is observed runtime evidence for highlighting,
not copied-text acceptance. No binary, theme or additional raw-output setting
change was made. The revised tagged-block instruction and append-only preference
were synced by `fish -c 'refresh-config'`, which exited 0 with `REFRESH COMPLETE`
(log: `/tmp/refresh-config-20261009-152833-985343.log`). Fresh installed AGENTS
matched its source, live raw_output_mode remained true, and all before-edit
feedback bytes were preserved.

Prefer top-level `fish` or `bash` language-tagged fenced blocks under raw mode,
with one physical, unindented command line inside each block and no containing
list, blockquote or prompt marker. Use plain command paragraphs only as a
fallback if an actual copying problem remains. Source formatting and observed
colors do not by themselves establish clean terminal selection or pasting.

The user subsequently asked for commands to check in a new Codex window. This
requests manual examples; it is not confirmation that copying or pasting works.

Status remains activation_pending, with supported confidence and code
verification scope for the overall copy remedy. The user-confirmed runtime
color observation is recorded separately. The parent has asked whether that
same highlighted, visibly wrapped block pastes into a new fish terminal without
leading spaces or hard line breaks and reaches the expected `PASS permission`
result; the reply is pending. For a fresh Codex session use the saved raw-output
preference, or toggle `/raw` or Alt+R in an existing session. The available
toolset cannot operate the active native terminal. Do not label clipboard
repair verified before the actual same-block paste/execution check passes.

## Learning

Finding `local-codex-rendered-command-copy` records the narrow reusable lesson:
a one-line source command and fish probes cannot verify rendered-copy behavior.
Raw mode with a language-tagged top-level shell fence has user-confirmed syntax
colors in this session, so the earlier blanket no-fences remedy is superseded.
Prefer that combination with one physical unindented command line; keep plain
paragraphs as a fallback for an observed unresolved copying problem. Verify
installed/effective settings, rendered colors and actual pasted-command
acceptance separately. Retain **activation_pending**, **supported** confidence,
and overall **code** verification scope until the latter passes. Move the
reviewed report hash and reciprocal finding/reference links together, then run
the targeted memory check. Preserve unrelated ledger edits and the prior task
incident.
