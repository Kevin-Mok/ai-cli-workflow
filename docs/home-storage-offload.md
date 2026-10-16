# Offload cold home folders

This helper previews moving four cold folders to a mounted storage destination, verifies each copy, replaces the original with a symlink, and clears rebuildable caches. Mount the destination, close applications using the folders, preview, then explicitly apply. Run as your normal account without sudo.

From the repository root, preview with `./scripts/executable_home-storage-offload --destination /mnt/storage`. `/mnt/storage` is an example: supply your actual writable mount on a different filesystem. Add `--apply` to execute, `--plain` for ASCII output, or `--details` for underlying diagnostics. Python 3, rsync, GNU du, GNU rm, and GNU sync are required.

## Scope and checks

The fixed move list is `~/Videos`, `~/Downloads`, `~/root-backup`, and `~/Android`. Each folder keeps its basename directly beneath the destination. Other folders, including Ollama data, stay local. The destination must have enough free space for apparent source sizes plus 1 GiB. Existing destinations, retained originals, unexpected links, and unmounted destinations are refused.

After successful moves, available npm, pip, uv, and Go cache cleaners run. Missing tools are skipped; cleaner failures produce a nonzero exit. Cache cleanup cannot be undone.

## Safety and recovery

Close all writers before applying. Copying preserves archive metadata, hardlinks, ACLs, and extended attributes. A checksum comparison checks copied bytes and extra files, then the copy is flushed before the original is renamed and replaced by a link. Destination identity is checked before original removal. Progress appears every five seconds during child commands.

This is relocation, not a backup. Keep the destination mounted whenever applications need the relocated folders. Concurrent writes and physical disconnection can still cause problems.

An interrupted copy leaves the source and partial destination. An interrupted link switch or original removal can leave `<folder>.offload-original`; retain it until you identify the complete copy. The helper refuses to guess which copy is authoritative. Successful reruns skip correct links and missing source folders.

To restore local storage, ensure enough local free space, close writers, copy and verify the destination folder into a separate local directory, then replace the home symlink with that verified directory. Retain the destination copy until applications work.

## Verification

Run `python3 -B tests/test_home_storage_offload.py` for disposable regressions using real rsync. Tests cover explicit destination selection, preview, copied data and links, reruns, collision refusal, missing mounts, unexpected links, corruption refusal, and keeping Ollama local. A real apply remains an explicit operator action.
