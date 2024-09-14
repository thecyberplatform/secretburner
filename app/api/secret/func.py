from django.utils import timezone
from django.contrib.auth.hashers import check_password
from .models import Verification
from .exceptions import EmailVerificationError


def burn_now(burn_at: int):
    return burn_at < timezone.now().timestamp()


def check_verification(verified_token: str, sender_email: str, recipient_email: str):
    verification = Verification.objects.filter(verified_token=verified_token).first()

    # make sure this token is valid.
    if not verification:
        raise EmailVerificationError("email verification failed")

    # ensure the email is only sent to the correct recipient and from the verified sender.
    if not check_password(sender_email, verification.sender_email_hash):
        raise EmailVerificationError("email verification failed")

    if not check_password(recipient_email, verification.recipient_email_hash):
        raise EmailVerificationError("email verification failed")

    # Get rid of this now. It's used.
    verification.delete()

    return True


def pop_if_in(obj, key):
    if key in obj:
        return obj.pop(key)

    return None
