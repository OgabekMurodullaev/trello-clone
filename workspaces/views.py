from rest_framework import status, generics
from rest_framework.generics import get_object_or_404, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workspaces.models import Workspace, WorkspaceMember
from workspaces.permissions import IsOwner
from workspaces.serializers import WorkspaceSerializer, AddMemberWorkspaceSerializer


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


class AddMemberToWorkspace(APIView):
    serializer_class = AddMemberWorkspaceSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_workspace(self):
        return get_object_or_404(Workspace, id=self.kwargs["workspace_id"], owner=self.request.user)

    def post(self, request, *args, **kwargs):
        workspace = self.get_workspace()
        serializer = AddMemberWorkspaceSerializer(data=request.data, context={"workspace": workspace})

        if serializer.is_valid():
            serializer.save()
            data = {
                "success": True,
                "message": f"Foydalanuvchi {workspace.name} ish maydoniga muvaffaqiyatli qo'shildi",
                "data": serializer.data
            }
            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveMemberFromWorkspace(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = AddMemberWorkspaceSerializer

    def get_object(self):
        workspace = get_object_or_404(Workspace, id=self.kwargs['workspace_id'], owner=self.request.user)
        return get_object_or_404(WorkspaceMember, workspace=workspace, member_id=self.kwargs['member_id'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "success": True,
                "message": f"{instance.member.email} foydalanuvchisi {instance.workspace.name} ish maydonidan o'chirildi"
            },
            status=status.HTTP_200_OK
        )