from unittest import mock

from django.test import TestCase
from django.urls import reverse
from webhooks.models import GatewayType, Notification, NotificationStatus

VALID_IPN_NOTIFICATION = "transaction_subject=Transaction Title&payment_date=03:19:29 Nov 30, 2021 PST&txn_type=subscr_payment&subscr_id=I-U5J6K5LBNHJ5&last_name=Raybon&residence_country=BR&item_name=Transaction Title&payment_gross=&mc_currency=BRL&business=contact@receiver.com&payment_type=instant&protection_eligibility=Eligible&verify_sign=AvdDeOMbtfESfLs445gdB-d7.oTyA1cGOw.6du8LpfTZO9OqFvwscLQW&payer_status=verified&payer_email=payer@email.com&txn_id=3FDS5R43543G49105&receiver_email=receiver@email.com&first_name=Abel&payer_id=FWF4354GFGDFG&receiver_id=432F43F4VL7P8&item_number=transaction-title&payment_status=Completed&payment_fee=&mc_fee=5.40&btn_id=423543424&mc_gross=75.00&charset=windows-1252&notify_version=3.9&ipn_track_id=f45345435vc48"


class PaypalWebhook(TestCase):
    def test_receive_ipn_notification(self):
        with mock.patch("webhooks.views.paypal_handshake.delay"):
            response = self.client.post(
                reverse("webhooks:paypal-ipn-listener"),
                content_type="application/x-www-form-urlencoded",
                data=VALID_IPN_NOTIFICATION,
            )
            self.assertEqual(response.status_code, 200)

    def test_received_ipn_notification_stored_as_received(self):
        with mock.patch("webhooks.views.paypal_handshake.delay"):
            self.client.post(
                reverse("webhooks:paypal-ipn-listener"),
                content_type="application/x-www-form-urlencoded",
                data=VALID_IPN_NOTIFICATION,
            )

            self.assertTrue(
                Notification.objects.filter(
                    gateway=GatewayType.PAYPAL,
                    raw_notification=VALID_IPN_NOTIFICATION,
                    status=NotificationStatus.RECEIVED,
                ).exists()
            )

    def test_received_ipn_notification_trigger_paypal_handshake(self):
        with mock.patch(
            "webhooks.views.paypal_handshake.delay"
        ) as mock_paypal_handshake:
            self.client.post(
                reverse("webhooks:paypal-ipn-listener"),
                content_type="application/x-www-form-urlencoded",
                data=VALID_IPN_NOTIFICATION,
            )
            notification = Notification.objects.filter(
                gateway=GatewayType.PAYPAL,
                raw_notification=VALID_IPN_NOTIFICATION,
                status=NotificationStatus.RECEIVED,
            ).first()

            mock_paypal_handshake.assert_called_with(notification)
