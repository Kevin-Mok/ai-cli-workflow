"""Existing-page protocol and manual-result validation for the Lavish checker."""
import hashlib
from html.parser import HTMLParser
from http.client import HTTPException
import ipaddress
import json
import math
from pathlib import Path
import re
import sys
import time
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener
from uuid import UUID, uuid4


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, _req, _fp, _code, _msg, _headers, _newurl):
        raise ValueError('The local server redirected the request; use its direct session URL.')


def session_url(value):
    parsed = urlsplit(value)
    try:
        local = parsed.hostname == 'localhost' or ipaddress.ip_address(parsed.hostname or '').is_loopback
    except ValueError:
        local = False
    if (parsed.scheme != 'http' or not local or parsed.username or parsed.password
            or parsed.query or parsed.fragment or not re.fullmatch(r'/session/[0-9a-f]{16}', parsed.path)):
        raise ValueError('Use a local HTTP Lavish session URL, such as http://127.0.0.1:4387/session/<key>.')
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ValueError('Use a valid local server port.')
    return f'http://{parsed.netloc}', parsed.path.rsplit('/', 1)[1]


def response_json(response, deadline):
    chunks = []
    size = 0
    while True:
        if time.monotonic() >= deadline:
            raise ValueError('Timed out waiting for the live server response.')
        chunk = response.read1(65536)
        if time.monotonic() >= deadline:
            raise ValueError('Timed out waiting for the live server response.')
        if not chunk:
            return json.loads(b''.join(chunks))
        size += len(chunk)
        if size > 1048576:
            raise ValueError('Invalid oversized response from the live Lavish server.')
        chunks.append(chunk)


