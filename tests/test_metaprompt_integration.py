#!/usr/bin/env python3
"""Packaging and reviewed-update contracts for the two metaprompt skills."""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "dot_agents/skills"
NEW = SKILLS / "metaprompt"
OLD = SKILLS / "metaprompt-alxve"
PIN = "d18b7aa8ba878354e5c348310230e652f7690f9c"
CANDIDATE = ROOT / "benchmarks/metaprompt-selection/candidates/sentry-prompt-optimizer"
NATIVE_FILES = {
    "UPSTREAM.md": "SKILL.md", "LICENSE.txt": "LICENSE",
    "SOURCES.md": "SOURCES.md", "SPEC.md": "SPEC.md",
    **{f"references/{name}.md": f"references/{name}.md" for name in
       ("core-patterns", "meta-optimization-loop", "model-family-notes", "transformed-examples")},
}


class MetapromptIntegrationTest(unittest.TestCase):
    def test_independent_names_and_invocations(self):
        for name in ("metaprompt", "metaprompt-alxve"):
            with self.subTest(name=name):
                root = SKILLS / name
                self.assertTrue((root / "SKILL.md").is_file())
                self.assertIn(f"name: {name}\n", (root / "SKILL.md").read_text())
                self.assertIn(f"${name} ", (root / "agents/openai.yaml").read_text())
        if OLD.exists():
            self.assertNotIn("Use for /metaprompt,", (OLD / "SKILL.md").read_text())

    def test_legacy_references_and_license_are_unchanged(self):
        expected = {
            "LICENSE.txt": "fb3d1cf94dbd25af40177c401761ddf55c08ea41c91b410e5ab0d1229ede8dea",
            "references/execution-routing.md": "828d0bacf3839f7dfe1b67389307a116597d050b131e94dc5cf81a195763fcfb",
            "references/examples.md": "62317639b35865f128da1de2c60b9c1f31c10d3fb9ade211b74b42dfcfad08b0",
            "references/model-profiles.md": "ea522da5314a1d90331504fbc7bd8f2fbc5c7ad9dd62ab7856d7870a714a8d3e",
            "references/compilation-rules.md": "552e00eb520686aff99d38602c3750dafc58ce4f36a6ebbeb5b469023ff86d86",
        }
        for name, digest in expected.items():
            with self.subTest(name=name):
                self.assertTrue((OLD / name).is_file())
                self.assertEqual(hashlib.sha256((OLD / name).read_bytes()).hexdigest(), digest)

    def test_imported_bytes_match_manifest(self):
        self.assertTrue((NEW / "UPSTREAM.json").is_file())
        manifest = json.loads((NEW / "UPSTREAM.json").read_text())
        self.assertEqual(manifest["repository"], "getsentry/skills")
        self.assertEqual(manifest["revision"], PIN)
        self.assertEqual(manifest["source_path"], "skills/prompt-optimizer")
        self.assertEqual(set(manifest["files"]), set(NATIVE_FILES))
        for name, record in manifest["files"].items():
            self.assertEqual(hashlib.sha256((NEW / name).read_bytes()).hexdigest(), record["sha256"], name)
            self.assertEqual((NEW / name).read_bytes(), (CANDIDATE / NATIVE_FILES[name]).read_bytes(), name)
            source = NATIVE_FILES[name]
            self.assertEqual(record["source"], source if source == "LICENSE" else "skills/prompt-optimizer/" + source)
        self.assertIn("UPSTREAM.md", manifest["files"])
        self.assertIn("LICENSE.txt", manifest["files"])

    def test_adapter_supplies_prompt_artifact_contract(self):
        content = " ".join((NEW / "SKILL.md").read_text().split())
        for requirement in ("UPSTREAM.md", "prompt-authoring", "prompts/", "collision",
                            "compiled prompt only", "separate request", "{{variables}}",
                            "Sentry", "eight", "Optimized Prompt", "Saved:",
                            "prepared", "executed"):
            self.assertIn(requirement, content)

    def test_no_retired_resources_remain_in_active_package(self):
        expected = set(NATIVE_FILES) | {
            "SKILL.md", "SOURCE.md", "UPSTREAM.json", "agents/openai.yaml", "scripts/update_upstream.py"
        }
        actual = {str(p.relative_to(NEW)) for p in NEW.rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
        self.assertEqual(actual, expected)


class UpstreamUpdateTest(unittest.TestCase):
    def setUp(self):
        path = NEW / "scripts/update_upstream.py"
        self.assertTrue(path.is_file(), "reviewed update helper is missing")
        spec = importlib.util.spec_from_file_location("metaprompt_update", path)
        self.helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.helper)

    def test_stage_pins_sources_without_touching_existing_destination(self):
        tree = {"truncated": False, "tree": [
            {"path": "skills/prompt-optimizer/SKILL.md", "type": "blob", "mode": "100644"},
            {"path": "skills/prompt-optimizer/SOURCES.md", "type": "blob", "mode": "100644"},
            {"path": "skills/prompt-optimizer/SPEC.md", "type": "blob", "mode": "100644"},
            {"path": "skills/prompt-optimizer/references/core-patterns.md", "type": "blob", "mode": "100644"},
            {"path": "LICENSE", "type": "blob", "mode": "100644"},
        ]}
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / "candidate"
            with patch.object(self.helper, "fetch_json", return_value=tree), patch.object(
                self.helper, "fetch_bytes", return_value=b"upstream bytes\n"
            ) as fetch:
                self.helper.stage_candidate(dest, PIN)
                self.assertEqual((dest / "UPSTREAM.md").read_bytes(), b"upstream bytes\n")
                self.assertTrue((dest / "SOURCES.md").is_file())
                self.assertTrue((dest / "SPEC.md").is_file())
                self.assertTrue((dest / "references/core-patterns.md").is_file())
                self.assertFalse((dest / "SKILL.md").exists())
                manifest = json.loads((dest / "UPSTREAM.json").read_text())
                self.assertEqual(manifest["revision"], PIN)
                self.assertEqual(manifest["repository"], "getsentry/skills")
                self.assertEqual(manifest["source_path"], "skills/prompt-optimizer")
                self.assertTrue(all(PIN in call.args[0] for call in fetch.call_args_list))
                self.assertTrue(all("getsentry/skills/" in call.args[0] for call in fetch.call_args_list))
                with self.assertRaises(FileExistsError):
                    self.helper.stage_candidate(dest, PIN)

    def test_rejects_unpinned_revision(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                self.helper.stage_candidate(Path(temp) / "candidate", "main")

    def test_rejects_paths_escaping_skill_and_symlinks(self):
        for path, mode in (("skills/prompt-optimizer/../../escape", "100644"),
                           ("skills/prompt-optimizer/link", "120000")):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as temp:
                tree = {"truncated": False, "tree": [{"path": path, "type": "blob", "mode": mode}]}
                with patch.object(self.helper, "fetch_json", return_value=tree):
                    with self.assertRaises(ValueError):
                        self.helper.stage_candidate(Path(temp) / "candidate", PIN)
                self.assertEqual(list(Path(temp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
