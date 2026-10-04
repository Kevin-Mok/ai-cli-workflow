# Second Brain Beginner Guide

Use Second Brain to keep enough context to continue a work session later.
Check your current notes, capture useful discoveries privately, confirm one
focus, then save a reviewed closeout and run the health check.

## What this is (in 30 seconds)

Second Brain is a Markdown vault with two layers:

- `second-brain/` is tracked and reviewable in Git (context you want the agents and repo work to retain).
- Raw, unstructured session text lives outside Git in private state and is not copied into the tracked vault unless you confirm a clean, safe write.

The result is that you can capture raw thoughts quickly, while only keeping
cleaned and approved context in tracked notes.

## Start here first

1) Check where you are

```bash
second-brain status --format text
```

Read the short list and note:

- current projects
- inbox count
- latest daily note
- last known checkpoint state

2) Capture private notes while you work

```bash
second-brain capture --kind raw-session --payload -
```

Paste your note on stdin and finish with Ctrl-D. This stays private and local.

3) Set a focus for the day/session

```bash
second-brain focus --payload -
```

This confirms what you want to work on. Agents should reuse this focus instead of
guessing context.

4) Close out when done

```bash
second-brain closeout --payload -
```

This turns your session into a public-safe closeout record after confirmation.

5) Verify structure and privacy checks

```bash
second-brain doctor --format json --check
```

If it passes, you are in a healthy state. If it fails, fix the reported issue first.

## Minimal daily routine

1. Run `second-brain status --format text`.
2. Capture important thoughts with `capture`.
3. Keep one concise focus with `focus`.
4. At the end of the day, run `closeout`.
5. Run `doctor --format json --check` if anything feels off.

## Folder map for beginners

Everything below is already wired and Obsidian-friendly:

- `second-brain/00 Context/`: identity, memory map, durable preferences, decision notes.
- `second-brain/01 Inbox/`: quick dumps and temporary items.
- `second-brain/02 Projects/`: active repositories, work packages, and teaching projects.
- `second-brain/03 Areas/`: ongoing disciplines (work, AI workflow, teaching, wellbeing, relationships).
- `second-brain/04 Resources/`: reusable references and templates.
- `second-brain/05 Daily Notes/`: dated work notes.
- `second-brain/06 Archive/`: long-lived references.
- `second-brain/07 Attachments/`: attachment index and media pointers.

Use the vault as a map, not as a dumping ground.

## Common mistakes (what to avoid)

- Putting credentials, raw journaling, or sensitive private details in tracked files.
- Editing tracked files by hand without using the approved session flow.
- Ignoring doctor failures and continuing changes.
- Trying to invent multiple focuses in one day; keep one confirmed focus at a time.

## Where to go next

- Quick front door: [`second-brain/README.md`](../second-brain/README.md)
- Full operator details: [`docs/second-brain.md`](second-brain.md)
