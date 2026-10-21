# Reconcile refresh launcher conflict

Unblock refresh by reconciling the reviewed media launcher permission difference,
then verify the normal refresh and installed commands without changing content.

## Scope and decisions

The live launcher and rendered target share identical content; live mode0755
conflicts with target0775 (chezmoi umask002). The explicit installer sets0755.
Use a single exact-target apply; do not change installer policy or force the
broad apply. Current ignore rules preserve local Fish configuration; a raw
template rendering was insufficient evidence of refresh scope in the prior task.
Preserve all initial dirty source, plans, prompts, smoke and learning edits.
No commit/push requested.

## Atomic checklist

- [x] Inspect the private log, prior findings, source/live contents and mode diff.
- [x] Observe exact-target `chezmoi verify` RED; reconcile only launcher mode.
- [x] Confirm unchanged content and target verification; run normal refresh.
- [x] Check installed screensaver status and original Fish startup fix.
- [x] Update smoke/incident/knowledge and record final verification.

## Verification, risks and rollback

Use `chezmoi verify ~/scripts/media-screensaver` for defining RED/GREEN and
hash comparison to prove content unchanged. Check status for other conflicts
before retrying `refresh-config`; retain unforced broad conflict protection.
Run installed screensaver status without starting a preview and a Fish login
with VT absent. No sudo; normal home writes need workspace escalation.

Changing0755 to0775 follows the existing rendered target/source mode. Future
explicit screensaver installation can recreate the mode difference; this task
reconciles refresh state without redesigning installer permissions. Rollback:
restore only launcher mode0755, knowingly restoring the refresh conflict.

## Progress and review

Private log confirms prompt/EOF on this target. Source/live/rendered content
hashes agree. Actual `chezmoi diff` is mode-only, and `chezmoi status` identifies
no other both-modified target. Global refresh remains unforced.

Exact-target verify observed RED(exit1), guarded apply changed only mode to0775,
and verify observed GREEN(exit0) with unchanged SHA-256. A no-config Fish probe
could not discover the helper and exited127 before apply; normal configured
`fish -c refresh-config` then completed all phases(exit0, REFRESH COMPLETE).
Installed status exits0 and the missing-VT Fish probe exits0 with zero stderr.
Refresh-helper and Fish-startup regressions pass(exit0). No X/preview launched.
README and shared smoke checks clarify hook versus executable-file exclusion.

Suggested commit: `docs: explain refresh permission conflict recovery`.

Final learning review: scan registered incident SHA-256
`69f79a196a4b8c80a4b36ac72a6ab0ca196c8e270163cd9bbadd7048ed1ee2b1`;
finding `local-screensaver-launcher-mode-drift` is verified_workaround/workaround.
Targeted incident check passed(exit0, no errors or uncovered aliases). The real
successful refresh private log is empty. README and smoke documentation match
the observed hook/file distinction. Recovery is complete; repeat-install mode
drift remains an explicit limit. No commit or push performed.

Cursor handoff: Follow this plan; preserve unrelated dirty work. Verify the
exact launcher mode/content, real refresh, installed status and unset-VT Fish
startup; do not force other conflicts or launch X/screensaver previews.

## Session delivery milestone

This plan ships with the Fish fix under
`fix(fish): handle unset virtual terminal during login`. Direct-write evidence
supplies scope after the helper's unsafe/no-parsed-writes result. Source/target
mode verification and real refresh passed; focused tests and README gate pass.
The original recovery required no tracked installer change. Commit only the
recovery's observed documentation/knowledge hunks with its matching plan; leave
all unrelated dirty work untouched. The authorized next step is privacy-gated
commit and one push to origin/main. Reinstall mode drift remains the stated limit.
