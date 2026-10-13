# Notification Markdown inspection environment

Locate the running Kitty installation and inspect its notification dispatch before adding Markdown formatting.

## Symptom and impact
Inspection guessed /usr/lib/kitty/kitty/notifications.py, which is absent; executable is user-local. A piped memory search also emitted BrokenPipeError because head closed stdout. No notification behavior was changed by those commands.

## Lookup and status
Search `missing installed path broken pipe diagnostic`: applicable guidance is to locate actual executable/module paths and capture complete structured output before selecting records. Use kitty +runpy to locate its real notifications module; avoid truncating helper stdout through head. Actual frozen module located with kitty +runpy; installed 0.49.2 NotificationCommand is a regular annotated class, not a dataclass. The earlier dataclasses.fields inspection raised TypeError; corrected to class annotations. No runtime fix claimed.

## Next steps
Read actual module path, implement after defining RED, then test delivery. This incident contains no new reusable learning beyond existing path-discovery and structured-output guidance.

## Recovery evidence
Installed class annotations and bytecode inspected successfully; official matching source confirms FreeDesktopIntegration prevents body markup by replacing angle brackets and ampersands with zero-width-separated variants. Query output is now captured before selecting results. No new learning beyond existing path/API discovery.

## Activation failure
After successful refresh and seven unit checks, --activate-all returned no reachable instance despite known socket files. Callback writes are deployed; activation is not yet verified. Inspect one remote custom-kitten response before retrying to distinguish socket reachability from plugin invocation failure.

## Activation resolution and verification
Remote custom kitten response showed NameError: __file__ is not defined. A test deliberately removes __file__ and observed RED; use Kitty's config_dir instead, then all seven focused checks pass. The corrected helper reports diagnostics under --details instead of conflating plugin failures with missing sockets.
Refresh completed; --activate-all succeeded in 12 live Kitty instances. A native DBus capture confirms the generated bold tags reach Dunst intact. Literal/code and plain cases send successfully. Existing notification regression suite exits 0. No terminal restart or native manager reset. The earlier dataclass/path inspections were corrected with installed class annotations and real frozen-module dispatch evidence.

## Learning review
No new general finding: installed API/context discovery and optional-path guidance already cover assumptions about module layout and execution globals. This incident records the specific config_dir adaptation and runtime evidence; source hash reviewed with explicit no-new-learning decision. Future formatting changes must exercise actual Kitty dispatch rather than unit fixtures alone.

## Staged fixture limitation
The isolated staged snapshot passed seven Markdown checks, but the existing 60-test sound suite raised one FileNotFoundError because it reads ignored machine-local dot_codex/config.toml, which git checkout-index does not export. The same suite passes in the working repository. Inspect the test prerequisite and add only a sanitized temporary fixture, never stage the local config, before rerunning. This is fixture completeness, not a Markdown regression.

## Type-check review
Host basedpyright identified a real str.replace override mismatch (count must accept SupportsIndex), a nullable __doc__ CLI description, and an imprecise native Boss annotation. Fix those scoped contracts. Add a defining RED for a count object implementing __index__, then normalize it with operator.index. Embedded frozen Kitty imports are unavailable in host Python; exclude only those specific import diagnostics and rely on the verified native activation/DBus checks for that API boundary. No broad type diagnostics disabled.

The isolated snapshot type check resolves embedded Kitty imports differently from the repository namespace. Its OnlyWhen import additionally needed the same narrowly scoped reportMissingImports exclusion; no broad diagnostics disabled. Recheck both staged and live API boundaries.

## Final commit verification
Resolved staged prerequisite with a minimal public notify-only TOML fixture in /tmp; no ignored/local config staged or copied. All 68 staged tests pass (8 Markdown and 60 existing sound checks). Final staged basedpyright reports zero errors with only the documented embedded-import exclusions. Refresh completed; current activation acknowledged 11 reachable instances and a fresh native DBus capture confirms intact bold tags. Targeted incident learning and staged README validation pass. Host import-layout differences and standard SupportsIndex contract are documented; no additional repo-specific policy required.