def run(args, report=True):
    origin, key = session_url(args.url)
    expected = str(UUID(args.expect_thread))
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        raise ValueError('Timeout must be a positive finite number of seconds.')
    start = time.monotonic()
    deadline = start + args.timeout
    opener = build_opener(ProxyHandler({}), NoRedirect())

    def say(message, icon='🔌', stream=sys.stderr):
        print(f'{"" if args.plain else icon + " "}{message}', file=stream, flush=True)

    def remaining_time():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ValueError('Timed out waiting for the expected agent; the test message may remain queued.')
        return remaining

    def request(path, body=None):
        remaining = remaining_time()
        data = None if body is None else json.dumps(body).encode()
        req = Request(origin + path, data=data, headers={'Origin': origin, 'Content-Type': 'application/json'})
        try:
            with opener.open(req, timeout=min(5, remaining)) as response:
                payload = response_json(response, deadline)
        except (OSError, URLError, HTTPException):
            raise ValueError('Cannot reach the live Lavish server. Run this check on its host and confirm it is running.') from None
        except json.JSONDecodeError:
            raise ValueError('Invalid JSON from the live Lavish server; check its installed API version.') from None
        if not isinstance(payload, dict):
            raise ValueError('Invalid response from the live Lavish server.')
        return payload

    def live_state(require_listener=True):
        health = request('/health')
        if health.get('ok') is not True or health.get('app') != 'lavish-axi':
            raise ValueError('This address is not a ready Lavish server.')
        listeners = health.get('listeners')
        if not isinstance(listeners, list) or any(not isinstance(item, dict) for item in listeners):
            raise ValueError('Invalid live listener data; check the installed Lavish API version.')
        listening = any(item.get('key') == key for item in listeners)
        if require_listener and not listening:
            raise ValueError('No active listener for this page. Resume foreground lavish-axi poll in its generating conversation.')
        directory = health.get('state_dir')
        if not isinstance(directory, str) or not Path(directory).is_absolute():
            raise ValueError('Invalid live state directory; run this check on the Lavish host.')
        state = Path(directory).resolve() / 'state.json'
        if health.get('state_id') != hashlib.sha256(str(state).encode()).hexdigest()[:16]:
            raise ValueError('Invalid state identity from the live Lavish server.')
        for attempt in range(3):
            remaining_time()
            try:
                document = json.loads(state.read_text())
                session = document['sessions'][key]
                break
            except json.JSONDecodeError:
                if attempt == 2:
                    raise ValueError('Invalid live session state; check its installed API version.') from None
                time.sleep(min(.05, remaining_time()))
            except (OSError, KeyError, TypeError):
                raise ValueError('Invalid or missing live session state; run this check on the Lavish host.') from None
        remaining_time()
        if (not isinstance(session, dict) or session.get('key') != key
                or not isinstance(session.get('url'), str)
                or urlsplit(session['url']).path != f'/session/{key}'):
            raise ValueError('Invalid session identity in the live server state.')
        if session.get('status') not in (('open',) if require_listener else ('open', 'feedback')):
            raise ValueError('The review session is not open. Reopen it intentionally before testing.')
        chat = session.get('chat')
        if not isinstance(chat, list) or any(not isinstance(item, dict) for item in chat):
            raise ValueError('Invalid session chat data; check the installed Lavish API version.')
        return chat, listening

    say('2/4 Verify the connection and creator identity...' if getattr(args, 'manual_test', False)
        else 'Checking live Lavish listener...')
    live_state()
    nonce = uuid4().hex
    marker = f'LAVISH_CONNECTION_ACK {nonce}'
    question = ('Connection test only; do not modify the artifact. Read your own CODEX_THREAD_ID '
                'from your environment and include this exact standalone line in your Lavish reply '
                '(put any greeting on a separate line), replacing '
                f'<your-session-id> with that value: {marker} <your-session-id>. '
                'Then resume your existing feedback poll. Do not copy a thread ID from another message.')
    if getattr(args, 'manual_test', False):
        question += (' In the same chat reply, after the ACK line add this notice: '
                     'Expected result: after the smoke test automatically sends its isolated edit request, '
                     'the page heading becomes "Connection verified" and you reply with your own '
                     'session ID plus confirmation of that heading. Do not perform that edit yet.')
    response = request(f'/api/{key}/prompts', {'prompts': [{'prompt': question, 'tag': 'message', 'text': ''}]})
    if response.get('status') != 'queued':
        raise ValueError('The server did not accept the connection-test message.')
    say(f'Test message sent; nonce {nonce}. Waiting for the agent (0s elapsed)...')
    next_progress = time.monotonic() + 5
    while True:
        if time.monotonic() >= deadline:
            raise ValueError('Timed out waiting for the expected agent; the test message may remain queued.')
        chat, listening = live_state(False)
        for index, entry in enumerate(chat):
            if entry.get('role') != 'user' or entry.get('text') != question or not entry.get('delivered_at'):
                continue
            for reply in chat[index + 1:]:
                if reply.get('role') != 'agent' or not isinstance(reply.get('text'), str):
                    continue
                match = re.search(r'^' + re.escape(marker) + r' ([0-9a-fA-F-]{36})$',
                                  reply['text'].strip(), re.MULTILINE)
                if not match:
                    continue
                if getattr(args, 'manual_test', False) and (
                        'Expected result:' not in reply['text'] or 'Connection verified' not in reply['text']):
                    continue
                try:
                    actual = str(UUID(match.group(1)))
                except ValueError:
                    raise ValueError('Invalid session ID in the agent acknowledgement.') from None
                if actual != expected:
                    raise ValueError(f'Wrong agent replied: {actual}; expected {expected}.')
                if listening:
                    remaining_time()
                    if report:
                        say(f'PASS: connected to Codex {actual}; nonce {nonce}.', '✅', sys.stdout)
                    return actual, nonce
        now = time.monotonic()
        if now >= next_progress:
            say(f'Waiting for the expected agent ({now-start:.0f}s elapsed)...', '⏳')
            next_progress = now + 5
        time.sleep(min(.2, max(0, deadline - time.monotonic())))


class ManualHeading(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.finished = False
        self.hidden = False
        self.helper = False
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script' and dict(attrs).get('id') == 'manual-test-prefill':
            self.helper = True
        if tag == 'h1' and not self.finished:
            self.active = True
        if tag in ('script', 'style'):
            self.hidden = True

    def handle_endtag(self, tag):
        if tag == 'h1' and self.active:
            self.active, self.finished = False, True
        if tag in ('script', 'style'):
            self.hidden = False

    def handle_data(self, data):
        if self.active and not self.hidden:
            self.text.append(data)


def manual_edit_complete(session, artifact, creator):
    """Require matching chat evidence and the actual edit, not just a live process."""
    try:
        page = ManualHeading()
        page.feed(artifact.read_text())
    except (OSError, UnicodeError):
        return False
    if ' '.join(''.join(page.text).split()) != 'Connection verified' or page.helper:
        return False
    chat = session.get('chat', [])
    for index, item in enumerate(chat):
        if (item.get('role') == 'user' and str(item.get('text', '')).startswith('Manual edit test:')
                and item.get('delivered_at') and item.get('done_at')):
            for reply in chat[index + 1:]:
                text = str(reply.get('text', ''))
                identity = re.search(r'\bCODEX_THREAD_ID\b\s*(?::|=|is)\s*`?([0-9a-f-]{36})(?![0-9a-f-])', text, re.I)
                if (reply.get('role') == 'agent' and identity and identity[1].lower() == creator.lower()
                        and 'Connection verified' in text):
                    return True
    return False
