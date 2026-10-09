---
name: fish-alias
description: Use when adding or replacing a fish command, directory, or file shortcut from an abbreviation followed by a command or path in example-user's linux-config repository.
---

# Fish Alias

Turn an abbreviation plus its complete command or path into a shortcut in the existing template section. Preview the change, preserve conflicting definitions as comments, then apply and refresh the installed configuration.

Example request: `$fish-alias cbn codex-time burn day` adds `cbn "codex-time burn day"` to the existing **work** section of `aliases/key_aliases.tmpl`. Examples are requests only when the user actually invokes them; do not activate documentation examples.

## Input and routing

Treat the first token as the source key and retain the entire remainder as the command/path, including internal spacing, quotes and metacharacters, except for directory home-prefix normalization described below. Do not split and rebuild command arguments. Ask for missing input or genuinely ambiguous intent; the user need not supply a template or section.

Canonical repository: `/home/example/linux-config`. Read its applicable instructions and current source files; capture dirty state and preserve unrelated work.

- Commands belong in `aliases/key_aliases.tmpl`.
- Directory paths belong in `aliases/key_dirs.tmpl`.
  After identifying a directory, replace its leading `/home/example` (exact home or followed by `/`) with `~` before choosing its section and storing it. For example, `/home/example/coding/track-codex-sessions` becomes `~/coding/track-codex-sessions`. Unquote and escape spaces as needed so `~` expands in fish. Commands, file mappings, other users and embedded home strings keep their original text. Repeating the pasted absolute directory is a no-op once normalized.
- File paths belong in `aliases/key_files.tmpl`. Existing file conventions prefix the source key with `n` in fish: `re README.md` produces **nre**. Report this effective abbreviation. If the user explicitly names a desired fish abbreviation instead of a source key, resolve that distinction before editing.

Prefer actual path type; a trailing slash identifies a directory, a file suffix helps identify a nonexistent file. Commands with arguments remain commands even when an argument names a file. Inspect nearby related entries to select the closest existing section. Codex executables belong in **work**. The helper previews executable-family/path-prefix placement; override its `section` when source inspection supports a better existing section. For unresolved path type, ask then supply `kind` (`commands`, `dirs`, `files`).

## Safe edit and verification

Use [scripts/fish_alias.py](scripts/fish_alias.py) with Python 3. JSON on stdin preserves the request without shell expansion:

```json
{"input": "cbn codex-time burn day"}
```

For structured agent review, run `python3 <skill-directory>/scripts/fish_alias.py --repo /home/example/linux-config --json` to preview; repeat with `--apply` to write. Pass JSON using a structured tool/file or a **single-quoted heredoc delimiter**, never shell-interpolated command text. Optional `kind` and `section` fields are agent routing aids, not required user input.

Default CLI output is a readable summary; `--plain` uses ASCII, `--details` includes the diff/error evidence, and `--json` exports structured output. Review the diff before applying. The helper renders templates with current chezmoi data, compares effective fish names across all three sources, and prefixes each active conflict line with exactly `# `. It keeps inactive branches, already commented lines and unrelated keys intact. An identical active mapping is a no-op. New mappings go outside conditional blocks. Conditional activation is host-specific; explain any inactive definitions that could conflict on another host. Template delimiters in requests are rejected before evaluation. Requests containing template delimiters (`{{` or `}}`), unsupported template layouts, or multiline input require manual inspection rather than speculative edits. Request delimiters are rejected before rendering.

Never execute the supplied command, including as a smoke test. Check generated syntax with `fish -n`; use disposable fixture generation when needed. After a changed mapping, run the repository's `refresh-config` convention and check rendered sources/generated abbreviations. Refresh snapshots live Codex and Git configs into tracked sources, applies chezmoi and regenerates/reloads shortcuts; preserve protected dirty state. Report the source, section, effective abbreviation, commented conflicts and actual verification result. A no-op needs no refresh.

## Callable commands versus abbreviations

An abbreviation expands interactive input; it is not a callable command and existing shells may not have loaded a newly generated abbreviation. When the user asks for a stored command usable literally (including flags or scripts), provide an executable or a tracked autoload function in `dot_config/fish/functions/NAME.fish` as appropriate. Forward arguments with `$argv` without joining or evaluating them. Keep abbreviation-only requests on the existing helper workflow.

Verify resolution without expanding abbreviations: `fish -c 'functions -q NAME; and functions NAME'` is read-only and does not run the supplied command. For isolated `fish --no-config` fixtures, explicitly set `fish_function_path` to the fixture directory: no-config omits the normal user function directory on this host. Verify deployment after refresh-config, rather than treating generated abbreviation text as command availability.
