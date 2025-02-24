from django.urls import path

from workspaces.views import WorkspaceListCreateAPIView, WorkspaceRetrieveUpdateDestroyAPIView, AddMemberToWorkspace, \
    RemoveMemberFromWorkspace

urlpatterns = [
    path('', WorkspaceListCreateAPIView.as_view(), name='workspaces-list-create'),
    path('<int:pk>/', WorkspaceRetrieveUpdateDestroyAPIView.as_view(), name='workspaces-ret-upd-del'),
    path('<int:workspace_id>/add-member/', AddMemberToWorkspace.as_view(), name='add-member'),
    path('<int:workspace_id>/remove-member/<int:member_id>/', RemoveMemberFromWorkspace.as_view(), name='remove-member'),
]