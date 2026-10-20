import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import subprocess

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/executable_redshift-control"

class RedshiftControlTest(unittest.TestCase):
    def test_steps_presets_reset_bounds_and_failure(self):
        self.assertTrue(SCRIPT.exists(), "shared temperature controller is missing")
        loader = importlib.machinery.SourceFileLoader("redshift_control", str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"XDG_STATE_HOME": directory}), patch.object(module.subprocess, "run") as run:
            self.assertEqual(module.apply("adjust", -250), 6250)
            self.assertEqual(module.apply("set", 2100), 2100)
            self.assertEqual(module.apply("adjust", 250), 2350)
            self.assertEqual(module.apply("adjust", -10000), 1000)
            self.assertEqual(module.apply("adjust", 10000), 6500)
            self.assertEqual(module.apply("reset", None), 6500)
            self.assertIn(["redshift", "-x"], [c.args[0] for c in run.call_args_list])
            module.apply("set", 1800)
            run.side_effect = module.subprocess.CalledProcessError(1, "redshift")
            with self.assertRaises(module.subprocess.CalledProcessError):
                module.apply("adjust", 250)
            run.side_effect = None
            self.assertEqual(module.apply("adjust", 250), 2050)
            self.assertIn(["redshift", "-P", "-O", "2050"], [c.args[0] for c in run.call_args_list])

    def load_controller(self):
        loader = importlib.machinery.SourceFileLoader("redshift_control", str(SCRIPT))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        return module

    def test_success_notifies_applied_temperature_after_persistence(self):
        module = self.load_controller()
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"XDG_STATE_HOME": directory}):
            state = Path(directory) / "redshift/temperature"
            notifications = []
            def backend(command, **kwargs):
                if command[0] == "notify-send":
                    self.assertEqual(state.read_text().strip() + " K", command[-1])
                    notifications.append(command)
            with patch.object(module.subprocess, "run", side_effect=backend):
                for action, value, want in (("set", 2100, 2100), ("adjust", 250, 2350),
                                             ("adjust", -10000, 1000), ("adjust", 10000, 6500),
                                             ("reset", None, 6500)):
                    self.assertEqual(module.apply(action, value), want)
                    self.assertTrue(notifications, "successful operation did not notify")
                    self.assertEqual(notifications[-1][-1], f"{want} K")
            self.assertEqual(len(notifications), 5)
            for command in notifications:
                self.assertIn("string:x-dunst-stack-tag:redshift-temperature", command)

    def test_failed_redshift_does_not_notify_or_change_state(self):
        module = self.load_controller()
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"XDG_STATE_HOME": directory}):
            with patch.object(module.subprocess, "run"):
                module.apply("set", 2100)
            calls = []
            def backend(command, **kwargs):
                calls.append(command[0])
                if command[0] == "redshift":
                    raise subprocess.CalledProcessError(1, command)
            with patch.object(module.subprocess, "run", side_effect=backend):
                with self.assertRaises(subprocess.CalledProcessError):
                    module.apply("adjust", 250)
            self.assertEqual(calls, ["redshift"])
            self.assertEqual((Path(directory) / "redshift/temperature").read_text(), "2100\n")

    def test_notification_errors_do_not_fail_temperature_change(self):
        module = self.load_controller()
        for error in (FileNotFoundError(), subprocess.CalledProcessError(1, "notify-send"),
                      subprocess.TimeoutExpired("notify-send", 2)):
            with self.subTest(error=type(error).__name__), tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"XDG_STATE_HOME": directory}):
                calls = []
                def backend(command, **kwargs):
                    calls.append(command[0])
                    if command[0] == "notify-send":
                        raise error
                with patch.object(module.subprocess, "run", side_effect=backend):
                    self.assertEqual(module.apply("set", 2100), 2100)
                self.assertEqual(calls, ["redshift", "notify-send"])
                self.assertEqual((Path(directory) / "redshift/temperature").read_text(), "2100\n")

    def test_updates_existing_notification_id(self):
        module = self.load_controller()
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"XDG_STATE_HOME": directory}):
            state = Path(directory) / "redshift"
            state.mkdir()
            (state / "notification-id").write_text("invalid\n")
            notifications = []
            def backend(command, **kwargs):
                if command[0] == "notify-send":
                    notifications.append(command)
                return subprocess.CompletedProcess(command, 0, stdout="123\n")
            with patch.object(module.subprocess, "run", side_effect=backend):
                module.apply("set", 2100)
                module.apply("adjust", 250)
            self.assertIn("--replace-id=0", notifications[0])
            self.assertIn("--replace-id=123", notifications[1])
            self.assertIn("--print-id", notifications[1])

    def test_malformed_notification_state_cannot_fail_applied_change(self):
        module = self.load_controller()
        for contents in (b"\xff", b"9" * 5000):
            with self.subTest(size=len(contents)), tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"XDG_STATE_HOME": directory}):
                state = Path(directory) / "redshift"
                state.mkdir()
                (state / "notification-id").write_bytes(contents)
                with patch.object(module.subprocess, "run"):
                    self.assertEqual(module.apply("set", 2100), 2100)
                self.assertEqual((state / "temperature").read_text(), "2100\n")

if __name__ == "__main__":
    unittest.main()
