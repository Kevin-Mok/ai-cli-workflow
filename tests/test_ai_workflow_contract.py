#!/usr/bin/env python3

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_ACTIVE_INSTRUCTION_BYTES = 34_805
MAX_ACTIVE_INSTRUCTION_BYTES = int(BASELINE_ACTIVE_INSTRUCTION_BYTES * 0.70)
PUSH_POLICY = (
    "Single-commit workflows push after the commit passes verification; "
    "multi-commit workflows push once after the complete verified series, "
    "unless the user explicitly requests another cadence."
)


def read_repo_file(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class AIWorkflowContractTest(unittest.TestCase):
    def test_execplan_contract_is_decision_complete(self) -> None:
        contract_path = REPO_ROOT / ".agent/PLANS.md"
        self.assertTrue(contract_path.is_file(), ".agent/PLANS.md must exist")

        contract = contract_path.read_text(encoding="utf-8").lower()
        for required_text in (
            "decision-complete",
            "- [ ]",
            "## assumptions",
            "## verification evidence",
            "## review notes",
            "same commit",
        ):
            self.assertIn(required_text, contract)

    def test_root_instruction_files_are_compact_routing_layers(self) -> None:
        root_agents = read_repo_file("AGENTS.md")
        base_agents = read_repo_file("AGENTS-BASE.md")
        repo_agents = read_repo_file("AGENTS.repo.md")
        canonical = read_repo_file("dot_codex/AGENTS.md")

        self.assertLessEqual(len(root_agents), 1_200)
        self.assertLessEqual(len(base_agents), 900)
        self.assertLessEqual(len(repo_agents), 1_200)
        for routing_layer in (root_agents, base_agents, repo_agents):
            self.assertIn("dot_codex/AGENTS.md", routing_layer)
            for duplicated_heading in (
                "## 0) Prime Directive",
                "## 1) Workflow Orchestration",
                "## 2) Task Management",
                "## 3) Problem-Solving Approach",
                "## 4) Workflow Principles",
                "## 5) Code Principles",
                "## 6) PR Checklist",
                '## 7) What "Done" Looks Like',
                "## 8) Communication Standards",
                "## 9) Failure Modes to Avoid",
                "## 10) Local Override Mechanism",
            ):
                self.assertNotIn(duplicated_heading, routing_layer)

        self.assertIn("canonical Codex instruction", canonical)
        active_instruction_bytes = len((root_agents + canonical).encode("utf-8"))
        self.assertLessEqual(active_instruction_bytes, MAX_ACTIVE_INSTRUCTION_BYTES)

    def test_active_plan_satisfies_execplan_contract(self) -> None:
        plan = read_repo_file("plans/ai-workflow-optimization.md")
        for required_section in (
            "## Current Context And Scope",
            "## Assumptions",
            "## Risks, Edge Cases, And Rollback",
            "## Verification Evidence",
            "## Review Notes",
        ):
            self.assertIn(required_section, plan)

        for required_evidence in (
            "Command: `python3 tests/test_ai_workflow_contract.py`",
            "Expected:",
            "Observed:",
            "Exit status:",
            "`wc -c AGENTS.md dot_codex/AGENTS.md`",
            "`sha256sum dot_agents/skills/metaprompt/SKILL.md`",
            "`./scripts/executable_readme-recruiter-sync`",
            "dot_agents/skills/commit-dirty/agents/openai.yaml",
            "dot_agents/skills/commit-session/agents/openai.yaml",
            "Implement the minimal standard-library CLI to pass the tests. Semantic",
        ):
            self.assertIn(required_evidence, plan)

        manual_heading = "### Task 1 Manual Verification"
        self.assertIn(manual_heading, plan)
        manual_evidence = plan.split(manual_heading, 1)[1].split("\n## ", 1)[0]
        for required_label in (
            "Manual action:",
            "Expected:",
            "Observed:",
            "Status:",
        ):
            self.assertIn(required_label, manual_evidence)

    def test_canonical_policy_preserves_required_boundaries(self) -> None:
        canonical = read_repo_file("dot_codex/AGENTS.md").lower()
        for required_text in (
            "failing test or executable reproducer",
            "fails for the expected reason",
            "small, safe, reversible",
            "same change",
            "readme-recruiter-sync",
            "docs/smoke-tests.md",
            "refresh-config",
            "unless the user explicitly asks for one",
            "feedback.log",
            "append-only",
            "tasks/lessons.md",
            "verification",
        ):
            self.assertIn(required_text, canonical)

    def test_system_design_routing_is_explicit(self) -> None:
        canonical = read_repo_file("dot_codex/AGENTS.md").lower()
        for reference_name in (
            "architecture.md",
            "coding-standards.md",
            "ui-design.md",
            "knowledge-base.md",
            "student-practice-packages.md",
            "trusted-sources.md",
            "business-strategy.md",
        ):
            self.assertIn(
                f"~/.agents/system-design/{reference_name}", canonical
            )

        self.assertIn(
            "`~/.agents/system-design/coding-standards.md` before implementing",
            canonical,
        )
        self.assertIn(
            "`~/.agents/system-design/ui-design.md` before all ui work",
            canonical,
        )

    def test_readme_invariants_live_in_the_lazy_contract(self) -> None:
        contract = read_repo_file(
            "dot_agents/skills/readme-recruiter-sync/references/readme-contract.md"
        ).lower()
        for required_text in (
            "hero workflow image",
            "table of contents",
            "single terminal `license` section",
            "representative examples from every skill category",
            "inline relative links",
            "how the underlying tool is obtained",
        ):
            self.assertIn(required_text, contract)

    def test_smoke_docs_cover_instruction_sync_without_implying_a_push(self) -> None:
        smoke_tests = read_repo_file("docs/smoke-tests.md").lower()
        self.assertIn("standing workflow rule", smoke_tests)
        self.assertIn(
            "explains that a verified single-commit workflow", smoke_tests
        )

    def test_instruction_size_metrics_are_labeled_as_bytes(self) -> None:
        optimization_doc = read_repo_file("docs/ai-workflow-optimization.md")
        active_plan = read_repo_file("plans/ai-workflow-optimization.md")
        self.assertIn("| File | Bytes |", optimization_doc)
        self.assertIn(
            "Combined `AGENTS.md` and `dot_codex/AGENTS.md` bytes", active_plan
        )
        for stale_label in (
            "| File | Characters |",
            "active instruction characters",
            "34,805-character baseline",
        ):
            self.assertNotIn(stale_label, optimization_doc)
            self.assertNotIn(stale_label, active_plan)

    def test_push_policy_is_consistent_in_active_workflows(self) -> None:
        policy_files = (
            "dot_codex/AGENTS.md",
            "dot_agents/skills/commit-dirty/SKILL.md",
            "dot_agents/skills/commit-dirty/agents/openai.yaml",
            "dot_agents/skills/commit-plan/SKILL.md",
            "dot_agents/skills/commit-session/SKILL.md",
            "dot_agents/skills/commit-session/agents/openai.yaml",
        )
        for relative_path in policy_files:
            self.assertIn(PUSH_POLICY, read_repo_file(relative_path), relative_path)

        active_workflow_files = policy_files + (
            "AGENTS.md",
            "AGENTS.repo.md",
            "AGENTS-BASE.md",
            "dot_agents/skills/README.md",
            "dot_agents/skills/commit-plan/agents/openai.yaml",
            "tasks/lessons.md",
        )
        banned_fragments = (
            "push immediately after each successful",
            "push immediately after the successful",
            "after each successful commit by default",
            "each successful commit will be pushed",
            "each successful commit is followed by a push",
        )
        for relative_path in active_workflow_files:
            content = read_repo_file(relative_path).lower()
            for banned_fragment in banned_fragments:
                self.assertNotIn(banned_fragment, content, relative_path)

    def test_delivery_preference_lives_only_in_feedback_log(self) -> None:
        latest_feedback = read_repo_file(
            "dot_agents/skills/feedback-memory/feedback.log"
        ).splitlines()[-1]
        self.assertEqual(
            latest_feedback,
            "2026-07-13 - Single-commit workflows push after the commit passes "
            "verification; multi-commit workflows push once after the complete "
            "verified series, unless I explicitly request another cadence.",
        )

        lessons = read_repo_file("tasks/lessons.md")
        self.assertNotIn(PUSH_POLICY, lessons)
        self.assertIn(
            "Apply the newest delivery-cadence preference from the canonical "
            "feedback log.",
            lessons,
        )

    def test_optimization_doc_records_the_audited_baseline(self) -> None:
        doc_path = REPO_ROOT / "docs/ai-workflow-optimization.md"
        self.assertTrue(doc_path.is_file(), "optimization provenance doc must exist")

        document = doc_path.read_text(encoding="utf-8")
        for required_text in (
            "34,805",
            "12 duplicated top-level blocks",
            "5c86715f453f0eca188451a48bf5b165831d8b29",
            "8e5f9534182212e77a4607c74afd22aab4ceb05a4a740a02ce0c91f5ea86b94a",
        ):
            self.assertIn(required_text, document)


if __name__ == "__main__":
    unittest.main()
