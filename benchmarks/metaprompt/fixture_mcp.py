"""Minimal stdio MCP: only the supplied scratch files and append-only artifacts."""
import json
from pathlib import Path
import sys

from benchlib import FixtureFiles


def respond(message: dict, fs: FixtureFiles, log: Path) -> dict | None:
    ident = message.get('id')
    method = message.get('method')
    result = {}
    if method == 'initialize':
        result = {'protocolVersion': message.get('params', {}).get('protocolVersion', '2024-11-05'),
                  'capabilities': {'tools': {}}, 'serverInfo': {'name': 'benchmark-fixtures', 'version': '1'}}
    elif method == 'tools/list':
        result = {'tools': [
            {'name': 'read_file', 'description': 'Read a supplied relative fixture or candidate reference path.',
             'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path'], 'additionalProperties': False}},
            {'name': 'write_file', 'description': ('Write only '+fs.prefix+'. '+
                 ('This is the authorized fixture target and may be replaced.' if fs.replace_existing else 'Create new artifacts; never overwrite.')),
             'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}, 'content': {'type': 'string'}}, 'required': ['path', 'content'], 'additionalProperties': False}},
            {'name': 'list_files', 'description': 'List the available relative fixture files.',
             'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}},
        ]}
    elif method == 'tools/call':
        params = message.get('params', {})
        name, args = params.get('name'), params.get('arguments', {})
        record = {'tool': name, 'arguments': args}
        try:
            if name == 'read_file':
                content = fs.read(args['path'])
            elif name == 'write_file':
                fs.write(args['path'], args['content'])
                content = 'Saved: ' + args['path']
            elif name == 'list_files':
                content = '\n'.join(str(p.relative_to(fs.root)) for p in sorted(fs.root.rglob('*')) if p.is_file())
            else:
                raise ValueError('Tool is not authorized in this fixture')
            result = {'content': [{'type': 'text', 'text': content}]}
            record['status'] = 'ok'
        except (OSError, ValueError, KeyError, TypeError) as exc:
            result = {'content': [{'type': 'text', 'text': str(exc)}], 'isError': True}
            record['status'] = 'denied' if isinstance(exc, ValueError) else 'error'
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('a') as handle:
            handle.write(json.dumps(record) + '\n')
    elif ident is not None and method != 'ping':
        return {'jsonrpc': '2.0', 'id': ident, 'error': {'code': -32601, 'message': 'Unsupported method'}}
    if ident is not None:
        return {'jsonrpc': '2.0', 'id': ident, 'result': result}
    return None


def main() -> None:
    root, prefix, log, *options = sys.argv[1:]
    fs = FixtureFiles(Path(root), prefix, replace_existing=options == ['--replace-target'])
    for line in sys.stdin:
        value = respond(json.loads(line), fs, Path(log))
        if value is not None:
            print(json.dumps(value), flush=True)


if __name__ == '__main__':
    main()
