import unittest
from unittest.mock import patch, MagicMock
from .mail import send_mail, build_email_templates


class EmailFunctionTests(unittest.TestCase):

    @patch("core.base.functions.mail.django_send_mail")
    @patch("core.base.functions.mail.settings")
    def test_01_send_mail_enabled(self, mock_settings, mock_send_mail):
        mock_settings.ALLOW_EMAIL = True
        send_mail("Subject", "Message", "from@localhost", ["to@localhost"])
        mock_send_mail.assert_called_once()

    @patch("core.base.functions.mail.django_send_mail")
    @patch("core.base.functions.mail.settings")
    def test_02_send_mail_disabled(self, mock_settings, mock_send_mail):
        mock_settings.ALLOW_EMAIL = False
        send_mail("Subject", "Message", "from@localhost", ["to@localhost"])
        mock_send_mail.assert_not_called()

    @patch("core.base.functions.mail.get_template")
    def test_03_build_email_templates(self, mock_get_template):
        # Mock the template and its render method
        mock_template = MagicMock()
        mock_template.render.return_value = "Rendered Content"
        mock_get_template.return_value = mock_template

        html_content, text_content = build_email_templates(
            "html_template.html", "text_template.txt", {"key": "value"}
        )

        # Assert both templates were called and rendered correctly
        self.assertEqual(html_content, "Rendered Content")
        self.assertEqual(text_content, "Rendered Content")
        mock_get_template.assert_any_call("html_template.html")
        mock_get_template.assert_any_call("text_template.txt")
        mock_template.render.assert_called_with({"key": "value"})
