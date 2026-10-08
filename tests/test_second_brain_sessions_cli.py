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

    def test_review_text_is_compact_by_default_and_details_are_opt_in(self):
        report = {"schema_version": 1, "pending_count": 0, "sessions": []}
        for extra in ([], ["--details"]):
            output = io.StringIO()
            with patch.object(cli.sessions, "review", return_value=report) as review:
                with contextlib.redirect_stdout(output):
                    result = cli.main(["sessions", "review", "--limit", "1", *extra])
            self.assertEqual(result, 0)
            review.assert_called_once_with(limit=1)
            if extra:
                self.assertIn("# Private Codex work digest", output.getvalue())
            else:
                self.assertNotIn("# Private Codex work digest", output.getvalue())
                self.assertIn("No work sessions", output.getvalue())

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


if __name__ == "__main__":
    unittest.main()
