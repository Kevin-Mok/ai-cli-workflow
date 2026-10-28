# Cli And Shell

Read this procedure when its mandatory canonical AGENTS trigger applies. Follow
the preserved rules below before acting; active user/developer instructions govern.

- All human-facing CLI, script and shell-helper output must include appropriate
  decorative emojis by default: headings, progress, prompts, successes, warnings
  and errors. Keep clear hierarchy, plain-language labels, aligned values and
  readable dates/durations; text must remain understandable without the glyphs.
  Apply this to existing tools when changing them and to all new tools. Keep raw
  diagnostics behind `--details` with concise actionable accuracy warnings.
  Provide `--plain` for ASCII output; legacy helpers may use `CLI_PLAIN=1`.
  Preserve JSON/CSV, protocol/status tokens, paths consumed by tools, clipboard
  data, generated files and command substitutions. Keep silent commands silent.
  Respect terminal width; `NO_COLOR` disables ANSI colors without removing emojis.
- When creating or changing a CLI that may run for a long time or appear to
  hang, always show ongoing progress by default: periodic status lines, a
  progress indicator, percentage complete, or elapsed time and estimated time
  remaining when reliable. Keep updates flowing during slow or blocking phases;
  a startup message alone is insufficient. If total work is unknown, report
  activity and elapsed time rather than inventing a percentage or ETA. Send
  progress to stderr when stdout carries machine-readable output.
- Separate runnable shell commands from code intended for reading in Codex
  replies. Shell commands intended to paste into another terminal must be
  standalone raw-text lines, one physical line per command, starting at column
  zero and using valid fish syntax. Do not use fences, inline backticks, list
  prefixes, blockquotes, prompt markers, continuation backslashes or inserted
  line breaks. Keep every argument and flag on that line; terminal visual
  wrapping is acceptable only when selection preserves the command text.
  Code intended for reading, including source snippets, diffs, JSON and
  illustrative shell code, uses normal language-tagged fenced blocks with
  meaningful indentation and syntax highlighting. Expected output belongs in
  a separate labeled code block. Put explanations, working-directory and sudo
  requirements outside runnable command lines. “Raw” describes runnable command
  presentation; it does not require raw rendering for the whole conversation.
  Verify actual wrapped selection/paste into a fresh fish terminal separately
  from visible syntax colors in Python, JSON and diff blocks; source formatting,
  language tags and syntax parsing alone do not establish either result. Change
  supported rendering settings only after observing that the alternative meets
  both requirements; otherwise report the exact installed-TUI limitation.
- When a user must run commands manually, create a reusable script instead of a
  chat-only command list. State when it requires `sudo` and provide the exact
  invocation.
