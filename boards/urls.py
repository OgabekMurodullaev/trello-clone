from django.urls import path

from boards.views import BoardListCreateAPIView, BoardDetailAPIView, TasksListAPIView, TaskListCreateAPIView, \
    TaskListDetailAPIView

urlpatterns = [
    path('', BoardListCreateAPIView.as_view(), name='board_list_create'),
    path('<int:board_id>/', BoardDetailAPIView.as_view(), name='board_get_update_delete'),
    path('<int:board_id>/lists/', TasksListAPIView.as_view(), name='tasks_list'),
    path('<int:board_id>/lists/create/', TaskListCreateAPIView.as_view(), name='tasks_list_create'),
    path('<int:board_id>/lists/<int:list_id>/', TaskListDetailAPIView.as_view(), name='tasks_list_get_update_delete')
]