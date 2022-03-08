from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from webhooks.models import GatewayType, Notification
from webhooks.utils import paypal_handshake


@csrf_exempt
def paypal_listener(request):
    raw_notification = request.body.decode("utf-8")
    notification = Notification.objects.create(
        gateway=GatewayType.PAYPAL, raw_notification=raw_notification
    )
    paypal_handshake.delay(notification)
    return HttpResponse("")
