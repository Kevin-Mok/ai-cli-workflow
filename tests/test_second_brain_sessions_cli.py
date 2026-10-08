"""CLI contracts for opt-in private session review."""

import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from second_brain import cli


class SessionsCliTests(unittest.TestCase):
    def test_refresh_and_review_accept_both_formats(self):
        parser = cli.build_parser()
        for command in ("refresh", "review"):
            for format_value in ("text", "json"):
                with self.subTest(command=command, format=format_value):
                    args = parser.parse_args(["sessions", command, "--format", format_value])
                    self.assertEqual(args.sessions_command, command)
                    self.assertEqual(args.format, format_value)

    def test_bounded_refresh_and_review_limit(self):
        parser = cli.build_parser()
        for command in ("refresh", "review"):
            args = parser.parse_args(["sessions", command, "--limit", "1"])
            self.assertEqual(args.limit, 1)
            for invalid in ("0", "21", "invalid"):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        parser.parse_args(["sessions", command, "--limit", invalid])
        with patch.object(cli.sessions, "refresh", return_value={}) as refresh:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(["sessions", "refresh", "--limit", "1"]), 0)
        refresh.assert_called_once_with(limit=1)

    def test_default_and_details_use_the_same_full_prettified_report(self):
        report = {"schema_version": 1, "pending_count": 0, "sessions": []}
        outputs=[]
        for extra in ([], ["--details"]):
            output = io.StringIO()
            with patch.object(cli.sessions, "review", return_value=report) as review:
                with contextlib.redirect_stdout(output):
                    result = cli.main(["sessions", "review", "--limit", "1", *extra])
            self.assertEqual(result, 0)
            review.assert_called_once_with(limit=1)
            self.assertNotIn("# Private Codex work digest", output.getvalue())
            self.assertIn("No work sessions", output.getvalue())
            self.assertIn("Review coverage", output.getvalue())
            outputs.append(output.getvalue())
        self.assertEqual(outputs[0],outputs[1])

    def test_json_review_with_details_preserves_full_report(self):
        import json
        report = {"schema_version": 1, "sessions": [{"summary": "FULL_EVIDENCE"}]}
        output = io.StringIO()
        with patch.object(cli.sessions, "review", return_value=report):
            with contextlib.redirect_stdout(output):
                self.assertEqual(cli.main(["sessions", "review", "--details", "--format", "json"]), 0)
        self.assertEqual(json.loads(output.getvalue()), report)

    def test_review_all_conflicts_with_explicit_limit_and_budget_accepts_zero(self):
        parser=cli.build_parser()
        args=parser.parse_args(['sessions','review','--all','--refresh-limit','0'])
        self.assertTrue(args.all_sessions)
        self.assertEqual(args.refresh_limit,0)
        for options in (['--all','--limit','5'], ['--refresh-limit','-1'], ['--refresh-limit','21']):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit): parser.parse_args(['sessions','review',*options])
        with patch.object(cli.sessions,'review',return_value={'sessions':[]}) as review:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(['sessions','review','--limit','3','--refresh-limit','0']),0)
        review.assert_called_once_with(limit=3,refresh_limit=0)
        with patch.object(cli.sessions,'review',return_value={'sessions':[]}) as review:
            with contextlib.redirect_stdout(io.StringIO()): cli.main(['sessions','review','--all'])
        review.assert_called_once_with(all_sessions=True)

    def test_plain_review_ascii_and_clean_json(self):
        report={'sessions':[]}
        with patch.object(cli.sessions,'review',return_value=report):
            output=io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(cli.main(['sessions','review','--plain']),0)
            self.assertTrue(output.getvalue().isascii())
            output=io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(cli.main(['sessions','review','--plain','--format','json']),0)
            import json
            self.assertEqual(json.loads(output.getvalue()),report)

    def test_resolution_requires_stdin_payload(self):
        parser = cli.build_parser()
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parser.parse_args(["sessions", "resolve", "--payload", "private.json"])
        args = parser.parse_args(["sessions", "resolve", "--payload", "-"])
        self.assertEqual(args.payload, "-")


    def test_review_dispatches_refreshing_review_and_json_output(self):
        report = {"schema_version": 1, "pending_count": 2}
        with patch.object(cli.sessions, "review", return_value=report) as review:
            with patch.object(cli.sessions, "refresh") as refresh:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    result = cli.main(["sessions", "review", "--format", "json"])
        self.assertEqual(result, 0)
        review.assert_called_once_with()
        refresh.assert_not_called()
        self.assertIn('"pending_count":2', output.getvalue())

    def test_refresh_reports_safe_metadata_without_review_content_or_prompt(self):
        report = {
            "schema_version": 1, "model_calls": 0, "pending_count": 2,
            "backlog_count": 1, "refreshed_at": None, "coverage": {"partial": 1},
            "sessions": [{"summary": "PRIVATE_DETAIL"}], "open_checks": ["PRIVATE_CHECK"],
        }
        for format_value in ("text", "json"):
            with self.subTest(format=format_value):
                with patch.object(cli.sessions, "refresh", return_value=report) as refresh:
                    with patch.object(cli.sessions, "render", return_value="PRIVATE_DETAIL\n"):
                        output = io.StringIO()
                        with contextlib.redirect_stdout(output):
                            result = cli.main(["sessions", "refresh", "--format", format_value])
                self.assertEqual(result, 0)
                refresh.assert_called_once_with()
                self.assertNotIn("PRIVATE_DETAIL", output.getvalue())
                self.assertNotIn("PRIVATE_CHECK", output.getvalue())
                self.assertNotIn("Which outstanding", output.getvalue())
                self.assertIn("1", output.getvalue())

    def test_refresh_error_reports_safe_metadata_and_nonzero_exit(self):
        report = {"schema_version": 1, "model_calls": 1, "error": "authentication"}
        with patch.object(cli.sessions, "refresh", return_value=report):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = cli.main(["sessions", "refresh", "--format", "json"])
        self.assertEqual(result, 1)
        self.assertIn('"error":"authentication"', output.getvalue())

    def test_resolve_passes_stdin_payload_and_safe_result(self):
        payload = {"schema_version": 1, "check_id": "stable", "disposition": "checked", "confirmed": True}
        with patch.object(cli, "load_payload", return_value=payload) as load:
            with patch.object(cli.sessions, "resolve", return_value={"result": "updated"}) as resolve:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    result = cli.main(["sessions", "resolve", "--payload", "-"])
        self.assertEqual(result, 0)
        load.assert_called_once_with("-")
        resolve.assert_called_once_with(payload)
        self.assertNotIn("stable", output.getvalue())

    def test_status_text_shows_only_safe_digest_metadata(self):
        report = {
            "date": "2026-10-07", "active_projects": [],
            "inbox": {"count": 0, "path": "01 Inbox/Brain Dump.md"},
            "private_reminders": {"someday": 0, "deferred": 0, "inbox": 0},
            "private_sessions": {"pending_count": 3, "refreshed_at": None},
            "latest_daily_notes": [],
        }
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            cli._print_status_text(report)
        self.assertIn("3 pending check(s), last refresh never", output.getvalue())


