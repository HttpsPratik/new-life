from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Pet, PetImage
from .serializers import (
    PetListSerializer, PetDetailSerializer, PetCreateUpdateSerializer, PetImageSerializer
)
from core.permissions import IsOwnerOrAdmin, HasAcceptedTerms
from .filters import PetFilter
from users.utils import send_pet_listing_confirmation


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.filter(is_active=True).select_related('owner').prefetch_related('images')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PetFilter
    search_fields = ['name', 'breed', 'description', 'location']
    ordering_fields = ['created_at', 'age', 'name']
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
            return PetListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PetCreateUpdateSerializer
        return PetDetailSerializer
    
    def get_queryset(self):
        #Filter queryset based on action
        
        queryset = super().get_queryset()
        
        # For list view, only show available pets by default
        if self.action == 'list':
            status_filter = self.request.query_params.get('status')
            if not status_filter:
                queryset = queryset.filter(status='AVAILABLE')
        
        return queryset
    
    def perform_create(self, serializer):
        #Set owner when creating pet
        
        pet = serializer.save(
            owner=self.request.user,
            contact_phone=self.request.user.phone_number,
            contact_email=self.request.user.email
        )
        
        # Send confirmation email
        try:
            send_pet_listing_confirmation(self.request.user, pet)
        except Exception as e:
            print(f"Failed to send pet listing confirmation: {e}")
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-listings')
    def my_listings(self, request):
        #Get current user's pet listings
        #GET /api/v1/pets/my-listings/
       
        pets = Pet.objects.filter(owner=request.user).select_related('owner').prefetch_related('images')
        serializer = PetListSerializer(pets, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOwnerOrAdmin])
    def mark_adopted(self, request, pk=None):
        #Mark pet as adopted
        #POST /api/v1/pets/{id}/mark-adopted/
        
        pet = self.get_object()
        pet.mark_as_adopted()
        
        return Response({
            'success': True,
            'message': 'Pet marked as adopted',
            'data': PetDetailSerializer(pet, context={'request': request}).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOwnerOrAdmin], url_path='upload-images')
    def upload_images(self, request, pk=None):
        #Upload additional images to pet
        #POST /api/v1/pets/{id}/upload-images/
        
        pet = self.get_object()
        images = request.FILES.getlist('images')
        
        if not images:
            return Response({
                'success': False,
                'error': 'No images provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check total images count
        current_count = pet.images.count()
        if current_count + len(images) > 5:
            return Response({
                'success': False,
                'error': f'Maximum 5 images allowed. Current: {current_count}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create images
        created_images = []
        for image in images:
            pet_image = PetImage.objects.create(pet=pet, image=image)
            created_images.append(pet_image)
        
        serializer = PetImageSerializer(created_images, many=True, context={'request': request})
        return Response({
            'success': True,
            'message': f'{len(created_images)} image(s) uploaded',
            'data': serializer.data
        })
    
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated, IsOwnerOrAdmin], url_path='images/(?P<image_id>[^/.]+)')
    def delete_image(self, request, pk=None, image_id=None):
        #Delete a pet image
        #DELETE /api/v1/pets/{id}/images/{image_id}/
       
        pet = self.get_object()
        
        try:
            image = PetImage.objects.get(id=image_id, pet=pet)
            
            # Don't allow deleting last image
            if pet.images.count() <= 1:
                return Response({
                    'success': False,
                    'error': 'Cannot delete the last image'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            image.delete()
            
            return Response({
                'success': True,
                'message': 'Image deleted successfully'
            })
        except PetImage.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Image not found'
            }, status=status.HTTP_404_NOT_FOUND)