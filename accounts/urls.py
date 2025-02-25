from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import UserCreateView, UserLoginAPIView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]