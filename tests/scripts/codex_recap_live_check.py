#!/usr/bin/env python3
"""Opt-in single synthetic recap through the installed Codex login/model; no sudo."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from codex_search_recaps import SummaryManager


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--live',action='store_true',help='authorize exactly one synthetic model request; consumes the existing Codex account allowance')
    cli.add_argument('--summary-model',help='override the configured model')
    args=cli.parse_args()
    if not args.live:
        cli.print_help();return 0
    home=Path(os.environ.get('CODEX_HOME') or Path.home()/'.codex').expanduser().resolve()
    before_sessions=set((home/'sessions').rglob('*.jsonl'))
    with tempfile.TemporaryDirectory(prefix='codex-recap-live-') as temporary:
        root=Path(temporary)
        name='1'*32+'.dialogue.jsonl'
        dialogue=[{'role':'user','text':'SYNTHETIC TASK: design a local weather-cache schema. No real implementation is needed in this fixture.'},
                  {'role':'assistant','text':'I drafted a schema proposal. No implementation or tests have been run. Remaining work is to review the proposal.'}]
        content=''.join(json.dumps(row,separators=(',',':'))+'\n' for row in dialogue)
        source=root/name;source.write_text(content);source.chmod(0o600)
        entry={'id':'00000000-0000-4000-8000-000000000001','dialogue':name,
               'dialogue_hash':hashlib.sha256(content.encode()).hexdigest(),'cwd':str(root),'timestamp':'2026-10-07T00:00:00Z'}
        manager=SummaryManager(root,home,args.summary_model,count=1)
        try:
            manager.start([entry])
            deadline=time.monotonic()+180
            while time.monotonic()<deadline:
                state=manager.status(entry)
                if state['status'] in ('ready','unavailable'):
                    break
                time.sleep(.1)
            else:
                raise RuntimeError('single synthetic recap did not finish within the smoke deadline')
            if state['status']!='ready':
                raise RuntimeError(state['detail'])
            print('Single synthetic recap: ready; model='+str(manager.model))
            print(json.dumps(state['recap'],ensure_ascii=True))
        finally:
            manager.close()
        assert source.read_text()==content,'synthetic source changed'
    new_sessions=set((home/'sessions').rglob('*.jsonl'))-before_sessions
    print('Synthetic source unchanged; new browsable session files:',len(new_sessions))
    if new_sessions:
        raise RuntimeError('new session files appeared during smoke; inspect concurrent-session attribution')
    return 0


if __name__=='__main__':
    try:
        sys.exit(main())
    except (RuntimeError,AssertionError) as error:
        print('Synthetic recap smoke:',str(error),file=sys.stderr)
        sys.exit(1)
