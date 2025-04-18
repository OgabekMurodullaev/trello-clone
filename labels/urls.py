from django.urls import path
from .views import LabelListCreateAPIView, LabelRetrieveUpdateDestroyAPIView, CardLabelCreateAPIView, CardLabelDeleteAPIView


urlpatterns = [
    path('', LabelListCreateAPIView.as_view(), name='list_and_create'),
    path('<int:id>/', LabelRetrieveUpdateDestroyAPIView.as_view(), name='label_detail'),
    path('<int:card_id>/label/create/', CardLabelCreateAPIView.as_view(), name='create_card_label'),
    path('<int:card_id>/label/<int:id>/delete/', CardLabelDeleteAPIView.as_view(), name='delete_card_label'),
]