from django.urls import path

from workspaces.views import WorkspaceListCreateAPIView, WorkspaceRetrieveUpdateDestroyAPIView, WorkspaceMembersListView, InviteMemberToWorkspace, \
    RemoveMemberFromWorkspace, AcceptInvitationView, RejectInvitationView

urlpatterns = [
    path('', WorkspaceListCreateAPIView.as_view(), name='workspaces_list_create'),
    path('<int:pk>/', WorkspaceRetrieveUpdateDestroyAPIView.as_view(), name='workspaces_ret_upd_del'),
    path('<int:workspace_id>/members/', WorkspaceMembersListView.as_view(), name='members_list'),
    path('<int:workspace_id>/invite-member/', InviteMemberToWorkspace.as_view(), name='invite_member'),
    path('<int:workspace_id>/accept/<str:email>/', AcceptInvitationView.as_view(), name='accept_invitation'),
    path('<int:workspace_id>/reject/<str:email>/', RejectInvitationView.as_view(), name='reject_invitation'),
    path('<int:workspace_id>/remove-member/<int:member_id>/', RemoveMemberFromWorkspace.as_view(), name='remove_member'),
]