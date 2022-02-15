import requests
from django.conf import settings
from django_rq import job
from webhooks.models import NotificationStatus


@job
def paypal_handshake(request, notification):
    notification.status = NotificationStatus.VERIFIED
    notification.save()

    # notification["cmd"] = "_notify-validate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.paypal.com",
    }
    validation_response = requests.post(
        settings.PAYPAL_URL,
        data=notification.raw_notification,
        headers=headers,
        verify=True,
    )
    validation_response.raise_for_status()
