"""Subscription Codex transport with an atomic, pre-forward inference gate.

Credentials are supplied by Codex itself and exist only in request memory.
This module never reads auth files. All inference goes through a custom HTTP
provider and the sole upstream destination is the normal official Codex route.
The model tool catalog is identically filtered to fixture MCP tools for every
request. This explicit harness adaptation is recorded in the returned settings.
"""
from __future__ import annotations

import http.client
import json
import os
import re
from pathlib import Path
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable

OFFICIAL_HOST = "chatgpt.com"
OFFICIAL_BASE = "/backend-api/codex"
ALLOWED_TOOLS = frozenset("mcp__benchmark__" + name for name in
                          ("read_file", "write_file", "list_files"))
FIXTURE_NAMES = frozenset(("read_file", "write_file", "list_files"))


def _installed_skill_envelope_name(item, part, protected_prompt):
    """Recognize only the CLI's separate installed-skill user fragment.

    Supplied prompt text and tool/reference outputs are never rewritten. A
    fragment in an unknown shape remains subject to the fail-closed host guard.
    """
    if (item.get("role") != "user" or item.get("type") != "message"
            or not isinstance(part, dict) or part.get("type") != "input_text"):
        return None
    text = part.get("text", "")
    if not isinstance(text, str) or text == protected_prompt:
        return None
    match = re.fullmatch(r"<skill>\s*<name>([^<>\r\n]+)</name>\s*"
                         r"<path>([^<>\r\n]+)</path>\s*[\s\S]*</skill>\s*", text)
    if not match:
        return None
    name, path_text = match.groups()
    path = Path(path_text)
    roots = (Path.home() / ".agents" / "skills", Path.home() / ".codex" / "skills")
    if (not path.is_absolute() or ".." in path.parts or path.name != "SKILL.md"
            or not any(path.is_relative_to(root) and len(path.relative_to(root).parts) >= 2
                       for root in roots)):
        return None
    return name


def _filter_tools(tools):
    kept, excluded = [], []
    for tool in tools:
        if tool.get("type") == "function" and tool.get("name") in ALLOWED_TOOLS:
            kept.append(tool)
        elif tool.get("type") == "namespace" and tool.get("name") == "mcp__benchmark":
            children = tool.get("tools", [])
            if not isinstance(children, list) or any(not isinstance(t, dict) for t in children):
                raise ValueError("Malformed namespace tools")
            allowed = [t for t in children if t.get("type") == "function"
                       and t.get("name") in FIXTURE_NAMES]
            excluded.extend("mcp__benchmark." + str(t.get("name", t.get("type")))
                            for t in children if t not in allowed)
            if allowed:
                kept.append({**tool, "tools": allowed})
        else:
            excluded.append(tool.get("name", tool.get("type", "unknown")))
    return kept, excluded


def _filter_catalogs(payload):
    """Responses Lite carries schemas in input.additional_tools, not tools."""
    tools = payload.get("tools", [])
    if not isinstance(tools, list) or any(not isinstance(t, dict) for t in tools):
        raise ValueError("Malformed tool catalog")
    payload["tools"], excluded = _filter_tools(tools)
    available = bool(payload["tools"])
    items = payload.get("input", [])
    if not isinstance(items, list):
        raise ValueError("Unsupported input framing")
    kept = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Unsupported input item")
        if item.get("type") == "additional_tools":
            if item.get("role") != "developer" or set(item) - {"type", "id", "role", "tools"}:
                raise ValueError("Unknown additional tool carrier")
            nested = item.get("tools")
            if not isinstance(nested, list) or any(not isinstance(t, dict) for t in nested):
                raise ValueError("Malformed additional tool catalog")
            filtered, removed = _filter_tools(nested)
            excluded.extend("input.additional_tools:" + str(name) for name in removed)
            if filtered:
                available = True
                kept.append({**item, "tools": filtered})
        elif "tools" in item or item.get("type") in {"tool_catalog", "tool_definition", "tool_definitions"}:
            raise ValueError("Unknown tool carrier")
        else:
            kept.append(item)
    payload["input"] = kept
    if "additional_tools" in payload:
        raise ValueError("Unknown top-level tool carrier")
    return available, excluded


def _persisted_payload(value):
    """Storage-only copy: encrypted reasoning is opaque and not reproducible."""
    if isinstance(value, dict):
        return {key: _persisted_payload(item) for key, item in value.items()
                if key != "encrypted_content"}
    if isinstance(value, list):
        return [_persisted_payload(item) for item in value]
    return value


