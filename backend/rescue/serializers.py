from rest_framework import serializers
from .models import RescueContact


class RescueContactListSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = RescueContact
        fields = (
            'id', 'name', 'type', 'type_display', 'city',
            'phone', 'email', 'is_verified', 'emergency_service'
        )
        read_only_fields = ('id',)


class RescueContactDetailSerializer(serializers.ModelSerializer):
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = RescueContact
        fields = (
            'id', 'name', 'type', 'type_display', 'address', 'city',
            'phone', 'email', 'website', 'description', 'operating_hours',
            'capacity', 'specialization', 'services', 'emergency_service',
            'is_verified', 'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')