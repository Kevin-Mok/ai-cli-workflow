"""Protect the current-main merge boundary and overnight report inputs."""

import json
import runpy
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = '8662fa3c30da549fbdb20b8477c80e015e7d5236'
PRE_MERGE_HEAD = 'd448de05'
ORIGINAL = '3e898a0f39172d7c30a6b0ae0258209cfe2c7f0c'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True)


def repo_creation_rule(text):
    start = text.index('- When asked to create a new GitHub repository,')
    return text[start:text.index('\n\n', start)]


def model_effort_lines(text):
    return [line for line in text.splitlines()
            if line.lstrip().startswith(('model =', 'model_reasoning_effort =', 'reasoning_effort ='))]


def test_main_merge_is_plain_and_preserves_protected_policy_and_culls():
    assert git('merge-base', 'HEAD', MAIN).strip() == MAIN
    assert git('merge-base', 'HEAD', PRE_MERGE_HEAD).strip().startswith(PRE_MERGE_HEAD)
    # The PR's original integration remains reachable through main's second parent.
    commits = git('rev-list', '--parents', 'HEAD').splitlines()
    pre_merge = git('rev-parse', PRE_MERGE_HEAD).strip()
    assert any(row.split()[1:] == [pre_merge, MAIN] for row in commits)
    current_agents = (ROOT / 'dot_codex/AGENTS.md').read_text()
    main_agents = git('show', f'{MAIN}:dot_codex/AGENTS.md')
    delivery = (ROOT / 'dot_codex/references/delivery.md').read_text()
    main_rule = repo_creation_rule(main_agents)
    assert main_rule in delivery
    assert delivery.count(main_rule) == 1

    before_config = git('show', f'{PRE_MERGE_HEAD}:dot_codex/config.toml')
    current_config = (ROOT / 'dot_codex/config.toml').read_text()
    assert model_effort_lines(current_config) == model_effort_lines(before_config)
    assert 'model' in tomllib.loads(current_config)
    assert git('show', f'{PRE_MERGE_HEAD}:benchmarks/trim/CULL.json') == (
        ROOT / 'benchmarks/trim/CULL.json').read_text()
    assert 'Always select Google Chrome for link previews, never Firefox.' in current_agents
    assert 'commit and push after every commit' not in current_agents


def test_original_baseline_is_kept_alongside_current_main_baseline():
    original = json.loads((ROOT / 'benchmarks/trim/BASELINE-original.json').read_text())
    measured_original = runpy.run_path(str(ROOT / 'scripts/trim-benchmark'))['collect'](ROOT, ORIGINAL)
    current = json.loads((ROOT / 'benchmarks/trim/BASELINE.json').read_text())
    assert original == measured_original
    assert current['base_commit'] == MAIN


def test_historical_denied_ai_ux_body_was_preserved_before_approved_consolidation():
    path = 'dot_agents/skills/ai-ux-deslop/SKILL.md'
    upstream = git('show', f'{MAIN}:{path}')
    current = git('show', f'978696a:{path}')
    split = runpy.run_path(str(ROOT / 'scripts/trim-benchmark'))['description_and_body']
    assert split(upstream)[1] == split(current)[1]
