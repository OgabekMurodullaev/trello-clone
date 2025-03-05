from rest_framework import serializers

from boards.models import Board, TaskList
from workspaces.models import Workspace


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


class TaskListSerializer(serializers.ModelSerializer):
    board = serializers.SerializerMethodField(method_name="get_board")
    board_id = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), write_only=True)

    class Meta:
        model = TaskList
        fields = ('id', 'title', 'board', 'board_id', 'colour')

    def get_board(self, obj):
        return {"id", obj.board.id, "title", obj.board.title}

    def validate_board_id(self, value):
        user = self.context['request'].user
        if user != value.workspace.owner and user not in value.workspace.members.all():
            raise serializers.ValidationError("Siz ushbu workspace egasi/a'zosi emassiz")
        return value

    def create(self, validated_data):
        board = validated_data['board_id']
        t_list = TaskList.objects.create(board=board, **validated_data)
        return t_list