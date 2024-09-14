from typing import List
from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.template.loader import get_template

from core.base.functions.data import contains_invalid_characters


def send_mail(*args, **kwargs):
    """
    Sends an email only if the email sending feature is enabled in the settings.

    This function wraps Django's `send_mail` function, adding a conditional check to ensure
    that emails are only sent when the `ALLOW_EMAIL` setting is true. This is useful for
    controlling email sending in different environments (e.g., development, testing, production).

    Parameters:
        *args: Variable length argument list passed directly to `django_send_mail`.
        **kwargs: Arbitrary keyword arguments passed directly to `django_send_mail`.
    """
    if settings.ALLOW_EMAIL is True:
        django_send_mail(*args, **kwargs)


def build_email_templates(
    html_template: str = None, text_template: str = None, context=None
):
    """
    Renders specified HTML and text templates with the provided context.

    This function is designed to load and render email templates, returning the rendered HTML
    and text content. It supports both HTML and text formats to accommodate different email clients.

    Parameters:
        html_template (str, optional): The path to the HTML template to render.
        text_template (str, optional): The path to the text template to render.
        context (dict, optional): A dictionary containing context variables to render the templates with.

    Returns:
        tuple: A tuple containing the rendered HTML content and text content.
    """
    rendered_html = ""
    rendered_text = ""

    if html_template:
        template_html = get_template(html_template)
        rendered_html = template_html.render(context)

    if text_template:
        template_text = get_template(text_template)
        rendered_text = template_text.render(context)

    return rendered_html, rendered_text


def render_and_send_mail(
    subject: str, template_name: str, context: object, recipient_list: List[str]
):
    # check the template. If there are any characters that are 0-9, a-Z or hyphens/underscores,
    # just bail out of this function.
    if contains_invalid_characters(template_name):
        raise Exception("Invalid template name")

    # render the templates
    rendered_html, rendered_text = build_email_templates(
        html_template=f"email/html/{template_name}.html",
        text_template=f"email/text/{template_name}.txt",
        context=context,
    )

    # send the email
    send_mail(
        subject=subject,
        message=rendered_text,
        from_email=settings.MAILER_FROM_EMAIL,
        recipient_list=recipient_list,
        html_message=rendered_html,
    )
