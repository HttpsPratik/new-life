from rest_framework import serializers
from .models import Pet, PetImage
from users.serializers import UserSerializer


class PetImageSerializer(serializers.ModelSerializer):
    """Serializer for pet images"""
    
    class Meta:
        model = PetImage
        fields = ('id', 'image', 'is_primary', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at')


class PetListSerializer(serializers.ModelSerializer):
    """Serializer for pet list view (minimal data)"""
    
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Pet
        fields = (
            'id', 'name', 'category', 'category_display', 'breed',
            'age', 'gender', 'size', 'location', 'status',
            'primary_image', 'owner_name', 'created_at'
        )
        read_only_fields = ('id', 'created_at')
    
    def get_primary_image(self, obj):
        """Get primary image URL"""
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            request = self.context.get('request')
            return request.build_absolute_uri(primary.image.url) if request else primary.image.url
        return None


class PetDetailSerializer(serializers.ModelSerializer):
    """Serializer for pet detail view (full data)"""
    
    owner = UserSerializer(read_only=True)
    images = PetImageSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    size_display = serializers.CharField(source='get_size_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Pet
        fields = (
            'id', 'owner', 'name', 'category', 'category_display',
            'breed', 'age', 'gender', 'gender_display', 'size', 'size_display',
            'description', 'health_info', 'location', 'contact_phone',
            'contact_email', 'status', 'status_display', 'is_active',
            'images', 'created_at', 'updated_at', 'adoption_date'
        )
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at', 'adoption_date')


class PetCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating pets"""
    
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        allow_empty=True,
        max_length=5  # Maximum 5 images
    )
    
    class Meta:
        model = Pet
        fields = (
            'name', 'category', 'breed', 'age', 'gender', 'size',
            'description', 'health_info', 'location', 'contact_phone',
            'contact_email', 'images'
        )
    
    def validate_age(self, value):
        """Validate age is reasonable"""
        if value < 0:
            raise serializers.ValidationError("Age cannot be negative.")
        if value > 300:  # 25 years
            raise serializers.ValidationError("Age seems unrealistic.")
        return value
    
    def validate_images(self, value):
        """Validate images"""
        if len(value) > 5:
            raise serializers.ValidationError("Maximum 5 images allowed.")
        
        for image in value:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise serializers.ValidationError("Image size must be less than 5MB.")
        
        return value
    
    def create(self, validated_data):
        """Create pet with images"""
        images_data = validated_data.pop('images', [])
        pet = Pet.objects.create(**validated_data)
        
        # Create images
        for index, image in enumerate(images_data):
            PetImage.objects.create(
                pet=pet,
                image=image,
                is_primary=(index == 0)  # First image is primary
            )
        
        return pet
    
    def update(self, instance, validated_data):
        #Update pet (images handled separately)
        validated_data.pop('images', None)  # Don't update images here
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance