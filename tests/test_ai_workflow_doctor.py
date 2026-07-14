#!/usr/bin/env python3

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCTOR = REPO_ROOT / "scripts" / "executable_ai-workflow-doctor"


def write_tree(root: Path, files: dict[str, str]) -> None:
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def healthy_files() -> dict[str, str]:
    return {
        "AGENTS.md": (
            "# Agent instructions\n\n"
            "Use [the canonical policy](dot_codex/AGENTS.md) and "
            "[the plan contract](.agent/PLANS.md).\n"
        ),
        "dot_codex/AGENTS.md": (
            "# Canonical instructions\n\n"
            "## Delivery\n\nUse verified evidence before completion.\n"
        ),
        ".agent/PLANS.md": "# Plan contract\n",
        "plans/ai-workflow-optimization.md": "# Active plan\n",
        "docs/ai-workflow-optimization.md": "# Optimization notes\n",
        "dot_agents/skills/README.md": (
            "# Skills\n\n- [example](example/SKILL.md): Example skill.\n"
        ),
        "dot_agents/skills/example/SKILL.md": (
            "---\nname: example\ndescription: Example fixture skill.\n---\n"
        ),
    }


class AiWorkflowDoctorTests(unittest.TestCase):
    def make_repo(
        self, overrides: dict[str, str] | None = None, remove: tuple[str, ...] = ()
    ) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        files = healthy_files()
        files.update(overrides or {})
        for relative_path in remove:
            files.pop(relative_path, None)
        write_tree(root, files)
        return directory, root

    def make_git_source(
        self, files: dict[str, str]
    ) -> tuple[tempfile.TemporaryDirectory[str], Path, str]:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        commit = self.init_git_source(root, files)
        return directory, root, commit

    @staticmethod
    def init_git_source(root: Path, files: dict[str, str]) -> str:
        write_tree(root, files)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Workflow Doctor Test",
                "-c",
                "user.email=doctor@example.invalid",
                "commit",
                "-qm",
                "fixture",
            ],
            cwd=root,
            check=True,
        )
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return commit

    def run_doctor(
        self,
        repo: Path,
        *arguments: str,
        check: bool = False,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            [sys.executable, str(DOCTOR), "--repo", str(repo), *arguments],
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
        )
        if check and completed.returncode != 0:
            self.fail(
                f"doctor exited {completed.returncode}\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )
        return completed

    def json_report(self, repo: Path, *arguments: str) -> dict:
        completed = self.run_doctor(repo, "--format", "json", *arguments, check=True)
        return json.loads(completed.stdout)

    @staticmethod
    def finding_codes(report: dict) -> list[str]:
        return [finding["code"] for finding in report["findings"]]

    def test_text_and_json_reports_share_summary_and_versioned_metrics(self) -> None:
        directory, repo = self.make_repo()
        self.addCleanup(directory.cleanup)

        text_report = self.run_doctor(repo, check=True)
        json_report = self.json_report(repo)

        self.assertIn("AI workflow doctor", text_report.stdout)
        self.assertIn("Status: pass", text_report.stdout)
        self.assertIn("Errors: 0", text_report.stdout)
        self.assertEqual(json_report["schema_version"], 1)
        self.assertEqual(
            json_report["token_estimate_method"], "ceil(unicode_characters/4)"
        )
        self.assertEqual(
            json_report["summary"],
            {"errors": 0, "status": "pass", "warnings": 0},
        )
        self.assertEqual(
            json_report["metrics"]["skills"], {"actual": 1, "catalogued": 1}
        )

    def test_composes_second_brain_findings_without_rewriting_existing_keys(
        self,
    ) -> None:
        files = healthy_files()
        files["AGENTS.md"] += "\n[missing](docs/missing.md)\n"
        directory, repo = self.make_repo(files)
        self.addCleanup(directory.cleanup)
        (repo / ".git").mkdir()
        shutil.copytree(REPO_ROOT / "second-brain", repo / "second-brain")
        learning = repo / "second-brain" / "00 Context" / "Learnings.md"
        learning.write_text(
            learning.read_text(encoding="utf-8") + "\n{{review later}}\n",
            encoding="utf-8",
        )

        report = self.json_report(repo)
        keys = {finding["key"] for finding in report["findings"]}
        self.assertIn(
            "broken_local_reference:AGENTS.md:docs/missing.md",
            keys,
        )
        self.assertIn(
            "unresolved_placeholder:00 Context/Learnings.md",
            keys,
        )

    def test_non_git_fixture_with_second_brain_skips_git_extension_safely(
        self,
    ) -> None:
        directory, repo = self.make_repo()
        self.addCleanup(directory.cleanup)
        shutil.copytree(REPO_ROOT / "second-brain", repo / "second-brain")

        completed = self.run_doctor(repo, "--format", "json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["summary"]["status"], "pass")

    def test_metrics_distinguish_utf8_bytes_characters_and_token_estimate(self) -> None:
        content = "# Café 🚀\n"
        directory, repo = self.make_repo({"AGENTS.md": content})
        self.addCleanup(directory.cleanup)

        report = self.json_report(repo)
        metric = next(
            item
            for item in report["metrics"]["instructions"]
            if item["path"] == "AGENTS.md"
        )

        self.assertEqual(metric["bytes"], len(content.encode("utf-8")))
        self.assertEqual(metric["characters"], len(content))
        self.assertGreater(metric["bytes"], metric["characters"])
        self.assertEqual(metric["estimated_tokens"], math.ceil(len(content) / 4))
        self.assertRegex(metric["sha256"], r"^[0-9a-f]{64}$")

    def test_snapshot_is_stable_and_compare_reports_deltas_and_finding_keys(self) -> None:
        directory, repo = self.make_repo()
        self.addCleanup(directory.cleanup)
        snapshot = repo / "baseline.json"

        first = self.run_doctor(
            repo, "--format", "json", "--snapshot", str(snapshot), check=True
        )
        first_bytes = snapshot.read_bytes()
        second = self.run_doctor(
            repo, "--format", "json", "--snapshot", str(snapshot), check=True
        )
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_bytes, snapshot.read_bytes())
        serialized = snapshot.read_text(encoding="utf-8")
        self.assertNotIn(str(repo), serialized)
        self.assertNotIn("timestamp", serialized.lower())

        agents = repo / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8") + "\n[missing](missing.md)\n",
            encoding="utf-8",
        )
        compared = self.json_report(repo, "--compare", str(snapshot))
        comparison = compared["comparison"]
        self.assertGreater(comparison["metric_deltas"]["active_totals.bytes"], 0)
        self.assertIn(
            "broken_local_reference:AGENTS.md:missing.md",
            comparison["added_finding_keys"],
        )
        self.assertEqual(comparison["resolved_finding_keys"], [])

        text_comparison = self.run_doctor(
            repo, "--compare", str(snapshot), check=True
        ).stdout
        self.assertIn("active_totals.bytes: +", text_comparison)
        self.assertIn(
            "Added finding keys: broken_local_reference:AGENTS.md:missing.md",
            text_comparison,
        )
        self.assertIn("Resolved finding keys: none", text_comparison)

    def test_duplicate_blocks_use_normalized_200_character_boundary(self) -> None:
        block_199 = ("alpha " * 33) + "x"
        directory, repo = self.make_repo(
            {
                "AGENTS.md": f"# Root\n\n{block_199}\n",
                "dot_codex/AGENTS.md": f"# Canonical\n\n{block_199}\n",
            }
        )
        self.addCleanup(directory.cleanup)
        self.assertNotIn(
            "duplicate_instruction_block", self.finding_codes(self.json_report(repo))
        )

        block_200 = ("alpha " * 33) + "xy"
        wrapped = block_200.replace("alpha alpha", "alpha\nalpha", 1)
        (repo / "AGENTS.md").write_text(f"# Root\n\n{block_200}\n", encoding="utf-8")
        (repo / "dot_codex/AGENTS.md").write_text(
            f"# Canonical\n\n{wrapped}\n", encoding="utf-8"
        )
        report = self.json_report(repo)
        finding = next(
            item
            for item in report["findings"]
            if item["code"] == "duplicate_instruction_block"
        )
        self.assertEqual(finding["severity"], "error")
        self.assertEqual(finding["details"]["normalized_characters"], 200)
        self.assertEqual(len(finding["locations"]), 2)

    def test_markdown_reference_checks_are_bounded_and_fence_aware(self) -> None:
        directory, repo = self.make_repo(
            {
                "AGENTS.md": (
                    "# Root\n\n"
                    "[valid](docs/My%20File.md)\n"
                    "[missing](docs/missing.md)\n"
                    "[escape](../outside.md)\n"
                    "[web](https://example.com) [anchor](#local) [home](~/notes.md)\n"
                    "[balanced](docs/foo(bar).md)\n"
                    "[reference use][reference]\n"
                    "[reference]: <docs/ref file.md>\n"
                    "~~~markdown\n[example only](docs/fenced-missing.md)\n~~~\n"
                    "````markdown\n```markdown\n"
                    "[nested example](docs/nested-fenced-missing.md)\n"
                    "```\n````\n"
                    "````markdown\n````python\n"
                    "[same-run info](docs/info-fenced-missing.md)\n"
                    "````\n"
                ),
                "docs/My File.md": "# Present\n",
                "docs/foo(bar).md": "# Present\n",
                "docs/ref file.md": "# Present\n",
            }
        )
        self.addCleanup(directory.cleanup)

        report = self.json_report(repo)
        keys = {finding["key"] for finding in report["findings"]}
        self.assertIn("broken_local_reference:AGENTS.md:docs/missing.md", keys)
        self.assertIn("reference_escapes_repo:AGENTS.md:../outside.md", keys)
        self.assertFalse(any("fenced-missing" in key for key in keys))
        self.assertFalse(any("nested-fenced-missing" in key for key in keys))
        self.assertFalse(any("info-fenced-missing" in key for key in keys))
        self.assertFalse(any("example.com" in key for key in keys))
        self.assertFalse(any("~/notes" in key for key in keys))
        self.assertFalse(any("foo(bar)" in key for key in keys))
        self.assertFalse(any("ref file" in key for key in keys))
        reported_targets = {
            finding["details"]["target"]
            for finding in report["findings"]
            if finding["code"]
            in ("broken_local_reference", "reference_escapes_repo")
        }
        self.assertEqual(reported_targets, {"docs/missing.md", "../outside.md"})

        self.assertEqual(self.run_doctor(repo).returncode, 0)
        self.assertEqual(self.run_doctor(repo, "--check").returncode, 1)

        text_report = self.run_doctor(repo).stdout
        self.assertIn("AGENTS.md:4", text_report)
        self.assertIn("target=docs/missing.md", text_report)

    def test_duplicate_skill_slugs_across_active_roots_are_reported(self) -> None:
        directory, repo = self.make_repo(
            {
                ".agents/skills/example/SKILL.md": (
                    "---\nname: example\ndescription: Duplicate fixture skill.\n---\n"
                )
            }
        )
        self.addCleanup(directory.cleanup)

        report = self.json_report(repo)
        finding = next(
            item
            for item in report["findings"]
            if item["code"] == "duplicate_active_skill_slug"
        )

        self.assertEqual(finding["severity"], "warning")
        self.assertEqual(finding["details"]["skill"], "example")
        self.assertEqual(
            {location["path"] for location in finding["locations"]},
            {
                ".agents/skills/example/SKILL.md",
                "dot_agents/skills/example/SKILL.md",
            },
        )
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(report["summary"]["warnings"], 1)

    def test_installed_skill_uses_a_cwd_independent_entrypoint(self) -> None:
        skill = (
            REPO_ROOT / "dot_agents" / "skills" / "ai-workflow-doctor" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn('"$HOME/scripts/ai-workflow-doctor" --repo <repo>', skill)
        self.assertNotIn(
            "scripts/executable_ai-workflow-doctor --repo <repo>", skill
        )

    def test_plan_contract_is_required_only_when_instructions_reference_it(self) -> None:
        directory, repo = self.make_repo(remove=(".agent/PLANS.md",))
        self.addCleanup(directory.cleanup)
        report = self.json_report(repo)
        plan_findings = [
            item for item in report["findings"] if item["code"] == "missing_plan_contract"
        ]
        self.assertEqual(len(plan_findings), 1)
        self.assertFalse(
            any(
                item["code"] == "broken_local_reference"
                and item["details"].get("target") == ".agent/PLANS.md"
                for item in report["findings"]
            )
        )

        (repo / "AGENTS.md").write_text(
            "# Agent instructions\n\nUse the canonical policy.\n", encoding="utf-8"
        )
        self.assertNotIn(
            "missing_plan_contract", self.finding_codes(self.json_report(repo))
        )

    def test_catalog_reports_uncatalogued_and_stale_entries(self) -> None:
        directory, repo = self.make_repo(
            {
                "dot_agents/skills/README.md": (
                    "# Skills\n\n"
                    "- [example](example/SKILL.md): Present.\n"
                    "- [ghost](ghost/SKILL.md): Missing.\n"
                ),
                "dot_agents/skills/new-skill/SKILL.md": (
                    "---\nname: new-skill\ndescription: New.\n---\n"
                ),
            }
        )
        self.addCleanup(directory.cleanup)
        keys = {item["key"] for item in self.json_report(repo)["findings"]}
        self.assertIn("uncatalogued_skill:new-skill", keys)
        self.assertIn("stale_catalog_entry:ghost", keys)

    def test_adaptation_sentinel_requires_valid_source_sidecar(self) -> None:
        sentinel_skill = (
            "---\nname: example\ndescription: Adapted fixture.\n---\n\n"
            "<!-- example: adapted -->\n"
        )
        directory, repo = self.make_repo(
            {"dot_agents/skills/example/SKILL.md": sentinel_skill}
        )
        self.addCleanup(directory.cleanup)
        self.assertIn(
            "missing_source_provenance", self.finding_codes(self.json_report(repo))
        )

        invalid_source = (
            "# Source\n\n"
            "- Upstream repo: /source\n"
            "- Upstream commit: abc123\n"
            "- Original source path: prompt.md\n"
            "- Adapted on: not-a-date\n"
            "- Adaptation basis: clean-room paraphrase.\n"
            "- Local adaptation: deterministic checks.\n"
        )
        write_tree(repo, {"dot_agents/skills/example/SOURCE.md": invalid_source})
        self.assertIn(
            "invalid_source_provenance", self.finding_codes(self.json_report(repo))
        )
        invalid_text = self.run_doctor(repo).stdout
        self.assertIn("invalid_fields=[date, immutable revision]", invalid_text)

        source_directory, source_repo, source_commit = self.make_git_source(
            {"prompt.md": "source material\n", "support.md": "support\n"}
        )
        self.addCleanup(source_directory.cleanup)
        valid_source = (
            invalid_source.replace("/source", str(source_repo))
            .replace("abc123", source_commit)
            .replace("not-a-date", "2026-07-13")
            .replace(
                "- Adapted on:",
                "- Supporting source paths: `support.md`\n- Adapted on:",
            )
        )
        (repo / "dot_agents/skills/example/SOURCE.md").write_text(
            valid_source, encoding="utf-8"
        )
        codes = self.finding_codes(self.json_report(repo, "--verify-sources"))
        self.assertNotIn("missing_source_provenance", codes)
        self.assertNotIn("invalid_source_provenance", codes)

        missing_support = valid_source.replace("support.md", "missing.md")
        (repo / "dot_agents/skills/example/SOURCE.md").write_text(
            missing_support, encoding="utf-8"
        )
        report = self.json_report(repo, "--verify-sources")
        invalid = next(
            finding
            for finding in report["findings"]
            if finding["code"] == "invalid_source_provenance"
        )
        self.assertIn("supporting source path at revision", invalid["details"]["invalid_fields"])

    def test_unavailable_source_archive_is_optional_and_nonblocking(self) -> None:
        source = (
            "# Source\n\n"
            "- Upstream repo: /definitely/not/available\n"
            "- Upstream commit: " + ("a" * 40) + "\n"
            "- Original source path: prompt.md\n"
            "- Adapted on: 2026-07-13\n"
            "- Adaptation basis: clean-room paraphrase.\n"
            "- Local adaptation: deterministic checks.\n"
        )
        directory, repo = self.make_repo(
            {"dot_agents/skills/example/SOURCE.md": source}
        )
        self.addCleanup(directory.cleanup)

        default_codes = self.finding_codes(self.json_report(repo))
        self.assertNotIn("invalid_source_provenance", default_codes)
        self.assertNotIn("unverifiable_source_provenance", default_codes)

        verified = self.json_report(repo, "--verify-sources")
        finding = next(
            item
            for item in verified["findings"]
            if item["code"] == "unverifiable_source_provenance"
        )
        self.assertEqual(finding["severity"], "warning")
        self.assertEqual(finding["details"]["reason"], "source repository unavailable")
        self.assertEqual(
            self.run_doctor(repo, "--verify-sources", "--check").returncode,
            0,
        )

    def test_relative_source_archive_is_resolved_from_the_audited_repo(self) -> None:
        directory, repo = self.make_repo()
        self.addCleanup(directory.cleanup)
        source_repo = repo / "source-archive"
        source_commit = self.init_git_source(
            source_repo, {"prompt.md": "source material\n"}
        )
        source = (
            "# Source\n\n"
            "- Upstream repo: source-archive\n"
            f"- Upstream commit: {source_commit}\n"
            "- Original source path: prompt.md\n"
            "- Adapted on: 2026-07-13\n"
            "- Adaptation basis: clean-room paraphrase.\n"
            "- Local adaptation: deterministic checks.\n"
        )
        write_tree(repo, {"dot_agents/skills/example/SOURCE.md": source})

        completed = self.run_doctor(
            repo,
            "--format",
            "json",
            "--verify-sources",
            check=True,
            cwd=Path(tempfile.gettempdir()),
        )
        codes = self.finding_codes(json.loads(completed.stdout))
        self.assertNotIn("invalid_source_provenance", codes)
        self.assertNotIn("unverifiable_source_provenance", codes)

    def test_legacy_source_aliases_are_validated_without_a_sentinel(self) -> None:
        legacy_source = (
            "# Source\n\n"
            "- Upstream repo: https://example.com/repo\n"
            "- Upstream commit: " + ("b" * 40) + "\n"
            "- Original source path: skill/SKILL.md\n"
            "- Imported on: 2026-07-13\n"
            "- Import basis: imported with permission.\n"
            "- Local modifications after import: metadata only.\n"
        )
        directory, repo = self.make_repo(
            {"dot_agents/skills/example/SOURCE.md": legacy_source}
        )
        self.addCleanup(directory.cleanup)
        self.assertNotIn(
            "invalid_source_provenance", self.finding_codes(self.json_report(repo))
        )
        self.assertNotIn(
            "unverifiable_source_provenance",
            self.finding_codes(self.json_report(repo, "--verify-sources")),
        )

    def test_semantic_conflicts_are_human_review_warnings_and_nonblocking(self) -> None:
        directory, repo = self.make_repo(
            {
                "AGENTS.md": "# Root\n\n## Delivery\n\nPush after each commit.\n",
                "dot_codex/AGENTS.md": (
                    "# Canonical\n\n## Delivery\n\n"
                    "Push once after the verified series.\n"
                ),
            }
        )
        self.addCleanup(directory.cleanup)
        report = self.json_report(repo)
        finding = next(
            item
            for item in report["findings"]
            if item["code"] == "semantic_conflict_candidate"
        )
        self.assertEqual(finding["severity"], "warning")
        self.assertEqual(finding["details"]["review"], "human_review_required")
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(self.run_doctor(repo, "--check").returncode, 0)

    def test_snapshot_and_compare_can_run_together(self) -> None:
        directory, repo = self.make_repo()
        self.addCleanup(directory.cleanup)
        baseline = repo / "baseline.json"
        current = repo / "current.json"
        self.run_doctor(repo, "--snapshot", str(baseline), check=True)

        agents = repo / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8") + "\nMore guidance.\n",
            encoding="utf-8",
        )
        completed = self.run_doctor(
            repo,
            "--format",
            "json",
            "--compare",
            str(baseline),
            "--snapshot",
            str(current),
            check=True,
        )
        output_report = json.loads(completed.stdout)
        snapshot_report = json.loads(current.read_text(encoding="utf-8"))
        self.assertIn("comparison", output_report)
        self.assertNotIn("comparison", snapshot_report)
        self.assertEqual(output_report["metrics"], snapshot_report["metrics"])
        self.assertGreater(
            output_report["comparison"]["metric_deltas"]["active_totals.bytes"],
            0,
        )

    def test_usage_and_snapshot_errors_exit_two_without_tracebacks(self) -> None:
        directory, repo = self.make_repo()
        self.addCleanup(directory.cleanup)

        self.assertEqual(self.run_doctor(repo, "--format", "yaml").returncode, 2)
        self.assertEqual(
            self.run_doctor(repo, "--compare", str(repo / "missing.json")).returncode,
            2,
        )

        malformed = repo / "malformed.json"
        malformed.write_text('{"schema_version": 99}\n', encoding="utf-8")
        self.assertEqual(
            self.run_doctor(repo, "--compare", str(malformed)).returncode, 2
        )

        malformed.write_text(
            '{"schema_version": 1, "metrics": {}, "findings": []}\n',
            encoding="utf-8",
        )
        completed = self.run_doctor(repo, "--compare", str(malformed))
        self.assertEqual(completed.returncode, 2)
        self.assertNotIn("Traceback", completed.stderr)

        malformed.write_text(
            '{"schema_version": 1, "metrics": {"active_totals": '
            '{"bytes": 1, "characters": 1, "estimated_tokens": 1}}, '
            '"findings": [{}]}\n',
            encoding="utf-8",
        )
        completed = self.run_doctor(repo, "--compare", str(malformed))
        self.assertEqual(completed.returncode, 2)
        self.assertNotIn("Traceback", completed.stderr)

    def test_script_is_executable(self) -> None:
        self.assertTrue(os.access(DOCTOR, os.X_OK))


if __name__ == "__main__":
    unittest.main()
