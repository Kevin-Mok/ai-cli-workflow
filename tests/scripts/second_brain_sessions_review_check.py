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
from unittest.mock import patch


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-dir', type=Path, default=Path.home()/'scripts',
                        help='Directory containing the installed second_brain package.')
    args=parser.parse_args()
    sys.path.insert(0,str(args.runtime_dir.resolve()))
    from second_brain import cli, sessions
    calls=[]
    summary={'title':'Fixture recap','goal':'Finish fixture work','intentions':[],
             'accomplishments':['Implemented the requested change and checked the output.'],
             'remaining':[],'blockers':[],'verification':['Reported fixture checks passed'],
             'checks':[{'key':'manual','text':'Inspect the fixture result.'}]}
    def infer(dialogue, previous):
        calls.append(dialogue)
        return copy.deepcopy(summary)
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
        def source(number, *, helper=False):
            sid=f'00000000-0000-0000-0000-{number:012d}'
            date=f'2026-10-08T{number+10 if not helper else 23}:00:00Z'
            meta={'id':sid,'cwd':f'/fixture/project-{number}'}
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
            source(99,helper=True)
            default=json.loads(run('review','--format','json'))
            assert [entry['title'] for entry in default['sessions']]==['Work 8','Work 7','Work 6','Work 5','Work 4']
            assert default['model_calls']==5 and default['pending_count']==0
            count=len(calls)
            text=run('review')
            assert len(calls)==count and '1. Work 8' in text and '5. Work 4' in text
            assert 'Recap: Implemented' in text and 'EDT' in text and 'Coverage:' not in text
            single=json.loads(run('review','--limit','1','--refresh-limit','0','--format','json'))
            assert len(single['sessions'])==1 and single['model_calls']==0
            details=run('review','--limit','1','--details')
            assert 'Reported accomplishments:' in details and 'Source:' in details and 'Work 7' not in details
            all_rows=json.loads(run('review','--all','--refresh-limit','0','--format','json'))
            assert len(all_rows['sessions'])==8 and all_rows['model_calls']==0
            retained=next(entry for entry in all_rows['sessions'] if entry['title']=='Work 1')
            assert retained['checks'][0]['id']==cid and retained['checks'][0]['disposition']=='dismissed'
            budget=json.loads(run('review','--all','--refresh-limit','1','--format','json'))
            assert budget['model_calls']==1
            with contextlib.redirect_stderr(io.StringIO()):
                try: cli.build_parser().parse_args(['sessions','review','--all','--limit','1'])
                except SystemExit as error: assert error.code==2
                else: raise AssertionError('conflicting selection accepted')
            refresh=json.loads(run('refresh','--limit','1','--format','json'))
            assert 'sessions' not in refresh and 'open_checks' not in refresh
    print(json.dumps({'runtime':str(args.runtime_dir.resolve()),'default_sessions':5,
                      'unchanged_model_calls':0,'helpers_excluded':True,'dispositions_preserved':True,
                      'live_state_modified':False}))
    return 0

if __name__=='__main__': raise SystemExit(main())
