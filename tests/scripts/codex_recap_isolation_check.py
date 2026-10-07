#!/usr/bin/env python3
"""Zero-upstream, actual-CLI isolation check using synthetic local config."""
import argparse
import http.server
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
argparse.ArgumentParser(description=__doc__).parse_args()
from codex_search_runtime import IsolatedCodex

captured = []


def names(items):
    result = []
    for item in items:
        name = item.get('name', item.get('type'))
        result.append(name)
        result.extend(names(item.get('tools', [])))
    return result


class Sink(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'{"error":"Use bundled catalog"}')

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        catalog = names(payload.get('tools', []))
        for item in payload.get('input', []):
            if item.get('type') == 'additional_tools':
                catalog.extend(names(item.get('tools', [])))
        # Store only names and fixed synthetic facts, never headers or prompts.
        captured.append({'model': payload.get('model'), 'catalog': catalog})
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'{"error":{"message":"Intentional zero-inference catalog check","type":"invalid_request_error"}}')


server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Sink)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
try:
    with tempfile.TemporaryDirectory(prefix='codex-recap-catalog-') as temporary:
        root = Path(temporary)
        home = root/'codex'
        home.mkdir()
        canary = root/'mcp-started'
        mcp = root/'mcp-canary.py'
        mcp.write_text('from pathlib import Path\nPath('+repr(str(canary))+').touch()\n')
        config = '\n'.join([
            'model="gpt-6-astra"', 'model_provider="recap-local-check"',
            '[model_providers.recap-local-check]', 'name="Local synthetic sink"',
            'base_url="http://127.0.0.1:'+str(server.server_port)+'"',
            'wire_api="responses"', 'requires_openai_auth=false',
            'supports_websockets=false', 'request_max_retries=0', 'stream_max_retries=0',
            '[mcp_servers.canary]', 'command='+json.dumps(sys.executable),
            'args=['+json.dumps(str(mcp))+']', 'enabled=true',
        ])
        (home/'config.toml').write_text(config)
        runtime = IsolatedCodex(home)
        try:
            model = runtime.prepare()
            assert not canary.exists(), 'config-only preflight started the MCP canary'
            cwd = root/'scratch'
            cwd.mkdir()
            schema = cwd/'schema.json'
            schema.write_text(json.dumps({'type': 'object', 'properties': {
                key: {'type': 'string'} for key in ('headline','goal','progress','state','next_steps')},
                'required': ['headline','goal','progress','state','next_steps'],
                'additionalProperties': False}))
            output = cwd/'output.json'
            output.touch(mode=0o600)
            argv, env = runtime.command(cwd, schema, output)
            cwd.chmod(0o500)
            try:
                process = subprocess.run(argv, input='Synthetic dialogue: user requested a recap; assistant has not started.',
                                         capture_output=True, text=True, env=env, timeout=20)
            finally:
                cwd.chmod(0o700)
            assert process.returncode == 1, 'the local sink must reject without inference'
            assert len(captured) == 1, 'the synthetic request must not be retried'
            allowed = {'functions', 'exec', 'wait', 'request_user_input', 'request_user_input_async'}
            assert set(captured[0]['catalog']) <= allowed, 'unexpected effective tool capability'
            assert 'Code Mode is unavailable because code-mode host is disabled' in process.stdout
            assert not canary.exists(), 'an isolated phase started the configured MCP server'
            print(json.dumps({'model': model, 'requests_to_local_sink': len(captured),
                              'upstream_requests': 0, 'configured_mcp_started': False,
                              'catalog_names': captured[0]['catalog'],
                              'code_mode_host': 'disabled, fail-closed',
                              'expected_rejected_exit': process.returncode}, indent=2))
        finally:
            runtime.cancel()
finally:
    server.shutdown()
    server.server_close()
    thread.join()
