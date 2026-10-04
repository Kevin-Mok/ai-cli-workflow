"""Deterministic scoring and durable accounting; no model access here."""
import ast
from collections import Counter, defaultdict
import fcntl
import hashlib
import json
import os
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile
import time

MINIMAL = ('Complete the task below using only supplied inputs. Preserve every explicit '
           'constraint. State unknown facts as unknown; do not invent facts or permissions. '
           'Return the requested deliverable and stop.\n\n')
FINISHED = {'completed', 'compile_failed', 'solver_failed', 'infrastructure_error',
            'interrupted', 'episode_limit', 'quota_truncated'}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)


class Budget:
    """Reserve requests before forwarding. Failed requests never refund quota."""
    def __init__(self, path: Path, cap: int):
        if type(cap) is not int or cap < 1 or cap > 2000:
            raise ValueError('The authorized selection benchmark requires a cap from 1 through 2000')
        self.path, self.cap = path, cap
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            with path.open() as handle:
                fcntl.flock(handle, fcntl.LOCK_SH)
                if json.load(handle).get('cap') != cap:
                    raise ValueError('Cannot change an existing run budget')

    def permit(self, label: str) -> bool:
        with self.path.open('a+') as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            handle.seek(0)
            content = handle.read()
            state = json.loads(content) if content else {'cap': self.cap, 'reserved': 0, 'requests': []}
            if state['cap'] != self.cap or state['reserved'] >= self.cap:
                return False
            state['reserved'] += 1
            state['requests'].append({'label': label, 'reserved_at': time.time()})
            handle.seek(0)
            handle.truncate()
            json.dump(state, handle, indent=2)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
            return True

    @property
    def used(self) -> int:
        if not self.path.exists():
            return 0
        with self.path.open() as handle:
            fcntl.flock(handle, fcntl.LOCK_SH)
            return json.load(handle)['reserved']


class FixtureFiles:
    """A model's filesystem is its scratch tree, not the host filesystem."""
    def __init__(self, root: Path, writable_prefix: str, replace_existing: bool = False):
        self.root = root.resolve()
        self.prefix = writable_prefix
        self.replace_existing = replace_existing

    def resolve(self, name: str) -> Path:
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or not path.parts:
            raise ValueError('Only relative fixture paths are accessible')
        target = (self.root / path).resolve()
        if not target.is_relative_to(self.root):
            raise ValueError('Fixture path escapes its workspace')
        return target

    def read(self, name: str) -> str:
        return self.resolve(name).read_text()

    def write(self, name: str, content: str) -> None:
        target = self.resolve(name)
        if self.replace_existing and name != self.prefix:
            raise ValueError('Only the declared fixture target may be replaced')
        if not (name.startswith(self.prefix + '/') or name == self.prefix):
            raise ValueError('Writing outside the declared artifact area is forbidden')
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open('w' if self.replace_existing else 'x') as handle:
                handle.write(content)
        except FileExistsError as exc:
            raise ValueError('Artifact exists; choose a non-destructive suffix') from exc


def saved_name(output: str) -> str | None:
    named = re.search(r'(?m)^Saved:\s*`?([^`\n]+?)`?\s*$', output)
    return named.group(1).removeprefix('<scratch>/fixture/').removeprefix('./') if named else None


