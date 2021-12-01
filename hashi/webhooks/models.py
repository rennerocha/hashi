from django.db import models


class GatewayType(models.IntegerChoices):
    PAYPAL = 1, "PAYPAL"


class Notification(models.Model):
    gateway = models.PositiveSmallIntegerField(choices=GatewayType.choices)
    raw_notification = models.TextField()
    processed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
