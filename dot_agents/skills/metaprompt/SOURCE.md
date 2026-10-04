# Source

Use this guide to update the Sentry-based `$metaprompt` skill and recover the
previous installation if needed. Check the pinned source, stage and review
a candidate, back up the existing installation, then follow the checks and
refresh steps before using the updated skill.

- Upstream repository: [getsentry/skills](https://github.com/getsentry/skills).
- Pinned revision: `d18b7aa8ba878354e5c348310230e652f7690f9c`.
- Native path: `skills/prompt-optimizer`.
- Imported on: `2026-10-04`, from the locally verified benchmark snapshot.
- Selection evidence: [completed comparison](../../../docs/metaprompt-selection.md).
  Sentry achieved 14/16 end-to-end successes; raw/minimal reached 15/16. The
  recorded limitations and costs remain applicable; no new efficacy claim is
  implied by this installation.
- License: complete [Apache-2.0 license](LICENSE.txt) from the pinned repository.
- Integrity inventory: [UPSTREAM.json](UPSTREAM.json) records source paths and
  SHA-256 digests for all eight native files.

The native `SKILL.md` is retained byte-for-byte as [UPSTREAM.md](UPSTREAM.md).
Its four references, [SOURCES.md](SOURCES.md), and [SPEC.md](SPEC.md) are unchanged.
The native package supplies no scripts, assets, or UI metadata. `SOURCES.md`
cites files in Sentry's own repository as provenance; those foreign paths do
not become local runtime dependencies or override this repository's rules.

The local [SKILL.md](SKILL.md) exposes `$metaprompt`, preserves Sentry's eight
output sections, uses canonical template variables, and saves only the
Optimized Prompt under the active workspace's `prompts/` with collision-safe
filenames. Embedded production-task execution still needs a separate user
request. Prepared evals and actual executed comparisons must be distinguished.
Local UI metadata, this provenance document, the manifest, and the reviewed
update helper are outside the native content inventory.

This replaces the previous Majkey adaptation. Its references, helper scripts,
asset and upstream UI metadata are retired from the active package; the local
update helper is retained and now targets Sentry. `$metaprompt-alxve` remains
unchanged. The outgoing source and installed packages are backed up at
`/tmp/metaprompt-sentry-migration-mp4gysfi`; this machine-local rollback copy is
not a durable archive and should be retained separately if long-term recovery
of the uncommitted Majkey adaptation is needed.

## Reviewed updates

From the repository root (Python 3.10+, network access, no sudo):

```bash
python3 dot_agents/skills/metaprompt/scripts/update_upstream.py --check
python3 dot_agents/skills/metaprompt/scripts/update_upstream.py --stage /tmp/metaprompt-sentry-candidate
```

To reproduce this exact upstream import in a new review directory:

```bash
python3 dot_agents/skills/metaprompt/scripts/update_upstream.py --stage /tmp/metaprompt-sentry-pinned --revision d18b7aa8ba878354e5c348310230e652f7690f9c
```

`--check` compares the pinned revision with the latest skill-path commit; exit 0
means the check succeeded, including when an update is available. `--stage`
downloads regular files at an immutable revision, remaps the native entrypoint
and license, and records hashes. It refuses existing destinations, unsafe paths,
symlinks and incomplete tree responses. It does not replace installed skills.
A failed write may leave a partial candidate; inspect it and retry in a fresh
path. A newer path commit alone does not establish substantive maintenance.

Review the staged native files and license, relevant commit diffs, runtime
requirements and output contract. Preserve the local alias, artifact-saving
contract, metadata and updater. Update the pin, inventory, provenance and
integration test together. Back up outgoing source and installed bytes before
removing obsolete imported files; remove only attributed files still matching
that backup, preserving unknown or modified live children. Chezmoi apply alone
can retain old files after they disappear from the source tree.

Run the [guide's checks and refresh procedure](../../../docs/metaprompt-skills.md).
Verify installed files against source, including the absence of retired paths.
Start a fresh agent session to reload the skill catalog. File synchronization
does not prove an already-running picker refreshed its description.

## Rollback

For the original compiler, use the separately preserved `$metaprompt-alxve`.
For this Sentry replacement, restore the backed-up outgoing source package and
its matching updater/manifest, then apply that skill through the reviewed
refresh procedure and verify it against the backup. Preserve unrelated source
and live configuration. Do not pass a Majkey revision to the Sentry updater:
its repository and path now explicitly target Sentry. The previous adaptation
and its historical observations are distinct from the original alxve compiler.
