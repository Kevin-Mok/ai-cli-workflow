import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

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
            self.assertEqual(run.call_args.args[0], ["redshift", "-x"])
            module.apply("set", 1800)
            run.side_effect = module.subprocess.CalledProcessError(1, "redshift")
            with self.assertRaises(module.subprocess.CalledProcessError):
                module.apply("adjust", 250)
            run.side_effect = None
            self.assertEqual(module.apply("adjust", 250), 2050)
            self.assertEqual(run.call_args.args[0], ["redshift", "-P", "-O", "2050"])

if __name__ == "__main__":
    unittest.main()
