from django.db import models


class GatewayType(models.IntegerChoices):
    PAYPAL = 1, "PAYPAL"


class NotificationStatus(models.IntegerChoices):
    RECEIVED = 1, "RECEIVED"


class Notification(models.Model):
    gateway = models.PositiveSmallIntegerField(choices=GatewayType.choices)
    raw_notification = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=NotificationStatus.choices, default=NotificationStatus.RECEIVED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
