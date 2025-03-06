from django.urls import path

from boards.views import BoardListCreateAPIView, BoardDetailAPIView, TasksListAPIView, TaskListCreateAPIView

urlpatterns = [
    path('', BoardListCreateAPIView.as_view(), name='board_list_create'),
    path('<int:board_id>/', BoardDetailAPIView.as_view(), name='board_get_update_delete'),
    path('<int:board_id>/list/', TasksListAPIView.as_view(), name='tasks_list'),
    path('<int:board_id>/list/create/', TaskListCreateAPIView.as_view(), name='tasks_list_create'),
]