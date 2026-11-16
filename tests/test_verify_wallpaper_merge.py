"""Regression tests for the read-only wallpaper merge verifier."""

from __future__ import annotations

import colorsys
from itertools import combinations
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import pywal


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "scripts" / "executable_verify-wallpaper-merge"
SUPPORTED = ("jpg", "jpeg", "png", "webp", "bmp", "gif", "tif", "tiff", "xcf", "ppm")


def contrast_ratio(first: str, second: str) -> float:
    def luminance(color: str) -> float:
        channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
                  for channel in channels]
        return sum(channel * weight for channel, weight in zip(linear, (0.2126, 0.7152, 0.0722)))

    low, high = sorted((luminance(first), luminance(second)))
    return (high + 0.05) / (low + 0.05)


def oklab(color: str) -> tuple[float, float, float]:
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    red, green, blue = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
                        for value in channels]
    l = (0.4122214708 * red + 0.5363325363 * green + 0.0514459929 * blue) ** (1 / 3)
    m = (0.2119034982 * red + 0.6806995451 * green + 0.1073969566 * blue) ** (1 / 3)
    s = (0.0883024619 * red + 0.2817188376 * green + 0.6299787005 * blue) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklab_distance(first: str, second: str) -> float:
    return sum((a - b) ** 2 for a, b in zip(oklab(first), oklab(second))) ** 0.5


def palette(background: str, text: str) -> dict:
    return {
        "special": {"background": background, "foreground": text, "cursor": text},
        "colors": {f"color{index}": text for index in range(16)},
    }


