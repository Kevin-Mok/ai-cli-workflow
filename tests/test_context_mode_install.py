"""Executable installer contracts; external downloads are fixture controlled."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "run_onchange_after_install-context-mode.sh"


class ContextModeInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / "home"
        self.bin = Path(self.tmp.name) / "bin"
        self.home.mkdir()
        self.bin.mkdir()
        self.log = Path(self.tmp.name) / "calls"
        self.env = dict(os.environ, HOME=str(self.home), CLI_PLAIN="1",
                        PATH=f"{self.bin}:{os.environ['PATH']}", CALLS=str(self.log))
        self.stub("curl", 'echo curl >> "$CALLS"; while [ "$1" != -o ]; do shift; done; printf artifact > "$2"')
        self.stub("sha256sum", 'cat >/dev/null; [ "${BAD_HASH:-0}" = 0 ]')
        self.stub("npm", '''echo "npm $*" >> "$CALLS"
if [ "$1" = install ]; then
  shift; while [ "$1" != --prefix ]; do shift; done; shift
  mkdir -p "$1/node_modules/context-mode"
  printf '{"version":"1.0.169"}' > "$1/node_modules/context-mode/package.json"
  touch "$1/node_modules/context-mode/cli.bundle.mjs"
fi''')
        self.stub("node", '''if [ "$1" = -e ]; then exit 0
elif [ "$1" = -p ]; then echo 1.0.169
elif [ "${FTS_FAIL:-0}" = 1 ] && [ ! -e "$HOME/rebuilt" ]; then exit 1
fi''')

    def stub(self, name, code):
        file = self.bin / name
        file.write_text("#!/bin/bash\nset -eu\n" + code + "\n")
        file.chmod(0o755)

    def run_installer(self, **env):
        self.assertTrue(INSTALLER.exists(), "pinned installer is missing")
        return subprocess.run(["bash", str(INSTALLER)], env=self.env | env,
                              capture_output=True, text=True)

    def test_installs_once_and_second_run_is_offline(self):
        first = self.run_installer()
        self.assertEqual(first.returncode, 0, first.stderr)
        before = self.log.read_text()
        self.assertIn("--ignore-scripts", before)
        self.assertIn("--no-audit", before)
        self.assertEqual(self.run_installer().returncode, 0)
        self.assertEqual(self.log.read_text(), before)
        self.assertTrue((self.home / ".local/share/context-mode/1.0.169/node_modules/context-mode/cli.bundle.mjs").exists())

    def test_bad_checksum_never_installs(self):
        result = self.run_installer(BAD_HASH="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("npm", self.log.read_text())
        self.assertFalse((self.home / ".local/share/context-mode/1.0.169").exists())

    def test_rebuilds_only_native_dependency_when_fts_unavailable(self):
        self.stub("npm", '''echo "npm $*" >> "$CALLS"
if [[ " $* " = *" rebuild better-sqlite3 "* ]]; then touch "$HOME/rebuilt"; exit 0; fi
shift; while [ "$1" != --prefix ]; do shift; done; shift
mkdir -p "$1/node_modules/context-mode"
printf '{"version":"1.0.169"}' > "$1/node_modules/context-mode/package.json"
touch "$1/node_modules/context-mode/cli.bundle.mjs"''')
        result = self.run_installer(FTS_FAIL="1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("rebuild better-sqlite3", self.log.read_text())
        self.assertNotIn("rebuild context-mode", self.log.read_text())

    def test_failed_install_preserves_previous_directory(self):
        dest = self.home / ".local/share/context-mode/1.0.169"
        dest.mkdir(parents=True)
        (dest / "marker").write_text("preserve")
        self.stub("npm", "exit 7")
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((dest / "marker").read_text(), "preserve")

    def test_concurrent_publish_never_nests_a_second_runtime(self):
        self.stub("mv", '''destination="${@: -1}"
mkdir -p "$destination/node_modules/context-mode"
printf competing > "$destination/marker"
exec /bin/mv "$@"''')
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0, "a concurrent publisher must not report installation success")
        dest = self.home / ".local/share/context-mode/1.0.169"
        self.assertEqual((dest / "marker").read_text(), "competing")
        self.assertFalse((dest / "runtime").exists())

    def test_empty_demo_rejects_an_unexpected_search_response(self):
        package = Path(self.tmp.name) / "package"
        package.mkdir()
        (package / "cli.bundle.mjs").touch()
        self.stub("node", '''exec python3 -u -c '
import json,sys
for line in sys.stdin:
    req=json.loads(line)
    if "id" not in req: continue
    result={} if req["method"]=="initialize" else {"content":[{"type":"text","text":"Unexpected search response"}]}
    print(json.dumps({"jsonrpc":"2.0","id":req["id"],"result":result}),flush=True)
' ''')
        result = subprocess.run(["python3", str(ROOT / "scripts/executable_context-mode-demo"),
                                 "--package", str(package), "--case", "empty", "--plain"],
                                env=self.env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, "empty demo must check no-result semantics")


if __name__ == "__main__":
    unittest.main()
