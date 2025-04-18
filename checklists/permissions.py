from rest_framework.permissions import BasePermission

class IsCardMemberOrWorkspaceOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        card = None

        if hasattr(obj, 'card'):
            card = obj.card
        elif hasattr(obj, 'checklist') and hasattr(obj.checklist, 'card'):
            card = obj.checklist.card

        if not card:
            return False

        is_member = card.members.filter(user=request.user).exists()

        is_owner = (card.list.board.workspace.owner == request.user)

        return is_member or is_owner