def extract_prompt(output: str, artifacts: dict[str, str], candidate: str = '') -> dict:
    """Extract bytes mechanically; never rewrite a candidate's product."""
    fences = re.findall(r'```prompt\s*\n(.*?)\n```', output, re.S)
    if len(fences) > 1:
        return {'prompt': None, 'adapter': 'ambiguous_prompt_fences'}
    named = saved_name(output)
    if named in artifacts:
        if fences and fences[0].rstrip('\n') != artifacts[named].rstrip('\n'):
            return {'prompt': None, 'adapter': 'saved_prompt_mismatch'}
        return {'prompt': artifacts[named], 'adapter': 'saved_artifact'}
    if len(artifacts) == 1:
        return {'prompt': next(iter(artifacts.values())), 'adapter': 'only_saved_artifact'}
    if len(fences) == 1:
        return {'prompt': fences[0], 'adapter': 'single_prompt_fence'}
    if len(fences) > 1:
        return {'prompt': None, 'adapter': 'ambiguous_prompt_fences'}
    if candidate == 'sentry':
        section = re.search(r'(?ims)^#{1,4}\s*(?:\d+[.)]?\s*)?Optimized Prompt\s*\n(.*?)(?=^#{1,4}\s|\Z)', output)
        if section:
            raw = section.group(1).strip()
            match = re.fullmatch(r'```[^\n]*\n(.*?)\n```', raw, re.S)
            return {'prompt': match.group(1) if match else raw, 'adapter': 'sentry_optimized_prompt_section'}
    if candidate == 'github':
        fences = re.findall(r'```[^\n]*\n(.*?)\n```', output, re.S)
        if len(fences) == 1:
            return {'prompt': fences[0], 'adapter': 'github_single_fence'}
    if candidate == 'talki' and output.strip():
        return {'prompt': output, 'adapter': 'talki_entire_native_output'}
    return {'prompt': None, 'adapter': 'no_unambiguous_prompt'}


def native_contract(candidate: str, output: str, artifacts: dict[str, str]) -> list[str]:
    failures = []
    if candidate in {'metaprompt', 'metaprompt-alxve'}:
        if not artifacts:
            failures.append('required_saved_artifact_missing')
        if len(re.findall(r'```prompt\s*\n', output)) != 1:
            failures.append('required_prompt_fence_missing_or_ambiguous')
        named = saved_name(output)
        if named not in artifacts:
            failures.append('saved_path_not_verified')
        else:
            fences = re.findall(r'```prompt\s*\n(.*?)\n```', output, re.S)
            if len(fences) == 1 and fences[0].rstrip('\n') != artifacts[named].rstrip('\n'):
                failures.append('saved_prompt_mismatch')
        metadata = re.sub(r'```.*?```', '', output, flags=re.S)
        if candidate == 'metaprompt-alxve' and (not re.search(r'\bgo\b', metadata) or
                'Run:' not in metadata or 'Weight:' not in metadata):
            failures.append('legacy_gate_missing')
    return failures


def failure_status(stage: dict, earlier_calls: int = 0) -> str:
    if stage['local_request_limit_exceeded']:
        return 'episode_limit'
    if stage['status'] == 'budget_exhausted':
        return 'quota_truncated' if stage['call_count'] + earlier_calls else 'budget_exhausted'
    return 'infrastructure_error'


def bind_template(prompt: str, bindings: dict[str, str]) -> str:
    slots = set(re.findall(r'{{([A-Za-z_][A-Za-z_0-9]*)}}', prompt))
    if slots != set(bindings):
        raise ValueError('Template variables were lost, renamed, or invented')
    return re.sub(r'{{([A-Za-z_][A-Za-z_0-9]*)}}', lambda m: bindings[m.group(1)], prompt)


