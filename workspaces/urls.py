from django.urls import path

from workspaces.views import WorkspaceListView

urlpatterns = [
    path("", WorkspaceListView.as_view(), name='workspaces'),
]