class PagerTests(unittest.TestCase):
    class Terminal(io.StringIO):
        def isatty(self): return True

    def run_review(self, *options):
        report={'schema_version':1, 'pending_count':0, 'sessions':[]}
        self.output=self.Terminal()
        with patch.object(cli.sessions,'review',return_value=report), \
             patch.object(cli.sys,'stdin',self.Terminal()), \
             patch.object(cli.sys,'stdout',self.output):
            return cli.main(['sessions','review',*options])

    def test_interactive_text_review_uses_bat_with_less(self):
        with patch('shutil.which',side_effect=lambda name:'/bin/'+name if name in ('bat','less') else None), \
             patch('subprocess.run') as run:
            run.return_value.returncode=0
            self.assertEqual(self.run_review(),0)
        self.assertEqual(run.call_count,1)
        argv=run.call_args.args[0]
        self.assertEqual(argv[0],'/bin/bat')
        self.assertIn('--paging=always',argv)
        self.assertIn('--style=plain',argv)
        self.assertIn('--pager',argv)
        self.assertIn('Recent work directories',run.call_args.kwargs['input'])
        self.assertTrue(run.call_args.kwargs['text'])

    def test_json_plain_no_pager_and_non_terminal_bypass_paging(self):
        with patch('subprocess.run') as run:
            for options in (['--format','json'],['--plain'],['--no-pager']):
                self.assertEqual(self.run_review(*options),0)
            with patch.object(cli.sessions,'review',return_value={'sessions':[]}), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(['sessions','review']),0)
            run.assert_not_called()

    def test_batcat_and_less_fallback_and_no_color(self):
        import os
        for installed,expected in [({'batcat','less'},'/bin/batcat'),({'less'},'/bin/less')]:
            with self.subTest(installed=installed), \
                 patch('shutil.which',side_effect=lambda name:'/bin/'+name if name in installed else None), \
                 patch('subprocess.run') as run, patch.dict(os.environ,{'NO_COLOR':'1'}):
                run.return_value.returncode=0
                self.assertEqual(self.run_review('--details'),0)
                self.assertEqual(run.call_args.args[0][0],expected)
                self.assertIn('Review coverage',run.call_args.kwargs['input'])
                if 'batcat' in installed:self.assertIn('--color=never',run.call_args.args[0])

    def test_missing_or_failed_pager_falls_back_and_quitting_is_success(self):
        from unittest.mock import Mock
        with patch('shutil.which',return_value=None), patch('subprocess.run') as run:
            self.assertEqual(self.run_review(),0); run.assert_not_called()
            self.assertIn('Recent work directories',self.output.getvalue())
        with patch('shutil.which',return_value='/bin/bat'), patch('subprocess.run',side_effect=OSError('missing')):
            self.assertEqual(self.run_review(),0)
            self.assertIn('Recent work directories',self.output.getvalue())
        with patch('shutil.which',return_value='/bin/bat'), patch('subprocess.run',return_value=Mock(returncode=141)):
            self.assertEqual(self.run_review(),0)
            self.assertEqual(self.output.getvalue(),'')


