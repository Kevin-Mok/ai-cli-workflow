"""Exercise automatic owned-page edits and creator cleanup through the CLI."""
import json
import os
from pathlib import Path
import queue
import runpy
import signal
import subprocess
import sys
import tempfile
import time
import threading
import unittest

from lavish_connection_fixtures import (
    ROOT, SCRIPT, KEY, THREAD, OTHER, lavish, fake_creator,
)


class ConnectionSmokeTest(unittest.TestCase):
    def test_no_arguments_creates_and_tests_its_own_page_without_input(self):
        with lavish('auto-complete') as (_origin, server, requests), fake_creator(server) as (environment, calls):
            process = subprocess.Popen([sys.executable, str(SCRIPT), '--plain', '--timeout', '2'], stdin=subprocess.DEVNULL,
                                       env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                output, error = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.send_signal(signal.SIGINT)
                process.communicate(timeout=6)
                self.fail('No-input flow did not automatically send and verify the edit')
            result = subprocess.CompletedProcess(process.args, process.returncode, output, error)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('PASS', result.stdout)
            self.assertIn('TEST COMPLETE:', result.stdout)
            self.assertNotIn('Click Send', result.stdout)
            self.assertIn('Expected result: heading', result.stdout)
            self.assertIn('Connection verified', result.stdout)
            page = Path(json.loads(server.state.read_text())['sessions'][KEY]['file']).read_text()
            self.assertNotIn('manual-test-prefill', page)
            self.assertIn('<h1>Connection verified</h1>', page)
            self.assertEqual(json.loads(Path(str(calls)+'.sdk').read_text()), {'queued': 1, 'sent': True})
            self.assertEqual(json.loads(server.state.read_text())['sessions'][KEY]['status'], 'ended')
            self.assertTrue(result.stdout.rstrip().endswith('TEST COMPLETE: connection and edit passed; owned test session closed.'))
            self.assertTrue((result.stdout+result.stderr).isascii())
            argv = json.loads(calls.read_text())
            self.assertIn('--json', argv)
            self.assertIn('--approve-for-me', argv)
            self.assertIn('lavish-axi index.html --no-open', argv[-1])
            self.assertIn('google-chrome', argv[-1])
            self.assertNotIn('--ignore-user-config', argv)
            self.assertNotIn('--model', argv)
            self.assertEqual(sum(method == 'POST' for method, _ in requests), 2)

    def test_automatic_edit_timeout_is_bounded_and_cleans_up(self):
        with lavish('auto-timeout') as (_origin, server, _requests), fake_creator(server) as (environment, calls):
            process = subprocess.Popen([sys.executable, str(SCRIPT), '--plain', '--timeout', '.5'], stdin=subprocess.DEVNULL,
                                       env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                output, error = process.communicate(timeout=3)
            except subprocess.TimeoutExpired:
                process.send_signal(signal.SIGINT)
                process.communicate(timeout=6)
                self.fail('Automatic edit wait ignored its phase deadline')
            self.assertNotEqual(process.returncode, 0)
            self.assertIn('Timed out waiting for the automatic edit', error)
            self.assertNotIn('TEST COMPLETE:', output)
            self.assertTrue(Path(str(calls)+'.end').exists())
            self.assertEqual(json.loads(server.state.read_text())['sessions'][KEY]['status'], 'ended')

    def test_completion_requires_readable_ended_owned_page_after_cleanup(self):
        for mode in ('cleanup-unreadable', 'cleanup-open'):
            with self.subTest(mode=mode), lavish('auto-complete') as (_origin, server, _requests), fake_creator(server, mode) as (environment, _calls):
                result = subprocess.run([sys.executable, str(SCRIPT), '--plain', '--timeout', '2'], input='',
                                        env=environment, capture_output=True, text=True, timeout=8)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('TEST COMPLETE:', result.stdout)
                self.assertIn('could not be closed', result.stderr)

    def test_manual_result_rejects_commented_heading_and_mentions_of_other_creator(self):
        check = runpy.run_path(str(SCRIPT))['manual_edit_complete']
        cases = [
            ('<!-- <h1>Connection verified</h1> --><h1>Original heading</h1>', f'CODEX_THREAD_ID: {THREAD}. Heading Connection verified.'),
            ('<script>"<h1>Connection verified</h1>"</script><h1>Original heading</h1>', f'CODEX_THREAD_ID: {THREAD}. Heading Connection verified.'),
            ('<h1>Connection verified</h1>', f'CODEX_THREAD_ID: {OTHER}. Original creator: {THREAD}. Heading Connection verified.'),
        ]
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / 'index.html'
            for content, reply in cases:
                with self.subTest(content=content, reply=reply):
                    artifact.write_text(content)
                    session = {'chat': [{'role': 'user', 'text': 'Manual edit test:', 'delivered_at': 'now', 'done_at': 'now'},
                                        {'role': 'agent', 'text': reply}]}
                    self.assertFalse(check(session, artifact, THREAD))

    def test_successful_manual_edit_finishes_without_user_ending_review(self):
        with lavish('manual-auto-finish') as (_origin, server, _requests), fake_creator(server) as (environment, calls):
            process = subprocess.Popen([sys.executable, str(SCRIPT), '--plain'], stdin=subprocess.DEVNULL,
                                       env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                output, error = process.communicate(timeout=4)
            except subprocess.TimeoutExpired:
                process.send_signal(signal.SIGINT)
                process.communicate(timeout=6)
                self.fail('Completed edit did not conclude without another user action')
            self.assertEqual(process.returncode, 0, error)
            self.assertTrue(any(line.startswith('EDIT TEST PASS:') for line in output.splitlines()))
            self.assertTrue(any(line.startswith('TEST COMPLETE:') for line in output.splitlines()))
            self.assertEqual(json.loads(server.state.read_text())['sessions'][KEY]['status'], 'ended')
            self.assertTrue(Path(str(calls)+'.end').exists())

    def test_manual_completion_reports_once_and_requires_both_edit_and_correct_reply(self):
        for mode in ('manual-complete', 'manual-wrong', 'manual-no-edit', 'manual-no-reply'):
            with self.subTest(mode=mode), lavish(mode) as (_origin, server, _requests), fake_creator(server) as (environment, _calls):
                result = subprocess.run([sys.executable, str(SCRIPT), '--plain'], input='',
                                        env=environment, capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0 if mode == 'manual-complete' else 1, result.stderr)
                reports = sum(line.startswith('EDIT TEST PASS:') for line in result.stdout.splitlines())
                self.assertEqual(reports, 1 if mode == 'manual-complete' else 0, result.stdout)

    def test_bare_requires_the_expected_result_notice_in_chat_before_pass(self):
        with lavish('missing-notice') as (_origin, server, _requests), fake_creator(server) as (environment, _calls):
            result = subprocess.run([sys.executable, str(SCRIPT), '--plain', '--timeout', '.3'],
                                    input='', env=environment, capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('PASS', result.stdout)

    def test_owned_edit_queues_then_sends_through_lavish_sdk(self):
        javascript = ROOT / 'scripts/lavish-manual-test.js'
        self.assertTrue(javascript.is_file(), 'Manual edit prefill helper is missing')
        harness = """const fs=require('fs'); let calls=[], sent=0;
const window={lavish:{queuePrompt:(prompt,options)=>calls.push({prompt,options}),
sendQueuedPrompts:()=>{if(calls.length!==1) throw Error('Send before queue');sent++}}};
eval(fs.readFileSync(process.argv[1],'utf8'));
if(calls.length!==1||sent!==1) throw Error('Expected one automatically sent edit');
if(!calls[0].prompt.includes('Connection verified')) throw Error('Missing edit request');
if(calls[0].options.tag!=='message'||!calls[0].options.queueKey) throw Error('Missing stable draft key');
console.log(JSON.stringify(calls[0]));"""
        result = subprocess.run(['node', '-e', harness, str(javascript)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('CODEX_THREAD_ID', result.stdout)

    def test_bare_creator_failure_closes_only_its_owned_page(self):
        with lavish() as (_origin, server, requests), fake_creator(server, 'early') as (environment, calls):
            document = json.loads(server.state.read_text())
            document['sessions']['fedcba9876543210'] = {'file': '/tmp/unrelated.html', 'status': 'open'}
            server.state.write_text(json.dumps(document))
            result = subprocess.run([sys.executable, str(SCRIPT), '--plain'], input='',
                                    env=environment, capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('creator stopped', result.stderr)
            self.assertIn('Private diagnostics', result.stderr)
            self.assertFalse(any(method == 'POST' for method, _ in requests))
            document = json.loads(server.state.read_text())
            self.assertEqual(document['sessions'][KEY]['status'], 'ended')
            self.assertEqual(document['sessions']['fedcba9876543210']['status'], 'open')
            self.assertEqual(json.loads(Path(str(calls)+'.end').read_text()),
                             ['end', document['sessions'][KEY]['file']])

    def test_bare_rejects_modified_preset_before_sending_probe(self):
        with lavish('bare') as (_origin, server, requests), fake_creator(server, 'tamper') as (environment, _calls):
            result = subprocess.run([sys.executable, str(SCRIPT), '--plain'], input='',
                                    env=environment, capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('preset', result.stderr.lower())
            self.assertNotIn('PASS', result.stdout)
            self.assertFalse(any(method == 'POST' for method, _ in requests))

    def test_bare_reaps_term_ignoring_owned_child_after_creator_exits(self):
        with lavish() as (_origin, server, _requests), fake_creator(server, 'early-child') as (environment, calls):
            child_pid = None
            try:
                result = subprocess.run([sys.executable, str(SCRIPT), '--plain'], input='',
                                        env=environment, capture_output=True, text=True, timeout=10)
                child_pid = int(Path(str(calls)+'.child').read_text())
                self.assertNotEqual(result.returncode, 0)
                proc = Path(f'/proc/{child_pid}/stat')
                self.assertTrue(not proc.exists() or proc.read_text().split()[2] == 'Z',
                                'Owned child remained running after its creator exited')
            finally:
                if child_pid:
                    try:
                        os.kill(child_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    def test_bare_cleanup_closes_page_registered_during_creator_shutdown(self):
        with lavish() as (_origin, server, requests), fake_creator(server, 'register-on-stop') as (environment, calls):
            process = subprocess.Popen([sys.executable, str(SCRIPT), '--plain'], stdin=subprocess.DEVNULL,
                                       env=environment, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                deadline = time.monotonic()+5
                while not Path(str(calls)+'.ready').exists():
                    self.assertLess(time.monotonic(), deadline)
                    time.sleep(.02)
                process.send_signal(signal.SIGINT)
                self.assertEqual(process.wait(timeout=8), 130)
                document = json.loads(server.state.read_text())
                self.assertEqual(document['sessions'][KEY]['status'], 'ended')
                self.assertFalse(any(method == 'POST' for method, _ in requests))
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()

    def test_bare_ctrl_c_after_pass_closes_page_and_reaps_creator(self):
        with lavish() as (_origin, server, _requests), fake_creator(server) as (environment, calls):
            process = subprocess.Popen([sys.executable, str(SCRIPT), '--plain'], stdin=subprocess.DEVNULL,
                                       env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output = queue.Queue()
            def collect():
                for line in process.stdout:
                    output.put(line)
            collector = threading.Thread(target=collect, daemon=True)
            collector.start()
            try:
                deadline = time.monotonic()+10
                while not output.get(timeout=max(.1, deadline-time.monotonic())).startswith('PASS:'):
                    self.assertLess(time.monotonic(), deadline)
                process.send_signal(signal.SIGINT)
                self.assertEqual(process.wait(timeout=8), 130)
                document = json.loads(server.state.read_text())
                self.assertEqual(document['sessions'][KEY]['status'], 'ended')
                pid = int(Path(str(calls)+'.pid').read_text())
                with self.assertRaises(ProcessLookupError):
                    os.kill(pid, 0)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()
                collector.join(timeout=1)
                process.stdout.close()
