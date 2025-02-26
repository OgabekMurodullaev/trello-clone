from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet

router = DefaultRouter()
router.register(r'', BoardViewSet, basename="board")

urlpatterns = [
    path('', include(router.urls)),
]