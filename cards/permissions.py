from rest_framework.permissions import BasePermission


class IsOwnerOrCardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        card_member_ids = obj.members.values_list("user", flat=True)

        if user == obj.list.board.workspace.owner or user.id in card_member_ids:
            return True
        return False


class CanDeleteAttachment(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        upload_by = obj.uploaded_by
        if user == obj.list.board.workspace.owner or user == upload_by:
            return True
        return False