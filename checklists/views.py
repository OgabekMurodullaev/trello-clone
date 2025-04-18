from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from checklists.models import CheckList, CheckListItem
from checklists.permissions import IsCardMemberOrWorkspaceOwner
from checklists.serializers import CheckListSerializer, CheckListItemSerializer


class CheckListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CheckListSerializer

    def get(self, request):
        card_id = request.query_params.get('card')
        queryset = CheckList.objects.all()
        if card_id:
            queryset = queryset.filter(card_id=card_id)
        serializer = CheckListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CheckListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckListDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCardMemberOrWorkspaceOwner]

    def get_object(self, list_id):
        try:
            return CheckList.objects.get(id=list_id)
        except CheckList.DoesNotExist:
            return None

    def get(self, request, list_id):
        checklist = self.get_object(list_id)
        if not checklist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, checklist)
        serializer = CheckListSerializer(checklist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, list_id):
        checklist = self.get_object(list_id)
        if not checklist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, checklist)
        serializer = CheckListSerializer(checklist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, list_id):
        checklist = self.get_object(list_id)
        if not checklist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, checklist)
        serializer = CheckListSerializer(checklist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, list_id):
        checklist = self.get_object(list_id)
        if not checklist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, checklist)
        checklist.delete()
        return Response({'detail': 'Checklist deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class CheckListItemListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCardMemberOrWorkspaceOwner]
    serializer_class = CheckListItemSerializer

    def get(self, request, checklist_id):
        items = CheckListItem.objects.filter(checklist_id=checklist_id)
        serializer = CheckListItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, checklist_id):
        serializer = CheckListItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckListItemDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCardMemberOrWorkspaceOwner]
    serializer_class = CheckListItemSerializer

    def get_object(self, checklist_id, item_id):
        try:
            return CheckListItem.objects.get(checklist_id=checklist_id, id=item_id)
        except CheckListItem.DoesNotExist:
            return None

    def get(self, request, checklist_id, item_id):
        checklist = CheckList.objects.get(id=checklist_id)
        item = self.get_object(checklist_id, item_id)
        if not item:
            return Response({'detail': 'Not found'}, status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request, checklist)
        serializer = CheckListItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, checklist_id, item_id):
        checklist = CheckList.objects.get(id=checklist_id)
        self.check_object_permissions(request, checklist)
        item = self.get_object(checklist_id, item_id)
        if not item:
            return Response({'detail': 'Not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CheckListItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, checklist_id, item_id):
        checklist = CheckList.objects.get(id=checklist_id)
        self.check_object_permissions(request, checklist)
        item = self.get_object(checklist_id, item_id)
        if not item:
            return Response({'detail': 'Not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CheckListItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, checklist_id, item_id):
        checklist = CheckList.objects.get(id=checklist_id)
        self.check_object_permissions(request, checklist)
        item = self.get_object(checklist_id, item_id)
        item.delete()
        return Response({'detail': 'Successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
