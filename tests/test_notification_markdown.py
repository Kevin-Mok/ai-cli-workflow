#!/usr/bin/env python3
"""Bold rendering, literal safety and native metadata preservation."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("notification_markdown", ROOT / "dot_config/kitty/notifications.py")
CALLBACK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CALLBACK)

class MarkdownTests(unittest.TestCase):
    def render(self, text):
        self.assertTrue(hasattr(CALLBACK, "markdown_bold"), "Markdown formatter missing")
        return CALLBACK.markdown_bold(text)

    def test_bold_and_multiple_spans(self):
        self.assertEqual(self.render("Done **tests passed**."), "Done <b>tests passed</b>.")
        self.assertEqual(self.render("**one** and **two**"), "<b>one</b> and <b>two</b>")

    def test_literal_html_is_escaped(self):
        self.assertEqual(self.render("**A & <span>**"), "<b>A &amp; &lt;span&gt;</b>")

    def test_code_and_escaped_markers_remain_literal(self):
        self.assertEqual(self.render("`**code**` then **bold**"), "`**code**` then <b>bold</b>")
        self.assertEqual(self.render("```\n**code**\n```\n**bold**"), "```\n**code**\n```\n<b>bold</b>")
        self.assertEqual(self.render(r"\**literal** then **bold**"), r"\**literal** then <b>bold</b>")

    def test_plain_unmatched_and_spaced_markers_unchanged(self):
        for text in ("plain", "**unfinished", "** spaced **", "***nested***", "`**code**`"):
            self.assertIsNone(self.render(text))

    def test_callback_preserves_delivery_metadata(self):
        integration = SimpleNamespace(supports_body_markup=True)
        boss = SimpleNamespace(notification_manager=SimpleNamespace(desktop_integration=integration), window_id_map={})
        command = SimpleNamespace(channel_id=7, application_name="", title="**Ready**", body="**Passed** & <literal>", actions=frozenset({"focus"}), timeout=5000, identifier="abc")
        before = vars(command).copy()
        modules = {"kitty": SimpleNamespace(), "kitty.fast_data_types": SimpleNamespace(get_boss=lambda: boss)}
        with patch.dict(sys.modules, modules):
            self.assertIs(CALLBACK.main(command), False)
        self.assertEqual(str(command.title), "<b>Ready</b>")
        self.assertEqual(str(command.body), "<b>Passed</b> &amp; &lt;literal&gt;")
        self.assertEqual({k: v for k, v in vars(command).items() if k not in ("title", "body")}, {k: v for k, v in before.items() if k not in ("title", "body")})
        # These are the real Kitty backend's markup-neutralizing operations.
        self.assertEqual(command.body.replace("<", "<\u200c").replace("&", "&\u200c"), command.body)
        self.assertEqual(command.body.replace("Passed", "Ready"), "<b>Ready</b> &amp; &lt;literal&gt;")

    def test_markup_replace_accepts_string_index_protocol(self):
        self.assertTrue(hasattr(CALLBACK, "PangoMarkup"))
        class Count:
            def __index__(self):
                return -1
        body = CALLBACK.PangoMarkup("<b>bold</b>")
        self.assertIs(body.replace("<", "<\u200c", Count()), body)

    def test_unsupported_backend_keeps_original(self):
        boss = SimpleNamespace(notification_manager=SimpleNamespace(desktop_integration=SimpleNamespace(supports_body_markup=False)), window_id_map={})
        command = SimpleNamespace(channel_id=0, application_name="", title="**Title**", body="**Body**")
        with patch.dict(sys.modules, {"kitty": SimpleNamespace(), "kitty.fast_data_types": SimpleNamespace(get_boss=lambda: boss)}):
            self.assertIs(CALLBACK.main(command), False)
        self.assertEqual(command.body, "**Body**")

class ActivationTests(unittest.TestCase):
    def test_activation_keeps_existing_manager_state(self):
        path = ROOT / "dot_config/kitty/notification_markdown.py"
        self.assertTrue(path.exists(), "No-UI activation kitten missing")
        handler_module = SimpleNamespace(result_handler=lambda **options: lambda function: function)
        with patch.dict(sys.modules, {"kittens": SimpleNamespace(), "kittens.tui": SimpleNamespace(), "kittens.tui.handler": handler_module}):
            spec = importlib.util.spec_from_file_location("markdown_activation", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        # Kitty executes custom kittens without defining __file__.
        module.__dict__.pop("__file__", None)
        original_state = {"existing": "notification"}
        manager = SimpleNamespace(filter_script=lambda command: False, in_progress_notification_commands=original_state)
        boss = SimpleNamespace(notification_manager=manager)
        with patch.dict(sys.modules, {"kitty.constants": SimpleNamespace(config_dir=str(path.parent))}):
            self.assertEqual(module.handle_result([str(path), "activate"], None, 7, boss), "Notification Markdown active.")
        self.assertIs(manager.in_progress_notification_commands, original_state)
        self.assertEqual(manager.filter_script.__name__, "main")

if __name__ == "__main__":
    unittest.main()
