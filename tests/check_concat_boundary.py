#!/usr/bin/env python3
"""Make a short, inspectable stream-copy sample across two source clips."""

import argparse
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import tempfile


CONCAT = Path(__file__).resolve().parents[1] / "scripts" / "executable_concat-timestamped-videos"
VIDEO_SUFFIXES = {".mp4", ".mov", ".m4v"}


def run(*args):
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    for line in result.stderr.splitlines():
        if "non-monotonic" in line.lower() or "non monotonically increasing" in line.lower():
            print(f"  Timestamp warning: {line}", flush=True)
    if result.returncode:
        print(result.stderr, file=sys.stderr)
        raise subprocess.CalledProcessError(result.returncode, args)


def duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def sources_from_list(list_path, directory):
    lines = list_path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "ffconcat version 1.0":
        raise ValueError(f"invalid FFmpeg concat list: {list_path}")
    sources = []
    for line in lines[1:]:
        parts = shlex.split(line)
        if len(parts) != 2 or parts[0] != "file":
            raise ValueError(f"unsupported concat list entry: {line}")
        source = Path(parts[1]).resolve()
        if source.parent != directory or not source.is_file() or source.suffix.lower() not in VIDEO_SUFFIXES:
            raise ValueError(f"concat list source is not a video in {directory}: {source}")
        sources.append(source)
    if len(sources) < 2:
        raise ValueError(f"concat list needs at least two clips: {list_path}")
    return sources


def check_pair(first, second, seconds, output_dir):
    first_duration = duration(first)
    if first_duration <= seconds or duration(second) <= seconds:
        raise ValueError(f"each source must be longer than {seconds} seconds: {first.name}, {second.name}")
    clips = output_dir / "clips"
    clips.mkdir()
    first_sample = clips / "0001.mp4"
    second_sample = clips / "0002.mp4"
    joined = output_dir / "joined.mp4"
    sheet = output_dir / "boundary.png"
    run("ffmpeg", "-v", "error", "-ss", str(first_duration - seconds),
        "-i", str(first), "-t", str(seconds), "-map", "0:v:0", "-map", "0:a:0?",
        "-c", "copy", "-avoid_negative_ts", "make_zero", str(first_sample))
    run("ffmpeg", "-v", "error", "-i", str(second), "-t", str(seconds),
        "-map", "0:v:0", "-map", "0:a:0?", "-c", "copy", str(second_sample))
    run(sys.executable, str(CONCAT), str(clips), str(joined))
    run("ffmpeg", "-v", "error", "-xerror", "-i", str(joined), "-f", "null", "-")

    boundary = duration(first_sample)
    run("ffmpeg", "-v", "error", "-ss", str(max(0.0, boundary - 1.5)),
        "-i", str(joined), "-t", "3", "-vf",
        "fps=2,scale=640:360,tile=3x2", "-frames:v", "1", str(sheet))
    print(f"{first.name} -> {second.name}: join at about {boundary:.2f} seconds", flush=True)
    print(f"  Joined sample: {joined}", flush=True)
    print(f"  Boundary contact sheet: {sheet}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", nargs="?", type=Path, help="clip whose end will be sampled")
    parser.add_argument("second", nargs="?", type=Path, help="clip whose start will be sampled")
    parser.add_argument("--directory", type=Path, help="check every adjacent top-level video pair in filename order")
    parser.add_argument("--concat-list", type=Path, help="use this FFmpeg concat list for --directory source selection")
    parser.add_argument("--seconds", type=float, default=4.0, help="seconds to take from each clip (default: 4)")
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error("--seconds must be positive")
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            parser.error(f"{tool} is required")
    if args.directory:
        if args.first or args.second:
            parser.error("use --directory or two positional clips")
        if not args.directory.is_dir():
            parser.error(f"directory is unavailable: {args.directory}")
        directory = args.directory.resolve()
        lists = sorted(directory.glob("*.ffconcat.txt"))
        if args.concat_list:
            selected_list = args.concat_list.resolve()
        elif directory / f"{directory.name}.ffconcat.txt" in lists:
            selected_list = directory / f"{directory.name}.ffconcat.txt"
        elif len(lists) == 1:
            selected_list = lists[0]
        elif len(lists) > 1:
            parser.error("multiple concat lists found; specify --concat-list")
        else:
            selected_list = None
        if selected_list:
            if not selected_list.is_file():
                parser.error(f"concat list is unavailable: {selected_list}")
            sources = sources_from_list(selected_list, directory)
            print(f"Using concat list: {selected_list}", flush=True)
        else:
            sources = sorted(
                (path.resolve() for path in directory.iterdir()
                 if path.is_file() and not path.is_symlink() and path.suffix.lower() in VIDEO_SUFFIXES),
                key=lambda path: path.name,
            )
        if len(sources) < 2:
            parser.error("directory needs at least two top-level video clips")
        pairs = list(zip(sources, sources[1:]))
    else:
        if args.concat_list:
            parser.error("--concat-list requires --directory")
        if not args.first or not args.second:
            parser.error("provide two clips or --directory")
        for source in (args.first, args.second):
            if not source.is_file():
                parser.error(f"source file is unavailable: {source}")
        pairs = [(args.first.resolve(), args.second.resolve())]

    output_dir = Path(tempfile.mkdtemp(prefix="concat-boundary-"))
    print(f"Sample directory: {output_dir}", flush=True)
    for index, (first, second) in enumerate(pairs, start=1):
        pair_dir = output_dir / f"pair-{index:02d}" if args.directory else output_dir
        pair_dir.mkdir(exist_ok=True)
        check_pair(first, second, args.seconds, pair_dir)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"concat boundary check failed: {exc}", file=sys.stderr)
        sys.exit(1)
