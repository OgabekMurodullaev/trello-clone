from django.db import models

from accounts.models import User


class Workspace(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workspaces")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name} - owner {self.owner.email}"

    class Meta:
        verbose_name = "Workspace"
        verbose_name_plural = "Workspaces"


class WorkspaceMember(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.workspace.name} - {self.member.email}"

    class Meta:
        verbose_name = "WorkspaceMember"
        verbose_name_plural = "WorkspaceMembers"


class Board(models.Model):
    VISIBILITY_CHOICES = (
        ('Private', 'private'),
        ('Public', 'public'),
        ('Workspace', 'workspace')
    )

    title = models.CharField(max_length=120)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="boards")
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    background = models.ImageField(upload_to='board-backgrounds/', null=True, blank=True)

    def __str__(self):
        return f"{self.workspace.name} - {self.title}"

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"


class List(models.Model):
    title = models.CharField(max_length=120)
    colour = models.ImageField(upload_to='list-colours/')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")

    def __str__(self):
        return f"{self.board.title} - {self.title}"

    class Meta:
        verbose_name = "List"
        verbose_name_plural = "Lists"

class Card(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="cards")
    due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.list.title} - {self.title}"

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