def python_score(output: str, key: dict) -> tuple[bool, list[str], str]:
    code = output
    match = re.fullmatch(r'\s*```(?:python)?\n(.*?)\n```\s*', output, re.S)
    if match:
        return False, ['output_format'], 'Code-only contract forbids Markdown fences'
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return False, [], f'Invalid Python: {exc.msg}'
    safe_methods = {'append', 'extend', 'pop', 'get', 'keys', 'values', 'items', 'copy',
                    'strip', 'lower', 'upper', 'split', 'join', 'replace', 'sort', 'count', 'index', 'add',
                    'median','mean','fmean','floor','ceil','sqrt','isfinite','fabs',
                    'splitlines','partition','rpartition','rsplit','lstrip','rstrip',
                    'startswith','endswith','casefold','setdefault',
                    'List','Dict','Tuple','Sequence','Iterable','Iterator','Mapping','Optional','Union','Any',
                    'Counter','defaultdict','deque','chain','islice'}
    safe_modules = {'math','statistics','typing','collections','itertools'}
    blocked_names = {'open', 'eval', 'exec', 'compile', 'getattr', 'setattr', 'globals', 'locals',
                     'vars', 'type', 'object', 'help', 'input', 'breakpoint', 'memoryview'}
    for node in ast.walk(tree):
        if (isinstance(node, (ast.ClassDef, ast.AsyncFunctionDef))
                or isinstance(node, ast.Import) and any(a.name not in safe_modules for a in node.names)
                or isinstance(node, ast.ImportFrom) and (node.module not in safe_modules or node.level or
                    any(a.name not in safe_methods for a in node.names))
                or isinstance(node, ast.Name) and (node.id.startswith('__') or node.id in blocked_names)
                or isinstance(node, ast.Attribute) and node.attr not in safe_methods):
            return False, ['unsafe_code'], 'Code exceeds pure-function fixture execution boundary'
    # Hidden test imports refer only to the submitted module; remove those trusted
    # import nodes and evaluate the independently written assertions in its namespace.
    tests = ast.parse(key['python_tests'])
    module = Path(key['target_file']).stem
    tests.body = [node for node in tests.body
                  if not (isinstance(node, ast.ImportFrom) and node.module == module)]
    test_code = ast.unparse(tests)
    driver = '''import inspect,json,resource,sys
resource.setrlimit(resource.RLIMIT_CPU,(2,2))
resource.setrlimit(resource.RLIMIT_AS,(134217728,134217728))
resource.setrlimit(resource.RLIMIT_FSIZE,(0,0))
payload=json.load(sys.stdin)
allowed={k:getattr(__import__('builtins'),k) for k in ('abs','all','any','bool','dict','enumerate','float','int','isinstance','len','list','max','min','range','reversed','round','set','sorted','str','sum','tuple','zip','iter','next','pow','divmod','ValueError','TypeError','AssertionError','StopIteration','KeyError','IndexError','ZeroDivisionError','OverflowError','Exception')}
ns={'__builtins__':allowed}
def pure_import(name,globals=None,locals=None,fromlist=(),level=0):
    if name not in ('math','statistics','typing','collections','itertools') or level:
        raise ValueError('Unsupported fixture import')
    return __import__(name,globals,locals,fromlist,level)
allowed['__import__']=pure_import
exec(compile(payload['code'],'submission','exec'),ns)
for name,names in payload['public_parameters'].items():
    params=list(inspect.signature(ns[name]).parameters.values())
    assert [p.name for p in params]==names, 'Public parameter names changed'
    assert all(p.kind==inspect.Parameter.POSITIONAL_OR_KEYWORD and p.default is inspect.Parameter.empty for p in params), 'Public parameter kinds or defaults changed'
exec(compile(payload['tests'],'hidden_tests','exec'),ns)
'''
    with tempfile.TemporaryDirectory(prefix='metaprompt-score-') as tmp:
        try:
            result = subprocess.run([sys.executable, '-I', '-c', driver],
                                    input=json.dumps({'code': code, 'tests': test_code,
                                                      'public_parameters': key.get('public_parameters', {})}),
                                    text=True, capture_output=True, cwd=tmp,
                                    env={'PATH': os.defpath}, timeout=4)
        except subprocess.TimeoutExpired:
            return False, [], 'Fixture execution timed out'
    return result.returncode == 0, [], 'Hidden assertions passed' if result.returncode == 0 else result.stderr[-1200:]