def _response_values(body):
    if body.lstrip().startswith((b"{", b"[")):
        return [json.loads(body)]
    return [json.loads(line[5:].strip()) for line in body.splitlines()
            if line.startswith(b"data:") and line[5:].strip() not in (b"", b"[DONE]")]


def _response_metadata(body):
    model, usage = None, None
    try:
        for value in _response_values(body):
            if not isinstance(value, dict):
                continue
            response = value.get("response", value if value.get("object") == "response" else {})
            if isinstance(response, dict):
                model = response.get("model") or model
                usage = response.get("usage") or usage
    except (ValueError, UnicodeError):
        pass
    return model, usage


def _startup_diagnostic(stderr):
    lines = []
    for line in re.sub(r"\x1b\[[0-9;]*m", "", stderr).splitlines():
        if re.search(r"authorization|bearer|token|credential|password|secret|cookie|sk-[A-Za-z0-9]|auth\.json", line, re.I):
            continue
        if re.search(r"error:|unknown|unrecognized|unsupported|invalid|not supported|failed to", line, re.I):
            lines.append(line[:300])
    return "\n".join(lines[:8])


def _official_request(path: str, headers: dict, body: bytes) -> tuple:
    connection = http.client.HTTPSConnection(OFFICIAL_HOST, timeout=180)
    try:
        forwarded_headers = {
            key: value for key, value in headers.items()
            if key.lower() not in {"host", "connection", "content-length", "transfer-encoding", "content-encoding", "accept-encoding"}
        }
        forwarded_headers["Accept-Encoding"] = "identity"
        connection.request("POST", OFFICIAL_BASE + path, body=body, headers=forwarded_headers)
        response = connection.getresponse()
        # Buffer before forwarding so unexpected tool actions cannot run locally.
        return response.status, dict(response.getheaders()), response.read()
    finally:
        connection.close()


def _safe_response(body: bytes) -> bool:
    """Inspect tool-bearing SSE/JSON items before the CLI can execute them."""
    def safe(value):
        if isinstance(value, list):
            return all(safe(item) for item in value)
        if not isinstance(value, dict):
            return True
        kind = value.get("type", "")
        allowed_call = (value.get("name") in ALLOWED_TOOLS or
                        (value.get("namespace") == "mcp__benchmark" and value.get("name") in FIXTURE_NAMES))
        if kind == "function_call" and not allowed_call:
            return False
        if kind.endswith("_call") and kind != "function_call":
            return False
        return all(safe(item) for item in value.values())
    try:
        return all(safe(value) for value in _response_values(body))
    except (ValueError, UnicodeError):
        return False


