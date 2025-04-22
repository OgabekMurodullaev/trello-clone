from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from activity_log.models import ActivityLog
from activity_log.permissions import IsOwnerOrMember
from activity_log.serializers import ActivityLogSerializer
from boards.models import Board


# class ActivityLogListView(generics.ListAPIView):
#     queryset = ActivityLog.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = ActivityLogSerializer


class ActivityLogListView(APIView):
    permission_classes = [IsOwnerOrMember]
    serializer_class = ActivityLogSerializer

    def get(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_permissions(request)

        logs = board.logs.all()
        serializer = ActivityLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)