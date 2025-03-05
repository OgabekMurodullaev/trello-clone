from rest_framework import serializers

from boards.models import Board, List
from workspaces.models import Workspace, WorkspaceMember
from workspaces.serializers import WorkspaceSerializer


class BoardSerializer(serializers.ModelSerializer):
    workspace = serializers.SerializerMethodField(method_name="get_workspace")
    workspace_id = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.all(),
        write_only=True
    )

    class Meta:
        model = Board
        fields = ('id', 'title', 'workspace', 'workspace_id', 'visibility', 'background')

    def get_workspace(self, obj):
        return {"id": obj.workspace.id, "name": obj.workspace.name}

    def validate_workspace_id(self, value):
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("Siz bu Workspace egasi emassiz.")
        return value

    def create(self, validated_data):
        workspace = validated_data.pop('workspace_id')
        board = Board.objects.create(workspace=workspace, **validated_data)
        return board
