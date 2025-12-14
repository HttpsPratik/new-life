from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Donation
from .serializers import (
    DonationListSerializer, DonationDetailSerializer, DonationCreateSerializer
)
from core.permissions import IsOwnerOrAdmin
from .utils import send_donation_confirmation_email


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_status', 'payment_method', 'currency']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]  # Anyone can donate
        elif self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser()]  # Only admins can view all
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DonationCreateSerializer
        elif self.action == 'list':
            return DonationListSerializer
        return DonationDetailSerializer
    
    def perform_create(self, serializer):
        #Set donor if authenticated
      
        if self.request.user.is_authenticated:
            serializer.save(donor=self.request.user)
        else:
            serializer.save()
    
    @action(detail=False, methods=['post'], url_path='initiate')
    def initiate(self, request):
        #Initiate donation process
        #POST /api/v1/donations/initiate/
        
        serializer = DonationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set donor if authenticated
        if request.user.is_authenticated:
            donation = serializer.save(donor=request.user)
        else:
            donation = serializer.save()
        
        # TODO: Generate payment gateway URL based on payment method
        payment_url = None
        if donation.payment_method == 'ESEWA':
            # Generate eSewa payment URL
            pass
        elif donation.payment_method == 'PAYPAL':
            # Generate PayPal payment URL
            pass
        
        # Send donation confirmation email
        try:
            send_donation_confirmation_email(donation)
        except Exception as e:
            print(f"Failed to send donation confirmation: {e}")
        
        return Response({
            'success': True,
            'message': 'Donation initiated',
            'data': {
                'donation_id': str(donation.id),
                'payment_url': payment_url,
                'payment_method': donation.payment_method
            }
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-donations')
    def my_donations(self, request):
        #Get current user's donations
        #GET /api/v1/donations/my-donations/
        
        donations = Donation.objects.filter(donor=request.user)
        serializer = DonationListSerializer(donations, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })