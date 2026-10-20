"""Browser state is a strict private input; uncertainty must suppress idle start."""
import importlib.util
import json
import os
from pathlib import Path
import selectors
import stat
import struct
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/media_screensaver/bridge.py"
MIDDLE = {"x": 2048, "y": 0, "width": 3840, "height": 2160}


def payload(x=2100, playing=True, state="normal"):
    return {"version": 1, "healthy": True, "windows": [{
        "id": 3, "state": state,
        "bounds": {"x": x-20, "y": 0, "width": 1200, "height": 900},
        "videos": [{"playing": playing, "rect": {
            "x": x, "y": 80, "width": 640, "height": 360}}]}]}


class BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if SCRIPT.exists():
            spec = importlib.util.spec_from_file_location("screensaver_bridge", SCRIPT)
            cls.bridge = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.bridge)

    def setUp(self):
        self.assertTrue(SCRIPT.exists(), "native browser bridge is not implemented")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.directory.chmod(0o700)

    def state(self, data=None, updated=100, name="bridge-100.json"):
        path = self.directory / name
        path.write_text(json.dumps({"updated": updated, "state": data or payload()}))
        path.chmod(0o600)
        return path

    def gate(self, now=101):
        return self.bridge.read_gate(self.directory, MIDDLE, now=now)

    def test_playing_visible_video_on_middle_blocks_and_edge_touch_does_not(self):
        self.state()
        allowed, reason = self.gate()
        self.assertFalse(allowed)
        self.assertTrue(reason.startswith("playing video"))
        self.state(payload(x=1408))
        self.assertTrue(self.gate()[0])
        self.state(payload(x=5888))
        self.assertTrue(self.gate()[0])

    def test_paused_audio_only_and_minimized_do_not_block_but_fullscreen_does(self):
        for data in [payload(playing=False), payload(state="minimized"),
                     {"version": 1, "healthy": True, "windows": []}]:
            with self.subTest(data=data):
                self.state(data)
                self.assertTrue(self.gate()[0])
        self.state(payload(state="fullscreen"))
        self.assertFalse(self.gate()[0])

    def test_all_connected_profiles_are_aggregated(self):
        self.state(payload(playing=False))
        self.state(payload(), name="bridge-200.json")
        self.assertTrue(self.gate()[1].startswith("playing video"))

    def test_read_windows_exposes_only_valid_fresh_aggregate_geometry(self):
        first = payload(playing=False)
        second = payload(x=6000, state="minimized")
        self.state(first)
        self.state(second, name="bridge-200.json")
        self.assertEqual(self.bridge.read_windows(self.directory, now=101),
                         first["windows"] + second["windows"])
        self.state(second, updated=90, name="bridge-200.json")
        with self.assertRaises(ValueError):
            self.bridge.read_windows(self.directory, now=101)

    def test_read_windows_requires_connected_healthy_bridge_and_window_bounds(self):
        with self.assertRaises(ValueError):
            self.bridge.read_windows(self.directory, now=101)
        data = payload(playing=False)
        data["windows"][0].pop("bounds")
        self.state(data)
        self.assertFalse(self.gate()[0])
        with self.assertRaises(ValueError):
            self.bridge.read_windows(self.directory, now=101)
        data = payload(playing=False)
        data["windows"][0]["bounds"]["x"] = float("nan")
        self.state(data)
        self.assertFalse(self.gate()[0])

    def test_missing_stale_future_and_unhealthy_state_fail_closed_with_action(self):
        allowed, reason = self.gate()
        self.assertFalse(allowed)
        self.assertRegex(reason, "install|connect|enable")
        for stamp in [96, 103, float("nan")]:
            self.state(payload(playing=False), updated=stamp)
            self.assertFalse(self.gate()[0])
        data = payload(playing=False)
        data["healthy"] = False
        self.state(data)
        self.assertFalse(self.gate()[0])

    def test_any_broken_client_suppresses_activation_even_with_other_healthy_clients(self):
        self.state(payload(playing=False))
        path = self.state(payload(playing=False), name="bridge-200.json")
        path.write_text("{")
        self.assertFalse(self.gate()[0])

    def test_unknown_content_duplicate_keys_and_nonfinite_geometry_are_rejected(self):
        for kind in ["url", "nan", "negative", "bool", "oversized", "unknown-window"]:
            data = payload(playing=False)
            if kind == "url":
                data["url"] = "https://must-not-be-retained.invalid"
            elif kind == "nan":
                data["windows"][0]["videos"][0]["rect"]["x"] = float("nan")
            elif kind == "negative":
                data["windows"][0]["videos"][0]["rect"]["width"] = -1
            elif kind == "bool":
                data["windows"][0]["id"] = True
            elif kind == "oversized":
                data["windows"][0]["videos"][0]["rect"]["width"] = 10**20
            else:
                data["windows"][0]["title"] = "private"
            self.state(data)
            with self.subTest(kind=kind):
                self.assertFalse(self.gate()[0])
        path = self.state(payload(playing=False))
        path.write_text('{"updated":100,"updated":100,"state":{}}')
        self.assertFalse(self.gate()[0])

    def test_private_files_only_and_symlinks_are_not_followed(self):
        path = self.state(payload(playing=False))
        path.chmod(0o644)
        self.assertFalse(self.gate()[0])
        path.unlink()
        target = self.directory / "target"
        target.write_text("do not touch")
        path.symlink_to(target)
        self.assertFalse(self.gate()[0])
        self.assertEqual(target.read_text(), "do not touch")

    def test_deeply_nested_malformed_json_fails_closed_without_crashing_gate(self):
        path = self.state(payload(playing=False))
        path.write_text('{"updated":100,"state":' + '['*2000 + '0' + ']'*2000 + '}')
        self.assertFalse(self.gate()[0])
        with self.assertRaises(ValueError):
            self.bridge.read_windows(self.directory, now=101)

    def test_runtime_directory_is_private_and_refuses_existing_symlink_or_public_dir(self):
        with patch.dict(os.environ, {"XDG_RUNTIME_DIR": str(self.directory)}):
            result = self.bridge.runtime_dir()
            self.assertEqual(result, self.directory / "media-screensaver")
            self.assertEqual(stat.S_IMODE(result.stat().st_mode), 0o700)
            result.rmdir()
            result.symlink_to(self.directory, target_is_directory=True)
            with self.assertRaises((OSError, RuntimeError, ValueError)):
                self.bridge.runtime_dir()
            result.unlink()
            result.mkdir(mode=0o755)
            with self.assertRaises((OSError, RuntimeError, ValueError)):
                self.bridge.runtime_dir()

    def native(self):
        process = subprocess.Popen([sys.executable, str(SCRIPT)], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env={**os.environ, "XDG_RUNTIME_DIR": str(self.directory)})
        def cleanup():
            if process.poll() is None:
                process.kill()
            process.wait(timeout=3)
            for stream in [process.stdin, process.stdout, process.stderr]:
                stream.close()
        self.addCleanup(cleanup)
        return process

    def ack(self, process):
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            self.assertTrue(selector.select(3), "native host did not acknowledge update")
        header = process.stdout.read(4)
        self.assertEqual(len(header), 4, "native host closed before acknowledging")
        return json.loads(process.stdout.read(struct.unpack("=I", header)[0]))

    def test_real_native_framing_partial_reads_private_state_host_timestamp_and_eof_cleanup(self):
        process = self.native()
        encoded = json.dumps(payload()).encode()
        framed = struct.pack("=I", len(encoded)) + encoded
        for part in [framed[:2], framed[2:7], framed[7:]]:
            process.stdin.write(part)
            process.stdin.flush()
        self.assertEqual(self.ack(process), {"ok": True})
        files = list((self.directory / "media-screensaver").glob("bridge-*.json"))
        self.assertEqual(len(files), 1)
        self.assertEqual(stat.S_IMODE(files[0].stat().st_mode), 0o600)
        stored = json.loads(files[0].read_text())
        self.assertLess(abs(stored["updated"] - time.time()), 2)
        self.assertEqual(stored["state"], payload())
        process.stdin.close()
        self.assertEqual(process.wait(timeout=3), 0)
        self.assertFalse(files[0].exists())

    def test_native_rejects_content_without_persisting_it_and_recovers_next_update(self):
        process = self.native()
        bad = payload()
        bad["url"] = "private browsing content"
        for data, expected in [(bad, False), (payload(playing=False), True)]:
            encoded = json.dumps(data).encode()
            process.stdin.write(struct.pack("=I", len(encoded)) + encoded)
            process.stdin.flush()
            self.assertEqual(self.ack(process), {"ok": expected})
            stored = list((self.directory / "media-screensaver").glob("bridge-*.json"))[0].read_text()
            self.assertNotIn("private browsing", stored)
            if not expected:
                self.assertFalse(json.loads(stored)["state"]["healthy"])

    def test_truncated_and_oversized_native_frames_exit_and_cleanup(self):
        for framed in [b"\x01\x00", struct.pack("=I", 100) + b"{}",
                       struct.pack("=I", 2**30)]:
            with self.subTest(framed=framed):
                process = self.native()
                process.stdin.write(framed)
                process.stdin.close()
                self.assertNotEqual(process.wait(timeout=3), 0)
                self.assertFalse(list((self.directory / "media-screensaver").glob("bridge-*.json")))

    def test_extension_id_is_derived_from_manifest_public_key(self):
        import base64
        import hashlib
        manifest = json.loads((SCRIPT.parent / "browser/manifest.json").read_text())
        digest = hashlib.sha256(base64.b64decode(manifest["key"], validate=True)).hexdigest()[:32]
        identifier = "".join(chr(ord("a") + int(character, 16)) for character in digest)
        self.assertEqual(self.bridge.EXTENSION_ID, identifier)


if __name__ == "__main__":
    unittest.main()
