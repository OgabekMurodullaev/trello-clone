from rest_framework import serializers

from activity_log.models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    board = serializers.StringRelatedField()

    class Meta:
        model = ActivityLog
        fields = ['id', 'board', 'user', 'action_type', 'action_description', 'created_at']