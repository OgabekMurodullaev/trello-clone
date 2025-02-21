from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workspaces.models import Workspace
from workspaces.permissions import IsOwner
from workspaces.serializers import WorkspaceSerializer


class WorkspaceListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        return Workspace.objects.select_related("owner").all()

    def perform_create(self, serializer):
        workspace = serializer.save(owner=self.request.user)
        data = {
            "detail": "Workspace successfully created",
            "data": WorkspaceSerializer(workspace).data
        }
        return Response(data, status=status.HTTP_201_CREATED)


class WorkspaceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        return Workspace.objects.select_related("owner").all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Workspace successfully deleted"}, status=status.HTTP_200_OK)