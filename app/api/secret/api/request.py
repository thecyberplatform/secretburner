from uuid import uuid4
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from secret.models import Secret
from secret.func import burn_now
from django.urls import re_path
from django.conf import settings

from secret.api.serializers import (
    BaseSerializer,
    SerializerWithEmailResponse,
    handle_passphrase,
)


class RequestIn(BaseSerializer):
    expiry_seconds = serializers.IntegerField(min_value=60)
    passphrase = serializers.CharField(max_length=500, required=False)
    public_key = serializers.CharField(max_length=4096, required=False)
    recipient_email = serializers.EmailField(required=False)
    sender_email = serializers.EmailField(required=False)
    verified_token = serializers.CharField(required=False)

    def is_valid(self, raise_exception=False):
        self.initial_data = handle_passphrase(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        validated_data["request_id"] = str(uuid4())
        request_url = f"{settings.UI_HOSTNAME}{settings.UI_FULFIL_REQUEST_URI}{validated_data.get('request_id')}"

        self.send_verified_email(
            context_from_serializer=["sender_email"],
            additional_context={"request_url": request_url},
            template_name="secret-request",
            subject="Secret Burner: Somebody is requesting a secret from you",
        )

        return Secret.objects.create(**validated_data)


class RequestOut(SerializerWithEmailResponse):
    secret_id = serializers.CharField()
    request_id = serializers.CharField()
    burn_at = serializers.IntegerField()


class RequestFulfilmentRetrievalIn(BaseSerializer):
    request_id = serializers.CharField(max_length=40)

    def save(self, **kwargs):
        request_id = self.validated_data.get("request_id")
        secret = Secret.objects.filter(request_id=request_id).first()

        if not secret:
            raise serializers.ValidationError("request not found.")

        if burn_now(secret.burn_at):
            secret.delete()
            raise serializers.ValidationError("request not found.")

        if secret.fulfilment_id:
            raise serializers.ValidationError("request not found.")

        secret.fulfilment_id = uuid4()
        secret.save()

        return secret


class RequestFulfilmentRetrievalOut(BaseSerializer):
    request_id = serializers.CharField()
    fulfilment_id = serializers.CharField()
    public_key = serializers.CharField(required=False)


class RequestFulfilmentIn(BaseSerializer):
    request_id = serializers.CharField(max_length=40)
    fulfilment_id = serializers.CharField(max_length=40)
    secret_text = serializers.CharField(max_length=512000)
    recipient_email = serializers.EmailField(required=False)
    sender_email = serializers.EmailField(required=False)
    verified_token = serializers.CharField(required=False)

    def update(self, instance: Secret, validated_data):
        instance.secret_text = validated_data.get("secret_text")
        instance.save()

        self.send_verified_email(
            context_from_serializer=["sender_email"],
            template_name="request-fulfilled",
            subject="Secret Burner: Your secret request has been fulfilled",
        )

        return instance


class RequestFulfilmentOut(SerializerWithEmailResponse):
    request_id = serializers.CharField(max_length=40)
    burn_at = serializers.IntegerField()


@api_view(["POST"])
def handle_store_request(request):
    request_data = RequestIn(data=request.data)

    if request_data.is_valid(raise_exception=True):
        secret = request_data.save()
        response_data = RequestOut(
            secret, email_response=request_data.get_email_response()
        ).data
        return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def handle_retrieve_request_fulfilment(request):
    request_data = RequestFulfilmentRetrievalIn(data=request.data)

    if request_data.is_valid(raise_exception=True):
        secret = request_data.save()
        response_data = RequestFulfilmentRetrievalOut(secret).data
        return Response(response_data)


@api_view(["POST"])
def handle_fulfil_request(request):
    secret = Secret.objects.filter(
        fulfilment_id=request.data.get("fulfilment_id")
    ).first()
    if not secret:
        raise serializers.ValidationError("request not found or never existed")

    request_data = RequestFulfilmentIn(secret, data=request.data)

    if request_data.is_valid(raise_exception=True):
        secret = request_data.save()
        response_data = RequestFulfilmentOut(
            secret, email_response=request_data.get_email_response()
        ).data
        return Response(response_data)


urlpatterns = [
    re_path(
        r"^$",
        handle_store_request,
        name="handle_store_request",
    ),
    re_path(
        r"^retrieve/$",
        handle_retrieve_request_fulfilment,
        name="handle_retrieve_request",
    ),
    re_path(
        r"^fulfil/$",
        handle_fulfil_request,
        name="handle_fulfil_request",
    ),
]
