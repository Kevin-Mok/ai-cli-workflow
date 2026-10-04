"""Actual Codex CLI/MCP integration with synthetic, offline model responses.

Run: python3 tests/test_metaprompt_selection_runtime.py
No model endpoint is called. The sole runtime upstream function is replaced,
HTTPS transport is rejected, and fixture changes remain in temporary directories.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / 'benchmarks' / 'metaprompt-selection'
sys.path.insert(0, str(BENCHMARK))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime = load_module('selection_offline_test_runtime', BENCHMARK / 'selection_runtime.py')
mcp = load_module('selection_offline_test_mcp', BENCHMARK / 'selection_mcp.py')


class SyntheticUpstream:
    """One scripted tool/message item per request; no model or HTTP client."""

    def __init__(self, steps):
        self.steps = steps
        self.payloads = []

    def __call__(self, path, headers, body):
        # Never persist, inspect, or print authorization headers.
        payload = json.loads(body)
        self.payloads.append(payload)
        n = len(self.payloads)
        if path != '/responses' or n > len(self.steps):
            raise AssertionError('Unexpected synthetic request')
        step = self.steps[n - 1]
        if step[0] == 'final':
            item = {'type': 'message', 'id': 'msg_offline_' + str(n),
                    'role': 'assistant', 'status': 'completed',
                    'content': [{'type': 'output_text', 'text': step[1], 'annotations': []}]}
        else:
            name, arguments = step
            item = {'type': 'function_call', 'id': 'fc_offline_' + str(n),
                    'call_id': 'call_offline_' + str(n), 'name': name,
                    'namespace': 'mcp__benchmark', 'arguments': json.dumps(arguments),
                    'status': 'completed'}
        response = {'id': 'resp_offline_' + str(n), 'object': 'response',
                    'model': 'gpt-6.1-sol', 'status': 'completed', 'output': [item],
                    'usage': {'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0}}
        events = [
            {'type': 'response.created', 'response': {**response, 'status': 'in_progress', 'output': []}},
            {'type': 'response.output_item.added', 'output_index': 0, 'item': item},
            {'type': 'response.output_item.done', 'output_index': 0, 'item': item},
            {'type': 'response.completed', 'response': response},
        ]
        return (200, {'Content-Type': 'text/event-stream'},
                ''.join('data: ' + json.dumps(event) + '\n\n' for event in events).encode())


class ActualCodexOfflineIntegration(unittest.TestCase):
    def run_stage(self, scratch, prefix, steps, replace=False):
        if not shutil.which('codex'):
            self.skipTest('Actual Codex CLI is not installed')
        upstream = SyntheticUpstream(steps)
        log = scratch.parent / (scratch.name + '-tools.jsonl')
        command = [sys.executable, str(BENCHMARK / 'selection_mcp.py'),
                   str(scratch), prefix, str(log)]
        if replace:
            command.append('--replace-target')
        with mock.patch.object(runtime, '_official_request', upstream), \
                mock.patch.object(runtime.http.client, 'HTTPSConnection',
                                  side_effect=AssertionError('Remote HTTPS forbidden')) as remote:
            result = runtime.run_codex('Perform the supplied offline fixture steps.', scratch,
                                       lambda: len(upstream.payloads) < len(steps),
                                       timeout=45, mcp_command=command)
            self.assertEqual(remote.call_count, 0, 'No remote/model HTTPS may be opened')
        self.assertEqual(result['status'], 'ok',
                         (result['error'], result['startup_diagnostic'], result['events']))
        self.assertEqual(result['call_count'], len(steps))
        self.assertEqual(len(upstream.payloads), len(steps))
        self.assertEqual(result['output'], steps[-1][1])
        self.assertTrue(log.is_file(), 'Real MCP server must persist tool effects')
        trace = [json.loads(line) for line in log.read_text().splitlines()]
        self.assertEqual([row['tool'] for row in trace], [step[0] for step in steps[:-1]])
        self.assertTrue(all(row['status'] == 'ok' for row in trace), trace)
        return result, trace, upstream

    def test_compiler_reads_reference_and_saves_real_prompt(self):
        with tempfile.TemporaryDirectory(prefix='selection-offline-compiler-') as tmp:
            scratch = Path(tmp) / 'compiler'
            (scratch / 'references').mkdir(parents=True)
            (scratch / 'references' / 'contract.md').write_text('Synthetic reference: preserve missing facts.')
            prompt = 'Use supplied facts; missing facts are unknown. Return only JSON.'
            steps = [
                ('read_file', {'path': 'references/contract.md'}),
                ('write_file', {'path': 'prompts/result.md', 'content': prompt}),
                ('final', 'Saved: prompts/result.md'),
            ]
            _, trace, upstream = self.run_stage(scratch, 'prompts', steps)
            self.assertEqual((scratch / 'prompts' / 'result.md').read_text(), prompt)
            self.assertEqual(trace[0]['result'], 'Synthetic reference: preserve missing facts.')
            self.assertIn('Synthetic reference', json.dumps(upstream.payloads[1]['input']))
            self.assertEqual(sorted(str(p.relative_to(scratch)) for p in scratch.rglob('*') if p.is_file()),
                             ['prompts/result.md', 'references/contract.md'])

    def test_solver_edits_real_target_runs_public_tests_and_finishes(self):
        with tempfile.TemporaryDirectory(prefix='selection-offline-solver-') as tmp:
            scratch = Path(tmp) / 'solver'
            scratch.mkdir()
            original = 'def double(value):\n    return value\n'
            corrected = 'def double(value):\n    return value * 2\n'
            public = 'from target import double\nassert double(3) == 6\nassert double(-2) == -4\n'
            (scratch / 'target.py').write_text(original)
            (scratch / 'public_tests.py').write_text(public)
            steps = [
                ('read_file', {'path': 'target.py'}),
                ('write_file', {'path': 'target.py', 'content': corrected}),
                ('run_tests', {}),
                ('final', corrected),
            ]
            _, trace, upstream = self.run_stage(scratch, 'target.py', steps, replace=True)
            self.assertEqual((scratch / 'target.py').read_text(), corrected)
            self.assertEqual((scratch / 'public_tests.py').read_text(), public)
            self.assertTrue(json.loads(trace[2]['result'])['success'])
            self.assertIn('Public assertions passed', trace[2]['result'])
            self.assertIn('Public assertions passed', json.dumps(upstream.payloads[3]['input']))
            self.assertEqual(sorted(p.name for p in scratch.iterdir()), ['public_tests.py', 'target.py'])

    def test_native_helper_traversal_is_denied_before_process_start(self):
        with tempfile.TemporaryDirectory(prefix='selection-offline-denial-') as tmp:
            scratch = Path(tmp) / 'compiler'
            (scratch / 'prompts').mkdir(parents=True)
            (scratch / 'prompts' / 'draft.md').write_text('Synthetic prompt')
            fs = mcp.FixtureFiles(scratch, 'prompts')
            log = Path(tmp) / 'denials.jsonl'
            message = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                       'params': {'name': 'run_skill_check',
                                  'arguments': {'prompt_path': 'prompts/draft.md'}}}
            with mock.patch.object(mcp.subprocess, 'run') as process:
                response = mcp.respond(message, fs, log, helper='../outside-helper.py')
                process.assert_not_called()
            self.assertTrue(response['result']['isError'])
            record = json.loads(log.read_text())
            self.assertEqual(record['status'], 'denied')
            self.assertEqual(record['tool'], 'run_skill_check')


if __name__ == '__main__':
    unittest.main(verbosity=2)
