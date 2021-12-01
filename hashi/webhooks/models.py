from django.db import models


class Notification(models.Model):
    gateway = models.PositiveSmallIntegerField()
    raw_notification = models.TextField()
    processed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
