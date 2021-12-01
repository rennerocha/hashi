from django.http import HttpResponse
from webhooks.models import GatewayType, Notification


def paypal_listener(request):
    raw_notification = request.body.decode("utf-8")
    Notification.objects.create(
        gateway=GatewayType.PAYPAL, raw_notification=raw_notification
    )
    return HttpResponse("")
