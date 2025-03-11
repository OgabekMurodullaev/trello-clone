from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from workspaces.models import Workspace, WorkspaceMember


class WorkspaceSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Workspace
        fields = ("id", "name", "owner", "owner_email", "created_at")
        read_only_fields = ("id", "owner", "owner_email", "created_at")


class MemberSerializer(serializers.ModelSerializer):
    member = UserSerializer()

    class Meta:
        model = WorkspaceMember
        fields = ("id", "member", "is_active")

class AddMemberWorkspaceSerializer(serializers.ModelSerializer):
    member_email = serializers.EmailField(write_only=True)
    workspace = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WorkspaceMember
        fields = ("workspace", "member_email")

    def validate_member_email(self, value):
        try:
            return User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Bunday foydalanuvchi topilmadi.")

    def create(self, validated_data):
        workspace = self.context["workspace"]
        member = validated_data["member_email"]

        if WorkspaceMember.objects.filter(workspace=workspace, member=member).exists():
            raise serializers.ValidationError({"detail": "Ushbu foydalanuvchi allaqachon qo'shilgan"})

        return WorkspaceMember.objects.create(workspace=workspace, member=member)


class InviteMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
