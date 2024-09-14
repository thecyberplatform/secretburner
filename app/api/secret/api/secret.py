from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from secret.api.serializers import (
    BaseSerializer,
    SerializerWithEmailResponse,
    handle_passphrase,
)

from django.contrib.auth.hashers import check_password

from secret.models import Secret
from secret.func import burn_now
from django.urls import re_path
from django.conf import settings


class SecretIn(BaseSerializer):
    secret_text = serializers.CharField(max_length=512000)
    expiry_seconds = serializers.IntegerField(min_value=60)
    passphrase = serializers.CharField(max_length=500, required=False)
    passphrase_hash = serializers.CharField(required=False, read_only=True)
    public_key = serializers.CharField(max_length=4096, required=False)
    recipient_email = serializers.EmailField(required=False)
    sender_email = serializers.EmailField(required=False)
    verified_token = serializers.CharField(required=False)

    def is_valid(self, raise_exception=False):
        self.initial_data = handle_passphrase(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        secret = Secret.objects.create(**validated_data)
        secret_url = (
            f"{settings.UI_HOSTNAME}{settings.UI_VIEW_SECRET_URL}{secret.secret_id}"
        )

        self.send_verified_email(
            context_from_serializer=["sender_email"],
            additional_context={"secret_url": secret_url},
            template_name="secret-ready",
            subject="Secret Burner: Somebody has sent you a secret",
        )

        return secret


class SecretOut(SerializerWithEmailResponse):
    secret_id = serializers.CharField()
    burn_at = serializers.IntegerField()


class SecretRetrieveIn(BaseSerializer):
    secret_id = serializers.CharField(max_length=40)
    passphrase = serializers.CharField(max_length=500, required=False)

    def save(self, **kwargs):
        secret_id = self.validated_data.get("secret_id")
        passphrase = self.validated_data.get("passphrase")

        secret = Secret.objects.filter(secret_id=secret_id).first()

        if not secret:
            raise serializers.ValidationError("secret not found")

        if secret.passphrase_hash and not check_password(
            password=passphrase, encoded=secret.passphrase_hash
        ):
            raise serializers.ValidationError("secret not found")

        if burn_now(secret.burn_at):
            secret.delete()
            raise serializers.ValidationError("secret not found")

        return secret


class SecretRetrieveOut(BaseSerializer):
    secret_text = serializers.CharField()
    burn_at = serializers.IntegerField()
    passphrase_encrypted = serializers.BooleanField()
    pki_encrypted = serializers.BooleanField()


class SecretRetrieveCheckIn(BaseSerializer):
    secret_id = serializers.CharField(max_length=40)

    def save(self, **kwargs):
        secret_id = self.validated_data.get("secret_id")
        secret = Secret.objects.filter(secret_id=secret_id).first()

        if not secret:
            raise serializers.ValidationError("secret not found")

        return secret


class SecretRetrieveCheckOut(BaseSerializer):
    passphrase_protected = serializers.BooleanField()


@api_view(["POST"])
def handle_store_secret(request):
    request_data = SecretIn(data=request.data)

    if request_data.is_valid(raise_exception=True):
        secret = request_data.save()
        response_data = SecretOut(
            secret, email_response=request_data.get_email_response()
        ).data
        return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def handle_retrieve_secret_check(request):
    request_serializer = SecretRetrieveCheckIn(data=request.data)

    if request_serializer.is_valid(raise_exception=True):
        secret = request_serializer.save()

        response_obj = {
            "passphrase_protected": False,
        }

        if secret.passphrase_hash:
            response_obj["passphrase_protected"] = True

        response_data = SecretRetrieveCheckOut(response_obj).data
        return Response(response_data)


@api_view(["POST"])
def handle_retrieve_secret(request):
    request_serializer = SecretRetrieveIn(data=request.data)

    if request_serializer.is_valid(raise_exception=True):
        secret = request_serializer.save()

        response_obj = {
            "secret_text": secret.secret_text,
            "burn_at": secret.burn_at,
            "passphrase_encrypted": False,
            "pki_encrypted": False,
        }

        if secret.request_id and secret.public_key:
            response_obj["pki_encrypted"] = True

        elif not secret.request_id and secret.public_key:
            response_obj["pki_encrypted"] = True

        elif not secret.request_id and secret.passphrase_hash:
            response_obj["passphrase_encrypted"] = True
        else:
            # Nothing to do.
            pass

        response_data = SecretRetrieveOut(response_obj).data
        secret.delete()
        return Response(response_data)


urlpatterns = [
    re_path(
        r"^$",
        handle_store_secret,
        name="handle_store_secret",
    ),
    re_path(
        r"^retrieve/$",
        handle_retrieve_secret,
        name="handle_retrieve_secret",
    ),
    re_path(
        r"^check/$",
        handle_retrieve_secret_check,
        name="handle_retrieve_secret_check",
    ),
]
