from django.db import models

from accounts.models import User
from boards.models import Board


class ActivityLog(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="logs")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actions")
    action = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.board.title} - {self.user}"

    class Meta:
        verbose_name = "ActivityLog"
        verbose_name_plural = "ActivityLogs"

