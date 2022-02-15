from unittest import mock

from django.conf import settings
from django.test import RequestFactory, TestCase
from django.urls import reverse
from webhooks.models import GatewayType, Notification, NotificationStatus
from webhooks.utils import paypal_handshake


class PaypalHandshake(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_set_as_confirmed_when_handshake_is_executed(self):
        request = self.factory.post(
            reverse("webhooks:paypal-listener"),
            content_type="application/x-www-form-urlencoded",
            data="notification_content",
        )
        notification = Notification.objects.create(
            gateway=GatewayType.PAYPAL,
            raw_notification="notification_content",
            status=NotificationStatus.RECEIVED,
        )

        paypal_handshake(request, notification)

        self.assertEqual(notification.status, NotificationStatus.VERIFIED)

    def test_set_as_refused_if_paypal_does_not_accept_handshake(self):
        request = self.factory.post(
            reverse("webhooks:paypal-listener"),
            content_type="application/x-www-form-urlencoded",
            data="notification_content",
        )
        notification = Notification.objects.create(
            gateway=GatewayType.PAYPAL,
            raw_notification="notification_content",
            status=NotificationStatus.RECEIVED,
        )

        paypal_handshake(request, notification)

        self.assertEqual(notification.status, NotificationStatus.INVALID)

    def test_send_message_back_to_paypal_for_verification(self):
        with mock.patch("webhooks.utils.requests.post") as mock_requests:
            request = self.factory.post(
                reverse("webhooks:paypal-listener"),
                content_type="application/x-www-form-urlencoded",
                data="notification_content",
            )
            notification = Notification.objects.create(
                gateway=GatewayType.PAYPAL,
                raw_notification="notification_content",
                status=NotificationStatus.RECEIVED,
            )
            paypal_handshake(request, notification)

            mock_requests.assert_called_with(
                settings.PAYPAL_URL,
                data=notification.raw_notification,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "www.paypal.com",
                },
                verify=True,
            )


# Your listener HTTPS POSTs the complete, unaltered
# message back to PayPal; the message must contain the same fields
# (in the same order) as the original message and be Abel T encoded
# in the same way as the original message.


# PayPal sends a single word back - either VERIFIED
# (if the message matches the original) or INVALID (if the message does not match the original).
