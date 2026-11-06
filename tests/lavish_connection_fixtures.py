"""Local HTTP and creator-process fixtures for the Lavish connection tests."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import time
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/executable_lavish-connection-test'
KEY = '0123456789abcdef'
THREAD = '11111111-2222-4333-8444-555555555555'
OTHER = 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee'


@contextmanager
def lavish(mode='success'):
    with tempfile.TemporaryDirectory() as directory:
        state = Path(directory) / 'state.json'
        requests = []
        timers = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def do_GET(self):
                requests.append(('GET', self.path))
                if self.path != '/health':
                    self.send_error(404)
                    return
                if mode == 'redirect':
                    self.send_response(302)
                    self.send_header('Location', 'http://example.com/health')
                    self.end_headers()
                    return
                payload = {'ok': True, 'app': 'lavish-axi', 'state_dir': directory,
                           'state_id': hashlib.sha256(str(state.resolve()).encode()).hexdigest()[:16],
                           'listeners': [] if mode == 'disconnected' else [{'key': KEY, 'label': 'creator'}]}
                if mode == 'queued' and hasattr(self.server, 'submitted'):
                    self.server.wait_health = getattr(self.server, 'wait_health', 0) + 1
                    if self.server.wait_health >= 3:
                        document = json.loads(state.read_text())
                        session = document['sessions'][KEY]
                        session['status'] = 'open'
                        session['chat'][-1]['delivered_at'] = '2026-11-06T00:00:02Z'
                        session['chat'].append({'role': 'agent', 'text': f'LAVISH_CONNECTION_ACK {self.server.nonce} {THREAD}'})
                        state.write_text(json.dumps(document))
                if mode in ('reconnect', 'never-reconnect') and hasattr(self.server, 'submitted'):
                    self.server.wait_health = getattr(self.server, 'wait_health', 0) + 1
                    if mode == 'never-reconnect' or self.server.wait_health <= 2:
                        payload['listeners'] = []
                if mode == 'state-mismatch':
                    payload['state_id'] = 'wrong'
                if mode == 'malformed':
                    payload['listeners'] = 'invalid'
                self.send_response(200)
                self.end_headers()
                encoded = json.dumps(payload).encode()
                if mode == 'late' and hasattr(self.server, 'submitted'):
                    try:
                        for offset in range(0, len(encoded), 30):
                            self.wfile.write(encoded[offset:offset+30])
                            self.wfile.flush()
                            time.sleep(.1)
                    except BrokenPipeError:
                        pass
                else:
                    self.wfile.write(encoded)

            def do_POST(self):
                requests.append(('POST', self.path))
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                self.server.submitted = body
                self.server.origin = self.headers.get('Origin')
                question = body['prompts'][0]['prompt']
                if question.startswith('Manual edit test:'):
                    document = json.loads(state.read_text())
                    session = document['sessions'][KEY]
                    session['chat'].append({'role': 'user', 'text': question,
                                            'delivered_at': 'now', 'done_at': 'now'})
                    if mode == 'auto-complete':
                        artifact = Path(session['file'])
                        content = artifact.read_text().replace('One page. One creating agent.', 'Connection verified')
                        artifact.write_text(re.sub(r'<script id="manual-test-prefill">.*?</script>', '', content, flags=re.S))
                        session['chat'].append({'role': 'agent', 'text': f'CODEX_THREAD_ID: {THREAD}. Heading Connection verified.'})
                    state.write_text(json.dumps(document))
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"status":"queued"}')
                    return
                nonce = re.search(r'LAVISH_CONNECTION_ACK ([0-9a-f]{32})', question).group(1)
                self.server.nonce = nonce
                document = json.loads(state.read_text())
                session = document['sessions'][KEY]
                if mode == 'queued':
                    session['status'] = 'feedback'
                user = {'role': 'user', 'kind': 'message', 'text': question,
                        'prompt_id': 'probe', 'at': '2026-11-06T00:00:01Z'}
                if mode not in ('undelivered', 'queued'):
                    user['delivered_at'] = '2026-11-06T00:00:02Z'
                session['chat'].append(user)
                if mode not in ('timeout', 'undelivered', 'queued'):
                    ack_nonce = '0' * 32 if mode == 'stale' else nonce
                    ack_thread = OTHER if mode == 'wrong' else THREAD
                    greeting = 'Captain, connection checked.\n' if mode == 'greeting' else ''
                    notice = '\nExpected result: heading Connection verified; creator confirms its own ID.' if 'Expected result:' in question and mode != 'missing-notice' else ''
                    session['chat'].append({'role': 'agent', 'text': f'{greeting}LAVISH_CONNECTION_ACK {ack_nonce} {ack_thread}{notice}',
                                            'at': '2026-11-06T00:00:03Z'})
                if mode == 'undelivered':
                    session['chat'].append({'role': 'agent', 'text': f'LAVISH_CONNECTION_ACK {nonce} {THREAD}'})
                if mode == 'partial':
                    state.write_text('{')
                    timer = threading.Timer(.05, state.write_text, args=(json.dumps(document),))
                    timers.append(timer)
                    timer.start()
                else:
                    state.write_text(json.dumps(document))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status":"queued"}')
                if mode in ('bare', 'missing-notice', 'manual-complete', 'manual-wrong', 'manual-no-edit', 'manual-no-reply', 'manual-auto-finish'):
                    def finish():
                        document = json.loads(state.read_text())
                        session = document['sessions'][KEY]
                        if mode.startswith('manual-'):
                            artifact = Path(session['file'])
                            if mode != 'manual-no-edit':
                                content = artifact.read_text().replace('One page. One creating agent.', 'Connection verified')
                                artifact.write_text(re.sub(r'<script id="manual-test-prefill">.*?</script>', '', content, flags=re.S))
                            session['chat'].append({'role': 'user', 'text': 'Manual edit test: Change the main page heading.',
                                                    'delivered_at': 'now', 'done_at': 'now'})
                            if mode != 'manual-no-reply':
                                creator = OTHER if mode == 'manual-wrong' else THREAD
                                session['chat'].append({'role': 'agent', 'text': f'CODEX_THREAD_ID: {creator}. Heading Connection verified.'})
                            state.write_text(json.dumps(document))
                            def end():
                                current = json.loads(state.read_text())
                                current['sessions'][KEY]['status'] = 'ended'
                                state.write_text(json.dumps(current))
                            if mode != 'manual-auto-finish':
                                closing = threading.Timer(.6, end)
                                timers.append(closing)
                                closing.start()
                        else:
                            session['status'] = 'ended'
                            state.write_text(json.dumps(document))
                    timer = threading.Timer(.5, finish)
                    timers.append(timer)
                    timer.start()
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        server.state = state
        server.mode = mode
        origin = f'http://127.0.0.1:{server.server_port}'
        document = {'sessions': {KEY: {'key': KEY, 'file': '/tmp/example.html',
                    'url': f'{origin}/session/{KEY}', 'status': 'ended' if mode == 'ended' else 'open', 'chat': []}}}
        if mode == 'bad-url':
            document['sessions'][KEY]['url'] = 42
        if mode == 'alias':
            document['sessions'][KEY]['url'] = f'https://machine.example/session/{KEY}'
        state.write_text(json.dumps(document))
        thread = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': .01}, daemon=True)
        thread.start()
        try:
            yield origin, server, requests
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
            for timer in timers:
                timer.join()


@contextmanager
def fake_creator(server, mode="success"):
    with tempfile.TemporaryDirectory() as directory:
        bindir = Path(directory)
        calls = bindir / 'calls.json'
        codex = bindir / 'codex'
        codex.write_text("""#!/usr/bin/env python3
