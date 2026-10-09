Update Codex command-formatting guidance in /home/example/linux-config.

Apply this distinction throughout replies:
- Shell commands intended for the user to paste into another terminal must appear as standalone raw text, one physical line per command, starting at column zero. Do not use fences, inline backticks, list prefixes, blockquotes, prompt markers, continuation backslashes or inserted line breaks. Keep every argument and flag on that line and use valid fish syntax.
- Code intended for reading—including source snippets, diffs, JSON and illustrative shell code—should use normal language-tagged fenced blocks with syntax highlighting. Preserve meaningful indentation.
- Expected output belongs in a separate labeled code block. Keep explanations and working-directory or sudo requirements outside runnable command lines.

Use the latest user preference to replace conflicting guidance in dot_codex/AGENTS.md. Append the preference to canonical feedback without rewriting history, and align the existing README, smoke checks and formatting plan.

Scope changes to instructions and supported configuration. Preserve unrelated work. Do not patch Codex binaries, renderer source or terminal software.

Verify copying and highlighting separately in a mixed-content response. Test a visibly wrapped command by selecting it and pasting into a fresh fish terminal; source formatting and syntax parsing alone do not prove copying works. Confirm actual syntax colors on Python, JSON and diff blocks rather than assuming language tags guarantee them.

Change rendering settings only when observed evidence demonstrates that the supported alternative satisfies both requirements. If the installed Codex cannot provide both, report the exact limitation without claiming success.

Follow repository planning, verification and refresh-config requirements. Do not commit or push unless separately requested.
