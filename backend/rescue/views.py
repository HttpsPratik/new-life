from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import RescueContact
from .serializers import RescueContactListSerializer, RescueContactDetailSerializer
from .filters import RescueContactFilter

class RescueContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RescueContact.objects.filter(is_active=True)
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RescueContactFilter
    search_fields = ['name', 'city', 'address', 'description', 'services']
    ordering_fields = ['name', 'city', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RescueContactListSerializer
        return RescueContactDetailSerializer
    
    def get_queryset(self):
        #Filter queryset - optionally filter by type in URL
        
        queryset = super().get_queryset()
        
        # Filter by type if specified in path
        contact_type = self.request.query_params.get('type')
        if contact_type:
            queryset = queryset.filter(type=contact_type.upper())
        
        return queryset