import json, os, pathlib, shutil, signal, subprocess, sys, time
args = sys.argv[1:]
root = pathlib.Path(args[args.index('--cd')+1])
shutil.copyfile(root/'preset.html', root/'index.html')
if os.environ.get('LAVISH_TEST_MODE')=='tamper': (root/'index.html').write_text('not the static preset')
state = pathlib.Path(os.environ['LAVISH_TEST_STATE'])
doc = json.loads(state.read_text())
doc['sessions']['0123456789abcdef']['file'] = str(root/'index.html')
if os.environ.get('LAVISH_TEST_MODE')=='register-on-stop':
 def late_register(*_args):
  state.write_text(json.dumps(doc))
  sys.exit(0)
 signal.signal(signal.SIGTERM, late_register)
 pathlib.Path(os.environ['LAVISH_TEST_CALLS']+'.ready').touch()
else:
 state.write_text(json.dumps(doc))
pathlib.Path(os.environ['LAVISH_TEST_CALLS']).write_text(json.dumps(args))
pathlib.Path(os.environ['LAVISH_TEST_CALLS']+'.pid').write_text(str(os.getpid()))
print(json.dumps({'type':'thread.started','thread_id':'11111111-2222-4333-8444-555555555555'}), flush=True)
if os.environ.get('LAVISH_TEST_MODE')=='early-child':
 child=subprocess.Popen([sys.executable,'-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(30)'])
 pathlib.Path(os.environ['LAVISH_TEST_CALLS']+'.child').write_text(str(child.pid))
 time.sleep(.1)
 sys.exit(3)
