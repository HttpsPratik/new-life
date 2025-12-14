from rest_framework import serializers
from .models import Feedback
from users.serializers import UserSerializer


class FeedbackListSerializer(serializers.ModelSerializer):
    
    sender_display = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Feedback
        fields = (
            'id', 'sender_display', 'subject', 'type', 'type_display',
            'status', 'status_display', 'created_at'
        )
        read_only_fields = ('id', 'created_at')
    
    def get_sender_display(self, obj):
        return obj.get_sender_display()


class FeedbackDetailSerializer(serializers.ModelSerializer):
    
    sender_info = UserSerializer(source='user', read_only=True)
    sender_display = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Feedback
        fields = (
            'id', 'user', 'sender_info', 'sender_display', 'name',
            'email', 'subject', 'type', 'type_display', 'message',
            'status', 'status_display', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'status', 'created_at', 'updated_at')
    
    def get_sender_display(self, obj):
        return obj.get_sender_display()


class FeedbackCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback
        fields = ('name', 'email', 'subject', 'type', 'message')
    
    def validate(self, attrs):
        request = self.context.get('request')
        if not request.user.is_authenticated and not attrs.get('name'):
            raise serializers.ValidationError({
                'name': 'Name is required for non-authenticated users.'
            })
        return attrs