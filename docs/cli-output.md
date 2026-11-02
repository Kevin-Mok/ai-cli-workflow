# CLI and script output

Human-facing script output now uses appropriate decorative emojis so headings, progress, prompts, successes, warnings and errors are easier to scan. Use normal output first, choose plain mode when needed, and keep machine/protocol output clean. The commands below exercise safe help and listing paths without installing packages, playing audio or changing services.

## Output conventions

- 📖 help, 🔧 setup, ⏳ progress, ✅ success, ⚠️ warning and ❌ error cues accompany readable words. Topic cues such as 🎙️ voices, 🐟 fish, 💾 backups and 📅 file dates identify the task.
- Existing `--plain` flags retain their behavior. For legacy scripts without that flag, set `CLI_PLAIN=1` for the invocation. This removes decoration; it does not rewrite user data, paths, names or third-party diagnostics to ASCII.
- `NO_COLOR` controls ANSI colors independently of emoji decoration. Narrow-width rendering and `--details` remain in existing formatted CLIs.
- JSON/CSV, status tokens, numeric data, raw filenames, passwords/clipboard data, generated files, diffs and command-substitution results remain undecorated. Silent commands stay silent. External tools and unmodified parser diagnostics keep their own formatting.
- Scripts remain independently runnable; shell/Python prose helpers are local. Fish functions use the installed autoloadable `cli-message` helper.

## Workflow checks in agents and pipes

The README gate, workflow doctor and vetted-skill checker automatically suppress
decoration when stdout is not a terminal or CODEX_*/CLAUDECODE variables are set.
Human terminals keep their existing presentation; NO_COLOR alone keeps emojis.
Use --plain (first argument for the README helper) or CLI_PLAIN=1 explicitly.
Doctor text and vetted --check use concise agent summaries; --details restores
full findings/inventory. Every inventory error and failure status remains.
Doctor --format json and vetted --json remain complete machine-readable data.
Other legacy helpers retain their documented presentation controls.

## Safe direct verification

Working directory: `/home/example/linux-config`. No sudo is needed. All commands below are read-only help/listing or presentation checks. Expected examples are abbreviated and variable paths/data may differ.

```bash
bash scripts/executable_setup-mosh.sh --help
```

Expected output:

```text
📖 Usage:
  ./scripts/executable_setup-mosh.sh [--udp-port PORT|START:END]
...
```

```bash
env CLI_PLAIN=1 bash scripts/executable_setup-mosh.sh --help
```

Expected output:

```text
Usage:
  ./scripts/executable_setup-mosh.sh [--udp-port PORT|START:END]
...
```

```bash
python3 scripts/executable_codex-voice-auditions --list
```

Expected output:

```text
🎙️ Ten local voice alternatives
🎙️  1 Amy          US  en_US-amy-medium
...
```

```bash
env CLI_PLAIN=1 python3 scripts/executable_codex-voice-auditions --list
```

Expected output:

```text
Ten local voice alternatives
 1 Amy          US  en_US-amy-medium
...
```

```bash
bash scripts/executable_backup-pc excludes
```

Expected output:

```text
# Omit runtime/cache contents; retain mount directories and persistent state.
./dev/*
./proc/*
...
```

```fish
fish --no-config -c 'source dot_config/fish/functions/cli-message.fish; cli-message ✅ "Output ready"'
```

Expected output:

```text
✅ Output ready
```

```fish
env CLI_PLAIN=1 fish --no-config -c 'source dot_config/fish/functions/cli-message.fish; cli-message ✅ "Output ready"'
```

Expected output:

```text
Output ready
```

## Scope and verification record

The [rollout plan](../plans/cli-emoji-rollout.md) records the approved scope, protected dirty state, exact automated checks, activation evidence, review notes and remaining baseline limitations. It also includes the atomic continuation plan and a paste-ready Cursor prompt. The [source inventory](cli-output-inventory.json) distinguishes human output from data, protocols, library modules, terminal art and third-party passthrough. Benchmark CLI descriptions are decorated while JSON trial/results and immutable candidate snapshots remain unchanged. Skill helpers decorate authored prose/help while keeping requests, transcripts, screenshot paths and generated diffs clean.

For a future commit, include the matching plan and documentation updates with the implementation; suggested subject: `feat(cli): decorate human-readable script output`.
