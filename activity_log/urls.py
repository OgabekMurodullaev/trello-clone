from django.urls import path

from activity_log.views import ActivityLogListView

urlpatterns = [
    path('', ActivityLogListView.as_view(), name='list')
]