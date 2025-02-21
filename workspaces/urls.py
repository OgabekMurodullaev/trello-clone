from django.urls import path

from workspaces.views import WorkspaceListCreateAPIView, WorkspaceRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', WorkspaceListCreateAPIView.as_view(), name='workspaces-list-create'),
    path('<int:pk>/', WorkspaceRetrieveUpdateDestroyAPIView.as_view(), name='workspaces-ret-upd-del'),
]