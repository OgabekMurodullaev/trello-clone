from rest_framework import serializers

from workspaces.models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Workspace
        fields = ("id", "name", "owner", "owner_email", "created_at")
        read_only_fields = ("id", "owner", "owner_email", "created_at")