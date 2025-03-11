from django.urls import path

from cards.views import CardListCreateAPIView, CardDetailAPIView, AddCardMemberAPIView, RemoveCardMemberAPIView

urlpatterns = [
    path('<int:board_id>/<int:list_id>/cards', CardListCreateAPIView.as_view(), name="cards_list"),
    path('<int:card_id>', CardDetailAPIView.as_view(), name="retrieve_update_delete"),
    path('<int:card_id>/members/add/', AddCardMemberAPIView.as_view(), name="add_member_to_card"),
    path('<int:card_id>/members/<int:user_id>/remove/', RemoveCardMemberAPIView.as_view(), name="remove_member_from_card")
]