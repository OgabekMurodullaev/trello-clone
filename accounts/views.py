from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializers import UserRegisterSerializer, LoginSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            if user:
                refresh = RefreshToken.for_user(user)
                access = str(refresh.access_token)

                data = {
                    "message": "Siz muvaqqiyatli login qildingiz!",
                    "access": access,
                    "refresh": str(refresh)
                }
                return Response(data=data, status=status.HTTP_200_OK)
            return Response({"data": "Ma'lumotlar noto'g'ri kiritildi"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
