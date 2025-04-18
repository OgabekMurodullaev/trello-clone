from django.urls import path

from checklists.views import CheckListCreateAPIView, CheckListDetailAPIView, CheckListItemListCreateAPIView

urlpatterns = [
    path('', CheckListCreateAPIView.as_view(), name='get_and_create'),
    path('<int:list_id>/', CheckListDetailAPIView.as_view(), name='detail'),
    path('<int:checklist_id>/items/', CheckListItemListCreateAPIView.as_view(), name='items_get_create'),
]