class GateProxy:
    """Loopback-only HTTP proxy. One permit per upstream POST, including retry."""

    def __init__(self, permit: Callable[[], bool], *, model="gpt-6.1-sol",
                 upstream=None, require_mcp=False, protected_prompt=None):
        self.permit = permit
        self.model = model
        self.upstream = upstream or _official_request
        self.call_count = 0
        self.budget_exhausted = False
        self.error = None
        self.events = []
        self.requests = []
        self.require_mcp = require_mcp
        self.protected_prompt = protected_prompt
        self.lock = threading.Lock()

    def __enter__(self):
        owner = self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def reply(self, status, body=b"", content_type="application/json"):
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                try:
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def reject(self, message, status=403):
                owner.error = message
                self.reply(status, json.dumps({"error": message}).encode())

            def do_GET(self):
                if (self.path == OFFICIAL_BASE + "/models" or
                        self.path.startswith(OFFICIAL_BASE + "/models?")) and not self.headers.get("Upgrade"):
                    owner.events.append({"type": "local_model_catalog_fallback", "http_status": 404})
                    return self.reply(404, b'{"error":"Use installed bundled model catalog"}')
                self.reject("Non-inference route or WebSocket rejected")

            do_PUT = do_GET
            do_DELETE = do_GET
            do_PATCH = do_GET
            do_CONNECT = do_GET

            def do_POST(self):
                if self.path != OFFICIAL_BASE + "/responses" or self.headers.get("Upgrade"):
                    return self.reject("Unsupported inference route or WebSocket rejected")
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    if not 0 < length <= 4_000_000 or self.headers.get("Transfer-Encoding"):
                        return self.reject("Unsupported request framing")
                    payload = json.loads(self.rfile.read(length))
                    if not isinstance(payload, dict) or payload.get("model") != owner.model:
                        return self.reject("Unexpected model")
                    if payload.get("reasoning", {}).get("effort") != "medium":
                        return self.reject("Unexpected reasoning effort")
                    items = payload.get("input", [])
                    if any(isinstance(item, dict) and item.get("type") == "function_call_output"
                           and "MCP tool call requires approval, but approval policy is never" in json.dumps(item.get("output"))
                           for item in items if isinstance(items, list)):
                        return self.reject("Fixture MCP approval infrastructure failure; no further inference sent")
                    removed = 0
                    removed_skills = []
                    if owner.protected_prompt is not None and isinstance(items, list):
                        kept = []
                        for item in items:
                            parts = item.get("content", []) if isinstance(item, dict) else []
                            kept_parts = []
                            for part in parts:
                                text = part.get("text", "") if isinstance(part, dict) else ""
                                envelope = (isinstance(item, dict) and item.get("role") == "user"
                                    and text.startswith("# AGENTS.md instructions")
                                    and "\n<INSTRUCTIONS>\n# Canonical Codex Instructions" in text
                                    and text.rstrip().endswith("</INSTRUCTIONS>")
                                    and text != owner.protected_prompt)
                                skill_name = _installed_skill_envelope_name(item, part, owner.protected_prompt) if isinstance(item, dict) else None
                                if envelope:
                                    removed += 1
                                elif skill_name is not None:
                                    removed_skills.append(skill_name)
                                else:
                                    kept_parts.append(part)
                            if len(kept_parts) != len(parts):
                                if kept_parts:
                                    kept.append({**item, "content": kept_parts})
                            else:
                                kept.append(item)
                        payload["input"] = items = kept
                    if removed:
                        owner.events.append({"type": "host_agents_envelope_removed", "count": removed})
                    if removed_skills:
                        owner.events.append({"type": "host_skill_envelope_removed",
                                             "names": removed_skills, "count": len(removed_skills)})
                    # Protect the original candidate/task text even if it quotes a
                    # host marker; examine only other harness/context messages.
                    guard_items = [item for item in items if not (isinstance(item, dict)
                        and item.get("role") == "user" and any(isinstance(part, dict)
                            and part.get("text") == owner.protected_prompt
                            for part in item.get("content", [])))] if isinstance(items, list) else items
                    context = json.dumps(guard_items) + str(payload.get("instructions", ""))
                    marker = next((marker for marker in (
                            "# Canonical Codex Instructions", "<skills_instructions>",
                            "/home/example/linux-config", "/home/example/.agents/skills/",
                            "/home/example/.codex/skills/") if marker in context), None)
                    if marker:
                        owner.events.append({"type": "blocked_host_context_structure",
                            "top_instructions": marker in str(payload.get("instructions", "")),
                            "items": [{"role": item.get("role"), "type": item.get("type"),
                                "parts": [{"type": part.get("type"),
                                    "has_marker": marker in str(part.get("text", "")),
                                    "agents_prefix": str(part.get("text", "")).startswith("# AGENTS.md instructions for "),
                                    "user_agents_prefix": str(part.get("text", "")).startswith("User-provided AGENTS.md instructions for "),
                                    "hash_user_agents_prefix": str(part.get("text", "")).startswith("# User-provided AGENTS.md instructions for "),
                                    "starts_instructions_tag": str(part.get("text", "")).startswith("<INSTRUCTIONS>"),
                                    "instruction_tags": "<INSTRUCTIONS>" in str(part.get("text", "")) and "</INSTRUCTIONS>" in str(part.get("text", ""))}
                                    for part in item.get("content", []) if isinstance(part, dict)]}
                                for item in items if isinstance(item, dict)] if isinstance(items, list) else []})
                        return self.reject("Host instructions or installed skill context detected: " + marker)
                    tools = payload.get("tools", [])
                    if not isinstance(tools, list) or any(not isinstance(t, dict) for t in tools):
                        return self.reject("Malformed tool catalog")
                    try:
                        available, excluded = _filter_catalogs(payload)
                    except ValueError:
                        return self.reject("Unknown or malformed tool catalog carrier")
                    if owner.require_mcp and not available:
                        owner.events.append({"type": "missing_fixture_catalog",
                            "additional_tools": [{"keys": list(item),
                                "tools": [{"keys": list(t), "type": t.get("type"), "name": t.get("name"),
                                    "children": [child.get("name") for child in t.get("tools", []) if isinstance(child, dict)]}
                                    for t in item.get("tools", []) if isinstance(t, dict)]}
                                for item in payload.get("input", []) if isinstance(item, dict) and item.get("type") == "additional_tools"],
                            "catalog": [{"type": t.get("type"), "name": t.get("name"),
                                "children": [child.get("name") for child in t.get("tools", []) if isinstance(child, dict)]}
                                for t in tools]})
                        return self.reject("Fixture MCP tool catalog missing; no inference sent")
                    choice = payload.get("tool_choice")
                    if isinstance(choice, dict) or choice not in (None, "auto", "none", "required"):
                        return self.reject("Unsupported tool choice")
                    # Serialize charges before any external connection is opened.
                    with owner.lock:
                        if not owner.permit():
                            owner.budget_exhausted = True
                            return self.reject("Inference budget exhausted", 429)
                        owner.call_count += 1
                        evidence = {"payload": _persisted_payload(payload), "http_status": None,
                                    "usage": None, "served_model": None}
                        owner.requests.append(evidence)
                        owner.events.append({"type": "inference_forwarded",
                                             "call": owner.call_count,
                                             "excluded_tools": excluded})
                    status, headers, body = owner.upstream("/responses", dict(self.headers),
                                                          json.dumps(payload).encode())
                    evidence["http_status"] = status
                    if status == 200:
                        evidence["served_model"], evidence["usage"] = _response_metadata(body)
                        if evidence["served_model"] is not None and evidence["served_model"] != owner.model:
                            return self.reject("Served model differs from requested model", 502)
                    if 300 <= status < 400:
                        return self.reject("Upstream redirect rejected", 502)
                    if status == 200 and not _safe_response(body):
                        return self.reject("Unexpected upstream tool action rejected", 502)
                    # Error bodies could contain diagnostics or credentials; never relay them.
                    if status != 200:
                        return self.reject("Official upstream inference failed", status)
                    self.reply(status, body, headers.get("Content-Type", "application/json"))
                except Exception:
                    # Exception text may contain headers; report only a fixed safe message.
                    self.reject("Inference transport failed", 502)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.base_url = f"http://127.0.0.1:{self.server.server_port}{OFFICIAL_BASE}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()


