"""Index/tree privacy checks and reversible pre-commit installation."""
from __future__ import annotations

import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import threading
import time
import fnmatch

HERE = Path(__file__).resolve().parent
BACKUP = "pre-commit.privacy-gate-previous"
BUNDLE = "privacy-gate.d"
BUNDLE_FILES = ("executable_privacy-gate", "privacy_gate.py", "executable_audit-public-history", "privacy_gate_approvals.json")
# Keep executable scanner entry point and history CLI on the same implementation.
loader = importlib.machinery.SourceFileLoader("public_history_scanner", str(HERE / "executable_audit-public-history"))
spec = importlib.util.spec_from_loader(loader.name, loader)
scanner = importlib.util.module_from_spec(spec)
loader.exec_module(scanner)


class GateError(RuntimeError):
    pass


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        prefix = "" if "--plain" in sys.argv else "🔒 "
        print(prefix + "Privacy gate ERROR: invalid arguments; use --help locally.", file=sys.stderr)
        raise SystemExit(2)


def git(repo: Path, *args: str, optional: bool = False) -> bytes:
    result = subprocess.run(["git", "--no-replace-objects", "--no-optional-locks", *args], cwd=repo, capture_output=True)
    if result.returncode and not (optional and result.returncode == 1):
        raise GateError("Git candidate inspection failed")
    return result.stdout


