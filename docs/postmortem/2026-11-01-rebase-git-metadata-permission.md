# Rebase fetch blocked by Git metadata permissions

The requested rebase needs writable Git metadata. Use scoped approved Git access while preserving the existing dirty working tree.

- Symptom: `git fetch origin main` exited 255: cannot open `.git/FETCH_HEAD`: Read-only file system.
- Impact: Initial fetch did not run; no branch or working-tree changes occurred.
- Lookup: searched `FETCH_HEAD read-only`; no exact matching finding. Existing `ext-sandbox-loopback` guidance distinguishes environment restrictions from application defects, but its loopback symptom does not match this metadata mount restriction.
- Evidence: sandbox permits repository content writes but mounts `.git` read-only. Scoped approved fetch exited 0 and advanced origin/main from 8662fa3 to 978696a.
- Root cause: execution permissions, not a Git repository defect.
- Resolution: approved scoped Git metadata writes; original sandbox restriction remains.
- Status: fetch workaround verified; branch advanced to 978696a. Autostash restoration conflicted only in dot_codex/AGENTS.md. Preserved upstream conditional routing and the local PR-review addition; the pre-existing repository-origin rule remains in upstream delivery.md.
- Verification: all 19 original tracked edits preserved (exact bytes where upstream was unchanged; local additions retained where upstream changed), index empty, no unmerged paths, HEAD equals origin/main at 978696a. Original untracked paths remain present. Autostash be9a6ff remains as recovery evidence. No push or new commit.
- Learning: no new general remedy beyond the known scoped-permission workflow; do not equate a successful rebase with successful autostash restoration. The latter was separately resolved and verified.
