from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cards.models import Card
from cards.permissions import IsOwnerOrCardMember
from .models import Label, CardLabel
from .serializers import LabelSerializer, CardLabelSerializer


class LabelListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class LabelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    lookup_field = "id"


class CardLabelCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrCardMember]
    serializer_class = CardLabelSerializer

    def post(self, request, card_id):
        card = get_object_or_404(Card, id=card_id)
        self.check_object_permissions(request, card)
        serializer = CardLabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardLabelDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrCardMember]

    def delete(self, request, card_id, id):
        card = get_object_or_404(Card, id=card_id)
        self.check_object_permissions(request, card)
        try:
            card_label = CardLabel.objects.get(id=id, card=card)
        except CardLabel.DoesNotExist:
            return Response({'detail': 'CardLabel found'}, status=status.HTTP_404_NOT_FOUND)

        card_label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)