from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from workspaces.filters import MembersFilter
from workspaces.models import Workspace, WorkspaceMember, WorkspaceInvitation
from workspaces.permissions import IsOwnerOrMember
from workspaces.serializers import WorkspaceSerializer, MemberSerializer, AddMemberWorkspaceSerializer, InviteMemberSerializer
from workspaces.tasks import send_invite_email


class WorkspaceListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        return Workspace.objects.select_related("owner").all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        data = {
            'detail': 'Workspace created successfully',
            'data': serializer.data
        }

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class WorkspaceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrMember]
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        return Workspace.objects.select_related("owner").all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Workspace successfully deleted"}, status=status.HTTP_200_OK)


class WorkspaceMembersListView(ListAPIView):
    queryset = WorkspaceMember.objects.all()
    permission_classes = [IsOwnerOrMember]
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MembersFilter


class InviteMemberToWorkspace(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InviteMemberSerializer

    def post(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, id=workspace_id, owner=request.user)
        serializer = InviteMemberSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            invited_user = User.objects.filter(email=email).first()

            if WorkspaceInvitation.objects.filter(workspace=workspace, email=email, status='pending').exists():
                return Response({"detail": "Bu foydalanuvchiga allaqachon taklif yuborilgan"}, status=status.HTTP_400_BAD_REQUEST)

            WorkspaceInvitation.objects.create(
                workspace=workspace,
                invited_by=request.user,
                invite_user=invited_user,
                email = email
            )

            accept_url = f"http://127.0.0.1:8000/api/workspaces/{workspace_id}/accept/{email}/"
            reject_url = f"http://127.0.0.1:8000/api/workspaces/{workspace_id}/reject/{email}/"
            send_invite_email.delay(workspace.name, email, accept_url, reject_url)
            return Response({"detail": "Taklif yuborildi"}, status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AcceptInvitationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InviteMemberSerializer

    def post(self, request, workspace_id, email):
        invitation = get_object_or_404(WorkspaceInvitation, workspace_id=workspace_id, email=email, status='pending')

        if invitation.email != request.user.email:
            return Response({"detail": "Bu taklif siz uchun atalmagan"}, status=status.HTTP_403_FORBIDDEN)

        if invitation.accept():
            return Response({"detail": "Siz workspace' ga muvaffaqiyatli qo'shildingiz"}, status=status.HTTP_200_OK)
        return Response({"detail": "Taklif allaqachon qabul qilingan yoki rad etilgan."}, status=status.HTTP_400_BAD_REQUEST)


class RejectInvitationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InviteMemberSerializer

    def post(self, request, workspace_id, email):
        invitation = get_object_or_404(WorkspaceInvitation, workspace_id=workspace_id, email=email, status='pending')

        if invitation.email != request.user.email:
            return Response({"detail": "Bu taklif siz uchun atalmagan"}, status=status.HTTP_403_FORBIDDEN)

        if invitation.reject():
            return Response({"detail": "Taklifni rad etdingiz"}, status=status.HTTP_200_OK)
        return Response({"detail": "Taklif allaqachon qabul qilingan yoki rad etilgan"}, status=status.HTTP_400_BAD_REQUEST)


class RemoveMemberFromWorkspace(DestroyAPIView):
    permission_classes = [IsOwnerOrMember]
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