from rest_framework import serializers
from .models import TermsAndConditions, TermsAcceptance


class TermsAndConditionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TermsAndConditions
        fields = (
            'id', 'version', 'content', 'effective_date',
            'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class TermsAcceptanceSerializer(serializers.ModelSerializer):
    
    terms_version = serializers.CharField(source='terms.version', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = TermsAcceptance
        fields = (
            'id', 'user', 'user_email', 'terms', 'terms_version',
            'accepted_at', 'ip_address', 'user_agent'
        )
        read_only_fields = ('id', 'user', 'accepted_at', 'ip_address', 'user_agent')


class AcceptTermsSerializer(serializers.Serializer):
    
    terms_id = serializers.IntegerField(required=True)
    
    def validate_terms_id(self, value):

        try:
            terms = TermsAndConditions.objects.get(id=value, is_active=True)
        except TermsAndConditions.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive terms version.")
        return value