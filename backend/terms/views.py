from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TermsAndConditions, TermsAcceptance
from .serializers import (
    TermsAndConditionsSerializer, TermsAcceptanceSerializer, AcceptTermsSerializer
)


class TermsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'], url_path='current')
    def current(self, request):
        #Get current active Terms and Conditions
        #GET /api/v1/terms/current/
        
        try:
            terms = TermsAndConditions.objects.get(is_active=True)
            serializer = self.get_serializer(terms)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except TermsAndConditions.DoesNotExist:
            return Response({
                'success': False,
                'error': 'No active terms found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request):
        #Accept current Terms and Conditions
        #POST /api/v1/terms/accept/
        
        serializer = AcceptTermsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        terms_id = serializer.validated_data['terms_id']
        terms = TermsAndConditions.objects.get(id=terms_id)
        
        # Get IP address and user agent
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Check if already accepted
        if TermsAcceptance.objects.filter(user=request.user, terms=terms).exists():
            return Response({
                'success': False,
                'error': 'You have already accepted this version'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create acceptance record
        acceptance = TermsAcceptance.objects.create(
            user=request.user,
            terms=terms,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Update user model
        request.user.accept_terms(terms.version)
        
        return Response({
            'success': True,
            'message': 'Terms accepted successfully',
            'data': TermsAcceptanceSerializer(acceptance).data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-acceptance')
    def my_acceptance(self, request):
        #Get user's terms acceptance history
        #GET /api/v1/terms/my-acceptance/
        
        acceptances = TermsAcceptance.objects.filter(user=request.user)
        serializer = TermsAcceptanceSerializer(acceptances, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def get_client_ip(self, request):
        #Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip