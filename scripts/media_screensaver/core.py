"""Display-independent conveyor and live-layout geometry."""
from dataclasses import dataclass
from pathlib import Path
import os
import random
import re

MEDIA_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.heic', '.mp4', '.mov', '.mkv'}
VIDEOS = {'.mp4', '.mov', '.mkv'}
CADENCE = 10.0
SLIDE = 0.75


def discover(root: Path, progress=lambda count: None) -> list[Path]:
    if not root.is_dir():
        raise ValueError('Media mount unavailable; mount the library or use --media DIR.')
    paths = []
    def onerror(error):
        raise ValueError('Media directory unreadable; check mount permissions.') from error
    for directory, _, files in os.walk(root, followlinks=False, onerror=onerror):
        for name in files:
            path = Path(directory) / name
            if path.suffix.lower() in MEDIA_EXTENSIONS and not path.is_symlink():
                paths.append(path.absolute())
        progress(len(paths))
    if not paths:
        raise ValueError('No supported media found; check --media DIR and the mount.')
    return paths


def parse_monitors(output: str) -> list[dict]:
    monitors = []
    for line in output.splitlines()[1:]:
        match = re.match(r'\s*\d+:\s+\S+\s+(\d+)(?:/\d+)?x(\d+)(?:/\d+)?([+-]\d+)([+-]\d+)\s+(\S+)', line)
        if match:
            w, h, x, y, name = match.groups()
            monitors.append(dict(name=name, x=int(x), y=int(y), width=int(w), height=int(h)))
    monitors.sort(key=lambda m: m['x'])
    if len(monitors) != 3:
        raise ValueError('Exactly three enabled X11 monitors are required; inspect xrandr --listmonitors.')
    if any(m['width'] <= 0 or m['height'] <= 0 for m in monitors):
        raise ValueError('Invalid monitor dimensions.')
    if any(a['x'] + a['width'] > b['x'] for a, b in zip(monitors, monitors[1:])):
        raise ValueError('Monitors must be arranged left to right without horizontal overlap.')
    return monitors


def placement(monitors: list[dict], slot: int, progress: float) -> dict:
    def rect(index):
        if index < 0:
            return dict(monitors[0], x=monitors[0]['x'] - monitors[0]['width'])
        if index >= len(monitors):
            return dict(monitors[-1], x=monitors[-1]['x'] + monitors[-1]['width'])
        return monitors[index]
    before, after = rect(slot - 1), rect(slot)
    return {key: round(before[key] + (after[key] - before[key]) * progress)
            for key in ('x', 'y', 'width', 'height')}


@dataclass(eq=False)
class Entry:
    identity: int
    path: Path
    slot: int = 0


class Conveyor:
    def __init__(self, paths: list[Path], start: float):
        self.paths = list(paths)
        self.entries = []
        self.last = None
        self.sequence = 0
        self.next_advance = start + CADENCE
        self.slide_start = start - SLIDE
        for slot in range(3):
            self._enter(slot)
        self.last = self.entries[0].path if self.entries else None

    def _enter(self, slot=0):
        if not self.paths:
            return
        choices = [p for p in self.paths if p != self.last] or self.paths
        self.last = random.choice(choices)
        self.sequence += 1
        self.entries.append(Entry(self.sequence, self.last, slot))

    def progress(self, now: float) -> float:
        return max(0., min(1., (now - self.slide_start) / SLIDE))

    def tick(self, now: float):
        while now >= self.next_advance:
            self.entries = [entry for entry in self.entries if entry.slot < 3]
            for entry in self.entries:
                entry.slot += 1
            self.slide_start = self.next_advance
            self.next_advance += CADENCE
            self._enter()
        if self.progress(now) >= 1:
            self.entries = [entry for entry in self.entries if entry.slot < 3]

    def reject(self, path: Path):
        self.paths = [p for p in self.paths if p != path]
        self.entries = [e for e in self.entries if e.path != path]
