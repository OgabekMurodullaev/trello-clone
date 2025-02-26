from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from boards.models import Board
from boards.serializers import BoardSerializer
from boards.permissions import IsOwnerOrReadOnly
from workspaces.models import WorkspaceMember


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="id",
            type=int,
            location=OpenApiParameter.PATH,
            required=True,
            description="Board ID"
        )
    ]
)
class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workspace', 'visibility']
    search_fields = ["title"]
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user

        if getattr(self, "swagger_fake_view", False):
            return Board.objects.none()

        workspaces = WorkspaceMember.objects.filter(member=user, is_active=True).values_list("workspace_id", flat=True)

        return Board.objects.filter(workspace_id__in=workspaces)