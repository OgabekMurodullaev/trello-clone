from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import serialize

from boards.models import TaskList, Board
from boards.permissions import IsWorkspaceMemberOrOwner, IsOwnerOrReadOnly
from .models import Card, CardMember
from cards.serializers import CardSerializer, AddMemberCardSerializer


class CardListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsWorkspaceMemberOrOwner]
    serializer_class = CardSerializer

    def get(self, request, board_id, list_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request, board)

        list_obj = get_object_or_404(TaskList, id=list_id)
        cards = Card.objects.select_related("list").filter(list=list_obj)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, board_id, list_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request, board)

        list_obj = get_object_or_404(TaskList, id=list_id)

        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsWorkspaceMemberOrOwner]
    serializer_class = CardSerializer

    def get_card(self, card_id):
        return get_object_or_404(Card.objects.select_related("list__board"), id=card_id)

    @extend_schema(operation_id="retrieve_card")
    def get(self, request, card_id):
        card = self.get_card(card_id)
        self.check_object_permissions(request, card.list.board)
        serializer = CardSerializer(card)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(operation_id="put_card")
    def put(self, request, card_id):
        card = self.get_card(card_id)
        self.check_object_permissions(request, card.list.board)
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "detail": "Successfully updated",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(operation_id="patch_card")
    def patch(self, request, card_id):
        card = self.get_card(card_id)
        self.check_object_permissions(request, card.list.board)
        serializer = CardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "detail": "Successfully updated",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(operation_id="delete_card")
    def delete(self, request, card_id):
        card = self.get_card(card_id)
        self.check_object_permissions(request, card.list.board)
        card.delete()
        return Response(data={"detail": "Card deleted"}, status=status.HTTP_204_NO_CONTENT)


class AddCardMemberAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AddMemberCardSerializer

    def get_card(self, card_id):
        return get_object_or_404(Card, id=card_id)

    def post(self, request, card_id):
        card = self.get_card(card_id)
        self.check_object_permissions(request, card.list.board)

        serializer = AddMemberCardSerializer(data=request.data, context={"card": card})
        if serializer.is_valid():
            serializer.save()
            data = {
                "detail": "Foydalanuvchi cardga qo'shildi",
                "data": serializer.data
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCardMemberAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AddMemberCardSerializer

    def delete(self, request, card_id, user_id):
        card_member = get_object_or_404(CardMember, card__id=card_id, user__id=user_id)
        card_member.delete()
        return Response({"detail": "Member o'chirib tashlandi"}, status=status.HTTP_204_NO_CONTENT)