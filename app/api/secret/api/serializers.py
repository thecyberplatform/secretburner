from rest_framework.serializers import Serializer, CharField
from django.contrib.auth.hashers import make_password
from core.base.functions.data import pop_if_in
from core.base.functions.mail import render_and_send_mail
from secret.func import check_verification, pop_if_in
from secret.exceptions import EmailVerificationError


class BaseSerializer(Serializer):

    def __init__(self, *args, **kwargs):
        self._email_response = None  # future gets/sets are done by class methods.

        self._verified_token = None
        self._sender_email = None
        self._recipient_email = None
        self._allowed_context = {}

        super().__init__(*args, **kwargs)

    def is_valid(self, raise_exception=False):
        self._verified_token = pop_if_in(self.initial_data, "verified_token")
        self._sender_email = pop_if_in(self.initial_data, "sender_email")
        self._recipient_email = pop_if_in(self.initial_data, "recipient_email")

        self._allowed_context["sender_email"] = self._sender_email
        self._allowed_context["recipient_email"] = self._recipient_email

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
    ):
        try:
            # this can raise an EmailVerificationError
            verified = check_verification(
                verified_token=self._verified_token,
                sender_email=self._sender_email,
                recipient_email=self._recipient_email,
            )

            if all([self._recipient_email, self._sender_email, verified]):
                # start building up the context
                final_context = {}

                if context_from_serializer:
                    for key in context_from_serializer:
                        # we have two special fields in this serializer: see is_valid() override.
                        if key in self._allowed_context:
                            final_context[key] = self._allowed_context[key]

                        # don't raise an error, just set the key to None.
                        else:
                            final_context[key] = None

                if additional_context:
                    final_context = final_context | additional_context

                render_and_send_mail(
                    subject=subject,
                    template_name=template_name,
                    context=final_context,
                    recipient_list=[self._recipient_email],
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
