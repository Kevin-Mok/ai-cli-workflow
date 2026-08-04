# Dated iPad Media Transfer Design

## Purpose

Provide a reusable command that copies original iPad videos captured on one
ISO calendar date into a flat destination folder.

## Interface

```text
rsync-media-date YYYY-MM-DD SOURCE DESTINATION
```

Example:

```text
rsync-media-date 2026-07-28 /mnt/ipad /mnt/linux-files-3/concerts/jcole
```

## Behavior

- Search only `SOURCE/DCIM` for `MOV`, `MP4`, and `M4V` files whose filesystem
  modification time falls on the requested local calendar date.
- Create `DESTINATION` when it does not exist.
- Copy selected files directly into `DESTINATION`, with no source folder
  hierarchy.
- Invoke `rsync` with archive mode, visible transfer progress, and overwrite
  behavior. Re-running the command can resume incomplete transfers and updates
  same-named destination files from the source.
- Reject malformed ISO dates, missing/unreadable source media folders, and
  nonexistent `rsync` with actionable errors.

## Non-goals

- No dry-run gate, interactive confirmation, deletion, or source mutation.
- No import of Photos metadata, thumbnails, or `PhotoData` caches.
- No filename renaming or collision avoidance beyond rsync overwriting the
  same destination name as requested.

## Tests and verification

- A shell test will construct a temporary `DCIM` fixture and stub `rsync` to
  assert that only requested-date media files are selected, flat target paths
  are used, and overwrite-capable flags are supplied.
- A separate case will assert malformed dates fail before `rsync` runs.
- Manual verification will run against `/mnt/ipad` using `2026-07-28` and the
  J. Cole destination, first checking the reported selection and then the
  resulting flat files.

## Risks and rollback

The HDD currently has roughly 49.5 GiB available while the July 28 originals
total about 45.7 GiB, leaving little headroom. The command overwrites matching
destination names; rollback is removal of the newly copied destination files,
not automatic restoration of replaced files.
