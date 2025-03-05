from django.urls import path

from boards.views import BoardListCreateAPIView, BoardDetailAPIView, TasksListAPIView

urlpatterns = [
    path('', BoardListCreateAPIView.as_view(), name='list_create'),
    path('<int:board_id>/', BoardDetailAPIView.as_view(), name='get_update_delete'),
    path('', TasksListAPIView.as_view(), name='tasks_create'),
]