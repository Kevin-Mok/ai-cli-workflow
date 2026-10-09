# Codex mixed-content rendering: copying and code colors

This comparison separates command copying from code highlighting in the installed TUI. Review the two live views, inspect actual selected bytes, and require a clean paste and execution in a fresh fish terminal before accepting a rendering setting.

## Symptom, scope and evidence

- Installed npm TUI: `codex-cli 0.162.0`, with live/tracked `tui.raw_output_mode = true`. No Codex binary, renderer, terminal or theme was patched.
- User intent: standalone bare fish commands, with normal tagged fences and indentation for Python, JSON, diffs and expected output. The earlier fenced-runnable-command preference is superseded; its historical evidence remains intact.
- Raw-view screenshot [mixed content](/tmp/codex-command-formatting-mixed-raw.png) visibly shows literal fence markers and uniform pink text for the Python, JSON and diff examples. The bare long command wraps visually. This is an observed highlighting failure for these examples, not a blanket statement about every language or prior shell-color observation.
- Formatted-view screenshot [selected command and code colors](/tmp/codex-formatting-ui/formatted-cases.png) shows Python token colors, JSON key/value colors and red/green diff lines, preserving reading-code indentation. The long bare command is rendered on indented hard lines. Native selected clipboard bytes contain hard newlines and two-space prefixes inside that command, including a break within the long argument.
- The formatted selection also included preceding context and missed its final character. It proves those selected command fragments contain renderer hard breaks/padding, but is not a valid exact-command paste acceptance test. It was never executed.
- Initial disposable drag probes produced no selection or wrong boundaries. Their false exact-match results are measurement limitations, not evidence that raw copying fails. Later native selection did copy actual terminal bytes, but exact wrapped-command boundaries were not validated. Do not promote a stale clipboard or partial selection into a passing/failing command-copy claim.
- Both views were reached through the advertised per-session Alt+R toggle via the supported Kitty send-key API. The window-directed synthetic toggle did not establish a mode change. Restored the original raw session view; no saved rendering setting was changed.
- All five saved evaluation commands were executed with `fish --no-config -c` in `/home/example/linux-config`: wrapped flags, quoted punctuation, pipeline, fish substitution and mixed-response command. Each returned its documented stdout, empty stderr and exit 0. Separate `fish --no-config -n -c` checks passed. Source execution and parsing do not prove clipboard behavior.

## Impact, cause and resolution status

The instruction and documentation distinction can be implemented, but these observed views have not established both required outcomes. Session-wide raw rendering loses the tested code colors; formatted rendering introduces command padding/hard wrapping. The exact clipboard-to-fresh-fish acceptance check remains pending because native selection boundaries could not be reliably automated. No alternative rendering setting was persisted without both outcomes.

The cause is supported at the observed rendering boundary; no underlying renderer internals were modified or diagnosed. Do not claim a clipboard repair, a complete product fix, or impossibility across every supported setting.

## Lookup, learning and follow-up

- Lookup: `Kitty selection clipboard XSendEvent coordinates` returned `local-codex-rendered-command-copy`; its distinction between source syntax, colors and actual clipboard acceptance applies to the same installed npm version. Its earlier fenced-command remedy is superseded by current user intent, while its prior user-confirmed shell colors remain valid historical evidence.
- Update the tracked finding and editing-shell-transport reference with the current distinction, observed Python/JSON/diff view comparison, and explicit unverified exact-paste limit. Keep status `activation_pending`, confidence `supported`, verification scope `code`; runtime color observations do not establish clipboard repair.
- Follow-up: perform the five saved cases using deliberate native selection in a stable viewport and paste the exact captured command into a fresh fish terminal. Inspect visible colors independently. Persist a supported alternative only if both requirements pass; keep this limitation explicit until then.
- Disposable-probe defects and the startup workaround are recorded separately in [the task verification incident](2026-10-09-command-formatting-sandbox-startup.md). No new generic finding is warranted for those helper mistakes.
