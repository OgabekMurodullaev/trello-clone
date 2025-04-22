from django.urls import path

from activity_log.views import ActivityLogListView

urlpatterns = [
    path('<int:board_id>/', ActivityLogListView.as_view(), name='list')
]