if os.environ.get('LAVISH_TEST_MODE')=='early': sys.exit(3)
while True:
 try:
  current=json.loads(state.read_text())['sessions']['0123456789abcdef']
 except json.JSONDecodeError:
  time.sleep(.01)
  continue
 if current['status']=='ended': break
 if os.environ.get('LAVISH_TEST_HTTP_MODE','').startswith('auto-') and not pathlib.Path(os.environ['LAVISH_TEST_CALLS']+'.sdk').exists():
  content=(root/'index.html').read_text()
  if '<script id="manual-test-prefill">' in content:
   harness=r'''const fs=require('fs');const queued=[];let sent;
const window={lavish:{queuePrompt:(prompt,options)=>queued.push({prompt,tag:options.tag,text:options.text}),
sendQueuedPrompts:()=>{sent=fetch(process.argv[2],{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompts:queued})}).then(r=>r.json())}}};
const html=fs.readFileSync(process.argv[1],'utf8');eval(html.match(/<script id="manual-test-prefill">([\\s\\S]*?)<\\/script>/)[1]);
Promise.resolve(sent).then(()=>fs.writeFileSync(process.argv[3],JSON.stringify({queued:queued.length,sent:!!sent})));'''
   url=current['url'].replace('/session/','/api/')+'/prompts'
   subprocess.run(['node','-e',harness,str(root/'index.html'),url,os.environ['LAVISH_TEST_CALLS']+'.sdk'],check=True)
 time.sleep(.02)
""")
        codex.chmod(0o755)
        lavish_cli = bindir / 'lavish-axi'
        lavish_cli.write_text("""#!/usr/bin/env python3
import json, os, pathlib, sys
state = pathlib.Path(os.environ['LAVISH_TEST_STATE'])
doc = json.loads(state.read_text())
pathlib.Path(os.environ['LAVISH_TEST_CALLS']+'.end').write_text(json.dumps(sys.argv[1:]))
for session in doc['sessions'].values():
 if session['file'] == sys.argv[-1] and os.environ.get('LAVISH_TEST_MODE')!='cleanup-open': session['status']='ended'
state.write_text('{' if os.environ.get('LAVISH_TEST_MODE')=='cleanup-unreadable' else json.dumps(doc))
""")
        lavish_cli.chmod(0o755)
        environment = dict(os.environ, PATH=str(bindir)+os.pathsep+os.environ['PATH'],
                           LAVISH_AXI_STATE_DIR=str(server.state.parent),
                           LAVISH_TEST_STATE=str(server.state), LAVISH_TEST_CALLS=str(calls))
        environment["LAVISH_TEST_MODE"] = mode
        environment["LAVISH_TEST_HTTP_MODE"] = server.mode
        yield environment, calls
