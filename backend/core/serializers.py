
#Core serializers with reusable base classes

from rest_framework import serializers


class TimestampedSerializer(serializers.ModelSerializer):
    #Base serializer with timestamp fields
    
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)