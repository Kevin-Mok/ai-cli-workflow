"""Exercise existing-page challenge delivery and connection validation."""
import subprocess
import sys
import time
import unittest

from lavish_connection_fixtures import SCRIPT, KEY, THREAD, lavish


class ConnectionProtocolTest(unittest.TestCase):
    def run_cli(self, url, *args):
        return subprocess.run([sys.executable, str(SCRIPT), url, '--expect-thread', THREAD,
                               '--timeout', '.4', *args], capture_output=True, text=True, timeout=5)


    def test_missing_expected_thread_is_prompted_without_changing_explicit_url(self):
        with lavish() as (origin, _server, _requests):
            result = subprocess.run([sys.executable, str(SCRIPT), f'{origin}/session/{KEY}'],
                                    input=THREAD+'\n', capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('PASS', result.stdout)
            self.assertNotIn('URL:', result.stdout)

    def test_guided_eof_is_actionable_without_submission_or_traceback(self):
        with lavish() as (_origin, _server, requests):
            result = subprocess.run([sys.executable, str(SCRIPT), '--expect-thread', THREAD], input='',
                                    capture_output=True, text=True, timeout=5)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('input', result.stderr.lower())
            self.assertNotIn('Traceback', result.stderr)
            self.assertFalse(any(method == 'POST' for method, _ in requests))

    def test_guided_blank_values_do_not_submit(self):
        with lavish() as (origin, _server, requests):
            cases = [(['--expect-thread', THREAD], '\n'),
                     ([f'{origin}/session/{KEY}'], '\n')]
            for flags, answers in cases:
                with self.subTest(flags=flags):
                    result = subprocess.run([sys.executable, str(SCRIPT), *flags], input=answers,
                                            capture_output=True, text=True, timeout=5)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn('Traceback', result.stderr)
                    self.assertFalse(any(method == 'POST' for method, _ in requests))

    def test_fresh_delivered_echo_from_expected_thread_passes(self):
        with lavish() as (origin, server, requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('PASS', result.stdout)
            self.assertIn(THREAD, result.stdout)
            self.assertNotIn(THREAD, server.submitted['prompts'][0]['prompt'])
            self.assertEqual(server.origin, origin)
            self.assertEqual([path for method, path in requests if method == 'POST'], [f'/api/{KEY}/prompts'])
            self.assertFalse(any('poll' in path for _, path in requests))

    def test_stored_public_url_alias_does_not_break_local_connection(self):
        with lavish('alias') as (origin, _server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_transient_partial_state_write_is_retried(self):
        with lavish('partial') as (origin, _server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_slow_health_body_cannot_pass_after_deadline(self):
        with lavish('late') as (origin, _server, _requests):
            started = time.monotonic()
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('timed out', result.stderr.lower())
            self.assertLess(time.monotonic()-started, 1.5)

    def test_ack_line_with_separate_greeting_passes(self):
        with lavish('greeting') as (origin, _server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_queued_feedback_status_waits_for_delivery(self):
        with lavish('queued') as (origin, _server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}', '--timeout', '1.5')
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_normal_processing_gap_waits_for_listener_to_resume(self):
        with lavish('reconnect') as (origin, server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}', '--timeout', '1.5')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertGreaterEqual(server.wait_health, 3)

    def test_ack_without_resumed_listener_does_not_claim_connected(self):
        with lavish('never-reconnect') as (origin, _server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('timed out', result.stderr.lower())

    def test_no_listener_fails_before_sending_a_message(self):
        with lavish('disconnected') as (origin, _server, requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('listener', result.stderr.lower())
            self.assertFalse(any(method == 'POST' for method, _ in requests))

    def test_wrong_thread_echo_fails(self):
        with lavish('wrong') as (origin, _server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('wrong', result.stderr.lower())

    def test_old_nonce_cannot_pass(self):
        with lavish('stale') as (origin, _server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('timed out', result.stderr.lower())

    def test_undelivered_question_cannot_pass_even_with_an_echo(self):
        with lavish('undelivered') as (origin, _server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('timed out', result.stderr.lower())

    def test_ended_session_fails_without_sending(self):
        with lavish('ended') as (origin, _server, requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('open', result.stderr.lower())
            self.assertFalse(any(method == 'POST' for method, _ in requests))

    def test_malformed_health_fails_without_sending(self):
        with lavish('malformed') as (origin, _server, requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('invalid', result.stderr.lower())
            self.assertFalse(any(method == 'POST' for method, _ in requests))

    def test_timeout_is_bounded_and_shows_progress_in_plain_mode(self):
        with lavish('timeout') as (origin, _server, _requests):
            result = self.run_cli(f'{origin}/session/{KEY}', '--timeout', '1.2', '--plain')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Waiting', result.stderr)
            self.assertIn('elapsed', result.stderr)
            self.assertTrue(result.stderr.isascii())

    def test_malformed_persisted_url_fails_without_traceback_or_submission(self):
        with lavish('bad-url') as (origin, _server, requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('Traceback', result.stderr)
            self.assertFalse(any(method == 'POST' for method, _ in requests))

    def test_live_state_identity_mismatch_cannot_pass(self):
        with lavish('state-mismatch') as (origin, _server, requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('identity', result.stderr.lower())
            self.assertFalse(any(method == 'POST' for method, _ in requests))

    def test_redirect_is_rejected_without_sending(self):
        with lavish('redirect') as (origin, _server, requests):
            result = self.run_cli(f'{origin}/session/{KEY}')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('redirect', result.stderr.lower())
            self.assertEqual(requests, [('GET', '/health')])

    def test_dead_server_fails_without_traceback(self):
        with lavish() as (origin, _server, _requests):
            url = f'{origin}/session/{KEY}'
        result = self.run_cli(url)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('live Lavish server', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_rejects_nonlocal_url_and_invalid_timeout(self):
        for url, args in [('https://example.com/session/'+KEY, []),
                          ('http://127.0.0.1:4387/session/'+KEY, ['--timeout', 'nan']),
                          ('http://127.0.0.1:4387/session/'+KEY, ['--timeout', '0'])]:
            with self.subTest(url=url, args=args):
                result = self.run_cli(url, *args)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
