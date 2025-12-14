from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RescueContactViewSet

router = DefaultRouter()
router.register('', RescueContactViewSet, basename='rescue')

urlpatterns = [
    path('', include(router.urls)),
]