def reference(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()[:12]


def private_path(path: str) -> bool:
    parts = PurePosixPath(path).parts
    lower = [part.lower() for part in parts]
    name = lower[-1]
    if path == "second-brain/README.md":
        return False
    return (
        any(part in {"recovery", "recoveries", "backup", "backups", "private", ".aws", "dot_ssh", ".ssh", "private_dot_gnupg", "dot_minikube"} for part in lower)
        or path.startswith(("benchmarks/metaprompt/runs/", "benchmarks/metaprompt-selection/runs/", "second-brain/", "dot_kube/private_config"))
        or name in {"auth.json", "credentials.json", "cookies.txt", "cookies.sqlite", "session.json", "session.jsonl", ".chezmoi.toml", ".chezmoidata.toml", ".chezmoidata.yaml"}
        or (name == ".env" or name.startswith(".env.")) and name != ".env.example"
        or name.endswith((".key", ".pem", ".p12", ".pfx", ".local"))
        or ".local." in name
    )


def rules_for(repo: Path, explicit: Path | None):
    configured = git(repo, "config", "--path", "--get", "privacyGate.rules", optional=True).rstrip(b"\n")
    path = explicit or (Path(os.fsdecode(configured)) if configured else None)
    if path is not None:
        path = path.expanduser()
        if not path.is_absolute():
            path = repo / path
        # Local private policy must never be a public candidate itself.
        resolved = path.resolve()
        if resolved.is_relative_to(repo.resolve()):
            raise GateError("Private rules must live outside the repository")
    rules = scanner.load_rules(path)
    identities = []
    if path:
        payload = json.loads(path.read_text())
        identities = payload.get("approved_public_identities", [])
        if not isinstance(identities, list) or any(
            not isinstance(item, dict) or set(item) != {"name", "email"}
            or not all(isinstance(v, str) and v and "\n" not in v for v in item.values())
            for item in identities
        ):
            raise GateError("Invalid public identity policy")
    return rules, identities


def load_approvals():
    payload = json.loads((HERE / "privacy_gate_approvals.json").read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"schema_version", "entries"} or payload["schema_version"] != 1 or not isinstance(payload["entries"], list):
        raise GateError("Invalid reviewed-content policy")
    approvals = {}
    for entry in payload["entries"]:
        if (not isinstance(entry, dict) or set(entry) != {"path_ref", "content_sha256", "categories", "reason"}
            or not isinstance(entry["path_ref"], str) or not re.fullmatch(r"[0-9a-f]{12}", entry["path_ref"])
            or not isinstance(entry["content_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", entry["content_sha256"])
            or not isinstance(entry["reason"], str) or not entry["reason"].strip()
            or not isinstance(entry["categories"], list) or not entry["categories"]
            or any(category not in {"credential", "provider_token", "sensitive_path", "email", "ip_address"} for category in entry["categories"])):
            raise GateError("Invalid reviewed-content policy entry")
        key = (entry["path_ref"], entry["content_sha256"])
        if key in approvals:
            raise GateError("Duplicate reviewed-content policy entry")
        approvals[key] = frozenset(entry["categories"])
    return approvals


def candidate(repo: Path, tree: str | None):
    if tree:
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", tree):
            raise GateError("Invalid candidate tree")
        raw = git(repo, "ls-tree", "-r", "-z", "--full-tree", tree)
    else:
        raw = git(repo, "ls-files", "--stage", "--full-name", "-z")
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, oid, stage = metadata.split() if not tree else (metadata.split()[0], metadata.split()[2], b"0")
        if stage != b"0":
            raise GateError("Unresolved index conflicts; resolve them before committing")
        if mode not in {b"100644", b"100755", b"120000"}:
            raise GateError("Unsupported candidate mode; submodules need separate review")
        entries.append((oid.decode("ascii"), path))
    return entries


def lfs_payload(repo: Path, content: bytes) -> bytes:
    if not content.startswith(b"version https://git-lfs.github.com/spec/"):
        return content
    match = re.fullmatch(rb"version https://git-lfs.github.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize ([0-9]+)\n", content)
    if not match:
        raise GateError("Invalid LFS pointer; repair it locally")
    oid = match[1].decode("ascii")
    output = git(repo, "lfs", "env")
    locations = [line.split(b"=", 1)[1] for line in output.splitlines() if line.startswith(b"LocalMediaDir=")]
    if len(locations) != 1:
        raise GateError("Local LFS storage is unavailable")
    payload = (Path(os.fsdecode(locations[0])) / oid[:2] / oid[2:4] / oid).read_bytes()
    if len(payload) != int(match[2]) or hashlib.sha256(payload).hexdigest() != oid:
        raise GateError("Local LFS payload verification failed")
    return payload


def literal_categories(content: bytes, location: str, rules):
    return {
        category for value, category, ignore_case, locations in rules
        if location in locations and (
            value.lower() in content.lower() if ignore_case else value in content
        )
    }


def check(repo: Path, *, tree: str | None = None, rules_path: Path | None = None):
    repo = Path(os.fsdecode(git(repo, "rev-parse", "--show-toplevel").rstrip(b"\n")))
    rules, _ = rules_for(repo, rules_path)
    findings = []
    approvals = load_approvals()
    for oid, encoded_path in candidate(repo, tree):
        path = os.fsdecode(encoded_path)
        categories = scanner.scan_content(encoded_path, "blob")
        if private_path(path):
            categories.add("sensitive_path")
        # git cat-file reads index object IDs, never worktree bytes or patch lines.
        content = git(repo, "cat-file", "blob", oid)
        categories.update(scanner.scan_content(content, "blob"))
        approved = approvals.get((reference(encoded_path), hashlib.sha256(content).hexdigest()), ())
        categories.difference_update(approved)
        categories.discard("home_path")
        # Explicit private prohibitions always override public metadata defaults.
        categories.update(literal_categories(encoded_path, "blob", rules["literals"]))
        categories.update(literal_categories(content, "blob", rules["literals"]))
        if any(fnmatch.fnmatchcase(path, pattern) for pattern in rules["path_globs"]):
            categories.add("sensitive_path")
        payload = lfs_payload(repo, content)
        if payload is not content:
            categories.update(scanner.scan_content(payload, "blob") - {"home_path"})
            categories.update(literal_categories(payload, "blob", rules["literals"]))
        findings.extend((category, reference(encoded_path)) for category in sorted(categories))
    for kind in ("AUTHOR", "COMMITTER"):
        ident = git(repo, "var", "GIT_" + kind + "_IDENT").strip()
        match = re.fullmatch(rb"(.*?) <([^<>\n]+)> [0-9]+ [+-][0-9]{4}", ident)
        if not match:
            raise GateError("Git identity is unavailable")
        name, email = match.group(1, 2)
        identity = name + b" <" + email + b">"
        categories = scanner.scan_content(identity, "commit") - {"email", "home_path"}
        categories.update(literal_categories(identity, "commit", rules["literals"]))
        findings.extend((category, "identity-" + kind.lower()) for category in sorted(categories))
    return findings


def hook_bytes() -> bytes:
    return b'''#!/bin/sh
# public-privacy-gate v1
hookdir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 2
# Scan again after a preserved hook in case it modifies the index.
python3 "$hookdir/privacy-gate.d/executable_privacy-gate" check || exit $?
if [ -x "$hookdir/pre-commit.privacy-gate-previous" ]; then
    "$hookdir/pre-commit.privacy-gate-previous" "$@" || exit $?
    python3 "$hookdir/privacy-gate.d/executable_privacy-gate" check || exit $?
fi
'''


def hook_directory(repo: Path) -> Path:
    raw = git(repo, "rev-parse", "--path-format=absolute", "--git-path", "hooks").rstrip(b"\n")
    return Path(os.fsdecode(raw))


def owned(hook: Path) -> bool:
    return hook.is_file() and not hook.is_symlink() and hook.read_bytes() == hook_bytes()


def install(repo: Path):
    directory = hook_directory(repo)
    directory.mkdir(parents=True, exist_ok=True)
    hook = directory / "pre-commit"
    backup = directory / BACKUP
    bundle = directory / BUNDLE
    active = owned(hook)
    if hook.exists() or hook.is_symlink():
        if not active:
            if backup.exists() or backup.is_symlink() or bundle.exists():
                raise GateError("Existing installation changed; preserve it and review locally")
            if not hook.is_file() or hook.is_symlink():
                raise GateError("Existing hook needs manual preservation")
    elif backup.exists() or bundle.exists():
        raise GateError("Incomplete installation; review locally")
    # Prepare scanner before touching the active hook. Keep original permissions.
    if not active:
        bundle.mkdir(mode=0o700)
    for name in BUNDLE_FILES:
        source = HERE / name
        target = bundle / name
        if source.resolve() != target.resolve():
            temporary = target.with_suffix(target.suffix + ".new")
            shutil.copyfile(source, temporary)
            temporary.chmod(0o700)
            temporary.replace(target)
    if not active:
        if hook.exists():
            hook.rename(backup)
        with hook.open("xb") as stream:
            stream.write(hook_bytes())
        hook.chmod(0o700)


def uninstall(repo: Path):
    directory = hook_directory(repo)
    hook = directory / "pre-commit"
    if not owned(hook):
        raise GateError("Hook is absent or changed; nothing removed")
    hook.unlink()
    backup = directory / BACKUP
    if backup.exists():
        backup.rename(hook)
    shutil.rmtree(directory / BUNDLE)



def pre_push(repo: Path, records: bytes, rules_path: Path | None = None):
    if git(repo, "rev-parse", "--is-shallow-repository").strip() != b"false":
        raise GateError("Complete outgoing history is required")
    rules = rules_for(repo, rules_path)[0]
    findings = []
    checked_trees = set()
    checked_commits = set()
    for record in records.splitlines():
        fields = record.split()
        if len(fields) != 4:
            raise GateError("Invalid push update")
        _, local, _, remote = fields
        if any(not re.fullmatch(rb"[0-9a-f]{40}|[0-9a-f]{64}", oid) for oid in (local, remote)) or len(local) != len(remote):
            raise GateError("Invalid push object")
        if local == b"0" * len(local):
            continue
        revision = local.decode("ascii")
        git(repo, "rev-parse", revision + "^{commit}")
        # A new remote branch has no remote base; skip history already on any remote-tracking ref.
        revisions = [revision, "--not", "--remotes"] if remote == b"0" * len(remote) else [revision, "^" + remote.decode("ascii")]
        for oid in git(repo, "rev-list", *revisions).splitlines():
            if oid in checked_commits:
                continue
            checked_commits.add(oid)
            commit = oid.decode("ascii")
            tree = git(repo, "rev-parse", commit + "^{tree}").strip().decode("ascii")
            if tree not in checked_trees:
                checked_trees.add(tree)
                findings.extend(check(repo, tree=tree, rules_path=rules_path))
            for fmt, allowed in (("%an <%ae>%n%cn <%ce>", {"email", "home_path"}), ("%B", {"home_path"})):
                content = git(repo, "show", "-s", "--format=" + fmt, commit)
                categories = scanner.scan_content(content, "commit") - allowed
                categories.update(literal_categories(content, "commit", rules["literals"]))
                findings.extend((category, "history") for category in sorted(categories))
    return findings


def main() -> int:
    parser = SafeParser(description="Local privacy gate: inspect exact staged bytes without printing private values.")
    parser.add_argument("command", nargs="?", choices=("check", "pre-push", "install", "status", "uninstall"), default="check")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--tree", help="Exact immutable tree OID for commit-tree callers")
    parser.add_argument("--rules", type=Path, help="Private mode-0600 policy outside repository")
    parser.add_argument("--plain", action="store_true")
    parser.add_argument("--details", action="store_true", help="Show only safe categories and hashed location references")
    parser.add_argument("--hook-args", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args()
    prefix = "" if args.plain else "🔒 "
    stop = threading.Event()
    started = time.monotonic()
    def progress():
        while not stop.wait(10):
            print(f"{prefix}Privacy gate: checking locally; elapsed {int(time.monotonic()-started)}s", file=sys.stderr, flush=True)
    worker = threading.Thread(target=progress, daemon=True)
    worker.start()
    try:
        if args.command == "install":
            install(args.repo)
            print(prefix + "Privacy gate installed; prior hook preserved.")
        elif args.command == "uninstall":
            uninstall(args.repo)
            print(prefix + "Privacy gate removed; prior hook restored.")
        elif args.command == "status":
            hook = hook_directory(args.repo) / "pre-commit"
            installed = owned(hook) and os.access(hook, os.X_OK)
            current = installed and all((hook.parent / BUNDLE / name).read_bytes() == (HERE / name).read_bytes() for name in BUNDLE_FILES)
            print(prefix + ("Privacy gate active (scanner current)." if current else "Privacy gate inactive or needs reinstall."))
            return 0 if current else 1
        else:
            records = sys.stdin.buffer.read() if args.command == "pre-push" else b""
            findings = pre_push(args.repo, records, args.rules) if args.command == "pre-push" else check(args.repo, tree=args.tree, rules_path=args.rules)
            if findings:
                repair = "Repair pushed history locally and retry." if args.command == "pre-push" else "Repair locally, stage the safe version, and retry."
                print(prefix + f"Privacy gate BLOCKED: {len(findings)} findings. {repair}")
                for category in sorted({item[0] for item in findings}):
                    # Private policy category names are untrusted; never echo them.
                    safe = category if category in {"provider_token", "credential", "private_key", "email", "home_path", "ip_address", "runtime_identifier", "sensitive_path"} else "private_literal"
                    print(f"{prefix}Category: {safe}")
                if args.details:
                    for _, location in findings:
                        print(f"{prefix}Location reference: {location}")
                return 1
            if args.command == "pre-push":
                if args.hook_args is not None:
                    previous = HERE.parent / "pre-push.privacy-gate-previous"
                    if previous.is_file() and os.access(previous, os.X_OK):
                        result = subprocess.run([str(previous), *args.hook_args], input=records)
                        if result.returncode:
                            return result.returncode
                print(prefix + "Privacy gate PASS: pushed history checked locally.")
            else:
                print(prefix + "Privacy gate PASS: exact candidate checked locally.")
        return 0
    except Exception:
        # Errors can contain Git output, filenames, rules, or interpreter details.
        print(prefix + "Privacy gate ERROR: inspection incomplete; operation refused. Check index conflicts, local objects, private rules and scanner installation locally.", file=sys.stderr)
        return 2
    finally:
        stop.set()
        worker.join()
