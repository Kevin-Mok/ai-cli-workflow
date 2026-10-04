"""Fixture-only tools and two narrowly bounded, deterministic check actions."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from selection_core import FixtureFiles, score_output
from selection_eval import evaluate_prompt


def skill_check(fs: FixtureFiles, args: dict, helper: str | None) -> str:
    if not helper:
        raise ValueError('This candidate has no approved native helper')
    if set(args) - {'prompt_path', 'baseline_path', 'output_path'} or 'prompt_path' not in args:
        raise ValueError('Only prompt_path, baseline_path and output_path are accepted')
    prompt = fs.resolve(args['prompt_path'])
    command = [sys.executable, '-I', str(fs.resolve(helper)), str(prompt), '--analyze', '--json']
    if args.get('baseline_path'):
        command.extend(['--compare', str(fs.resolve(args['baseline_path']))])
    if args.get('output_path'):
        name = args['output_path']
        if not name.startswith('artifacts/'):
            raise ValueError('Helper outputs must be new artifacts/ files')
        output = fs.resolve(name)
        if output.exists():
            raise ValueError('Helper output exists; use a new filename')
        output.parent.mkdir(parents=True, exist_ok=True)
        command.extend(['--output', str(output)])
    result = subprocess.run(command, text=True, capture_output=True, cwd=fs.root,
                            env={'PATH': os.defpath}, timeout=10)
    return json.dumps({'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})


def respond(message: dict, fs: FixtureFiles, log: Path, helper: str | None = None,
            evaluation: tuple[Path, str] | None = None) -> dict | None:
    ident, method = message.get('id'), message.get('method')
    result = {}
    empty = {'type': 'object', 'properties': {}, 'additionalProperties': False}
    if method == 'initialize':
        result = {'protocolVersion': message.get('params', {}).get('protocolVersion', '2024-11-05'),
                  'capabilities': {'tools': {}}, 'serverInfo': {'name': 'selection-fixtures', 'version': '1'}}
    elif method == 'tools/list':
        def schema(properties, required):
            return {'type': 'object', 'properties': {p: {'type': 'string'} for p in properties},
                    'required': required, 'additionalProperties': False}
        result = {'tools': [
            {'name': 'read_file', 'description': 'Read a supplied relative fixture or native skill reference.',
             'inputSchema': schema(['path'], ['path'])},
            {'name': 'read_files', 'description': 'Read several supplied references or fixture files in one tool call.',
             'inputSchema': {'type': 'object', 'properties': {'paths': {'type': 'array', 'items': {'type': 'string'}, 'minItems': 1, 'maxItems': 20}}, 'required': ['paths'], 'additionalProperties': False}},
            {'name': 'write_file', 'description': 'Write only ' + fs.prefix +
             ('; replace this authorized target.' if fs.replace_existing else '/; create new prompt artifacts without overwriting.'),
             'inputSchema': schema(['path', 'content'], ['path', 'content'])},
            {'name': 'write_files', 'description': 'Save related prompt drafts and public eval inputs together; same permissions as write_file. Validate the full batch before writing.',
             'inputSchema': {'type': 'object', 'properties': {'files': {'type': 'array', 'items': schema(['path', 'content'], ['path', 'content']), 'minItems': 1, 'maxItems': 20}}, 'required': ['files'], 'additionalProperties': False}},
            {'name': 'list_files', 'description': 'List supplied fixture paths.', 'inputSchema': empty},
            {'name': 'run_tests', 'description': 'Run supplied public_tests.py against the authorized coding target. No arguments; hidden tests are unavailable.', 'inputSchema': empty},
            {'name': 'run_skill_check', 'description': 'Run the pinned senior-prompt-engineer prompt_optimizer.py with --analyze --json, optional --compare baseline_path and --output output_path. Only available when that skill is supplied. No model calls.',
             'inputSchema': schema(['prompt_path', 'baseline_path', 'output_path'], ['prompt_path'])},
            {'name': 'evaluate_prompt', 'description': 'Evaluate a saved prompt on 1-20 public cases [{id,input,expected}] in one fresh no-tools model context; exact JSON compare, use string outputs for text/code. Expected values stay local. Charges the compiler stage. Save to a new artifacts/ path.',
             'inputSchema': schema(['prompt_path', 'cases_path', 'output_path'], ['prompt_path', 'cases_path', 'output_path'])},
        ]}
        if not evaluation:
            result['tools'] = [tool for tool in result['tools'] if tool['name'] != 'evaluate_prompt']
        if not helper:
            result['tools'] = [tool for tool in result['tools'] if tool['name'] != 'run_skill_check']
        if not fs.replace_existing:
            result['tools'] = [tool for tool in result['tools'] if tool['name'] != 'run_tests']
    elif method == 'tools/call':
        params = message.get('params', {})
        name, args = params.get('name'), params.get('arguments', {})
        record = {'tool': name, 'arguments': args}
        try:
            if name == 'read_file' and set(args) == {'path'}:
                content = fs.read(args['path'])
            elif name == 'read_files' and set(args) == {'paths'}:
                paths = args['paths']
                if not isinstance(paths, list) or not 1 <= len(paths) <= 20 or any(not isinstance(p, str) for p in paths):
                    raise ValueError('Expected 1-20 relative file paths')
                content = json.dumps({path: fs.read(path) for path in paths})
            elif name == 'write_file' and set(args) == {'path', 'content'}:
                fs.write(args['path'], args['content'])
                content = 'Saved: ' + args['path']
            elif name == 'write_files' and set(args) == {'files'}:
                files = args['files']
                if not isinstance(files, list) or not 1 <= len(files) <= 20:
                    raise ValueError('Expected 1-20 files')
                targets = set()
                for item in files:
                    if not isinstance(item, dict) or set(item) != {'path', 'content'} or any(not isinstance(v, str) for v in item.values()):
                        raise ValueError('Each file requires path and content strings')
                    path = fs.resolve(item['path'])
                    allowed = item['path'] == fs.prefix if fs.replace_existing else item['path'].startswith(fs.prefix + '/')
                    if not allowed:
                        raise ValueError('Writing outside the declared artifact area is forbidden')
                    if path in targets or (path.exists() and not fs.replace_existing):
                        raise ValueError('Batch contains duplicate or existing target; use new paths')
                    targets.add(path)
                for item in files:
                    fs.write(item['path'], item['content'])
                content = 'Saved: ' + ', '.join(item['path'] for item in files)
            elif name == 'list_files' and not args:
                content = '\n'.join(str(p.relative_to(fs.root)) for p in sorted(fs.root.rglob('*')) if p.is_file())
            elif name == 'run_tests' and not args:
                if not fs.replace_existing:
                    raise ValueError('No authorized coding target in this stage')
                key = {'kind': 'python', 'target_file': fs.prefix, 'python_tests': fs.read('public_tests.py')}
                content = json.dumps(score_output(fs.read(fs.prefix), key)).replace('Hidden assertions passed', 'Public assertions passed')
            elif name == 'run_skill_check':
                content = skill_check(fs, args, helper)
            elif name == 'evaluate_prompt' and evaluation:
                evaluated = evaluate_prompt(fs, args, evaluation[0], evaluation[1])
                record['native_runtime'] = evaluated.pop('runtime') or {}
                content = json.dumps(evaluated)
            else:
                raise ValueError('Tool or arguments are not authorized in this fixture')
            result = {'content': [{'type': 'text', 'text': content}]}
            record.update(status='ok', result=content)
        except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
            result = {'content': [{'type': 'text', 'text': str(exc)}], 'isError': True}
            denied = any(marker in str(exc) for marker in (
                'Only relative fixture paths', 'Fixture path escapes',
                'Only the declared fixture target', 'Writing outside the declared artifact area'))
            record.update(status='denied' if denied else 'error', result=str(exc))
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('a') as handle:
            handle.write(json.dumps(record) + '\n')
        if evaluation:
            from selection_eval import StageBudget
            remaining = max(0, 10 - StageBudget(evaluation[0], evaluation[1]).used)
            result['content'].append({'type': 'text', 'text': 'Compiler inference requests remaining: ' + str(remaining) + '. Reserve one request for the final deliverable; report unexecuted checks honestly.'})
    elif ident is not None and method != 'ping':
        return {'jsonrpc': '2.0', 'id': ident, 'error': {'code': -32601, 'message': 'Unsupported method'}}
    return {'jsonrpc': '2.0', 'id': ident, 'result': result} if ident is not None else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('prefix')
    parser.add_argument('log', type=Path)
    parser.add_argument('--replace-target', action='store_true')
    parser.add_argument('--skill-check')
    parser.add_argument('--budget', type=Path)
    parser.add_argument('--stage-label')
    args = parser.parse_args()
    fs = FixtureFiles(args.root, args.prefix, args.replace_target)
    for line in sys.stdin:
        evaluation = (args.budget, args.stage_label) if args.budget and args.stage_label else None
        result = respond(json.loads(line), fs, args.log, args.skill_check, evaluation)
        if result is not None:
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
