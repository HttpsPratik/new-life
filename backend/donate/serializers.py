from rest_framework import serializers
from .models import Donation
from users.serializers import UserSerializer


class DonationListSerializer(serializers.ModelSerializer):
    
    donor_display = serializers.SerializerMethodField()
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Donation
        fields = (
            'id', 'donor_display', 'amount', 'currency',
            'payment_method', 'payment_method_display',
            'payment_status', 'payment_status_display',
            'created_at'
        )
        read_only_fields = ('id', 'created_at')
    
    def get_donor_display(self, obj):
        """Get donor name respecting anonymity"""
        return obj.get_donor_display_name()


class DonationDetailSerializer(serializers.ModelSerializer):
    
    donor_display = serializers.SerializerMethodField()
    donor_info = UserSerializer(source='donor', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    
    class Meta:
        model = Donation
        fields = (
            'id', 'donor', 'donor_info', 'donor_display', 'donor_name',
            'donor_email', 'donor_phone', 'amount', 'currency', 'currency_display',
            'payment_method', 'payment_method_display', 'payment_reference',
            'payment_status', 'payment_status_display', 'message',
            'is_anonymous', 'created_at', 'updated_at', 'completed_at'
        )
        read_only_fields = (
            'id', 'donor', 'payment_reference', 'payment_status',
            'created_at', 'updated_at', 'completed_at'
        )
    
    def get_donor_display(self, obj):
        return obj.get_donor_display_name()


class DonationCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Donation
        fields = (
            'donor_name', 'donor_email', 'donor_phone',
            'amount', 'currency', 'payment_method',
            'message', 'is_anonymous'
        )
    
    def validate_amount(self, value):
        if value < 100:
            raise serializers.ValidationError("Minimum donation amount is 100.")
        if value > 1000000:
            raise serializers.ValidationError("Maximum donation amount is 1,000,000.")
        return value