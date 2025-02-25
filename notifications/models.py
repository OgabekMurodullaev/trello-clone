from django.db import models

from accounts.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