def score_output(output: str, key: dict, violations: list[str] | None = None) -> dict:
    hard = list(violations or [])
    checks = []
    kind = key['kind']
    if kind == 'json':
        try:
            value = json.loads(output)
            # JSON serialization distinguishes booleans from numeric values.
            passed = json.dumps(value, sort_keys=True) == json.dumps(key['expected'], sort_keys=True)
        except (ValueError, TypeError):
            passed = False
        checks.append('exact_json_match' if passed else 'json_mismatch')
    elif kind == 'python':
        passed, code_hard, detail = python_score(output, key)
        hard.extend(code_hard)
        checks.append(detail)
    elif kind in {'facts', 'writing'}:
        missing = [phrase for phrase in key.get('required', []) if phrase.casefold() not in output.casefold()]
        forbidden = [phrase for phrase in key.get('forbidden', []) if phrase.casefold() in output.casefold()]
        hard.extend('forbidden_phrase:' + phrase for phrase in forbidden)
        passed = not missing and len(output.split()) <= key.get('max_words', float('inf'))
        checks.extend('missing:' + phrase for phrase in missing)
    else:
        raise ValueError(f'Unknown scorer: {kind}')
    return {'success': bool(passed and not hard), 'hard_failures': hard, 'checks': checks,
            'subjective_quality_measured': False}


def aggregate(rows: list[dict]) -> dict:
    output = {}
    for name in sorted({r['candidate'] for r in rows}):
        own = [r for r in rows if r['candidate'] == name]
        attempted = [r for r in own if r['status'] in FINISHED]
        families = {}
        for family in sorted({r['family'] for r in attempted}):
            part = [r for r in attempted if r['family'] == family]
            families[family] = {'successes': sum(r['success'] is True for r in part), 'attempted': len(part)}
            families[family]['rate'] = families[family]['successes'] / len(part)
        output[name] = {'successes': sum(r['success'] is True for r in attempted),
                        'attempted': len(attempted),
                        'pending': sum(r['status'] in {'pending', 'budget_exhausted'} for r in own),
                        'unsupported': sum(r['status'] == 'unsupported' for r in own),
                        'infrastructure_errors': sum(r['status'] == 'infrastructure_error' for r in own),
                        'failure_counts': dict(Counter(r['status'] for r in attempted if not r['success'])),
                        'per_family': families,
                        'family_weighted_rate': sum(f['rate'] for f in families.values()) / len(families) if families else None}
        output[name]['success_rate'] = output[name]['successes'] / len(attempted) if attempted else None
    return output


def paired_interval(rows: list[dict], left: str, right: str, seed: int = 7) -> dict:
    scores = defaultdict(lambda: defaultdict(list))
    families = {}
    for row in rows:
        if row['status'] in FINISHED and row['candidate'] in {left, right}:
            scores[row['case_id']][row['candidate']].append(float(row['success'] is True))
            families[row['case_id']] = row['family']
    groups = defaultdict(list)
    for case, values in scores.items():
        if left in values and right in values:
            groups[families[case]].append(sum(values[left])/len(values[left]) - sum(values[right])/len(values[right]))
    n = sum(map(len, groups.values()))
    if not n:
        return {'paired_cases': 0, 'difference': None, 'interval': None, 'method': 'no_pairs'}
    rng = random.Random(seed)
    samples = sorted(sum(sum(rng.choices(v, k=len(v))) / len(v) for v in groups.values()) / len(groups)
                     for _ in range(2000))
    return {'paired_cases': n, 'difference': sum(sum(v)/len(v) for v in groups.values())/len(groups),
            'interval': [samples[49], samples[1949]], 'method': 'family_stratified_case_cluster_bootstrap',
            'warning': 'Exploratory; tiny samples cannot establish superiority' if n < 12 else 'Exploratory multiple comparisons'}


def freeze(path: Path, inputs: list[Path], settings: dict) -> None:
    if path.exists():
        raise ValueError('Protocol already frozen; use a new run, never overwrite')
    save_json(path, {'schema_version': 1, 'settings': settings,
                     'files': {os.path.relpath(p.resolve(), path.parent.resolve()): digest(p) for p in inputs},
                     'frozen_at': time.time()})


def verify_freeze(path: Path) -> dict:
    value = json.loads(path.read_text())
    if value.get('schema_version') != 1:
        raise ValueError('Unsupported frozen protocol version')
    for relative, expected in value['files'].items():
        p = path.parent / relative
        if not p.is_file() or digest(p) != expected:
            raise ValueError(f'Frozen input changed: {relative}')
    return value
