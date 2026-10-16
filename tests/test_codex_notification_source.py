"""Source attribution and temporary outline lifecycle never compromise audio."""
import importlib.util
import os
from pathlib import Path
import struct
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]


class SourceTests(unittest.TestCase):
    def setUp(self):
        path = ROOT / 'scripts/codex_notification_source.py'
        self.assertTrue(path.exists(), 'optional source module is not implemented')
        spec = importlib.util.spec_from_file_location('notification_source', path)
        self.source = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.source)

    def test_proc_identity_handles_parentheses_and_start_time(self):
        fields = ['S', '21'] + ['0'] * 17 + ['4567'] + ['0'] * 4
        with patch.object(Path, 'read_text', return_value='42 (a tricky ) name) ' + ' '.join(fields)):
            self.assertEqual(self.source._process(42), (21, 4567))
        self.assertIsNone(self.source._process(-1))

    def test_real_ancestry_includes_current_process(self):
        chain = self.source._ancestry()
        self.assertEqual(chain[0]['pid'], os.getpid())
        self.assertGreater(chain[0]['start'], 0)

    def test_capture_prefers_verified_tmux_and_does_not_fall_back_for_unknown_pane(self):
        with patch.dict(os.environ, {'TMUX': '/tmp/server,51,0', 'TMUX_PANE': '%7'}), patch.object(self.source, '_ancestry', return_value=[{'pid': 8, 'start': 9}]), patch.object(self.source, '_capture_tmux', return_value={'kind': 'tmux'}) as tmux, patch.object(self.source, '_capture_x11') as x11:
            self.assertEqual(self.source.capture_source(), {'kind': 'tmux'})
            tmux.return_value = None
            self.assertIsNone(self.source.capture_source())
            x11.assert_not_called()

    def test_unavailable_capture_and_invalid_payload_are_silent(self):
        with patch.object(self.source, '_ancestry', side_effect=OSError('gone')):
            self.assertIsNone(self.source.capture_source())
        for payload in (None, {}, {'kind': 'other'}, {'kind': 'x11', 'window': 'no'}, []):
            with self.subTest(payload=payload):
                with self.source.outline(payload):
                    pass

    def test_outline_setup_failure_preserves_body_and_body_error_is_not_suppressed(self):
        with patch.object(self.source, '_open_outline', side_effect=RuntimeError('no display')):
            with self.source.outline({'kind': 'x11'}):
                ran = True
            self.assertTrue(ran)
        with self.assertRaisesRegex(RuntimeError, 'player failed'):
            with self.source.outline(None):
                raise RuntimeError('player failed')

    def test_outline_always_closes_after_playback_and_ignores_close_failure(self):
        closer = Mock()
        with patch.object(self.source, '_open_outline', return_value=closer):
            with self.assertRaisesRegex(TimeoutError, 'player timeout'):
                with self.source.outline({'kind': 'x11'}):
                    closer.close.assert_not_called()
                    raise TimeoutError('player timeout')
            closer.close.assert_called_once()
            closer.close.side_effect = RuntimeError('already destroyed')
            with self.source.outline({'kind': 'x11'}):
                pass

    def test_tmux_requires_server_and_pane_process_ancestry(self):
        chain = [{'pid': 8, 'start': 9}]
        with patch.dict(os.environ, {'TMUX': '/tmp/server,51,0', 'TMUX_PANE': '%7'}), patch.object(self.source, '_tmux', return_value='51\t8\t%7\t@3'), patch.object(self.source, '_process', side_effect=lambda pid: (1, {8: 9, 51: 100}[pid])):
            captured = self.source._capture_tmux(chain)
            self.assertEqual(captured['pane'], '%7')
            self.assertEqual(captured['owner'], chain[0])
            self.assertEqual(captured['server'], {'pid': 51, 'start': 100})
            self.assertIsNone(self.source._capture_tmux([{'pid': 8, 'start': 10}]))
        with patch.dict(os.environ, {'TMUX': '/tmp/server,52,0', 'TMUX_PANE': '%7'}), patch.object(self.source, '_tmux', return_value='51\t8\t%7\t@3'):
            self.assertIsNone(self.source._capture_tmux(chain))

    def test_x11_requires_unique_owned_kitty_window(self):
        owner = {'pid': 42, 'start': 999}
        kitty = SimpleNamespace(id=17, get_wm_class=lambda: ('kitty', 'kitty'), get_full_property=lambda *args: SimpleNamespace(value=[42]))
        root = SimpleNamespace(get_full_property=lambda *args: SimpleNamespace(value=[17]))
        display = SimpleNamespace(screen=lambda: SimpleNamespace(root=root), intern_atom=lambda *args, **kwargs: 1, create_resource_object=lambda *args: kitty, close=Mock())
        with patch.dict(os.environ, {'DISPLAY': ':1'}), patch.object(self.source, '_x11_display', return_value=display):
            self.assertEqual(self.source._capture_x11([owner]), {'kind': 'x11', 'display': ':1', 'window': 17, 'owner': owner})
            root.get_full_property = lambda *args: SimpleNamespace(value=[17, 18])
            self.assertIsNone(self.source._capture_x11([owner]))
            root.get_full_property = lambda *args: SimpleNamespace(value=[17])
            kitty.get_wm_class = lambda: ('other', 'other')
            self.assertIsNone(self.source._capture_x11([owner]))

    def test_x11_stale_pid_never_opens_outline(self):
        captured = {'kind': 'x11', 'display': ':1', 'window': 17, 'owner': {'pid': 42, 'start': 999}}
        with patch.object(self.source, '_process', return_value=(1, 1000)), patch.object(self.source, '_x11_display') as display:
            with self.source.outline(captured):
                pass
            display.assert_not_called()

    def test_x11_shape_ring_is_click_through_and_resize_updates_geometry(self):
        owner = {'pid': 42, 'start': 999}
        constants = SimpleNamespace(StructureNotifyMask=1, CopyFromParent=0, Unsorted=0, Above=0)
        shape = SimpleNamespace(SO=SimpleNamespace(Set=0), SK=SimpleNamespace(Input=2, Bounding=0))
        child = Mock()
        parent = Mock()
        parent.create_window.return_value = child
        parent.get_geometry.return_value = SimpleNamespace(width=100, height=80)
        display = Mock()
        display.create_resource_object.return_value = parent
        display.shape_query_version.return_value = SimpleNamespace(major_version=1, minor_version=1)
        colormap = display.screen.return_value.default_colormap
        colormap.alloc_named_color.side_effect = AttributeError('legacy Xlib uses removed string.atoi')
        colormap.alloc_color.return_value.pixel = 123
        modules = {'Xlib.X': constants, 'Xlib.ext.shape': shape}
        with patch.object(self.source, '_x11_display', return_value=display), patch.object(self.source, '_owned_windows', return_value=[(17, owner)]), patch.object(self.source, '_identity', return_value=owner), patch.object(self.source.importlib, 'import_module', side_effect=lambda name: modules[name]), patch.object(self.source.threading, 'Thread') as thread:
            ring = self.source._X11Outline({'display': ':1', 'window': 17}, owner)
            colormap.alloc_color.assert_called_once_with(0x8F8F, 0xBCBC, 0x8F8F)
            colormap.alloc_named_color.assert_not_called()
            child.shape_rectangles.assert_any_call(0, 2, 0, 0, 0, [])
            child.shape_rectangles.assert_any_call(0, 0, 0, 0, 0, self.source._ring_rectangles(100, 80))
            parent.set_input_focus.assert_not_called()
            ring._resize(120, 90)
            child.shape_rectangles.assert_any_call(0, 0, 0, 0, 0, self.source._ring_rectangles(120, 90))
            ring.close()
            thread.return_value.join.assert_called_once()
            ring._destroy()
            child.destroy.assert_called_once()
            display.close.assert_called_once()

    def test_ring_is_two_pixels_and_empty_inside(self):
        rectangles = self.source._ring_rectangles(100, 80)
        self.assertEqual(rectangles, [(0, 0, 100, 2), (0, 78, 100, 2), (0, 2, 2, 76), (98, 2, 2, 76)])
        self.assertTrue(all(w > 0 and h > 0 for _, _, w, h in self.source._ring_rectangles(1, 1)))

    def test_legacy_shape_input_uses_protocol_kind_without_old_enum_validation(self):
        try:
            rq = importlib.import_module('Xlib.protocol.rq')
        except ImportError:
            self.skipTest('optional python3-xlib is unavailable')
        ring = self.source._X11Outline.__new__(self.source._X11Outline)
        ring.shape = SimpleNamespace()
        ring.constants = SimpleNamespace(Unsorted=0)
        ring.child = Mock(id=17)
        ring.child.display.get_extension_major.return_value = 129
        with patch.object(self.source.importlib, 'import_module', return_value=rq):
            ring._input_shape()
        request = ring.child.display.send_request.call_args.args[0]
        self.assertEqual(struct.unpack('=BBHBBBBIhh', request._binary),
                         (129, 1, 4, 0, 2, 0, 0, 17, 0, 0))
        ring.child.shape_rectangles.assert_not_called()

    def test_x11_interrupted_setup_closes_connection_and_propagates_exit(self):
        display = Mock()
        with patch.object(self.source, '_x11_display', return_value=display), patch.object(self.source, '_owned_windows', side_effect=SystemExit(143)):
            with self.assertRaises(SystemExit):
                self.source._X11Outline({'display': ':1', 'window': 17}, {'pid': 42, 'start': 999})
        display.close.assert_called_once()

    def test_tmux_interrupted_setup_restores_applied_style_and_propagates_exit(self):
        captured = {'kind': 'tmux', 'socket': '/tmp/server', 'pane': '%7', 'window': '@3', 'owner': {'pid': 8, 'start': 9}, 'server': {'pid': 51, 'start': 100}}
        local = {'pane-border-style': None, 'pane-active-border-style': None}
        def tmux(socket, *args):
            if args[0] == 'display-message':
                return '51\t8\t%7\t@3'
            name = args[-1] if args[0] == 'show-options' or '-u' in args else args[-2]
            if args[0] == 'show-options':
                return (local[name] or '') if '-v' in args else (name + ' value' if local[name] is not None else '')
            if '-u' in args:
                local[name] = None
            else:
                local[name] = args[-1]
                if name == 'pane-active-border-style':
                    raise SystemExit(143)
            return ''
        with patch.object(self.source, '_process', side_effect=lambda pid: (1, {8: 9, 51: 100}[pid])), patch.object(self.source, '_tmux', side_effect=tmux):
            with self.assertRaises(SystemExit):
                with self.source.outline(captured):
                    self.fail('interrupted setup must never start playback')
        self.assertEqual(local, {'pane-border-style': None, 'pane-active-border-style': None})

    def test_tmux_restores_exact_local_styles_and_inheritance(self):
        captured = {'kind': 'tmux', 'socket': '/tmp/server', 'pane': '%7', 'window': '@3', 'owner': {'pid': 8, 'start': 9}, 'server': {'pid': 51, 'start': 100}}
        local = {'pane-border-style': None, 'pane-active-border-style': 'fg=blue,bg=black'}
        effective = {'pane-border-style': 'fg=grey', 'pane-active-border-style': local['pane-active-border-style']}
        mutations = []
        def tmux(socket, *args):
            if args[0] == 'display-message':
                return '51\t8\t%7\t@3'
            name = args[-1] if args[0] == 'show-options' else args[-2] if args[-2] in local else args[-1]
            if args[0] == 'show-options':
                if '-v' in args:
                    return (effective[name] if '-A' in args else local[name]) or ''
                return '' if local[name] is None else name + ' ' + local[name]
            mutations.append(args)
            if '-u' in args:
                local[name] = None
            else:
                local[name] = args[-1]
            return ''
        with patch.object(self.source, '_process', side_effect=lambda pid: (1, {8: 9, 51: 100}[pid])), patch.object(self.source, '_tmux', side_effect=tmux):
            with self.source.outline(captured):
                self.assertIn('#{==:#{pane_id},%7}', local['pane-border-style'])
                self.assertIn('#8FBC8F', local['pane-active-border-style'])
            self.assertEqual(local, {'pane-border-style': None, 'pane-active-border-style': 'fg=blue,bg=black'})
            with self.source.outline(captured):
                local['pane-active-border-style'] = 'fg=red'
            self.assertEqual(local['pane-active-border-style'], 'fg=red')
            self.assertTrue(mutations)


if __name__ == '__main__':
    unittest.main()
