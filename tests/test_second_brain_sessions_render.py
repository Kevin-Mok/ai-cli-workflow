"""Compact review shows progress; full evidence stays in details."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from second_brain import sessions


def fixture():
    summary={'title':'Inferred title','goal':'Join the concert videos without a freeze.',
             'intentions':['PRIVATE_INTENTION'],'accomplishments':['Joined the video and verified the transition. '*10],
             'remaining':['Listen at the transition.'],'blockers':[],
             'verification':['PRIVATE_VERIFICATION '*40],
             'checks':[{'key':'current','text':'Check current output.'}]}
    entry={'key':'c'*64,'cwd':'/mnt/usb-8tb/concerts/logic','title':'Repair joined video',
           'id':'01a0e91e-9594-7002-8319-45e8d058e513','source':'/private/session.jsonl',
           'last_activity':'2026-10-07T17:00:26.860Z','summarized_at':None,
           'status':'ready','reason':'','summary':summary,
           'checks':[{'id':'a'*64,'key':'old','text':'OLD_RETAINED_CHECK','disposition':'open'},
                     {'id':'b'*64,'key':'current','text':'Check current output.','disposition':'open'}]}
    return {'sessions':[entry],'pending_count':2,'backlog_count':200,
            'coverage':{'partial':1,'unknown':200,'hidden':100},'error':None}


class TerminalRenderTests(unittest.TestCase):
    def test_numbered_progress_and_toronto_activity_without_global_noise(self):
        report=fixture(); original=copy.deepcopy(report)
        text=sessions.render_terminal(report,width=64)
        for useful in ('1. Repair joined video','/mnt/usb-8tb/concerts/logic','Oct 7, 2026','1:00 PM EDT',
                       'Joined the video','Next: Listen at the transition.','--details'):
            self.assertIn(useful,text)
        for noise in ('OLD_RETAINED_CHECK','PRIVATE_','queued','Coverage:','hidden','Source:',report['sessions'][0]['id']):
            self.assertNotIn(noise,text)
        self.assertTrue(all(len(line)<=64 for line in text.splitlines()))
        recap=text.split('Recap: ',1)[1].split('Next: ',1)[0]
        self.assertLessEqual(len(recap.strip().splitlines()),2)
        self.assertEqual(report,original)
        self.assertIn('PRIVATE_VERIFICATION',sessions.render(report))
        self.assertIn('OLD_RETAINED_CHECK',sessions.render(report))

    def test_next_step_uses_only_current_unresolved_checks(self):
        report=fixture(); entry=report['sessions'][0]; entry['summary']['remaining']=[]
        text=sessions.render_terminal(report,width=64)
        self.assertIn('Next: Check current output.',text)
        self.assertNotIn('OLD_RETAINED_CHECK',text)
        entry['checks'][1]['disposition']='dismissed'
        self.assertNotIn('Next:',sessions.render_terminal(report))
        entry['summary']['checks']=[]
        self.assertNotIn('Next:',sessions.render_terminal(report))

    def test_empty_pending_and_refresh_failure_are_local_to_displayed_recap(self):
        self.assertIn('No work sessions',sessions.render_terminal({'sessions':[]}))
        report=fixture(); report['error']='authentication'
        self.assertNotIn('authentication',sessions.render_terminal(report))
        entry=report['sessions'][0]
        entry.update(summary=None,status='pending')
        self.assertIn('Recap not generated',sessions.render_terminal(report))
        entry.update(status='failed',reason='authentication')
        self.assertIn('authentication',sessions.render_terminal(report))
        entry['summary']=fixture()['sessions'][0]['summary']
        self.assertIn('stale',sessions.render_terminal(report).lower())

    def test_long_words_and_full_details_preserved(self):
        report=fixture(); entry=report['sessions'][0]
        entry['cwd']='/'+'long-project-'*15
        entry['summary']['remaining']=['A next step with a great many words '*20]
        text=sessions.render_terminal(report,width=40)
        self.assertTrue(all(len(line)<=40 for line in text.splitlines()))
        next_lines=text.split('Next:',1)[1].split('\n\n',1)[0].splitlines()
        self.assertEqual(len(next_lines),1)
        self.assertIn(entry['summary']['remaining'][0],sessions.render(report))
        entry.update(title='',status='stale',reason='source_unavailable')
        self.assertIn('Inferred title',sessions.render_terminal(report))
        self.assertIn('source unavailable',sessions.render_terminal(report))

    def test_selected_sessions_stay_in_global_order_even_when_projects_repeat(self):
        report=fixture(); second=copy.deepcopy(report['sessions'][0]); second['title']='Other project'
        second['cwd']='/project/b'; third=copy.deepcopy(report['sessions'][0]); third['title']='Earlier work'
        report['sessions'] += [second,third]
        text=sessions.render_terminal(report)
        self.assertLess(text.index('1. Repair'),text.index('2. Other'))
        self.assertLess(text.index('2. Other'),text.index('3. Earlier'))
        self.assertEqual(text.count('/mnt/usb-8tb/concerts/logic'),2)

    def test_plain_output_is_ascii_and_no_color_stays_uncolored(self):
        from unittest.mock import patch
        report=fixture(); report['sessions'][0]['title']='Résumé work'
        decorated=sessions.render_terminal(report)
        self.assertIn('🗂',decorated)
        plain=sessions.render_terminal(report,plain=True,width=40)
        self.assertTrue(plain.isascii())
        self.assertIn('Recent work sessions',plain)
        self.assertTrue(all(len(line)<=40 for line in plain.splitlines()))
        with patch.dict('os.environ',{'NO_COLOR':'1'}):
            self.assertNotIn('\x1b',sessions.render_terminal(report))

if __name__=='__main__': unittest.main()
