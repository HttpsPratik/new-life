from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import MissingPet, MissingPetImage
from .serializers import (
    MissingPetListSerializer, MissingPetDetailSerializer,
    MissingPetCreateUpdateSerializer, MissingPetImageSerializer
)
from core.permissions import IsOwnerOrAdmin, HasAcceptedTerms
from .filters import MissingPetFilter
from users.utils import send_missing_pet_confirmation


class MissingPetViewSet(viewsets.ModelViewSet):
    queryset = MissingPet.objects.filter(is_active=True).select_related('reporter').prefetch_related('images')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MissingPetFilter
    search_fields = ['name', 'breed', 'description', 'last_seen_location']
    ordering_fields = ['created_at', 'last_seen_date']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated(), HasAcceptedTerms()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MissingPetListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MissingPetCreateUpdateSerializer
        return MissingPetDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # For list view, only show missing pets by default
        if self.action == 'list':
            status_filter = self.request.query_params.get('status')
            if not status_filter:
                queryset = queryset.filter(status='MISSING')
        
        return queryset
    
    def perform_create(self, serializer):
        #Set reporter when creating missing pet report
        
        missing_pet = serializer.save(
            reporter=self.request.user,
            contact_phone=self.request.user.phone_number,
            contact_email=self.request.user.email
        )
        
        # Send confirmation email
        try:
            send_missing_pet_confirmation(self.request.user, missing_pet)
        except Exception as e:
            print(f"Failed to send missing pet confirmation: {e}")
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-reports')
    def my_reports(self, request):
        #Get current user's missing pet reports
        #GET /api/v1/missing-pets/my-reports/
        
        reports = MissingPet.objects.filter(reporter=request.user).select_related('reporter').prefetch_related('images')
        serializer = MissingPetListSerializer(reports, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOwnerOrAdmin])
    def mark_found(self, request, pk=None):
        #Mark pet as found
        #POST /api/v1/missing-pets/{id}/mark-found/
       
        missing_pet = self.get_object()
        missing_pet.mark_as_found()
        
        return Response({
            'success': True,
            'message': 'Pet marked as found',
            'data': MissingPetDetailSerializer(missing_pet, context={'request': request}).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOwnerOrAdmin], url_path='upload-images')
    def upload_images(self, request, pk=None):
        #Upload additional images
        #POST /api/v1/missing-pets/{id}/upload-images/
        
        missing_pet = self.get_object()
        images = request.FILES.getlist('images')
        
        if not images:
            return Response({
                'success': False,
                'error': 'No images provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        current_count = missing_pet.images.count()
        if current_count + len(images) > 5:
            return Response({
                'success': False,
                'error': f'Maximum 5 images allowed. Current: {current_count}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        created_images = []
        for image in images:
            pet_image = MissingPetImage.objects.create(missing_pet=missing_pet, image=image)
            created_images.append(pet_image)
        
        serializer = MissingPetImageSerializer(created_images, many=True, context={'request': request})
        return Response({
            'success': True,
            'message': f'{len(created_images)} image(s) uploaded',
            'data': serializer.data
        })