# Refresh Config Overwrote A Protected Dirty Source

## Symptom

During post-activation deployment, `refresh-config` changed the protected
`dot_codex/config.toml` checksum from its recorded pre-session value.

## Impact

The newer live Codex config remained intact, but its bytes replaced the
intentional unstaged repo-side version. Nothing was staged, committed, pushed,
or checkpointed while the protected checksum was wrong.

## Evidence

The repo checksum changed from
`3edd706e3cc03132764d9d0a1b741e0713f42e39dc16a6018ab205f9d1a85e2e` to the
live checksum
`f9e84d469f63addd863192cbadbac9145bea54872ed4526ece953efe4dc8f088`. The
snapshot helper reported a completed copy before chezmoi prompted about the
config state. A pre-refresh local Codex session log retained the exact two-line
repo diff needed for recovery.

## Root Cause

`refresh-config` is intentionally live-to-repo for Codex config. It was run
despite an active invariant that the protected dirty repo file must retain its
exact checksum. A successful dry-run of the broader chezmoi layer did not
authorize that snapshot overwrite.

## Resolution

The two repo-side values were restored from the local session evidence. The
repo checksum returned exactly to the recorded value, while the newer live
file retained its own checksum and bytes.

## Verification

`sha256sum` reports the exact pre-refresh repo checksum and the unchanged newer
live checksum. Git status again contains only the original protected config
plus the explicit follow-up work; the protected file remains unstaged.

## Follow-Up

- Run `snapshot-codex-config --dry-run` before refresh when the tracked config
  is protected or intentionally dirty.
- Stop on live/source divergence until overwrite ownership is explicit.
- Deploy exact changed targets when a full refresh would violate that boundary.
