"""Behavior checks for timestamp-ordered FFmpeg stream-copy concat."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "executable_concat-timestamped-videos"
BOUNDARY_CHECK = Path(__file__).resolve().parent / "check_concat_boundary.py"


class ConcatTimestampedVideosTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.clips = self.root / "clips"
        self.clips.mkdir()
        self.output = self.root / "joined.mp4"

    def run_script(self, *args, env=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

    def test_dry_run_writes_ordered_concat_list_without_running_ffmpeg(self):
        for name in ("PXL_20260928_002000.mp4", "PXL_20260928_001000.mp4"):
            (self.clips / name).write_bytes(b"clip")
        (self.clips / "nested").mkdir()
        (self.clips / "nested" / "PXL_20260928_000000.mp4").write_bytes(b"nested")
        (self.clips / "notes.txt").write_text("notes")

        result = self.run_script(self.clips, self.output, "--list-only")

        self.assertEqual(result.returncode, 0, result.stderr)
        listing = (self.root / "joined.ffconcat.txt").read_text()
        self.assertEqual(
            listing,
            "ffconcat version 1.0\n"
            + f"file '{self.clips / 'PXL_20260928_001000.mp4'}'\n"
            + f"file '{self.clips / 'PXL_20260928_002000.mp4'}'\n",
        )
        self.assertFalse(self.output.exists())

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_dry_run_orders_pixel_and_iphone_clips_by_capture_time(self):
        iphone = self.clips / "IMG_1377.MOV"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
             "color=c=red:s=64x64:r=10:d=1", "-metadata",
             "creation_time=2026-09-28T01:21:49Z", "-c:v", "mpeg4", str(iphone)],
            check=True, capture_output=True, text=True,
        )
        pixel = self.clips / "PXL_20260928_011900910.mp4"
        pixel.write_bytes(b"clip")

        result = self.run_script(self.clips, self.output, "--list-only")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (self.root / "joined.ffconcat.txt").read_text(),
            "ffconcat version 1.0\n"
            + f"file '{pixel}'\n"
            + f"file '{iphone}'\n",
        )

    def test_dry_run_keeps_other_video_names_without_capture_metadata(self):
        pixel = self.clips / "PXL_20260928_011900910.mp4"
        pixel.write_bytes(b"clip")
        other = self.clips / "logic.mp4"
        other.write_bytes(b"prior join")

        result = self.run_script(self.clips, self.output, "--list-only")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (self.root / "joined.ffconcat.txt").read_text(),
            "ffconcat version 1.0\n"
            + f"file '{pixel}'\n"
            + f"file '{other}'\n",
        )

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_clips_selects_only_named_pair_in_capture_order(self):
        iphone = self.clips / "IMG_1377.MOV"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
             "color=c=red:s=64x64:r=10:d=1", "-metadata",
             "creation_time=2026-09-28T01:21:49Z", "-c:v", "mpeg4", str(iphone)],
            check=True, capture_output=True, text=True,
        )
        pixel = self.clips / "PXL_20260928_011900910.mp4"
        pixel.write_bytes(b"clip")
        (self.clips / "logic.mp4").write_bytes(b"existing output")
        (self.clips / "PXL_20260928_011854718.mp4").write_bytes(b"other clip")

        result = self.run_script(
            self.clips, self.output, "--clips", iphone.name, pixel.name, "--list-only"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (self.root / "joined.ffconcat.txt").read_text(),
            "ffconcat version 1.0\n"
            + f"file '{pixel}'\n"
            + f"file '{iphone}'\n",
        )

    @unittest.skipUnless(
        shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required"
    )
    def test_reencode_joins_mixed_sdr_and_hlg_clips_without_decode_errors(self):
        pixel = self.clips / "PXL_20260928_011900910.mp4"
        iphone = self.clips / "IMG_1377.MOV"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
             "color=c=red:s=64x64:r=10:d=1", "-f", "lavfi", "-i",
             "sine=frequency=440:duration=1", "-c:v", "libx264", "-pix_fmt",
             "yuv420p", "-c:a", "aac", "-shortest", str(pixel)],
            check=True, capture_output=True, text=True,
        )
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
             "color=c=blue:s=64x64:r=10:d=1", "-f", "lavfi", "-i",
             "sine=frequency=660:duration=1", "-c:v", "libx265", "-pix_fmt",
             "yuv420p10le", "-x265-params", "log-level=error", "-color_primaries",
             "bt2020", "-color_trc", "arib-std-b67", "-colorspace", "bt2020nc",
             "-metadata", "creation_time=2026-09-28T01:21:49Z", "-c:a", "aac",
             "-shortest", str(iphone)],
            check=True, capture_output=True, text=True,
        )

        result = self.run_script(
            self.clips, self.output, "--clips", iphone.name, pixel.name, "--reencode"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        decode = subprocess.run(
            ["ffmpeg", "-v", "error", "-xerror", "-i", str(self.output),
             "-f", "null", "-"], capture_output=True, text=True,
        )
        self.assertEqual(decode.returncode, 0, decode.stderr)
        self.assertEqual(decode.stderr, "")
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=pix_fmt,color_transfer", "-of", "default=noprint_wrappers=1",
             str(self.output)], capture_output=True, text=True, check=True,
        )
        self.assertIn("pix_fmt=yuv420p", probe.stdout)
        self.assertIn("color_transfer=bt709", probe.stdout)
        media = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
             "-of", "json", str(self.output)], capture_output=True, text=True, check=True,
        )
        details = json.loads(media.stdout)
        self.assertTrue(any(stream["codec_type"] == "audio" for stream in details["streams"]))
        self.assertGreater(float(details["format"]["duration"]), 1.8)
        self.assertLess(float(details["format"]["duration"]), 2.2)
        for second in (0.4, 1.4):
            pcm = subprocess.run(
                ["ffmpeg", "-v", "error", "-ss", str(second), "-i", str(self.output),
                 "-t", "0.2", "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                capture_output=True, check=True,
            ).stdout
            self.assertTrue(any(pcm))
        for second, dominant_channel in ((0.5, 0), (1.5, 2)):
            frame = subprocess.run(
                ["ffmpeg", "-v", "error", "-ss", str(second), "-i", str(self.output),
                 "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                capture_output=True, check=True,
            ).stdout
            self.assertEqual(len(frame), 64 * 64 * 3)
            pixel_value = frame[(32 * 64 + 32) * 3:(32 * 64 + 32) * 3 + 3]
            self.assertGreater(pixel_value[dominant_channel], 100)

    def test_stream_copy_uses_concat_demuxer_and_refuses_existing_output(self):
        (self.clips / "PXL_20260928_001000.mp4").write_bytes(b"clip")
        fake_bin = self.root / "bin"
        fake_bin.mkdir()
        invocation = self.root / "invocation.txt"
        fake_ffmpeg = fake_bin / "ffmpeg"
        fake_ffmpeg.write_text(
            "#!/usr/bin/env python3\n"
            "import os, sys\n"
            "from pathlib import Path\n"
            "Path(os.environ['FFMPEG_INVOCATION']).write_text('\\n'.join(sys.argv[1:]))\n"
            "Path(sys.argv[-1]).write_bytes(b'joined')\n"
        )
        fake_ffmpeg.chmod(0o755)
        env = dict(os.environ, PATH=f"{fake_bin}:{os.environ['PATH']}", FFMPEG_INVOCATION=str(invocation))

        first = self.run_script(self.clips, self.output, env=env)
        second = self.run_script(self.clips, self.output, env=env)

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(
            invocation.read_text().splitlines(),
            ["-hide_banner", "-f", "concat", "-safe", "0", "-i", str(self.root / "joined.ffconcat.txt"), "-c", "copy", str(self.output)],
        )
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("already exists", second.stderr)
        self.assertEqual(self.output.read_bytes(), b"joined")

    def test_empty_directory_is_rejected(self):
        result = self.run_script(self.clips, self.output, "--list-only")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no video files", result.stderr)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_real_join_decodes_cleanly_and_has_frames_from_both_clips(self):
        for name, color, tone in (
            ("PXL_20260928_001000.mp4", "red", "440"),
            ("PXL_20260928_002000.mp4", "blue", "660"),
        ):
            subprocess.run(
                [
                    "ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                    f"color=c={color}:s=64x64:r=10:d=1", "-f", "lavfi", "-i",
                    f"sine=frequency={tone}:duration=1", "-c:v", "mpeg4",
                    "-c:a", "aac", "-shortest", str(self.clips / name),
                ],
                check=True, capture_output=True, text=True,
            )

        result = self.run_script(self.clips, self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        decode = subprocess.run(
            ["ffmpeg", "-v", "error", "-xerror", "-i", str(self.output), "-f", "null", "-"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(decode.returncode, 0, decode.stderr)
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
             "default=noprint_wrappers=1:nokey=1", str(self.output)],
            capture_output=True, text=True, check=True,
        )
        self.assertGreater(float(probe.stdout), 1.8)
        self.assertLess(float(probe.stdout), 2.2)

        for second, dominant_channel in ((0.5, 0), (1.5, 2)):
            frame = subprocess.run(
                ["ffmpeg", "-v", "error", "-ss", str(second), "-i", str(self.output),
                 "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                capture_output=True, check=True,
            ).stdout
            self.assertEqual(len(frame), 64 * 64 * 3)
            pixel = frame[(32 * 64 + 32) * 3:(32 * 64 + 32) * 3 + 3]
            self.assertGreater(pixel[dominant_channel], 180)
            self.assertLess(max(pixel[index] for index in range(3) if index != dominant_channel), 80)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_directory_boundary_check_covers_every_adjacent_pair(self):
        for index, color in enumerate(("red", "green", "blue"), start=1):
            subprocess.run(
                ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                 f"color=c={color}:s=64x64:r=10:d=1", "-c:v", "mpeg4",
                 str(self.clips / f"PXL_20260928_00000{index}.mp4")],
                check=True, capture_output=True, text=True,
            )

        result = subprocess.run(
            [sys.executable, str(BOUNDARY_CHECK), "--directory", str(self.clips),
             "--seconds", "0.5"],
            capture_output=True, text=True, check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        sample_dir = Path(result.stdout.split("Sample directory: ", 1)[1].splitlines()[0])
        self.addCleanup(shutil.rmtree, sample_dir)
        self.assertTrue((sample_dir / "pair-01" / "joined.mp4").is_file())
        self.assertTrue((sample_dir / "pair-02" / "joined.mp4").is_file())
        self.assertTrue((sample_dir / "pair-01" / "boundary.png").is_file())
        self.assertTrue((sample_dir / "pair-02" / "boundary.png").is_file())

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_directory_check_uses_existing_concat_list_sources(self):
        names = [f"PXL_20260928_00000{index}.mp4" for index in range(1, 4)]
        for name in names:
            subprocess.run(
                ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                 "color=c=red:s=64x64:r=10:d=1", "-c:v", "mpeg4",
                 str(self.clips / name)],
                check=True, capture_output=True, text=True,
            )
        (self.clips / "clips.ffconcat.txt").write_text(
            "ffconcat version 1.0\n"
            + f"file '{self.clips / names[0]}'\n"
            + f"file '{self.clips / names[2]}'\n"
        )
        (self.clips / "clips.mp4").write_bytes(b"existing combined output")

        result = subprocess.run(
            [sys.executable, str(BOUNDARY_CHECK), "--directory", str(self.clips),
             "--seconds", "0.5"],
            capture_output=True, text=True, check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        sample_dir = Path(result.stdout.split("Sample directory: ", 1)[1].splitlines()[0])
        self.addCleanup(shutil.rmtree, sample_dir)
        self.assertTrue((sample_dir / "pair-01" / "joined.mp4").is_file())
        self.assertFalse((sample_dir / "pair-02").exists())
        self.assertIn(f"{names[0]} -> {names[2]}", result.stdout)


if __name__ == "__main__":
    unittest.main()
