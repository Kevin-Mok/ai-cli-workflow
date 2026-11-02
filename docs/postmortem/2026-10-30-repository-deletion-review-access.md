# Repository deletion review access failures

This report records read-only inspection failures during the duplicate-repository deletion assessment and the evidence used to continue safely.

## Symptom and impact

Initial gh-axi repository reads returned “error connecting to api.github.com” in the restricted sandbox. An unrelated private-context lookup used an assumed helper filename that does not exist. A file inventory also named an absent optional .github directory. These failures delayed the assessment; no remote mutation occurred.

## Lookup and applicability

Searched postmortem memory for api.github.com, helper path, network sandbox and missing helper symptoms. Ranked results were not specific to these failures. Reviewed ext-sandbox-loopback: its permission-boundary principle is applicable, while its loopback-specific root cause is not established here.

## Resolution and evidence

Scoped approved gh-axi repository reads succeeded outside the restricted sandbox for both the old private repository and the replacement public repository. This establishes a working access path, not repair of default sandbox networking. File discovery located context_store.py; its topics read succeeded. The absent optional directory needs no repair. A subsequent gh-axi PR-list request rejected --fields number: the wrapper lists number by default but accepts only its documented additional fields. The REST inventory already verified 38 open PRs; use its supported count query for reproducibility.

## Status, limitations and next steps

Access workaround verified. Continue read-only metadata checks; do not delete either repository as part of an advisory request. Future helper calls must use discovered paths. No new reusable finding: existing permission-boundary and path-discovery practices cover these execution mistakes.
