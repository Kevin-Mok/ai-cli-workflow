#!/usr/bin/env python3
"""Exercise CCR in a disposable HOME without providers or live agent settings."""
import argparse
import json
import os
from pathlib import Path
import secrets
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def run(package: Path, plain: bool) -> None:
    def report(message: str) -> None:
        print(('' if plain else '✅ ') + message, flush=True)

    if not (package/'dist/main/cli.js').is_file():
        raise RuntimeError('CCR package missing; install the pinned release first or pass --package-dir.')
    with tempfile.TemporaryDirectory(prefix='ccr-smoke-') as temp:
        home = Path(temp)
        prefix = home/'.local/share/claude-code-router/lib/node_modules/@musistudio'
        prefix.mkdir(parents=True)
        (prefix/'claude-code-router').symlink_to(package.resolve(), target_is_directory=True)
        directory = home/'.claude-code-router'
        directory.mkdir(mode=0o700)
        seed = ROOT/'dot_claude-code-router/create_private_config.json'
        (directory/'config.json').write_bytes(seed.read_bytes())
        (directory/'config.json').chmod(0o600)
        env = {'HOME': str(home), 'PATH': os.environ['PATH'], 'CLI_PLAIN': '1',
               'CCR_WEB_AUTH_TOKEN': secrets.token_urlsafe(32)}
        command = ['bash', str(ROOT/'dot_local/bin/executable_ccr')]
        for flag, expected in [('--version', '3.1.3'), ('--help', 'Usage:')]:
            result = subprocess.run(command+[flag], env=env, capture_output=True, text=True,
                                    timeout=20, check=True)
            if expected not in result.stdout:
                raise RuntimeError(f'Unexpected {flag} output')
        report('Pinned version 3.1.3 and real CLI help verified')
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            port = listener.getsockname()[1]
        # Even --gateway must respect the explicitly disabled seed gateway.
        with tempfile.TemporaryFile(mode='w+') as output, tempfile.TemporaryFile(mode='w+') as errors:
            process = subprocess.Popen(command+['serve', '--no-open', '--gateway', '--host',
                                               '127.0.0.1', '--port', str(port)], env=env,
                                       stdout=output, stderr=errors)
            try:
                def rpc(method: str, token: str) -> dict:
                    request = urllib.request.Request(f'http://127.0.0.1:{port}/api/ccr/rpc',
                        data=json.dumps({'method': method, 'args': []}).encode(),
                        headers={'Content-Type': 'application/json', 'x-ccr-web-auth': token})
                    with urllib.request.urlopen(request, timeout=2) as response:
                        return json.load(response)

                config = None
                print(('' if plain else '⏳ ')+'Starting isolated management service (no provider requests)', flush=True)
                for attempt in range(80):
                    try:
                        config = rpc('getConfig', env['CCR_WEB_AUTH_TOKEN'])['value']
                        break
                    except urllib.error.URLError:
                        if process.poll() is not None:
                            raise RuntimeError('Isolated service exited before readiness')
                        if attempt and attempt % 10 == 0:
                            print(('' if plain else '⏳ ')+f'Waiting for isolated startup ({attempt / 10:.0f}s elapsed)', flush=True)
                        time.sleep(0.1)
                if config is None:
                    raise RuntimeError('Isolated service did not become ready')
                assert config['profile']['enabled'] is False
                assert config['profile']['profiles'] == []
                assert config['profile']['claudeCode']['enabled'] is False
                assert config['profile']['codex']['enabled'] is False
                assert config['observability']['requestLogs'] is False
                assert config['observability']['agentAnalysis'] is False
                assert config['observability']['requestLogBodyCapture'] == 'none'
                assert config['observability']['requestLogMaxBodyBytes'] == 0
                for section in ('proxy', 'contextArchive', 'toolHub', 'mediaTools', 'botGateway'):
                    assert config[section]['enabled'] is False, section
                assert rpc('getGatewayStatus', env['CCR_WEB_AUTH_TOKEN'])['value']['state'] == 'stopped'
                try:
                    rpc('getConfig', 'invalid-token')
                    raise RuntimeError('Management RPC accepted invalid authentication')
                except urllib.error.HTTPError as error:
                    assert error.code == 401
                assert not (home/'.claude').exists() and not (home/'.codex').exists()
                report('Gateway stopped; profiles/logging disabled; invalid token rejected (401); agent settings untouched')
            finally:
                process.terminate()
                try:
                    process.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            with sqlite3.connect(directory/'config.sqlite') as database:
                stored = json.loads(database.execute("SELECT value_json FROM app_config WHERE key='default'").fetchone()[0])
            assert stored['profile']['enabled'] is False and stored['profile']['profiles'] == []
            assert stored['observability']['requestLogs'] is False
            report('Safe seed persisted to SQLite; temporary runtime cleaned up')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('' if '--plain' in sys.argv else '🔎 ')+
        'Isolated real CCR smoke check; no sudo, paid calls or live config writes.')
    parser.add_argument('--package-dir', type=Path, default=Path.home()/'.local/share/claude-code-router/lib/node_modules/@musistudio/claude-code-router')
    parser.add_argument('--plain', action='store_true', help='ASCII status output')
    args = parser.parse_args()
    try:
        run(args.package_dir, args.plain)
    except (AssertionError, OSError, RuntimeError, subprocess.SubprocessError, KeyError) as error:
        parser.exit(1, ('' if args.plain else '❌ ')+f'CCR smoke check failed: {error}\n')
