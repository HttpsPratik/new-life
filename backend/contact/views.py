from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Feedback
from .serializers import (
    FeedbackListSerializer, FeedbackDetailSerializer, FeedbackCreateSerializer
)
from core.permissions import IsAdminUser
from .utils import send_feedback_confirmation_email


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'status']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]  # Anyone can submit feedback
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            return [IsAdminUser()]  # Only admins can view/update
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FeedbackCreateSerializer
        elif self.action == 'list':
            return FeedbackListSerializer
        return FeedbackDetailSerializer
    
    def perform_create(self, serializer):
        #Set user if authenticated
        
        feedback = None
        if self.request.user.is_authenticated:
            feedback = serializer.save(user=self.request.user, email=self.request.user.email)
        else:
            feedback = serializer.save()
        
        # Send confirmation email
        try:
            send_feedback_confirmation_email(feedback)
        except Exception as e:
            print(f"Failed to send feedback confirmation: {e}")
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-feedback')
    def my_feedback(self, request):
        #Get current user's feedback
        #GET /api/v1/feedback/my-feedback/
        
        feedback = Feedback.objects.filter(user=request.user)
        serializer = FeedbackListSerializer(feedback, many=True, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })