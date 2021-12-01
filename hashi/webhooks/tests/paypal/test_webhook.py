from django.test import TestCase
from django.urls import reverse

# PayPal HTTPS POSTs an IPN message to your listener that notifies it of an event.
# Your listener returns an empty HTTP 200 response to PayPal.
# Your listener HTTPS POSTs the complete, unaltered message back to PayPal; the message must contain the same fields (in the same order) as the original message and be encoded in the same way as the original message.
# PayPal sends a single word back - either VERIFIED (if the message matches the original) or INVALID (if the message does not match the original).


class PaypalWebhook(TestCase):
    def test_receive_ipn_notification(self):
        response = self.client.post(reverse("webhooks:paypal-listener"))
        self.assertEqual(response.status_code, 200)


# import pytest
# from dynaconf import settings
# from fastapi.testclient import TestClient

# from finance_api.gateways.paypal import paypal_handshake


# @pytest.fixture
# def ipn_message():
#     return {
#         "receiver_email": settings.PAYPAL_ACCOUNT,
#     }


# def test_empty_post_to_paypal_gateway(client):
#     response = client.post("/gateway/paypal")
#     assert response.status_code == 400


# def test_post_with_correct_paypal_user_agent_accepted(mocker, client, ipn_message):
#     paypal_handshake = mocker.patch("finance_api.gateways.paypal.paypal_handshake")

#     response = client.post("/gateway/paypal", data=ipn_message,)
#     assert response.status_code == 200


# def test_valid_paypal_request_trigger_handshake_process(mocker, client, ipn_message):
#     paypal_handshake = mocker.patch("finance_api.gateways.paypal.paypal_handshake")

#     response = client.post("/gateway/paypal", data=ipn_message,)

#     paypal_handshake.assert_called_with(ipn_message)


# def test_raise_error_if_request_to_not_intended_account(mocker, client, ipn_message):
#     ipn_message["receiver_email"] = "not_expected@account.com"
#     response = client.post("/gateway/paypal", data=ipn_message,)
#     assert response.status_code == 400


# def test_do_not_trigger_handshake_process_if_not_intended_account(
#     mocker, client, ipn_message
# ):
#     paypal_handshake = mocker.patch("finance_api.gateways.paypal.paypal_handshake")

#     ipn_message["receiver_email"] = "not_expected@account.com"
#     response = client.post("/gateway/paypal", data=ipn_message,)
#     assert not paypal_handshake.called


# def test_paypal_handshake_send_request_to_verify_url(mocker, client, ipn_message):
#     mock_post_request = mocker.patch("finance_api.gateways.paypal.requests.post")
#     paypal_handshake(ipn_message)

#     mock_post_request.assert_called_with(
#         settings.PAYPAL_VERIFY_IPN_URL, data=ipn_message
#     )


# def test_paypal_after_verified_store_notification_content(mocker, client, ipn_message):
#     mock_response = mocker.patch("finance_api.gateways.paypal.requests.post")
#     mock_response.return_value.text = "VERIFIED"

#     mock_store_notification = mocker.patch(
#         "finance_api.gateways.paypal.store_notification"
#     )

#     paypal_handshake(ipn_message)

#     mock_store_notification.assert_called_with(ipn_message)


# def test_log_error_when_paypal_replied_with_invalid_message_received(
#     mocker, client, ipn_message
# ):
#     mock_response = mocker.patch("finance_api.gateways.paypal.requests.post")
#     mock_response.return_value.text = "INVALID"
#     mock_store_notification = mocker.patch(
#         "finance_api.gateways.paypal.store_notification"
#     )
#     mock_logger_error = mocker.patch("finance_api.gateways.paypal.logger.error")

#     paypal_handshake(ipn_message)

#     mock_logger_error.assert_called()
