from django.db import models

from accounts.models import User
from boards.models import Board


class ActivityLog(models.Model):
    class ActionType(models.TextChoices):
        CREATED = 'created', 'Created'
        UPDATED = 'updated', 'Updated'
        DELETED = 'deleted', 'Deleted'
        MOVED = 'moved', 'Moved'
        COMMENTED = 'commented', 'Commented'
        COMPLETED = 'completed', 'Completed'
        OTHER = 'other', 'Other'

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="logs")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actions")
    action_type = models.CharField(max_length=20, choices=ActionType.choices, default=ActionType.OTHER)
    action_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M')}] {self.user} {self.action_type} - {self.action_description}"



    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-created_at']