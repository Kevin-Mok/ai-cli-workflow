# Delivery helper path discovery

The delivery review encountered two nonexistent helper paths. Use the paths
listed in the active skill catalog and repository documentation before reads.

## Symptom, impact and evidence

- A combined read returned exit 1 because the guessed installed Ponytail skill
  path did not exist; the other requested files were read successfully.
- A later optional read of `scripts/executable_refresh-config` reported a missing
  file. Refresh is a Fish function, as the README already documents.
- Neither failed read modified files or prevented review of the dirty worktree.
- A configured Fish inspection returned exit 0 but emitted startup write errors
  for fnm multishells, universal variables and generated aliases under the
  read-only sandbox. Its printed function is valid evidence; exit 0 does not
  establish successful shell startup or configuration activation.

## Lookup and resolution

- Query: `skill path missing file installed catalog`.
- Applicable finding: `local-discover-paths-before-reads` in the tracked
  postmortem-memory paths/ownership reference. Its remedy explicitly identifies
  refresh as a Fish function and requires observed paths before reads.
- Read the Ponytail skill successfully from the active plugin catalog path.
  Use `dot_config/fish/functions/refresh-config.fish` for refresh inspection.
- Status: resolved read-path discovery; configuration activation is tracked
  separately in the delivery plan.
- Next: run the required refresh through normal scoped filesystem approval,
  inspect its actual result and preserve any source/live conflicts.
- Approved `fish -c 'refresh-config'` reached the helper and returned exit 1
  during chezmoi apply. It explicitly reported that no files were adopted;
  shortcuts were not regenerated. Preserve local differences and report
  activation as incomplete rather than forcing deployment.
- The private log identifies `.config/mimeapps.list` as changed since chezmoi
  last wrote it; noninteractive input ended with EOF. This pre-existing
  unrelated local conflict is outside delivery scope and was left intact.
- The first Git staging attempt could not create `.git/index.lock` because
  repository metadata is read-only in the sandbox. No files were staged.
  Use normal scoped approval for authorized Git index/commit writes.
- Lookup for Fish read-only startup returned `ext-sandbox-loopback`: its
  approved scoped-command route applies to the filesystem boundary, while
  its networking diagnosis does not. Refresh-conflict lookup returned
  `local-screensaver-launcher-mode-drift`; its no-forced-overwrite limit
  applies, but no launcher-mode diagnosis is asserted for mimeapps.
- The first documentation candidate failed the mandatory staged privacy gate
  (exit 1, one email-category finding). The conditional commit did not run.
  Locate the exact candidate boundary and repair only task-owned content;
  preserve scanner policy and active hooks.
- A follow-up search guessed a package layout for the privacy scanner and
  returned missing-file errors. The implementation must be located from the
  file inventory instead; this repeats the same path-discovery failure class.
- Read-only diagnosis mapped privacy location `e350269cdd8e` to this task's
  delivery plan. Its literal GitHub SSH address matched the blob-email
  heuristic. Replace the address with the public repository name; no scanner,
  policy, hook or pre-existing document change is required for this finding.
- Learning: no new reusable finding; the existing path-discovery guidance
  directly covers both mistakes. Register this report's reviewed hash and run
  its targeted coverage check before committing.

- A delivery-plan patch failed its context check because the expected sentence
  was only part of an existing line. No partial edit occurred. An exact string
  update against the current plan preserved the preceding milestone; this is
  covered by existing patch-operation contract guidance.
- Resolution evidence: the repaired documentation candidate passed both the
  explicit privacy gate and active commit hook; commit `349b65d` contains exactly
  the ten reviewed paths. Configuration activation remains blocked solely by
  the preserved mimeapps conflict.
