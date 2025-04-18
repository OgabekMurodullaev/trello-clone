from django.urls import path

from checklists.views import CheckListCreateAPIView, CheckListDetailAPIView, CheckListItemListCreateAPIView, \
    CheckListItemDetailAPIView

urlpatterns = [
    path('', CheckListCreateAPIView.as_view(), name='get_and_create'),
    path('<int:checklist_id>/', CheckListDetailAPIView.as_view(), name='detail'),
    path('<int:checklist_id>/items/', CheckListItemListCreateAPIView.as_view(), name='items_get_create'),
    path('<int:checklist_id>/items/<int:item_id>/', CheckListItemDetailAPIView.as_view(), name='item_detail'),
]