def _arguments(prompt, scratch, proxy, model, effort, mcp_command):
    args = ["codex", "exec", "--ignore-user-config", "--ignore-rules", "--ephemeral",
            "--json", "--skip-git-repo-check", "--strict-config", "-s", "read-only",
            "-C", str(scratch), "-m", model]
    config = {
        "model_provider": "metaprompt-benchmark", "model_reasoning_effort": effort,
        "approval_policy": "never", "approvals_reviewer": "user",
        "project_doc_max_bytes": 0, "web_search": "disabled",
        "skills.include_instructions": False, "skills.bundled.enabled": False,
        "cloud.skills.enabled": False, "agents.enabled": False,
        "features.code_mode.enabled": False,
        "features.code_mode.direct_only_tool_namespaces": ["mcp__benchmark"],
        "features.code_mode_only": False,
        "tools.update_plan.enabled": False, "model_post_turn_compact_threshold_percent": 0,
        "model_providers.metaprompt-benchmark.name": "Metaprompt benchmark transport",
        "model_providers.metaprompt-benchmark.base_url": proxy.base_url,
        "model_providers.metaprompt-benchmark.wire_api": "responses",
        "model_providers.metaprompt-benchmark.requires_openai_auth": True,
        "model_providers.metaprompt-benchmark.supports_websockets": False,
        "model_providers.metaprompt-benchmark.request_max_retries": 0,
        "model_providers.metaprompt-benchmark.stream_max_retries": 0,
    }
    for feature in ("shell_tool", "unified_exec", "view_image", "apps", "plugins",
                    "browser_use", "computer_use", "image_generation", "multi_agent",
                    "multi_agent_v2", "skill_search", "hooks", "code_mode_host",
                    "memories", "goals", "sleep_tool", "unbounded_connection_retries"):
        config["features." + feature] = False
    config["features.skip_host_skill_discovery"] = True
    if mcp_command:
        config["mcp_servers.benchmark.command"] = mcp_command[0]
        config["mcp_servers.benchmark.args"] = mcp_command[1:]
        config["mcp_servers.benchmark.enabled_tools"] = sorted(FIXTURE_NAMES)
        for name in sorted(FIXTURE_NAMES):
            config["mcp_servers.benchmark.tools." + name + ".approval_mode"] = "approve"
    for key, value in config.items():
        args.extend(["-c", key + "=" + json.dumps(value)])
    args.append("-")
    return args, config


