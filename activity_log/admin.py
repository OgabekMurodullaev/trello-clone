from django.contrib import admin

from activity_log.models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["id", "board", "user", "action"]
