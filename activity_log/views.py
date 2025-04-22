from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from activity_log.models import ActivityLog
from activity_log.serializers import ActivityLogSerializer


class ActivityLogListView(generics.ListAPIView):
    queryset = ActivityLog.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityLogSerializer
