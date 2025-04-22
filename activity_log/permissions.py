from rest_framework.permissions import BasePermission

from boards.models import Board


class IsOwnerOrMember(BasePermission):
    def has_permission(self, request, view):
        board_id = view.kwargs.get("board_id")

        board = Board.objects.filter(id=board_id).first()
        if not board:
            return False

        if not request.user.is_authenticated:
            return False

        if board.workspace.owner == request.user:
            return True

        if request.user in board.member.all():
            return True

        return False
