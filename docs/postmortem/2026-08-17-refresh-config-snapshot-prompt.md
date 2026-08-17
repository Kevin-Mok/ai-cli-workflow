# Refresh-Config Snapshot Apply Prompt

## Symptom

`refresh-config` copied the live Codex configuration into the tracked source,
then paused at ChezMoi's `diff/overwrite/all-overwrite/skip/quit` prompt for
that same `~/.codex/config.toml` target.

## Impact

The one-step refresh workflow required manual intervention even when the user
had explicitly chosen to snapshot that live configuration, interrupting the
remaining ChezMoi apply, shortcut refresh, and Fish reload.

## Evidence

The captured terminal output shows `Codex config snapshot completed` followed
by ChezMoi reporting `.codex/config.toml has changed since chezmoi last wrote
it?`. A later retry emitted `snapshot-codex-config: snapshot validation failed`;
read-only diagnostics confirmed the original interactive `chezmoi apply` process
remains on `pts/14` and holds ChezMoi persistent state.

## Current Status

Resolved: the helper captures and targeted-force-applies its Codex and Git
configurations, normalizes only blank Git helper assignments, and then completes
the unforced broad ChezMoi apply without prompts.

## Additional Finding

The requested Git-config capture used a direct copy, preserving trailing spaces
after blank `helper =` assignments. Those spaces are semantically unnecessary
but fail repository diff validation.

## Root Cause

The broad `chezmoi apply` ran after `refresh-config` had intentionally changed
its own tracked Codex source, and later its tracked Git source. ChezMoi therefore
treated each matching live target as locally modified since its last write and
requested an overwrite decision.

## Resolution

After each intentional capture, `refresh-config` now force-applies only that
exact target: `~/.codex/config.toml` after `snapshot-codex-config`, and
`~/.gitconfig` after copying it into the ChezMoi source. It normalizes only
blank `helper =` assignments to satisfy whitespace validation, then runs the
existing unforced broad apply so unrelated targets retain normal conflict
protection.

## Verification

The focused shell regression first failed because neither targeted Git-config
resolution nor force-apply existed, then passed after the change. A live run
completed the Codex snapshot, both targeted applies, the normal ChezMoi apply,
shortcut synchronization, and Fish reload without a prompt; `git diff --check`
then reported no whitespace error for the captured Git config.

## Follow-up

Keep future intentional captures paired with a force apply for only their exact
managed target; never broaden `--force` to the full ChezMoi apply.
