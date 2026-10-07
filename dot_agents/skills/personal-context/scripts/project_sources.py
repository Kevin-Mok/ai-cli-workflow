#!/usr/bin/env python3
"""Read-only, bounded technical observations from local project sources.

Nothing here executes project code, follows source instructions, or writes a
project file. Callers persist the returned summaries only in private storage.
"""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tomllib

MANIFESTS = frozenset({
    "package.json", "pyproject.toml", "Cargo.toml", "go.mod", "pom.xml",
    "build.gradle", "build.gradle.kts", "composer.json", "Gemfile",
    "CMakeLists.txt", "requirements.txt", "setup.py", "mix.exs",
    "Package.swift", "pubspec.yaml", "deno.json", "deno.jsonc",
})
EXCLUDED_DIRS = frozenset({
    "personal-context", "private", "personal", "private-payload", "private-payloads",
    "payloads", "secrets", "credentials", "node_modules", "vendor", "dist", "build", "target",
    "coverage", "htmlcov", "__pycache__", "venv", "env", "site-packages",
    "cache", "caches", "generated", "out", "tmp", "temp", "logs",
    "bower_components", "bower-cache", "data", "datasets", "uploads",
    "backups", "backup", "fixtures", "test-results", "playwright-report",
})
MAX_SOURCES = 32
MAX_SOURCE_BYTES = 131072
MAX_CANDIDATES = 256
CODE_SUFFIXES = frozenset({".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".swift", ".java", ".rb", ".ex", ".php", ".sh"})
CONFIG_NAMES = frozenset({
    "Dockerfile", "Makefile", "docker-compose.yml", "docker-compose.yaml",
    "compose.yml", "compose.yaml", "tsconfig.json", "pytest.ini", "setup.cfg",
    "next.config.js", "next.config.ts", "next.config.mjs", "vite.config.ts",
    "vitest.config.ts", "playwright.config.ts", "tailwind.config.ts",
    "tailwind.config.js", "main.tf", "vercel.json", "firebase.json",
})
SENSITIVE_NAME = re.compile(r"(?:^\.env|secret|credential|password|token|private[-_]key|(?:^|[._-])id_rsa|\.pem$|\.key$)", re.I)
UNSAFE_PROSE = re.compile(
    r"(?:api[_ -]?key|password|secret|access[_ -]?token|authorization|bearer\s|"
    r"BEGIN\s.*PRIVATE|https?://[^\s/]+:[^\s/]+@|"
    r"ignore\s.*instructions|system\s+prompt|execute\s.*command|you are|assistant|agent must|"
    r"\brun\s+(?:rm|curl|wget|sudo|bash|sh)\b|rm\s+-rf|sk-[A-Za-z0-9]{16})", re.I
)
# Canonical labels are technical observations, never statements about the person.
TECH_MARKERS = {
    "React": r"\breact\b", "Next.js": r"\bnext(?:js|\.js)?\b",
    "TypeScript": r"\btypescript\b", "Tailwind CSS": r"\btailwindcss\b",
    "FastAPI": r"\bfastapi\b", "Pydantic": r"\bpydantic\b",
    "pytest": r"\bpytest\b", "unittest": r"\bunittest\b",
    "Playwright": r"\bplaywright\b", "Vitest": r"\bvitest\b",
    "PostgreSQL": r"\b(?:postgresql|postgres|psycopg|asyncpg)\b",
    "Supabase": r"\bsupabase\b", "SQLAlchemy": r"\bsqlalchemy\b",
    "Terraform": r"\bterraform\b", "Docker": r"\bdocker\b",
    "Express": r"\bexpress\b", "Flask": r"\bflask\b",
    "Django": r"\bdjango\b", "Vue": r"\bvue\b", "Svelte": r"\bsvelte\b",
}
PATTERNS = {
    "FastAPI": "FastAPI API framework dependency or source references",
    "Pydantic": "Pydantic validation dependency or source references",
    "pytest": "pytest testing dependency or source references",
    "unittest": "unittest regression-check source references",
    "Playwright": "Playwright browser-testing dependency or source references",
    "Vitest": "Vitest testing dependency or source references",
    "Terraform": "Terraform infrastructure configuration references",
    "Docker": "Docker container configuration references",
    "SQLAlchemy": "SQLAlchemy database dependency or source references",
    "React": "React component dependency or source references",
}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _skip_dir(path):
    return path.is_symlink() or path.name.startswith(".") or path.name.lower() in EXCLUDED_DIRS


def _project_marker(path, files, directories):
    return ".git" in files or ".git" in directories or bool(MANIFESTS.intersection(files))


def _assert_no_link_ancestors(path):
    if any(component.is_symlink() for component in (path, *path.parents)):
        raise ValueError("root and its ancestors must not contain symlinks")


def _open_directory(path):
    """Acquire an absolute directory without following any ancestor symlink."""
    path = Path(path).absolute()
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    descriptor = os.open(path.anchor, flags)
    try:
        for part in path.parts[1:]:
            next_fd = os.open(part, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_fd
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


MAX_GIT_COMMITS = 10000
MAX_GIT_OUTPUT_BYTES = 32 * 1024 * 1024
_REPO_INVENTORIES = {}


def _git(repo, *arguments):
    """Read Git metadata/objects without hooks, filters, inherited config or shell."""
    descriptor = _open_directory(repo)
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    environment.update({
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_SYSTEM": "/dev/null",
        "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_REPLACE_OBJECTS": "1", "GIT_ATTR_NOSYSTEM": "1",
        "GIT_PAGER": "cat", "LC_ALL": "C",
    })
    try:
        result = subprocess.run([
            "git", "--no-pager", "--no-optional-locks", "--literal-pathspecs",
            "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null",
            "-c", "diff.external=", "-c", "core.attributesFile=/dev/null",
            "-c", "log.showSignature=false", *arguments,
        ], cwd=f"/proc/self/fd/{descriptor}", pass_fds=(descriptor,),
            env=environment, capture_output=True, check=False, timeout=20)
        if result.returncode:
            raise ValueError("Git authorship unavailable or unreadable")
        if len(result.stdout) > MAX_GIT_OUTPUT_BYTES:
            raise ValueError("Git evidence output exceeds inspection limit")
        return result.stdout
    except subprocess.TimeoutExpired as exc:
        raise ValueError("Git authorship inspection timed out") from exc
    finally:
        os.close(descriptor)


def _nearest_git_owner(project, coding_root):
    path = project
    while True:
        descriptor = _open_directory(path)
        try:
            try:
                marker = os.stat(".git", dir_fd=descriptor, follow_symlinks=False)
            except FileNotFoundError:
                marker = None
            if marker is not None:
                if stat.S_ISLNK(marker.st_mode):
                    raise ValueError("symlinked Git metadata excluded")
                if stat.S_ISDIR(marker.st_mode) or stat.S_ISREG(marker.st_mode):
                    return path
        finally:
            os.close(descriptor)
        if path == coding_root:
            return None
        path = path.parent


def _repo_inventory(repo):
    head = _git(repo, "rev-parse", "--verify", "HEAD^{commit}").strip().decode("ascii")
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head):
        raise ValueError("invalid Git HEAD identity")
    key = (str(repo), head)
    if key in _REPO_INVENTORIES:
        return _REPO_INVENTORIES[key]
    tree = {}
    for record in _git(repo, "ls-tree", "-r", "-z", "-l", "--full-tree", head).split(b"\0"):
        if not record:
            continue
        metadata, name = record.split(b"\t", 1)
        mode, kind, oid, size = metadata.split()
        if kind == b"blob":
            tree[os.fsdecode(name)] = {"mode": mode.decode("ascii"), "oid": oid.decode("ascii"), "size": int(size)}
    history = _git(repo, "log", "--topo-order", "--full-history", "--diff-merges=first-parent",
        "--no-show-signature", "--no-notes", "--no-decorate", "--no-renames", "--no-abbrev",
        "--max-count=" + str(MAX_GIT_COMMITS + 1), "--format=%x00%H%x00%an%x00", "--raw", "-z", head)
    tokens = history.split(b"\0")
    latest = {}
    commits = set()
    commit = author = None
    index = 0
    while index < len(tokens):
        token = tokens[index].lstrip(b"\n")
        if not token:
            index += 1
            continue
        if re.fullmatch(rb"[0-9a-f]{40}|[0-9a-f]{64}", token):
            if index + 1 >= len(tokens):
                raise ValueError("incomplete Git author history")
            commit = token.decode("ascii")
            author = os.fsdecode(tokens[index + 1])
            commits.add(commit)
            index += 2
        elif re.fullmatch(rb":[0-7]{6} [0-7]{6} [0-9a-f]{40,64} [0-9a-f]{40,64} [A-Z][0-9]*", token):
            if commit is None or index + 1 >= len(tokens):
                raise ValueError("incomplete Git path history")
            name = os.fsdecode(tokens[index + 1])
            latest.setdefault(name, {"author": author, "commit": commit})
            index += 2
        else:
            raise ValueError("unrecognized Git author history")
    if len(commits) > MAX_GIT_COMMITS:
        raise ValueError("Git history exceeds 10000-commit inspection limit; authorship incomplete")
    inventory = {"head": head, "tree": tree, "latest": latest}
    _REPO_INVENTORIES[key] = inventory
    return inventory


def _authored_source(source, coding_root, repo, inventory):
    # Check eligibility before opening bytes from unqualified/untracked sources.
    if source.is_symlink():
        raise ValueError("symlink excluded")
    if not source.is_file():
        raise ValueError("non-regular source excluded")
    if repo is None or inventory is None:
        raise ValueError("no eligible Git author provenance")
    name = source.relative_to(repo).as_posix()
    committed = inventory["tree"].get(name)
    if committed is None:
        raise ValueError("untracked or absent from HEAD")
    if committed["mode"] not in {"100644", "100755"}:
        raise ValueError("non-regular committed source excluded")
    latest = inventory["latest"].get(name)
    if not latest or latest["author"].casefold() != "example-user mok":
        raise ValueError("latest modifying commit is not authored by example-user Mok")
    if committed["size"] > MAX_SOURCE_BYTES:
        raise ValueError(f"exceeds {MAX_SOURCE_BYTES}-byte inspection limit")
    data = _read_regular(source, coding_root)
    blob = _git(repo, "cat-file", "blob", committed["oid"])
    if data != blob:
        raise ValueError("working source differs from HEAD; uncommitted content excluded")
    return data, {"author": "example-user Mok", "commit": latest["commit"], "blob_sha256": hashlib.sha256(blob).hexdigest()}


def discover_projects(coding_root: Path) -> list[Path]:
    """Find Git and manifest roots, including nested roots, without link traversal."""
    root = Path(coding_root).absolute()
    _assert_no_link_ancestors(root)
    if not root.exists():
        return []
    if root.is_symlink() or not root.is_dir():
        raise ValueError("coding root must be a real directory, not a symlink")
    projects = []
    root_fd = _open_directory(root)
    try:
        for current, directories, files, _ in os.fwalk(".", dir_fd=root_fd, follow_symlinks=False):
            path = root / current
            if path != root and _project_marker(path, files, directories):
                projects.append(path)
            directories[:] = sorted(name for name in directories if not _skip_dir(path / name))
    finally:
        os.close(root_fd)
    eligible = []
    for project in sorted(projects, key=lambda path: path.relative_to(root).as_posix()):
        if inspect_project(project, root)["sources"]:
            eligible.append(project)
    return eligible


def _safe_prose(text, limit=360):
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = " ".join(text.strip(" #>*`-\t\r\n").split())
    if not text or UNSAFE_PROSE.search(text) or text.startswith(("http://", "https://", "![")):
        return None
    return text[:limit]


def _documentation(text):
    purpose = None
    constraints = []
    in_code = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.lstrip().startswith(("#", "|", "[!", "![", "<!--")):
            continue
        prose = _safe_prose(line)
        if not prose:
            continue
        if purpose is None and len(prose) >= 20 and not re.match(r"^(?:npm|pip|python|git|cd|bash|sudo|curl|Run|Install)\b", prose):
            purpose = prose
        if re.search(r"\b(?:must|requires?|only|never|do not|constraint|read.only)\b", prose, re.I):
            if len(constraints) < 4 and prose not in constraints:
                constraints.append(prose)
    return purpose, constraints


def _kind(path, relative):
    name = path.name
    if SENSITIVE_NAME.search(name):
        return None
    if name in MANIFESTS:
        return "manifest"
    if name.lower().startswith("readme") or (path.suffix.lower() == ".md" and name.lower() in {
        "architecture.md", "design.md", "contributing.md", "development.md", "testing.md", "overview.md", "constraints.md",
    }):
        return "documentation"
    if name in CONFIG_NAMES or (relative.parts[0] == ".github" and path.suffix in {".yml", ".yaml"}):
        return "configuration"
    if path.suffix in CODE_SUFFIXES:
        if any(part in {"test", "tests", "__tests__", "spec", "specs"} for part in relative.parts) or name.startswith("test_") or re.search(r"\.(?:test|spec)\.", name):
            return "test"
        if len(relative.parts) <= 3 and (name.startswith(("main.", "index.", "app.", "server.", "page.", "layout.")) or relative.parts[0] in {"src", "app", "lib", "scripts", "services"}):
            return "entrypoint"
    return None


def _candidates(project):
    found = []
    ignored = []
    # Inspect a shallow source slice, leaving the rest explicitly outside coverage.
    for current, directories, files in os.walk(project, followlinks=False):
        path = Path(current)
        relative = path.relative_to(project)
        if path != project and (".git" in files or ".git" in directories):
            ignored.append(relative.as_posix() + "/: nested project inspected separately")
            directories[:] = []
            continue
        directories[:] = sorted(name for name in directories if (name == ".github" or not _skip_dir(path / name)))
        if len(relative.parts) >= 4:
            if directories:
                ignored.append(relative.as_posix() + "/: deeper directories not inspected")
            directories[:] = []
        for name in sorted(files):
            source = path / name
            rel = source.relative_to(project)
            kind = _kind(source, rel)
            if kind:
                found.append((source, kind))
                if len(found) >= MAX_CANDIDATES:
                    ignored.append("remaining source candidates: discovery inspection limit reached")
                    break
        if len(found) >= MAX_CANDIDATES:
            break
    priorities = {"documentation": 0, "manifest": 1, "configuration": 2, "entrypoint": 3, "test": 4}
    found.sort(key=lambda pair: (priorities[pair[1]], len(pair[0].relative_to(project).parts), pair[0].relative_to(project).as_posix()))
    # Ensure large source trees cannot consume every test slot.
    selected = []
    for kind in priorities:
        group = [pair for pair in found if pair[1] == kind]
        quota = {"documentation": 6, "manifest": 6, "configuration": 6, "entrypoint": 8, "test": 6}[kind]
        selected.extend(group[:quota])
    extras = [pair for pair in found if pair not in selected]
    selected.extend(extras[:MAX_SOURCES - len(selected)])
    ignored.extend(pair[0].relative_to(project).as_posix() + ": outside selected source budget" for pair in found if pair not in selected)
    return selected, ignored


def _read_regular(path, coding_root):
    # Hold each directory descriptor and use O_NOFOLLOW at every component. This
    # blocks symlink substitution races as well as ordinary link escapes.
    directory_fd = _open_directory(coding_root)
    descriptor = None
    try:
        relative = path.relative_to(coding_root)
        for part in relative.parts[:-1]:
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        if path.is_symlink():
            raise ValueError("symlink excluded")
        descriptor = os.open(relative.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory_fd)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("non-regular source excluded")
        if info.st_size > MAX_SOURCE_BYTES:
            raise ValueError(f"exceeds {MAX_SOURCE_BYTES}-byte inspection limit")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            data = stream.read(MAX_SOURCE_BYTES + 1)
        if len(data) > MAX_SOURCE_BYTES:
            raise ValueError(f"exceeds {MAX_SOURCE_BYTES}-byte inspection limit")
        if b"\0" in data:
            raise ValueError("binary source excluded")
        return data
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(directory_fd)


def _technologies(path, text, kind):
    scan = text
    description = None
    if kind == "documentation":
        scan = "\n".join(
            line for line in text.splitlines()
            if _safe_prose(line) and not re.search(r"\b(?:do not|never|avoid|without|deprecated|instead of)\b", line, re.I)
        )
    if path.name in {"package.json", "composer.json", "deno.json"}:
        value = json.loads(text)
        if not isinstance(value, dict):
            raise ValueError("manifest must contain an object")
        dependency_keys = []
        for field in ("dependencies", "devDependencies", "peerDependencies", "require", "imports"):
            dependencies = value.get(field, {})
            if isinstance(dependencies, dict):
                dependency_keys.extend(dependencies)
        scan = " ".join(dependency_keys)
        if isinstance(value.get("description"), str):
            description = _safe_prose(value["description"])
    elif path.name in {"pyproject.toml", "Cargo.toml"}:
        value = tomllib.loads(text)
        scan = text
        metadata = value.get("project", value.get("package", {}))
        if isinstance(metadata, dict) and isinstance(metadata.get("description"), str):
            description = _safe_prose(metadata["description"])
    technologies = [label for label, marker in TECH_MARKERS.items() if re.search(marker, scan, re.I)]
    language = {".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript", ".go": "Go", ".rs": "Rust", ".swift": "Swift", ".java": "Java", ".rb": "Ruby", ".php": "PHP", ".sh": "Shell"}.get(path.suffix)
    if language:
        technologies.append(language)
    if path.name == "package.json":
        technologies.append("JavaScript")
    if path.name == "pyproject.toml":
        technologies.append("Python")
    if path.name == "Cargo.toml":
        technologies.append("Rust")
    if path.name == "go.mod":
        technologies.append("Go")
    if path.name == "Dockerfile" or "compose" in path.name:
        technologies.append("Docker")
    if path.suffix == ".tf":
        technologies.append("Terraform")
    return sorted(set(technologies)), description


def inspect_project(project: Path, coding_root: Path) -> dict:
    """Return concise summaries and provenance; never infer personal attributes."""
    root = Path(coding_root).absolute()
    _assert_no_link_ancestors(root)
    project = Path(project)
    if root.is_symlink() or project.is_symlink():
        raise ValueError("project and coding roots must not be symlinks")
    project = project.absolute()
    try:
        relative = project.relative_to(root)
    except ValueError as exc:
        raise ValueError("project must be contained in coding root") from exc
    if any(_skip_dir(root.joinpath(*relative.parts[:index])) for index in range(1, len(relative.parts) + 1)):
        raise ValueError("excluded or symlinked project path")
    if not project.is_dir():
        raise ValueError("project must be a readable directory")
    stamp = _now()
    identity = hashlib.sha256(relative.as_posix().encode()).hexdigest()[:16]
    value = {
        "id": "project-" + identity, "key": "project." + identity,
        "topic": "projects", "relative_path": relative.as_posix(),
        "purpose": "Purpose not established from selected readable documentation or manifests.",
        "technologies": [], "structure": [], "constraints": [], "patterns": [],
        "sources": [], "unavailable": [], "uninspected": [], "inspected_at": stamp,
    }
    repo = inventory = None
    try:
        repo = _nearest_git_owner(project, root)
        if repo is not None:
            value["repo_relative_path"] = repo.relative_to(root).as_posix()
            inventory = _repo_inventory(repo)
        else:
            value["unavailable"].append("project: no owning Git repository under coding root")
    except (OSError, ValueError) as exc:
        value["unavailable"].append("project: " + (str(exc) if isinstance(exc, ValueError) else "Git authorship unavailable or unreadable"))
    value["provenance_version"] = 1
    candidates, value["uninspected"] = _candidates(project)
    for kind in ("documentation", "manifest", "configuration", "entrypoint", "test"):
        if not any(candidate_kind == kind for _, candidate_kind in candidates):
            value["uninspected"].append(kind + ": no eligible sources found")
    tech = set()
    patterns = set()
    for source, kind in candidates:
        local = source.relative_to(project).as_posix()
        try:
            data, author_evidence = _authored_source(source, root, repo, inventory)
            text = data.decode("utf-8")
            technologies, description = _technologies(source, text, kind)
        except (OSError, ValueError, UnicodeError) as exc:
            # Errors deliberately contain no source contents or exception payloads.
            reason = str(exc) if isinstance(exc, ValueError) and str(exc) in {
                "symlink excluded", "non-regular source excluded", "binary source excluded",
                f"exceeds {MAX_SOURCE_BYTES}-byte inspection limit", "manifest must contain an object",
                "no eligible Git author provenance", "untracked or absent from HEAD",
                "non-regular committed source excluded", "latest modifying commit is not authored by example-user Mok",
                "working source differs from HEAD; uncommitted content excluded",
            } else "unreadable or malformed source"
            value["unavailable"].append(local + ": " + reason)
            continue
        tech.update(technologies)
        qualifier = "Documented technology reference: " if kind == "documentation" else "Source technology reference: "
        observations = [qualifier + label for label in technologies]
        source_patterns = sorted({PATTERNS[label] for label in technologies if label in PATTERNS}) if kind != "documentation" else []
        patterns.update(source_patterns)
        observations.extend("Technical pattern: " + pattern for pattern in source_patterns)
        if kind == "documentation":
            purpose, constraints = _documentation(text)
            if purpose and value["purpose"].startswith("Purpose not established"):
                value["purpose"] = purpose
                observations.append("Documented purpose: " + purpose)
            value["constraints"].extend(item for item in constraints if item not in value["constraints"])
            observations.extend("Documented constraint: " + item for item in constraints)
        elif description and value["purpose"].startswith("Purpose not established"):
            value["purpose"] = description
            observations.append("Manifest description: " + description)
        if not observations:
            observations = ["Selected " + kind + " source inspected; no additional pattern established."]
        value["sources"].append({
            "path": source.relative_to(root).as_posix(), "sha256": hashlib.sha256(data).hexdigest(),
            "inspected_at": stamp, "kind": kind, "observations": observations[:12], "author_evidence": author_evidence,
        })
    value["technologies"] = sorted(tech)
    value["patterns"] = sorted(patterns)
    value["constraints"] = value["constraints"][:8]
    structure = set()
    for source in value["sources"]:
        local = Path(source["path"]).relative_to(relative)
        structure.add(local.parts[0] + ("/" if len(local.parts) > 1 else ""))
    value["structure"] = sorted(structure)[:24]
    value["uninspected"] = value["uninspected"][:128]
    inputs = {
        "inspection_format_version": 1, "provenance_version": 1,
        "sources": [(item["path"], item["sha256"], item["author_evidence"]) for item in value["sources"]],
        "unavailable": value["unavailable"], "uninspected": value["uninspected"],
        "structure": value["structure"],
    }
    value["fingerprint"] = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    return value


def recurring_findings(projects: list[dict]) -> list[dict]:
    """Aggregate technical approaches supported by at least two project records."""
    groups = {}
    for project in projects:
        for source in project["sources"]:
            for observation in source["observations"]:
                if not observation.startswith("Technical pattern: "):
                    continue
                statement = observation.removeprefix("Technical pattern: ")
                evidence = {
                    "project_id": project["id"], "path": source["path"],
                    "sha256": source["sha256"], "inspected_at": source["inspected_at"],
                }
                group = groups.setdefault(statement, [])
                if evidence not in group:
                    group.append(evidence)
    findings = []
    for statement, evidence in sorted(groups.items()):
        project_ids = sorted({item["project_id"] for item in evidence})
        if len(project_ids) < 2:
            continue
        identifier = hashlib.sha256(statement.encode()).hexdigest()[:16]
        findings.append({
            "id": "finding-" + identifier, "key": "technical." + identifier,
            "topic": "architecture", "statement": statement + " appears in multiple inspected projects.",
            "scope": "Selected source slices of " + str(len(project_ids)) + " local projects; project status and ownership are not established.",
            "basis": "observed", "status": "source_backed",
            "implication": "Consider this existing approach when requirements fit; inspect supporting files before reuse.",
            "evidence": evidence,
            "inspected_at": max(item["inspected_at"] for item in evidence),
        })
    return findings
