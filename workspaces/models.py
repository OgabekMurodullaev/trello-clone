from django.db import models
from django.utils import timezone
from django.utils.timezone import now

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


class WorkspaceInvitation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="invitations")
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invitations")
    invite_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_invitations", null=True, blank=True)
    email = models.EmailField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.invited_by} - {self.invite_user} - {self.status}"

    class Meta:
        verbose_name = "WorkspaceInvitation"
        verbose_name_plural = "WorkspaceInvitations"

    def accept(self):
        if self.status != self.Status.PENDING:
            return False
        self.status = self.Status.ACCEPTED
        self.save()
        WorkspaceMember.objects.create(workspace=self.workspace, member=self.invite_user)
        return True

    def reject(self):
        if self.status != self.Status.PENDING:
            return False
        self.status = self.Status.REJECTED
        self.save()
        return True