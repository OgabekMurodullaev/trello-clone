from django.db import models

from workspaces.models import Workspace


class Board(models.Model):
    VISIBILITY_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('workspace', 'Workspace')
    )

    title = models.CharField(max_length=120)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="boards")
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    background = models.ImageField(upload_to='board-backgrounds/', null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.workspace.name} - {self.title}"

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"

class TaskList(models.Model):
    title = models.CharField(max_length=120)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")

    objects = models.Manager()

    def __str__(self):
        return f"{self.board.title} - {self.title}"

    class Meta:
        verbose_name = "TaskList"
        verbose_name_plural = "TaskLists"