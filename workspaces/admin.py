from django.contrib import admin

from workspaces.models import Workspace, WorkspaceMember, WorkspaceInvitation


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'created_at')
    search_fields = ('name', 'owner__email')
    list_filter = ('created_at',)


@admin.register(WorkspaceInvitation)
class WorkspaceInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'workspace', 'invite_user', 'status')
    search_fields = ('workspace__name', 'email')

@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'workspace', 'member', "is_active", "invited_at")
    search_fields = ('workspace__name', 'member__email')
