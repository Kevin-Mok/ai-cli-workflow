#!/usr/bin/env python3
"""Demonstrate handoff preflight without launching an agent or touching live state."""

from pathlib import Path
import subprocess
import sys
import tempfile

from handoff import HandoffParser


def main():
    plain = "--plain" in sys.argv
    parser = HandoffParser(
        description=("" if plain else "🧪 ") + "Disposable Grok handoff workflow demo (no sudo)")
    parser.add_argument("--plain", action="store_true", help="ASCII output")
    args = parser.parse_args()
    helper = Path(__file__).with_name("handoff.py")

    def report(label):
        print(("" if args.plain else "✅ ") + label, flush=True)

    with tempfile.TemporaryDirectory(prefix="grok-handoff-") as directory:
        repo = Path(directory) / "checkout with spaces"
        subprocess.run(["git", "init", "-q", "-b", "demo", str(repo)], check=True)

        def check(task, branch, expected):
            result = subprocess.run(
                [sys.executable, str(helper), "--plain", "preflight", "--repo", str(repo),
                 "--branch", branch, "--task", task], capture_output=True, text=True)
            if result.returncode != expected:
                raise RuntimeError(f"Expected exit {expected}, observed {result.returncode}")

        check("example", "demo", 0)
        report("Clear checkout: exit 0 (state check only)")
        task_marker = repo / ".harness/example/STOP"
        task_marker.parent.mkdir(parents=True)
        task_marker.touch()
        check("example", "demo", 3)
        check("other", "demo", 0)
        report("Task STOP: example exit 3; other task exit 0")
        (repo / ".harness/STOP").touch()
        check("other", "demo", 3)
        report("Project STOP: other task exit 3")
        check("example", "wrong", 2)
        report("Wrong branch: exit 2")
    report("Disposable workflow complete; no live jobs launched or checkout changed")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError, RuntimeError):
        print(("" if "--plain" in sys.argv else "⚠️ ") +
              "Smoke blocked: verify Python, Git and temporary-directory access", file=sys.stderr)
        sys.exit(2)
