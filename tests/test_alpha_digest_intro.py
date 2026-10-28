import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = REPO_ROOT / "prompts" / "alpha-digest-6h-intro.md"


class AlphaDigestIntroTest(unittest.TestCase):
    def test_intro_exists_with_required_sections(self) -> None:
        self.assertTrue(PROMPT_PATH.is_file(), "missing alpha digest intro")
        content = PROMPT_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.strip(), "empty alpha digest intro")
        for marker in (
            "Collect.",
            "Filter.",
            "Admission filter",
            "Report.",
            "open a PR for",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)


if __name__ == "__main__":
    unittest.main()
