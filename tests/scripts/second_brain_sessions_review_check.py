#!/usr/bin/env python3
"""Exercise the installed review CLI with disposable sources and fake inference."""
from __future__ import annotations
import argparse
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from unittest.mock import patch


def check_pager(cli):
    """Run real viewer/navigation against fixture-only state, never native work."""
    import pty
    import select
    import signal
    import shutil
    import time
    if not shutil.which('less'):
        raise RuntimeError('--pager-check requires less; no sudo is used')
    pid, master = pty.fork()
    if pid == 0:
        os.environ['TERM']='xterm-256color'
        try:
            result=cli.main(['sessions','review','--all','--refresh-limit','0'])
        except BaseException:
            os._exit(2)
        os._exit(result)
    reaped=False
    try:
        data=b''; deadline=time.monotonic()+10
        while (b'Recent work directories' not in data or b'refresh recaps' not in data) and time.monotonic()<deadline:
            if select.select([master],[],[],0.1)[0]:
                data+=os.read(master,65536)
        assert b'Recent work directories' in data, 'pager did not show fixture report'
        assert b'refresh recaps' in data and b'Space' in data and b'search' in data, 'pager controls are missing'
        assert os.waitpid(pid,os.WNOHANG)==(0,0), 'pager exited before q'
        # A new eligible work session arrives while the old snapshot is open.
        home=Path(os.environ['CODEX_HOME'])
        sid='00000000-0000-0000-0000-000000000100'
        timestamp='2026-10-08T20:00:00Z'
        rows=[{'type':'session_meta','timestamp':timestamp,
               'payload':{'id':sid,'cwd':'/fixture/refreshed'}},
              {'type':'event_msg','timestamp':timestamp,
               'payload':{'type':'user_message','message':'REFRESH_KEY_FIXTURE'}},
              {'type':'event_msg','timestamp':timestamp,
               'payload':{'type':'agent_message','message':'New work recorded.'}}]
        (home/'sessions'/'100.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in rows))
        with (home/'session_index.jsonl').open('a') as stream:
            stream.write(json.dumps({'id':sid,'thread_name':'New work after refresh'})+'\n')
        os.write(master,b'r')
        refreshed=b''; deadline=time.monotonic()+10
        while b'Fresh recap after refresh' not in refreshed and time.monotonic()<deadline:
            if select.select([master],[],[],0.1)[0]:
                try:refreshed+=os.read(master,65536)
                except OSError:break
        assert b'New work after refresh' in refreshed,'r did not rediscover sessions'
        assert b'Fresh recap after refresh' in refreshed,'r did not generate a missing recap after zero preview'
        assert os.waitpid(pid,os.WNOHANG)==(0,0),'refresh closed the review command'
        os.write(master,b' ')
        time.sleep(0.15)
        os.write(master,b'q')
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            child,status=os.waitpid(pid,os.WNOHANG)
            if child:
                reaped=True
                assert os.waitstatus_to_exitcode(status)==0, 'pager quit failed'
                return
            if select.select([master],[],[],0.1)[0]:
                try:os.read(master,65536)
                except OSError:pass
        raise AssertionError('pager did not quit with q')
    finally:
        if not reaped:
            try:os.killpg(pid,signal.SIGTERM)
            except ProcessLookupError:pass
            os.waitpid(pid,0)
        os.close(master)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-dir', type=Path, default=Path.home()/'scripts',
                        help='Directory containing the installed second_brain package.')
    parser.add_argument('--pager-check', action='store_true',
                        help='Also exercise real bat/less scrolling and q in a disposable PTY.')
    args=parser.parse_args()
    sys.path.insert(0,str(args.runtime_dir.resolve()))
    from second_brain import cli, sessions
    pager_checked=False
    calls=[]
    summary={'title':'Fixture recap','goal':'Finish fixture work','intentions':[],
             'accomplishments':['Implemented the requested change and checked the output.'],
             'remaining':[],'blockers':[],'verification':['Reported fixture checks passed'],
             'checks':[{'key':'manual','text':'Inspect the fixture result.'}]}
    def infer(dialogue, previous):
        calls.append(dialogue)
        value=copy.deepcopy(summary)
        if "REFRESH_KEY_FIXTURE" in dialogue:
            value["goal"]="Fresh recap after refresh"
        return value
    def run(*arguments):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            result=cli.main(['sessions',*arguments])
        assert result==0,(arguments,result,output.getvalue())
        return output.getvalue()
    with tempfile.TemporaryDirectory(prefix='second-brain-review-check-') as temporary:
        base=Path(temporary); home=base/'codex'; (home/'sessions').mkdir(parents=True)
        env={'CODEX_HOME':str(home),'XDG_STATE_HOME':str(base/'state'),
             'SECOND_BRAIN_NOW':'2026-10-08T15:00:00-04:00'}
        def source(number, *, helper=False, directory=None):
            sid=f'00000000-0000-0000-0000-{number:012d}'
            date=(datetime(2026,10,8,10,tzinfo=timezone.utc)+timedelta(minutes=number)).isoformat()
            meta={'id':sid,'cwd':f'/fixture/project-{number if directory is None else directory}'}
            if helper: meta['source']={'subagent':{'other':'guardian'}}
            rows=[{'type':'session_meta','timestamp':date,'payload':meta},
                  {'type':'event_msg','timestamp':date,'payload':{'type':'user_message','message':f'Work {number}'}},
                  {'type':'event_msg','timestamp':date,'payload':{'type':'agent_message','message':'Implemented and tested.'}}]
            (home/'sessions'/f'{number}.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in rows))
            with (home/'session_index.jsonl').open('a') as stream:
                stream.write(json.dumps({'id':sid,'thread_name':f'Work {number}'})+'\n')
        with patch.dict(os.environ,env), patch.object(sessions,'infer',side_effect=infer):
            source(1)
            first=json.loads(run('review','--format','json'))
            cid=first['open_checks'][0]['id']
            sessions.resolve({'schema_version':1,'check_id':cid,'disposition':'dismissed','confirmed':True})
            summary['checks']=[]
            for number in range(2,9): source(number)
            for directory in range(4,9):
                source(10+directory,directory=directory)
                source(20+directory,directory=directory)
            source(99,helper=True)
            default=json.loads(run('review','--format','json'))
            assert [entry['title'] for entry in default['sessions']]==[f'Work {number}' for directory in range(8,3,-1) for number in (20+directory,10+directory,directory)]
            assert default['model_calls']==15 and default['pending_count']==0
            count=len(calls)
            text=run('review')
            assert len(calls)==count and '1. 📁 /fixture/project-8' in text and '5. 📁 /fixture/project-4' in text and '3. 💬 Work 8' in text
            assert '📝 Recap:' in text and 'Implemented the requested change' in text and 'EDT' in text
            assert 'Review coverage' in text and 'Verification reports:' in text and 'Source:' in text
            single=json.loads(run('review','--limit','1','--refresh-limit','0','--format','json'))
            assert len(single['sessions'])==3 and single['model_calls']==0
            details=run('review','--limit','1','--details')
            assert '📝 Recap:' in details and 'Source:' in details and 'Work 7' not in details
            assert details==run('review','--limit','1','--refresh-limit','0')
            assert '# Private Codex' not in details and 'Checks:' in details and 'None reported.' in details
            all_rows=json.loads(run('review','--all','--refresh-limit','0','--format','json'))
            assert len(all_rows['sessions'])==18 and all_rows['model_calls']==0
            retained=next(entry for entry in all_rows['sessions'] if entry['title']=='Work 1')
            assert retained['checks'][0]['id']==cid and retained['checks'][0]['disposition']=='dismissed'
            history=run('review','--all','--refresh-limit','0')
            assert 'Current checks:' in history and 'Dismissed' in history and cid in history
            budget=json.loads(run('review','--all','--refresh-limit','1','--format','json'))
            assert budget['model_calls']==1
            with contextlib.redirect_stderr(io.StringIO()):
                try: cli.build_parser().parse_args(['sessions','review','--all','--limit','1'])
                except SystemExit as error: assert error.code==2
                else: raise AssertionError('conflicting selection accepted')
            assert '📁' in text and '💬' in text and '🕒' in text and '📝' in text
            assert run('review','--no-pager')==run('review')
            assert run('review','--plain').isascii()
            if args.pager_check:
                check_pager(cli)
                pager_checked=True
            refresh=json.loads(run('refresh','--limit','1','--format','json'))
            assert 'sessions' not in refresh and 'open_checks' not in refresh
    print(json.dumps({'runtime':str(args.runtime_dir.resolve()),'default_directories':5,'sessions_per_directory':3,'default_sessions':15,
                      'unchanged_model_calls':0,'helpers_excluded':True,'dispositions_preserved':True,
                      'live_state_modified':False,'interactive_pager_verified':pager_checked,'refresh_key_verified':pager_checked}))
    return 0

if __name__=='__main__': raise SystemExit(main())
