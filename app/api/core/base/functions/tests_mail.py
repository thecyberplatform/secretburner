import unittest
from unittest.mock import patch, MagicMock
from .mail import send_mail, build_email_templates, render_and_send_mail, settings


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


class TestRenderAndSendMail(unittest.TestCase):

    @patch("core.base.functions.mail.send_mail")
    @patch("core.base.functions.mail.build_email_templates")
    def test_render_and_send_mail_valid(
        self, mock_build_email_templates, mock_send_mail
    ):
        # Mock the return value of build_email_templates
        mock_build_email_templates.return_value = (
            "<html>Content</html>",
            "Text Content",
        )

        subject = "Test Subject"
        template_name = "test_template"
        context = {"key": "value"}
        recipient_list = ["recipient@example.com"]

        # Call the function
        render_and_send_mail(subject, template_name, context, recipient_list)

        # Assert build_email_templates was called with the correct arguments
        mock_build_email_templates.assert_called_once_with(
            html_template=f"email/html/{template_name}.html",
            text_template=f"email/text/{template_name}.txt",
            context=context,
        )

        # Assert send_mail was called with the correct arguments
        mock_send_mail.assert_called_once_with(
            subject=subject,
            message="Text Content",
            from_email=settings.MAILER_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message="<html>Content</html>",
        )
