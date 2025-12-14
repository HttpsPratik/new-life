from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TermsViewSet

router = DefaultRouter()
router.register('', TermsViewSet, basename='terms')

urlpatterns = [
    path('', include(router.urls)),
]
""" 

This creates:

GET    /                   (list all versions)
GET    /{id}/              (specific version)
GET    /current/           (custom action)
POST   /accept/            (custom action)
GET    /my-acceptance/     (custom action)

"""