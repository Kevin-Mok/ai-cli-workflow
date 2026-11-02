# Impeccable trim left native links

The retained-link check caught incomplete routing cleanup while importing the
pinned web skill. Review every retained Markdown link after removing platform
files, then verify the complete retained surface before delivery.

- Date: 2026-10-22.
- Symptom: The first implementation check reported 9 passed and 1 failed:
  `reference/audit.md` still linked to the omitted native audit reference.
- Impact: Verification blocked delivery; no configuration or live installation
  was changed.
- Evidence: `python -m pytest tests/test_design_skills_sync.py -q`; the retained
  link test failed on `audit.native.md`. A complete link scan also found the
  native reviewer links in `reference/new-work.md`.
- Lookup: Searched reviewed incident knowledge for
  `skill import removed reference dangling link`. Broad matches did not supply a
  direct routing remedy; current executable evidence establishes the incomplete
  cleanup. `local-discover-paths-before-reads` applies to a secondary read-only
  lookup that guessed a missing linker script path. Inventory found the actual
  `run_after_install-claude-skills.sh.tmpl`; no file was changed by that lookup.
- Root cause: The initial edit covered platform links in command routing and
  six playbooks, but missed a second audit route and the finish-review packet.
- Resolution: Removed only those native routes and changed the retained-link
  check to report all missing targets together. The source record now lists
  every edited playbook, preserving the original upstream inventory.
- Verification: `python -m pytest tests/test_design_skills_sync.py -q` passed all
  10 tests, including retained hashes, every remaining Markdown target, fixture
  engine handoff and Higgsfield-only refresh. Shell syntax and diff checks also
  passed. No downloaded engine or live installation was exercised.
- Current status: Code verified; activation intentionally not performed.
- Follow-up: Inventory file paths before reading and validate all retained links
  after trimming dependencies. These reinforce existing controls; no new
  standing instruction is justified by this isolated caught omission.
- Learning update: The canonical ledger
  `/home/example/linux-config/dot_agents/skills/postmortem-memory/sources.json`
  is outside this task's writable roots. Registering this report's reviewed hash
  and alias with the no-new-learning decision remains outstanding. No installed
  memory copy was edited. The canonical helper's targeted check exited 1 with
  exactly one new, unregistered report and no ledger contract errors.
