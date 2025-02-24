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
    is_active = models.BooleanField(default=False)
    invited_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.workspace.name} - {self.member.email}"

    class Meta:
        unique_together = ('workspace', 'member')
        verbose_name = "WorkspaceMember"
        verbose_name_plural = "WorkspaceMembers"
