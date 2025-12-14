from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet

router = DefaultRouter()
router.register('', PetViewSet, basename='pets')

urlpatterns = [
    path('', include(router.urls)),
]

"""

This creates:

GET    /                       (list)
POST   /                       (create)
GET    /{id}/                  (detail)
PUT    /{id}/                  (update)
PATCH  /{id}/                  (partial update)
DELETE /{id}/                  (delete)
GET    /my-listings/           (custom action)
POST   /{id}/mark-adopted/     (custom action)
POST   /{id}/upload-images/    (custom action)
"""