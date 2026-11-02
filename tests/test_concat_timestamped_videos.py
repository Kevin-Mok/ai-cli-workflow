"""Behavior checks for timestamp-ordered FFmpeg stream-copy concat."""

import json
import fcntl
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


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

    def test_mtime_order_includes_uppercase_mov_and_breaks_ties_by_name(self):
        for name, mtime in (("z.MOV", 1), ("b.mp4", 2), ("a.MP4", 2)):
            path = self.clips / name
            path.write_bytes(b"clip")
            os.utime(path, (mtime, mtime))
        result = self.run_script(self.clips, self.output, "--sort", "mtime", "--list-only")
        self.assertEqual(result.returncode, 0, result.stderr)
        listing = (self.root / "joined.ffconcat.txt").read_text()
        self.assertLess(listing.index("z.MOV"), listing.index("a.MP4"))
        self.assertLess(listing.index("a.MP4"), listing.index("b.mp4"))

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_landscape_joins_then_checks_each_start_with_rotation_and_side_bars(self):
        portrait = self.clips / "z <portrait>.MOV"
        rotated = self.clips / "b rotated.mp4"
        wide = self.clips / "a wide.mp4"
        rotation_source = self.root / "rotation-source.mp4"
        for path, size, top_color in (
            (portrait, "48x96", "red"), (wide, "96x54", "lime"),
            (rotation_source, "96x54", "yellow"),
        ):
            subprocess.run(
                ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                 f"color=c=blue:s={size}:r=60:d=0.6,drawbox=x=0:y=0:w=iw:h=ih/2:color={top_color}:t=fill",
                 "-f", "lavfi", "-i", "sine=frequency=440:duration=0.6",
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                 "-shortest", str(path)], check=True, capture_output=True,
            )
        subprocess.run(
            ["ffmpeg", "-v", "error", "-noautorotate", "-display_rotation", "180",
             "-i", str(rotation_source), "-c", "copy", str(rotated)], check=True, capture_output=True,
        )
        rotation = json.loads(subprocess.run(
            ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(rotated)],
            check=True, capture_output=True, text=True,
        ).stdout)["streams"][0]["side_data_list"][0]["rotation"]
        self.assertEqual(abs(rotation), 180, "fixture must carry real display rotation")
        for mtime, path in enumerate((portrait, rotated, wide), 1):
            os.utime(path, (mtime, mtime))

        result = self.run_script(
            self.clips, self.output, "--landscape", "--sort", "mtime",
            "--rotate", f"{rotated.name}=180", "--plain",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Visual review required", result.stdout)
        self.assertNotIn("✅", result.stdout + result.stderr)
        streams = json.loads(subprocess.run(
            ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(self.output)],
            check=True, capture_output=True, text=True,
        ).stdout)["streams"]
        video = next(s for s in streams if s["codec_type"] == "video")
        self.assertEqual((video["width"], video["height"]), (96, 54))
        self.assertEqual(video["sample_aspect_ratio"], "1:1")
        self.assertFalse(any(d.get("rotation", 0) for d in video.get("side_data_list", [])))
        self.assertTrue(any(s["codec_type"] == "audio" for s in streams))
        subprocess.run(
            ["ffmpeg", "-v", "error", "-xerror", "-i", str(self.output), "-f", "null", "-"],
            check=True, capture_output=True,
        )
        review = self.root / "joined.review"
        page = (review / "index.html").read_text()
        self.assertIn("z &lt;portrait&gt;.MOV", page)
        self.assertIn("b rotated.mp4", page)
        self.assertIn("a wide.mp4", page)
        for index in range(1, 4):
            frame = subprocess.run(
                ["ffmpeg", "-v", "error", "-i", str(review / f"{index:03d}.png"),
                 "-vf", "scale=96:54", "-frames:v", "1", "-pix_fmt", "rgb24",
                 "-f", "rawvideo", "-"], check=True, capture_output=True,
            ).stdout
            self.assertEqual(len(frame), 96 * 54 * 3)
            top = frame[(10 * 96 + 48) * 3:(10 * 96 + 48) * 3 + 3]
            bottom = frame[(43 * 96 + 48) * 3:(43 * 96 + 48) * 3 + 3]
            self.assertGreater(top[0 if index < 3 else 1], 150, (index, top))
            if index == 2:
                self.assertGreater(top[1], 150, (index, top))
            else:
                self.assertLess(top[1 if index == 1 else 0], 60, (index, top))
            self.assertGreater(bottom[2], 150, (index, bottom))
            if index == 1:
                edge = frame[(27 * 96 + 4) * 3:(27 * 96 + 4) * 3 + 3]
                self.assertLess(max(edge), 30, edge)
        before = self.output.read_bytes()
        rerun = self.run_script(self.clips, self.output, "--landscape", "--sort", "mtime")
        self.assertNotEqual(rerun.returncode, 0)
        self.assertEqual(self.output.read_bytes(), before)

    def test_landscape_refuses_existing_review_and_unknown_rotation(self):
        (self.clips / "a.mp4").write_bytes(b"clip")
        review = self.root / "joined.review"
        review.mkdir()
        (review / "keep.txt").write_text("keep")
        result = self.run_script(self.clips, self.output, "--landscape", "--sort", "mtime")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("review", result.stderr.lower())
        self.assertEqual((review / "keep.txt").read_text(), "keep")
        self.assertFalse(self.output.exists())
        result = self.run_script(
            self.clips, self.root / "other.mp4", "--landscape", "--sort", "mtime",
            "--rotate", "missing.mp4=180",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("rotation", result.stderr.lower())
        self.assertFalse((self.root / "other.mp4").exists())

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_landscape_preserves_non_square_pixel_display_aspect(self):
        clip = self.clips / "square-display.mp4"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
             "color=c=red:s=48x96:r=10:d=0.3,setsar=2", "-f", "lavfi", "-i",
             "sine=duration=0.3", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-shortest", str(clip)], check=True, capture_output=True,
        )
        result = self.run_script(self.clips, self.output, "--landscape", "--sort", "mtime")
        self.assertEqual(result.returncode, 0, result.stderr)
        frame = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(self.output), "-frames:v", "1",
             "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], check=True, capture_output=True,
        ).stdout
        self.assertEqual(len(frame), 96 * 54 * 3)
        # SAR 2 makes the source display square: fit 54x54, centered at x=48.
        inside = frame[(27 * 96 + 28) * 3:(27 * 96 + 28) * 3 + 3]
        outside = frame[(27 * 96 + 12) * 3:(27 * 96 + 12) * 3 + 3]
        self.assertGreater(inside[0], 150, inside)
        self.assertLess(max(outside), 30, outside)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_resume_keeps_completed_clips_and_rejects_changed_source(self):
        for index, timescale in enumerate((600, 90000), 1):
            subprocess.run(
                ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                 f"color=c=red:s=96x54:r={10 if index == 1 else 15}:d=0.4",
                 "-f", "lavfi", "-i", "sine=duration=0.4", "-c:v", "libx264",
                 "-pix_fmt", "yuv420p", "-video_track_timescale", str(timescale),
                 "-c:a", "aac", "-shortest", str(self.clips / f"{index}.mp4")],
                check=True, capture_output=True,
            )
        command = (self.clips, self.output, "--landscape", "--resume", "--sort", "mtime")
        first = self.run_script(*command)
        self.assertEqual(first.returncode, 0, first.stderr)
        work = self.root / "joined.work"
        cached = [work / "001.mp4", work / "002.mp4"]
        before = [(p.stat().st_size, p.stat().st_mtime_ns) for p in cached]
        output_before = self.output.read_bytes()
        second = self.run_script(*command)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("Reuse 1/2", second.stderr)
        self.assertEqual(before, [(p.stat().st_size, p.stat().st_mtime_ns) for p in cached])
        self.assertEqual(self.output.read_bytes(), output_before)
        with (work / "lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            concurrent = self.run_script(*command)
            self.assertNotEqual(concurrent.returncode, 0)
            self.assertIn("already running", concurrent.stderr)
        for path in cached:
            streams = json.loads(subprocess.run(
                ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
                check=True, capture_output=True, text=True,
            ).stdout)["streams"]
            video = next(s for s in streams if s["codec_type"] == "video")
            audio = next(s for s in streams if s["codec_type"] == "audio")
            self.assertEqual(video["time_base"], "1/90000")
            self.assertEqual(video["avg_frame_rate"], "10/1")
            self.assertEqual((audio["sample_rate"], audio["channels"]), ("48000", 2))
        original = self.clips / "1.mp4"
        os.utime(original, ns=(original.stat().st_atime_ns, original.stat().st_mtime_ns + 1))
        changed = self.run_script(*command)
        self.assertNotEqual(changed.returncode, 0)
        self.assertIn("changed", changed.stderr.lower())
        self.assertEqual(self.output.read_bytes(), output_before)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_resume_rebuilds_missing_clip_without_reencoding_completed_clip(self):
        for name in ("1.mp4", "2.mp4"):
            subprocess.run(
                ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                 "color=c=blue:s=96x54:r=10:d=0.3", "-f", "lavfi", "-i",
                 "sine=duration=0.3", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-shortest", str(self.clips / name)],
                check=True, capture_output=True,
            )
        command = (self.clips, self.output, "--landscape", "--resume", "--sort", "mtime")
        result = self.run_script(*command)
        self.assertEqual(result.returncode, 0, result.stderr)
        work = self.root / "joined.work"
        first_mtime = (work / "001.mp4").stat().st_mtime_ns
        self.output.unlink()
        (work / "002.mp4").unlink()
        (work / "002.partial.mp4").write_bytes(b"interrupted encode")
        resumed = self.run_script(*command)
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        self.assertIn("Reuse 1/2", resumed.stderr)
        self.assertIn("Normalize 2/2", resumed.stderr)
        self.assertEqual((work / "001.mp4").stat().st_mtime_ns, first_mtime)
        self.assertTrue(self.output.exists())
        self.assertFalse((work / "002.partial.mp4").exists())

    def test_resume_requires_landscape_and_never_adopts_foreign_output(self):
        (self.clips / "clip.mp4").write_bytes(b"clip")
        result = self.run_script(self.clips, self.output, "--resume", "--sort", "mtime")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("landscape", result.stderr)
        self.output.write_bytes(b"foreign output")
        result = self.run_script(
            self.clips, self.output, "--landscape", "--resume", "--sort", "mtime"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.output.read_bytes(), b"foreign output")

    def make_resume_clip(self):
        clip = self.clips / "clip.mp4"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
             "color=c=blue:s=96x54:r=10:d=0.3", "-f", "lavfi", "-i",
             "sine=duration=0.3", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-shortest", str(clip)], check=True, capture_output=True,
        )
        return clip

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_resume_recovers_interruption_immediately_after_clip_publication(self):
        clip = self.make_resume_clip()
        join = runpy.run_path(str(SCRIPT))["landscape_join"]
        original_rename = Path.rename

        def interrupt_after_publication(path, target):
            result = original_rename(path, target)
            if path.name == "001.partial.mp4":
                raise KeyboardInterrupt("intentional interruption after clip publication")
            return result

        with mock.patch.object(Path, "rename", autospec=True, side_effect=interrupt_after_publication):
            with self.assertRaises(KeyboardInterrupt):
                join([clip], self.output, {}, False, resume=True)
        normalized = self.root / "joined.work" / "001.mp4"
        published_mtime = normalized.stat().st_mtime_ns
        result = self.run_script(self.clips, self.output, "--landscape", "--resume", "--sort", "mtime")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Reuse 1/1", result.stderr)
        self.assertEqual(normalized.stat().st_mtime_ns, published_mtime)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg tools required")
    def test_resume_recovers_interruption_immediately_after_review_directory_creation(self):
        clip = self.make_resume_clip()
        join = runpy.run_path(str(SCRIPT))["landscape_join"]
        review = self.root / "joined.review"
        original_mkdir = Path.mkdir

        def interrupt_after_creation(path, *args, **kwargs):
            result = original_mkdir(path, *args, **kwargs)
            if path == review:
                raise KeyboardInterrupt("intentional interruption after review directory creation")
            return result

        with mock.patch.object(Path, "mkdir", autospec=True, side_effect=interrupt_after_creation):
            with self.assertRaises(KeyboardInterrupt):
                join([clip], self.output, {}, False, resume=True)
        output_before = self.output.read_bytes()
        result = self.run_script(self.clips, self.output, "--landscape", "--resume", "--sort", "mtime")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.output.read_bytes(), output_before)
        self.assertTrue((review / "index.html").is_file())

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