def run_codex(prompt: str, scratch: Path, permit: Callable[[], bool],
              model="gpt-6.1-sol", effort="medium", timeout=180,
              mcp_command: list[str] | None = None) -> dict:
    started = time.monotonic()
    result = {"status": "infrastructure_error", "output": "", "usage": None,
              "latency_seconds": 0, "error": None, "call_count": 0,
              "requests": [], "served_model": None, "exit_code": None,
              "startup_diagnostic": "",
              "events": [], "settings": {"tool_filter": "fixture MCP allowlist",
                                          "host_context_filter": "Recognized injected canonical AGENTS and installed-root skill user envelopes; original prompt and fixture outputs preserved",
                                          "buffered_transport": True,
                                          "persisted_payload_omits": ["encrypted_content"]}}
    scratch = Path(scratch).resolve()
    if not scratch.is_dir() or model != "gpt-6.1-sol" or effort != "medium":
        result["error"] = "Invalid scratch directory or benchmark model/effort"
        return result
    with GateProxy(permit, model=model, require_mcp=bool(mcp_command), protected_prompt=prompt) as proxy:
        args, config = _arguments(prompt, scratch, proxy, model, effort, mcp_command)
        result["settings"].update(config)
        # No inherited paid API key or model endpoint overrides. Auth remains
        # normal Codex subscription auth; HOME and CODEX_HOME are never changed.
        env = dict(os.environ)
        for key in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "AZURE_OPENAI_API_KEY"):
            env.pop(key, None)
        try:
            completed = subprocess.run(args, input=prompt, text=True,
                                       capture_output=True, timeout=timeout, env=env)
            result["exit_code"] = completed.returncode
            if completed.returncode != 0:
                result["startup_diagnostic"] = _startup_diagnostic(completed.stderr)
            malformed = False
            for line in completed.stdout.splitlines():
                try:
                    event = json.loads(line)
                except ValueError:
                    malformed = True
                    continue
                kind = event.get("type")
                if kind in {"model/rerouted", "model.rerouted", "model_rerouted"}:
                    proxy.error = "Requested benchmark model was rerouted"
                item = event.get("item", {})
                if kind == "item.completed" and item.get("type") == "agent_message":
                    result["output"] = item.get("text", "")
                elif kind == "turn.completed":
                    result["usage"] = event.get("usage")
                elif kind in {"item.started", "item.completed"} and item.get("type") in {
                        "command_execution", "file_change", "web_search"}:
                    proxy.error = "Unexpected native action observed"
                if item.get("type") == "mcp_tool_call" and "MCP tool call requires approval, but approval policy is never" in json.dumps(item):
                    proxy.error = "Fixture MCP approval infrastructure failure"
                safe_event = {"type": kind, "item_type": item.get("type")}
                if item.get("type") == "error" or kind in {"error", "turn.failed"}:
                    error = event.get("error", {})
                    message = item.get("message") or item.get("text") or event.get("message")
                    if not message and isinstance(error, dict):
                        message = error.get("message")
                    if message:
                        safe_event["diagnostic"] = _startup_diagnostic("Error: " + str(message))
                result["events"].append(safe_event)
            if completed.returncode == 0 and not proxy.error and not malformed and result["output"]:
                result["status"] = "ok"
            else:
                result["error"] = proxy.error or "Codex invocation failed or produced incomplete evidence"
        except subprocess.TimeoutExpired:
            result["error"] = "Codex invocation timed out"
        except OSError:
            result["error"] = "Codex executable could not start"
        if proxy.budget_exhausted:
            result["status"] = "budget_exhausted"
        result["call_count"] = proxy.call_count
        result["events"].extend(proxy.events)
        result["requests"] = proxy.requests
        models = [request["served_model"] for request in proxy.requests if request["served_model"]]
        result["served_model"] = models[-1] if models else None
    result["latency_seconds"] = time.monotonic() - started
    return result
