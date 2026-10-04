# Source

- Upstream repo: [Majkey25/prompt-engineering-skill](https://github.com/Majkey25/prompt-engineering-skill)
- Upstream commit: `5c00259223196bd779c97d3234ef34a9a7119634`
- Original source path: `prompt-engineering/SKILL.md`
- Imported on: `2026-10-03`
- Import basis: the complete MIT-licensed `prompt-engineering/` package and
  repository license at the pinned revision.
- Local adaptation: the original entrypoint is retained unchanged as
  [UPSTREAM.md](UPSTREAM.md), and original UI metadata as
  [UPSTREAM.openai.yaml](UPSTREAM.openai.yaml). The local [SKILL.md](SKILL.md)
  exposes `metaprompt`, saves prompt artifacts, disables automatic task
  execution, and documents safe use of the upstream helpers. Local UI metadata
  uses `$metaprompt`. References, scripts, asset, and license are unchanged.
- License: [MIT notice](LICENSE.txt), retained in full.
- Integrity inventory: [UPSTREAM.json](UPSTREAM.json) maps each imported file to
  its source path and SHA-256 digest. Local adapter, metadata, provenance, and
  update helper are outside that inventory.

## Reviewable updates

From the repository root, check skill-specific upstream activity without
changing files (Python 3.10+ and network access; no sudo):

```bash
python3 dot_agents/skills/metaprompt/scripts/update_upstream.py --check
```

Stage the newest skill revision in a **new** directory:

```bash
python3 dot_agents/skills/metaprompt/scripts/update_upstream.py --stage /tmp/metaprompt-candidate
```

To reproduce this exact import:

```bash
python3 dot_agents/skills/metaprompt/scripts/update_upstream.py --stage /tmp/metaprompt-pinned --revision 5c00259223196bd779c97d3234ef34a9a7119634
```

`--check` reports pinned and latest skill commit IDs; exit 0 means the check
succeeded, including when an update exists. `--stage` downloads only regular
files at an immutable commit, remaps the two entrypoints, and writes hashes.
It refuses an existing destination and never changes tracked or installed
skills. A failed stage can leave a partial review directory; inspect it and
choose a fresh directory on retry.

Have the coding agent review the staged candidate against `UPSTREAM.json`,
including license, scripts, invocation boundaries, removed paths, references,
and relevant commit diffs. Apply only reviewed imported files, update the pin,
manifest, provenance, and pin assertion in the integration test together;
preserve the local adapter and update helper. Remove obsolete imported files
only after checking their callers. Run the checks and refresh procedure in
[the skill guide](../../../docs/metaprompt-skills.md). No automatic updates or
future maintenance guarantees are implied.

## Known limitations

The upstream eval generator overwrites file output; prefer `--out -`. Its
manifest and linter support evaluation preparation, not proof of improved
model performance. The included source/video audits are upstream claims;
local import verification does not certify every historical claim.
