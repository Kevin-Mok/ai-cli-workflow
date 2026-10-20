#!/usr/bin/env python3
import importlib
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
try:
    desktop = importlib.import_module('media_screensaver.desktop')
except ModuleNotFoundError:
    desktop = None

class DesktopTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(desktop, 'native browser-window coverage is not implemented')

    def test_each_visible_browser_window_needs_its_own_bridge_window(self):
        rect = dict(x=2048,y=0,width=3840,height=2160)
        known = [dict(id=1,state='normal',bounds=rect,videos=[])]
        self.assertIsNotNone(desktop.match_windows([rect],known))
        self.assertIsNone(desktop.match_windows([rect,rect],known))
        self.assertIsNone(desktop.match_windows([],known))

    def test_other_profile_and_minimized_snapshots_do_not_hide_uncovered_window(self):
        left = dict(x=0,y=504,width=2048,height=1152)
        middle = dict(x=2048,y=0,width=3840,height=2160)
        known = [dict(id=1,state='normal',bounds=left,videos=[])]
        self.assertIsNone(desktop.match_windows([middle],known))
        known.append(dict(id=2,state='minimized',bounds=middle,videos=[]))
        self.assertIsNone(desktop.match_windows([middle],known))
        self.assertIsNone(desktop.match_windows([left,middle],known[:1]))
        self.assertIsNotNone(desktop.match_windows([left,dict(middle,visible=False)],known))
        known[1]['state']='fullscreen'
        self.assertIsNotNone(desktop.match_windows([left,middle],known))
    def test_hidden_workspace_is_matched_but_its_video_is_not_displayed(self):
        rect = dict(x=2048,y=0,width=3840,height=2160)
        known = [dict(id=1,state='normal',bounds=rect,videos=[dict(playing=True,rect=rect)])]
        self.assertEqual(desktop.match_windows([dict(rect,visible=False)],known), [])
        self.assertIsNone(desktop.match_windows([dict(rect,visible=False),dict(rect,visible=True)],known))
        self.assertEqual(len(desktop.match_windows([dict(rect,visible=True)],known)), 1)


if __name__ == '__main__': unittest.main()
