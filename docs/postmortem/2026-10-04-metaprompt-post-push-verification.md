# Metaprompt post-push protected-file verification

- Symptom: after successfully pushing `414b01f` to `origin/main`, an assertion
  comparing five protected source/live files with the pre-refresh hashes failed.
- Impact: the push succeeded. The final preservation check requires attribution
  before claiming those files still match the earlier snapshot. No restoration
  or modification of protected files has been attempted.
- Evidence: `/tmp/metaprompt-commit-refresh-hashes.json`; the post-push command
  exited 1 at its aggregate hash assertion. The commit scope excluded configs
  and aliases, and the index is empty after committing.
- Root cause: the verification reused an 18:38:06 UTC snapshot across the scope
  approval wait. Live Codex config was modified at 18:39:02 and its local source
  at 18:43:19, before the 18:59:37 commit. The exact writer is not established.
  The comparison detects intervening local updates; it does not establish a
  change made by this commit. The tracked config has an existing skip-worktree
  flag, so ordinary status does not display its local divergence.
- Resolution: preserve both matching current config files and the existing
  index flag. Do not restore the older snapshot or include local config in the
  delivery. The Git configs and aliases still match their saved hashes.
- Verification: the source/live Codex files are byte-identical. Config blobs in
  `HEAD` and `HEAD^` are identical, and no protected path appears in the commit.
  All 299 directly attributed staged files were committed. Local `HEAD`,
  `origin/main` and `git ls-remote origin refs/heads/main` all resolve to
  `414b01ff887e7c2b5a264583f714c333ff109acd`; ahead/behind is `0 0`.
- Status: resolved as a stale-baseline verification warning, with no config
  repair required. Record this finding in a documentation-only follow-up.
- Follow-up: refresh preservation baselines immediately before a delivery
  mutation after a user-input pause; separately verify committed scope and
  current local state rather than inferring writer identity from hashes.
