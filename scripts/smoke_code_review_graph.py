#!/usr/bin/env python3
"""Exercise the installed CRG CLI or stdio MCP against disposable source only."""
import argparse
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import tempfile
import time

TOOLS = "get_minimal_context_tool,get_impact_radius_tool,query_graph_tool,list_graph_stats_tool"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", default=shutil.which("code-review-graph") or str(Path.home() / ".local/bin/code-review-graph"))
    parser.add_argument("--mode", choices=("cli", "mcp"), required=True)
    parser.add_argument("--plain", action="store_true")
    parser.add_argument("--details", action="store_true")
    args = parser.parse_args()
    binary = str(Path(args.binary).resolve())

    def say(emoji, message):
        print(message if args.plain else f"{emoji} {message}", flush=True)

    def run(argv):
        process = subprocess.Popen(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        started = time.monotonic()
        while True:
            try:
                stdout, stderr = process.communicate(timeout=5)
                break
            except subprocess.TimeoutExpired:
                elapsed = int(time.monotonic() - started)
                say("⏳", f"Running {Path(argv[0]).name} {argv[1]}; elapsed {elapsed}s.")
                if elapsed >= 90:
                    process.kill()
                    process.communicate()
                    raise RuntimeError(f"{Path(argv[0]).name} timed out after 90s")
        if args.details:
            print(stdout, end="")
            print(stderr, end="")
        if process.returncode:
            raise RuntimeError(f"{Path(argv[0]).name} {argv[1]} failed (exit {process.returncode}); use --details")
        return stdout

    try:
        with tempfile.TemporaryDirectory(prefix="crg-smoke-") as folder:
            root = Path(folder)
            env = {key: value for key, value in os.environ.items() if not key.startswith(("CRG_", "GIT_"))}
            env.update(HOME=str(root / "home"), CRG_HOME=str(root / "registry"),
                       XDG_CONFIG_HOME=str(root / "config"), XDG_CACHE_HOME=str(root / "cache"),
                       XDG_DATA_HOME=str(root / "data"), XDG_STATE_HOME=str(root / "state"),
                       GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                       CRG_ALLOW_REMOTE_CODE="0", DO_NOT_TRACK="1", HF_HUB_DISABLE_TELEMETRY="1")
            (root / "home").mkdir()
            say("🔎", f"Exercising {args.mode} in disposable source (no live client or model calls).")
            run(["git", "-c", "init.templateDir=", "init", "-q", folder])
            source = root / "sample.py"
            source.write_text("def helper():\n    return 1\n\ndef caller():\n    return helper()\n")
            run(["git", "-C", folder, "add", "sample.py"])
            run(["git", "-C", folder, "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "-c", "user.name=CRG Smoke", "-c", "user.email=smoke@example.invalid", "commit", "-qm", "fixture"])
            say("⏳", "Building two-function fixture; command timeout 90s.")
            run([binary, "build", "--repo", folder, "--skip-flows"])
            if args.mode == "cli":
                result = json.loads(run([binary, "query", "callers_of", "helper", "--repo", folder]))
                if result.get("status") != "ok" or {node["name"] for node in result["results"]} != {"caller"}:
                    raise RuntimeError("CLI did not identify caller -> helper")
                source.write_text(source.read_text() + "\ndef second():\n    return helper()\n")
                run([binary, "update", "--repo", folder, "--skip-flows"])
                result = json.loads(run([binary, "query", "callers_of", "helper", "--repo", folder]))
                if {node["name"] for node in result["results"]} != {"caller", "second"}:
                    raise RuntimeError("Incremental update missed the second caller")
                say("✅", "CLI: caller -> helper found; incremental update found caller + second.")
                return 0

            with tempfile.TemporaryFile() as errors:
                process = subprocess.Popen([binary, "serve", "--repo", folder, "--tools", TOOLS], env=env,
                                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors)
                selector = selectors.DefaultSelector()
                selector.register(process.stdout, selectors.EVENT_READ)
                pending = b""

                def rpc(request):
                    nonlocal pending
                    process.stdin.write((json.dumps(request) + "\n").encode())
                    process.stdin.flush()
                    if "id" not in request:
                        return None
                    deadline = time.monotonic() + 45
                    progress = time.monotonic()
                    while time.monotonic() < deadline:
                        if selector.select(timeout=1):
                            chunk = os.read(process.stdout.fileno(), 65536)
                            if not chunk:
                                raise RuntimeError("MCP exited before responding; use --details")
                            pending += chunk
                            while b"\n" in pending:
                                line, pending = pending.split(b"\n", 1)
                                response = json.loads(line)
                                if response.get("id") == request["id"]:
                                    if "error" in response:
                                        raise RuntimeError(f"MCP protocol error: {response['error']}")
                                    return response["result"]
                        if time.monotonic() - progress >= 5:
                            say("⏳", "Waiting for stdio MCP response.")
                            progress = time.monotonic()
                    raise RuntimeError("MCP response timed out after 45s")

                def call(number, method, params):
                    return rpc({"jsonrpc": "2.0", "id": number, "method": method, "params": params})

                try:
                    call(1, "initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "dotfiles-smoke", "version": "1"}})
                    rpc({"jsonrpc": "2.0", "method": "notifications/initialized"})
                    tools = call(2, "tools/list", {})
                    if {item["name"] for item in tools["tools"]} != set(TOOLS.split(",")):
                        raise RuntimeError("MCP tool list differs from the four-tool allowlist")
                    reply = call(3, "tools/call", {"name": "query_graph_tool", "arguments": {"pattern": "callers_of", "target": "helper", "repo_root": folder}})
                    data = reply.get("structuredContent") or json.loads(next(c["text"] for c in reply["content"] if c["type"] == "text"))
                    if reply.get("isError") or data.get("status") != "ok" or data.get("result_count") != 1:
                        raise RuntimeError("MCP query did not return the fixture caller")
                    for number, name, arguments in (
                        (5, "list_graph_stats_tool", {"repo_root": folder}),
                        (6, "get_impact_radius_tool", {"repo_root": folder, "changed_files": ["sample.py"]}),
                    ):
                        reply = call(number, "tools/call", {"name": name, "arguments": arguments})
                        data = reply.get("structuredContent") or json.loads(next(c["text"] for c in reply["content"] if c["type"] == "text"))
                        if reply.get("isError") or data.get("status") != "ok":
                            raise RuntimeError(f"MCP {name} did not succeed")
                    missing = root / "unbuilt"
                    missing.mkdir()
                    (missing / ".git").mkdir()
                    reply = call(4, "tools/call", {"name": "get_minimal_context_tool", "arguments": {"repo_root": str(missing)}})
                    data = reply.get("structuredContent") or json.loads(next(c["text"] for c in reply["content"] if c["type"] == "text"))
                    if data.get("status") != "not_ready" or (missing / ".code-review-graph").exists():
                        raise RuntimeError("Missing-graph check did not remain not_ready without a build")
                    say("✅", "MCP: exactly four tools; query/stats/impact passed; unbuilt graph reports not_ready.")
                finally:
                    selector.close()
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                    if args.details:
                        errors.seek(0)
                        print(errors.read().decode(errors="replace"), end="")
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired) as error:
        say("❌", str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