class WallpaperMergeVerifierTest(unittest.TestCase):
    def load_verifier(self):
        self.assertTrue(VERIFIER.is_file(), f"missing verifier script: {VERIFIER}")
        return runpy.run_path(str(VERIFIER))

    def make_root(self, base: Path) -> Path:
        root = base / "Backgrounds"
        for theme in ("bright", "dim"):
            (root / theme / "non-editing").mkdir(parents=True)
            (root / theme / "editing").mkdir(parents=True)
        return root

    def image(self, path: Path, data: bytes = b"image") -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_scan_covers_all_background_directories_and_skips_non_image_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(Path(temporary))
            expected = []
            for theme in ("bright", "dim"):
                source = root / theme / "non-editing"
                (source / "shuffle.txt").write_text("preserve this order\n")
                for extension in SUPPORTED:
                    expected.append(self.image(source / "nested" / f"sample.{extension}"))
            expected.extend([
                self.image(root / "bright/editing/4k/photo.jpeg"),
                self.image(root / "bright/editing/calvin-hobbes/strip.xcf"),
                self.image(root / "bright/editing/root/portrait.png"),
                self.image(root / "dim/editing/4k/wallpaper.webp"),
                self.image(root / "dim/editing/calvin-hobbes/cast.bmp"),
                self.image(root / "dim/editing/root/scene.gif"),
                self.image(root / "root-level.png"),
                self.image(root / "bright/editing/4k/extensionless", b"\xff\xd8\xffjpeg-signature"),
                self.image(root / "dim/editing/root/photo.jpg.1", b"\xff\xd8\xffjpeg-signature"),
            ])
            self.image(root / ".git/objects/ignored.png")
            self.image(root / "bright/editing/.git/nested/ignored.png")
            (root / "scripts").mkdir()
            (root / "scripts/helper.py").write_text("preserve repository metadata")
            (root / "bright/editing/README.txt").write_text("editing notes are metadata")
            (root / "dim/editing/partial.jpg.crdownload").write_bytes(b"\xff\xd8\xffincomplete download")

            images, collisions, skipped_metadata, failures = self.load_verifier()["scan"](root)

            self.assertEqual(set(images), set(expected))
            self.assertEqual(collisions, [])
            self.assertEqual(set(skipped_metadata), {
                root / "bright/non-editing/shuffle.txt",
                root / "dim/non-editing/shuffle.txt",
                root / "bright/editing/README.txt",
                root / "scripts/helper.py",
                root / "dim/editing/partial.jpg.crdownload",
            })
            self.assertEqual(failures, [])
            self.assertEqual((root / "bright/non-editing/shuffle.txt").read_text(), "preserve this order\n")
            self.assertFalse(any(".git" in str(path) for path in images))
            self.assertEqual((root / "scripts/helper.py").read_text(), "preserve repository metadata")

    def test_scan_picks_up_future_images_on_the_next_recursive_scan(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(Path(temporary))
            first_image = self.image(root / "bright/non-editing/current.jpg")
            scan = self.load_verifier()["scan"]

            first = scan(root)[0]
            future_image = self.image(root / "dim/editing/4k/calvin-hobbes/root/new-future.png")
            second = scan(root)[0]

            self.assertEqual(set(first), {first_image})
            self.assertEqual(set(second), {first_image, future_image})

    def test_scan_records_traversal_errors_from_unreadable_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(Path(temporary))
            unreadable = root / "scripts/private"
            unreadable.mkdir(parents=True)
            real_walk = os.walk
            verifier = self.load_verifier()

            def walk_with_error(top, *, followlinks=False, onerror=None):
                if onerror is not None:
                    onerror(PermissionError(13, "Permission denied", str(unreadable)))
                yield from real_walk(top, followlinks=followlinks)

            with mock.patch.object(verifier["os"], "walk", side_effect=walk_with_error):
                _, _, _, failures = verifier["scan"](root)

            self.assertTrue(any(str(unreadable) in str(failure) for failure in failures))

    def test_cli_rejects_fifo_without_blocking_while_reading_image_header(self):
        self.assertTrue(VERIFIER.is_file(), f"missing verifier script: {VERIFIER}")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = self.make_root(base)
            fifo = root / "scripts" / "untrusted-image"
            fifo.parent.mkdir()
            os.mkfifo(fifo)
            report_path = base / "report.json"

            try:
                result = subprocess.run(
                    [sys.executable, str(VERIFIER), "--root", str(root), "--report", str(report_path), "--plain"],
                    capture_output=True, text=True, check=False, timeout=2,
                    env={**os.environ, "HOME": str(base / "home"),
                         "PYTHONPATH": str(Path(pywal.__file__).parent.parent)},
                )
            except subprocess.TimeoutExpired:
                self.fail("verifier blocked while reading a FIFO as an image")

            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            report = json.loads(report_path.read_text())
            self.assertFalse(report["safe_to_merge"])
            self.assertTrue(any(str(fifo) in str(item) for item in report["skipped_metadata"] + report["failures"]))

    def test_scan_blocks_unknown_files_and_symlinks_without_following_them(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(Path(temporary))
            outside = Path(temporary) / "outside.png"
            self.image(outside)
            self.image(root / "bright/non-editing/valid.png")
            (root / "bright/non-editing/notes.txt").write_text("not shuffle metadata")
            (root / "dim/non-editing/linked.png").symlink_to(outside)

            images, collisions, skipped_metadata, failures = self.load_verifier()["scan"](root)

            self.assertTrue(any("notes.txt" in str(failure) for failure in failures))
            self.assertTrue(any("linked.png" in str(item) for item in collisions + failures))
            self.assertFalse(any(Path(image).name == "outside.png" for image in images))
            self.assertEqual(skipped_metadata, [root / "bright/non-editing/notes.txt"])

    def test_scan_blocks_exact_and_directory_ancestor_destination_collisions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(Path(temporary))
            source = self.image(root / "bright/non-editing/same.jpg", b"same bytes")
            self.image(root / "bright/editing/same.jpg", b"same bytes")
            self.image(root / "dim/non-editing/nested/photo.png")
            (root / "dim/editing/nested").write_text("blocks destination directory")

            _, collisions, _, _ = self.load_verifier()["scan"](root)

            self.assertGreaterEqual(len(collisions), 2)
            collision_text = json.dumps(collisions)
            self.assertIn(str(source), collision_text)
            self.assertIn("same.jpg", collision_text)
            self.assertIn("nested", collision_text)
            for item in collisions:
                self.assertTrue({"source", "destination", "reason"}.issubset(item))

    def test_scan_fails_when_categories_are_missing_or_no_images_exist(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "Backgrounds"
            root.mkdir()
            _, _, _, missing_failures = self.load_verifier()["scan"](root)
            self.assertTrue(missing_failures)

            empty = self.make_root(Path(temporary) / "empty")
            _, _, _, empty_failures = self.load_verifier()["scan"](empty)
            self.assertTrue(empty_failures)

    def test_palette_validation_checks_each_ansi_and_special_text_slot(self):
        validate_palette = self.load_verifier()["validate_palette"]
        report = validate_palette(palette("#050412", "#dddddd"))

        self.assertGreaterEqual(report["minimum_contrast"], 4.5)
        self.assertEqual(report["unsafe_slots"], [])
        self.assertIn("per_slot", report)
        self.assertEqual(len(report["per_slot"]), 18)
        for measured in report["per_slot"]:
            self.assertIn("slot", measured)
            self.assertIn("color", measured)
            required = 7 if measured["slot"] in ("color7", "foreground", "cursor") else 4.5
            self.assertEqual(measured["required_contrast"], required)
            self.assertGreaterEqual(measured["minimum_contrast"], required)
            self.assertTrue(measured["passed"])
            self.assertEqual(len(measured["measurements"]), 3)
            for sample in measured["measurements"]:
                self.assertAlmostEqual(sample["contrast"], contrast_ratio(measured["color"], sample["background"]))

    def test_palette_validation_reports_unsafe_slots_against_opaque_and_translucent_bounds(self):
        validate_palette = self.load_verifier()["validate_palette"]
        report = validate_palette(palette("#050412", "#1626c7"))

        slots = {item["slot"] for item in report["unsafe_slots"]}
        self.assertEqual(slots, {*(f"color{index}" for index in range(16)), "foreground", "cursor"})
        self.assertLess(report["minimum_contrast"], 4.5)
        self.assertTrue(all(item["contrast"] < 4.5 for item in report["unsafe_slots"]))

    def test_palette_validation_handles_light_side_contrast_at_supported_upper_background(self):
        validate_palette = self.load_verifier()["validate_palette"]
        report = validate_palette(palette("#666666", "#010101"))

        self.assertLess(report["minimum_contrast"], 4.5)
        self.assertEqual(len(report["unsafe_slots"]), 18)

    def test_palette_validation_accepts_light_text_on_supported_upper_background(self):
        validate_palette = self.load_verifier()["validate_palette"]
        report = validate_palette(palette("#666666", "#ffffff"))

        self.assertEqual({item["slot"] for item in report["unsafe_slots"]}, {"color7", "foreground", "cursor"})
        self.assertLess(report["minimum_contrast"], 7)

    def test_colorfulness_validation_rejects_neon_and_collapsed_pairs(self):
        validate = self.load_verifier()['validate_colorfulness']
        helper = runpy.run_path(str(ROOT / 'scripts/executable_pywal-readable'))
        source = palette('#050412', '#dddddd')
        helper['repair_palette'](source)
        report = validate(source)
        self.assertTrue(report['passed'], report)
        self.assertLessEqual(report['maximum_chroma'], .105)
        self.assertEqual(report['distinct_colors'], 12)
        independent = min(oklab_distance(a, b) for a, b in combinations(
            [source['colors'][f'color{i}'] for i in (*range(1,7), *range(9,15))], 2))
        self.assertAlmostEqual(report['minimum_oklab_distance'], independent, places=5)
        source['colors']['color1'] = '#FF0000'
        self.assertFalse(validate(source)['passed'])
        source['colors'] = {f'color{i}': '#a0a0a0' for i in range(16)}
        self.assertFalse(validate(source)['passed'])

    def test_background_validation_allows_only_necessary_supported_safe_darkening(self):
        check_background = self.load_verifier()["check_background"]
        preserved = check_background("#050412", "#050412")
        self.assertTrue(preserved["passed"])
        self.assertTrue(preserved["preserved"])
        self.assertFalse(preserved["adjusted"])

        self.assertFalse(check_background("#666666", "#666666")["passed"])
        upper_normalized = check_background("#666666", "#000000")
        self.assertTrue(upper_normalized["passed"])
        self.assertTrue(upper_normalized["adjusted"])

        original = "#11820f"
        accepted = check_background(original, "#000000")
        self.assertTrue(accepted["passed"])
        self.assertFalse(accepted["preserved"])
        self.assertTrue(accepted["adjusted"])
        self.assertIn("reason", accepted)
        self.assertLess(accepted["original_white_bound_contrast"], 7.0)
        self.assertGreaterEqual(accepted["corrected_white_bound_contrast"], 7.0)

        self.assertFalse(check_background(original, "#ffffff")["passed"])
        self.assertFalse(check_background("#050412", "#000000")["passed"])

    def test_cli_checks_real_ppm_palettes_in_isolated_cache(self):
        self.assertTrue(VERIFIER.is_file(), f"missing verifier script: {VERIFIER}")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = self.make_root(base)
            colors = [(red, green, blue)
                      for red in (0, 85, 170, 255)
                      for green in (0, 85, 170, 255)
                      for blue in (0, 85, 170, 255)]

            def write_pattern(path: Path) -> None:
                import random
                chooser = random.Random(42)
                pixels = [chooser.choice(colors) for _ in range(160 * 160)]
                body = " ".join(str(channel) for pixel in pixels for channel in pixel)
                path.write_text(f"P3\n160 160\n255\n{body}\n")

            write_pattern(root / "bright/non-editing/pattern.ppm")
            write_pattern(root / "dim/non-editing/pattern.ppm")
            (root / "bright/non-editing/shuffle.txt").write_text("preserve sequence\n")
            report_path = base / "report.json"
            isolated_home = base / "home"
            active_cache = base / "fake-live-cache"
            active_cache.mkdir()
            sentinel = active_cache / "colors.json"
            sentinel.write_text("preserve live active palette\n")
            active_cache_before = sentinel.read_bytes()

            result = subprocess.run(
                [sys.executable, str(VERIFIER), "--root", str(root), "--report", str(report_path), "--plain"],
                capture_output=True, text=True, check=False,
                env={**os.environ, "HOME": str(isolated_home),
                     "XDG_CACHE_HOME": str(isolated_home / ".cache"),
                     "XDG_CONFIG_HOME": str(isolated_home / ".config"),
                     "PYWAL_CACHE_DIR": str(active_cache),
                     "PYTHONPATH": str(Path(pywal.__file__).parent.parent)},
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            report = json.loads(report_path.read_text())
            self.assertTrue(report["safe_to_merge"])
            self.assertEqual(report["checked"], 2)
            self.assertEqual(report["passed"], 2)
            self.assertEqual(report["failures"], [])
            self.assertEqual(report["collisions"], [])
            self.assertEqual(len(report["results"]), 2)
            self.assertEqual((root / "bright/non-editing/shuffle.txt").read_text(), "preserve sequence\n")
            self.assertFalse((root / "bright/editing/pattern.ppm").exists())
            self.assertEqual(sentinel.read_bytes(), active_cache_before)

    def test_cli_reports_blocked_collision_and_preserves_metadata(self):
        self.assertTrue(VERIFIER.is_file(), f"missing verifier script: {VERIFIER}")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = self.make_root(base)
            source = self.image(root / "bright/non-editing/sample.png")
            destination = self.image(root / "bright/editing/sample.png", source.read_bytes())
            metadata = root / "bright/non-editing/shuffle.txt"
            metadata.write_text("keep exact order\n")
            report_path = base / "report.json"

            result = subprocess.run(
                [sys.executable, str(VERIFIER), "--root", str(root), "--report", str(report_path), "--plain"],
                capture_output=True, text=True, check=False,
                env={**os.environ, "HOME": str(base / "home"), "XDG_CACHE_HOME": str(base / "cache"),
                     "PYTHONPATH": str(Path(pywal.__file__).parent.parent)},
            )

            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(report_path.read_text())
            self.assertFalse(report["safe_to_merge"])
            for field in ("checked", "passed", "failures", "collisions", "skipped_metadata", "results"):
                self.assertIn(field, report)
            self.assertGreaterEqual(len(report["collisions"]), 1)
            self.assertIn(str(destination), json.dumps(report["collisions"]))
            self.assertEqual(metadata.read_text(), "keep exact order\n")

    def test_cli_refuses_report_path_that_would_replace_shuffle_metadata(self):
        self.assertTrue(VERIFIER.is_file(), f"missing verifier script: {VERIFIER}")
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(Path(temporary))
            metadata = root / "bright/non-editing/shuffle.txt"
            metadata.write_text("preserve this exact metadata\n")

            result = subprocess.run(
                [sys.executable, str(VERIFIER), "--root", str(root), "--report", str(metadata), "--plain"],
                capture_output=True, text=True, check=False,
                env={**os.environ, "HOME": str(Path(temporary) / "home"),
                     "PYTHONPATH": str(Path(pywal.__file__).parent.parent)},
            )

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(metadata.read_text(), "preserve this exact metadata\n")

    def test_cli_refuses_report_path_inside_scanned_tree_or_active_cache(self):
        self.assertTrue(VERIFIER.is_file(), f"missing verifier script: {VERIFIER}")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = self.make_root(base)
            active_cache = base / "active-cache"
            active_cache.mkdir()
            sentinel = active_cache / "colors.json"
            sentinel.write_text("active palette bytes\n")
            for report in (root / "bright/non-editing/report.json", sentinel):
                with self.subTest(report=report):
                    result = subprocess.run(
                        [sys.executable, str(VERIFIER), "--root", str(root), "--report", str(report), "--plain"],
                        capture_output=True, text=True, check=False,
                        env={**os.environ, "HOME": str(base / "home"),
                             "PYWAL_CACHE_DIR": str(active_cache),
                             "PYTHONPATH": str(Path(pywal.__file__).parent.parent)},
                    )
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(sentinel.read_text(), "active palette bytes\n")
                    if report != sentinel:
                        self.assertFalse(report.exists())

    def test_cli_does_not_overwrite_an_existing_external_report(self):
        self.assertTrue(VERIFIER.is_file(), f"missing verifier script: {VERIFIER}")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = self.make_root(base)
            report = base / "existing-report.json"
            report.write_text("existing report bytes\n")
            result = subprocess.run(
                [sys.executable, str(VERIFIER), "--root", str(root), "--report", str(report), "--plain"],
                capture_output=True, text=True, check=False,
                env={**os.environ, "HOME": str(base / "home"),
                     "PYTHONPATH": str(Path(pywal.__file__).parent.parent)},
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(report.read_text(), "existing report bytes\n")

    def test_cli_failure_report_contains_actionable_commands_diagnostics_and_palettes(self):
        self.assertTrue(VERIFIER.is_file(), f"missing verifier script: {VERIFIER}")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = self.make_root(base)
            bad_image = root / "bright/non-editing/broken.png"
            bad_image.write_bytes(b"not a real PNG image")
            report_path = base / "report.json"
            isolated_home = base / "home"

            result = subprocess.run(
                [sys.executable, str(VERIFIER), "--root", str(root), "--report", str(report_path), "--plain"],
                capture_output=True, text=True, check=False,
                env={**os.environ, "HOME": str(isolated_home),
                     "XDG_CACHE_HOME": str(isolated_home / ".cache"),
                     "XDG_CONFIG_HOME": str(isolated_home / ".config"),
                     "PYWAL_CACHE_DIR": str(base / "isolated-cache"),
                     "PYTHONPATH": str(Path(pywal.__file__).parent.parent)},
            )

            self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
            row = json.loads(report_path.read_text())["results"][0]
            self.assertEqual(row["image"], str(bad_image))
            self.assertIn("failed_checks", row)
            self.assertTrue(row["failed_checks"])
            self.assertIn("commands", row)
            self.assertIn(str(bad_image), " ".join(row["commands"]["generation"]))
            self.assertIn("-R", row["commands"]["restore"])
            self.assertIn("diagnostics", row)
            self.assertIn("generation", row["diagnostics"])
            self.assertIn("stdout", row["diagnostics"]["generation"])
            self.assertIn("stderr", row["diagnostics"]["generation"])
            self.assertIn("improper image header", " ".join(row["diagnostics"]["generation"].values()).lower())
            self.assertIn("before_palette", row)
            self.assertIn("after_palette", row)


if __name__ == "__main__":
    unittest.main()
