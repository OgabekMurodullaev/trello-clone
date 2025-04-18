from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from boards.models import TaskList, Board
from boards.permissions import IsWorkspaceMemberOrOwner, IsOwnerOrReadOnly
from .models import Card, CardMember, Attachment
from cards.serializers import CardSerializer, AddMemberCardSerializer, AttachmentSerializer
from .permissions import IsOwnerOrCardMember, CanDeleteAttachment


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


class AttachmentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrCardMember]
    serializer_class = AttachmentSerializer

    def get(self, request, card_id):
        card = get_object_or_404(Card, id=card_id)
        self.check_object_permissions(request, card)
        attachments = Attachment.objects.filter(card_id=card_id)
        serializer = AttachmentSerializer(attachments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, card_id):
        serializer = AttachmentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(card_id=self.kwargs["card_id"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttachmentDetailAPIView(APIView):
    permission_classes = [CanDeleteAttachment]
    serializer_class = AttachmentSerializer

    def get_object(self, card_id, attachment_id):
        return get_object_or_404(Attachment, card_id=card_id, id=attachment_id)

    def get(self, request, card_id, attachment_id):
        attachment = self.get_object(card_id, attachment_id)
        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, card_id, attachment_id):
        attachment = self.get_object(card_id, attachment_id)
        self.check_object_permissions(request, attachment)
        attachment.delete()
        return Response(data={"detail": "Attachment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


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