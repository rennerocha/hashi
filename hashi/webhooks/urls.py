from django.urls import path
from webhooks import views

app_name = "webhooks"

urlpatterns = [
    path("paypal", views.paypal_listener, name="paypal-ipn-listener"),
]
