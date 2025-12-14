from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MissingPetViewSet

router = DefaultRouter()
router.register('', MissingPetViewSet, basename='missing-pets')

urlpatterns = [
    path('', include(router.urls)),
]