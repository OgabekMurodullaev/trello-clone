from django.urls import path

from accounts.views import UserCreateView, UserLoginAPIView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
]