from unittest import mock

from django.conf import settings
from django.test import RequestFactory, TestCase
from webhooks.models import GatewayType, Notification, NotificationStatus
from webhooks.utils import paypal_handshake

VALID_IPN_NOTIFICATION = "transaction_subject=Transaction Title&payment_date=03:19:29 Nov 30, 2021 PST&txn_type=subscr_payment&subscr_id=I-U5J6K5LBNHJ5&last_name=Raybon&residence_country=BR&item_name=Transaction Title&payment_gross=&mc_currency=BRL&business=contact@receiver.com&payment_type=instant&protection_eligibility=Eligible&verify_sign=AvdDeOMbtfESfLs445gdB-d7.oTyA1cGOw.6du8LpfTZO9OqFvwscLQW&payer_status=verified&payer_email=payer@email.com&txn_id=3FDS5R43543G49105&receiver_email=receiver@email.com&first_name=Abel&payer_id=FWF4354GFGDFG&receiver_id=432F43F4VL7P8&item_number=transaction-title&payment_status=Completed&payment_fee=&mc_fee=5.40&btn_id=423543424&mc_gross=75.00&charset=windows-1252&notify_version=3.9&ipn_track_id=f45345435vc48"


class PaypalHandshake(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_set_as_confirmed_when_handshake_is_executed(self):
        with mock.patch("webhooks.utils.requests.post") as mock_requests:
            mock_requests.return_value.text = "VERIFIED"

            notification = Notification.objects.create(
                gateway=GatewayType.PAYPAL,
                raw_notification=VALID_IPN_NOTIFICATION,
                status=NotificationStatus.RECEIVED,
            )

            paypal_handshake(notification)

            self.assertEqual(notification.status, NotificationStatus.VERIFIED)

    def test_set_as_refused_if_paypal_does_not_accept_handshake(self):
        with mock.patch("webhooks.utils.requests.post") as mock_requests:
            mock_requests.return_value.text = "INVALID"

            notification = Notification.objects.create(
                gateway=GatewayType.PAYPAL,
                raw_notification=VALID_IPN_NOTIFICATION,
                status=NotificationStatus.RECEIVED,
            )

            paypal_handshake(notification)

            self.assertEqual(notification.status, NotificationStatus.INVALID)

    def test_send_message_back_to_paypal_for_verification(self):
        with mock.patch("webhooks.utils.requests.post") as mock_requests:

            notification = Notification.objects.create(
                gateway=GatewayType.PAYPAL,
                raw_notification=VALID_IPN_NOTIFICATION,
                status=NotificationStatus.RECEIVED,
            )
            paypal_handshake(notification)

            mock_requests.assert_called_with(
                settings.PAYPAL_URL,
                data=f"cmd=_notify-validate&{notification.raw_notification}",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "www.paypal.com",
                },
                verify=True,
            )
