from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, set_rollback

from boards.models import Board, TaskList
from boards.serializers import BoardSerializer, TaskListSerializer
from boards.permissions import IsOwnerOrReadOnly, IsWorkspaceMemberOrOwner
from workspaces.models import  WorkspaceMember


class BoardListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = BoardSerializer

    def get(self, request):
        workspaces = WorkspaceMember.objects.filter(member=request.user, is_active=True).values_list("workspace_id", flat=True)
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


class TasksListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskListSerializer

    def get(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        user = request.user
        if user != board.workspace.owner and user not in board.workspace.members.all():
            return Response({"detail": "Siz bu workspace'ning egasi/a'zosi emas"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskListSerializer(board.lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsWorkspaceMemberOrOwner]
    serializer_class = TaskListSerializer

    def post(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)

        self.check_object_permissions(request, board)

        serializer = TaskListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(board=board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsWorkspaceMemberOrOwner]
    serializer_class = TaskListSerializer

    @extend_schema(operation_id="retrieve_task_list")
    def get(self, request, board_id, list_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request, board)

        t_list = get_object_or_404(TaskList, id=list_id)
        serializer = TaskListSerializer(t_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(operation_id="update_put_task_list")
    def put(self, request, board_id, list_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request, board)

        t_list = get_object_or_404(TaskList, id=list_id)
        serializer = TaskListSerializer(t_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(operation_id="update_patch_task_list")
    def patch(self, request, board_id, list_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request, board)

        t_list = get_object_or_404(TaskList, id=list_id)
        serializer = TaskListSerializer(t_list, data=request.data, partial=True)

    @extend_schema(operation_id="delete_task_list")
    def delete(self, request, board_id, list_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request, board)

        t_list = get_object_or_404(TaskList, id=list_id)
        t_list.delete()
        return Response({"detail": "List o'chirib tashlandi"}, status=status.HTTP_204_NO_CONTENT)