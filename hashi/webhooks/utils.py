import requests
from django.conf import settings
from django_rq import job
from webhooks.models import NotificationStatus


@job
def paypal_handshake(notification):
    """
    PayPal IPN Listener flow is documented at:
    https://developer.paypal.com/api/nvp-soap/ipn/IPNIntro/
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.paypal.com",
    }
    data = f"cmd=_notify-validate&{notification.raw_notification}"
    validation_response = requests.post(
        settings.PAYPAL_URL,
        data=data,
        headers=headers,
        verify=True,
    )
    validation_response.raise_for_status()

    if validation_response.text == "VERIFIED":
        notification.status = NotificationStatus.VERIFIED
    elif validation_response.text == "INVALID":
        notification.status = NotificationStatus.INVALID
    notification.save()
