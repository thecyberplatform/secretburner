from rest_framework.serializers import Serializer, CharField
from django.conf import settings
from django.contrib.auth.hashers import make_password
from core.base.functions.data import pop_if_in, contains_invalid_characters
from core.base.functions.mail import send_mail, build_email_templates
from secret.func import check_verification, pop_if_in
from secret.exceptions import EmailVerificationError


class BaseSerializer(Serializer):

    def __init__(self, *args, **kwargs):
        self._email_response = None  # future gets/sets are done by class methods.

        self._verified_token = None
        self._from_email = None
        self._to_email = None
        self._allowed_context = {}

        super().__init__(*args, **kwargs)

    def is_valid(self, raise_exception=False):
        self._verified_token = pop_if_in(self.initial_data, "verified_token")
        self._from_email = pop_if_in(self.initial_data, "from_email")
        self._to_email = pop_if_in(self.initial_data, "to_email")

        self._allowed_context["from_email"] = self._from_email
        self._allowed_context["to_email"] = self._to_email

        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        attrs["passphrase_hash"] = self.initial_data.get("passphrase_hash")
        return attrs

    def send_verified_email(
        self,
        template_name,
        subject,
        context_from_serializer=None,
        additional_context=None,
        bypass_verification_check=False,
    ):
        try:
            # We only do this if emails are enabled.
            if settings.ALLOW_EMAIL:
                if bypass_verification_check:
                    verified = True
                else:
                    # This can raise an EmailVerificationError
                    verified = check_verification(
                        verified_token=self._verified_token, email=self._from_email
                    )

                if self._to_email and verified:
                    # start building up the context
                    final_context = {}

                    if context_from_serializer:
                        for key in context_from_serializer:
                            # # find the key from the validated data of the serializer
                            # if key in self.validated_data:
                            #     final_context[key] = self.validated_data.get(key)

                            # we have two special fields in this serializer: see is_valid() override.
                            if key in self._allowed_context:
                                final_context[key] = self._allowed_context[key]

                            # don't raise an error, just set the key to None.
                            else:
                                final_context[key] = None

                    if additional_context:
                        final_context = final_context | additional_context

                    # check the template. If there are any characters that are 0-9, a-Z or hyphens/underscores,
                    # just bail out of this function.
                    if contains_invalid_characters(template_name):
                        raise Exception("Invalid template name")

                    rendered_html, rendered_text = build_email_templates(
                        html_template=f"email/html/{template_name}.html",
                        text_template=f"email/text/{template_name}.txt",
                        context=final_context,
                    )

                    send_mail(
                        subject=subject,
                        message=rendered_text,
                        from_email=settings.MAILER_FROM_EMAIL,
                        recipient_list=[self._to_email],
                        html_message=rendered_html,
                    )

                    self.set_email_response("ok")

        except EmailVerificationError as e:
            self.set_email_response(str(e))

        except Exception as e:
            raise e

    def get_email_response(self):
        return self._email_response

    def set_email_response(self, value):
        self._email_response = value


class SerializerWithEmailResponse(BaseSerializer):
    email_response = CharField(default=None, allow_blank=True)

    def __init__(self, *args, email_response=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_email_response(email_response)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        if self.get_email_response():
            response["email_response"] = self.get_email_response()
        return response


def handle_passphrase(initial_data):
    passphrase = pop_if_in(initial_data, "passphrase")

    if passphrase:
        initial_data["passphrase_hash"] = make_password(passphrase)

    return initial_data
