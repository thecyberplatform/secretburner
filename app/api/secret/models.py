from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.conf import settings
import math


def set_burn_at(seconds: int):
    return math.floor(
        (timezone.now() + timezone.timedelta(seconds=float(seconds))).timestamp()
    )


class Secret(models.Model):
    secret_id = models.TextField(primary_key=True, default=uuid4)
    secret_text = models.TextField(null=True)
    expiry_seconds = models.IntegerField(default=3600)
    burn_at = models.BigIntegerField(db_index=True)
    passphrase_hash = models.TextField(null=True)
    public_key = models.TextField(null=True)
    request_id = models.TextField(null=True, db_index=True)
    fulfilment_id = models.TextField(null=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.burn_at:
            self.burn_at = set_burn_at(seconds=int(self.expiry_seconds))
        super().save(*args, **kwargs)


class Verification(models.Model):
    verify_id = models.TextField(primary_key=True, default=uuid4)
    burn_at = models.BigIntegerField(db_index=True)
    code = models.TextField(max_length=20, db_index=True)
    verified_token = models.TextField(null=True, db_index=True)
    sender_email_hash = models.TextField(null=False)
    recipient_email_hash = models.TextField(null=False)

    def save(self, *args, **kwargs):
        if not self.burn_at:
            self.burn_at = set_burn_at(
                seconds=settings.EMAIL_VERIFICATION_EXPIRY_SECONDS
            )
        super().save(*args, **kwargs)