class RefreshKeyTests(unittest.TestCase):
    def test_r_reloads_report_and_generates_pending_recaps_after_zero_preview(self):
        reports=[{'sessions':[], 'backlog_count':9}, {'sessions':[], 'backlog_count':3}]
        output=io.StringIO()
        with patch.object(cli.sessions,'review',side_effect=reports) as review, \
             patch.object(cli,'_write_review',side_effect=[True,False]) as viewer, \
             contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(['sessions','review','--limit','1','--refresh-limit','0']),0)
        self.assertEqual(review.call_args_list,[unittest.mock.call(limit=1,refresh_limit=0),
                                               unittest.mock.call(limit=1)])
        self.assertIn('9',viewer.call_args_list[0].args[0])
        self.assertIn('3',viewer.call_args_list[1].args[0])

    def test_repeated_r_preserves_all_and_positive_budget_recovers_from_failure(self):
        reports=[{'sessions':[], 'error':'quota'}, {'sessions':[], 'error':None}, {'sessions':[], 'error':None}]
        with patch.object(cli.sessions,'review',side_effect=reports) as review, \
             patch.object(cli,'_write_review',side_effect=[True,True,False]):
            self.assertEqual(cli.main(['sessions','review','--all','--refresh-limit','1']),0)
        self.assertEqual(review.call_args_list,[unittest.mock.call(all_sessions=True,refresh_limit=1)]*3)

    def test_bat_inner_pager_failure_keeps_report_readable(self):
        import shlex
        from unittest.mock import Mock
        terminal=PagerTests.Terminal()
        def failed_inner_pager(argv, **kwargs):
            pager=shlex.split(argv[argv.index('--pager')+1])
            # A wrapper status remains observable even if bat exits successfully.
            Path(pager[2]).write_text('1')
            return Mock(returncode=0)
        with patch.object(cli.sys,'stdout',terminal), patch.object(cli.sys,'stdin',terminal), \
             patch('shutil.which',side_effect=lambda name:'/bin/'+name if name in ('bat','less') else None), \
             patch('subprocess.run',side_effect=failed_inner_pager):
            self.assertFalse(cli._write_review('REPORT',plain=False,no_pager=False))
        self.assertEqual(terminal.getvalue(),'REPORT')

    def test_direct_less_r_signals_refresh_and_q_does_not(self):
        from unittest.mock import Mock
        terminal=PagerTests.Terminal()
        with patch.object(cli.sys,'stdout',terminal), patch.object(cli.sys,'stdin',terminal), \
             patch('shutil.which',side_effect=lambda name:'/bin/less' if name=='less' else None):
            with patch('subprocess.run',return_value=Mock(returncode=82)):
                self.assertTrue(cli._write_review('REPORT',plain=False,no_pager=False))
                self.assertEqual(terminal.getvalue(),'')
            with patch('subprocess.run',return_value=Mock(returncode=0)):
                self.assertFalse(cli._write_review('REPORT',plain=False,no_pager=False))

class ProgressTests(unittest.TestCase):
    def test_slow_review_reports_periodic_elapsed_time_to_stderr(self):
        import time
        output=io.StringIO()
        with contextlib.redirect_stderr(output):
            with cli._review_progress(interval=0.01,plain=True):time.sleep(0.045)
        text=output.getvalue()
        self.assertGreaterEqual(len(text.splitlines()),2)
        self.assertIn('Reviewing work sessions',text)
        self.assertIn('elapsed',text)
        self.assertTrue(text.isascii())
        count=len(text)
        time.sleep(0.025)
        self.assertEqual(len(output.getvalue()),count)

    def test_fast_review_does_not_emit_progress_noise(self):
        output=io.StringIO()
        with contextlib.redirect_stderr(output):
            with cli._review_progress(interval=10):pass
        self.assertEqual(output.getvalue(),'')


if __name__ == "__main__":
    unittest.main()
