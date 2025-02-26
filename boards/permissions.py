from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if obj.workspace.owner == user:
            return True

        if user in obj.workspace.members.all():
            return request.method in ["GET", "HEAD", "OPTIONS"]

        return False