from django.urls import path

from cards.views import CardListCreateAPIView, CardDetailAPIView

urlpatterns = [
    path('<int:board_id>/<int:list_id>/cards', CardListCreateAPIView.as_view(), name="cards_list"),
    path('<int:card_id>', CardDetailAPIView.as_view(), name="retrieve_update_delete"),
]