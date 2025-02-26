from rest_framework import serializers

from boards.models import Board
from workspaces.models import Workspace
from workspaces.serializers import WorkspaceSerializer


class BoardSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer(read_only=True)
    workspace_id = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.all(),
        write_only=True,
        source="workspace"
    )

    class Meta:
        model = Board
        fields = ('id', 'title', 'workspace', 'workspace_id', 'visibility', 'background')