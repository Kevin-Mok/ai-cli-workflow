"""CLI checks for calendar-based dust spending plans."""

from pathlib import Path
import subprocess
import sys
import unittest


COMMAND = Path(__file__).resolve().parents[1] / "dot_local/bin/executable_dust-budget"


def budget(*args, as_of="2026-11-25"):
    return subprocess.run(
        [sys.executable, str(COMMAND), *args, "--as-of", as_of, "--plain"],
        capture_output=True,
        text=True,
    )


class DustBudgetTest(unittest.TestCase):
    def rows(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.isascii())
        return [
            line.split() for line in result.stdout.splitlines()
            if line.startswith("2026-")
        ]

    def test_budget_distributes_whole_units_and_excludes_cutoff(self):
        result = budget("178k", "2026-12-04")
        rows = self.rows(result)
        self.assertEqual(len(rows), 9)
        self.assertEqual(rows[0], ["2026-11-25", "19,778", "158,222"])
        self.assertEqual(rows[-1], ["2026-12-03", "19,777", "0"])
        self.assertEqual(
            [row[1] for row in rows], ["19,778"] * 7 + ["19,777"] * 2
        )
        self.assertIn("End target: 0", result.stdout)

    def test_short_balance_uses_thousands_and_default_cutoff(self):
        result = budget("187")
        rows = self.rows(result)
        self.assertIn("cutoff 2026-12-04", result.stdout)
        self.assertEqual(len(rows), 9)
        self.assertEqual(rows[0], ["2026-11-25", "20,778", "166,222"])
        self.assertEqual(rows[-1], ["2026-12-03", "20,777", "0"])

    def test_exact_balance_and_cutoff_override(self):
        rows = self.rows(budget("187d", "2026-12-02", "--target", "87",
                                as_of="2026-12-01"))
        self.assertEqual(rows, [["2026-12-01", "100", "87"]])

    def test_reserve_and_one_remaining_day(self):
        rows = self.rows(budget("178,000", "2026-12-04", "--target", "25k",
                                as_of="2026-12-03"))
        self.assertEqual(rows, [["2026-12-03", "153,000", "25,000"]])

    def test_rejects_unusable_inputs(self):
        cases = [
            (("bad", "2026-12-04"), "whole dust"),
            (("178k", "2026-02-30"), "YYYY-MM-DD"),
            (("178k", "2026-12-04", "--target", "200k"), "current balance"),
            (("178k", "2026-11-25"), "no spending days"),
        ]
        for args, message in cases:
            with self.subTest(args=args):
                result = budget(*args)
                self.assertEqual(result.returncode, 2)
                self.assertIn(message, result.stderr)
                self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
