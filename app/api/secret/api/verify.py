from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from secret.models import Verification
from secret.api.serializers import BaseSerializer
from django.urls import re_path
from core.base.functions.crypto import RandomStringGenerator
from django.contrib.auth.hashers import make_password


class VerifyEmailRequestIn(BaseSerializer):
    to_email = serializers.EmailField(max_length=500, required=False)

    def create(self, validated_data):
        if self._to_email:
            generator = RandomStringGenerator(
                length=6, include_alpha=False, include_symbols=False
            )
            code = generator.generate()

            verification = Verification.objects.create(
                code=code, email_hash=make_password(self._to_email)
            )

            self.send_verified_email(
                additional_context={"code": code},
                template_name="verify-email",
                subject="Secret Burner: Please verify your email",
                bypass_verification_check=True,
            )

            return verification
        else:
            raise ValidationError("no email address to verify.")


class VerifyEmailRequestOut(BaseSerializer):
    verify_id = serializers.CharField(max_length=40)


class VerifyEmailIn(BaseSerializer):
    verify_id = serializers.CharField(max_length=40)
    code = serializers.CharField(max_length=20)

    def create(self, validated_data):
        verification = Verification.objects.filter(
            verify_id=validated_data.get("verify_id")
        ).first()

        if not verification:
            raise serializers.ValidationError("verification failed")

        if verification.code != validated_data.get("code"):
            raise serializers.ValidationError("verification failed")

        generator = RandomStringGenerator(length=128, include_symbols=True)
        verification.verified_token = generator.generate()
        verification.save()

        return verification


class VerifyEmailOut(BaseSerializer):
    ok = serializers.BooleanField()
    verified_token = serializers.CharField()


@api_view(["POST"])
def handle_request_verification(request):
    request_serializer = VerifyEmailRequestIn(data=request.data)

    if request_serializer.is_valid(raise_exception=True):
        verification = request_serializer.save()
        response_data = VerifyEmailRequestOut(verification).data
        return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def handle_verify_request(request):
    request_data = VerifyEmailIn(data=request.data)

    if request_data.is_valid(raise_exception=True):
        verification = request_data.save()
        response_data = VerifyEmailOut(
            {
                "ok": True if verification.verified_token else False,
                "verified_token": verification.verified_token,
            }
        ).data
        return Response(response_data)


urlpatterns = [
    re_path(
        r"^request/$",
        handle_request_verification,
        name="handle_request_verification",
    ),
    re_path(
        r"^$",
        handle_verify_request,
        name="handle_retrieve_secret",
    ),
]
