# Discord pronunciation commit needs Git write permission

Commit staging needs an approved Git metadata write. Preserve the candidate and unrelated working changes, then repeat staging with the required permission.

## Symptom and impact

The initial candidate-staging command could not write a Git blob or create `.git/index.lock`: the repository metadata is mounted read-only in the default sandbox. No files were staged and no commit was created. The working pronunciation change and task-status addition remain intact.

## Evidence and status

`git hash-object -w --stdin` exited 128 with “Read-only file system”; `git add` reported the same error for the index lock. This is a Git metadata permission boundary, not a source or test failure. The command wrapper continued with read-only diff commands; their success does not establish successful staging.

## Next steps

Search the reviewed Git permission guidance, retry only the authorized staging/commit operations with elevated permission, inspect the exact candidate, run the privacy gate, and push the verified commit. Keep unrelated dirty hunks out of the index. The approved elevated staging retry exited 0; exact staged review and commit privacy checks follow below.

## Lookup, resolution and verification

Queries `git index.lock Read-only file system` and `sandbox git metadata permission` found lock-publication and sandbox guidance, but no exact metadata-mount remedy. Owned-lock guidance does not apply: no competing lock exists; the environment explicitly marks `.git` read-only. No application-code change is needed.

Repeating the same scoped staging operation with approved elevated permission exited 0. It staged the pronunciation files and only their README/smoke-test hunks. Unrelated working content stayed intact. This resolves staging; the commit and remote push are separate operations. No new reusable learning is required beyond observing declared filesystem permissions and checking each modifying subprocess result.
