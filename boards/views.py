from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from yaml import serialize

from boards.models import Board, List
from boards.serializers import BoardSerializer
from boards.permissions import IsOwnerOrReadOnly
from workspaces.models import WorkspaceMember, Workspace


class BoardListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = BoardSerializer

    def get(self, request):
        workspaces = Workspace.objects.filter(member=request.user, is_active=True).values_list("workspace_id", flat=True)
        boards = Board.objects.filter(workspace_id__in=workspaces).select_related("workspace")
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BoardSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BoardDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer

    def get_object(self, board_id):
        return get_object_or_404(Board, id=board_id)

    @extend_schema(operation_id="retrieve_board")
    def get(self, request, board_id):
        board = self.get_object(board_id)
        serializer = BoardSerializer(board, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(operation_id="update_board")
    def put(self, request, board_id):
        board = self.get_object(board_id)
        serializer = BoardSerializer(board, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(operation_id="update_patch_board")
    def patch(self, request, board_id):
        board = self.get_object(board_id)
        serializer = BoardSerializer(board, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(operation_id="delete_board")
    def delete(self, request, board_id):
        board = self.get_object(board_id)

        if board.workspace.owner != request.user:
            return Response({"detail": "Siz bu huquqga ega emassiz"}, status=status.HTTP_403_FORBIDDEN)

        board.delete()
        return Response({"detail": "Board o'chirildi!"}, status=status.HTTP_204_NO_CONTENT)