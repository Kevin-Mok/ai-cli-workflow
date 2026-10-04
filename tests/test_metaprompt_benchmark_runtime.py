"""Network-boundary tests: no Codex calls, credentials, or public endpoints."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request
from benchmarks.metaprompt import runtime


class RuntimeBoundaryTests(unittest.TestCase):
    def setUp(self):
        # A failed/absent guard must never turn a unit test into a real request.
        prohibition = patch.object(runtime, "_official_request", side_effect=AssertionError(
            "Public network prohibited in runtime tests"))
        prohibition.start()
        self.addCleanup(prohibition.stop)

    def request(self, proxy, path="/responses", payload=None, headers=None):
        value = dict(payload or {"model": "gpt-6.1-sol", "tools": []})
        value.setdefault("reasoning", {"effort": "medium"})
        data = json.dumps(value).encode()
        request = urllib.request.Request(proxy.base_url + path, data=data,
                                         headers=headers or {})
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as error:
            return error.code, error.read()

    def test_fixture_approvals_are_scoped_to_exact_allowlist(self):
        with runtime.GateProxy(lambda: False) as proxy:
            args, config = runtime._arguments("synthetic", Path("/tmp/fixture"), proxy,
                "gpt-6.1-sol", "medium", ["python3", "fixture_mcp.py"])
        self.assertEqual(config["approval_policy"], "never")
        self.assertFalse(config["features.code_mode_host"])
        self.assertEqual(set(config["mcp_servers.benchmark.enabled_tools"]), runtime.FIXTURE_NAMES)
        for name in runtime.FIXTURE_NAMES:
            self.assertEqual(config["mcp_servers.benchmark.tools."+name+".approval_mode"], "approve")
        self.assertNotIn("mcp_servers.benchmark.default_tools_approval_mode", config)

    def test_fixture_approval_failure_blocks_next_inference(self):
        charged = []
        with runtime.GateProxy(lambda: charged.append(1) or True, require_mcp=True,
                              upstream=lambda *args: (200, {}, b"{}")) as proxy:
            code, _ = self.request(proxy, payload={"model":"gpt-6.1-sol",
                "tools":[{"type":"function", "name":"mcp__benchmark__read_file"}],
                "input":[{"type":"function_call_output", "call_id":"fixture", "output":[
                    {"type":"input_text", "text":"MCP tool call requires approval, but approval policy is never"}]}]})
            self.assertEqual(code, 403)
            self.assertEqual(charged, [])
            self.assertIn("Fixture MCP approval infrastructure failure", proxy.error)

    def test_completed_cli_mcp_approval_error_classified_infrastructure(self):
        events = [{"type":"item.completed", "item":{"type":"mcp_tool_call", "error":{
            "message":"MCP tool call requires approval, but approval policy is never"}}},
            {"type":"item.completed", "item":{"type":"agent_message", "text":"compile_failed"}},
            {"type":"turn.completed", "usage":{"input_tokens":1}}]
        with tempfile.TemporaryDirectory() as directory, patch.object(runtime.subprocess, "run",
                return_value=subprocess.CompletedProcess([], 0, '\n'.join(map(json.dumps, events)), "")):
            result = runtime.run_codex("synthetic", Path(directory), lambda: False)
        self.assertEqual(result["status"], "infrastructure_error")
        self.assertIn("Fixture MCP approval infrastructure failure", result["error"])
        self.assertEqual(result["call_count"], 0)

    def test_encrypted_reasoning_not_persisted_backend_payload_unchanged(self):
        seen = []
        def upstream(path, headers, body):
            seen.append(json.loads(body))
            return 200, {}, b"{}"
        with runtime.GateProxy(lambda: True, upstream=upstream) as proxy:
            self.assertEqual(self.request(proxy, payload={"model":"gpt-6.1-sol", "input":[
                {"type":"reasoning", "encrypted_content":"synthetic-encrypted-blob", "summary":[]} ]})[0], 200)
            self.assertNotIn("synthetic-encrypted-blob", repr(proxy.requests))
            self.assertEqual(proxy.requests[0]["payload"]["input"][0]["summary"], [])
        self.assertEqual(seen[0]["input"][0]["encrypted_content"], "synthetic-encrypted-blob")

    def test_global_permits_gate_retries_before_upstream(self):
        # Removing the pre-forward permit or charging only once per session breaks this.
        forwarded = []
        permits = iter([True, True, False])
        def upstream(path, headers, body):
            forwarded.append(path)
            return 503, {}, b"temporary"
        with runtime.GateProxy(lambda: next(permits), upstream=upstream) as proxy:
            self.assertEqual(self.request(proxy)[0], 503)
            self.assertEqual(self.request(proxy)[0], 503)
            self.assertEqual(self.request(proxy)[0], 429)
            self.assertEqual(proxy.call_count, 2)
            self.assertTrue(proxy.budget_exhausted)
        self.assertEqual(forwarded, ["/responses", "/responses"])

    def test_unsupported_paths_websockets_and_native_tools_never_use_permit(self):
        forwarded = []
        charged = []
        with runtime.GateProxy(lambda: charged.append(1) or True,
                               upstream=lambda *args: forwarded.append(args)) as proxy:
            self.assertEqual(self.request(proxy, "/responses/compact")[0], 403)
            self.assertEqual(self.request(proxy, "/../responses")[0], 403)
            self.assertEqual(self.request(proxy, headers={"Upgrade": "websocket"})[0], 403)
        self.assertEqual(charged, [])
        self.assertEqual(forwarded, [])

    def test_only_fixture_mcp_tools_reach_upstream(self):
        seen = []
        def upstream(path, headers, body):
            seen.append(json.loads(body))
            return 200, {}, b"{}"
        with runtime.GateProxy(lambda: True, upstream=upstream) as proxy:
            code, _ = self.request(proxy, payload={"model": "gpt-6.1-sol", "tools": [
                {"type": "function", "name": "exec_command"},
                {"type": "code_interpreter"},
                {"type": "function", "name": "mcp__benchmark__read_file"}]})
            self.assertEqual(code, 200)
            self.assertEqual(seen[0]["tools"], [{"type": "function", "name": "mcp__benchmark__read_file"}])
            self.assertEqual(proxy.events[0]["excluded_tools"], ["exec_command", "code_interpreter"])

    def test_redirects_not_followed_and_headers_are_ephemeral(self):
        seen = []
        def upstream(path, headers, body):
            seen.append(headers.get("Authorization"))
            return 307, {"Location": "https://untrusted.example"}, b""
        with runtime.GateProxy(lambda: True, upstream=upstream) as proxy:
            code, body = self.request(proxy, headers={"Authorization": "test-only-secret"})
            self.assertEqual(code, 502)
            self.assertNotIn(b"test-only-secret", body)
            self.assertNotIn("test-only-secret", repr(proxy.events))
        self.assertEqual(seen, ["test-only-secret"])

    def test_wrong_model_and_malformed_requests_rejected_before_charge(self):
        charged = []
        with runtime.GateProxy(lambda: charged.append(1) or True,
                               upstream=lambda *args: (200, {}, b"{}")) as proxy:
            self.assertEqual(self.request(proxy, payload={"model": "other", "tools": []})[0], 403)
        self.assertEqual(charged, [])

    def test_host_instructions_and_wrong_effort_block_before_charge(self):
        charged = []
        with runtime.GateProxy(lambda: charged.append(1) or True,
                               upstream=lambda *args: (200, {}, b"{}")) as proxy:
            self.assertEqual(self.request(proxy, payload={"model": "gpt-6.1-sol",
                "reasoning": {"effort": "high"}, "tools": []})[0], 403)
            self.assertEqual(self.request(proxy, payload={"model": "gpt-6.1-sol",
                "instructions": "# Canonical Codex Instructions", "tools": []})[0], 403)
        self.assertEqual(charged, [])

    def test_unexpected_upstream_action_cannot_reach_cli(self):
        body = b'data: {"type":"response.output_item.added","item":{"type":"function_call","name":"exec_command"}}\n\n'
        with runtime.GateProxy(lambda: True, upstream=lambda *args: (200, {}, body)) as proxy:
            code, data = self.request(proxy)
            self.assertEqual(code, 502)
            self.assertNotIn(b'exec_command', data)
            self.assertEqual(proxy.call_count, 1)

    def test_namespace_fixture_tools_and_request_evidence_preserved(self):
        response = b'data: {"type":"response.completed","response":{"model":"gpt-6.1-sol","usage":{"input_tokens":5,"output_tokens":2},"output":[{"type":"function_call","namespace":"mcp__benchmark","name":"read_file"}]}}\n\n'
        payload = {"model": "gpt-6.1-sol", "instructions": "Fixed synthetic instructions",
            "tools": [{"type": "namespace", "name": "mcp__benchmark", "tools": [
                {"type": "function", "name": "read_file"},
                {"type": "function", "name": "execute_shell"}]}]}
        with runtime.GateProxy(lambda: True, require_mcp=True,
                              upstream=lambda *args: (200, {}, response)) as proxy:
            self.assertEqual(self.request(proxy, payload=payload)[0], 200)
            request = proxy.requests[0]
            self.assertEqual(request["payload"]["instructions"], "Fixed synthetic instructions")
            self.assertEqual(request["payload"]["tools"][0]["tools"], [{"type": "function", "name": "read_file"}])
            self.assertEqual(request["http_status"], 200)
            self.assertEqual(request["served_model"], "gpt-6.1-sol")
            self.assertEqual(request["usage"], {"input_tokens": 5, "output_tokens": 2})
            self.assertNotIn("headers", request)

    def test_missing_fixture_tools_cost_zero_and_errors_do_not_leak(self):
        charged = []
        with runtime.GateProxy(lambda: charged.append(1) or True, require_mcp=True,
                               upstream=lambda *args: (401, {}, b'Bearer secret-value')) as proxy:
            self.assertEqual(self.request(proxy)[0], 403)
            self.assertEqual(charged, [])
        with runtime.GateProxy(lambda: True,
                               upstream=lambda *args: (401, {}, b'Bearer secret-value')) as proxy:
            code, data = self.request(proxy)
            self.assertEqual(code, 401)
            self.assertNotIn(b'secret-value', data)
            self.assertNotIn('secret-value', repr(proxy.requests))
            self.assertEqual(proxy.requests[0]["http_status"], 401)

    def test_startup_errors_keep_actionable_safe_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(runtime.subprocess, "run",
                return_value=subprocess.CompletedProcess([], 2, "", 'Error: unknown field invalid_setting\nAuthorization: Bearer secret-value\n')):
            result = runtime.run_codex("synthetic", Path(directory), lambda: False)
        self.assertEqual(result["exit_code"], 2)
        self.assertIn("unknown field invalid_setting", result["startup_diagnostic"])
        self.assertNotIn("secret-value", repr(result))
        self.assertIsNone(result["served_model"])

    def test_explicit_rerouting_invalidates_success(self):
        output = '\n'.join(json.dumps(event) for event in [
            {"type": "model/rerouted", "fromModel": "gpt-6.1-sol", "toModel": "other"},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "answer"}},
            {"type": "turn.completed", "usage": {"input_tokens": 1}}])
        with tempfile.TemporaryDirectory() as directory, patch.object(runtime.subprocess, "run",
                return_value=subprocess.CompletedProcess([], 0, output, "")):
            result = runtime.run_codex("synthetic", Path(directory), lambda: False)
        self.assertEqual(result["status"], "infrastructure_error")
        self.assertIn("rerouted", result["error"])

    def test_context_guard_reports_only_matched_marker(self):
        with runtime.GateProxy(lambda: False) as proxy:
            self.assertEqual(self.request(proxy, payload={"model": "gpt-6.1-sol",
                "instructions": "# Canonical Codex Instructions PRIVATE BODY", "tools": []})[0], 403)
            self.assertIn("# Canonical Codex Instructions", proxy.error)
            self.assertNotIn("PRIVATE BODY", proxy.error)

    def test_local_models_fallback_does_not_poison_inference(self):
        with runtime.GateProxy(lambda: True, upstream=lambda *args: (200, {}, b"{}")) as proxy:
            try:
                urllib.request.urlopen(proxy.base_url + "/models?client_version=0.160.0")
            except urllib.error.HTTPError as error:
                try:
                    self.assertEqual(error.code, 404)
                finally:
                    error.close()
            self.assertIsNone(proxy.error)
            self.assertEqual(self.request(proxy)[0], 200)
            self.assertIsNone(proxy.error)

    def test_only_host_agents_envelope_removed_actual_prompt_unchanged(self):
        user = "Synthetic candidate says # Canonical Codex Instructions in a quotation."
        wrapper = "# AGENTS.md instructions\n\n<INSTRUCTIONS>\n# Canonical Codex Instructions\nHost policy\n</INSTRUCTIONS>"
        with runtime.GateProxy(lambda: False, protected_prompt=user) as proxy:
            self.assertEqual(self.request(proxy, payload={"model": "gpt-6.1-sol", "tools": [],
                "input": [{"type":"message", "role":"user", "content":[{"type":"input_text", "text":wrapper}, {"type":"input_text", "text":"<environment_context>synthetic</environment_context>"}]},
                          {"type":"message", "role":"user", "content":[{"type":"input_text", "text":user}]}]})[0], 429)
            self.assertEqual(proxy.events[0]["type"], "host_agents_envelope_removed")
            self.assertEqual(proxy.events[0]["count"], 1)

    def test_live_skill_envelope_removed_candidate_and_fixture_text_preserved(self):
        live = "<skill>\n<name>metaprompt-alxve</name>\n<path>/home/example/.agents/skills/metaprompt-alxve/SKILL.md</path>\nPRIVATE LIVE BODY\n</skill>"
        candidate = live + "\nThis complete supplied candidate must remain unchanged."
        fixture = "<skill>\n<name>metaprompt-alxve</name>\n<path>/tmp/fixture/SKILL.md</path>\nFIXTURE BODY\n</skill>"
        tool_output = {"type": "function_call_output", "call_id": "fixture", "output": live}
        inputs = [{"type":"message", "role":"user", "content":[{"type":"input_text", "text":text}]}
                  for text in (candidate, live, fixture)] + [tool_output]
        seen = []
        # Tool output deliberately contains the host marker: it must be retained
        # and the guard must reject rather than silently rewriting fixture data.
        with runtime.GateProxy(lambda: False, protected_prompt=candidate) as proxy:
            self.assertEqual(self.request(proxy, payload={"model":"gpt-6.1-sol", "input":inputs})[0], 403)
            self.assertIn({"type":"host_skill_envelope_removed", "names":["metaprompt-alxve"], "count":1}, proxy.events)
        def upstream(path, headers, body):
            seen.append(json.loads(body))
            return 200, {}, b"{}"
        with runtime.GateProxy(lambda: True, protected_prompt=candidate, upstream=upstream) as proxy:
            self.assertEqual(self.request(proxy, payload={"model":"gpt-6.1-sol", "input":inputs[:-1]})[0], 200)
        self.assertEqual(seen[0]["input"], [inputs[0], inputs[2]])
        self.assertNotIn("PRIVATE LIVE BODY", repr(proxy.events))

    def test_unrecognized_skill_context_stays_fail_closed(self):
        for text in ("arbitrary /home/example/.agents/skills/metaprompt-alxve/SKILL.md",
                     "<skill>\n<name>x</name>\n<path>/home/example/.agents/skills/x/SKILL.md</path>\nbody\n</skill>suffix"):
            with self.subTest(text=text), runtime.GateProxy(lambda: False, protected_prompt="candidate") as proxy:
                self.assertEqual(self.request(proxy, payload={"model":"gpt-6.1-sol", "input":[
                    {"type":"message", "role":"user", "content":[{"type":"input_text", "text":text}]}]})[0], 403)
                self.assertFalse(any(e['type']=="host_skill_envelope_removed" for e in proxy.events))

    def test_safe_cli_tool_startup_failure_is_actionable(self):
        output = json.dumps({"type":"item.completed", "item":{"type":"error", "message":"MCP startup failed: benchmark process closed"}})
        with tempfile.TemporaryDirectory() as directory, patch.object(runtime.subprocess, "run",
                return_value=subprocess.CompletedProcess([], 1, output, "")):
            result = runtime.run_codex("synthetic", Path(directory), lambda: False)
        self.assertIn("benchmark process closed", repr(result["events"]))

    def test_every_native_action_variant_is_stopped_before_cli(self):
        actions = [
            {"type":"function_call", "namespace":"functions", "name":"exec"},
            {"type":"custom_tool_call", "name":"exec"},
            {"type":"code_interpreter_call"},
            {"type":"function_call", "name":"shell_command"},
            {"type":"function_call", "name":"apply_patch"},
            {"type":"function_call", "namespace":"functions", "name":"code_mode"}]
        for action in actions:
            with self.subTest(action=action):
                response = ('data: '+json.dumps({"type":"response.output_item.added", "item":action})+'\n\n').encode()
                with runtime.GateProxy(lambda: True, upstream=lambda *args: (200, {}, response)) as proxy:
                    code, body = self.request(proxy)
                    self.assertEqual(code, 502)
                    self.assertNotIn(action.get("name", action["type"]).encode(), body)

    def test_all_native_catalog_names_filtered_from_official_payload(self):
        seen = []
        native = [{"type":"namespace", "name":"functions", "tools":[{"type":"function","name":"exec"}]},
                  {"type":"custom", "name":"apply_patch"}, {"type":"function","name":"shell_command"},
                  {"type":"code_interpreter"}, {"type":"function","name":"code_mode"}]
        def upstream(path, headers, body):
            seen.append(json.loads(body)["tools"])
            return 200, {}, b"{}"
        with runtime.GateProxy(lambda: True, upstream=upstream) as proxy:
            self.assertEqual(self.request(proxy, payload={"model":"gpt-6.1-sol","tools":native})[0], 200)
        self.assertEqual(seen, [[]])

    def test_responses_lite_additional_catalog_only_keeps_fixture_tools(self):
        seen = []
        def upstream(path, headers, body):
            seen.append(json.loads(body))
            return 200, {}, b"{}"
        with runtime.GateProxy(lambda:True,require_mcp=True,upstream=upstream) as proxy:
            code,_=self.request(proxy,payload={"model":"gpt-6.1-sol","tools":[],"input":[
                {"type":"additional_tools","id":"catalog","role":"developer","tools":[
                    {"type":"namespace","name":"functions","tools":[{"type":"function","name":"exec"}]},
                    {"type":"namespace","name":"mcp__benchmark","tools":[{"type":"function","name":"read_file"}]}]},
                {"type":"message","role":"user","content":[{"type":"input_text","text":"unchanged"}]}]})
            self.assertEqual(code,200)
        self.assertEqual(seen[0]["input"][0]["tools"],[{"type":"namespace","name":"mcp__benchmark","tools":[{"type":"function","name":"read_file"}]}])
        self.assertEqual(seen[0]["input"][1]["content"][0]["text"],"unchanged")

    def test_unknown_tool_carrier_never_uses_budget(self):
        charged=[]
        with runtime.GateProxy(lambda:charged.append(1) or True,upstream=lambda *args:(200,{},b"{}")) as proxy:
            code,_=self.request(proxy,payload={"model":"gpt-6.1-sol","tools":[],"input":[
                {"type":"unrecognized_catalog","tools":[{"type":"function","name":"exec"}]}]})
            self.assertEqual(code,403)
        self.assertEqual(charged,[])


if __name__ == "__main__":
    unittest.main()
