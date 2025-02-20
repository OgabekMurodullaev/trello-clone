from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workspaces.models import Workspace
from workspaces.serializers import WorkspaceListSerializer


class WorkspaceListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceListSerializer

    def get(self, request):
        workspaces = Workspace.objects.select_related("owner").all()
        serializer = WorkspaceListSerializer(workspaces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
