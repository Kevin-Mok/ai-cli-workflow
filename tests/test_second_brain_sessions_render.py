"""Full terminal reviews preserve evidence without raw archival Markdown."""
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
    def test_full_report_preserves_every_summary_field_and_metadata(self):
        report=fixture(); original=copy.deepcopy(report)
        entry=report['sessions'][0]
        entry['summary']['blockers']=['Waiting on the original recording.']
        original=copy.deepcopy(report)
        text=sessions.render_terminal(report,width=88)
        flattened=' '.join(text.split())
        for useful in ('1. 💬 Repair joined video','/mnt/usb-8tb/concerts/logic',
                       'Oct 7, 2026 at 1:00 PM EDT','Join the concert videos without a freeze.',
                       'PRIVATE_INTENTION','Waiting on the original recording.',
                       'Verification','Session:',entry['id'],'Source:',entry['source'],
                       'Resume:','codex -C /mnt/usb-8tb/concerts/logic resume',
                       'Review coverage','200','100'):
            self.assertIn(useful,flattened)
        self.assertEqual(flattened.count('Joined the video and verified the transition.'),10)
        self.assertEqual(flattened.count('PRIVATE_VERIFICATION'),40)
        self.assertNotIn('# Private Codex',text)
        self.assertNotIn('--details',text)
        self.assertEqual(report,original)
        self.assertIn('PRIVATE_VERIFICATION',sessions.render(report))

    def test_check_history_preserves_dispositions_ids_and_resolution_times(self):
        report=fixture(); entry=report['sessions'][0]
        entry['checks'][0].update(disposition='checked',resolved_at='2026-10-08T16:00:00Z')
        entry['checks'].append({'id':'d'*64,'key':'dismissed','text':'Dismissed old task.',
                                'disposition':'dismissed','resolved_at':None})
        text=sessions.render_terminal(report)
        flat=' '.join(text.split())
        for value in ('Current checks','Earlier checks','OLD_RETAINED_CHECK','Checked',
                      'Dismissed','a'*64,'b'*64,'d'*64,'Oct 8, 2026 at 12:00 PM EDT'):
            self.assertIn(value,flat)
        self.assertLess(text.index('Current checks'),text.index('Earlier checks'))
        self.assertIn('Next: Listen at the transition.',text)

    def test_next_step_uses_only_current_unresolved_checks(self):
        report=fixture(); entry=report['sessions'][0]; entry['summary']['remaining']=[]
        text=sessions.render_terminal(report,width=64)
        self.assertIn('Next: Check current output.',text)
        self.assertNotIn('Next: OLD_RETAINED_CHECK',text)
        entry['checks'][1]['disposition']='dismissed'
        self.assertNotIn('Next:',sessions.render_terminal(report))
        entry['summary']['checks']=[]
        self.assertNotIn('Next:',sessions.render_terminal(report))

    def test_empty_pending_and_refresh_failure_are_local_to_displayed_recap(self):
        self.assertIn('No work sessions',sessions.render_terminal({'sessions':[]}))
        report=fixture(); report['error']='authentication'
        self.assertNotIn('authentication',sessions.render_terminal(report).split('Review coverage')[0])
        self.assertIn('authentication',sessions.render_terminal(report).split('Review coverage')[1])
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
        self.assertEqual(' '.join(text.split()).count('A next step with a great many words'),40)
        self.assertIn(entry['summary']['remaining'][0],sessions.render(report))
        entry.update(title='',status='stale',reason='source_unavailable')
        self.assertIn('Inferred title',sessions.render_terminal(report))
        self.assertIn('source unavailable',sessions.render_terminal(report))

    def test_directory_headers_and_three_session_rows_are_grouped(self):
        report=fixture(); second=copy.deepcopy(report['sessions'][0]); second['title']='Earlier work'
        third=copy.deepcopy(report['sessions'][0]); third['title']='Other project'; third['cwd']='/project/b'
        report['sessions'] += [second,third]
        text=sessions.render_terminal(report)
        self.assertIn('Recent work directories',text)
        self.assertIn('1. 📁 /mnt/usb-8tb/concerts/logic',text)
        self.assertIn('   1. 💬 Repair joined video',text)
        self.assertIn('   2. 💬 Earlier work',text)
        self.assertIn('2. 📁 /project/b',text)
        self.assertEqual(text.count('1. 📁 /mnt/usb-8tb/concerts/logic'),1)
        self.assertLess(text.index('Earlier work'),text.index('2. 📁 /project/b'))

    def test_resume_preserves_quoted_directory_spaces_and_metadata_is_cleaned(self):
        report=fixture(); entry=report['sessions'][0]
        entry['cwd']='/work/two  spaces'
        entry['source']='/private/source\x1b\x07.jsonl'
        text=sessions.render_terminal(report)
        self.assertIn("codex -C '/work/two  spaces' resume",text)
        self.assertNotIn('\x1b',text)
        self.assertNotIn('\x07',text)

    def test_missing_recap_still_shows_metadata_and_retained_checks(self):
        report=fixture(); entry=report['sessions'][0]; entry['summary']=None
        text=sessions.render_terminal(report)
        for value in ('Recap not generated',entry['id'],'Source:','OLD_RETAINED_CHECK'):
            self.assertIn(value,text)
        self.assertNotIn('Next:',text)

    def test_plain_output_is_ascii_and_no_color_stays_uncolored(self):
        from unittest.mock import patch
        report=fixture(); report['sessions'][0]['title']='Résumé work'
        decorated=sessions.render_terminal(report)
        self.assertIn('🗂',decorated)
        plain=sessions.render_terminal(report,plain=True,width=40)
        self.assertTrue(plain.isascii())
        self.assertIn('Recent work directories',plain)
        self.assertTrue(all(len(line)<=40 for line in plain.splitlines()))
        with patch.dict('os.environ',{'NO_COLOR':'1'}):
            self.assertNotIn('\x1b',sessions.render_terminal(report))

    def test_real_privacy_exclusion_warns_that_recent_work_is_incomplete(self):
        report=fixture(); report['coverage']['restricted']=1
        self.assertIn('Private or uncertain sessions are excluded', sessions.render_terminal(report))
        report['coverage']['restricted']=0
        self.assertNotIn('Private or uncertain sessions are excluded', sessions.render_terminal(report))

    def test_emoji_hierarchy_marks_directory_session_activity_recap_and_next(self):
        text=sessions.render_terminal(fixture())
        for cue in ('📁','💬','🕒','📝','🔜'):
            self.assertIn(cue,text)
        plain=sessions.render_terminal(fixture(),plain=True)
        self.assertTrue(plain.isascii())
        self.assertIn('Recap:',plain)
        self.assertIn('Next:',plain)

    def test_emoji_prefixes_fit_real_terminal_columns(self):
        import unicodedata
        def cells(line):
            return sum(0 if unicodedata.combining(c) or c=='\ufe0f' else
                       2 if unicodedata.east_asian_width(c) in ('W','F') else 1 for c in line)
        report=fixture(); report['sessions'][0]['summary']['accomplishments']=['x'*120, '演奏 🎵 '*30]
        text=sessions.render_terminal(report,width=40)
        self.assertTrue(all(cells(line)<=40 for line in text.splitlines()),text)

    def test_variation_selector_emoji_fit_terminal_columns(self):
        import unicodedata
        report=fixture(); report['sessions'][0]['summary']['accomplishments']=['☀️ '*30]
        text=sessions.render_terminal(report,width=40)
        for line in text.splitlines():
            # Each sun + emoji variation selector occupies two cells.
            base=sum(0 if unicodedata.combining(c) or c=='\ufe0f' else
                     2 if unicodedata.east_asian_width(c) in ('W','F') else 1 for c in line)
            self.assertLessEqual(base+line.count('☀️'),40,line)
        self.assertEqual(text.count('☀️'),30)

    def test_stale_partial_recap_reports_both_limits(self):
        report=fixture(); report['sessions'][0].update(status='stale',reason='changed_source',partial=True)
        text=sessions.render_terminal(report)
        self.assertIn('Recap stale',text)
        self.assertIn('partial conversation',text)

if __name__=='__main__': unittest.main()
